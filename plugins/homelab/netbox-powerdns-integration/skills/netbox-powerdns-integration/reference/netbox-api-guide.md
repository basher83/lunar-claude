# NetBox REST API Guide

**NetBox Version:** 4.3.0
**API Documentation:** <https://netboxlabs.com/docs/netbox/en/stable/>

Complete reference for working with the NetBox REST API, including authentication, common operations, filtering, pagination, and error handling patterns for the Virgo-Core infrastructure.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [API Endpoints Structure](#api-endpoints-structure)
- [Common Operations](#common-operations)
- [Filtering and Search](#filtering-and-search)
- [Pagination](#pagination)
- [Bulk Operations](#bulk-operations)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Python Client (pynetbox)](#python-client-pynetbox)
- [Best Practices](#best-practices)
- [Security](#security)

---

## Quick Start

### Using curl

```bash
# Get all sites
curl -H "Authorization: Token YOUR_API_TOKEN" \
  https://netbox.spaceships.work/api/dcim/sites/

# Create a new IP address
curl -X POST \
  -H "Authorization: Token YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "192.168.3.10/24",
    "dns_name": "docker-01-nexus.spaceships.work",
    "status": "active",
    "tags": ["production-dns", "terraform"]
  }' \
  https://netbox.spaceships.work/api/ipam/ip-addresses/
```

### Using pynetbox (Python)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pynetbox>=7.0.0", "infisical-python>=2.3.3"]
# ///

import pynetbox
from infisical import InfisicalClient

# Get token from Infisical (following Virgo-Core security pattern)
client = InfisicalClient()
token = client.get_secret(
    secret_name="NETBOX_API_TOKEN",
    project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
    environment="prod",
    path="/matrix"
).secret_value

# Connect to NetBox
nb = pynetbox.api('https://netbox.spaceships.work', token=token)

# Query sites
sites = nb.dcim.sites.all()
for site in sites:
    print(f"{site.name}: {site.description}")
```

See [../tools/netbox_api_client.py](../tools/netbox_api_client.py) for complete working example.

---

## Authentication

### Token Authentication

NetBox uses token-based authentication for API access.

#### Creating a Token

1. Log into NetBox web UI
2. Navigate to **User** → **API Tokens**
3. Click **Add Token**
4. Configure permissions (read, write)
5. Copy token (only shown once)

#### Storing Tokens Securely

**❌ NEVER hardcode tokens:**

```python
# DON'T DO THIS
token = "a1b2c3d4e5f6..."  # NEVER hardcode!
```

**✅ Use Infisical (Virgo-Core standard):**

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
```

See [netbox-best-practices.md](netbox-best-practices.md#security) for complete security patterns.

#### Using Tokens

**With curl:**

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  https://netbox.spaceships.work/api/dcim/sites/
```

**With pynetbox:**

```python
import pynetbox
nb = pynetbox.api('https://netbox.spaceships.work', token='YOUR_TOKEN')
```

### Session Authentication

Session authentication is available when using the NetBox web interface (browser-based). Not recommended for API automation.

---

## API Endpoints Structure

All API endpoints are prefixed with `/api/` followed by the app name:

| Prefix | Purpose | Example Endpoints |
|--------|---------|-------------------|
| `/api/dcim/` | Data Center Infrastructure Management | sites, racks, devices, cables |
| `/api/ipam/` | IP Address Management | ip-addresses, prefixes, vlans, vrfs |
| `/api/virtualization/` | Virtual Machines | virtual-machines, clusters |
| `/api/circuits/` | Circuit Management | circuits, providers |
| `/api/tenancy/` | Multi-tenancy | tenants, tenant-groups |
| `/api/extras/` | Additional Features | tags, custom-fields, webhooks |

### Common Endpoint Patterns

All endpoints follow REST conventions:

```text
GET    /api/{app}/{model}/          # List all objects
POST   /api/{app}/{model}/          # Create new object(s)
GET    /api/{app}/{model}/{id}/     # Get specific object
PUT    /api/{app}/{model}/{id}/     # Full update
PATCH  /api/{app}/{model}/{id}/     # Partial update
DELETE /api/{app}/{model}/{id}/     # Delete object
```

---

## Common Operations

### Sites

**List all sites:**

```bash
GET /api/dcim/sites/
```

```python
sites = nb.dcim.sites.all()
```

**Create a site:**

```bash
POST /api/dcim/sites/
{
  "name": "Matrix Cluster",
  "slug": "matrix",
  "status": "active",
  "description": "3-node Proxmox cluster",
  "region": null,
  "tags": ["proxmox", "production"]
}
```

```python
site = nb.dcim.sites.create(
    name="Matrix Cluster",
    slug="matrix",
    status="active",
    description="3-node Proxmox cluster",
    tags=[{"name": "proxmox"}, {"name": "production"}]
)
```

**Get specific site:**

```bash
GET /api/dcim/sites/{id}/
GET /api/dcim/sites/?slug=matrix
```

```python
site = nb.dcim.sites.get(slug='matrix')
```

**Update a site:**

```bash
PATCH /api/dcim/sites/{id}/
{
  "description": "Updated description"
}
```

```python
site.description = "Updated description"
site.save()
```

**Delete a site:**

```bash
DELETE /api/dcim/sites/{id}/
```

```python
site.delete()
```

### Devices

**List devices:**

```bash
GET /api/dcim/devices/
GET /api/dcim/devices/?site=matrix
```

```python
devices = nb.dcim.devices.filter(site='matrix')
```

**Create a device:**

```bash
POST /api/dcim/devices/
{
  "name": "foxtrot",
  "device_type": 1,
  "site": 1,
  "device_role": 3,
  "status": "active",
  "tags": ["proxmox-node"]
}
```

```python
device = nb.dcim.devices.create(
    name="foxtrot",
    device_type=1,
    site=nb.dcim.sites.get(slug='matrix').id,
    device_role=3,
    status="active",
    tags=[{"name": "proxmox-node"}]
)
```

**Get device with related objects:**

```bash
GET /api/dcim/devices/{id}/?include=interfaces,config_context
```

```python
device = nb.dcim.devices.get(name='foxtrot')
interfaces = device.interfaces  # Related interfaces
```

### IP Addresses

**List IP addresses:**

```bash
GET /api/ipam/ip-addresses/
GET /api/ipam/ip-addresses/?vrf=management
```

```python
ips = nb.ipam.ip_addresses.all()
ips_mgmt = nb.ipam.ip_addresses.filter(vrf='management')
```

**Create IP address with DNS:**

```bash
POST /api/ipam/ip-addresses/
{
  "address": "192.168.3.10/24",
  "dns_name": "docker-01-nexus.spaceships.work",
  "status": "active",
  "description": "Docker host for Nexus registry",
  "tags": ["production-dns", "terraform"]
}
```

```python
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.10/24",
    dns_name="docker-01-nexus.spaceships.work",
    status="active",
    description="Docker host for Nexus registry",
    tags=[{"name": "production-dns"}, {"name": "terraform"}]
)
```

**Assign IP to interface:**

```python
ip = nb.ipam.ip_addresses.get(address='192.168.3.10/24')
interface = nb.dcim.interfaces.get(device='foxtrot', name='eth0')

ip.assigned_object_type = 'dcim.interface'
ip.assigned_object_id = interface.id
ip.save()
```

**Get IP with assigned device:**

```bash
GET /api/ipam/ip-addresses/{id}/
```

```python
ip = nb.ipam.ip_addresses.get(address='192.168.3.10/24')
if ip.assigned_object:
    print(f"Assigned to: {ip.assigned_object.device.name}")
```

### Prefixes

**List prefixes:**

```bash
GET /api/ipam/prefixes/
GET /api/ipam/prefixes/?site=matrix
```

```python
prefixes = nb.ipam.prefixes.filter(site='matrix')
```

**Get available IPs in prefix:**

```bash
GET /api/ipam/prefixes/{id}/available-ips/
```

```python
prefix = nb.ipam.prefixes.get(prefix='192.168.3.0/24')
available = prefix.available_ips.list()
print(f"Available IPs: {len(available)}")
```

**Create IP from available pool:**

```bash
POST /api/ipam/prefixes/{id}/available-ips/
{
  "dns_name": "k8s-01-worker.spaceships.work",
  "tags": ["production-dns"]
}
```

```python
prefix = nb.ipam.prefixes.get(prefix='192.168.3.0/24')
ip = prefix.available_ips.create(
    dns_name="k8s-01-worker.spaceships.work",
    tags=[{"name": "production-dns"}]
)
```

### Virtual Machines

**List VMs:**

```bash
GET /api/virtualization/virtual-machines/
GET /api/virtualization/virtual-machines/?cluster=matrix
```

```python
vms = nb.virtualization.virtual_machines.filter(cluster='matrix')
```

**Create VM:**

```bash
POST /api/virtualization/virtual-machines/
{
  "name": "docker-01",
  "cluster": 1,
  "role": 2,
  "vcpus": 4,
  "memory": 8192,
  "disk": 100,
  "status": "active",
  "tags": ["docker", "production"]
}
```

```python
vm = nb.virtualization.virtual_machines.create(
    name="docker-01",
    cluster=nb.virtualization.clusters.get(name='matrix').id,
    vcpus=4,
    memory=8192,
    disk=100,
    status="active",
    tags=[{"name": "docker"}, {"name": "production"}]
)
```

**Create VM interface:**

```python
vm_interface = nb.virtualization.interfaces.create(
    virtual_machine=vm.id,
    name='eth0',
    type='virtual',
    enabled=True
)
```

**Assign IP to VM interface:**

```python
ip = nb.ipam.ip_addresses.create(
    address='192.168.3.10/24',
    dns_name='docker-01-nexus.spaceships.work',
    assigned_object_type='virtualization.vminterface',
    assigned_object_id=vm_interface.id,
    tags=[{"name": "production-dns"}]
)

# Set as primary IP
vm.primary_ip4 = ip.id
vm.save()
```

---

## Filtering and Search

### Query Parameters

Most endpoints support filtering via query parameters:

```bash
# Filter by single value
GET /api/dcim/devices/?site=matrix

# Filter by multiple values (OR logic)
GET /api/dcim/devices/?site=matrix&site=backup

# Exclude values
GET /api/dcim/devices/?site__n=decommissioned

# Partial matching (case-insensitive)
GET /api/dcim/devices/?name__ic=docker

# Starts with
GET /api/dcim/devices/?name__isw=k8s

# Ends with
GET /api/dcim/devices/?name__iew=worker

# Greater than / less than
GET /api/ipam/prefixes/?prefix_length__gte=24

# Empty / not empty
GET /api/dcim/devices/?tenant__isnull=true
```

### Python Filtering

```python
# Single filter
devices = nb.dcim.devices.filter(site='matrix')

# Multiple filters (AND logic)
devices = nb.dcim.devices.filter(site='matrix', status='active')

# Partial matching
devices = nb.dcim.devices.filter(name__ic='docker')

# Greater than
prefixes = nb.ipam.prefixes.filter(prefix_length__gte=24)

# Get single object
device = nb.dcim.devices.get(name='foxtrot')
```

### Full-Text Search

```bash
# Search across all fields
GET /api/dcim/devices/?q=foxtrot
```

```python
results = nb.dcim.devices.filter(q='foxtrot')
```

### Tag Filtering

```bash
# Devices with specific tag
GET /api/dcim/devices/?tag=proxmox-node

# Multiple tags (OR logic)
GET /api/dcim/devices/?tag=proxmox-node&tag=ceph-node
```

```python
devices = nb.dcim.devices.filter(tag='proxmox-node')
```

---

## Pagination

API responses are paginated by default (50 results per page).

### Response Format

```json
{
  "count": 1000,
  "next": "https://netbox.spaceships.work/api/dcim/devices/?limit=50&offset=50",
  "previous": null,
  "results": [...]
}
```

### Controlling Pagination

```bash
# Custom page size (max 1000)
GET /api/dcim/devices/?limit=100

# Skip to offset
GET /api/dcim/devices/?limit=50&offset=100
```

### Python Pagination

```python
# Get all (handles pagination automatically)
all_devices = nb.dcim.devices.all()

# Custom page size
devices = nb.dcim.devices.filter(limit=100)

# Manual pagination
page1 = nb.dcim.devices.filter(limit=50, offset=0)
page2 = nb.dcim.devices.filter(limit=50, offset=50)
```

**⚠️ Warning:** Using `all()` on large datasets can be slow. Use filtering to reduce result set.

---

## Bulk Operations

NetBox supports bulk creation, update, and deletion.

### Bulk Create

**curl:**

```bash
POST /api/dcim/devices/
[
  {"name": "device1", "device_type": 1, "site": 1},
  {"name": "device2", "device_type": 1, "site": 1},
  {"name": "device3", "device_type": 1, "site": 1}
]
```

**pynetbox:**

```python
devices_data = [
    {"name": "device1", "device_type": 1, "site": 1},
    {"name": "device2", "device_type": 1, "site": 1},
    {"name": "device3", "device_type": 1, "site": 1}
]

# Bulk create (more efficient than loop)
devices = nb.dcim.devices.create(devices_data)
```

### Bulk Update

**curl:**

```bash
PUT /api/dcim/devices/
[
  {"id": 1, "status": "active"},
  {"id": 2, "status": "active"},
  {"id": 3, "status": "offline"}
]
```

**pynetbox:**

```python
# Update multiple objects
for device in nb.dcim.devices.filter(site='matrix'):
    device.status = 'active'
    device.save()

# Or bulk update with PUT
updates = [
    {"id": 1, "status": "active"},
    {"id": 2, "status": "active"}
]
nb.dcim.devices.update(updates)
```

### Bulk Delete

**curl:**

```bash
DELETE /api/dcim/devices/
[
  {"id": 1},
  {"id": 2},
  {"id": 3}
]
```

**pynetbox:**

```python
# Delete multiple objects
devices_to_delete = nb.dcim.devices.filter(status='decommissioned')
for device in devices_to_delete:
    device.delete()
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid data or malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Not found.",
  "error": "Object does not exist"
}
```

### Python Error Handling

```python
import pynetbox
from requests.exceptions import HTTPError

try:
    device = nb.dcim.devices.get(name='nonexistent')
    if not device:
        print("Device not found")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Resource not found")
    elif e.response.status_code == 403:
        print("Permission denied")
    else:
        print(f"HTTP Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Validation Errors

```python
try:
    site = nb.dcim.sites.create(
        name="Invalid Site",
        slug="invalid slug"  # Spaces not allowed
    )
except pynetbox.RequestError as e:
    print(f"Validation error: {e.error}")
```

### Best Practices

1. **Always check for None:**

   ```python
   device = nb.dcim.devices.get(name='foo')
   if device:
       print(device.name)
   else:
       print("Device not found")
   ```

2. **Use try/except for create/update:**

   ```python
   try:
       ip = nb.ipam.ip_addresses.create(address='192.168.1.1/24')
   except pynetbox.RequestError as e:
       print(f"Failed to create IP: {e.error}")
   ```

3. **Validate data before API calls:**

   ```python
   import ipaddress

   def validate_ip(ip_str: str) -> bool:
       try:
           ipaddress.ip_interface(ip_str)
           return True
       except ValueError:
           return False
   ```

See [../tools/netbox_api_client.py](../tools/netbox_api_client.py) for complete error handling examples.

---

## Rate Limiting

NetBox may enforce rate limits on API requests.

### Response Headers

```text
X-RateLimit-Limit: 1000        # Total requests allowed
X-RateLimit-Remaining: 950     # Remaining requests
X-RateLimit-Reset: 1640000000  # Reset time (Unix timestamp)
```

### Handling Rate Limits

```python
import time
from requests.exceptions import HTTPError

def api_call_with_retry(func, max_retries=3):
    """Retry API call if rate limited."""
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                retry_after = int(e.response.headers.get('Retry-After', 60))
                print(f"Rate limited. Retrying in {retry_after}s...")
                time.sleep(retry_after)
            else:
                raise
    raise Exception("Max retries exceeded")

# Usage
result = api_call_with_retry(lambda: nb.dcim.devices.all())
```

### Best Practices

1. **Use pagination** to reduce request count
2. **Cache responses** when data doesn't change frequently
3. **Batch operations** using bulk endpoints
4. **Implement exponential backoff** for retries
5. **Monitor rate limit headers** in production

---

## Python Client (pynetbox)

### Installation

```bash
pip install pynetbox
```

Or with uv (Virgo-Core standard):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pynetbox>=7.0.0"]
# ///
```

### Basic Usage

```python
import pynetbox

# Connect
nb = pynetbox.api(
    'https://netbox.spaceships.work',
    token='your-token'
)

# Query
sites = nb.dcim.sites.all()
device = nb.dcim.devices.get(name='foxtrot')

# Create
site = nb.dcim.sites.create(
    name='Matrix',
    slug='matrix'
)

# Update
device.status = 'active'
device.save()

# Delete
device.delete()
```

### Advanced Patterns

**Lazy loading:**

```python
# Only fetches when accessed
device = nb.dcim.devices.get(name='foxtrot')
interfaces = device.interfaces  # API call happens here
```

**Custom fields:**

```python
device.custom_fields['serial_number'] = 'ABC123'
device.save()
```

**Relationships:**

```python
# Get device's primary IP
device = nb.dcim.devices.get(name='foxtrot')
if device.primary_ip4:
    print(device.primary_ip4.address)

# Get IP's assigned device
ip = nb.ipam.ip_addresses.get(address='192.168.3.5/24')
if ip.assigned_object:
    print(ip.assigned_object.device.name)
```

**Threading (for bulk operations):**

```python
from concurrent.futures import ThreadPoolExecutor

def get_device_info(device_name):
    return nb.dcim.devices.get(name=device_name)

device_names = ['foxtrot', 'golf', 'hotel']

with ThreadPoolExecutor(max_workers=5) as executor:
    devices = list(executor.map(get_device_info, device_names))
```

---

## Best Practices

### 1. Use Filtering to Reduce Data Transfer

```python
# ❌ Inefficient: Get all devices then filter
all_devices = nb.dcim.devices.all()
matrix_devices = [d for d in all_devices if d.site.slug == 'matrix']

# ✅ Efficient: Filter on server
matrix_devices = nb.dcim.devices.filter(site='matrix')
```

### 2. Use Specific Fields

```bash
# Only get specific fields
GET /api/dcim/devices/?fields=name,status,primary_ip4
```

### 3. Cache Responses

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_site(site_slug: str):
    """Cache site lookups."""
    return nb.dcim.sites.get(slug=site_slug)
```

### 4. Validate Before API Calls

```python
import ipaddress
import re

def validate_dns_name(name: str) -> bool:
    """Validate DNS naming convention."""
    pattern = r'^[a-z0-9-]+-\d{2}-[a-z0-9-]+\.[a-z0-9.-]+$'
    return bool(re.match(pattern, name))

def validate_ip(ip_str: str) -> bool:
    """Validate IP address format."""
    try:
        ipaddress.ip_interface(ip_str)
        return True
    except ValueError:
        return False

# Use before API calls
if validate_dns_name(dns_name) and validate_ip(ip_address):
    ip = nb.ipam.ip_addresses.create(
        address=ip_address,
        dns_name=dns_name
    )
```

### 5. Use Bulk Operations

```python
# ❌ Slow: Create in loop
for ip in ip_list:
    nb.ipam.ip_addresses.create(address=ip)

# ✅ Fast: Bulk create
nb.ipam.ip_addresses.create([
    {"address": ip} for ip in ip_list
])
```

### 6. Implement Proper Error Handling

See [Error Handling](#error-handling) section above.

### 7. Use HTTPS in Production

```python
# ✅ Always use HTTPS
nb = pynetbox.api('https://netbox.spaceships.work', token=token)

# ❌ Never use HTTP in production
nb = pynetbox.api('http://netbox.spaceships.work', token=token)
```

### 8. Rotate Tokens Regularly

Store tokens in Infisical and rotate every 90 days. See [Security](#security) section.

---

## Security

### API Token Security

1. **Store in Infisical (never hardcode):**

   ```python
   from infisical import InfisicalClient

   client = InfisicalClient()
   token = client.get_secret(
       secret_name="NETBOX_API_TOKEN",
       project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
       environment="prod",
       path="/matrix"
   ).secret_value
   ```

2. **Use environment variables (alternative):**

   ```python
   import os
   token = os.getenv('NETBOX_API_TOKEN')
   if not token:
       raise ValueError("NETBOX_API_TOKEN not set")
   ```

3. **Rotate tokens regularly** (every 90 days)

4. **Use minimal permissions** (read-only for queries, write for automation)

### HTTPS Only

```python
# ✅ Verify SSL certificates
nb = pynetbox.api(
    'https://netbox.spaceships.work',
    token=token,
    ssl_verify=True  # Default, but explicit is better
)

# ⚠️ Only disable for dev/testing
nb = pynetbox.api(
    'https://netbox.local',
    token=token,
    ssl_verify=False  # Self-signed cert
)
```

### Audit API Usage

Monitor API calls in production:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_api_call(action: str, resource: str, details: dict):
    """Log API calls for audit."""
    logger.info(f"API Call: {action} {resource} - {details}")

# Example usage
ip = nb.ipam.ip_addresses.create(address='192.168.1.1/24')
audit_api_call('CREATE', 'ip-address', {'address': '192.168.1.1/24'})
```

### Network Security

- Use VPN for remote access to NetBox
- Restrict NetBox API access by IP (firewall rules)
- Use Proxmox VLANs to isolate management traffic

---

## Additional Resources

- **Official API Docs:** <https://netboxlabs.com/docs/netbox/en/stable/>
- **pynetbox Docs:** <https://pynetbox.readthedocs.io/>
- **OpenAPI Schema:** `GET https://netbox.spaceships.work/api/schema/`
- **GraphQL API:** `https://netbox.spaceships.work/graphql/`

## Related Documentation

- [NetBox Data Models](netbox-data-models.md) - Data model relationships
- [NetBox Best Practices](netbox-best-practices.md) - Infrastructure patterns
- [Tools: netbox_api_client.py](../tools/netbox_api_client.py) - Complete working example
- [DNS Naming Conventions](../workflows/naming-conventions.md) - DNS naming rules

---

**Next:** [NetBox Data Models Guide](netbox-data-models.md)
