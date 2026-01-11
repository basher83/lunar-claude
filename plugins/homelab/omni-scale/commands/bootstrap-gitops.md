---
description: Bootstrap GitOps stack (ArgoCD, ESO, Longhorn) onto existing Talos cluster
allowed-tools: Bash(kubectl:create), mcp__plugin_omni-scale_kubernetes__*
---

# GitOps Bootstrap

Deploy the GitOps stack onto an existing talos-prod-01 cluster.

**Note:** This is a WIP command that will be refined as bootstrap procedures evolve.

## Prerequisites

Before starting:

1. **Cluster operational** - Verify with `/omni-scale:status`
2. **kubectl access** - Nodes showing Ready
3. **Infisical credentials** - `$INFISICAL_CLIENT_ID` and `$INFISICAL_CLIENT_SECRET` set in environment

## Instructions

### Phase 1: Verify Cluster Ready

```text
mcp__plugin_omni-scale_kubernetes__kubectl_get(resourceType: "nodes")
```

All nodes should show `Ready`. If not, stop and troubleshoot.

### Phase 2: Create Bootstrap Secret

The one manual secret for Infisical authentication:

```bash
kubectl create namespace external-secrets

kubectl create secret generic universal-auth-credentials \
  --namespace external-secrets \
  --from-literal=clientId="$INFISICAL_CLIENT_ID" \
  --from-literal=clientSecret="$INFISICAL_CLIENT_SECRET"
```

If command fails → Stop → Inform user env vars are not properly set.

### Phase 3: Apply Bootstrap

```text
mcp__plugin_omni-scale_kubernetes__kubectl_apply(manifest: "https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml")
```

This deploys the App of Apps which manages everything else.

### Phase 4: Monitor Sync Waves

```text
mcp__plugin_omni-scale_kubernetes__kubectl_get(resourceType: "applications", namespace: "argocd")
```

Expected wave order:

- Wave 0-1: Networking (if managed)
- Wave 2: Secrets (ESO + ClusterSecretStores)
- Wave 3-4: Storage (Longhorn)
- Wave 5: Platform services (Tailscale, Netdata)
- Wave 99: ArgoCD HA (manual sync)

### Phase 5: Verify Completion

```text
mcp__plugin_omni-scale_kubernetes__kubectl_get(resourceType: "applications", namespace: "argocd")
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

If bootstrap fails mid-way, delete and retry:

```text
mcp__plugin_omni-scale_kubernetes__kubectl_delete(manifest: "https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml")
```

Fix the issue, then reapply Phase 3.
