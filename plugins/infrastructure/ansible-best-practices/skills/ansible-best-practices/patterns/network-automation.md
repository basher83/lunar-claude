# Network Automation Patterns

Best practices for declarative network configuration in Proxmox VE environments with Ansible.

## Pattern: Declarative Network Interface Configuration

**Problem**: Network configuration is complex, error-prone when done manually, and difficult to maintain across multiple nodes.

**Solution**: Use declarative configuration with data structures that describe desired state.

### Configuration Model

```yaml
# group_vars/matrix_cluster.yml
network_interfaces:
  management:
    bridge: vmbr0
    physical_port: enp4s0
    address: "192.168.3.{{ node_id }}/24"
    gateway: "192.168.3.1"
    vlan_aware: true
    vlan_ids: "9"
    mtu: 1500
    comment: "Management network"

  ceph_public:
    bridge: vmbr1
    physical_port: enp5s0f0np0
    address: "192.168.5.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Public network"

  ceph_private:
    bridge: vmbr2
    physical_port: enp5s0f1np1
    address: "192.168.7.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Private network"

# VLAN configuration
vlans:
  - id: 9
    raw_device: vmbr0
    address: "192.168.8.{{ node_id }}/24"
    comment: "Corosync network"

# Node-specific IDs
node_ids:
  foxtrot: 5
  golf: 6
  hotel: 7

# Set node_id based on hostname
node_id: "{{ node_ids[inventory_hostname_short] }}"
```

### Implementation

```yaml
# roles/proxmox_networking/tasks/bridges.yml
---
- name: Create Proxmox bridge interfaces in /etc/network/interfaces
  ansible.builtin.blockinfile:
    path: /etc/network/interfaces
    marker: "# {mark} ANSIBLE MANAGED BLOCK - {{ item.key }}"
    block: |
      # {{ item.value.comment }}
      auto {{ item.value.bridge }}
      iface {{ item.value.bridge }} inet static
          address {{ item.value.address }}
          {% if item.value.gateway is defined %}
          gateway {{ item.value.gateway }}
          {% endif %}
          bridge-ports {{ item.value.physical_port }}
          bridge-stp off
          bridge-fd 0
          {% if item.value.vlan_aware | default(false) %}
          bridge-vlan-aware yes
          {% endif %}
          {% if item.value.vlan_ids is defined %}
          bridge-vids {{ item.value.vlan_ids }}
          {% endif %}
          {% if item.value.mtu is defined and item.value.mtu != 1500 %}
          mtu {{ item.value.mtu }}
          {% endif %}
    create: false
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"
  notify:
    - reload networking
```

## Pattern: VLAN Interface Creation

**Problem**: VLAN interfaces must be created at runtime and persist across reboots.

**Solution**: Manage both persistent configuration and runtime state.

### Implementation

```yaml
# roles/proxmox_networking/tasks/vlans.yml
---
- name: Configure VLAN interfaces in /etc/network/interfaces
  ansible.builtin.blockinfile:
    path: /etc/network/interfaces
    marker: "# {mark} ANSIBLE MANAGED BLOCK - vlan{{ item.id }}"
    block: |
      # {{ item.comment }}
      auto vlan{{ item.id }}
      iface vlan{{ item.id }} inet static
          address {{ item.address }}
          vlan-raw-device {{ item.raw_device }}
    create: false
  loop: "{{ vlans }}"
  loop_control:
    label: "vlan{{ item.id }}"
  notify:
    - reload networking

- name: Check if VLAN interface exists
  ansible.builtin.command:
    cmd: "ip link show vlan{{ item.id }}"
  register: vlan_check
  failed_when: false
  changed_when: false
  loop: "{{ vlans }}"
  loop_control:
    label: "vlan{{ item.id }}"

- name: Create VLAN interface at runtime
  ansible.builtin.command:
    cmd: "ip link add link {{ item.item.raw_device }} name vlan{{ item.item.id }} type vlan id {{ item.item.id }}"
  when: item.rc != 0
  loop: "{{ vlan_check.results }}"
  loop_control:
    label: "vlan{{ item.item.id }}"
  notify:
    - reload networking

- name: Bring up VLAN interface
  ansible.builtin.command:
    cmd: "ip link set vlan{{ item.item.id }} up"
  when: item.rc != 0
  loop: "{{ vlan_check.results }}"
  loop_control:
    label: "vlan{{ item.item.id }}"
```

## Pattern: MTU Configuration for Jumbo Frames

**Problem**: CEPH storage networks require jumbo frames (MTU 9000) for optimal performance.

**Solution**: Configure MTU at both interface and bridge level with verification.

### Implementation

```yaml
# roles/proxmox_networking/tasks/mtu.yml
---
- name: Set MTU on physical interfaces
  ansible.builtin.command:
    cmd: "ip link set {{ item.value.physical_port }} mtu {{ item.value.mtu }}"
  when: item.value.mtu is defined and item.value.mtu > 1500
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.physical_port }}"
  register: mtu_set
  changed_when: mtu_set.rc == 0

- name: Set MTU on bridge interfaces
  ansible.builtin.command:
    cmd: "ip link set {{ item.value.bridge }} mtu {{ item.value.mtu }}"
  when: item.value.mtu is defined and item.value.mtu > 1500
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"
  register: bridge_mtu_set
  changed_when: bridge_mtu_set.rc == 0

- name: Verify MTU configuration
  ansible.builtin.command:
    cmd: "ip link show {{ item.value.bridge }}"
  register: mtu_check
  changed_when: false
  failed_when: "'mtu ' + (item.value.mtu | string) not in mtu_check.stdout"
  when: item.value.mtu is defined and item.value.mtu > 1500
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Test jumbo frame connectivity (CEPH networks only)
  ansible.builtin.command:
    cmd: "ping -c 3 -M do -s 8972 {{ hostvars[item].ansible_host }}"
  register: jumbo_test
  changed_when: false
  failed_when: false
  when:
    - "'ceph' in network_interfaces"
    - item != inventory_hostname
  loop: "{{ groups['proxmox'] }}"
  loop_control:
    label: "{{ item }}"

- name: Report jumbo frame test results
  ansible.builtin.debug:
    msg: "Jumbo frame test to {{ item.item }}: {{ 'PASSED' if item.rc == 0 else 'FAILED' }}"
  when: item is not skipped
  loop: "{{ jumbo_test.results }}"
  loop_control:
    label: "{{ item.item }}"
```

## Pattern: Bridge VLAN-Aware Configuration

**Problem**: VMs need access to multiple VLANs through a single bridge interface.

**Solution**: Enable VLAN-aware bridges and specify allowed VLAN IDs.

### Implementation

```yaml
# roles/proxmox_networking/tasks/vlan_aware.yml
---
- name: Check current bridge VLAN awareness
  ansible.builtin.command:
    cmd: "bridge vlan show dev {{ item.value.bridge }}"
  register: vlan_aware_check
  changed_when: false
  failed_when: false
  when: item.value.vlan_aware | default(false)
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Enable VLAN filtering on bridge
  ansible.builtin.command:
    cmd: "ip link set {{ item.value.bridge }} type bridge vlan_filtering 1"
  when:
    - item.value.vlan_aware | default(false)
    - "'vlan_filtering 0' in vlan_aware_check.results[ansible_loop.index0].stdout | default('')"
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"
    extended: true
  register: vlan_filtering
  changed_when: vlan_filtering.rc == 0

- name: Configure allowed VLANs on bridge
  ansible.builtin.command:
    cmd: "bridge vlan add vid {{ item.value.vlan_ids }} dev {{ item.value.bridge }} self"
  when:
    - item.value.vlan_aware | default(false)
    - item.value.vlan_ids is defined
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"
  register: vlan_add
  changed_when: vlan_add.rc == 0
  failed_when:
    - vlan_add.rc != 0
    - "'already exists' not in vlan_add.stderr"
```

## Pattern: Network Configuration Validation

**Problem**: Network misconfigurations can cause node isolation and cluster failures.

**Solution**: Validate configuration before and after applying changes.

### Implementation

```yaml
# roles/proxmox_networking/tasks/validate.yml
---
- name: Verify interface configuration file syntax
  ansible.builtin.command:
    cmd: ifup --no-act {{ item.value.bridge }}
  register: config_syntax
  changed_when: false
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Check interface operational status
  ansible.builtin.command:
    cmd: "ip link show {{ item.value.bridge }}"
  register: interface_status
  changed_when: false
  failed_when: "'state UP' not in interface_status.stdout"
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Verify IP address assignment
  ansible.builtin.command:
    cmd: "ip addr show {{ item.value.bridge }}"
  register: ip_status
  changed_when: false
  failed_when: item.value.address.split('/')[0] not in ip_status.stdout
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Test connectivity to gateway
  ansible.builtin.command:
    cmd: "ping -c 3 -W 2 {{ item.value.gateway }}"
  register: gateway_ping
  changed_when: false
  when: item.value.gateway is defined
  loop: "{{ network_interfaces | dict2items }}"
  loop_control:
    label: "{{ item.value.bridge }}"

- name: Test connectivity to cluster peers
  ansible.builtin.command:
    cmd: "ping -c 3 -W 2 {{ hostvars[item].ansible_host }}"
  register: peer_ping
  changed_when: false
  when: item != inventory_hostname
  loop: "{{ groups['proxmox'] }}"
  loop_control:
    label: "{{ item }}"
```

## Anti-Pattern: Excessive Shell Commands

**❌ Don't Do This**:

```yaml
- name: Create VLAN interface if needed
  ansible.builtin.shell: |
    if ! ip link show vmbr0.{{ item.vlan }} >/dev/null 2>&1; then
      ip link add link vmbr0 name vmbr0.{{ item.vlan }} type vlan id {{ item.vlan }}
      ip link set vmbr0.{{ item.vlan }} up
    fi
```

**Problems**:

- Shell-specific syntax
- Limited idempotency
- No check-mode support
- Harder to test
- Error handling is fragile

**✅ Do This Instead**:

```yaml
- name: Check if VLAN interface exists
  ansible.builtin.command:
    cmd: "ip link show vmbr0.{{ item.vlan }}"
  register: vlan_check
  failed_when: false
  changed_when: false

- name: Create VLAN interface
  ansible.builtin.command:
    cmd: "ip link add link vmbr0 name vmbr0.{{ item.vlan }} type vlan id {{ item.vlan }}"
  when: vlan_check.rc != 0
  register: vlan_create
  changed_when: vlan_create.rc == 0

- name: Bring up VLAN interface
  ansible.builtin.command:
    cmd: "ip link set vmbr0.{{ item.vlan }} up"
  when: vlan_check.rc != 0
```

## Handler Configuration

```yaml
# roles/proxmox_networking/handlers/main.yml
---
- name: reload networking
  ansible.builtin.systemd:
    name: networking
    state: reloaded
  listen: reload networking
  throttle: 1  # One node at a time to prevent cluster disruption

- name: restart networking
  ansible.builtin.systemd:
    name: networking
    state: restarted
  listen: restart networking
  throttle: 1
  when: not ansible_check_mode  # Don't restart in check mode
```

## Complete Role Example

```yaml
# roles/proxmox_networking/tasks/main.yml
---
- name: Validate prerequisites
  ansible.builtin.include_tasks: prerequisites.yml

- name: Configure bridge interfaces
  ansible.builtin.include_tasks: bridges.yml

- name: Configure VLAN interfaces
  ansible.builtin.include_tasks: vlans.yml
  when: vlans is defined and vlans | length > 0

- name: Configure VLAN-aware bridges
  ansible.builtin.include_tasks: vlan_aware.yml

- name: Configure MTU for jumbo frames
  ansible.builtin.include_tasks: mtu.yml
  when: network_jumbo_frames_enabled | default(false)

- name: Validate network configuration
  ansible.builtin.include_tasks: validate.yml
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/network-config.yml

# Check mode (dry run) - won't restart networking
ansible-playbook playbooks/network-config.yml --check --diff

# Apply to single node first
ansible-playbook playbooks/network-config.yml --limit foxtrot

# Verify MTU configuration
ansible -i inventory/proxmox.yml matrix_cluster -m shell \
  -a "ip link show | grep -E 'vmbr[12]' | grep mtu"

# Test jumbo frames
ansible -i inventory/proxmox.yml matrix_cluster -m shell \
  -a "ping -c 3 -M do -s 8972 192.168.5.6"
```

## Matrix Cluster Example

```yaml
# Example playbook for Matrix cluster networking
---
- name: Configure Matrix Cluster Networking
  hosts: matrix_cluster
  become: true
  serial: 1  # Configure one node at a time

  roles:
    - role: proxmox_networking
      vars:
        network_jumbo_frames_enabled: true
```

## Related Patterns

- [Cluster Automation](cluster-automation.md) - Cluster formation with corosync networking
- [CEPH Storage](ceph-automation.md) - CEPH network requirements
- [Error Handling](error-handling.md) - Network validation error handling

## References

- ProxSpray analysis: `docs/proxspray-analysis.md` (lines 209-331)
- Proxmox VE Network Configuration documentation
- Linux bridge configuration guide
- VLAN configuration best practices
