---
name: ansible-playbook-design
description: >
  This skill should be used when creating new Ansible playbooks, designing playbook
  structure, implementing state-based playbooks with present/absent patterns, organizing
  plays and tasks, or structuring playbook variables. Covers play organization, variable
  scoping, and state-based design patterns.
---

# Ansible Playbook Design

Patterns for designing well-structured, maintainable Ansible playbooks.

## State-Based Playbook Pattern

Design playbooks to handle both creation and removal via a `state` variable.

### Core Pattern

```yaml
---
- name: Manage admin user account
  hosts: all
  become: true

  vars:
    admin_state: present  # or absent

  tasks:
    - name: Create admin user
      ansible.builtin.user:
        name: "{{ admin_name }}"
        groups: "{{ admin_groups }}"
        state: "{{ admin_state }}"

    - name: Configure SSH key
      ansible.posix.authorized_key:
        user: "{{ admin_name }}"
        key: "{{ admin_ssh_key }}"
        state: "{{ admin_state }}"
      when: admin_state == 'present'
```

### Usage

```bash
# Create user (default)
uv run ansible-playbook playbooks/manage-admin.yml \
  -e "admin_name=alice" \
  -e "admin_ssh_key='ssh-ed25519 AAAA...'"

# Remove user
uv run ansible-playbook playbooks/manage-admin.yml \
  -e "admin_name=alice" \
  -e "admin_state=absent"
```

### Benefits

- Single source of truth
- Consistent interface
- Less code duplication
- Follows community role conventions

## Play Structure

### Recommended Play Sections

Order sections consistently across all playbooks:

```yaml
---
- name: Descriptive play name
  hosts: target_group
  become: true
  gather_facts: true

  vars:
    # Play-level variables
    app_version: "2.0.0"

  vars_files:
    # External variable files
    - vars/secrets.yml

  pre_tasks:
    # Tasks that must run before roles
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

  roles:
    # Role includes
    - role: common
    - role: app_deploy
      vars:
        deploy_version: "{{ app_version }}"

  tasks:
    # Play-specific tasks
    - name: Verify deployment
      ansible.builtin.uri:
        url: http://localhost:8080/health

  post_tasks:
    # Cleanup or finalization
    - name: Send deployment notification
      ansible.builtin.debug:
        msg: "Deployment complete"

  handlers:
    # Event-triggered tasks
    - name: restart app
      ansible.builtin.systemd:
        name: myapp
        state: restarted
```

## Variable Organization

### Variable Precedence (Key Levels)

From lowest to highest precedence:

1. Role defaults (`roles/x/defaults/main.yml`)
2. Inventory group_vars (`group_vars/all.yml`)
3. Inventory host_vars (`host_vars/hostname.yml`)
4. Play vars (`vars:` in playbook)
5. Task vars (`vars:` on task)
6. Extra vars (`-e` on command line) - **highest**

### Organizing Variables

```text
ansible/
├── group_vars/
│   ├── all.yml           # Variables for ALL hosts
│   ├── proxmox.yml       # Proxmox cluster hosts
│   └── docker_hosts.yml  # Docker host group
├── host_vars/
│   ├── node01.yml        # Host-specific overrides
│   └── node02.yml
└── playbooks/
    └── deploy.yml        # Uses vars: for playbook-specific
```

### Variable Naming by Scope

```yaml
# group_vars/all.yml - Global defaults
default_timezone: "UTC"
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

# group_vars/proxmox.yml - Group-specific
proxmox_api_host: "192.168.1.10"
proxmox_cluster_name: "production"

# host_vars/node01.yml - Host-specific overrides
proxmox_node_id: 1
ceph_osd_devices:
  - /dev/sdb
  - /dev/sdc
```

## Task Organization with Includes

### When to Split Tasks

Split playbook tasks into separate files when:

- Tasks exceed 50 lines
- Logical groupings emerge (networking, storage, users)
- Conditional sections can be skipped entirely

### Include Patterns

```yaml
# playbooks/setup-cluster.yml
---
- name: Setup Proxmox cluster
  hosts: proxmox
  become: true

  tasks:
    - name: Configure networking
      ansible.builtin.include_tasks: tasks/networking.yml

    - name: Setup storage
      ansible.builtin.include_tasks: tasks/storage.yml
      when: setup_storage | default(true)

    - name: Initialize cluster
      ansible.builtin.include_tasks: tasks/cluster-init.yml
      when: inventory_hostname == groups['proxmox'][0]
```

### import_tasks vs include_tasks

| Feature | import_tasks | include_tasks |
|---------|--------------|---------------|
| When evaluated | Parse time (static) | Runtime (dynamic) |
| Supports loops | No | Yes |
| Supports conditionals on import | Limited | Full |
| Use case | Ordered execution | Conditional/looped |

```yaml
# Static import - always loaded, order matters
- ansible.builtin.import_tasks: users.yml
- ansible.builtin.import_tasks: permissions.yml

# Dynamic include - conditional, looped
- ansible.builtin.include_tasks: "setup-{{ ansible_os_family }}.yml"
- ansible.builtin.include_tasks: deploy-app.yml
  loop: "{{ applications }}"
```

## Multi-Play Playbooks

Use multiple plays for different host groups or privilege levels:

```yaml
---
# Play 1: Gather facts from all nodes
- name: Gather cluster information
  hosts: proxmox
  gather_facts: true
  tasks:
    - name: Set cluster facts
      ansible.builtin.set_fact:
        cluster_node_count: "{{ groups['proxmox'] | length }}"

# Play 2: Initialize primary node
- name: Initialize cluster on primary
  hosts: proxmox[0]
  become: true
  tasks:
    - name: Create cluster
      ansible.builtin.command: pvecm create {{ cluster_name }}
      when: not cluster_exists

# Play 3: Join secondary nodes
- name: Join cluster on secondary nodes
  hosts: proxmox[1:]
  become: true
  serial: 1  # One node at a time
  tasks:
    - name: Join cluster
      ansible.builtin.command: pvecm add {{ primary_node }}
      when: not node_in_cluster
```

## Handler Best Practices

### Define Handlers at Play Level

```yaml
---
- name: Configure web server
  hosts: webservers
  become: true

  tasks:
    - name: Update nginx config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: reload nginx

    - name: Update SSL certificates
      ansible.builtin.copy:
        src: "{{ item }}"
        dest: /etc/nginx/ssl/
      loop:
        - cert.pem
        - key.pem
      notify: reload nginx

  handlers:
    - name: reload nginx
      ansible.builtin.systemd:
        name: nginx
        state: reloaded
```

### Handler Execution Order

Handlers run:

1. At the end of each play
2. In the order they are defined (not notified)
3. Only once, even if notified multiple times

Force immediate handler execution:

```yaml
- name: Update critical config
  ansible.builtin.template:
    src: config.j2
    dest: /etc/app/config.yml
  notify: restart app

- name: Flush handlers now
  ansible.builtin.meta: flush_handlers

- name: Verify app is running
  ansible.builtin.uri:
    url: http://localhost:8080/health
```

## Playbook Validation

### Pre-flight Checks

Add validation at the start of playbooks:

```yaml
---
- name: Deploy application
  hosts: app_servers
  become: true

  tasks:
    - name: Validate required variables
      ansible.builtin.assert:
        that:
          - app_version is defined
          - app_version | regex_search('^\d+\.\d+\.\d+$')
          - deploy_env in ['staging', 'production']
        fail_msg: "Invalid configuration. Check app_version and deploy_env."

    - name: Check disk space
      ansible.builtin.assert:
        that: ansible_mounts | selectattr('mount', 'equalto', '/') | map(attribute='size_available') | first > 1073741824
        fail_msg: "Insufficient disk space. Need at least 1GB free."
```

## Template Patterns

### Playbook Template Structure

```yaml
---
# playbooks/template-playbook.yml
# Description: [What this playbook does]
# Usage: uv run ansible-playbook playbooks/template-playbook.yml -e "var=value"
# Requirements: [Any prerequisites]

- name: [Descriptive play name]
  hosts: [target_group]
  become: [true/false]
  gather_facts: [true/false]

  vars:
    # Configurable variables with defaults
    resource_state: present

  tasks:
    - name: Validate inputs
      ansible.builtin.assert:
        that:
          - required_var is defined
        fail_msg: "required_var must be defined"

    # Main tasks...

    - name: Verify completion
      ansible.builtin.debug:
        msg: "Playbook completed successfully"
```

## Additional Resources

For detailed playbook patterns and techniques, consult:

- **`references/playbook-role-patterns.md`** - Comprehensive playbook organization patterns, play structure, import strategies

## Related Skills

- **ansible-role-design** - When to use roles vs playbooks
- **ansible-fundamentals** - Core module selection and naming
- **ansible-error-handling** - Block/rescue patterns in playbooks
