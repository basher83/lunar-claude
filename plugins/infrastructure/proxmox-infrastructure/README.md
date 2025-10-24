# Proxmox Infrastructure Management

Expert guidance for managing Proxmox VE clusters, creating templates, provisioning VMs, and configuring network infrastructure.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install proxmox-infrastructure:

```bash
/plugin install proxmox-infrastructure@lunar-claude
```

## Components

### Skills

- **proxmox-infrastructure** - Comprehensive skill for Proxmox VE management
  - VM template creation with cloud-init
  - VM provisioning via cloning (Ansible/Terraform)
  - VLAN-aware bridge configuration
  - Network infrastructure (bridges, VLANs, bonds)
  - CEPH storage pool management
  - QEMU guest agent integration
  - Proxmox API interactions (Python/Ansible)
  - Cluster health monitoring

## Usage

### Autonomous Mode

Simply ask Claude to help with Proxmox:

```
"Create a cloud-init VM template for Ubuntu"
"Configure VLAN-aware bridging on Proxmox"
"Set up CEPH storage with MTU 9000"
"Deploy a VM using Terraform and Proxmox provider"
"Troubleshoot VM network issues with VLANs"
```

Claude will automatically use the proxmox-infrastructure skill.

## How It Works

The proxmox-infrastructure skill provides comprehensive guidance on:

- **Template Creation**: Cloud-init patterns for Ubuntu/Debian templates
- **VM Provisioning**: Ansible and Terraform patterns for VM deployment
- **Network Configuration**: VLAN-aware bridges, bonds, MTU configuration
- **Storage Management**: CEPH deployment and configuration
- **API Integration**: Python and Ansible automation patterns
- **Troubleshooting**: Common issues and solutions

## Supporting Documentation

The skill includes extensive reference material:
- `/reference/` - Cloud-init patterns, networking, API, storage, QEMU guest agent
- `/workflows/` - Cluster formation, CEPH deployment automation
- `/examples/` - Real Terraform configurations
- `/tools/` - Python management tools (uv-based)
  - `validate_template.py` - Template health validation
  - `cluster_status.py` - Cluster health metrics
  - `check_ceph_health.py` - CEPH health monitoring
  - `check_cluster_health.py` - Comprehensive cluster checks
- `/anti-patterns/` - Common mistakes from real deployments

## Key Features

### Cloud-Init Templates

Complete automation for creating production-ready VM templates:
- Virtio-SCSI controller configuration
- Serial console setup for cloud images
- Cloud-init CD-ROM drive (ide2)
- Proper boot order configuration
- Template conversion workflow

### VLAN-Aware Networking

Multi-VLAN support on single bridge:
- vmbr0: Management network
- vmbr1: CEPH Public (MTU 9000)
- vmbr2: CEPH Private (MTU 9000)
- 802.3ad LACP bonding support

### CEPH Storage

Complete CEPH deployment patterns:
- Multi-OSD configuration per node
- MTU 9000 for storage networks
- Public/private network separation
- Health monitoring and validation

### Real-World Architecture

Based on production 3-node Proxmox cluster:
- **Nodes**: Foxtrot, Golf, Hotel (MINISFORUM MS-A2)
- **CPU**: AMD Ryzen 9 9955HX (16C/32T)
- **RAM**: 64GB DDR5 @ 5600 MT/s
- **Storage**: 3× NVMe (1× 1TB boot, 2× 4TB CEPH)
- **Network**: 4× NICs (2× 10GbE SFP+, 2× 2.5GbE)

## Version History

- 1.0.0 - Initial release with comprehensive Proxmox VE management guidance
