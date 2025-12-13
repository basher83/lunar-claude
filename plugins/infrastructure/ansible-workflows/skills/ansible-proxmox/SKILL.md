---
name: ansible-proxmox
description: >
  This skill should be used when automating Proxmox VE with Ansible, creating VMs
  or templates, managing Proxmox clusters, using community.proxmox collection,
  or deciding between native modules and CLI commands (pvecm, pveceph, qm).
---

# Ansible Proxmox Integration

Expert Proxmox automation using community.proxmox collection with minimal CLI usage.

## Module Selection

### Prefer Native Modules

Use `community.proxmox` modules when available:

| Operation | Use Module | NOT CLI |
|-----------|------------|---------|
| Create VM | `community.proxmox.proxmox_kvm` | `qm create` |
| Clone VM | `community.proxmox.proxmox_kvm` | `qm clone` |
| Manage users | `community.proxmox.proxmox_user` | `pveum user` |
| Manage groups | `community.proxmox.proxmox_group` | `pveum group` |
| Manage pools | `community.proxmox.proxmox_pool` | `pveum pool` |
| Manage ACLs | `community.proxmox.proxmox_acl` | `pveum acl` |
| Storage | `community.proxmox.proxmox_storage` | `pvesm` |

### When CLI is Required

Some operations lack native modules:

| Operation | Requires CLI | Reason |
|-----------|--------------|--------|
| Cluster create | `pvecm create` | No module exists |
| Cluster join | `pvecm add` | No module exists |
| CEPH init | `pveceph init` | Complex workflow |
| CEPH OSD | `pveceph osd create` | Complex workflow |

## Native Module Examples

### Create VM from Template

```yaml
- name: Create VM from template
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_token_id: "{{ proxmox_token_id }}"
    api_token_secret: "{{ proxmox_token_secret }}"
    node: "{{ proxmox_node }}"
    vmid: "{{ vm_id }}"
    name: "{{ vm_name }}"
    clone: "{{ template_name }}"
    full: true
    storage: local-lvm
    memory: "{{ vm_memory | default(4096) }}"
    cores: "{{ vm_cores | default(2) }}"
    state: present
  delegate_to: localhost
```

### Manage Proxmox User

```yaml
- name: Create Terraform user
  community.proxmox.proxmox_user:
    api_host: "{{ proxmox_api_host }}"
    api_user: "root@pam"
    api_password: "{{ proxmox_root_password }}"
    userid: "terraform@pve"
    comment: "Terraform automation user"
    groups:
      - automation
    state: present
  no_log: true
  delegate_to: localhost
```

### Configure ACLs

```yaml
- name: Grant terraform permissions
  community.proxmox.proxmox_acl:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_token_id: "{{ proxmox_token_id }}"
    api_token_secret: "{{ proxmox_token_secret }}"
    path: "/"
    users:
      - terraform@pve
    roles:
      - Administrator
    state: present
  delegate_to: localhost
```

## CLI with Idempotency

When CLI is required, add proper idempotency controls:

### Cluster Formation

```yaml
- name: Check existing cluster status
  ansible.builtin.command: pvecm status
  register: cluster_status
  failed_when: false
  changed_when: false

- name: Set cluster facts
  ansible.builtin.set_fact:
    is_cluster_member: "{{ cluster_status.rc == 0 }}"
    in_target_cluster: "{{ cluster_name in cluster_status.stdout }}"

- name: Create cluster on primary node
  ansible.builtin.command: pvecm create {{ cluster_name }}
  when:
    - inventory_hostname == groups['proxmox'][0]
    - not in_target_cluster
  register: cluster_create
  changed_when: cluster_create.rc == 0

- name: Join cluster on secondary nodes
  ansible.builtin.command: pvecm add {{ hostvars[groups['proxmox'][0]].ansible_host }}
  when:
    - inventory_hostname != groups['proxmox'][0]
    - not is_cluster_member
  register: cluster_join
  changed_when: cluster_join.rc == 0
```

### API Token Creation

```yaml
- name: Create API token
  ansible.builtin.command: >
    pveum user token add {{ username }}@pam {{ token_name }}
    --privsep 0
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
  no_log: true
```

## Authentication Patterns

### API Token (Recommended)

```yaml
# Store token in variables or Infisical
proxmox_api_host: "192.168.1.10"
proxmox_api_user: "terraform@pve"
proxmox_token_id: "automation"
proxmox_token_secret: "{{ lookup('infisical', 'PROXMOX_TOKEN_SECRET') }}"

- name: Create VM
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_token_id: "{{ proxmox_token_id }}"
    api_token_secret: "{{ proxmox_token_secret }}"
    # ... rest of config
```

### Root Password (Local Operations)

For operations on Proxmox nodes themselves:

```yaml
- name: Retrieve root password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_ROOT_PASSWORD'
    secret_var_name: 'proxmox_root_password'

- name: Configure via API
  community.proxmox.proxmox_user:
    api_host: "{{ inventory_hostname }}"
    api_user: "root@pam"
    api_password: "{{ proxmox_root_password }}"
    # ... config
  no_log: true
```

## Cluster Operations

### Idempotent Cluster Status Check

```yaml
- name: Get cluster status
  ansible.builtin.command: pvecm status
  register: cluster_status
  changed_when: false
  failed_when: false

- name: Get cluster nodes
  ansible.builtin.command: pvecm nodes
  register: cluster_nodes
  changed_when: false
  failed_when: false
  when: cluster_status.rc == 0

- name: Set cluster facts
  ansible.builtin.set_fact:
    cluster_exists: "{{ cluster_status.rc == 0 }}"
    cluster_node_count: "{{ cluster_nodes.stdout_lines | length | default(0) }}"
    is_quorate: "{{ 'Quorate: Yes' in cluster_status.stdout | default('') }}"
```

### Verify Cluster Health

```yaml
- name: Verify cluster quorum
  ansible.builtin.command: pvecm status
  register: cluster_health
  changed_when: false
  failed_when: "'Quorate: Yes' not in cluster_health.stdout"

- name: Verify expected node count
  ansible.builtin.command: pvecm nodes
  register: nodes_check
  changed_when: false
  failed_when: nodes_check.stdout_lines | length != groups['proxmox'] | length
```

## CEPH Integration

### Initialize CEPH

```yaml
- name: Check if CEPH is initialized
  ansible.builtin.command: pveceph status
  register: ceph_status
  changed_when: false
  failed_when: false

- name: Initialize CEPH
  ansible.builtin.command: >
    pveceph init --network {{ ceph_network }}
  when:
    - inventory_hostname == groups['proxmox'][0]
    - ceph_status.rc != 0
  register: ceph_init
  changed_when: ceph_init.rc == 0
```

### Create OSD

```yaml
- name: Check if OSD exists on device
  ansible.builtin.command: >
    pveceph osd list
  register: osd_list
  changed_when: false

- name: Create OSD
  ansible.builtin.command: >
    pveceph osd create {{ item }}
  loop: "{{ ceph_osd_devices }}"
  when: item not in osd_list.stdout
  register: osd_create
  changed_when: osd_create.rc == 0
```

## Network Configuration

Use `community.general.interfaces_file` for network config:

```yaml
- name: Configure VLAN-aware bridge
  community.general.interfaces_file:
    iface: vmbr1
    option: bridge-vlan-aware
    value: "yes"
    backup: true
    state: present
  notify: reload network

- name: Set bridge ports
  community.general.interfaces_file:
    iface: vmbr1
    option: bridge-ports
    value: "bond0"
    backup: true
    state: present
  notify: reload network
```

## Anti-Patterns

### Using CLI When Module Exists

```yaml
# BAD - Module exists for this
- name: Create user
  ansible.builtin.command: pveum user add terraform@pve

# GOOD
- name: Create user
  community.proxmox.proxmox_user:
    api_host: "{{ proxmox_api_host }}"
    api_user: "root@pam"
    api_password: "{{ password }}"
    userid: "terraform@pve"
    state: present
```

### Missing Idempotency on CLI

```yaml
# BAD - Will fail on second run
- name: Create cluster
  ansible.builtin.command: pvecm create MyCluster

# GOOD
- name: Check cluster status
  ansible.builtin.command: pvecm status
  register: cluster_check
  changed_when: false
  failed_when: false

- name: Create cluster
  ansible.builtin.command: pvecm create MyCluster
  when: cluster_check.rc != 0
```

### Running on Wrong Host

```yaml
# BAD - API calls from managed node
- name: Create VM
  community.proxmox.proxmox_kvm:
    api_host: "{{ inventory_hostname }}"  # Calling itself
    # ...

# GOOD - Delegate API calls to localhost
- name: Create VM
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
    # ...
  delegate_to: localhost
```

## Installing the Collection

```bash
# Install community.proxmox
uv run ansible-galaxy collection install community.proxmox

# Or via requirements.yml
cd ansible
uv run ansible-galaxy collection install -r requirements.yml
```

## Additional Resources

For detailed Proxmox automation patterns, consult:

- **`references/ceph-automation.md`** - CEPH storage deployment and OSD management
- **`references/cluster-automation.md`** - Proxmox cluster creation and node joining
- **`references/network-automation.md`** - VLAN-aware bridges and network configuration
- **`references/community-proxmox-plugin-index.md`** - Complete community.proxmox module reference

## Related Skills

- **ansible-fundamentals** - Core module selection patterns
- **ansible-idempotency** - Making CLI commands idempotent
- **ansible-error-handling** - Error recovery for cluster operations
