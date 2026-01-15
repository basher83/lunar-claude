---
description: Execute disaster recovery drill - destroy and recreate cluster from specs
allowed-tools: Bash(omnictl:*), Bash(ssh:*), Bash(kubectl:*), Bash(sleep:*), Read, AskUserQuestion, mcp__plugin_omni-scale_kubernetes__*
disable-model-invocation: true
---

# Disaster Recovery

Full cluster destruction and recreation from declarative specs.

**WARNING:** This destroys the entire cluster. Only run for DR drills or actual recovery.

**NOTE:** Cluster spec path hardcoded to `~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml`.

## Pre-flight Gate

**STOP** if omni-talos skill is not loaded.

Check: Do you have knowledge of `provider-ctl.py` and the provider operations table? If not, instruct user:

```text
Required setup not complete. Run this chain first:
  /omni-scale:omni-prime && /omni-scale:status && /omni-scale:omni-talos
Then re-run /omni-scale:disaster-recovery
```

## Instructions

### Phase 1: Confirm Intent

Use AskUserQuestion to confirm destruction of talos-prod-01 and all workloads. If user aborts, stop immediately.

### Phase 2: Destroy Cluster

**Outcome:** Cluster deleted, no talos VMs remain on Proxmox.

**Pre-step:** Restart provider via `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --restart` to ensure it's listening before destruction.

Delete cluster using `omnictl cluster template delete` with `--destroy-disconnected-machines` flag. Cluster spec at `~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml`.

**Poll:** Verify no machines remain via omnictl. <!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 10 min
- After 3 attempts, increase interval to 60s
- On timeout: consult omni-talos `references/debugging.md`

Confirm destruction complete with user before proceeding.

### Phase 3: Recreate Cluster

**Outcome:** Cluster recreated, all nodes reach `running` state.

Apply cluster template using `omnictl cluster template sync`.

**Poll:** Check machine status via omnictl with cluster label selector. <!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 20 min
- After 3 attempts, increase interval to 60s
- On timeout: consult omni-talos `references/debugging.md`

### Phase 4: Wait for API

**Outcome:** Kubernetes API available, kubeconfig merged.

Merge kubeconfig via omnictl, verify kubectl responds.

**Poll:** `kubectl get nodes` <!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 10 min
- After 3 attempts, increase interval to 60s
- On timeout: consult omni-talos `references/debugging.md`

Confirm cluster ready with user before GitOps bootstrap.

### Phase 5: Verify Cluster Health

**Outcome:** All nodes show `Ready`.

Use MCP kubernetes tools to verify node status.

**Note:** Nodes will show `NotReady` until CNI is deployed in Phase 6. This is
expected — the bootstrap-gitops command installs Cilium first.

### Phase 5.5: Pre-Bootstrap Cleanup Gate

**STOP** and use AskUserQuestion to confirm external cleanup:

Before GitOps bootstrap, external state from the old cluster must be cleaned up:

- **Tailscale dashboard:** Remove old devices (e.g., `talos-prod-operator`)
  Otherwise new operator registers as `talos-prod-operator-1` and old entry persists.
- **Omni service accounts:** Note that scoped SAs (Freelens, MCP) need recreation
  after bootstrap (tokens contain old cluster UUID).

Confirm cleanup complete before proceeding to Phase 6.

### Phase 6: Bootstrap GitOps

**Outcome:** All ArgoCD apps Synced/Healthy.

Execute `/omni-scale:bootstrap-gitops` procedure.

**Poll:** Check ArgoCD applications in argocd namespace. <!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 20 min
- After 3 attempts, increase interval to 60s
- On timeout: consult omni-talos `references/debugging.md`

Manually sync ArgoCD HA after Longhorn is healthy.

DR complete when all ArgoCD apps show Synced/Healthy.
