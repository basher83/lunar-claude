# NetBox Best Practices for Virgo-Core

**NetBox Version:** 4.3.0
**Audience:** Infrastructure automation engineers

Comprehensive best practices for using NetBox as the source of truth for the Matrix cluster infrastructure, including data organization, security, performance, and integration patterns.

---

## Table of Contents

- [Data Organization](#data-organization)
- [Naming Conventions](#naming-conventions)
- [IP Address Management](#ip-address-management)
- [Device Management](#device-management)
- [Virtualization](#virtualization)
- [Tagging Strategy](#tagging-strategy)
- [Security](#security)
- [Performance](#performance)
- [API Integration](#api-integration)
- [Automation Patterns](#automation-patterns)
- [Troubleshooting](#troubleshooting)

---

## Data Organization

### Hierarchical Structure

Follow this order when setting up infrastructure in NetBox:

```text
1. Sites          → Create physical locations first
2. Prefixes       → Define IP networks (IPAM)
3. VLANs          → Network segmentation
4. Device Types   → Hardware models
5. Device Roles   → Purpose categories
6. Clusters       → Virtualization clusters
7. Devices        → Physical hardware
8. Interfaces     → Network interfaces
9. IP Addresses   → Assign IPs to interfaces
10. VMs           → Virtual machines
```

**Why this order?**

- Parent objects must exist before children
- Avoids circular dependencies
- Enables atomic operations

### Site Organization

**✅ Good:**

```python
# One site per physical location
site = nb.dcim.sites.create(
    name="Matrix Cluster",
    slug="matrix",
    description="3-node Proxmox VE cluster at home lab",
    tags=[{"name": "production"}, {"name": "homelab"}]
)
```

**❌ Bad:**

```python
# Don't create separate sites for logical groupings
site_proxmox = nb.dcim.sites.create(name="Proxmox Nodes", ...)
site_vms = nb.dcim.sites.create(name="Virtual Machines", ...)
```

Use **device roles** and **tags** for logical grouping, not separate sites.

### Consistent Data Entry

**Required fields:** Always populate these

```python
device = nb.dcim.devices.create(
    name="foxtrot",                    # ✅ Required
    device_type=device_type.id,        # ✅ Required
    device_role=role.id,               # ✅ Required
    site=site.id,                      # ✅ Required
    status="active",                   # ✅ Required
    description="AMD Ryzen 9 9955HX",  # ✅ Recommended
    tags=[{"name": "proxmox-node"}]    # ✅ Recommended
)
```

**Optional but recommended:**

- `description` - Hardware specs, purpose
- `tags` - For filtering and automation
- `comments` - Additional notes
- `custom_fields` - Serial numbers, purchase dates

---

## Naming Conventions

### Device Names

**✅ Use hostname only (no domain):**

```python
device = nb.dcim.devices.create(name="foxtrot", ...)   # ✅ Good
device = nb.dcim.devices.create(name="foxtrot.spaceships.work", ...)  # ❌ Bad
```

**Rationale:** Domain goes in DNS name field, not device name.

### Interface Names

**✅ Match actual OS interface names:**

```python
# Linux
interface = nb.dcim.interfaces.create(name="enp1s0f0", ...)  # ✅ Good

# Not generic names
interface = nb.dcim.interfaces.create(name="eth0", ...)      # ❌ Bad (unless actually eth0)
```

**Why?** Enables automation that references interfaces by name.

### DNS Naming Convention

Follow the Matrix cluster pattern: **`<service>-<number>-<purpose>.<domain>`**

```python
# ✅ Good examples
dns_name="docker-01-nexus.spaceships.work"
dns_name="k8s-01-master.spaceships.work"
dns_name="proxmox-foxtrot-mgmt.spaceships.work"

# ❌ Bad examples
dns_name="server1.spaceships.work"         # Not descriptive
dns_name="nexus.spaceships.work"           # Missing number
dns_name="DOCKER-01.spaceships.work"       # Uppercase not allowed
```

See [../workflows/naming-conventions.md](../workflows/naming-conventions.md) for complete rules.

### Slugs

**✅ Lowercase with hyphens:**

```python
site = nb.dcim.sites.create(slug="matrix", ...)        # ✅ Good
site = nb.dcim.sites.create(slug="Matrix_Cluster", ...)  # ❌ Bad
```

**Pattern:** `^[a-z0-9-]+$`

---

## IP Address Management

### Plan IP Hierarchy

**Matrix cluster example:**

```text
192.168.0.0/16 (Home network supernet)
├── 192.168.3.0/24 (Management)
│   ├── 192.168.3.1     (Gateway)
│   ├── 192.168.3.5-7   (Proxmox nodes)
│   ├── 192.168.3.10+   (VMs)
│   └── 192.168.3.200+  (Reserved for future)
├── 192.168.5.0/24 (CEPH Public, MTU 9000)
├── 192.168.7.0/24 (CEPH Private, MTU 9000)
└── 192.168.8.0/24 (Corosync, VLAN 9)
```

### Use Prefix Roles

Create roles for clarity:

```python
# Create roles
role_mgmt = nb.ipam.roles.create(name='Management', slug='management')
role_storage = nb.ipam.roles.create(name='Storage', slug='storage')
role_cluster = nb.ipam.roles.create(name='Cluster', slug='cluster')

# Apply to prefixes
prefix = nb.ipam.prefixes.create(
    prefix='192.168.3.0/24',
    role=role_mgmt.id,
    description='Management network for Matrix cluster'
)
```

### Reserve Important IPs

**✅ Explicitly reserve gateway, broadcast, network addresses:**

```python
# Gateway
gateway = nb.ipam.ip_addresses.create(
    address='192.168.3.1/24',
    status='active',
    role='anycast',
    description='Management network gateway'
)

# DNS servers
dns1 = nb.ipam.ip_addresses.create(
    address='192.168.3.2/24',
    status='reserved',
    description='Primary DNS server'
)
```

### Use Prefixes as IP Pools

**✅ Enable automatic IP assignment:**

```python
prefix = nb.ipam.prefixes.create(
    prefix='192.168.3.0/24',
    is_pool=True,  # ✅ Allow automatic IP assignment
    ...
)

# Get next available IP
ip = prefix.available_ips.create(dns_name='docker-02.spaceships.work')
```

**❌ Don't manually track available IPs** - let NetBox do it.

### IP Status Values

Use appropriate status:

| Status | Use Case |
|--------|----------|
| `active` | Currently in use |
| `reserved` | Reserved for specific purpose |
| `deprecated` | Planned for decommission |
| `dhcp` | Managed by DHCP server |

```python
# Production VM
ip = nb.ipam.ip_addresses.create(address='192.168.3.10/24', status='active')

# Future expansion
ip = nb.ipam.ip_addresses.create(address='192.168.3.50/24', status='reserved')
```

### VRF for Isolation

**Use VRFs for true isolation:**

```python
# Management VRF (enforce unique IPs)
vrf_mgmt = nb.ipam.vrfs.create(
    name='management',
    enforce_unique=True,
    description='Management network VRF'
)

# Lab VRF (allow overlapping IPs)
vrf_lab = nb.ipam.vrfs.create(
    name='lab',
    enforce_unique=False,
    description='Lab/testing VRF'
)
```

**When to use VRFs:**

- Multiple environments (prod, dev, lab)
- Overlapping IP ranges
- Security isolation

---

## Device Management

### Create Device Types First

**✅ Always create device type before devices:**

```python
# 1. Create manufacturer
manufacturer = nb.dcim.manufacturers.get(slug='minisforum')
if not manufacturer:
    manufacturer = nb.dcim.manufacturers.create(
        name='MINISFORUM',
        slug='minisforum'
    )

# 2. Create device type
device_type = nb.dcim.device_types.create(
    manufacturer=manufacturer.id,
    model='MS-A2',
    slug='ms-a2',
    u_height=0,  # Not rack mounted
    is_full_depth=False
)

# 3. Create device
device = nb.dcim.devices.create(
    name='foxtrot',
    device_type=device_type.id,
    ...
)
```

### Use Device Roles Consistently

**Create specific roles:**

```python
roles = [
    ('Proxmox Node', 'proxmox-node', '2196f3'),    # Blue
    ('Docker Host', 'docker-host', '4caf50'),      # Green
    ('K8s Master', 'k8s-master', 'ff9800'),        # Orange
    ('K8s Worker', 'k8s-worker', 'ffc107'),        # Amber
    ('Storage', 'storage', '9c27b0'),              # Purple
]

for name, slug, color in roles:
    nb.dcim.device_roles.create(
        name=name,
        slug=slug,
        color=color,
        vm_role=True  # If role applies to VMs too
    )
```

**✅ Consistent naming helps automation:**

```python
# Get all Proxmox nodes
proxmox_nodes = nb.dcim.devices.filter(role='proxmox-node')

# Get all Kubernetes workers
k8s_workers = nb.virtualization.virtual_machines.filter(role='k8s-worker')
```

### Always Set Primary IP

**✅ Set primary IP after creating device and IPs:**

```python
# Create device
device = nb.dcim.devices.create(name='foxtrot', ...)

# Create interface
iface = nb.dcim.interfaces.create(device=device.id, name='enp2s0', ...)

# Create IP
ip = nb.ipam.ip_addresses.create(
    address='192.168.3.5/24',
    assigned_object_type='dcim.interface',
    assigned_object_id=iface.id
)

# ✅ Set as primary (critical for automation!)
device.primary_ip4 = ip.id
device.save()
```

**Why?** Primary IP is used by:

- Ansible dynamic inventory
- Monitoring tools
- DNS automation

### Document Interfaces

**✅ Include descriptions:**

```python
# Management
mgmt = nb.dcim.interfaces.create(
    device=device.id,
    name='enp2s0',
    type='2.5gbase-t',
    mtu=1500,
    description='Management interface (vmbr0)',
    tags=[{'name': 'management'}]
)

# CEPH public
ceph_pub = nb.dcim.interfaces.create(
    device=device.id,
    name='enp1s0f0',
    type='10gbase-x-sfpp',
    mtu=9000,
    description='CEPH public network (vmbr1)',
    tags=[{'name': 'ceph-public'}, {'name': 'jumbo-frames'}]
)
```

---

## Virtualization

### Create Cluster First

**✅ Create cluster before VMs:**

```python
# 1. Get/create cluster type
cluster_type = nb.virtualization.cluster_types.get(slug='proxmox')
if not cluster_type:
    cluster_type = nb.virtualization.cluster_types.create(
        name='Proxmox VE',
        slug='proxmox'
    )

# 2. Create cluster
cluster = nb.virtualization.clusters.create(
    name='Matrix',
    type=cluster_type.id,
    site=site.id,
    description='3-node Proxmox VE 9.x cluster'
)

# 3. Create VMs in cluster
vm = nb.virtualization.virtual_machines.create(
    name='docker-01',
    cluster=cluster.id,
    ...
)
```

### Standardize VM Sizing

**✅ Use consistent resource allocations:**

| Role | vCPUs | Memory (MB) | Disk (GB) |
|------|-------|-------------|-----------|
| Small (dev) | 2 | 2048 | 20 |
| Medium (app) | 4 | 8192 | 100 |
| Large (database) | 8 | 16384 | 200 |
| XL (compute) | 16 | 32768 | 500 |

```python
VM_SIZES = {
    'small': {'vcpus': 2, 'memory': 2048, 'disk': 20},
    'medium': {'vcpus': 4, 'memory': 8192, 'disk': 100},
    'large': {'vcpus': 8, 'memory': 16384, 'disk': 200},
}

# Create VM with standard size
vm = nb.virtualization.virtual_machines.create(
    name='docker-01',
    cluster=cluster.id,
    **VM_SIZES['medium']
)
```

### VM Network Configuration

**✅ Complete network setup:**

```python
# 1. Create VM
vm = nb.virtualization.virtual_machines.create(...)

# 2. Create interface
vm_iface = nb.virtualization.interfaces.create(
    virtual_machine=vm.id,
    name='eth0',
    type='virtual',
    enabled=True,
    mtu=1500
)

# 3. Assign IP from pool
prefix = nb.ipam.prefixes.get(prefix='192.168.3.0/24')
vm_ip = prefix.available_ips.create(
    dns_name='docker-01-nexus.spaceships.work',
    assigned_object_type='virtualization.vminterface',
    assigned_object_id=vm_iface.id,
    tags=[{'name': 'production-dns'}]  # ✅ Triggers PowerDNS sync
)

# 4. Set as primary IP
vm.primary_ip4 = vm_ip.id
vm.save()
```

---

## Tagging Strategy

### Tag Categories

Organize tags by purpose:

**Infrastructure Type:**

- `proxmox-node`, `ceph-node`, `docker-host`, `k8s-master`, `k8s-worker`

**Environment:**

- `production`, `staging`, `development`, `lab`

**DNS Automation:**

- `production-dns`, `lab-dns` (triggers PowerDNS sync)

**Management:**

- `terraform`, `ansible`, `manual`

**Networking:**

- `management`, `ceph-public`, `ceph-private`, `jumbo-frames`

### Tag Naming Convention

**✅ Lowercase with hyphens:**

```python
tags = [
    {'name': 'proxmox-node'},      # ✅ Good
    {'name': 'production-dns'},    # ✅ Good
    {'name': 'Proxmox Node'},      # ❌ Bad (spaces, capitals)
    {'name': 'production_dns'},    # ❌ Bad (underscores)
]
```

### Apply Tags Consistently

**✅ Tag at multiple levels:**

```python
# Tag device
device = nb.dcim.devices.create(
    name='foxtrot',
    tags=[{'name': 'proxmox-node'}, {'name': 'ceph-node'}, {'name': 'production'}]
)

# Tag interface
iface = nb.dcim.interfaces.create(
    device=device.id,
    name='enp1s0f0',
    tags=[{'name': 'ceph-public'}, {'name': 'jumbo-frames'}]
)

# Tag IP
ip = nb.ipam.ip_addresses.create(
    address='192.168.3.5/24',
    tags=[{'name': 'production-dns'}, {'name': 'terraform'}]
)
```

**Why?** Enables granular filtering:

```bash
# Get all CEPH nodes
ansible-playbook -i netbox-inventory.yml setup-ceph.yml --limit tag_ceph_node

# Get all production DNS-enabled IPs
ips = nb.ipam.ip_addresses.filter(tag='production-dns')
```

---

## Security

### API Token Management

**✅ Store tokens in Infisical (Virgo-Core standard):**

```python
from infisical import InfisicalClient

def get_netbox_token() -> str:
    """Get NetBox API token from Infisical."""
    client = InfisicalClient()
    secret = client.get_secret(
        secret_name="NETBOX_API_TOKEN",
        project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
        environment="prod",
        path="/matrix"
    )
    return secret.secret_value

# Use token
nb = pynetbox.api('https://netbox.spaceships.work', token=get_netbox_token())
```

**❌ Never hardcode tokens:**

```python
# ❌ NEVER DO THIS
token = "a1b2c3d4e5f6..."
nb = pynetbox.api(url, token=token)
```

### Use Minimal Permissions

Create tokens with appropriate scopes:

| Use Case | Permissions |
|----------|-------------|
| Read-only queries | Read only |
| Terraform automation | Read + Write (DCIM, IPAM, Virtualization) |
| Full automation | Read + Write (all) |
| Emergency admin | Full access |

**✅ Create separate tokens for different purposes:**

```text
NETBOX_API_TOKEN_READONLY   → Read-only queries
NETBOX_API_TOKEN_TERRAFORM  → Terraform automation
NETBOX_API_TOKEN_ANSIBLE    → Ansible dynamic inventory
```

### HTTPS Only

**✅ Always use HTTPS in production:**

```python
# ✅ Production
nb = pynetbox.api('https://netbox.spaceships.work', token=token)

# ❌ Never HTTP in production
nb = pynetbox.api('http://netbox.spaceships.work', token=token)
```

**For self-signed certs (dev/lab only):**

```python
# ⚠️ Dev/testing only
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

nb = pynetbox.api(
    'https://netbox.local',
    token=token,
    ssl_verify=False  # Only for self-signed certs in lab
)
```

### Rotate Tokens Regularly

**Best practice:** Rotate every 90 days

```bash
# 1. Create new token in NetBox UI
# 2. Update Infisical secret
infisical secrets set NETBOX_API_TOKEN="new-token-here"

# 3. Test new token
./tools/netbox_api_client.py sites list

# 4. Delete old token in NetBox UI
```

### Audit API Usage

**✅ Log API calls in production:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/var/log/netbox-api.log'
)

logger = logging.getLogger(__name__)

def audit_api_call(action: str, resource: str, details: dict):
    """Log API calls for security audit."""
    logger.info(f"API Call: {action} {resource} - User: {os.getenv('USER')} - {details}")

# Usage
ip = nb.ipam.ip_addresses.create(address='192.168.1.1/24')
audit_api_call('CREATE', 'ip-address', {'address': '192.168.1.1/24'})
```

---

## Performance

### Use Filtering Server-Side

**✅ Filter on server:**

```python
# ✅ Efficient: Server filters results
devices = nb.dcim.devices.filter(site='matrix', status='active')
```

**❌ Don't filter client-side:**

```python
# ❌ Inefficient: Downloads all devices then filters
all_devices = nb.dcim.devices.all()
matrix_devices = [d for d in all_devices if d.site.slug == 'matrix']
```

### Request Only Needed Fields

**✅ Use field selection:**

```python
# Get only specific fields
devices = nb.dcim.devices.filter(site='matrix', fields=['name', 'primary_ip4'])
```

### Use Pagination for Large Datasets

**✅ Process in batches:**

```python
# Paginate automatically
for device in nb.dcim.devices.filter(site='matrix'):
    process_device(device)  # pynetbox handles pagination

# Manual pagination for control
page_size = 100
offset = 0
while True:
    devices = nb.dcim.devices.filter(limit=page_size, offset=offset)
    if not devices:
        break
    for device in devices:
        process_device(device)
    offset += page_size
```

### Cache Lookups

**✅ Cache static data:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_site(site_slug: str):
    """Cached site lookup."""
    return nb.dcim.sites.get(slug=site_slug)

@lru_cache(maxsize=256)
def get_device_type(slug: str):
    """Cached device type lookup."""
    return nb.dcim.device_types.get(slug=slug)
```

### Use Bulk Operations

**✅ Bulk create is faster:**

```python
# ✅ Fast: Bulk create
ips = [
    {'address': f'192.168.3.{i}/24', 'status': 'active'}
    for i in range(10, 20)
]
nb.ipam.ip_addresses.create(ips)

# ❌ Slow: Loop with individual creates
for i in range(10, 20):
    nb.ipam.ip_addresses.create(address=f'192.168.3.{i}/24', status='active')
```

---

## API Integration

### Error Handling

**✅ Always handle errors:**

```python
import pynetbox
from requests.exceptions import HTTPError

try:
    device = nb.dcim.devices.get(name='foxtrot')
    if not device:
        console.print("[yellow]Device not found[/yellow]")
        return None

except HTTPError as e:
    if e.response.status_code == 404:
        console.print("[red]Resource not found[/red]")
    elif e.response.status_code == 403:
        console.print("[red]Permission denied[/red]")
    else:
        console.print(f"[red]HTTP Error: {e}[/red]")
    sys.exit(1)

except pynetbox.RequestError as e:
    console.print(f"[red]NetBox API Error: {e.error}[/red]")
    sys.exit(1)

except Exception as e:
    console.print(f"[red]Unexpected error: {e}[/red]")
    sys.exit(1)
```

### Validate Before Creating

**✅ Validate input before API calls:**

```python
import ipaddress
import re

def validate_ip(ip_str: str) -> bool:
    """Validate IP address format."""
    try:
        ipaddress.ip_interface(ip_str)
        return True
    except ValueError:
        return False

def validate_dns_name(name: str) -> bool:
    """Validate DNS naming convention."""
    pattern = r'^[a-z0-9-]+-\d{2}-[a-z0-9-]+\.[a-z0-9.-]+$'
    return bool(re.match(pattern, name))

# Use before API calls
if not validate_ip(ip_address):
    raise ValueError(f"Invalid IP address: {ip_address}")

if not validate_dns_name(dns_name):
    raise ValueError(f"Invalid DNS name: {dns_name}")

ip = nb.ipam.ip_addresses.create(address=ip_address, dns_name=dns_name)
```

### Check Before Create

**✅ Check existence before creating:**

```python
# Check if device exists
device = nb.dcim.devices.get(name='foxtrot')

if device:
    console.print("[yellow]Device already exists, updating...[/yellow]")
    device.status = 'active'
    device.save()
else:
    console.print("[green]Creating new device...[/green]")
    device = nb.dcim.devices.create(name='foxtrot', ...)
```

---

## Automation Patterns

### Idempotent Operations

**✅ Design operations to be safely re-run:**

```python
def ensure_vm_exists(name: str, cluster: str, **kwargs) -> pynetbox.core.response.Record:
    """Ensure VM exists (idempotent)."""
    # Check if exists
    vm = nb.virtualization.virtual_machines.get(name=name)

    if vm:
        # Update if needed
        updated = False
        for key, value in kwargs.items():
            if getattr(vm, key) != value:
                setattr(vm, key, value)
                updated = True

        if updated:
            vm.save()
            console.print(f"[yellow]Updated VM: {name}[/yellow]")
        else:
            console.print(f"[green]VM unchanged: {name}[/green]")

        return vm
    else:
        # Create new
        vm = nb.virtualization.virtual_machines.create(
            name=name,
            cluster=nb.virtualization.clusters.get(name=cluster).id,
            **kwargs
        )
        console.print(f"[green]Created VM: {name}[/green]")
        return vm
```

### Terraform Integration

See [terraform-provider-guide.md](terraform-provider-guide.md) for complete examples.

**Key pattern:**

```hcl
# Use NetBox as data source
data "netbox_prefix" "management" {
  prefix = "192.168.3.0/24"
}

# Create IP in NetBox via Terraform
resource "netbox_ip_address" "vm_ip" {
  ip_address  = cidrhost(data.netbox_prefix.management.prefix, 10)
  dns_name    = "docker-01-nexus.spaceships.work"
  status      = "active"
  tags        = ["terraform", "production-dns"]
}
```

### Ansible Dynamic Inventory

See [../workflows/ansible-dynamic-inventory.md](../workflows/ansible-dynamic-inventory.md).

**Key pattern:**

```yaml
# netbox-dynamic-inventory.yml
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...
group_by:
  - device_roles
  - tags
  - site
```

---

## Troubleshooting

### Common Issues

**Problem:** "Permission denied" errors

**Solution:** Check API token permissions

```bash
# Test token
curl -H "Authorization: Token YOUR_TOKEN" \
  https://netbox.spaceships.work/api/
```

**Problem:** IP not syncing to PowerDNS

**Solution:** Check tags

```python
# IP must have tag matching zone rules
ip = nb.ipam.ip_addresses.get(address='192.168.3.10/24')
print(f"Tags: {[tag.name for tag in ip.tags]}")
# Must include 'production-dns' or matching tag
```

**Problem:** Slow API queries

**Solution:** Use filtering and pagination

```python
# ❌ Slow
all_devices = nb.dcim.devices.all()

# ✅ Fast
devices = nb.dcim.devices.filter(site='matrix', limit=50)
```

### Debug Mode

**Enable verbose logging:**

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now pynetbox will log all API calls
nb = pynetbox.api('https://netbox.spaceships.work', token=token)
devices = nb.dcim.devices.all()
```

---

## Related Documentation

- [NetBox API Guide](netbox-api-guide.md) - Complete API reference
- [NetBox Data Models](netbox-data-models.md) - Data model relationships
- [DNS Naming Conventions](../workflows/naming-conventions.md) - Naming rules
- [Terraform Provider Guide](terraform-provider-guide.md) - Terraform integration
- [Tools: netbox_api_client.py](../tools/netbox_api_client.py) - Working examples

---

**Next:** Review [API Integration Patterns](netbox-api-guide.md#api-integration)
