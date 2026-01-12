# Architecture Overview

## Network Topology

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

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Omni on Holly (Quantum) | Separation of management plane from workload plane |
| Provider on Foxtrot LXC | L2 adjacency required for SideroLink registration |
| Auth0 for OIDC | Managed service, simpler than self-hosted tsidp |
| CEPH storage | Distributed storage across Matrix nodes |

## L2 Adjacency Requirement

The Proxmox provider must be network-adjacent to Talos VMs for SideroLink machine registration. When a Talos VM boots, it broadcasts on the local network to find the Omni control plane. The provider on Foxtrot LXC (192.168.3.10) shares L2 with Talos VMs on the Matrix cluster (192.168.3.x).

## Split-Horizon DNS

Talos VMs resolve `omni.spaceships.work` via Unifi local DNS to 192.168.10.20 (Holly's LAN IP). Static routing between 192.168.3.0/24 and 192.168.10.0/24 enables cross-subnet SideroLink registration.

External access uses Tailscale MagicDNS.
