---
name: omni-proxmox
description: This skill should be used when the user asks to "create a machine class",
  "configure Proxmox provider", "debug provider registration", "set up CEL storage
  selectors", "troubleshoot Omni provider", "check provider status", "create a Talos
  cluster", or needs guidance on Omni + Proxmox infrastructure integration for Talos
  Kubernetes clusters.
---

# Omni + Proxmox Infrastructure Provider

This skill provides guidance for deploying and managing Talos Linux Kubernetes clusters via Sidero Omni with the Proxmox infrastructure provider.

## Current Deployment

| Component | Location | IP | Endpoint |
|-----------|----------|-----|----------|
| Omni | Holly (VMID 101, Quantum) | 192.168.10.20 | <https://omni.spaceships.work> |
| Auth0 OIDC | Managed | — | Auth0 tenant |
| Proxmox Provider | Foxtrot LXC (CT 200, Matrix) | 192.168.3.10 | L2 adjacent to Talos VMs |
| Target Cluster | Matrix (Foxtrot/Golf/Hotel) | 192.168.3.{5,6,7} | <https://192.168.3.5:8006> |
| Storage | CEPH RBD | — | `vm_ssd` pool |

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Tailnet                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Quantum Cluster (192.168.10.0/24)       Matrix Cluster (192.168.3.0/24)   │
│   ┌───────────────────────────┐           ┌─────────────────────────────┐   │
│   │  Holly (VMID 101)         │           │  Foxtrot                    │   │
│   │  ┌─────────────────────┐  │           │  ┌───────────────────────┐  │   │
│   │  │  Docker Stack       │  │           │  │  LXC CT 200           │  │   │
│   │  │  ├─ omni-tailscale  │  │◄─────────►│  │  ├─ worker-tailscale  │  │   │
│   │  │  └─ omni            │  │  Tailnet  │  │  └─ proxmox-provider  │  │   │
│   │  └─────────────────────┘  │           │  └───────────────────────┘  │   │
│   │           │               │           │             │               │   │
│   │  LAN: 192.168.10.20       │           │    LAN: 192.168.3.10        │   │
│   └───────────────────────────┘           │             │               │   │
│              │                            │             ▼ L2 Adjacent   │   │
│              ▼                            │  ┌───────────────────────┐  │   │
│   ┌───────────────────────────┐           │  │  Proxmox API          │  │   │
│   │  Auth0 (External)         │           │  │  (Foxtrot/Golf/Hotel) │  │   │
│   │  OIDC Provider            │           │  └───────────────────────┘  │   │
│   └───────────────────────────┘           │             │               │   │
│                                           │             ▼               │   │
│   ┌───────────────────────────┐           │  ┌───────────────────────┐  │   │
│   │  Browser                  │──────────►│  │  Talos VMs            │  │   │
│   │  (Admin UI via Tailscale) │           │  │  (CEPH vm_ssd)        │  │   │
│   └───────────────────────────┘           │  └───────────────────────┘  │   │
│                                           └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key architectural decisions:**

| Decision | Rationale |
|----------|-----------|
| Omni on Holly (Quantum) | Separation of management plane from workload plane |
| Provider on Foxtrot LXC | L2 adjacency required for SideroLink registration |
| Auth0 for OIDC | Managed service, simpler than self-hosted tsidp |
| CEPH storage | Distributed storage across Matrix nodes |

**L2 Adjacency Requirement:**

The Proxmox provider must be network-adjacent to Talos VMs for SideroLink machine registration. When a Talos VM boots, it broadcasts on the local network to find the Omni control plane. The provider on Foxtrot LXC (192.168.3.10) shares L2 with Talos VMs on the Matrix cluster (192.168.3.x).

**Split-Horizon DNS:**

Talos VMs resolve `omni.spaceships.work` via Unifi local DNS to 192.168.10.20 (Holly's LAN IP). Static routing between 192.168.3.0/24 and 192.168.10.0/24 enables cross-subnet SideroLink registration.

## Provider Configuration

The Proxmox provider runs as Docker containers inside the `omni-provider` LXC (CT 200) on Foxtrot.

**File locations:**

| File | Purpose |
|------|---------|
| `proxmox-provider/compose.yml` | Docker Compose for provider + Tailscale sidecar |
| `proxmox-provider/config.yaml` | Proxmox API credentials (gitignored) |
| `proxmox-provider/.env` | Environment variables (gitignored) |

**Setup:**

```bash
# Copy example files
cp proxmox-provider/config.yaml.example proxmox-provider/config.yaml
cp proxmox-provider/.env.example proxmox-provider/.env

# Edit with actual credentials
vim proxmox-provider/config.yaml  # Proxmox API token
vim proxmox-provider/.env         # Tailscale key, Omni service account

# Deploy
cd proxmox-provider
docker compose up -d
```

### Provider Config (config.yaml)

```yaml
proxmox:
  url: "https://192.168.3.5:8006/api2/json"
  tokenID: "terraform@pam!automation"
  tokenSecret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  insecureSkipVerify: true  # Self-signed Proxmox certs
```

For Proxmox API token setup, see `references/proxmox-permissions.md`.

## MachineClass Structure

MachineClasses define VM specifications for auto-provisioning. Apply via omnictl.

```yaml
metadata:
  namespace: default
  type: MachineClasses.omni.sidero.dev
  id: matrix-worker
spec:
  autoprovision:
    providerid: matrix-cluster
    providerdata: |
      cores: 4
      sockets: 1
      memory: 16384
      disk_size: 100
      network_bridge: vmbr0
      storage_selector: name == "vm_ssd"
      node: foxtrot  # Pin to specific node (requires PR #38)
```

**Provider Data Fields:**

Source: [PR #36](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/36) (merged Dec 30, 2025)

| Category | Fields |
|----------|--------|
| **Compute** | `cores`, `sockets`, `memory`, `cpu_type`, `machine_type`, `numa`, `hugepages`, `balloon` |
| **Storage** | `disk_size`, `storage_selector`, `disk_ssd`, `disk_discard`, `disk_iothread`, `disk_cache`, `disk_aio`, `additional_disks` |
| **Network** | `network_bridge`, `vlan`, `additional_nics` |
| **PCI** | `pci_devices` (requires Proxmox resource mappings) |
| **Placement** | `node` ([PR #38](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/38)) |

### Compute Fields

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

### Storage Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `disk_size` | int | *required* | Primary disk size in GB |
| `storage_selector` | string | *required* | CEL expression for storage pool |
| `disk_ssd` | bool | false | Enable SSD emulation |
| `disk_discard` | bool | false | Enable TRIM/discard support |
| `disk_iothread` | bool | false | Enable dedicated IO thread |
| `disk_cache` | string | - | Cache mode: `none`, `writeback`, `writethrough`, `directsync`, `unsafe` |
| `disk_aio` | string | - | AIO mode: `native`, `io_uring`, `threads` |

**Additional disks:**

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

### Network Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `network_bridge` | string | `vmbr0` | Primary network bridge |
| `vlan` | int | 0 | VLAN tag (0 = untagged) |

**Additional NICs:**

```yaml
additional_nics:
  - bridge: vmbr1
    firewall: false
  - bridge: vmbr2
    vlan: 20
```

### PCI Passthrough

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

### Placement Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `node` | string | - | Pin VM to specific Proxmox node |

## CEL Storage Selectors

The provider uses CEL (Common Expression Language) to select storage pools.

**Available fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Storage pool name |

> **Warning:** The `type` field is NOT usable — `type` is a reserved CEL keyword. Use `name` for all storage selection.

**Matrix cluster storage:**

```text
# CEPH RBD pool (recommended)
name == "vm_ssd"

# Container storage
name == "vm_containers"
```

For complete CEL syntax, see `references/cel-storage-selectors.md`.

## omnictl CLI

**Service account key (automation):**

```bash
omnictl --omni-url https://omni.spaceships.work \
        --service-account-key $OMNICTL_SERVICE_ACCOUNT_KEY \
        get clusters
```

**OIDC browser flow (interactive):**

```bash
# Any command triggers browser auth if not authenticated
omnictl get clusters
```

**Common operations:**

```bash
# List machine classes
omnictl get machineclasses

# Apply machine class
omnictl apply -f machine-classes/matrix-worker.yaml

# Sync cluster template
omnictl cluster template sync -f clusters/talos-prod-01.yaml

# Check cluster status
omnictl cluster status talos-prod-01

# Get machines (use label selector, --cluster flag doesn't exist)
omnictl get machines -l omni.sidero.dev/cluster=talos-prod-01
```

## Cluster Templates

Multi-document YAML defining cluster, control plane, and workers:

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

See `clusters/talos-prod-01.yaml` for the full production template.

## Troubleshooting

Use `${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py` for provider container management:

```bash
# Check provider logs (filtered, human-readable)
$ ${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py --logs 50

# Raw JSON logs for debugging
$ ${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py --logs 100 --raw

# Restart provider container
$ ${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py --restart
```

### Provider not registering

```bash
# Check provider logs for registration errors
$ ${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py --logs 50

# Verify Tailscale connectivity
ssh omni-provider docker exec worker-tailscale tailscale status
```

### Machines stuck in provisioning

```bash
# Check Proxmox for VM creation
pvesh get /nodes/foxtrot/qemu --output-format json | jq '.[] | {vmid, name, status}'

# Check provider logs for errors
$ ${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py --logs 50
```

### Storage selector not matching

```bash
# List available storage pools
pvesh get /storage --output-format json | jq '.[].storage'

# Test CEL expression (provider logs show evaluation)
# Look for: "no storage pools matched selector"
```

For more diagnostics, see `references/debugging.md`. For recovery from stuck states, see `references/recovery-procedures.md`.

## Key Constraints

**Networking:**

- Provider MUST be L2 adjacent to Talos VMs (Foxtrot LXC on 192.168.3.x)
- Omni on Holly (192.168.10.20) reachable via static route
- Split-horizon DNS: `omni.spaceships.work` → 192.168.10.20 (LAN) or Tailscale IP (external)

**Provider limitations:**

- CEL `type` keyword reserved — use `name` only for storage selectors
- **Hostname conflict bug:** Upstream provider injects hostname config that conflicts with Omni. Requires local patched build (`:local-fix` tag). See `docs/TROUBLESHOOTING.md`.

**Omni template limitations:**

- **ControlPlane pinning not possible:** Omni requires exactly 1 `kind: ControlPlane` section per cluster template. Cannot use multiple pinned machine classes for CPs.
- Workers CAN be pinned via multiple `kind: Workers` sections with different machine classes.
- See `docs/TROUBLESHOOTING.md` → "Control Plane Node Distribution Cannot Be Pinned".

**Upstream PRs (merged):**

- [PR #36](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/36) — Advanced VM options (multi-disk, PCI passthrough, etc.)
- [PR #38](https://github.com/siderolabs/omni-infra-provider-proxmox/pull/38) — Node pinning support

**Storage:**

- Use CEPH `vm_ssd` pool for production VMs
- CEPH provides HA across Matrix nodes
- ~12TB usable capacity (replication factor 3)

## Reference Files

- `references/cel-storage-selectors.md` — CEL syntax and patterns
- `references/proxmox-permissions.md` — API token setup
- `references/omnictl-auth.md` — Authentication methods
- `references/debugging.md` — Common issues
- `references/recovery-procedures.md` — Recovery procedures

## Example Files

- `examples/machineclass-ceph.yaml` — MachineClass with CEPH storage
- `examples/machineclass-local.yaml` — MachineClass with local LVM
- `examples/cluster-template.yaml` — Complete cluster template
- `examples/proxmox-gpu-worker.yaml` — GPU worker MachineClass
- `examples/proxmox-storage-node.yaml` — Storage node MachineClass
- `examples/proxmox-worker-multi-net.yaml` — Multi-network worker MachineClass

## Scripts

- `${CLAUDE_PLUGIN_ROOT}/skills/omni-proxmox/scripts/provider-ctl.py` — Manage Omni Proxmox Provider container via SSH

| Command | Description |
|---------|-------------|
| `--restart` | Restart provider container (idempotent, 30s timeout) |
| `--logs [N]` | Show last N log lines, filtered (default: 25, max: 100) |
| `--logs N --raw` | Show raw JSON logs without filtering |
