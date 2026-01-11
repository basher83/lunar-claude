---
description: Execute disaster recovery drill - destroy and recreate cluster from specs
allowed-tools: Bash, Read, AskUserQuestion, mcp__kubernetes__*
argument-hint: "(no arguments - interactive confirmation required)"
---

# Disaster Recovery

Full cluster destruction and recreation from declarative specs.

**WARNING:** This destroys the entire cluster. Only run for DR drills or actual recovery.

## Prerequisites

- Access to Omni console (https://omni.spaceships.work)
- omnictl authenticated
- Infisical credentials available
- Backup of any stateful data (if applicable)

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

```bash
# Document current state for comparison after recovery
kubectl get nodes -o wide > /tmp/pre-dr-nodes.txt
kubectl get pv -o wide > /tmp/pre-dr-pvs.txt
omnictl get machines --cluster talos-prod-01 > /tmp/pre-dr-machines.txt
```

### Phase 3: Destroy Cluster

```bash
omnictl cluster template delete -f ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml
```

Watch Omni console for machine destruction.

Wait for all VMs to be destroyed in Proxmox:

```bash
# Monitor until no talos VMs remain
watch 'pvesh get /nodes/foxtrot/qemu --output-format json 2>/dev/null | jq -r ".[] | select(.name | startswith(\"talos\")) | .name"'
```

### Phase 4: Recreate Cluster

Apply cluster template:

```bash
omnictl cluster template sync -f ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml
```

Monitor provisioning:

```bash
watch 'omnictl get machines --cluster talos-prod-01'
```

Wait for all nodes to reach `running` state.

### Phase 5: Verify Cluster Health

```bash
# Get kubeconfig
omnictl kubeconfig talos-prod-01 > ~/.kube/config

# Verify nodes
kubectl get nodes
```

All nodes should show `Ready` within 5-10 minutes.

### Phase 6: Bootstrap GitOps

Follow `/omni-scale:bootstrap` procedure:

1. Create external-secrets namespace
2. Create universal-auth-credentials secret
3. Apply bootstrap.yaml
4. Monitor sync waves
5. Manually sync ArgoCD HA

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

- Check provider logs on Foxtrot LXC
- Verify service account key not expired
- Check storage pool availability

**Nodes not joining:**

- DNS issue - verify split-horizon resolves correctly
- SideroLink issue - check provider L2 adjacency

**GitOps apps failing:**

- Check ESO ClusterSecretStore health
- Verify Infisical credentials correct
- Check namespace PSA labels

## Post-Recovery Checklist

- [ ] All nodes Ready
- [ ] All ArgoCD apps Synced/Healthy
- [ ] Longhorn volumes healthy
- [ ] Tailscale Ingresses accessible
- [ ] Netdata reporting metrics
- [ ] ArgoCD HA running (if applicable)
