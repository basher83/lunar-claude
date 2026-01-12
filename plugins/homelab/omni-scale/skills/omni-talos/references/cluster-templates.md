# Cluster Templates

Multi-document YAML defining cluster, control plane, and workers.

## Structure

```yaml
kind: Cluster
name: <cluster-name>
kubernetes:
  version: v1.34.3
talos:
  version: v1.11.6
patches:
  - name: <patch-name>
    inline:
      <talos machine config patch>
---
kind: ControlPlane
machineClass:
  name: <machine-class-name>
  size: <count>
systemExtensions:
  - <extension>
---
kind: Workers
machineClass:
  name: <machine-class-name>
  size: <count>
systemExtensions:
  - <extension>
```

## Example: Production Cluster

```yaml
kind: Cluster
name: talos-prod-01
kubernetes:
  version: v1.34.3
talos:
  version: v1.11.6
patches:
  - name: disable-default-cni
    inline:
      cluster:
        network:
          cni:
            name: none    # Required for Cilium
        proxy:
          disabled: true  # Cilium replaces kube-proxy
---
kind: ControlPlane
machineClass:
  name: matrix-control-plane
  size: 3
systemExtensions:
  - siderolabs/qemu-guest-agent
  - siderolabs/iscsi-tools
---
kind: Workers
machineClass:
  name: matrix-worker
  size: 2
systemExtensions:
  - siderolabs/qemu-guest-agent
  - siderolabs/iscsi-tools
```

## Common Patches

### Disable Default CNI (for Cilium)

```yaml
patches:
  - name: disable-default-cni
    inline:
      cluster:
        network:
          cni:
            name: none
        proxy:
          disabled: true
```

### Custom Kubelet Args

```yaml
patches:
  - name: kubelet-args
    inline:
      machine:
        kubelet:
          extraArgs:
            rotate-server-certificates: "true"
```

## System Extensions

Common extensions for Proxmox VMs:

| Extension | Purpose |
|-----------|---------|
| `siderolabs/qemu-guest-agent` | Proxmox guest agent (required) |
| `siderolabs/iscsi-tools` | iSCSI support for Longhorn |

## Worker Pinning

Workers CAN be pinned using multiple `kind: Workers` sections:

```yaml
---
kind: Workers
machineClass:
  name: matrix-worker-foxtrot
  size: 1
---
kind: Workers
machineClass:
  name: matrix-worker-golf
  size: 1
---
kind: Workers
machineClass:
  name: matrix-worker-hotel
  size: 1
```

## Control Plane Limitation

**ControlPlane pinning is NOT possible.** Omni requires exactly 1 `kind: ControlPlane` section per cluster template. Cannot use multiple pinned machine classes for CPs.

## Applying Templates

```bash
# Sync cluster template
omnictl cluster template sync -f clusters/talos-prod-01.yaml

# Check cluster status
omnictl cluster status talos-prod-01
```
