# MachineClass Reference

MachineClasses define VM specifications for auto-provisioning. Apply via `omnictl apply -f`.

## Structure

```yaml
metadata:
  namespace: default
  type: MachineClasses.omni.sidero.dev
  id: <machine-class-name>
spec:
  autoprovision:
    providerid: matrix-cluster
    providerdata: |
      <provider data fields>
```

## Provider Data Fields

Source: [PR #36](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/36) (merged Dec 30, 2025)

| Category | Fields |
|----------|--------|
| **Compute** | `cores`, `sockets`, `memory`, `cpu_type`, `machine_type`, `numa`, `hugepages`, `balloon` |
| **Storage** | `disk_size`, `storage_selector`, `disk_ssd`, `disk_discard`, `disk_iothread`, `disk_cache`, `disk_aio`, `additional_disks` |
| **Network** | `network_bridge`, `vlan`, `additional_nics` |
| **PCI** | `pci_devices` (requires Proxmox resource mappings) |
| **Placement** | `node` ([PR #38](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/38)) |

## Compute Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cores` | int | *required* | CPU cores per socket |
| `sockets` | int | 1 | Number of CPU sockets |
| `memory` | int | *required* | RAM in MB |
| `cpu_type` | string | `x86-64-v2-AES` | CPU type. Use `host` for passthrough |
| `machine_type` | string | `i440fx` | VM machine type. Use `q35` for PCIe passthrough |
| `numa` | bool | false | Enable NUMA topology |
| `hugepages` | string | - | Hugepages size: `2`, `1024`, or `any` |
| `balloon` | bool | true | Enable memory ballooning. Disable for GPU/HPC |

## Storage Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `disk_size` | int | *required* | Primary disk size in GB |
| `storage_selector` | string | *required* | CEL expression for storage pool |
| `disk_ssd` | bool | false | Enable SSD emulation |
| `disk_discard` | bool | false | Enable TRIM/discard support |
| `disk_iothread` | bool | false | Enable dedicated IO thread |
| `disk_cache` | string | - | Cache mode: `none`, `writeback`, `writethrough`, `directsync`, `unsafe` |
| `disk_aio` | string | - | AIO mode: `native`, `io_uring`, `threads` |

### Additional Disks

```yaml
additional_disks:
  - disk_size: 500
    storage_selector: name == "nvme-pool"
    disk_ssd: true
    disk_iothread: true
  - disk_size: 1000
    storage_selector: name == "hdd-archive"
    disk_cache: writeback
```

## Network Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `network_bridge` | string | `vmbr0` | Primary network bridge |
| `vlan` | int | 0 | VLAN tag (0 = untagged) |

### Additional NICs

```yaml
additional_nics:
  - bridge: vmbr1
    firewall: false
  - bridge: vmbr2
    vlan: 20
```

## PCI Passthrough

Requires Proxmox Resource Mappings configured.

```yaml
pci_devices:
  - mapping: nvidia-rtx-4090
    pcie: true
```

| Field | Type | Description |
|-------|------|-------------|
| `mapping` | string | Proxmox resource mapping name |
| `pcie` | bool | Use PCIe (requires `machine_type: q35`) |

## Placement Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `node` | string | - | Pin VM to specific Proxmox node |

## Storage Selector (CEL)

> **Warning:** The `type` field is NOT usable — `type` is a reserved CEL keyword.

Use `name` for all storage selection:

```text
name == "vm_ssd"        # CEPH RBD pool (recommended)
name == "vm_containers" # Container storage
```

See `cel-storage-selectors.md` for complete CEL syntax.
