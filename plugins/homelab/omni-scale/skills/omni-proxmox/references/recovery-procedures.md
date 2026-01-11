# Recovery Procedures

When provisioning fails mid-way or state becomes corrupted, use these procedures.

> For debugging "why isn't X working", see `debugging.md`.
> For full context and war stories, see `docs/TROUBLESHOOTING.md`.

---

## Node Stuck in Reboot Loop

**Symptom:** New node boots, reboots repeatedly, never joins cluster.

**Check for this error in node events or kubelet logs:**

```
nodes X is forbidden: is not allowed to modify labels: node-role.kubernetes.io/worker
```

**Cause:** Kubernetes NodeRestriction admission controller blocks kubelets from setting labels in protected namespaces (`node-role.kubernetes.io/*`, `kubernetes.io/*`).

**Fix:**

1. Remove the protected label from cluster template `machine.nodeLabels`
2. Delete the stuck machine (see next section)
3. Redeploy

**Alternative:** Use unprivileged namespace like `omni.sidero.dev/role: worker`.

---

## Machine Stuck in "Destroying" State

**Symptom:** Machine shows "Destroying/Unreachable" in Omni UI. Won't go away.

**Common cause:** VM was deleted out-of-band (Proxmox UI, `qm destroy`). Omni still has the resource with finalizers.

**Key insight:** `machine` resources are read-only. Use `clustermachine` instead.

**Fix:**

```bash
# Find the stuck machine UUID
omnictl get machines -o table

# Delete the clustermachine (NOT the machine)
omnictl delete clustermachine <machine-uuid>

# Verify cleanup
omnictl get machines -o table
```

---

## "Only Read Access Is Permitted" Error

**Symptom:** `omnictl delete machine <uuid>` fails with permission error even for Admins.

**Cause:** This is expected. `machines.omni.sidero.dev` is read-only by design—machines are managed by the infrastructure provider.

**Fix:** Use `clustermachine`:

```bash
omnictl delete clustermachine <uuid>
```

---

## Service Account Key Expired Mid-Provision

**Symptom:** Provider disconnects during long provisioning. New VMs fail to register.

**Fix:**

1. Regenerate key in Omni UI (Infrastructure Providers → Provider → Regenerate Key)
2. Update provider environment with new key
3. Restart provider container

```bash
ssh omni-provider 'cd /opt/omni-provider && docker compose restart'
```

---

## State Drift After Out-of-Band Changes

**Symptom:** Omni state doesn't match reality (VMs deleted in Proxmox, resources stuck).

**General recovery pattern:**

1. Identify stuck resources: `omnictl get machines -o table`
2. Delete clustermachines for missing VMs: `omnictl delete clustermachine <uuid>`
3. Verify MachineClass is healthy: `omnictl get machineclasses`
4. Re-sync cluster template if needed: `omnictl cluster template sync -f <template>`

**Prevention:** Avoid modifying Talos VMs directly in Proxmox. Use Omni for all lifecycle operations.

---

## Full Cluster Recovery

**Symptom:** Cluster is unrecoverable. Need to start fresh.

**Procedure:**

```bash
# Delete cluster (Provider will clean up VMs)
omnictl cluster template delete -f clusters/<cluster>.yaml

# Wait for cleanup
sleep 30 && omnictl get machines -o table

# Verify no orphaned resources
omnictl get clustermachines

# Redeploy
omnictl cluster template sync -f clusters/<cluster>.yaml
```

**Note:** Longhorn data is lost unless backed up externally.
