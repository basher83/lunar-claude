---
description: Bootstrap GitOps stack (ArgoCD, ESO, Longhorn) onto existing Talos cluster
allowed-tools: Bash(kubectl:*), mcp__plugin_omni-scale_kubernetes__*
---

# GitOps Bootstrap

Deploy the GitOps stack onto an existing talos-prod-01 cluster.

## Pre-flight Gate

**STOP** if omni-talos skill is not loaded.

Check: Do you have knowledge of `provider-ctl.py` and the provider operations table? If not, instruct user:

```text
Required setup not complete. Run this chain first:
  /omni-scale:omni-prime && /omni-scale:status && /omni-scale:omni-talos
Then re-run /omni-scale:bootstrap-gitops
```

## Instructions

### Phase 1: Create Bootstrap Secret

**Outcome:** `external-secrets` namespace exists with `universal-auth-credentials` secret containing Infisical credentials.

Create namespace and secret using kubectl. Secret requires `$INFISICAL_CLIENT_ID` and `$INFISICAL_CLIENT_SECRET` env vars.

If command fails, stop and inform user env vars are not set.

### Phase 2: Apply Bootstrap

**Outcome:** App of Apps deployed from mothership-gitops bootstrap manifest.

Apply bootstrap manifest: `https://raw.githubusercontent.com/basher83/mothership-gitops/main/bootstrap/bootstrap.yaml`

### Phase 3: Monitor Sync Waves

**Outcome:** All apps (except argocd-ha) show Synced/Healthy.

**Poll:** Check ArgoCD applications in argocd namespace. <!-- REQUIRED: sleep 30s between attempts -->

Expected wave order:

- Wave 0-1: Networking (if managed)
- Wave 2: Secrets (ESO + ClusterSecretStores)
- Wave 3-4: Storage (Longhorn)
- Wave 5: Platform services (Tailscale, Netdata)
- Wave 99: ArgoCD HA (manual sync)

- Max wait: 20 min
- After 3 attempts, increase interval to 60s

### Phase 4: ArgoCD HA Upgrade (Manual)

**Outcome:** ArgoCD HA running.

After Longhorn healthy, instruct user to manually sync `argocd-ha` via ArgoCD UI (Tailscale). This is intentionally manual as safety gate.

Bootstrap complete when all ArgoCD apps show Synced/Healthy.
