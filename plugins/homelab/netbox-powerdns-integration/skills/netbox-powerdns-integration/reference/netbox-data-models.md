# NetBox Data Models and Relationships

**NetBox Version:** 4.3.0

Comprehensive guide to NetBox's data models, their relationships, and how they map to the Matrix cluster infrastructure in Virgo-Core.

---

## Table of Contents

- [Overview](#overview)
- [Core Data Models](#core-data-models)
- [Model Relationships](#model-relationships)
- [DCIM Models (Data Center)](#dcim-models-data-center)
- [IPAM Models (IP Management)](#ipam-models-ip-management)
- [Virtualization Models](#virtualization-models)
- [Matrix Cluster Example](#matrix-cluster-example)
- [Best Practices](#best-practices)

---

## Overview

NetBox organizes infrastructure data into logical models across several applications:

| Application | Purpose | Key Models |
|-------------|---------|------------|
| **DCIM** | Data Center Infrastructure | Site, Rack, Device, Interface, Cable |
| **IPAM** | IP Address Management | IP Address, Prefix, VLAN, VRF |
| **Virtualization** | Virtual Machines | Virtual Machine, Cluster, VM Interface |
| **Circuits** | WAN/Circuit Management | Circuit, Provider, Circuit Termination |
| **Tenancy** | Multi-tenant Support | Tenant, Tenant Group, Contact |
| **Extras** | Extensions | Tag, Custom Field, Webhook |

---

## Core Data Models

### Site

Represents a physical location containing infrastructure.

**Fields:**

- `name` - Display name (e.g., "Matrix Cluster")
- `slug` - URL-friendly identifier (e.g., "matrix")
- `status` - active, planned, retired, etc.
- `region` - Geographic region (optional)
- `description` - Purpose and details
- `tags` - Flexible categorization

**Example:**

```python
site = nb.dcim.sites.create(
    name="Matrix Cluster",
    slug="matrix",
    status="active",
    description="3-node Proxmox VE cluster (foxtrot, golf, hotel)",
    tags=[{"name": "proxmox"}, {"name": "homelab"}]
)
```

**Relationships:**

- Has many: Racks, Devices, Prefixes
- Belongs to: Region (optional)

---

### Rack

Physical rack within a site.

**Fields:**

- `name` - Rack identifier
- `site` - Parent site
- `u_height` - Units (typically 42U)
- `desc_units` - Count units top-down
- `width` - 19" or 23"
- `tags`

**Example:**

```python
rack = nb.dcim.racks.create(
    name="Rack-01",
    site=site.id,
    u_height=42,
    width=19
)
```

**Relationships:**

- Belongs to: Site
- Has many: Devices (mounted in rack)

---

### Device

Physical piece of equipment.

**Fields:**

- `name` - Device hostname (e.g., "foxtrot")
- `device_type` - Reference to device type
- `device_role` - Purpose (server, switch, etc.)
- `site` - Physical location
- `rack` - Optional rack location
- `position` - Rack unit position
- `status` - active, offline, planned, etc.
- `primary_ip4` - Primary IPv4 address
- `primary_ip6` - Primary IPv6 address
- `tags`

**Example:**

```python
device = nb.dcim.devices.create(
    name="foxtrot",
    device_type=device_type.id,
    device_role=role.id,
    site=site.id,
    status="active",
    tags=[{"name": "proxmox-node"}]
)
```

**Relationships:**

- Belongs to: Site, Rack, Device Type, Device Role
- Has many: Interfaces, Console Ports, Power Ports
- Has one: Primary IP4, Primary IP6

---

### Interface

Network interface on a device.

**Fields:**

- `device` - Parent device
- `name` - Interface name (e.g., "eth0", "enp1s0")
- `type` - Physical type (1000base-t, 10gbase-x, etc.)
- `enabled` - Administrative status
- `mtu` - Maximum transmission unit
- `mac_address` - MAC address
- `mode` - Access or Trunk (for VLANs)
- `untagged_vlan` - Native VLAN
- `tagged_vlans` - Tagged VLANs
- `tags`

**Example:**

```python
interface = nb.dcim.interfaces.create(
    device=device.id,
    name="enp1s0",
    type="10gbase-x-sfpp",
    enabled=True,
    mtu=9000,  # Jumbo frames for CEPH
    tags=[{"name": "ceph-public"}]
)
```

**Relationships:**

- Belongs to: Device
- Has many: IP Addresses (assigned to interface)
- Connected to: Cable (physical connection)

---

### Cable

Physical cable connection between interfaces.

**Fields:**

- `a_terminations` - End A (interface, console port, etc.)
- `b_terminations` - End B
- `type` - Cable type (cat6, fiber, dac, etc.)
- `status` - connected, planned, etc.
- `length` - Cable length
- `length_unit` - m, ft, etc.
- `color` - Cable color
- `tags`

**Example:**

```python
cable = nb.dcim.cables.create(
    a_terminations=[{"object_type": "dcim.interface", "object_id": iface1.id}],
    b_terminations=[{"object_type": "dcim.interface", "object_id": iface2.id}],
    type="dac-active",
    status="connected",
    length=3,
    length_unit="m"
)
```

**Relationships:**

- Connects: Two termination objects (interfaces, ports, etc.)

---

### IP Address

IPv4 or IPv6 address.

**Fields:**

- `address` - IP with CIDR (e.g., "192.168.3.5/24")
- `dns_name` - FQDN (e.g., "foxtrot.spaceships.work")
- `status` - active, reserved, deprecated, etc.
- `role` - loopback, secondary, anycast, etc.
- `assigned_object_type` - Interface type (dcim.interface or virtualization.vminterface)
- `assigned_object_id` - Interface ID
- `vrf` - Virtual routing and forwarding instance
- `tenant` - Tenant assignment
- `tags`

**Example:**

```python
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.5/24",
    dns_name="foxtrot.spaceships.work",
    status="active",
    assigned_object_type="dcim.interface",
    assigned_object_id=interface.id,
    tags=[{"name": "production-dns"}]
)
```

**Relationships:**

- Belongs to: Prefix, VRF (optional)
- Assigned to: Interface (device or VM)
- Referenced by: Device (as primary IP)

---

### Prefix

IP network or subnet.

**Fields:**

- `prefix` - Network in CIDR (e.g., "192.168.3.0/24")
- `status` - active, reserved, deprecated, etc.
- `role` - Purpose (e.g., "management", "ceph-public")
- `site` - Physical location
- `vrf` - VRF assignment
- `vlan` - Associated VLAN
- `is_pool` - Allow automatic IP assignment
- `description`
- `tags`

**Example:**

```python
prefix = nb.ipam.prefixes.create(
    prefix="192.168.3.0/24",
    status="active",
    role=nb.ipam.roles.get(slug='management').id,
    site=site.id,
    is_pool=True,
    description="Management network for Matrix cluster",
    tags=[{"name": "proxmox-mgmt"}]
)
```

**Relationships:**

- Belongs to: Site, VRF, VLAN (optional)
- Contains: IP Addresses
- Hierarchical: Can contain child prefixes

---

### VLAN

Virtual LAN.

**Fields:**

- `vid` - VLAN ID (1-4094)
- `name` - VLAN name
- `site` - Site assignment
- `group` - VLAN group (optional)
- `status` - active, reserved, deprecated
- `role` - Purpose
- `description`
- `tags`

**Example:**

```python
vlan = nb.ipam.vlans.create(
    vid=9,
    name="Corosync",
    site=site.id,
    status="active",
    description="Proxmox corosync cluster communication",
    tags=[{"name": "proxmox-cluster"}]
)
```

**Relationships:**

- Belongs to: Site, VLAN Group
- Assigned to: Prefixes, Interfaces

---

### VRF

Virtual Routing and Forwarding instance.

**Fields:**

- `name` - VRF name
- `rd` - Route distinguisher (optional)
- `description`
- `enforce_unique` - Enforce unique IP addressing
- `tags`

**Example:**

```python
vrf = nb.ipam.vrfs.create(
    name="management",
    enforce_unique=True,
    description="Management VRF"
)
```

**Relationships:**

- Has many: Prefixes, IP Addresses

---

### Virtual Machine

VM in a virtualization cluster.

**Fields:**

- `name` - VM hostname
- `cluster` - Virtualization cluster
- `role` - VM role (optional)
- `status` - active, offline, planned, etc.
- `vcpus` - Virtual CPU count
- `memory` - Memory in MB
- `disk` - Disk in GB
- `primary_ip4` - Primary IPv4
- `primary_ip6` - Primary IPv6
- `description`
- `tags`

**Example:**

```python
vm = nb.virtualization.virtual_machines.create(
    name="docker-01",
    cluster=cluster.id,
    status="active",
    vcpus=4,
    memory=8192,  # 8 GB
    disk=100,  # 100 GB
    tags=[{"name": "docker"}, {"name": "production"}]
)
```

**Relationships:**

- Belongs to: Cluster, Role (optional)
- Has many: VM Interfaces
- Has one: Primary IP4, Primary IP6

---

### Cluster

Virtualization cluster (e.g., Proxmox, VMware).

**Fields:**

- `name` - Cluster name
- `type` - Cluster type
- `site` - Physical location
- `description`
- `tags`

**Example:**

```python
cluster_type = nb.virtualization.cluster_types.get(slug='proxmox')
cluster = nb.virtualization.clusters.create(
    name="Matrix",
    type=cluster_type.id,
    site=site.id,
    description="3-node Proxmox VE 9.x cluster",
    tags=[{"name": "production"}]
)
```

**Relationships:**

- Belongs to: Site, Cluster Type
- Has many: Virtual Machines

---

### VM Interface

Network interface on a virtual machine.

**Fields:**

- `virtual_machine` - Parent VM
- `name` - Interface name (e.g., "eth0")
- `type` - Interface type (virtual, bridge)
- `enabled` - Administrative status
- `mtu` - MTU
- `mac_address` - MAC address
- `untagged_vlan` - Native VLAN
- `tagged_vlans` - Tagged VLANs
- `tags`

**Example:**

```python
vm_interface = nb.virtualization.interfaces.create(
    virtual_machine=vm.id,
    name="eth0",
    type="virtual",
    enabled=True,
    mtu=1500
)
```

**Relationships:**

- Belongs to: Virtual Machine
- Has many: IP Addresses

---

## Model Relationships

### Hierarchical Relationships

```text
Region (optional)
  └── Site
      ├── Rack
      │   └── Device
      │       └── Interface
      │           └── IP Address
      ├── Cluster
      │   └── Virtual Machine
      │       └── VM Interface
      │           └── IP Address
      └── Prefix
          └── IP Address
```

### Key Relationships

**Site containment:**

```text
Site
  ├── has many Racks
  ├── has many Devices
  ├── has many Clusters
  ├── has many Prefixes
  └── has many VLANs
```

**Device structure:**

```text
Device
  ├── belongs to Site
  ├── belongs to Rack (optional)
  ├── belongs to Device Type
  ├── belongs to Device Role
  ├── has many Interfaces
  ├── has one Primary IP4 (optional)
  └── has one Primary IP6 (optional)
```

**Interface connectivity:**

```text
Interface
  ├── belongs to Device
  ├── has many IP Addresses
  ├── connected via Cable
  ├── assigned to VLAN(s)
  └── assigned object for IP
```

**IP Address assignment:**

```text
IP Address
  ├── belongs to Prefix
  ├── assigned to Interface (device or VM)
  ├── belongs to VRF (optional)
  └── referenced as Primary IP by Device/VM
```

**VM structure:**

```text
Virtual Machine
  ├── belongs to Cluster
  ├── has many VM Interfaces
  ├── has one Primary IP4 (optional)
  └── has one Primary IP6 (optional)
```

**IPAM hierarchy:**

```text
VRF (optional)
  └── Prefix
      ├── child Prefix (nested)
      └── IP Address
```

---

## DCIM Models (Data Center)

### Complete Device Example

Creating a complete device with interfaces and IPs:

```python
# 1. Create device type (if not exists)
manufacturer = nb.dcim.manufacturers.get(slug='minisforum')
if not manufacturer:
    manufacturer = nb.dcim.manufacturers.create(name='MINISFORUM', slug='minisforum')

device_type = nb.dcim.device_types.get(slug='ms-a2')
if not device_type:
    device_type = nb.dcim.device_types.create(
        manufacturer=manufacturer.id,
        model='MS-A2',
        slug='ms-a2'
    )

# 2. Create device role
role = nb.dcim.device_roles.get(slug='proxmox-node')
if not role:
    role = nb.dcim.device_roles.create(
        name='Proxmox Node',
        slug='proxmox-node',
        color='2196f3'
    )

# 3. Create device
device = nb.dcim.devices.create(
    name='foxtrot',
    device_type=device_type.id,
    device_role=role.id,
    site=site.id,
    status='active',
    tags=[{'name': 'proxmox-node'}, {'name': 'ceph-node'}]
)

# 4. Create management interface
mgmt_iface = nb.dcim.interfaces.create(
    device=device.id,
    name='enp2s0',
    type='2.5gbase-t',
    enabled=True,
    mtu=1500,
    description='Management interface'
)

# 5. Assign management IP
mgmt_ip = nb.ipam.ip_addresses.create(
    address='192.168.3.5/24',
    dns_name='foxtrot.spaceships.work',
    status='active',
    assigned_object_type='dcim.interface',
    assigned_object_id=mgmt_iface.id,
    tags=[{'name': 'production-dns'}]
)

# 6. Set as primary IP
device.primary_ip4 = mgmt_ip.id
device.save()

# 7. Create CEPH public interface
ceph_pub_iface = nb.dcim.interfaces.create(
    device=device.id,
    name='enp1s0f0',
    type='10gbase-x-sfpp',
    enabled=True,
    mtu=9000,
    description='CEPH public network'
)

# 8. Assign CEPH public IP
ceph_pub_ip = nb.ipam.ip_addresses.create(
    address='192.168.5.5/24',
    dns_name='foxtrot-ceph-pub.spaceships.work',
    status='active',
    assigned_object_type='dcim.interface',
    assigned_object_id=ceph_pub_iface.id
)

# 9. Create CEPH private interface
ceph_priv_iface = nb.dcim.interfaces.create(
    device=device.id,
    name='enp1s0f1',
    type='10gbase-x-sfpp',
    enabled=True,
    mtu=9000,
    description='CEPH private network'
)

# 10. Assign CEPH private IP
ceph_priv_ip = nb.ipam.ip_addresses.create(
    address='192.168.7.5/24',
    status='active',
    assigned_object_type='dcim.interface',
    assigned_object_id=ceph_priv_iface.id
)
```

---

## IPAM Models (IP Management)

### Complete IPAM Example

Setting up IPAM for Matrix cluster:

```python
# 1. Create VRF (optional but recommended)
vrf_mgmt = nb.ipam.vrfs.create(
    name='management',
    enforce_unique=True,
    description='Management VRF'
)

# 2. Create prefix role
role_mgmt = nb.ipam.roles.get(slug='management')
if not role_mgmt:
    role_mgmt = nb.ipam.roles.create(
        name='Management',
        slug='management'
    )

# 3. Create management prefix
prefix_mgmt = nb.ipam.prefixes.create(
    prefix='192.168.3.0/24',
    status='active',
    role=role_mgmt.id,
    site=site.id,
    vrf=vrf_mgmt.id,
    is_pool=True,
    description='Management network for Matrix cluster'
)

# 4. Create CEPH public prefix
role_storage = nb.ipam.roles.create(name='Storage', slug='storage')
prefix_ceph_pub = nb.ipam.prefixes.create(
    prefix='192.168.5.0/24',
    status='active',
    role=role_storage.id,
    site=site.id,
    is_pool=True,
    description='CEPH public network (MTU 9000)'
)

# 5. Create CEPH private prefix
prefix_ceph_priv = nb.ipam.prefixes.create(
    prefix='192.168.7.0/24',
    status='active',
    role=role_storage.id,
    site=site.id,
    is_pool=True,
    description='CEPH private network (MTU 9000)'
)

# 6. Create Corosync VLAN
vlan_corosync = nb.ipam.vlans.create(
    vid=9,
    name='Corosync',
    site=site.id,
    status='active',
    description='Proxmox cluster communication'
)

# 7. Create Corosync prefix
prefix_corosync = nb.ipam.prefixes.create(
    prefix='192.168.8.0/24',
    status='active',
    site=site.id,
    vlan=vlan_corosync.id,
    description='Corosync cluster network (VLAN 9)'
)

# 8. Get available IPs from prefix
available_ips = prefix_mgmt.available_ips.list()
print(f"Available IPs in management network: {len(available_ips)}")

# 9. Reserve gateway
gateway = nb.ipam.ip_addresses.create(
    address='192.168.3.1/24',
    status='active',
    role='anycast',
    description='Management network gateway'
)
```

---

## Virtualization Models

### Complete VM Example

Creating a VM with network configuration:

```python
# 1. Create cluster type (if not exists)
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

# 3. Create VM role
vm_role = nb.dcim.device_roles.get(slug='docker-host')
if not vm_role:
    vm_role = nb.dcim.device_roles.create(
        name='Docker Host',
        slug='docker-host',
        vm_role=True,  # Mark as VM role
        color='4caf50'
    )

# 4. Create VM
vm = nb.virtualization.virtual_machines.create(
    name='docker-01',
    cluster=cluster.id,
    role=vm_role.id,
    status='active',
    vcpus=4,
    memory=8192,
    disk=100,
    description='Docker host for Nexus registry',
    tags=[{'name': 'docker'}, {'name': 'production'}]
)

# 5. Create VM interface
vm_iface = nb.virtualization.interfaces.create(
    virtual_machine=vm.id,
    name='eth0',
    type='virtual',
    enabled=True,
    mtu=1500
)

# 6. Get next available IP from prefix
prefix = nb.ipam.prefixes.get(prefix='192.168.3.0/24')
vm_ip = prefix.available_ips.create(
    dns_name='docker-01-nexus.spaceships.work',
    status='active',
    assigned_object_type='virtualization.vminterface',
    assigned_object_id=vm_iface.id,
    tags=[{'name': 'production-dns'}, {'name': 'terraform'}]
)

# 7. Set as primary IP
vm.primary_ip4 = vm_ip.id
vm.save()

# 8. Query VM with interfaces
vm = nb.virtualization.virtual_machines.get(name='docker-01')
print(f"VM: {vm.name}")
print(f"Cluster: {vm.cluster.name}")
print(f"Primary IP: {vm.primary_ip4.address}")
for iface in vm.interfaces:
    print(f"  Interface: {iface.name}")
    for ip in nb.ipam.ip_addresses.filter(vminterface_id=iface.id):
        print(f"    IP: {ip.address} ({ip.dns_name})")
```

---

## Matrix Cluster Example

Complete NetBox representation of the Matrix cluster:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pynetbox>=7.0.0", "infisical-python>=2.3.3"]
# ///

import pynetbox
from infisical import InfisicalClient

# Get token
client = InfisicalClient()
token = client.get_secret(
    secret_name="NETBOX_API_TOKEN",
    project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
    environment="prod",
    path="/matrix"
).secret_value

nb = pynetbox.api('https://netbox.spaceships.work', token=token)

# Create site
site = nb.dcim.sites.create(
    name="Matrix Cluster",
    slug="matrix",
    status="active",
    description="3-node Proxmox VE 9.x cluster with CEPH storage"
)

# Create cluster
cluster = nb.virtualization.clusters.create(
    name="Matrix",
    type=nb.virtualization.cluster_types.get(slug='proxmox').id,
    site=site.id
)

# Create prefixes
prefixes = {
    'mgmt': nb.ipam.prefixes.create(
        prefix='192.168.3.0/24',
        site=site.id,
        description='Management network',
        is_pool=True
    ),
    'ceph_pub': nb.ipam.prefixes.create(
        prefix='192.168.5.0/24',
        site=site.id,
        description='CEPH public (MTU 9000)',
        is_pool=True
    ),
    'ceph_priv': nb.ipam.prefixes.create(
        prefix='192.168.7.0/24',
        site=site.id,
        description='CEPH private (MTU 9000)',
        is_pool=True
    ),
    'corosync': nb.ipam.prefixes.create(
        prefix='192.168.8.0/24',
        site=site.id,
        description='Corosync (VLAN 9)',
        is_pool=True
    )
}

# Matrix nodes
nodes = [
    {'name': 'foxtrot', 'mgmt_ip': '192.168.3.5', 'ceph_pub': '192.168.5.5',
     'ceph_priv': '192.168.7.5', 'corosync': '192.168.8.5'},
    {'name': 'golf', 'mgmt_ip': '192.168.3.6', 'ceph_pub': '192.168.5.6',
     'ceph_priv': '192.168.7.6', 'corosync': '192.168.8.6'},
    {'name': 'hotel', 'mgmt_ip': '192.168.3.7', 'ceph_pub': '192.168.5.7',
     'ceph_priv': '192.168.7.7', 'corosync': '192.168.8.7'}
]

for node_data in nodes:
    # Create device
    device = nb.dcim.devices.create(
        name=node_data['name'],
        device_type=nb.dcim.device_types.get(slug='ms-a2').id,
        device_role=nb.dcim.device_roles.get(slug='proxmox-node').id,
        site=site.id,
        status='active'
    )

    # Create interfaces and IPs
    # Management
    mgmt_iface = nb.dcim.interfaces.create(
        device=device.id, name='enp2s0', type='2.5gbase-t', mtu=1500
    )
    mgmt_ip = nb.ipam.ip_addresses.create(
        address=f"{node_data['mgmt_ip']}/24",
        dns_name=f"{node_data['name']}.spaceships.work",
        assigned_object_type='dcim.interface',
        assigned_object_id=mgmt_iface.id,
        tags=[{'name': 'production-dns'}]
    )
    device.primary_ip4 = mgmt_ip.id
    device.save()

    # CEPH public
    ceph_pub_iface = nb.dcim.interfaces.create(
        device=device.id, name='enp1s0f0', type='10gbase-x-sfpp', mtu=9000
    )
    nb.ipam.ip_addresses.create(
        address=f"{node_data['ceph_pub']}/24",
        assigned_object_type='dcim.interface',
        assigned_object_id=ceph_pub_iface.id
    )

    # CEPH private
    ceph_priv_iface = nb.dcim.interfaces.create(
        device=device.id, name='enp1s0f1', type='10gbase-x-sfpp', mtu=9000
    )
    nb.ipam.ip_addresses.create(
        address=f"{node_data['ceph_priv']}/24",
        assigned_object_type='dcim.interface',
        assigned_object_id=ceph_priv_iface.id
    )

    # Corosync
    corosync_iface = nb.dcim.interfaces.create(
        device=device.id, name='enp2s0.9', type='virtual', mtu=1500
    )
    nb.ipam.ip_addresses.create(
        address=f"{node_data['corosync']}/24",
        assigned_object_type='dcim.interface',
        assigned_object_id=corosync_iface.id
    )

print("Matrix cluster created in NetBox!")
```

---

## Best Practices

### 1. Plan Hierarchy First

```text
1. Create Site
2. Create Prefixes (IPAM)
3. Create VLANs
4. Create Device Types/Roles
5. Create Devices
6. Create Interfaces
7. Assign IPs
8. Set Primary IPs
```

### 2. Use Consistent Naming

- Sites: Descriptive names (e.g., "Matrix Cluster")
- Devices: Hostname only (e.g., "foxtrot")
- Interfaces: Match OS names (e.g., "enp1s0f0")
- DNS names: Follow convention (e.g., "foxtrot.spaceships.work")

### 3. Tag Everything

```python
tags = [
    {'name': 'proxmox-node'},
    {'name': 'ceph-node'},
    {'name': 'production'},
    {'name': 'production-dns'},
    {'name': 'terraform'}
]
```

### 4. Use Prefixes as IP Pools

```python
prefix = nb.ipam.prefixes.create(
    prefix='192.168.3.0/24',
    is_pool=True  # Enable automatic IP assignment
)

# Get next available IP
ip = prefix.available_ips.create(dns_name='host.domain')
```

### 5. Always Set Primary IPs

```python
# After creating IPs, set primary
device.primary_ip4 = mgmt_ip.id
device.save()
```

### 6. Validate Relationships

```python
# Check if IP is assigned
ip = nb.ipam.ip_addresses.get(address='192.168.3.5/24')
if ip.assigned_object:
    print(f"Assigned to: {ip.assigned_object.name}")
else:
    print("IP not assigned to any interface")
```

### 7. Use Descriptions

```python
device = nb.dcim.devices.create(
    name='foxtrot',
    description='AMD Ryzen 9 9955HX, 64GB RAM, 3× NVMe (1TB + 2× 4TB)'
)
```

---

## Related Documentation

- [NetBox API Guide](netbox-api-guide.md) - API reference
- [NetBox Best Practices](netbox-best-practices.md) - Infrastructure patterns
- [Tools: netbox_api_client.py](../tools/netbox_api_client.py) - Working examples
- [DNS Naming Conventions](../workflows/naming-conventions.md) - Naming rules

---

**Next:** [NetBox Best Practices Guide](netbox-best-practices.md)
