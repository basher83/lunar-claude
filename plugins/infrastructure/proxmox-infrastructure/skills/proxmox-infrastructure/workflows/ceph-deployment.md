# CEPH Storage Deployment Workflow

Complete guide to deploying CEPH storage on a Proxmox VE cluster with automated OSD creation, pool
configuration, and health verification.

## Overview

This workflow automates CEPH deployment with:

- CEPH package installation
- Cluster initialization with proper network configuration
- Monitor and manager creation across all nodes
- Automated OSD creation with partition support
- Pool configuration with replication and compression
- Comprehensive health verification

## Prerequisites

Before deploying CEPH:

1. **Cluster must be formed:**
   - Proxmox cluster already initialized and healthy
   - All nodes showing quorum
   - See [Cluster Formation](cluster-formation.md) first

2. **Network requirements:**
   - Dedicated CEPH public network (192.168.5.0/24 for Matrix)
   - Dedicated CEPH private/cluster network (192.168.7.0/24 for Matrix)
   - MTU 9000 (jumbo frames) configured on CEPH networks
   - Bridges configured: vmbr1 (public), vmbr2 (private)

3. **Storage requirements:**
   - Dedicated disks for OSDs (not boot disks)
   - All OSD disks should be the same type (SSD/NVMe)
   - Matrix: 2× 4TB Samsung 990 PRO NVMe per node = 24TB raw

4. **System requirements:**
   - Minimum 3 nodes for production (replication factor 3)
   - At least 4GB RAM per OSD
   - Fast network (10GbE recommended for CEPH networks)

## Phase 1: Install CEPH Packages

### Step 1: Install CEPH

```yaml
# roles/proxmox_ceph/tasks/install.yml
---
- name: Check if CEPH is already installed
  ansible.builtin.stat:
    path: /etc/pve/ceph.conf
  register: ceph_conf_check

- name: Check CEPH packages
  ansible.builtin.command:
    cmd: dpkg -l ceph-common
  register: ceph_package_check
  failed_when: false
  changed_when: false

- name: Install CEPH packages via pveceph
  ansible.builtin.command:
    cmd: "pveceph install --repository {{ ceph_repository }}"
  when: ceph_package_check.rc != 0
  register: ceph_install
  changed_when: "'installed' in ceph_install.stdout | default('')"

- name: Verify CEPH installation
  ansible.builtin.command:
    cmd: ceph --version
  register: ceph_version
  changed_when: false
  failed_when: ceph_version.rc != 0

- name: Display CEPH version
  ansible.builtin.debug:
    msg: "Installed CEPH version: {{ ceph_version.stdout }}"
```

## Phase 2: Initialize CEPH Cluster

### Step 2: Initialize CEPH (First Node Only)

```yaml
# roles/proxmox_ceph/tasks/init.yml
---
- name: Check if CEPH cluster is initialized
  ansible.builtin.command:
    cmd: ceph status
  register: ceph_status_check
  failed_when: false
  changed_when: false

- name: Set CEPH initialization facts
  ansible.builtin.set_fact:
    ceph_initialized: "{{ ceph_status_check.rc == 0 }}"
    is_ceph_first_node: "{{ inventory_hostname == groups[cluster_group | default('matrix_cluster')][0] }}"

- name: Initialize CEPH cluster on first node
  ansible.builtin.command:
    cmd: >
      pveceph init
      --network {{ ceph_network }}
      --cluster-network {{ ceph_cluster_network }}
  when:
    - is_ceph_first_node
    - not ceph_initialized
  register: ceph_init
  changed_when: ceph_init.rc == 0

- name: Wait for CEPH cluster to initialize
  ansible.builtin.pause:
    seconds: 15
  when: ceph_init.changed

- name: Verify CEPH initialization
  ansible.builtin.command:
    cmd: ceph status
  register: ceph_init_verify
  changed_when: false
  when:
    - is_ceph_first_node
  failed_when:
    - ceph_init_verify.rc != 0

- name: Display initial CEPH status
  ansible.builtin.debug:
    var: ceph_init_verify.stdout_lines
  when:
    - is_ceph_first_node
    - ceph_init.changed or ansible_verbosity > 0
```

## Phase 3: Create Monitors and Managers

### Step 3: Create CEPH Monitors

```yaml
# roles/proxmox_ceph/tasks/monitors.yml
---
- name: Check existing CEPH monitors
  ansible.builtin.command:
    cmd: ceph mon dump --format json
  register: mon_dump
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  failed_when: false
  changed_when: false

- name: Parse monitor list
  ansible.builtin.set_fact:
    existing_monitors: "{{ (mon_dump.stdout | from_json).mons | map(attribute='name') | list }}"
  when: mon_dump.rc == 0

- name: Set monitor facts
  ansible.builtin.set_fact:
    has_monitor: "{{ inventory_hostname_short in existing_monitors | default([]) }}"

- name: Create CEPH monitor on first node
  ansible.builtin.command:
    cmd: pveceph mon create
  when:
    - is_ceph_first_node
    - not has_monitor
  register: mon_create_first
  changed_when: mon_create_first.rc == 0

- name: Wait for first monitor to stabilize
  ansible.builtin.pause:
    seconds: 10
  when: mon_create_first.changed

- name: Create CEPH monitors on other nodes
  ansible.builtin.command:
    cmd: pveceph mon create
  when:
    - not is_ceph_first_node
    - not has_monitor
  register: mon_create_others
  changed_when: mon_create_others.rc == 0

- name: Verify monitor quorum
  ansible.builtin.command:
    cmd: ceph quorum_status --format json
  register: quorum_status
  changed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Check monitor quorum size
  ansible.builtin.assert:
    that:
      - (quorum_status.stdout | from_json).quorum | length >= ((groups[cluster_group | default('matrix_cluster')] | length // 2) + 1)
    fail_msg: "Monitor quorum not established"
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
```

### Step 4: Create CEPH Managers

```yaml
# roles/proxmox_ceph/tasks/managers.yml
---
- name: Check existing CEPH managers
  ansible.builtin.command:
    cmd: ceph mgr dump --format json
  register: mgr_dump
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  failed_when: false
  changed_when: false

- name: Parse manager list
  ansible.builtin.set_fact:
    existing_managers: "{{ [(mgr_dump.stdout | from_json).active_name] + ((mgr_dump.stdout | from_json).standbys | map(attribute='name') | list) }}"
  when: mgr_dump.rc == 0

- name: Initialize empty manager list if check failed
  ansible.builtin.set_fact:
    existing_managers: []
  when: mgr_dump.rc != 0

- name: Set manager facts
  ansible.builtin.set_fact:
    has_manager: "{{ inventory_hostname_short in (existing_managers | default([])) }}"

- name: Create CEPH manager
  ansible.builtin.command:
    cmd: pveceph mgr create
  when: not has_manager
  register: mgr_create
  changed_when: mgr_create.rc == 0

- name: Wait for managers to stabilize
  ansible.builtin.pause:
    seconds: 5
  when: mgr_create.changed

- name: Enable CEPH dashboard module
  ansible.builtin.command:
    cmd: ceph mgr module enable dashboard
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  register: dashboard_enable
  changed_when: "'already enabled' not in dashboard_enable.stderr"
  failed_when:
    - dashboard_enable.rc != 0
    - "'already enabled' not in dashboard_enable.stderr"

- name: Enable Prometheus module
  ansible.builtin.command:
    cmd: ceph mgr module enable prometheus
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  register: prometheus_enable
  changed_when: "'already enabled' not in prometheus_enable.stderr"
  failed_when:
    - prometheus_enable.rc != 0
    - "'already enabled' not in prometheus_enable.stderr"
```

## Phase 4: Create OSDs

### Step 5: Prepare and Create OSDs

```yaml
# roles/proxmox_ceph/tasks/osd_create.yml
---
- name: Get list of existing OSDs
  ansible.builtin.command:
    cmd: ceph osd ls
  register: existing_osds
  changed_when: false
  failed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Check OSD devices availability
  ansible.builtin.command:
    cmd: "lsblk -ndo NAME,SIZE,TYPE {{ item.device }}"
  register: device_check
  failed_when: device_check.rc != 0
  changed_when: false
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"

- name: Display device information
  ansible.builtin.debug:
    msg: "Device {{ item.item.device }}: {{ item.stdout }}"
  loop: "{{ device_check.results }}"
  loop_control:
    label: "{{ item.item.device }}"
  when: ansible_verbosity > 0

- name: Wipe existing partitions on OSD devices
  ansible.builtin.command:
    cmd: "wipefs -a {{ item.device }}"
  when:
    - ceph_wipe_disks | default(false)
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"
  register: wipe_result
  changed_when: wipe_result.rc == 0

- name: Create OSDs from whole devices (no partitioning)
  ansible.builtin.command:
    cmd: >
      pveceph osd create {{ item.device }}
      {% if item.db_device is defined and item.db_device %}--db_dev {{ item.db_device }}{% endif %}
      {% if item.wal_device is defined and item.wal_device %}--wal_dev {{ item.wal_device }}{% endif %}
  when:
    - item.partitions | default(1) == 1
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"
  register: osd_create_whole
  changed_when: "'successfully created' in osd_create_whole.stdout | default('')"
  failed_when:
    - osd_create_whole.rc != 0
    - "'already in use' not in osd_create_whole.stderr | default('')"
    - "'ceph-volume' not in osd_create_whole.stderr | default('')"

- name: Create multiple OSDs per device (with partitioning)
  ansible.builtin.command:
    cmd: >
      pveceph osd create {{ item.0.device }}
      --size {{ (item.0.device_size_gb | default(4000) / item.0.partitions) | int }}G
      {% if item.0.db_device is defined and item.0.db_device %}--db_dev {{ item.0.db_device }}{% endif %}
      {% if item.0.wal_device is defined and item.0.wal_device %}--wal_dev {{ item.0.wal_device }}{% endif %}
  when:
    - item.0.partitions > 1
  with_subelements:
    - "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
    - partition_indices
    - skip_missing: true
  loop_control:
    label: "{{ item.0.device }} partition {{ item.1 }}"
  register: osd_create_partition
  changed_when: "'successfully created' in osd_create_partition.stdout | default('')"
  failed_when:
    - osd_create_partition.rc != 0
    - "'already in use' not in osd_create_partition.stderr | default('')"

- name: Wait for OSDs to come up
  ansible.builtin.command:
    cmd: ceph osd tree --format json
  register: osd_tree
  changed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  until: >
    (osd_tree.stdout | from_json).nodes
    | selectattr('type', 'equalto', 'osd')
    | selectattr('status', 'equalto', 'up')
    | list | length >= expected_osd_count | int
  retries: 20
  delay: 10
  vars:
    expected_osd_count: >-
      {{
        ceph_osds.values()
        | map('map', attribute='partitions')
        | map('default', 1)
        | sum
      }}
```

## Phase 5: Create and Configure Pools

### Step 6: Create CEPH Pools

```yaml
# roles/proxmox_ceph/tasks/pools.yml
---
- name: Get existing CEPH pools
  ansible.builtin.command:
    cmd: ceph osd pool ls
  register: existing_pools
  changed_when: false

- name: Create CEPH pools
  ansible.builtin.command:
    cmd: >
      ceph osd pool create {{ item.name }}
      {{ item.pg_num }}
      {{ item.pgp_num | default(item.pg_num) }}
  when: item.name not in existing_pools.stdout_lines
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_create
  changed_when: pool_create.rc == 0

- name: Set pool replication size
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} size {{ item.size }}"
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_size
  changed_when: "'set pool' in pool_size.stdout"

- name: Set pool minimum replication size
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} min_size {{ item.min_size }}"
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_min_size
  changed_when: "'set pool' in pool_min_size.stdout"

- name: Set pool application
  ansible.builtin.command:
    cmd: "ceph osd pool application enable {{ item.name }} {{ item.application }}"
  when: item.application is defined
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_app
  changed_when: "'enabled application' in pool_app.stdout"
  failed_when:
    - pool_app.rc != 0
    - "'already enabled' not in pool_app.stderr"

- name: Enable compression on pools
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} compression_mode aggressive"
  when: item.compression | default(false)
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_compression
  changed_when: "'set pool' in pool_compression.stdout"

- name: Set compression algorithm
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} compression_algorithm {{ item.compression_algorithm | default('zstd') }}"
  when: item.compression | default(false)
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_compression_algo
  changed_when: "'set pool' in pool_compression_algo.stdout"
```

## Phase 6: Verify CEPH Health

### Step 7: Health Verification

```yaml
# roles/proxmox_ceph/tasks/verify.yml
---
- name: Wait for CEPH to stabilize
  ansible.builtin.pause:
    seconds: 30

- name: Check CEPH cluster health
  ansible.builtin.command:
    cmd: ceph health
  register: ceph_health
  changed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Get CEPH status
  ansible.builtin.command:
    cmd: ceph status --format json
  register: ceph_status
  changed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Parse CEPH status
  ansible.builtin.set_fact:
    ceph_status_data: "{{ ceph_status.stdout | from_json }}"

- name: Calculate expected OSD count
  ansible.builtin.set_fact:
    expected_osd_count: >-
      {{
        ceph_osds.values()
        | map('map', attribute='partitions')
        | map('default', 1)
        | sum
      }}
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Verify OSD count
  ansible.builtin.assert:
    that:
      - ceph_status_data.osdmap.num_osds | int == expected_osd_count | int
    fail_msg: "Expected {{ expected_osd_count }} OSDs but found {{ ceph_status_data.osdmap.num_osds }}"
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Verify all OSDs are up
  ansible.builtin.assert:
    that:
      - ceph_status_data.osdmap.num_up_osds == ceph_status_data.osdmap.num_osds
    fail_msg: "Not all OSDs are up: {{ ceph_status_data.osdmap.num_up_osds }}/{{ ceph_status_data.osdmap.num_osds }}"
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Verify all OSDs are in
  ansible.builtin.assert:
    that:
      - ceph_status_data.osdmap.num_in_osds == ceph_status_data.osdmap.num_osds
    fail_msg: "Not all OSDs are in cluster: {{ ceph_status_data.osdmap.num_in_osds }}/{{ ceph_status_data.osdmap.num_osds }}"
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true

- name: Wait for PGs to become active+clean
  ansible.builtin.command:
    cmd: ceph pg stat --format json
  register: pg_stat
  changed_when: false
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
  until: >
    (pg_stat.stdout | from_json).num_pg_by_state
    | selectattr('name', 'equalto', 'active+clean')
    | map(attribute='num')
    | sum == (pg_stat.stdout | from_json).num_pgs
  retries: 60
  delay: 10

- name: Display CEPH cluster summary
  ansible.builtin.debug:
    msg: |
      CEPH Cluster Health: {{ ceph_health.stdout }}
      Total OSDs: {{ ceph_status_data.osdmap.num_osds }}
      OSDs Up: {{ ceph_status_data.osdmap.num_up_osds }}
      OSDs In: {{ ceph_status_data.osdmap.num_in_osds }}
      PGs: {{ ceph_status_data.pgmap.num_pgs }}
      Data: {{ ceph_status_data.pgmap.bytes_used | default(0) | human_readable }}
      Available: {{ ceph_status_data.pgmap.bytes_avail | default(0) | human_readable }}
  delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
  run_once: true
```

## Matrix Cluster Configuration Example

```yaml
# group_vars/matrix_cluster.yml (CEPH section)
---
# CEPH configuration
ceph_enabled: true
ceph_repository: "no-subscription"  # or "enterprise" with subscription
ceph_network: "192.168.5.0/24"          # vmbr1 - Public network
ceph_cluster_network: "192.168.7.0/24"  # vmbr2 - Private network

# OSD configuration (4 OSDs per node = 12 total)
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2  # Create 2 OSDs per 4TB NVMe
      device_size_gb: 4000
      partition_indices: [0, 1]
      db_device: null
      wal_device: null
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      device_size_gb: 4000
      partition_indices: [0, 1]
      db_device: null
      wal_device: null
      crush_device_class: nvme

  golf:
    - device: /dev/nvme1n1
      partitions: 2
      device_size_gb: 4000
      partition_indices: [0, 1]
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      device_size_gb: 4000
      partition_indices: [0, 1]
      crush_device_class: nvme

  hotel:
    - device: /dev/nvme1n1
      partitions: 2
      device_size_gb: 4000
      partition_indices: [0, 1]
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      device_size_gb: 4000
      partition_indices: [0, 1]
      crush_device_class: nvme

# Pool configuration
ceph_pools:
  - name: vm_ssd
    pg_num: 128
    pgp_num: 128
    size: 3           # Replicate across 3 nodes
    min_size: 2       # Minimum 2 replicas required
    application: rbd
    compression: false

  - name: vm_containers
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
    application: rbd
    compression: true
    compression_algorithm: zstd

# Safety flags
ceph_wipe_disks: false  # Set to true for fresh deployment (DESTRUCTIVE!)
```

## Complete Playbook Example

```yaml
# playbooks/ceph-deploy.yml
---
- name: Deploy CEPH Storage on Proxmox Cluster
  hosts: "{{ cluster_group | default('matrix_cluster') }}"
  become: true
  serial: 1  # Deploy one node at a time

  pre_tasks:
    - name: Verify cluster is healthy
      ansible.builtin.command:
        cmd: pvecm status
      register: cluster_check
      changed_when: false
      failed_when: "'Quorate: Yes' not in cluster_check.stdout"

    - name: Verify CEPH networks MTU
      ansible.builtin.command:
        cmd: "ip link show {{ item }}"
      register: mtu_check
      changed_when: false
      failed_when: "'mtu 9000' not in mtu_check.stdout"
      loop:
        - vmbr1  # CEPH public
        - vmbr2  # CEPH private

    - name: Display CEPH configuration
      ansible.builtin.debug:
        msg: |
          Deploying CEPH to cluster: {{ cluster_name }}
          Public network: {{ ceph_network }}
          Cluster network: {{ ceph_cluster_network }}
          Expected OSDs: {{ ceph_osds.values() | map('map', attribute='partitions') | map('default', 1) | sum }}
      run_once: true

  roles:
    - role: proxmox_ceph

  post_tasks:
    - name: Display CEPH OSD tree
      ansible.builtin.command:
        cmd: ceph osd tree
      register: osd_tree_final
      changed_when: false
      delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
      run_once: true

    - name: Show OSD tree
      ansible.builtin.debug:
        var: osd_tree_final.stdout_lines
      run_once: true

    - name: Display pool information
      ansible.builtin.command:
        cmd: ceph osd pool ls detail
      register: pool_info
      changed_when: false
      delegate_to: "{{ groups[cluster_group | default('matrix_cluster')][0] }}"
      run_once: true

    - name: Show pool details
      ansible.builtin.debug:
        var: pool_info.stdout_lines
      run_once: true
```

## Usage

### Deploy CEPH to Matrix Cluster

```bash
# Check syntax
ansible-playbook playbooks/ceph-deploy.yml --syntax-check

# Deploy CEPH
ansible-playbook playbooks/ceph-deploy.yml --limit matrix_cluster

# Verify CEPH status
ansible -i inventory/proxmox.yml foxtrot -m shell -a "ceph status"
ansible -i inventory/proxmox.yml foxtrot -m shell -a "ceph osd tree"
ansible -i inventory/proxmox.yml foxtrot -m shell -a "ceph df"
```

### Add mise Tasks

```toml
# .mise.toml
[tasks."ceph:deploy"]
description = "Deploy CEPH storage on cluster"
run = """
cd ansible
uv run ansible-playbook playbooks/ceph-deploy.yml
"""

[tasks."ceph:status"]
description = "Show CEPH cluster status"
run = """
ansible -i ansible/inventory/proxmox.yml foxtrot -m shell -a "ceph -s"
"""

[tasks."ceph:health"]
description = "Show CEPH health detail"
run = """
ansible -i ansible/inventory/proxmox.yml foxtrot -m shell -a "ceph health detail"
"""
```

## Troubleshooting

### OSDs Won't Create

**Symptoms:**

- `pveceph osd create` fails with "already in use" error

**Solutions:**

1. Check if disk has existing partitions: `lsblk /dev/nvme1n1`
2. Wipe disk: `wipefs -a /dev/nvme1n1` (DESTRUCTIVE!)
3. Set `ceph_wipe_disks: true` in group_vars
4. Check for existing LVM: `pvdisplay`, `lvdisplay`

### PGs Stuck in Creating

**Symptoms:**

- PGs stay in "creating" state for extended period

**Solutions:**

1. Check OSD status: `ceph osd tree`
2. Verify all OSDs are up and in: `ceph osd stat`
3. Check mon/mgr status: `ceph mon stat`, `ceph mgr stat`
4. Review logs: `journalctl -u ceph-osd@*.service -n 100`

### Poor CEPH Performance

**Symptoms:**

- Slow VM disk I/O

**Solutions:**

1. Verify MTU 9000: `ip link show vmbr1 | grep mtu`
2. Test network throughput: `iperf3` between nodes
3. Check OSD utilization: `ceph osd df`
4. Verify SSD/NVMe is being used: `ceph osd tree`
5. Check for rebalancing: `ceph -s` (look for "recovery")

## Related Workflows

- [Cluster Formation](cluster-formation.md) - Form cluster before CEPH
- [Network Configuration](../reference/networking.md) - Configure CEPH networks
- [Storage Management](../reference/storage-management.md) - Manage CEPH pools and OSDs

## References

- ProxSpray analysis: `docs/proxspray-analysis.md` (lines 1431-1562)
- Proxmox VE CEPH documentation
- CEPH deployment best practices
- [Ansible CEPH automation pattern](../../.claude/skills/ansible-best-practices/patterns/ceph-automation.md)
