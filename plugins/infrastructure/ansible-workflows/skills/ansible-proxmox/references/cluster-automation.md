# Cluster Automation Patterns

Best practices for automating Proxmox cluster formation with idempotent,
production-ready Ansible playbooks.

## Pattern: Idempotent Cluster Status Detection

**Problem**: Cluster formation commands (`pvecm create`, `pvecm add`) fail if run
on nodes already in a cluster, making automation brittle.

**Solution**: Always check cluster status before attempting destructive operations.

### Implementation

```yaml
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
    is_cluster_member: "{{ cluster_status.rc == 0 and (cluster_nodes_check.stdout_lines | length > 1 or cluster_name in cluster_status.stdout) }}"
    is_first_node: "{{ inventory_hostname == groups['proxmox'][0] }}"
    in_target_cluster: "{{ cluster_status.rc == 0 and cluster_name in cluster_status.stdout }}"

- name: Create new cluster on first node
  ansible.builtin.command:
    cmd: "pvecm create {{ cluster_name }}"
  when:
    - is_first_node
    - not in_target_cluster
  register: cluster_create
  changed_when: cluster_create.rc == 0

- name: Join cluster on other nodes
  ansible.builtin.command:
    cmd: "pvecm add {{ hostvars[groups['proxmox'][0]].ansible_host }}"
  when:
    - not is_first_node
    - not is_cluster_member
  register: cluster_join
  changed_when: cluster_join.rc == 0
```

### Key Benefits

1. **Safe Re-runs**: Playbook can run multiple times without breaking existing clusters
2. **Error Recovery**: Nodes can rejoin if removed from cluster
3. **Multi-Cluster Support**: Prevents accidentally joining wrong cluster
4. **Clear State**: `changed_when` accurately reflects actual changes

## Pattern: Hostname Resolution Verification

**Problem**: Cluster formation fails if nodes cannot resolve each other's
hostnames, but errors are cryptic.

**Solution**: Verify /etc/hosts configuration and DNS resolution before cluster operations.

### Implementation

```yaml
- name: Ensure cluster nodes in /etc/hosts
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: "^{{ item.ip }}\\s+"
    line: "{{ item.ip }} {{ item.fqdn }} {{ item.short_name }}"
    state: present
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.short_name }}"

- name: Verify hostname resolution
  ansible.builtin.command:
    cmd: "getent hosts {{ item.fqdn }}"
  register: host_lookup
  failed_when: host_lookup.rc != 0
  changed_when: false
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.fqdn }}"

- name: Verify reverse DNS resolution
  ansible.builtin.command:
    cmd: "getent hosts {{ item.ip }}"
  register: reverse_lookup
  failed_when:
    - reverse_lookup.rc != 0
  changed_when: false
  loop: "{{ cluster_nodes }}"
  loop_control:
    label: "{{ item.ip }}"
```

### Configuration Example

```yaml
# group_vars/proxmox_cluster.yml
cluster_name: "production"
cluster_nodes:
  - short_name: node01
    fqdn: node01.example.com
    ip: 192.168.3.5
    corosync_ip: 192.168.8.5
  - short_name: node02
    fqdn: node02.example.com
    ip: 192.168.3.6
    corosync_ip: 192.168.8.6
  - short_name: node03
    fqdn: node03.example.com
    ip: 192.168.3.7
    corosync_ip: 192.168.8.7
```

## Pattern: SSH Key Distribution for Cluster Operations

**Problem**: Some cluster operations require passwordless SSH between nodes.

**Solution**: Automate SSH key generation and distribution.

### Implementation

```yaml
- name: Generate SSH key for root (if not exists)
  ansible.builtin.user:
    name: root
    generate_ssh_key: true
    ssh_key_bits: 4096
    ssh_key_type: rsa
  register: root_ssh_key

- name: Fetch public keys from all nodes
  ansible.builtin.slurp:
    src: /root/.ssh/id_rsa.pub
  register: node_public_keys

- name: Distribute SSH keys to all nodes
  ansible.posix.authorized_key:
    user: root
    state: present
    key: "{{ hostvars[item].node_public_keys.content | b64decode }}"
  loop: "{{ groups['proxmox'] }}"
  when: item != inventory_hostname
```

## Pattern: Service Restart Orchestration

**Problem**: Cluster services must restart in specific order after configuration changes.

**Solution**: Use handlers with explicit dependencies and delays.

### Implementation

```yaml
# tasks/main.yml
- name: Configure corosync
  ansible.builtin.template:
    src: corosync.conf.j2
    dest: /etc/pve/corosync.conf
    validate: corosync-cfgtool -c %s
  notify:
    - reload corosync
    - restart pve-cluster
    - restart pvedaemon
    - restart pveproxy

# handlers/main.yml
- name: reload corosync
  ansible.builtin.systemd:
    name: corosync
    state: reloaded
  listen: reload corosync

- name: restart pve-cluster
  ansible.builtin.systemd:
    name: pve-cluster
    state: restarted
  listen: restart pve-cluster
  throttle: 1  # Restart one node at a time

- name: restart pvedaemon
  ansible.builtin.systemd:
    name: pvedaemon
    state: restarted
  listen: restart pvedaemon

- name: restart pveproxy
  ansible.builtin.systemd:
    name: pveproxy
    state: restarted
  listen: restart pveproxy
```

## Pattern: Quorum and Health Verification

**Problem**: Cluster may appear successful but have quorum issues or split-brain scenarios.

**Solution**: Always verify cluster health after operations.

### Implementation

```yaml
- name: Wait for cluster to stabilize
  ansible.builtin.pause:
    seconds: 10
  when: cluster_create.changed or cluster_join.changed

- name: Verify cluster quorum
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_health
  changed_when: false
  failed_when: "'Quorate: Yes' not in cluster_health.stdout"

- name: Check expected node count
  ansible.builtin.command:
    cmd: pvecm nodes
  register: cluster_nodes_final
  changed_when: false
  failed_when: cluster_nodes_final.stdout_lines | length != groups['proxmox'] | length

- name: Display cluster status
  ansible.builtin.debug:
    var: cluster_health.stdout_lines
  when: cluster_health.changed or ansible_verbosity > 0
```

## Anti-Pattern: Silent Error Suppression

**❌ Don't Do This**:

```yaml
- name: Join cluster on other nodes
  ansible.builtin.shell: |
    timeout 60 pvecm add {{ primary_node }}
  failed_when: false  # Silently ignores ALL errors
```

**Problems**:

- Hides real failures (network issues, authentication problems)
- Makes debugging impossible
- Creates inconsistent cluster state
- Provides false success signals

**✅ Do This Instead**:

```yaml
- name: Join cluster on other nodes
  ansible.builtin.command:
    cmd: "pvecm add {{ primary_node }}"
  register: cluster_join
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
    - "'cannot join cluster' not in cluster_join.stderr"
  changed_when: cluster_join.rc == 0

- name: Handle join failure
  ansible.builtin.fail:
    msg: |
      Failed to join cluster {{ cluster_name }}.
      Error: {{ cluster_join.stderr }}
      Hint: Check network connectivity and ensure first node is reachable.
  when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
```

## Complete Role Example

```yaml
# roles/proxmox_cluster/tasks/main.yml
---
- name: Verify prerequisites
  ansible.builtin.include_tasks: prerequisites.yml

- name: Configure /etc/hosts
  ansible.builtin.include_tasks: hosts_config.yml

- name: Distribute SSH keys
  ansible.builtin.include_tasks: ssh_keys.yml

- name: Initialize cluster (first node only)
  ansible.builtin.include_tasks: cluster_init.yml
  when: inventory_hostname == groups['proxmox'][0]

- name: Join cluster (other nodes)
  ansible.builtin.include_tasks: cluster_join.yml
  when: inventory_hostname != groups['proxmox'][0]

- name: Configure corosync
  ansible.builtin.include_tasks: corosync.yml

- name: Verify cluster health
  ansible.builtin.include_tasks: verify.yml
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/cluster-init.yml

# Check mode (dry run)
ansible-playbook playbooks/cluster-init.yml --check --diff

# Run on specific cluster
ansible-playbook playbooks/cluster-init.yml --limit proxmox_cluster

# Verify idempotency (should show 0 changes on second run)
ansible-playbook playbooks/cluster-init.yml --limit proxmox_cluster
ansible-playbook playbooks/cluster-init.yml --limit proxmox_cluster
```

## Related Patterns

- [Error Handling](error-handling.md) - Comprehensive error handling strategies
- [Network Automation](network-automation.md) - Network interface and bridge configuration
- [CEPH Storage](ceph-automation.md) - CEPH cluster deployment patterns

## References

- ProxSpray analysis: `docs/proxspray-analysis.md` (lines 153-207)
- Proxmox VE Cluster Manager documentation
- Corosync configuration guide
