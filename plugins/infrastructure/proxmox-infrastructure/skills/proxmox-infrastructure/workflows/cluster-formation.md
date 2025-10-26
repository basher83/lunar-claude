# Proxmox Cluster Formation Workflow

Complete guide to forming a Proxmox VE cluster using Ansible automation with idempotent patterns.

## Overview

This workflow automates the creation of a Proxmox VE cluster with:

- Hostname resolution configuration
- SSH key distribution for cluster operations
- Idempotent cluster initialization
- Corosync network configuration
- Quorum and health verification

## Prerequisites

Before forming a cluster:

1. **All nodes must have:**
   - Proxmox VE 9.x installed
   - Network connectivity on management network
   - Dedicated corosync network configured (VLAN 9 for Matrix)
   - Unique hostnames
   - Synchronized time (NTP configured)

2. **Minimum requirements:**
   - At least 3 nodes for quorum (production)
   - 1 node for development/testing (non-recommended)

3. **Network requirements:**
   - All nodes must be able to resolve each other's hostnames
   - Corosync network must be isolated (no VM traffic)
   - Low latency between nodes (<2ms recommended)
   - MTU 1500 on management network

## Phase 1: Prepare Cluster Nodes

### Step 1: Verify Prerequisites

```yaml
# roles/proxmox_cluster/tasks/prerequisites.yml
---
- name: Check Proxmox VE is installed
  ansible.builtin.stat:
    path: /usr/bin/pvecm
  register: pvecm_binary
  failed_when: not pvecm_binary.stat.exists

- name: Get Proxmox VE version
  ansible.builtin.command:
    cmd: pveversion
  register: pve_version
  changed_when: false

- name: Verify minimum Proxmox VE version
  ansible.builtin.assert:
    that:
      - "'pve-manager/9' in pve_version.stdout or 'pve-manager/8' in pve_version.stdout"
    fail_msg: "Proxmox VE 8.x or 9.x required"

- name: Verify minimum node count for production
  ansible.builtin.assert:
    that:
      - groups[cluster_group] | length >= 3
    fail_msg: "Production cluster requires at least 3 nodes for quorum"
  when: cluster_environment == 'production'

- name: Check no existing cluster membership
  ansible.builtin.command:
    cmd: pvecm status
  register: existing_cluster
  failed_when: false
  changed_when: false

- name: Display cluster warning if already member
  ansible.builtin.debug:
    msg: |
      WARNING: Node {{ inventory_hostname }} is already a cluster member.
      Current cluster: {{ existing_cluster.stdout }}
      This playbook will attempt to join the target cluster.
  when:
    - existing_cluster.rc == 0
    - cluster_name not in existing_cluster.stdout
```

### Step 2: Configure Hostname Resolution

```yaml
# roles/proxmox_cluster/tasks/hosts_config.yml
---
- name: Ensure cluster nodes in /etc/hosts (management IP)
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: "^{{ item.management_ip }}\\s+"
    line: "{{ item.management_ip }} {{ item.fqdn }} {{ item.short_name }}"
    state: present
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.short_name }}"

- name: Ensure corosync IPs in /etc/hosts
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: "^{{ item.corosync_ip }}\\s+"
    line: "{{ item.corosync_ip }} {{ item.short_name }}-corosync"
    state: present
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.short_name }}"

- name: Verify hostname resolution (forward)
  ansible.builtin.command:
    cmd: "getent hosts {{ item.fqdn }}"
  register: host_lookup
  failed_when: host_lookup.rc != 0
  changed_when: false
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.fqdn }}"

- name: Verify hostname resolution (reverse)
  ansible.builtin.command:
    cmd: "getent hosts {{ item.management_ip }}"
  register: reverse_lookup
  failed_when:
    - reverse_lookup.rc != 0
  changed_when: false
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.management_ip }}"

- name: Test corosync network connectivity
  ansible.builtin.command:
    cmd: "ping -c 3 -W 2 {{ item.corosync_ip }}"
  register: corosync_ping
  changed_when: false
  when: item.short_name != inventory_hostname_short
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.short_name }}"
```

### Step 3: Distribute SSH Keys

```yaml
# roles/proxmox_cluster/tasks/ssh_keys.yml
---
- name: Generate SSH key for root (if not exists)
  ansible.builtin.user:
    name: root
    generate_ssh_key: true
    ssh_key_type: ed25519
    ssh_key_comment: "root@{{ inventory_hostname }}"
  register: root_ssh_key

- name: Fetch public keys from all nodes
  ansible.builtin.slurp:
    src: /root/.ssh/id_ed25519.pub
  register: node_public_keys

- name: Distribute SSH keys to all nodes
  ansible.posix.authorized_key:
    user: root
    state: present
    key: "{{ hostvars[item].node_public_keys.content | b64decode }}"
    comment: "cluster-{{ item }}"
  loop: "{{ groups[cluster_group] }}"
  when: item != inventory_hostname

- name: Populate known_hosts with node SSH keys
  ansible.builtin.shell:
    cmd: "ssh-keyscan -H {{ item }} >> /root/.ssh/known_hosts"
  when: item != inventory_hostname
  loop: "{{ groups[cluster_group] }}"
  loop_control:
    label: "{{ item }}"
  changed_when: true

- name: Test SSH connectivity to all nodes
  ansible.builtin.command:
    cmd: "ssh -o ConnectTimeout=5 {{ item }} hostname"
  register: ssh_test
  changed_when: false
  when: item != inventory_hostname
  loop: "{{ groups[cluster_group] }}"
  loop_control:
    label: "{{ item }}"
```

## Phase 2: Initialize Cluster

### Step 4: Create Cluster (First Node Only)

```yaml
# roles/proxmox_cluster/tasks/cluster_init.yml
---
- name: Check existing cluster status
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_status
  failed_when: false
  changed_when: false

- name: Get cluster nodes list
  ansible.builtin.command:
    cmd: pvecm nodes
  register: cluster_nodes_check
  failed_when: false
  changed_when: false

- name: Set cluster facts
  ansible.builtin.set_fact:
    in_target_cluster: "{{ cluster_status.rc == 0 and cluster_name in cluster_status.stdout }}"

- name: Create new cluster on first node
  ansible.builtin.command:
    cmd: "pvecm create {{ cluster_name }} --link0 {{ corosync_link0_address }}"
  when: not in_target_cluster
  register: cluster_create
  changed_when: cluster_create.rc == 0

- name: Wait for cluster to initialize
  ansible.builtin.pause:
    seconds: 10
  when: cluster_create.changed

- name: Verify cluster creation
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_verify
  changed_when: false
  failed_when: cluster_name not in cluster_verify.stdout

- name: Display cluster status
  ansible.builtin.debug:
    var: cluster_verify.stdout_lines
  when: cluster_create.changed or ansible_verbosity > 0
```

### Step 5: Join Nodes to Cluster

```yaml
# roles/proxmox_cluster/tasks/cluster_join.yml
---
- name: Check if already in cluster
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_status
  failed_when: false
  changed_when: false

- name: Set membership facts
  ansible.builtin.set_fact:
    is_cluster_member: "{{ cluster_status.rc == 0 }}"
    in_target_cluster: "{{ cluster_status.rc == 0 and cluster_name in cluster_status.stdout }}"

- name: Get first node hostname
  ansible.builtin.set_fact:
    first_node_hostname: "{{ hostvars[groups[cluster_group][0]].inventory_hostname }}"

- name: Join cluster
  ansible.builtin.command:
    cmd: >
      pvecm add {{ first_node_hostname }}
      --link0 {{ corosync_link0_address }}
  when:
    - not is_cluster_member or not in_target_cluster
  register: cluster_join
  changed_when: cluster_join.rc == 0
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"

- name: Wait for node to join cluster
  ansible.builtin.pause:
    seconds: 10
  when: cluster_join.changed

- name: Verify cluster membership
  ansible.builtin.command:
    cmd: pvecm status
  register: join_verify
  changed_when: false
  failed_when:
    - "'Quorate: Yes' not in join_verify.stdout"
```

## Phase 3: Configure Corosync

### Step 6: Corosync Network Configuration

```yaml
# roles/proxmox_cluster/tasks/corosync.yml
---
- name: Get current corosync configuration
  ansible.builtin.slurp:
    src: /etc/pve/corosync.conf
  register: corosync_conf_current

- name: Parse current corosync config
  ansible.builtin.set_fact:
    current_corosync: "{{ corosync_conf_current.content | b64decode }}"

- name: Check if corosync config needs update
  ansible.builtin.set_fact:
    corosync_needs_update: "{{ corosync_network not in current_corosync }}"

- name: Backup corosync.conf
  ansible.builtin.copy:
    src: /etc/pve/corosync.conf
    dest: "/etc/pve/corosync.conf.{{ ansible_date_time.epoch }}.bak"
    remote_src: true
    mode: '0640'
  when: corosync_needs_update
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Update corosync configuration
  ansible.builtin.template:
    src: corosync.conf.j2
    dest: /etc/pve/corosync.conf.new
    validate: corosync-cfgtool -c %s
    mode: '0640'
  when: corosync_needs_update
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Apply new corosync configuration
  ansible.builtin.copy:
    src: /etc/pve/corosync.conf.new
    dest: /etc/pve/corosync.conf
    remote_src: true
    mode: '0640'
  when: corosync_needs_update
  notify:
    - reload corosync
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
```

**Corosync Template Example:**

```jinja2
# templates/corosync.conf.j2
totem {
  version: 2
  cluster_name: {{ cluster_name }}
  transport: knet
  crypto_cipher: aes256
  crypto_hash: sha256

  interface {
    linknumber: 0
    knet_link_priority: 255
  }
}

nodelist {
{% for node in cluster_nodes %}
  node {
    name: {{ node.short_name }}
    nodeid: {{ node.node_id }}
    quorum_votes: 1
    ring0_addr: {{ node.corosync_ip }}
  }
{% endfor %}
}

quorum {
  provider: corosync_votequorum
{% if cluster_nodes | length == 2 %}
  two_node: 1
{% endif %}
}

logging {
  to_logfile: yes
  logfile: /var/log/corosync/corosync.log
  to_syslog: yes
  timestamp: on
}
```

## Phase 4: Verify Cluster Health

### Step 7: Health Checks

```yaml
# roles/proxmox_cluster/tasks/verify.yml
---
- name: Wait for cluster to stabilize
  ansible.builtin.pause:
    seconds: 15

- name: Check cluster quorum
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_health
  changed_when: false
  failed_when: "'Quorate: Yes' not in cluster_health.stdout"

- name: Get cluster node count
  ansible.builtin.command:
    cmd: pvecm nodes
  register: cluster_nodes_final
  changed_when: false

- name: Verify expected node count
  ansible.builtin.assert:
    that:
      - cluster_nodes_final.stdout_lines | length >= groups[cluster_group] | length
    fail_msg: "Expected {{ groups[cluster_group] | length }} nodes but found {{ cluster_nodes_final.stdout_lines | length }}"

- name: Check corosync ring status
  ansible.builtin.command:
    cmd: corosync-cfgtool -s
  register: corosync_status
  changed_when: false

- name: Verify all nodes in corosync
  ansible.builtin.assert:
    that:
      - "'online' in corosync_status.stdout"
    fail_msg: "Corosync ring issues detected"

- name: Get cluster configuration version
  ansible.builtin.command:
    cmd: corosync-cmapctl -b totem.config_version
  register: config_version
  changed_when: false

- name: Display cluster health summary
  ansible.builtin.debug:
    msg: |
      Cluster: {{ cluster_name }}
      Quorum: {{ 'Yes' if 'Quorate: Yes' in cluster_health.stdout else 'No' }}
      Nodes: {{ cluster_nodes_final.stdout_lines | length }}
      Config Version: {{ config_version.stdout }}
```

## Matrix Cluster Example Configuration

```yaml
# group_vars/matrix_cluster.yml
---
cluster_name: "Matrix"
cluster_group: "matrix_cluster"
cluster_environment: "production"

# Corosync configuration
corosync_network: "192.168.8.0/24"  # VLAN 9

# Node configuration
cluster_nodes:
  - short_name: foxtrot
    fqdn: foxtrot.matrix.spaceships.work
    management_ip: 192.168.3.5
    corosync_ip: 192.168.8.5
    node_id: 1

  - short_name: golf
    fqdn: golf.matrix.spaceships.work
    management_ip: 192.168.3.6
    corosync_ip: 192.168.8.6
    node_id: 2

  - short_name: hotel
    fqdn: hotel.matrix.spaceships.work
    management_ip: 192.168.3.7
    corosync_ip: 192.168.8.7
    node_id: 3

# Set per-node corosync address
corosync_link0_address: "{{ cluster_nodes | selectattr('short_name', 'equalto', inventory_hostname_short) | map(attribute='corosync_ip') | first }}"
```

## Complete Playbook Example

```yaml
# playbooks/cluster-init.yml
---
- name: Initialize Proxmox Cluster
  hosts: "{{ cluster_group | default('matrix_cluster') }}"
  become: true
  serial: 1  # One node at a time for safety

  pre_tasks:
    - name: Validate cluster group is defined
      ansible.builtin.assert:
        that:
          - cluster_group is defined
          - cluster_name is defined
          - cluster_nodes is defined
        fail_msg: "Required variables not defined in group_vars"

    - name: Display cluster configuration
      ansible.builtin.debug:
        msg: |
          Forming cluster: {{ cluster_name }}
          Nodes: {{ cluster_nodes | map(attribute='short_name') | join(', ') }}
          Corosync network: {{ corosync_network }}
      run_once: true

  tasks:
    - name: Verify prerequisites
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/prerequisites.yml"

    - name: Configure /etc/hosts
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/hosts_config.yml"

    - name: Distribute SSH keys
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/ssh_keys.yml"

    # First node creates cluster
    - name: Initialize cluster on first node
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/cluster_init.yml"
      when: inventory_hostname == groups[cluster_group][0]

    # Wait for first node
    - name: Wait for first node to complete
      ansible.builtin.pause:
        seconds: 20
      when: inventory_hostname != groups[cluster_group][0]

    # Other nodes join
    - name: Join cluster on other nodes
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/cluster_join.yml"
      when: inventory_hostname != groups[cluster_group][0]

    - name: Configure corosync
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/corosync.yml"

    - name: Verify cluster health
      ansible.builtin.include_tasks: "{{ role_path }}/tasks/verify.yml"

  post_tasks:
    - name: Display final cluster status
      ansible.builtin.command:
        cmd: pvecm status
      register: final_status
      changed_when: false
      delegate_to: "{{ groups[cluster_group][0] }}"
      run_once: true

    - name: Show cluster status
      ansible.builtin.debug:
        var: final_status.stdout_lines
      run_once: true

  handlers:
    - name: reload corosync
      ansible.builtin.systemd:
        name: corosync
        state: reloaded
      throttle: 1
```

## Usage

### Initialize Matrix Cluster

```bash
# Check syntax
ansible-playbook playbooks/cluster-init.yml --syntax-check

# Dry run (limited functionality)
ansible-playbook playbooks/cluster-init.yml --check --diff

# Initialize cluster
ansible-playbook playbooks/cluster-init.yml --limit matrix_cluster

# Verify cluster status
ansible -i inventory/proxmox.yml foxtrot -m shell -a "pvecm status"
ansible -i inventory/proxmox.yml foxtrot -m shell -a "pvecm nodes"
```

### Add mise Task

```toml
# .mise.toml
[tasks."cluster:init"]
description = "Initialize Proxmox cluster"
run = """
cd ansible
uv run ansible-playbook playbooks/cluster-init.yml
"""

[tasks."cluster:status"]
description = "Show cluster status"
run = """
ansible -i ansible/inventory/proxmox.yml foxtrot -m shell -a "pvecm status"
"""
```

## Troubleshooting

### Node Won't Join Cluster

**Symptoms:**

- `pvecm add` fails with timeout or connection error

**Solutions:**

1. Verify SSH connectivity: `ssh root@first-node hostname`
2. Check /etc/hosts: `getent hosts first-node`
3. Verify corosync network: `ping -c 3 192.168.8.5`
4. Check firewall: `iptables -L | grep 5404`

### Cluster Shows No Quorum

**Symptoms:**

- `pvecm status` shows `Quorate: No`

**Solutions:**

1. Check node count: Must have majority (2 of 3, 3 of 5, etc.)
2. Verify corosync: `systemctl status corosync`
3. Check corosync ring: `corosync-cfgtool -s`
4. Review logs: `journalctl -u corosync -n 50`

### Configuration Sync Issues

**Symptoms:**

- Changes on one node don't appear on others

**Solutions:**

1. Verify pmxcfs: `systemctl status pve-cluster`
2. Check filesystem: `pvecm status | grep -i cluster`
3. Restart cluster filesystem: `systemctl restart pve-cluster`

## Related Workflows

- [CEPH Deployment](ceph-deployment.md) - Deploy CEPH after cluster formation
- [Network Configuration](../reference/networking.md) - Configure cluster networking
- [Cluster Maintenance](cluster-maintenance.md) - Add/remove nodes, upgrades

## References

- ProxSpray analysis: `docs/proxspray-analysis.md` (lines 1318-1428)
- Proxmox VE Cluster Manager documentation
- Corosync configuration guide
- [Ansible cluster automation pattern](../../ansible-best-practices/patterns/cluster-automation.md)
