---
description: Execute disaster recovery drill - destroy and recreate cluster from specs
allowed-tools: Bash(omnictl:*), Bash(ssh:*), Bash(kubectl:*), Bash(sleep:*), Read, AskUserQuestion, mcp__kubernetes__*
---

# Disaster Recovery

Full cluster destruction and recreation from declarative specs.

**WARNING:** This destroys the entire cluster. Only run for DR drills or actual recovery.

**NOTE:** Paths below reference user-specific locations. Consider setting `$OMNI_SCALE_ROOT` if needed.

## Prerequisites

- Access to Omni console (<https://omni.spaceships.work>)
- omnictl authenticated
- Infisical credentials available (`$INFISICAL_CLIENT_ID`, `$INFISICAL_CLIENT_SECRET`)
- Backup of any stateful data (if applicable)
- Provider connectivity verified:

```bash
omnictl get infraproviders
```

## Instructions

### Phase 1: Confirm Intent

Use AskUserQuestion to confirm:

```text
header: "DR Drill"
question: "This will DESTROY talos-prod-01 and all workloads. Continue?"
options:
  - "Yes, execute DR drill"
  - "No, abort"
```

If user selects abort, stop immediately.

### Phase 2: Capture Current State (Optional)

```text
mcp__kubernetes__kubectl_get(resourceType: "nodes")
mcp__kubernetes__kubectl_get(resourceType: "pv")
```

```bash
omnictl get machines --cluster talos-prod-01
```

### Phase 3: Destroy Cluster

**WARNING:** No rollback after this phase. Cluster will be destroyed.

```bash
omnictl cluster template delete -f ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml --destroy-disconnected-machines
```

**Poll loop:**

```bash
# Check status
ssh foxtrot "pvesh get /cluster/resources --type vm --output-format json" | jq -r '.[] | select(.name | startswith("talos")) | .name'

# REQUIRED - do not skip or reduce
sleep 30
```

Repeat until no talos VMs remain. Max wait: 10 min.

After 3 attempts at 30s intervals, INCREASE to 60s. Do not decrease below 30s.

If timeout exceeded, check failure scenarios below.

Use AskUserQuestion to confirm destruction complete before proceeding.

### Phase 4: Recreate Cluster

Apply cluster template:

```bash
omnictl cluster template sync -f ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml
```

**Poll loop:**

```bash
# Check status
omnictl get machines --cluster talos-prod-01

# REQUIRED - do not skip or reduce
sleep 30
```

Repeat until all nodes reach `running` state. Max wait: 20 min.

After 3 attempts at 30s intervals, INCREASE to 60s. Do not decrease below 30s.

If timeout exceeded, check failure scenarios below.

### Phase 4.5: Wait for API Availability

**Poll loop:**

```bash
# Check status
omnictl kubeconfig talos-prod-01 --merge
kubectl get nodes

# REQUIRED - do not skip or reduce
sleep 30
```

Repeat until API responds. Max wait: 10 min.

After 3 attempts at 30s intervals, INCREASE to 60s. Do not decrease below 30s.

If timeout exceeded, check failure scenarios below.

Use AskUserQuestion to confirm cluster is ready before GitOps bootstrap.

### Phase 5: Verify Cluster Health

```text
mcp__kubernetes__kubectl_get(resourceType: "nodes")
```

All nodes should show `Ready`.

### Phase 6: Bootstrap GitOps

Follow `/omni-scale:bootstrap-gitops` procedure:

1. Create external-secrets namespace
2. Create universal-auth-credentials secret
3. Apply bootstrap.yaml

**Poll loop:**

```text
mcp__kubernetes__kubectl_get(resourceType: "applications", namespace: "argocd")
```

```bash
# REQUIRED - do not skip or reduce
sleep 30
```

Repeat until all apps show Synced/Healthy. Max wait: 20 min.

After 3 attempts at 30s intervals, INCREASE to 60s. Do not decrease below 30s.

If timeout exceeded, check failure scenarios below.

Manually sync ArgoCD HA after Longhorn is healthy.

### Phase 7: Verify Recovery

Run `/omni-scale:status` to confirm full recovery.

Compare against pre-DR state if captured.

## Expected Timeline

| Phase | Duration |
|-------|----------|
| Cluster destruction | 2-5 min |
| VM provisioning | 10-15 min |
| Kubernetes ready | 5-10 min |
| GitOps bootstrap | 10-15 min |
| **Total** | **30-45 min** |

## Failure Scenarios

**VMs not destroying:**

- Check Omni console for errors
- Manually delete via Proxmox if stuck

**VMs not provisioning:**

- Check provider logs: `scripts/provider-ctl.py --logs 50`
- Verify service account key not expired
- Check storage pool availability

**Provider wrong image tag:**

- Must use `:local-fix` tag, not `:latest`
- Hostname conflict bug in upstream image
- Check compose.yml in proxmox-provider/

**Nodes not joining:**

- DNS issue - verify split-horizon resolves correctly
- SideroLink issue - check provider L2 adjacency

**GitOps apps failing:**

- Check ESO ClusterSecretStore health
- Verify Infisical credentials correct
- Check namespace PSA labels

**Longhorn volumes not attaching:**

- May need to patch nodes.longhorn.io with disk paths
- Check node disk configuration matches expectations

## Post-Recovery Checklist

- [ ] All nodes Ready
- [ ] All ArgoCD apps Synced/Healthy
- [ ] Longhorn volumes healthy
- [ ] Tailscale Ingresses accessible
- [ ] Netdata reporting metrics
- [ ] ArgoCD HA running (if applicable)
