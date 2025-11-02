# NetBox PowerDNS Integration

Expert guidance for implementing NetBox as your source of truth for infrastructure documentation and automating DNS
record management with PowerDNS.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install netbox-powerdns-integration:

```bash
/plugin install netbox-powerdns-integration@lunar-claude
```

## Components

### Skills

- **netbox-powerdns-integration** - Comprehensive skill for NetBox and PowerDNS integration
  - NetBox API usage (sites, devices, VMs, IPs, prefixes, VLANs)
  - DNS naming conventions (`service-NN-purpose.domain` pattern)
  - NetBox + PowerDNS sync plugin configuration
  - Terraform NetBox provider integration
  - Ansible dynamic inventory from NetBox
  - IPAM queries and management
  - Infrastructure documentation patterns

## Usage

### Autonomous Mode

Simply ask Claude to help with NetBox/PowerDNS:

```text
"Query NetBox API for all VMs in the matrix cluster"
"Create a VM in NetBox with auto-assigned IP"
"Set up NetBox PowerDNS sync plugin"
"Validate DNS naming convention for docker-01-nexus.spaceships.work"
"Create Terraform configuration using NetBox provider"
```

Claude will automatically use the netbox-powerdns-integration skill.

## How It Works

The netbox-powerdns-integration skill provides comprehensive guidance on:

- **NetBox API**: Complete pynetbox examples for querying infrastructure
- **DNS Automation**: Real-time sync between NetBox and PowerDNS
- **Naming Conventions**: `service-NN-purpose.domain` pattern validation
- **Terraform Integration**: NetBox provider usage for IaC
- **Ansible Integration**: Dynamic inventory from NetBox as source of truth
- **IPAM Management**: Prefix utilization, IP assignment, availability queries

## Supporting Documentation

The skill includes extensive reference material:

- `/reference/` - API guide, data models, sync plugin, Terraform provider, best practices
- `/workflows/` - Naming conventions, DNS automation, Ansible dynamic inventory
- `/examples/` - Real Terraform configurations with NetBox provider
- `/tools/` - Python API clients (uv-based)
  - `netbox_api_client.py` - Comprehensive NetBox API client
  - `netbox_vm_create.py` - Create VMs with IP assignment
  - `netbox_ipam_query.py` - Advanced IPAM queries
  - `validate_dns_naming.py` - DNS naming validation
- `/anti-patterns/` - Common mistakes and how to avoid them

## Key Features

### DNS Naming Convention

Structured pattern: `<service>-<number>-<purpose>.<domain>`

Examples:

- `docker-01-nexus.spaceships.work` - Docker host #1 running Nexus
- `k8s-01-master.spaceships.work` - Kubernetes master node #1
- `proxmox-foxtrot-mgmt.spaceships.work` - Proxmox mgmt interface

### Automated DNS Records

NetBox PowerDNS sync plugin creates DNS records automatically when:

1. IP address created in NetBox with `dns_name`
2. Resource tagged with zone trigger (e.g., `production-dns`)
3. A and PTR records created in PowerDNS automatically
4. No manual DNS configuration needed

### Infrastructure as Code

- Terraform NetBox provider for managing NetBox resources
- Ansible dynamic inventory using NetBox as source of truth
- Python API clients for automation

### Production-Ready

Based on real-world homelab infrastructure with multi-site deployment patterns.

## Version History

- 1.0.0 - Initial release with comprehensive NetBox PowerDNS integration guidance
