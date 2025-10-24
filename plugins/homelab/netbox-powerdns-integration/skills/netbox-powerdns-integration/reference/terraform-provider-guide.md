# Terraform NetBox Provider Guide

*Source: https://registry.terraform.io/providers/e-breuninger/netbox/latest/docs*

## Overview

The Terraform NetBox provider enables full lifecycle management of NetBox resources using Infrastructure as Code.

## Version Compatibility

| NetBox Version | Provider Version |
|---------------|------------------|
| v4.3.0 - 4.4.0 | v5.0.0 and up |
| v4.2.2 - 4.2.9 | v4.0.0 - 4.3.1 |
| v4.1.0 - 4.1.11 | v3.10.0 - 3.11.1 |
| v4.0.0 - 4.0.11 | v3.9.0 - 3.9.2 |
| v3.7.0 - 3.7.8 | v3.8.0 - 3.8.9 |
| v3.6.0 - 3.6.9 | v3.7.0 - 3.7.7 |
| v3.5.1 - 3.5.9 | v3.6.x |

**Important**: NetBox makes breaking API changes even in non-major releases. Match provider version to NetBox version.

## Provider Configuration

### Basic Setup

```hcl
terraform {
  required_providers {
    netbox = {
      source  = "e-breuninger/netbox"
      version = "~> 5.0.0"  # Match your NetBox version
    }
  }
}

provider "netbox" {
  server_url = "https://netbox.spaceships.work"
  api_token  = var.netbox_api_token
}
```

### Environment Variables

Configure via environment instead of hard-coding:

```bash
export NETBOX_SERVER_URL="https://netbox.spaceships.work"
export NETBOX_API_TOKEN="your-api-token-here"
```

```hcl
# Provider auto-reads from environment
provider "netbox" {}
```

## Configuration Schema

### Required

- `api_token` (String) - NetBox API authentication token
  - Environment: `NETBOX_API_TOKEN`
- `server_url` (String) - NetBox server URL (with scheme and port)
  - Environment: `NETBOX_SERVER_URL`

### Optional

- `allow_insecure_https` (Boolean) - Allow invalid certificates
  - Environment: `NETBOX_ALLOW_INSECURE_HTTPS`
  - Default: `false`

- `ca_cert_file` (String) - Path to PEM-encoded CA certificate
  - Environment: `NETBOX_CA_CERT_FILE`

- `default_tags` (Set of String) - Tags added to every resource
  - Useful for tracking Terraform-managed resources

- `headers` (Map of String) - Custom headers for all requests
  - Environment: `NETBOX_HEADERS`

- `request_timeout` (Number) - HTTP request timeout (seconds)
  - Environment: `NETBOX_REQUEST_TIMEOUT`

- `skip_version_check` (Boolean) - Skip NetBox version validation
  - Environment: `NETBOX_SKIP_VERSION_CHECK`
  - Default: `false`
  - Useful for: Testing, unsupported versions

- `strip_trailing_slashes_from_url` (Boolean) - Auto-fix URL format
  - Environment: `NETBOX_STRIP_TRAILING_SLASHES_FROM_URL`
  - Default: `true`

## Usage Examples

### Create IP Address

```hcl
resource "netbox_ip_address" "server_ip" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "docker-01-nexus.spaceships.work"
  status      = "active"
  description = "Docker host - Nexus container registry"

  tags = [
    "terraform",
    "production",
    "dns-auto"
  ]
}
```

### Create Device

```hcl
resource "netbox_device" "proxmox_node" {
  name        = "foxtrot"
  device_type = netbox_device_type.minisforum_ms_a2.id
  role        = netbox_device_role.hypervisor.id
  site        = netbox_site.homelab.id

  primary_ip4 = netbox_ip_address.foxtrot_mgmt.id

  tags = [
    "terraform",
    "proxmox",
    "cluster-matrix"
  ]

  comments = "Proxmox node in Matrix cluster - AMD Ryzen 9 9955HX"
}
```

### Create Prefix

```hcl
resource "netbox_prefix" "vlan_30_mgmt" {
  prefix      = "192.168.3.0/24"
  vlan        = netbox_vlan.management.id
  status      = "active"
  description = "Management network for Proxmox cluster"

  tags = [
    "terraform",
    "mgmt-network"
  ]
}
```

### Create VLAN

```hcl
resource "netbox_vlan" "management" {
  vid         = 30
  name        = "MGMT"
  site        = netbox_site.homelab.id
  status      = "active"
  description = "Management VLAN for infrastructure"

  tags = ["terraform"]
}
```

## Integration Patterns

### With Proxmox Provider

```hcl
# Create VM in Proxmox
resource "proxmox_vm_qemu" "docker_host" {
  name        = "docker-01-nexus"
  target_node = "foxtrot"
  # ... vm config ...
}

# Register in NetBox
resource "netbox_ip_address" "docker_host_ip" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "${proxmox_vm_qemu.docker_host.name}.spaceships.work"
  description = "Docker host for Nexus registry"

  tags = [
    "terraform",
    "production-dns",
    "docker-host"
  ]
}

# DNS record auto-created by netbox-powerdns-sync plugin
```

### Data Sources

Query existing NetBox data:

```hcl
# Get all production IPs
data "netbox_ip_addresses" "production" {
  filter {
    name  = "tag"
    value = "production"
  }
}

# Get device details
data "netbox_device" "proxmox_node" {
  name = "foxtrot"
}

# Use in other resources
resource "proxmox_vm_qemu" "new_vm" {
  target_node = data.netbox_device.proxmox_node.name
  # ... config ...
}
```

### Dynamic Inventory for Ansible

```hcl
# Export NetBox data for Ansible
output "ansible_inventory" {
  value = {
    for device in data.netbox_devices.all.devices :
    device.name => {
      ansible_host = device.primary_ip4_address
      device_role  = device.role
      site         = device.site
      tags         = device.tags
    }
  }
}
```

Save to file:

```bash
terraform output -json ansible_inventory > inventory.json
```

## Best Practices

### 1. Use Default Tags

Track all Terraform-managed resources:

```hcl
provider "netbox" {
  server_url   = var.netbox_url
  api_token    = var.netbox_token
  default_tags = ["terraform", "iac"]
}
```

### 2. Organize with Modules

```hcl
module "vm_network" {
  source = "./modules/netbox-vm"

  vm_name    = "docker-01"
  ip_address = "192.168.1.100/24"
  vlan_id    = 30
  dns_zone   = "spaceships.work"
}
```

### 3. Use Variables for Secrets

Never hard-code tokens:

```hcl
variable "netbox_api_token" {
  description = "NetBox API token"
  type        = string
  sensitive   = true
}
```

### 4. State Management

Use remote state for team collaboration:

```hcl
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "netbox/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### 5. Version Pinning

Pin provider version to prevent breaking changes:

```hcl
terraform {
  required_providers {
    netbox = {
      source  = "e-breuninger/netbox"
      version = "= 5.0.0"  # Exact version
    }
  }
}
```

## Common Workflows

### 1. VM Provisioning Workflow

```hcl
# 1. Reserve IP in NetBox
resource "netbox_ip_address" "vm_ip" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "app-server.spaceships.work"
  status      = "reserved"
  description = "Reserved for new application server"
}

# 2. Create VM in Proxmox
resource "proxmox_vm_qemu" "app_server" {
  # ... config using netbox_ip_address.vm_ip.ip_address ...
}

# 3. Mark IP as active
resource "netbox_ip_address" "vm_ip_active" {
  ip_address  = netbox_ip_address.vm_ip.ip_address
  status      = "active"  # Update status
  description = "Application server - deployed ${timestamp()}"
}
```

### 2. DNS Automation Workflow

```hcl
# Create IP with DNS name and auto-DNS tag
resource "netbox_ip_address" "service" {
  ip_address  = "192.168.1.200/24"
  dns_name    = "service-01-api.spaceships.work"

  tags = [
    "terraform",
    "production-dns"  # Triggers netbox-powerdns-sync
  ]
}

# DNS records created automatically by plugin
# No manual DNS configuration needed
```

### 3. Network Documentation Workflow

```hcl
# Document entire network in NetBox
module "network_documentation" {
  source = "./modules/network"

  site_name = "homelab"

  vlans = {
    "mgmt"    = { vid = 30, prefix = "192.168.3.0/24" }
    "storage" = { vid = 40, prefix = "192.168.5.0/24" }
    "ceph"    = { vid = 50, prefix = "192.168.7.0/24" }
  }

  devices = var.proxmox_nodes
}
```

## Troubleshooting

### Version Mismatch Warning

```
Warning: NetBox version X.Y.Z is not officially supported by provider version A.B.C
```

**Solution**: Use matching provider version or set `skip_version_check = true`

### API Authentication Errors

```
Error: authentication failed
```

**Solution**:
1. Verify `api_token` is valid
2. Check token has required permissions
3. Ensure `server_url` includes scheme (`https://`)

### SSL Certificate Errors

```
Error: x509: certificate signed by unknown authority
```

**Solution**:
```hcl
provider "netbox" {
  server_url          = var.netbox_url
  api_token           = var.netbox_token
  ca_cert_file        = "/path/to/ca.pem"
  # OR for dev/testing only:
  # allow_insecure_https = true
}
```

### Trailing Slash Issues

```
Error: invalid URL format
```

**Solution**: Remove trailing slashes from `server_url` or let provider auto-fix:

```hcl
provider "netbox" {
  server_url = "https://netbox.example.com"  # No trailing slash
  strip_trailing_slashes_from_url = true     # Auto-fix if present
}
```

## Further Resources

- [Provider GitHub Repository](https://github.com/e-breuninger/terraform-provider-netbox)
- [NetBox Official Documentation](https://docs.netbox.dev/)
- [NetBox API Reference](https://demo.netbox.dev/api/docs/)
