# GitOps Bootstrap Issues

Common issues discovered during DR drills and fresh cluster bootstraps.

> **Source:** DR drill 2026-01-14, documented in `docs/plugin-development-learnings-2026-01-12.md`

## CNI Chicken-and-Egg

### Problem

GitOps-managed CNI creates a scheduling deadlock:

1. bootstrap.yaml contains ArgoCD Application CRs → requires ArgoCD CRDs
2. ArgoCD pods need CNI to schedule → nodes NotReady without CNI
3. CNI (Cilium) managed by ArgoCD → can't deploy without ArgoCD running
4. Deadlock

### Solution

Install Cilium via Helm BEFORE ArgoCD:

```bash
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set ipam.mode=kubernetes \
  --set kubeProxyReplacement=false
```

Wait for nodes to show Ready, then proceed with ArgoCD install.

---

## ESO CRD Ordering

### Problem

External Secrets app contains ClusterSecretStore custom resources. ArgoCD tries
to sync them before ESO operator is installed, failing with "resource not found".

### Solution

Install ESO operator via Helm BEFORE applying app-of-apps:

```bash
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --set installCRDs=true
```

---

## PodSecurity Violations (Kubernetes 1.35+)

### Problem

Kubernetes 1.35 has stricter PodSecurity defaults. Privileged workloads (Longhorn,
Netdata) fail to schedule with no obvious error.

**Symptom:** DaemonSet shows `DESIRED: 3, READY: 0`, pods don't appear.

### Solution

Label namespaces BEFORE deploying privileged workloads:

```bash
kubectl label namespace longhorn-system \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/enforce-version=latest

kubectl label namespace netdata \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/enforce-version=latest
```

### Affected Namespaces

| Namespace | Workload | Why Privileged |
|-----------|----------|----------------|
| longhorn-system | Longhorn | Storage requires host access |
| netdata | Netdata | Host metrics collection |
| Any with DaemonSets | Various | Host networking/volumes |

---

## Helm Pre-Install Hook Deadlock

### Problem

Helm charts with pre-install/pre-upgrade hooks that depend on chart-created
resources deadlock on fresh install.

**Example:** Longhorn pre-upgrade job requires ServiceAccount that the chart creates.

**Symptom:** Job stuck in Pending, sync never completes.

### Solution

Install with `--no-hooks` on fresh clusters:

```bash
helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --no-hooks
```

Subsequent upgrades can use hooks normally.

### Known Charts with This Issue

- Longhorn (pre-upgrade hook)
- Charts with admission webhook pre-flight checks

---

## ArgoCD Raw Manifest Issues

### Problem

Default ArgoCD manifests (`argoproj/argo-cd/stable/manifests/install.yaml`) have
multiple issues on fresh clusters.

### Issue 1: NetworkPolicy Blocking

**Symptom:** Apps stuck in Unknown/OutOfSync, logs show "connection error: operation
not permitted"

**Cause:** Default manifests include restrictive NetworkPolicies.

**Fix:**

```bash
kubectl delete networkpolicy --all -n argocd
```

### Issue 2: Label Mismatch (Endpoint Resolution)

**Symptom:** `kubectl get endpoints argocd-repo-server` shows `<none>`

**Cause:** Service expects `app.kubernetes.io/instance: argocd`, pod missing it.

**Fix:**

```bash
kubectl patch deployment argocd-repo-server -n argocd --type='json' \
  -p='[{"op": "add", "path": "/spec/template/metadata/labels/app.kubernetes.io~1instance", "value": "argocd"}]'
```

### Issue 3: Port Naming Mismatch (EndpointSlice)

**Symptom:** EndpointSlice shows `ports: null`, connections fail.

**Cause:** Container port unnamed, service expects named port.

**Fix:**

```bash
kubectl patch deployment argocd-repo-server -n argocd --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/ports/0/name", "value": "tcp-repo-server"}]'
```

### Recommended Solution

Use Helm chart instead of raw manifests:

```bash
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set global.networkPolicy.create=false
```

---

## Stale ArgoCD Error Cache

### Problem

ArgoCD caches operation errors. After fixing underlying issues (network, CRDs),
apps still show old errors.

**Symptom:** Network fixed, but apps show "connection error" from before the fix.

### Solution

Restart application controller to clear cache:

```bash
kubectl rollout restart statefulset argocd-application-controller -n argocd
```

Or clear specific app's operation state:

```bash
kubectl patch application <app> -n argocd --type merge \
  -p '{"status":{"operationState":null}}'
```

---

## ArgoCD Selector Immutability (Manual → Helm Migration)

### Problem

Transitioning from manual ArgoCD install to helm-managed fails because Kubernetes
forbids changing deployment selectors.

**Symptom:** ArgoCD app sync fails with "field is immutable" errors.

### Solution

Delete ArgoCD resources before letting helm take over:

```bash
kubectl delete deployment -n argocd --all
kubectl delete statefulset -n argocd --all
# Then sync argocd app
```

**Risk:** ArgoCD briefly unavailable during recreation.

**Better approach:** Start with Helm from the beginning on fresh clusters.

---

## MCP vs CLI Kubeconfig Contexts

### Problem

MCP kubernetes tools use a separate kubeconfig with dedicated service account.
Context names don't match local kubectl.

**Symptom:** MCP tools work, but CLI fallback fails with "context not found".

### Context Mapping

| Tool | Context Name |
|------|--------------|
| MCP kubernetes | `omni-talos-prod-01-kubeconfig-mcp-sa` |
| Local kubectl | `omni-talos-prod-01` |

### Solution

When falling back from MCP to CLI, use the correct context:

```bash
kubectl --context omni-talos-prod-01 get pods
```

---

## External State Cleanup (Post-DR)

### Problem

External services retain state from old cluster that conflicts with new deployment.

### Tailscale Dashboard

**Issue:** Old devices (e.g., `talos-prod-operator`) persist. New operator registers
as `talos-prod-operator-1`.

**Fix:** Remove old devices from Tailscale admin console BEFORE deploying Tailscale
operator.

### Omni Service Accounts

**Issue:** Service account tokens contain old cluster UUID. Tokens invalid after
cluster recreation.

**Fix:** Delete and recreate service accounts after DR:

```bash
omnictl serviceaccount delete freelens-sa
omnictl serviceaccount create freelens-sa --role=<role> --use-user-role
```

---

## Bootstrap Sequence Summary

Correct order to avoid all above issues:

```text
1. Create bootstrap secret (Infisical creds)
2. Install Cilium via Helm (breaks CNI deadlock)
3. Wait for nodes Ready
4. Label privileged namespaces (longhorn-system, netdata)
5. Install ESO operator via Helm (creates CRDs)
6. Install Longhorn via Helm --no-hooks
7. Install ArgoCD via Helm (not raw manifests)
8. Apply app-of-apps bootstrap
9. Poll for Synced/Healthy
10. Manual: Sync argocd-ha via UI
```

This sequence is encoded in `/omni-scale:bootstrap-gitops`.
