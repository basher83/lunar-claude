# Ansible Dynamic Inventory from NetBox

## Overview

Use NetBox as a dynamic inventory source for Ansible, eliminating the need for static inventory
files and ensuring your automation always has up-to-date infrastructure data.

## Architecture

```text
┌──────────┐
│  NetBox  │ (Source of Truth)
│   IPAM   │
└────┬─────┘
     │
     │ API Query
     │
     ▼
┌────────────────┐
│ nb_inventory   │ (Ansible Plugin)
│    Plugin      │
└────┬───────────┘
     │
     │ Generates Dynamic Inventory
     │
     ▼
┌────────────────┐
│   Ansible      │ (Uses inventory for playbooks)
│  Playbooks     │
└────────────────┘
```

## Prerequisites

### Install NetBox Ansible Collection

```bash
cd ansible
uv run ansible-galaxy collection install netbox.netbox
```

**Or add to requirements.yml:**

```yaml
---
collections:
  - name: netbox.netbox
    version: ">=3.0.0"
```

```bash
uv run ansible-galaxy collection install -r requirements.yml
```

### NetBox API Token

Create read-only API token in NetBox:

**NetBox UI:** Admin → API Tokens → Add

- User: ansible (create service user)
- Key: Generated automatically
- Write enabled: No (read-only)

**Save token securely:**

```bash
# Option 1: Environment variable
export NETBOX_API_TOKEN="your-token-here"

# Option 2: Ansible Vault
ansible-vault create group_vars/all/vault.yml
# Add: netbox_token: "your-token-here"
```

## Basic Configuration

### Create Inventory File

**File:** `ansible/inventory/netbox.yml`

```yaml
---
plugin: netbox.netbox.nb_inventory

# NetBox API connection
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...

# Validate SSL (set to false for self-signed certs)
validate_certs: true

# Group hosts by these NetBox attributes
group_by:
  - device_roles
  - tags
  - sites
  - platforms

# Set ansible_host variable from primary_ip4
compose:
  ansible_host: primary_ip4

# Only include active devices/VMs
query_filters:
  - status: active
```

### Test Inventory

```bash
# List all hosts
ansible-inventory -i ansible/inventory/netbox.yml --list

# View in YAML format
ansible-inventory -i ansible/inventory/netbox.yml --list --yaml

# View specific host
ansible-inventory -i ansible/inventory/netbox.yml --host docker-01-nexus

# Graph inventory
ansible-inventory -i ansible/inventory/netbox.yml --graph
```

## Advanced Configuration

### Filter by Tags

**Only include hosts with specific tag:**

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

# Only hosts tagged with "ansible-managed"
query_filters:
  - tag: ansible-managed
  - status: active

group_by:
  - tags
```

### Filter by Device Role

**Only include specific device roles:**

```yaml
query_filters:
  - role: docker-host
  - role: k8s-node
  - status: active
```

### Custom Groups

**Create custom groups based on NetBox data:**

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

group_by:
  - device_roles
  - tags
  - sites

# Custom group mappings
keyed_groups:
  - key: tags
    prefix: tag
  - key: device_role.name
    prefix: role
  - key: platform.name
    prefix: platform

compose:
  ansible_host: primary_ip4
  ansible_user: ansible
  ansible_become: true
```

### Include Custom Fields

**Use NetBox custom fields in inventory:**

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

compose:
  ansible_host: primary_ip4

  # Use custom fields from NetBox
  backup_schedule: custom_fields.backup_schedule
  monitoring_enabled: custom_fields.monitoring_enabled
  application_owner: custom_fields.owner

group_by:
  - tags
  - custom_fields.environment
```

## Usage Examples

### Example 1: Configure All Docker Hosts

**Inventory:** `ansible/inventory/netbox.yml`

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

query_filters:
  - tag: docker-host
  - status: active

group_by:
  - tags

compose:
  ansible_host: primary_ip4
  ansible_user: ansible
  ansible_become: true
```

**Playbook:** `ansible/playbooks/configure-docker-hosts.yml`

```yaml
---
- name: Configure Docker hosts from NetBox inventory
  hosts: tag_docker_host
  become: true

  tasks:
    - name: Ensure Docker is running
      ansible.builtin.systemd:
        name: docker
        state: started
        enabled: true

    - name: Update Docker daemon config
      ansible.builtin.copy:
        dest: /etc/docker/daemon.json
        content: |
          {
            "log-driver": "json-file",
            "log-opts": {
              "max-size": "10m",
              "max-file": "3"
            }
          }
      notify: Restart Docker

  handlers:
    - name: Restart Docker
      ansible.builtin.systemd:
        name: docker
        state: restarted
```

**Run playbook:**

```bash
cd ansible
uv run ansible-playbook -i inventory/netbox.yml playbooks/configure-docker-hosts.yml
```

### Example 2: Site-Specific Deployments

**Inventory with site grouping:**

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

group_by:
  - sites
  - tags

compose:
  ansible_host: primary_ip4

query_filters:
  - status: active
```

**Playbook targeting specific site:**

```yaml
---
- name: Update hosts at primary site
  hosts: site_homelab  # Automatically grouped by site name
  become: true

  tasks:
    - name: Update all packages
      ansible.builtin.apt:
        upgrade: dist
        update_cache: true
      when: ansible_os_family == "Debian"
```

### Example 3: Platform-Specific Configuration

**Inventory:**

```yaml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: https://netbox.spaceships.work
token: !vault |
  $ANSIBLE_VAULT;...

group_by:
  - platforms

compose:
  ansible_host: primary_ip4

keyed_groups:
  - key: platform.name
    prefix: platform
```

**Playbook with platform-specific tasks:**

```yaml
---
- name: Platform-specific configuration
  hosts: all
  become: true

  tasks:
    - name: Configure Ubuntu hosts
      ansible.builtin.apt:
        name: netbox-agent
        state: present
      when: "'ubuntu' in group_names"

    - name: Configure Rocky hosts
      ansible.builtin.dnf:
        name: netbox-agent
        state: present
      when: "'rocky' in group_names"
```

## Integration with Secrets Management

### Use with Infisical

**Combine dynamic inventory with Infisical secrets:**

```yaml
---
- name: Deploy app with NetBox inventory and Infisical secrets
  hosts: tag_app_server
  become: true

  vars:
    infisical_project_id: "7b832220-24c0-45bc-a5f1-ce9794a31259"
    infisical_env: "prod"
    infisical_path: "/app-config"

  tasks:
    - name: Retrieve database password
      ansible.builtin.include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
      vars:
        secret_name: 'DB_PASSWORD'
        secret_var_name: 'db_password'

    - name: Deploy application config
      ansible.builtin.template:
        src: app-config.j2
        dest: /etc/app/config.yml
        owner: app
        group: app
        mode: '0600'
      vars:
        db_host: "{{ hostvars[groups['tag_database'][0]]['ansible_host'] }}"
        db_password: "{{ db_password }}"
```

## Caching for Performance

### Enable Inventory Caching

**File:** `ansible/ansible.cfg`

```ini
[defaults]
inventory_plugins = /usr/share/ansible/plugins/inventory

[inventory]
enable_plugins = netbox.netbox.nb_inventory

# Enable caching
cache = true
cache_plugin = jsonfile
cache_timeout = 3600  # 1 hour
cache_connection = /tmp/ansible-netbox-cache
```

**Benefits:**

- Faster playbook runs
- Reduced API calls to NetBox
- Works offline (for cache duration)

**Clear cache:**

```bash
rm -rf /tmp/ansible-netbox-cache
```

## Troubleshooting

### Authentication Errors

**Error:** `Failed to query NetBox API`

**Check:**

```bash
# Test API token
curl -H "Authorization: Token $NETBOX_API_TOKEN" \
  https://netbox.spaceships.work/api/dcim/devices/ | jq

# Verify token permissions
# Token must have read access to: DCIM, IPAM, Virtualization
```

### SSL Certificate Errors

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions:**

```yaml
# Option 1: Add CA certificate
validate_certs: true
ssl_ca_cert: /path/to/ca-bundle.crt

# Option 2: Disable for self-signed (dev only!)
validate_certs: false
```

### No Hosts Found

**Error:** Inventory is empty

**Check:**

```bash
# List all devices in NetBox
curl -H "Authorization: Token $NETBOX_API_TOKEN" \
  https://netbox.spaceships.work/api/dcim/devices/ | jq '.count'

# Check query filters
# Ensure devices match your filters (status, tags, etc.)
```

**Debug inventory plugin:**

```bash
ansible-inventory -i ansible/inventory/netbox.yml --list -vvv
```

### Primary IP Not Set

**Error:** `ansible_host` is undefined

**Cause:** Devices/VMs in NetBox don't have primary_ip4 set

**Solution:**

```yaml
# Fallback to custom field or use DNS name
compose:
  ansible_host: primary_ip4 | default(custom_fields.management_ip) | default(name + '.spaceships.work')
```

## Best Practices

### 1. Use Service Account

Create dedicated NetBox user for Ansible:

```text
Username: ansible-automation
Permissions: Read-only (DCIM, IPAM, Virtualization)
Token: Never expires (or set appropriate expiration)
```

### 2. Tag for Inventory

Tag devices/VMs intended for Ansible management:

```text
Tag: ansible-managed
```

**Filter in inventory:**

```yaml
query_filters:
  - tag: ansible-managed
```

### 3. Set Primary IPs

Always set primary_ip4 in NetBox for devices/VMs:

```text
Device → Edit → Primary IPv4
```

### 4. Use Custom Fields

Add custom fields to NetBox for Ansible-specific data:

```text
ansible_user (Text)
ansible_port (Integer)
ansible_python_interpreter (Text)
backup_enabled (Boolean)
```

### 5. Test Before Running

Always test inventory before running playbooks:

```bash
# Verify hosts
ansible-inventory -i inventory/netbox.yml --graph

# Test connectivity
ansible all -i inventory/netbox.yml -m ping
```

### 6. Document in NetBox

Use NetBox description fields to document:

- Ansible playbooks that manage this host
- Special configuration requirements
- Dependencies on other hosts

## Further Reading

- [NetBox Ansible Collection Documentation](https://docs.ansible.com/ansible/latest/collections/netbox/netbox/)
- [Dynamic Inventory Plugin Guide](https://docs.ansible.com/ansible/latest/plugins/inventory.html)
- [NetBox API Documentation](https://demo.netbox.dev/api/docs/)
