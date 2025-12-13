# CEPH Storage Automation Patterns

Best practices for automating CEPH cluster deployment in Proxmox VE environments.

## Pattern: Declarative CEPH OSD Configuration

**Problem**: ProxSpray leaves OSD creation as a manual step, defeating the purpose of automation.

**Solution**: Fully automate OSD creation with declarative configuration that specifies devices and partitioning.

### Configuration Model

```yaml
# group_vars/proxmox_cluster.yml
---
# CEPH network configuration
ceph_enabled: true
ceph_network: "192.168.5.0/24"          # Public network (vmbr1)
ceph_cluster_network: "192.168.7.0/24"  # Private network (vmbr2)

# OSD configuration per node (4 OSDs per node = 12 total)
ceph_osds:
  node01:
    - device: /dev/nvme1n1
      partitions: 2  # Create 2 OSDs per 4TB NVMe
      db_device: null
      wal_device: null
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      db_device: null
      wal_device: null
      crush_device_class: nvme

  node02:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

  node03:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

# Pool configuration
ceph_pools:
  - name: vm_ssd
    pg_num: 128
    pgp_num: 128
    size: 3           # Replicate across 3 nodes
    min_size: 2       # Minimum 2 replicas required
    application: rbd
    crush_rule: replicated_rule
    compression: false

  - name: vm_containers
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
    application: rbd
    crush_rule: replicated_rule
    compression: true
```

## Pattern: Idempotent CEPH Installation

**Problem**: CEPH installation commands fail if already installed.

**Solution**: Check CEPH status before attempting installation.

### Implementation

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

- name: Install CEPH packages
  ansible.builtin.command:
    cmd: "pveceph install --repository no-subscription"
  when:
    - ceph_package_check.rc != 0
  register: ceph_install
  changed_when: "'installed' in ceph_install.stdout"

- name: Verify CEPH installation
  ansible.builtin.command:
    cmd: ceph --version
  register: ceph_version
  changed_when: false
  failed_when: ceph_version.rc != 0
```

## Pattern: CEPH Cluster Initialization

**Problem**: CEPH cluster can only be initialized once, must be idempotent.

**Solution**: Check for existing cluster configuration before initialization.

### Implementation

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
    is_ceph_first_node: "{{ inventory_hostname == groups[cluster_group][0] }}"

- name: Initialize CEPH cluster on first node
  ansible.builtin.command:
    cmd: "pveceph init --network {{ ceph_network }} --cluster-network {{ ceph_cluster_network }}"
  when:
    - is_ceph_first_node | default(false)
    - not ceph_initialized
  register: ceph_init
  changed_when: ceph_init.rc == 0

- name: Wait for CEPH cluster to initialize
  ansible.builtin.pause:
    seconds: 15
  when: ceph_init.changed
```

## Pattern: CEPH Monitor Creation

**Problem**: Monitors must be created in specific order and verified for quorum.

**Solution**: Create monitors with proper ordering and quorum verification.

### Implementation

```yaml
# roles/proxmox_ceph/tasks/monitors.yml
---
- name: Check existing CEPH monitors
  ansible.builtin.command:
    cmd: ceph mon dump
  register: mon_dump
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  failed_when: false
  changed_when: false

- name: Set monitor facts
  ansible.builtin.set_fact:
    has_monitor: "{{ inventory_hostname in mon_dump.stdout }}"
  when: mon_dump.rc == 0

- name: Set local is_ceph_first_node fact
  ansible.builtin.set_fact:
    is_ceph_first_node: "{{ inventory_hostname == groups[cluster_group][0] }}"

- name: Create CEPH monitor on first node
  ansible.builtin.command:
    cmd: pveceph mon create
  when:
    - is_ceph_first_node | default(false)
    - not has_monitor | default(false)
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
    - not (is_ceph_first_node | default(false))
    - not has_monitor | default(false)
  register: mon_create_others
  changed_when: mon_create_others.rc == 0

- name: Verify monitor quorum
  ansible.builtin.command:
    cmd: ceph quorum_status
  register: quorum_status
  changed_when: false
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  vars:
    expected_mons: "{{ ceph_mon_count | default(3) }}"
  failed_when: ((quorum_status.stdout | from_json).quorum | length) < expected_mons
```

## Pattern: CEPH Manager Creation

**Problem**: Managers provide web interface and monitoring; should run on all nodes for HA.

**Solution**: Create managers on all nodes with proper verification.

### Implementation

```yaml
# roles/proxmox_ceph/tasks/managers.yml
---
- name: Check existing CEPH managers
  ansible.builtin.command:
    cmd: ceph mgr dump
  register: mgr_dump
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  failed_when: false
  changed_when: false

- name: Set manager facts
  ansible.builtin.set_fact:
    has_manager: "{{ inventory_hostname in mgr_dump.stdout }}"
  when: mgr_dump.rc == 0

- name: Create CEPH manager
  ansible.builtin.command:
    cmd: pveceph mgr create
  when: not has_manager | default(false)
  register: mgr_create
  changed_when: mgr_create.rc == 0

- name: Enable CEPH dashboard module
  ansible.builtin.command:
    cmd: ceph mgr module enable dashboard --force
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  register: dashboard_enable
  changed_when: "'already enabled' not in dashboard_enable.stderr"
  failed_when:
    - dashboard_enable.rc != 0
    - "'already enabled' not in dashboard_enable.stderr"
```

**CRITICAL:** Always use `--force` flag for module enablement! Without it, you'll encounter:

```text
Error ENOENT: all mgr daemons do not support module 'dashboard', pass --force to force enablement
```

**Why:** Known CEPH race condition during manager initialization (especially Octopus/Pacific+). The manager daemon may not have fully loaded all module capabilities when Ansible tries to enable modules. The `--force` flag bypasses this check.

**References:**

- kolla-ansible fix: [commit 361f61d4](https://opendev.org/openstack/kolla-ansible/commit/361f61d4a9fe91a138c21e0a51f54c5e52d83aaa)
- ceph-ansible issue: [#3100](https://github.com/ceph/ceph-ansible/issues/3100)

**Testing Insight:** This error only appears during actual execution, not in check mode! Always test with real runs.

## Pattern: Automated OSD Creation with Partitioning

**Problem**: Manual OSD creation is error-prone and doesn't support partitioning large drives.

**Solution**: Automate partition creation and OSD deployment.

### Implementation

```yaml
# roles/proxmox_ceph/tasks/osd_create.yml
---
- name: Get list of existing OSDs
  ansible.builtin.command:
    cmd: pveceph osd ls
  register: existing_osds
  changed_when: false
  failed_when: false

- name: Probe existing CEPH volumes
  ansible.builtin.command:
    cmd: ceph-volume lvm list --format json
  register: ceph_volume_probe
  changed_when: false
  failed_when: false

- name: Check OSD devices availability
  ansible.builtin.command:
    cmd: "lsblk -ndo NAME,TYPE {{ item.device }}"
  register: device_check
  failed_when: device_check.rc != 0
  changed_when: false
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"

- name: Wipe existing partitions on OSD devices
  ansible.builtin.command:
    cmd: "wipefs -a {{ item.device }}"
  when:
    - ceph_volume_probe.rc == 0
    - ceph_volume_probe.stdout | from_json | dict2items | selectattr('value.0.devices', 'defined') | map(attribute='value.0.devices') | flatten | select('match', '^' + item.device) | list | length == 0
    - ceph_wipe_disks | default(false)
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"
  register: wipe_result
  changed_when: wipe_result.rc == 0

- name: Build list of partitions to create
  ansible.builtin.set_fact:
    osd_partitions: >-
      {% set result = [] -%}
      {% for osd in ceph_osds[inventory_hostname_short] | default([]) -%}
        {% if (osd.partitions | default(1) | int) > 1 -%}
          {% for part_num in range(1, (osd.partitions | int) + 1) -%}
            {% set _ = result.append({
              'device': osd.device,
              'partition_num': part_num,
              'total_partitions': osd.partitions,
              'db_device': osd.get('db_device'),
              'wal_device': osd.get('wal_device')
            }) -%}
          {% endfor -%}
        {% endif -%}
      {% endfor -%}
      {{ result }}

- name: Create partitions for multiple OSDs per device
  community.general.parted:
    device: "{{ item.device }}"
    number: "{{ item.partition_num }}"
    state: present
    part_start: "{{ ((item.partition_num - 1) * (100 / item.total_partitions)) }}%"
    part_end: "{{ (item.partition_num * (100 / item.total_partitions)) }}%"
    label: gpt
  loop: "{{ osd_partitions }}"
  loop_control:
    label: "{{ item.device }}{{ 'p' if item.device.startswith('/dev/nvme') else '' }}{{ item.partition_num }}"

- name: Create OSDs from whole devices
  ansible.builtin.command:
    cmd: >
      pveceph osd create {{ item.device }}
      {% if item.db_device %}--db_dev {{ item.db_device }}{% endif %}
      {% if item.wal_device %}--wal_dev {{ item.wal_device }}{% endif %}
  when:
    - item.partitions | default(1) == 1
    - ceph_volume_probe.rc == 0
    - ceph_volume_probe.stdout | from_json | dict2items | selectattr('value.0.devices', 'defined') | map(attribute='value.0.devices') | flatten | select('match', '^' + item.device + '$') | list | length == 0
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    label: "{{ item.device }}"
  register: osd_create_whole
  changed_when: "'successfully created' in osd_create_whole.stdout"
  failed_when:
    - osd_create_whole.rc != 0
    - "'already in use' not in osd_create_whole.stderr"

- name: Create OSDs from partitions
  ansible.builtin.command:
    cmd: >
      pveceph osd create {{ item.device }}{{ 'p' if item.device.startswith('/dev/nvme') else '' }}{{ item.partition_num }}
      {% if item.db_device %}--db_dev {{ item.db_device }}{% endif %}
      {% if item.wal_device %}--wal_dev {{ item.wal_device %}{% endif %}
  when:
    - ceph_volume_probe.rc == 0
    - ceph_volume_probe.stdout | from_json | dict2items | selectattr('value.0.devices', 'defined') | map(attribute='value.0.devices') | flatten | select('match', '^' + item.device + ('p' if item.device.startswith('/dev/nvme') else '') + (item.partition_num | string) + '$') | list | length == 0
  loop: "{{ osd_partitions }}"
  loop_control:
    label: "{{ item.device }}{{ 'p' if item.device.startswith('/dev/nvme') else '' }}{{ item.partition_num }}"
  register: osd_create_partition
  changed_when: "'successfully created' in osd_create_partition.stdout"
  failed_when:
    - osd_create_partition.rc != 0
    - "'already in use' not in osd_create_partition.stderr"

- name: Wait for OSDs to come up
  ansible.builtin.command:
    cmd: ceph osd tree
  register: osd_tree
  changed_when: false
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  until: "'up' in osd_tree.stdout"
  retries: 10
  delay: 5
```

## Pattern: CEPH Pool Creation

**Problem**: Pools must be created with proper PG counts, replication, and application tags.

**Solution**: Declarative pool configuration with validation.

### Implementation

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
      replicated
      {{ item.crush_rule | default('replicated_rule') }}
  when: item.name not in existing_pools.stdout_lines
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_create
  changed_when: pool_create.rc == 0

- name: Get current pool replication size
  ansible.builtin.command:
    cmd: "ceph osd pool get {{ item.name }} size -f json"
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_size_current
  changed_when: false

- name: Set pool replication size
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} size {{ item.size }}"
  when: (pool_size_current.results[loop_index].stdout | from_json).size != item.size
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
    index_var: loop_index

- name: Get current pool minimum replication size
  ansible.builtin.command:
    cmd: "ceph osd pool get {{ item.name }} min_size -f json"
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_min_size_current
  changed_when: false

- name: Set pool minimum replication size
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} min_size {{ item.min_size }}"
  when: (pool_min_size_current.results[loop_index].stdout | from_json).min_size != item.min_size
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
    index_var: loop_index

- name: Get current pool applications
  ansible.builtin.command:
    cmd: "ceph osd pool application get {{ item.name }} -f json"
  when: item.application is defined
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_app_current
  changed_when: false
  failed_when: false

- name: Set pool application
  ansible.builtin.command:
    cmd: "ceph osd pool application enable {{ item.name }} {{ item.application }}"
  when:
    - item.application is defined
    - pool_app_current.results[loop_index].rc == 0
    - item.application not in (pool_app_current.results[loop_index].stdout | from_json | default({}))
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
    index_var: loop_index

- name: Get current pool compression mode
  ansible.builtin.command:
    cmd: "ceph osd pool get {{ item.name }} compression_mode -f json"
  when: item.compression | default(false)
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
  register: pool_compression_current
  changed_when: false

- name: Enable compression on pools
  ansible.builtin.command:
    cmd: "ceph osd pool set {{ item.name }} compression_mode aggressive"
  when:
    - item.compression | default(false)
    - (pool_compression_current.results[loop_index].stdout | from_json).compression_mode != 'aggressive'
  loop: "{{ ceph_pools }}"
  loop_control:
    label: "{{ item.name }}"
    index_var: loop_index
```

## Pattern: CEPH Health Verification

**Problem**: CEPH cluster may appear successful but have health issues.

**Solution**: Comprehensive health checks after deployment.

### Implementation

```yaml
# roles/proxmox_ceph/tasks/verify.yml
---
- name: Check CEPH cluster health
  ansible.builtin.command:
    cmd: ceph health
  register: ceph_health
  changed_when: false
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Get CEPH status
  ansible.builtin.command:
    cmd: ceph status
  register: ceph_status
  changed_when: false
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Verify expected OSD count
  ansible.builtin.set_fact:
    expected_osd_count: >-
      {{
        ceph_osds
        | dict2items
        | map(attribute='value')
        | sum(start=[])
        | map('default', {'partitions': 1})
        | map(attribute='partitions')
        | map('int')
        | sum
      }}
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Check OSD count matches expected
  ansible.builtin.assert:
    that:
      - "(ceph_status.stdout | from_json).osdmap.num_osds == (expected_osd_count | int)"
    fail_msg: >-
      Expected {{ expected_osd_count }} OSDs but found
      {{ (ceph_status.stdout | from_json).osdmap.num_osds }}
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Check all OSDs are up
  ansible.builtin.command:
    cmd: ceph osd tree
  register: osd_tree
  changed_when: false
  failed_when: "'down' in osd_tree.stdout"
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true

- name: Verify PG status
  ansible.builtin.command:
    cmd: ceph pg stat
  register: pg_stat
  changed_when: false
  failed_when: "'active+clean' not in pg_stat.stdout"
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
  retries: 30
  delay: 10
  until: "'active+clean' in pg_stat.stdout"

- name: Display CEPH status
  ansible.builtin.debug:
    msg: |
      CEPH Cluster Health: {{ ceph_health.stdout }}
      {{ ceph_status.stdout_lines | join('\n') }}
  delegate_to: "{{ groups[cluster_group][0] }}"
  run_once: true
```

## Anti-Pattern: Manual OSD Creation

**❌ Don't Do This** (from ProxSpray):

```yaml
- name: Create OSD on available disks (manual step required)
  ansible.builtin.debug:
    msg: |
      To create OSDs, run manually:
      pveceph osd create /dev/sda
      pveceph osd create /dev/sdb
```

**Problems**:

- Defeats purpose of automation
- Error-prone manual process
- No consistency across nodes
- Difficult to scale

**✅ Do This Instead**: Use the declarative OSD configuration pattern shown above.

## Complete Role Example

```yaml
# roles/proxmox_ceph/tasks/main.yml
---
- name: Install CEPH packages
  ansible.builtin.include_tasks: install.yml

- name: Initialize CEPH cluster (first node only)
  ansible.builtin.include_tasks: init.yml
  when: inventory_hostname == groups[cluster_group][0]

- name: Create CEPH monitors
  ansible.builtin.include_tasks: monitors.yml

- name: Create CEPH managers
  ansible.builtin.include_tasks: managers.yml

- name: Create OSDs
  ansible.builtin.include_tasks: osd_create.yml
  when: ceph_osds[inventory_hostname_short] is defined

- name: Create CEPH pools
  ansible.builtin.include_tasks: pools.yml
  when: inventory_hostname == groups[cluster_group][0]

- name: Verify CEPH health
  ansible.builtin.include_tasks: verify.yml
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/ceph-deploy.yml

# Check mode (limited - CEPH commands don't support check mode well)
ansible-playbook playbooks/ceph-deploy.yml --check --diff

# Deploy CEPH to cluster
ansible-playbook playbooks/ceph-deploy.yml --limit proxmox_cluster

# Verify CEPH status
ansible -i inventory/proxmox.yml node01 -m shell -a "ceph status"
ansible -i inventory/proxmox.yml node01 -m shell -a "ceph osd tree"
ansible -i inventory/proxmox.yml node01 -m shell -a "ceph health detail"
```

## Production Cluster Example

```yaml
# playbooks/ceph-deploy.yml
---
- name: Deploy CEPH Storage on Proxmox Cluster
  hosts: proxmox_cluster
  become: true
  serial: 1  # Deploy one node at a time

  pre_tasks:
    - name: Verify network MTU
      ansible.builtin.command:
        cmd: "ip link show vmbr1"
      register: mtu_check
      changed_when: false
      failed_when: "'mtu 9000' not in mtu_check.stdout"

  roles:
    - role: proxmox_ceph
      vars:
        cluster_group: proxmox_cluster
        ceph_wipe_disks: false  # Set to true for fresh deployment
```

## Related Patterns

- [Cluster Automation](cluster-automation.md) - Cluster formation prerequisite
- [Network Automation](network-automation.md) - Network configuration for CEPH
- [Error Handling](error-handling.md) - CEPH-specific error handling

## References

- ProxSpray analysis: `docs/proxspray-analysis.md` (lines 333-488)
- Proxmox VE CEPH documentation
- CEPH configuration reference
- OSD deployment best practices
