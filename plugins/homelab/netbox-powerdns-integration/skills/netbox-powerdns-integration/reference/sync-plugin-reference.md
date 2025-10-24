# NetBox PowerDNS Sync Plugin Reference

*Source: https://github.com/ArnesSI/netbox-powerdns-sync*

## Overview

A NetBox plugin that automatically generates DNS records in PowerDNS based on NetBox IP Address and Device objects.

## Features

- Automatically generates A, AAAA & PTR records
- Manages multiple DNS Zones across multiple PowerDNS servers
- Flexible rules to match NetBox IP Addresses into DNS zones
- Multiple options to generate DNS names from IP address or Device
- Scheduled sync of DNS zones
- Can add DNS records for new zones immediately
- Per-zone synchronization schedule

## DNS Name Generation

### Zone Matching Priority

When determining the zone for an IP Address, match rules are evaluated in this order:

1. Check if `IPAddress.dns_name` matches any zone
2. Check if IPAddress is assigned to Device/VirtualMachine and if its name matches any zone
3. Check if IPAddress is assigned to FHRPGroup and if its name matches any zone
4. Try to match based on assigned tags (in order):
   - `IPAddress.tags`
   - `Interface.tags`
   - `VMInterface.tags`
   - `Device.tags`
   - `VirtualMachine.tags`
   - `Device.device_role`
   - `VM.role`
5. Use default zone if configured

### Name Generation Methods

Each zone can use multiple naming methods (tried in order):

1. **IP naming method** - Generate name from IP address
2. **Device naming method** - Generate name from Device/VirtualMachine
3. **FHRP group method** - Generate name from FHRP Group

## Installation

### Via pip

```bash
# Activate NetBox virtual environment
source /opt/netbox/venv/bin/activate

# Install plugin
pip install netbox-powerdns-sync
```

### From GitHub

```bash
pip install git+https://github.com/ArnesSI/netbox-powerdns-sync.git@master
```

### Configuration

Add to `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = [
    'netbox_powerdns_sync'
]

PLUGINS_CONFIG = {
    "netbox_powerdns_sync": {
        "ttl_custom_field": "",
        "powerdns_managed_record_comment": "netbox-powerdns-sync",
        "post_save_enabled": False,
    },
}
```

### Apply Migrations

```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py reindex --lazy
```

## Configuration Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ttl_custom_field` | `None` | Name of NetBox Custom field applied to IP Address objects for TTL |
| `powerdns_managed_record_comment` | `"netbox-powerdns-sync"` | Plugin only touches records with this comment. Set to `None` to manage all records |
| `post_save_enabled` | `False` | Immediately create DNS records when creating/updating IP Address, Device, or FHRP Group |

### Custom TTL Field

To set TTL per DNS record:

1. Create NetBox Custom Field:
   - Type: Integer
   - Apply to: IP Address objects
   - Name: e.g., "dns_ttl"

2. Set in plugin config:
   ```python
   "ttl_custom_field": "dns_ttl"
   ```

3. Set TTL value on IP Address objects in NetBox

## Compatibility

| NetBox Version | Plugin Version |
|---------------|----------------|
| 3.5.0-7 | 0.0.1 - 0.0.6 |
| 3.5.8 | 0.0.7 |
| 3.6.x | 0.8.0 |

## Usage Workflow

### 1. Configure DNS Zones in NetBox

Create zones in the plugin interface with:
- Zone name (e.g., `spaceships.work`)
- PowerDNS server connection
- Tag matching rules
- DNS name generation method

### 2. Tag Resources

Apply tags to IP Addresses, Devices, or Interfaces to match zones:

```python
# Example: Tag IP for specific zone
ipaddress.tags.add("production-dns")
```

### 3. Schedule Sync

Configure sync schedule for each zone:
- Immediate (on save)
- Scheduled (cron-style)
- Manual only

### 4. Monitor Sync Results

View sync results in NetBox:
- Records created
- Records updated
- Records deleted
- Sync errors

## Best Practices

### DNS Naming Conventions

For homelab naming like `docker-01-nexus.spaceships.work`:

1. Use Device name as base: `docker-01-nexus`
2. Zone maps to domain: `spaceships.work`
3. Set device naming method in zone config

### Tag Organization

```python
# Production resources
tags: ["production", "dns-auto"]

# Development resources
tags: ["development", "dns-dev"]
```

### TTL Strategy

- Default TTL in zone: 300 (5 minutes)
- Override with custom field for specific records
- Longer TTL for stable infrastructure (3600)
- Shorter TTL for dynamic services (60-300)

### PowerDNS Server Management

- Configure multiple PowerDNS servers for HA
- Use different servers for different zones
- Monitor PowerDNS API connectivity

## Integration Patterns

### With Terraform

Use NetBox as data source, sync DNS automatically:

```hcl
# Terraform creates resource in NetBox
resource "netbox_ip_address" "server" {
  ip_address = "192.168.1.100/24"
  dns_name   = "docker-01-nexus"
  tags       = ["production-dns"]
}

# Plugin automatically creates DNS in PowerDNS
# A record: docker-01-nexus.spaceships.work -> 192.168.1.100
# PTR record: 100.1.168.192.in-addr.arpa -> docker-01-nexus.spaceships.work
```

### With Ansible

Use NetBox dynamic inventory with automatic DNS:

```yaml
---
# Ansible creates VM in Proxmox
- name: Create VM
  proxmox_kvm:
    name: docker-01-nexus
    # ... vm config ...

# Add to NetBox via API
- name: Register in NetBox
  netbox.netbox.netbox_ip_address:
    data:
      address: "192.168.1.100/24"
      dns_name: "docker-01-nexus"
      tags:
        - production-dns

# DNS records created automatically by plugin
```

## Troubleshooting

### Records Not Syncing

1. Check zone matching rules
2. Verify tags applied correctly
3. Check PowerDNS API connectivity
4. Review sync results for errors

### Duplicate Records

If `powerdns_managed_record_comment` is `None`, plugin manages ALL records. Set a comment to limit scope:

```python
"powerdns_managed_record_comment": "netbox-managed"
```

### Performance Issues

- Disable `post_save_enabled` for large environments
- Use scheduled sync instead
- Batch changes before sync

### Name Generation Not Working

1. Check zone name generation method configuration
2. Verify Device/IP naming follows expected pattern
3. Test with manual sync first

## API Endpoints

Plugin adds REST API endpoints:

- `/api/plugins/netbox-powerdns-sync/zones/` - List/manage zones
- `/api/plugins/netbox-powerdns-sync/servers/` - PowerDNS servers
- `/api/plugins/netbox-powerdns-sync/sync-results/` - Sync history

## Example Configuration

### Zone for Production

```python
zone_config = {
    "name": "spaceships.work",
    "server": powerdns_server_prod,
    "default_ttl": 300,
    "naming_methods": ["device", "ip"],
    "tag_match": ["production-dns"],
    "auto_sync": True,
    "sync_schedule": "*/15 * * * *"  # Every 15 minutes
}
```

### Zone for Lab

```python
zone_config = {
    "name": "lab.spaceships.work",
    "server": powerdns_server_dev,
    "default_ttl": 60,
    "naming_methods": ["ip", "device"],
    "tag_match": ["lab-dns"],
    "auto_sync": False  # Manual sync only
}
```
