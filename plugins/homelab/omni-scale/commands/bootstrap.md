---
description: Guide through GitOps bootstrap procedure for talos-prod-01
allowed-tools: Bash, Read, AskUserQuestion, mcp__kubernetes__*
argument-hint: "[infisical-client-id] [infisical-client-secret]"
---

# Bootstrap Procedure

Step-by-step guide for bootstrapping the GitOps stack on talos-prod-01.

**Note:** This is a WIP command that will be refined as bootstrap procedures evolve.

## Prerequisites

Before starting:

1. **Cluster operational** - Verify with `/omni-scale:status`
2. **kubectl access** - `kubectl get nodes` works
3. **Infisical credentials** - Client ID and secret for universal-auth

## Instructions

### Phase 1: Verify Cluster Ready

```bash
kubectl get nodes
```

All nodes should show `Ready`. If not, stop and troubleshoot.

### Phase 2: Create Bootstrap Secret

The one manual secret for Infisical authentication:

```bash
kubectl create namespace external-secrets

kubectl create secret generic universal-auth-credentials \
  --namespace external-secrets \
  --from-literal=clientId='<INFISICAL_CLIENT_ID>' \
  --from-literal=clientSecret='<INFISICAL_CLIENT_SECRET>'
```

Ask user for credentials if not provided.

### Phase 3: Apply Bootstrap

```bash
kubectl apply -f https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml
```

This deploys the App of Apps which manages everything else.

### Phase 4: Monitor Sync Waves

Watch ArgoCD applications deploy in order:

```bash
watch -n 5 'kubectl get applications -n argocd -o custom-columns="NAME:.metadata.name,WAVE:.metadata.annotations.argocd\.argoproj\.io/sync-wave,SYNC:.status.sync.status,HEALTH:.status.health.status" | sort -k2 -n'
```

Expected wave order:
- Wave 0-1: Networking (if managed)
- Wave 2: Secrets (ESO + ClusterSecretStores)
- Wave 3-4: Storage (Longhorn)
- Wave 5: Platform services (Tailscale, Netdata)
- Wave 99: ArgoCD HA (manual sync)

### Phase 5: Verify Completion

```bash
kubectl get applications -n argocd
```

All apps should show `Synced` and `Healthy`.

### Phase 6: ArgoCD HA Upgrade (Manual)

After Longhorn is healthy:

1. Access ArgoCD UI (via Tailscale)
2. Find `argocd-ha` application
3. Manually sync it

This is intentionally manual as a safety gate.

## Troubleshooting

**ESO not creating secrets:**

- Check ClusterSecretStore status
- Verify Infisical path matches store configuration

**Longhorn volumes pending:**

- Check node disk configuration
- Patch nodes.longhorn.io with disk paths

**Apps stuck OutOfSync:**

- Check for ignoreDifferences on ESO-managed resources
- ESO adds default fields that cause drift

## Recovery

If bootstrap fails mid-way:

```bash
# Delete and retry
kubectl delete -f https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml

# Fix issue, then reapply
kubectl apply -f https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml
```
