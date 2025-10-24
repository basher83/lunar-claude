# DNS Automation Workflows

## Overview

This guide covers end-to-end workflows for automating DNS record management using NetBox as the source of truth and PowerDNS as the authoritative DNS server.

## Architecture

```text
┌─────────────┐
│  Terraform  │───┐
│   Ansible   │   │
│   Manual    │   │
└─────────────┘   │
                  ▼
            ┌──────────┐
            │  NetBox  │ (Source of Truth)
            │   IPAM   │
            └────┬─────┘
                 │
                 │ netbox-powerdns-sync plugin
                 │
                 ▼
            ┌──────────┐
            │ PowerDNS │ (Authoritative DNS)
            │   API    │
            └────┬─────┘
                 │
                 │ Zone files / API
                 │
                 ▼
            ┌──────────┐
            │   DNS    │ (Resolvers query here)
            │ Clients  │
            └──────────┘
```

## Workflow 1: Create VM with Automatic DNS

### Using Terraform

**End-to-end automation:**

```hcl
# 1. Create VM in Proxmox
resource "proxmox_vm_qemu" "docker_host" {
  name        = "docker-01-nexus"
  target_node = "foxtrot"
  vmid        = 101

  clone      = "ubuntu-template"
  full_clone = true

  cores   = 4
  memory  = 8192

  network {
    bridge = "vmbr0"
    model  = "virtio"
    tag    = 30
  }

  disk {
    storage = "local-lvm"
    type    = "scsi"
    size    = "50G"
  }

  # Cloud-init IP configuration
  ipconfig0 = "ip=192.168.1.100/24,gw=192.168.1.1"

  sshkeys = file("~/.ssh/id_rsa.pub")
}

# 2. Register in NetBox (triggers DNS sync)
resource "netbox_ip_address" "docker_host" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "docker-01-nexus.spaceships.work"
  status      = "active"
  description = "Docker host for Nexus container registry"

  tags = [
    "terraform",
    "production-dns",  # Triggers auto DNS sync
    "docker-host"
  ]

  # Ensure VM is created first
  depends_on = [proxmox_vm_qemu.docker_host]
}

# 3. DNS records automatically created by netbox-powerdns-sync plugin:
#    A:   docker-01-nexus.spaceships.work → 192.168.1.100
#    PTR: 100.1.168.192.in-addr.arpa → docker-01-nexus.spaceships.work

# 4. Output for verification
output "vm_fqdn" {
  value = netbox_ip_address.docker_host.dns_name
}

output "vm_ip" {
  value = split("/", netbox_ip_address.docker_host.ip_address)[0]
}
```

**Apply workflow:**

```bash
cd terraform/netbox-vm/
tofu init
tofu plan
tofu apply

# Verify DNS
dig @192.168.3.1 docker-01-nexus.spaceships.work +short
# Returns: 192.168.1.100

# Verify PTR
dig @192.168.3.1 -x 192.168.1.100 +short
# Returns: docker-01-nexus.spaceships.work
```

### Using Ansible

**Playbook for VM with DNS:**

```yaml
---
- name: Provision VM with automatic DNS
  hosts: localhost
  gather_facts: false

  vars:
    vm_name: docker-01-nexus
    vm_ip: 192.168.1.100
    vm_fqdn: "{{ vm_name }}.spaceships.work"
    proxmox_node: foxtrot

  tasks:
    # 1. Create VM in Proxmox
    - name: Clone template to create VM
      community.proxmox.proxmox_kvm:
        api_host: "{{ proxmox_api_host }}"
        api_user: "{{ proxmox_api_user }}"
        api_token_id: "{{ proxmox_token_id }}"
        api_token_secret: "{{ proxmox_token_secret }}"
        node: "{{ proxmox_node }}"
        vmid: 101
        name: "{{ vm_name }}"
        clone: ubuntu-template
        full: true
        storage: local-lvm
        net:
          net0: 'virtio,bridge=vmbr0,tag=30'
        ipconfig:
          ipconfig0: 'ip={{ vm_ip }}/24,gw=192.168.1.1'
        cores: 4
        memory: 8192
        agent: 1
        state: present
      register: vm_result

    - name: Start VM
      community.proxmox.proxmox_kvm:
        api_host: "{{ proxmox_api_host }}"
        api_user: "{{ proxmox_api_user }}"
        api_token_id: "{{ proxmox_token_id }}"
        api_token_secret: "{{ proxmox_token_secret }}"
        node: "{{ proxmox_node }}"
        vmid: 101
        state: started

    # 2. Register in NetBox
    - name: Create IP address in NetBox
      netbox.netbox.netbox_ip_address:
        netbox_url: "{{ netbox_url }}"
        netbox_token: "{{ netbox_token }}"
        data:
          address: "{{ vm_ip }}/24"
          dns_name: "{{ vm_fqdn }}"
          status: active
          description: "Docker host for Nexus container registry"
          tags:
            - name: production-dns
            - name: ansible
            - name: docker-host

    # 3. Wait for DNS propagation
    - name: Wait for DNS record
      ansible.builtin.command: dig @192.168.3.1 {{ vm_fqdn }} +short
      register: dns_check
      until: dns_check.stdout == vm_ip
      retries: 10
      delay: 5
      changed_when: false

    # 4. Verify DNS resolution
    - name: Verify DNS forward resolution
      ansible.builtin.command: dig @192.168.3.1 {{ vm_fqdn }} +short
      register: forward_dns
      changed_when: false

    - name: Verify DNS reverse resolution
      ansible.builtin.command: dig @192.168.3.1 -x {{ vm_ip }} +short
      register: reverse_dns
      changed_when: false

    - name: Report DNS status
      ansible.builtin.debug:
        msg:
          - "VM created: {{ vm_name }}"
          - "IP: {{ vm_ip }}"
          - "FQDN: {{ vm_fqdn }}"
          - "Forward DNS: {{ forward_dns.stdout }}"
          - "Reverse DNS: {{ reverse_dns.stdout }}"
```

**Run playbook:**

```bash
cd ansible
uv run ansible-playbook playbooks/provision-vm-with-dns.yml
```

## Workflow 2: Bulk IP Address Management

### Reserve IP Range in NetBox

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pynetbox"]
# ///

import pynetbox
import os

netbox = pynetbox.api(
    os.getenv("NETBOX_URL"),
    token=os.getenv("NETBOX_TOKEN")
)

# Define IP range for Docker hosts
docker_ips = [
    {"ip": "192.168.1.100/24", "dns": "docker-01-nexus.spaceships.work", "desc": "Nexus registry"},
    {"ip": "192.168.1.101/24", "dns": "docker-02-gitlab.spaceships.work", "desc": "GitLab CI/CD"},
    {"ip": "192.168.1.102/24", "dns": "docker-03-monitoring.spaceships.work", "desc": "Monitoring stack"},
]

for entry in docker_ips:
    ip = netbox.ipam.ip_addresses.create(
        address=entry["ip"],
        dns_name=entry["dns"],
        description=entry["desc"],
        status="reserved",
        tags=[{"name": "production-dns"}, {"name": "docker-host"}]
    )
    print(f"Created: {ip.dns_name} → {entry['ip']}")
```

**Run script:**

```bash
export NETBOX_URL="https://netbox.spaceships.work"
export NETBOX_TOKEN="your-api-token"

uv run reserve-docker-ips.py
```

### Update Status to Active

When VMs are deployed, update IPs from "reserved" to "active":

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pynetbox"]
# ///

import pynetbox
import os
import sys

netbox = pynetbox.api(
    os.getenv("NETBOX_URL"),
    token=os.getenv("NETBOX_TOKEN")
)

fqdn = sys.argv[1] if len(sys.argv) > 1 else "docker-01-nexus.spaceships.work"

# Find IP by DNS name
ips = netbox.ipam.ip_addresses.filter(dns_name=fqdn)
if not ips:
    print(f"No IP found for {fqdn}")
    sys.exit(1)

ip = ips[0]
ip.status = "active"
ip.save()

print(f"Updated {ip.dns_name}: {ip.address} → active")
```

## Workflow 3: DNS Record Auditing

### Verify NetBox and PowerDNS are in Sync

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pynetbox", "requests"]
# ///

import pynetbox
import requests
import os
import sys

netbox = pynetbox.api(
    os.getenv("NETBOX_URL"),
    token=os.getenv("NETBOX_TOKEN")
)

powerdns_url = os.getenv("POWERDNS_URL", "http://192.168.3.1:8081/api/v1")
powerdns_key = os.getenv("POWERDNS_API_KEY")
zone = sys.argv[1] if len(sys.argv) > 1 else "spaceships.work"

# Get NetBox IPs tagged for DNS
netbox_ips = netbox.ipam.ip_addresses.filter(tag="production-dns")

# Get PowerDNS records
headers = {"X-API-Key": powerdns_key}
pdns_resp = requests.get(f"{powerdns_url}/servers/localhost/zones/{zone}", headers=headers)
pdns_zone = pdns_resp.json()

# Extract A records from PowerDNS
pdns_records = {}
for rrset in pdns_zone.get("rrsets", []):
    if rrset["type"] == "A":
        name = rrset["name"].rstrip(".")
        for record in rrset["records"]:
            pdns_records[name] = record["content"]

# Compare
print("NetBox → PowerDNS Sync Status\n")
print(f"{'DNS Name':<45} {'NetBox IP':<15} {'PowerDNS IP':<15} {'Status'}")
print("-" * 90)

for nb_ip in netbox_ips:
    if not nb_ip.dns_name:
        continue

    dns_name = nb_ip.dns_name.rstrip(".")
    nb_addr = str(nb_ip.address).split("/")[0]
    pdns_addr = pdns_records.get(dns_name, "MISSING")

    if pdns_addr == nb_addr:
        status = "✓ SYNCED"
    elif pdns_addr == "MISSING":
        status = "✗ NOT IN POWERDNS"
    else:
        status = f"✗ MISMATCH"

    print(f"{dns_name:<45} {nb_addr:<15} {pdns_addr:<15} {status}")
```

**Run audit:**

```bash
export NETBOX_URL="https://netbox.spaceships.work"
export NETBOX_TOKEN="your-netbox-token"
export POWERDNS_URL="http://192.168.3.1:8081/api/v1"
export POWERDNS_API_KEY="your-powerdns-key"

uv run dns-audit.py spaceships.work
```

## Workflow 4: Dynamic Inventory for Ansible

### Use NetBox as Inventory Source

**Create dynamic inventory file:**

```yaml
# ansible/inventory/netbox.yml
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...

# Group hosts by tags
group_by:
  - tags

# Group hosts by device role
compose:
  ansible_host: primary_ip4

# Filter to only include VMs with production-dns tag
query_filters:
  - tag: production-dns
```

**Test inventory:**

```bash
ansible-inventory -i ansible/inventory/netbox.yml --list --yaml
```

**Use in playbook:**

```yaml
---
- name: Configure all Docker hosts
  hosts: tag_docker_host  # Automatically grouped by tag
  become: true

  tasks:
    - name: Ensure Docker is running
      ansible.builtin.systemd:
        name: docker
        state: started
        enabled: true

    - name: Report host info
      ansible.builtin.debug:
        msg: "Configuring {{ inventory_hostname }} ({{ ansible_host }})"
```

**Run with dynamic inventory:**

```bash
cd ansible
uv run ansible-playbook -i inventory/netbox.yml playbooks/configure-docker-hosts.yml
```

## Workflow 5: Cleanup and Decommission

### Remove VM and DNS Records

**Terraform destroy workflow:**

```bash
cd terraform/netbox-vm/
tofu destroy

# This will:
# 1. Remove NetBox IP address record
# 2. netbox-powerdns-sync plugin removes DNS records
# 3. Proxmox VM is deleted
```

**Ansible decommission playbook:**

```yaml
---
- name: Decommission VM and remove DNS
  hosts: localhost
  gather_facts: false

  vars:
    vm_fqdn: docker-01-nexus.spaceships.work
    vm_ip: 192.168.1.100

  tasks:
    - name: Remove IP from NetBox
      netbox.netbox.netbox_ip_address:
        netbox_url: "{{ netbox_url }}"
        netbox_token: "{{ netbox_token }}"
        data:
          address: "{{ vm_ip }}/24"
        state: absent

    # DNS records automatically removed by plugin

    - name: Verify DNS record removed
      ansible.builtin.command: dig @192.168.3.1 {{ vm_fqdn }} +short
      register: dns_check
      failed_when: dns_check.stdout != ""
      changed_when: false

    - name: Delete VM from Proxmox
      community.proxmox.proxmox_kvm:
        api_host: "{{ proxmox_api_host }}"
        api_user: "{{ proxmox_api_user }}"
        api_token_id: "{{ proxmox_token_id }}"
        api_token_secret: "{{ proxmox_token_secret }}"
        node: foxtrot
        vmid: 101
        state: absent
```

## Best Practices

### 1. Always Use Tags

Tag IP addresses for automatic DNS sync:

```hcl
tags = ["terraform", "production-dns", "service-type"]
```

### 2. Reserve Before Deploy

Reserve IPs in NetBox before deploying VMs:

```text
Status: reserved → active (after deployment)
```

### 3. Validate Names

Use naming convention validation before creating:

```bash
./tools/validate_dns_naming.py docker-01-nexus.spaceships.work
```

### 4. Monitor Sync Status

Regular audits to ensure NetBox and PowerDNS are in sync:

```bash
./tools/dns-audit.py spaceships.work
```

### 5. Use Descriptions

Document in NetBox description field:

```text
Description: Docker host for Nexus container registry
             Owner: Platform Team
             Related: docker-02-gitlab.spaceships.work
```

### 6. Test DNS Resolution

Always verify DNS after creation:

```bash
dig @192.168.3.1 <fqdn> +short
dig @192.168.3.1 -x <ip> +short
```

## Troubleshooting

### DNS Records Not Created

**Check 1: Tag matching**

```bash
# Verify IP has production-dns tag
curl -H "Authorization: Token $NETBOX_TOKEN" \
  "$NETBOX_URL/api/ipam/ip-addresses/?address=192.168.1.100" | jq '.results[0].tags'
```

**Check 2: Plugin configuration**

```python
# In NetBox: Plugins → NetBox PowerDNS Sync → Zones
# Verify zone exists and tag rules match
```

**Check 3: Manual sync**

```bash
# In NetBox UI: Plugins → NetBox PowerDNS Sync → Zones → <zone> → Sync Now
```

### DNS Resolution Failures

**Check PowerDNS API:**

```bash
curl -H "X-API-Key: $POWERDNS_API_KEY" \
  http://192.168.3.1:8081/api/v1/servers/localhost/zones/spaceships.work
```

**Check DNS server:**

```bash
dig @192.168.3.1 spaceships.work SOA
```

## Further Reading

- [NetBox PowerDNS Sync Plugin](../reference/sync-plugin-reference.md)
- [Terraform NetBox Provider](../reference/terraform-provider-guide.md)
- [DNS Naming Conventions](naming-conventions.md)
