---
description: Bootstrap GitOps stack (ArgoCD, ESO, Longhorn) onto existing Talos cluster
allowed-tools: Bash(kubectl:*), Bash(helm:*), Bash(sleep:*), mcp__plugin_omni-scale_kubernetes__*, AskUserQuestion
---

# GitOps Bootstrap

Deploy the GitOps stack onto an existing talos-prod-01 cluster.

**NOTE:** This command encodes the full bootstrap sequence to avoid chicken-and-egg
issues discovered during DR drills. Do not simplify or reorder phases.

## Pre-flight Gate

**STOP** if omni-talos skill is not loaded.

Check: Do you have knowledge of `provider-ctl.py` and the provider operations table?
If not, instruct user:

```text
Required setup not complete. Run this chain first:
  /omni-scale:omni-prime && /omni-scale:status && /omni-scale:omni-talos
Then re-run /omni-scale:bootstrap-gitops
```

## Instructions

### Phase 1: Create Bootstrap Secret

**Outcome:** `external-secrets` namespace exists with `universal-auth-credentials`
secret containing Infisical credentials.

Create namespace `external-secrets` and secret using kubectl. Secret requires:

- `$INFISICAL_UNIVERSAL_AUTH_CLIENT_ID`
- `$INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET`

If env vars not set, stop and inform user with exact var names needed.

### Phase 2: Install Cilium (CNI)

**Outcome:** Cilium installed, all nodes become Ready.

**Why first:** GitOps-managed CNI creates scheduling deadlock. Nodes stay NotReady
without CNI, pods can't schedule, ArgoCD can't deploy CNI. Break cycle with manual
Cilium install.

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update cilium
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set ipam.mode=kubernetes \
  --set kubeProxyReplacement=false
```

**Poll:** `kubectl get nodes` — wait for all nodes Ready.
<!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 5 min
- On timeout: Check Cilium pods in kube-system

### Phase 3: Label Privileged Namespaces

**Outcome:** Namespaces created and labeled for privileged workloads.

Kubernetes 1.35+ blocks privileged pods by default. Label namespaces before
deploying storage/monitoring:

```bash
kubectl create namespace longhorn-system --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace netdata --dry-run=client -o yaml | kubectl apply -f -

kubectl label namespace longhorn-system \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/enforce-version=latest --overwrite

kubectl label namespace netdata \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/enforce-version=latest --overwrite
```

### Phase 4: Install ESO Operator

**Outcome:** External Secrets Operator running, CRDs available.

**Why before ArgoCD:** ESO app contains ClusterSecretStore CRs. CRDs must exist
before ArgoCD tries to sync them.

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo update external-secrets
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --set installCRDs=true
```

**Poll:** ESO pods Running in external-secrets namespace.
<!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 3 min

### Phase 5: Install Longhorn

**Outcome:** Longhorn installed, storage available.

**Why `--no-hooks`:** Longhorn pre-upgrade hook requires ServiceAccount that the
chart creates. Hook deadlocks on fresh install.

```bash
helm repo add longhorn https://charts.longhorn.io
helm repo update longhorn
helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --no-hooks
```

**Poll:** Longhorn manager pods Running (DaemonSet).
<!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 5 min
- After 3 attempts, increase interval to 60s

### Phase 6: Install ArgoCD via Helm

**Outcome:** ArgoCD running with consistent labels/ports.

**Why Helm:** Raw manifests have NetworkPolicy, label, and port naming issues that
require runtime patches. Helm chart is consistent out of the box.

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set configs.params."server\.insecure"=true \
  --set server.service.type=ClusterIP \
  --set global.networkPolicy.create=false
```

**Poll:** ArgoCD pods Running in argocd namespace.
<!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 5 min

### Phase 7: Apply App-of-Apps Bootstrap

**Outcome:** App of Apps deployed from mothership-gitops bootstrap manifest.

```bash
kubectl apply -f https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml
```

### Phase 8: Monitor Sync Waves

**Outcome:** All apps (except argocd-ha) show Synced/Healthy.

**Poll:** Check ArgoCD applications in argocd namespace.
<!-- REQUIRED: sleep 30s between attempts -->

Expected wave order:

- Wave 0-1: Networking (if managed)
- Wave 2: Secrets (ESO + ClusterSecretStores)
- Wave 3-4: Storage (Longhorn)
- Wave 5: Platform services (Tailscale, Netdata)
- Wave 99: ArgoCD HA (manual sync)

Polling rules:

- Max wait: 20 min
- After 3 attempts, increase interval to 60s
- On timeout: consult `references/gitops-bootstrap-issues.md`

If apps show stale errors after fixes, restart ArgoCD application controller:

```bash
kubectl rollout restart statefulset argocd-application-controller -n argocd
```

### Phase 9: ArgoCD HA Upgrade (Manual)

**Outcome:** ArgoCD HA running.

After Longhorn healthy, instruct user to manually sync `argocd-ha` via ArgoCD UI
(Tailscale). This is intentionally manual as safety gate.

Bootstrap complete when all ArgoCD apps show Synced/Healthy.

## Troubleshooting

See `references/gitops-bootstrap-issues.md` for common issues:

- CNI chicken-and-egg
- ESO CRD ordering
- PodSecurity violations
- Helm hook deadlocks
- ArgoCD error caching
