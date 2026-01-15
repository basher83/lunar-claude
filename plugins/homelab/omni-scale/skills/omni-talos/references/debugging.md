# Debugging Guide

Common issues and diagnostics for the Omni + Proxmox provider.

> For recovery procedures (stuck machines, state drift), see `recovery-procedures.md`.
> For full context and war stories, see `docs/TROUBLESHOOTING.md`.

## Current Architecture

| Component | Location | IP |
|-----------|----------|-----|
| Omni | Holly (VMID 101, Quantum) | 192.168.10.20 |
| Proxmox Provider | Foxtrot LXC (CT 200, Matrix) | 192.168.3.10 |
| Proxmox API | Matrix cluster | 192.168.3.{5,6,7}:8006 |

## Provider Registration Issues

### Provider Not Appearing in Omni

**Symptoms:** Provider doesn't show in Omni UI under Infrastructure Providers.

**Checks:**

```bash
# Verify provider is running (on Foxtrot LXC)
ssh omni-provider docker ps

# Check provider logs for registration attempts
ssh omni-provider docker logs omni-provider-proxmox-provider-1 | grep -i register

# Or from omnictl
omnictl get infraproviders
```

**Common causes:**

1. **Invalid provider key:** Regenerate key in Omni UI and update environment
2. **Network issue:** Provider can't reach Omni API (check Tailscale connectivity)
3. **Wrong Omni URL:** Verify `--omni-api-endpoint` is `https://omni.spaceships.work`

### Provider Shows "Unhealthy"

**Checks:**

```bash
# Check provider logs for errors (on Foxtrot LXC)
ssh omni-provider docker logs --tail=50 omni-provider-proxmox-provider-1
```

**Common causes:**

1. **Proxmox API unreachable:** Test connectivity from host
2. **Invalid credentials:** Verify config.yaml settings
3. **SSL certificate issues:** Check `insecureSkipVerify` setting

## Storage Selector Issues

### CEL Selector Returns Empty

**Symptoms:** Machine provisioning fails with storage-related error.

**Checks:**

```bash
# On Proxmox node, list storage pools
pvesh get /storage

# Check storage types
pvesh get /storage --output-format json | jq '.[] | {storage, type, enabled, active}'
```

**Common causes:**

1. **Wrong storage type:** `lvmthin` vs `lvm` vs `zfspool`
2. **Storage not enabled/active:** Check Proxmox storage configuration
3. **Typo in storage name:** CEL expressions are case-sensitive

**Fix:** Update MachineClass storageSelector to match actual storage configuration.

### CEL Type Keyword Error

**Symptoms:** Storage selector using `type == "rbd"` fails with type mismatch error.

**Cause:** `type` is a reserved keyword in CEL and cannot be used as a field name.

**Fix:** Use `name` field only:

```yaml
# WRONG - type is reserved keyword
storage_selector: type == "rbd"

# CORRECT - use name field
storage_selector: name == "vm_ssd"
```

### Wrong Storage Selected

**Cause:** Multiple storage pools match the filter.

**Fix:** Use exact name match:

```yaml
storage_selector: name == "vm_ssd"
```

## Machine Provisioning Issues

### VMs Not Creating

**Symptoms:** MachineClass applied, but no VMs appear in Proxmox.

**Checks:**

```bash
# Check provider logs (on Foxtrot LXC)
ssh omni-provider docker logs omni-provider-proxmox-provider-1 | grep -i error

# Verify MachineClass is recognized
omnictl get machineclasses
```

**Common causes:**

1. **Insufficient Proxmox resources:** Check node capacity
2. **Invalid MachineClass config:** Missing required fields
3. **Proxmox permissions:** User lacks VM.Allocate permission

### VMs Created But Not Registering

**Symptoms:** VMs exist in Proxmox but don't appear in Omni.

**Checks:**

1. VM is booting and running
2. VM has network connectivity to provider
3. Talos is installed correctly

**Common causes:**

1. **L2 adjacency missing:** Provider must be on same network segment as Talos VMs (SideroLink requirement). Provider on Foxtrot LXC (192.168.3.x) can reach Matrix VMs.
2. **Wrong Talos ISO:** Provider using incompatible Talos version
3. **Firewall blocking:** Ports 50000-50001 (Siderolink)

### VMs Stuck in "Provisioning"

**Symptoms:** Machines show "Provisioning" indefinitely.

**Checks:**

```bash
# Check machine status
omnictl get machines

# Check specific machine
omnictl get machine <machine-id> -o yaml
```

**Common causes:**

1. **Talos bootstrap failed:** Check VM console in Proxmox
2. **Network issues:** VM can't reach Omni
3. **Resource constraints:** VM stuck waiting for resources

## Cluster Issues

### Cluster Creation Fails

**Symptoms:** Cluster template sync fails or cluster stays unhealthy.

**Checks:**

```bash
# Check cluster status
omnictl get cluster <cluster-name> -o yaml

# Check cluster events
omnictl get events --cluster <cluster-name>
```

**Common causes:**

1. **Invalid MachineClass reference:** MachineClass doesn't exist
2. **Insufficient machines:** Not enough healthy machines
3. **etcd issues:** Control plane quorum problems

### Cluster Scaling Problems

**Symptoms:** Adding workers fails or times out.

**Checks:**

```bash
# Check machine allocations
omnictl get machines --cluster <cluster-name>

# Verify MachineClass capacity
omnictl get machineclass <class-name> -o yaml
```

**Common causes:**

1. **MachineClass exhausted:** No available resources
2. **Provider at capacity:** Proxmox cluster full
3. **Rate limiting:** Too many simultaneous provisions

## omnictl Issues

### "Unauthorized" Errors

**Symptoms:** omnictl commands fail with authentication errors.

**Fixes:**

1. Re-authenticate by running any command (triggers OIDC flow)
2. Check service account key validity
3. Verify key has required permissions

### "Connection Refused"

**Symptoms:** Can't connect to Omni.

**Fixes:**

1. Check Omni is running on Holly
2. Verify Tailscale connectivity
3. Test URL directly: `curl https://omni.spaceships.work/healthz`

## ArgoCD Bootstrap Issues

For comprehensive GitOps bootstrap troubleshooting, see `gitops-bootstrap-issues.md`.

Quick reference for common issues:

### NetworkPolicy Blocking

**Symptom:** Apps stuck Unknown/OutOfSync, "connection error: operation not permitted"

**Fix:** Delete NetworkPolicies or use Helm with `networkPolicy.enabled=false`

### Label/Port Mismatches (Raw Manifests)

**Symptom:** `kubectl get endpoints argocd-repo-server` shows `<none>`

**Fix:** Use Helm chart instead of raw manifests, or patch deployments

### Stale Error Cache

**Symptom:** Errors persist after fixing underlying issue

**Fix:** `kubectl rollout restart statefulset argocd-application-controller -n argocd`

### PodSecurity Violations

**Symptom:** DaemonSet `DESIRED: 3, READY: 0`, pods don't schedule

**Fix:** Label namespace with `pod-security.kubernetes.io/enforce=privileged`

## Log Locations

| Component | Location | Command |
|-----------|----------|---------|
| Omni | Holly | `ssh holly 'cd /path/to/omni && docker compose logs omni'` |
| Tailscale sidecar | Holly | `ssh holly 'cd /path/to/omni && docker compose logs omni-tailscale'` |
| Provider | Foxtrot LXC | `ssh omni-provider docker logs omni-provider-proxmox-provider-1` |
| Machine logs | Omni UI | Machines → [machine] → Logs |

## Health Checks

Quick health verification:

```bash
# Omni services running (on Holly)
ssh holly 'cd /path/to/omni && docker compose ps'

# Provider running (on Foxtrot LXC)
ssh omni-provider docker ps

# Provider registered
omnictl get infraproviders

# Machines available
omnictl get machines

# Clusters healthy
omnictl get clusters
```
