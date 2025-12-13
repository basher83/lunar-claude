---
name: ansible-role-design
description: >
  This skill should be used when creating Ansible roles, designing role directory
  structure, organizing role variables in defaults vs vars, writing role handlers,
  or structuring role tasks. Based on analysis of 7 production geerlingguy roles.
---

# Ansible Role Design

Production-grade role structure patterns derived from analysis of 7 geerlingguy roles.

## Standard Directory Structure

Every Ansible role follows this organizational pattern:

```text
role-name/
├── defaults/
│   └── main.yml          # User-configurable defaults (lowest precedence)
├── vars/
│   ├── Debian.yml        # OS-specific internal values
│   └── RedHat.yml
├── tasks/
│   ├── main.yml          # Task router
│   ├── install.yml       # Feature-specific tasks
│   └── configure.yml
├── handlers/
│   └── main.yml          # Event-triggered tasks
├── templates/
│   └── config.conf.j2    # Jinja2 templates
├── files/
│   └── static-file.txt   # Static files
├── meta/
│   └── main.yml          # Role metadata, dependencies
└── README.md             # Documentation
```

### Directory Purposes

| Directory | Purpose | Precedence |
|-----------|---------|------------|
| `defaults/` | User-overridable values | Lowest |
| `vars/` | Internal/OS-specific values | High |
| `tasks/` | Ansible tasks | N/A |
| `handlers/` | Service restarts, reloads | N/A |
| `templates/` | Jinja2 config files | N/A |
| `files/` | Static files to copy | N/A |
| `meta/` | Galaxy info, dependencies | N/A |

### When to Omit Directories

Only create directories that are actually needed:

- **Omit `templates/`** if using only `lineinfile` or `copy`
- **Omit `handlers/`** if role doesn't manage services
- **Omit `vars/`** if no OS-specific differences
- **Omit `files/`** if no static files to copy

## Task Organization

### Main Task File as Router

Use `tasks/main.yml` as a routing file that includes feature-specific files:

```yaml
# tasks/main.yml
---
- name: Include OS-specific variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"

- name: Install packages
  ansible.builtin.include_tasks: install.yml

- name: Configure service
  ansible.builtin.include_tasks: configure.yml

- name: Setup users
  ansible.builtin.include_tasks: users.yml
  when: role_users | length > 0
```

### When to Split Tasks

| Scenario | Approach |
|----------|----------|
| < 30 lines | Keep in main.yml |
| 30-100 lines | Consider splitting |
| > 100 lines | Definitely split |
| Optional features | Separate file with `when:` |
| OS-specific logic | Separate files per OS |

### Task File Naming

Use descriptive, feature-based names:

```text
tasks/
├── main.yml              # Router only
├── install.yml           # Package installation
├── configure.yml         # Configuration tasks
├── users.yml             # User management
├── install-Debian.yml    # Debian-specific install
└── install-RedHat.yml    # RedHat-specific install
```

## Variable Organization

### defaults/ vs vars/

| Location | Purpose | User Override? |
|----------|---------|----------------|
| `defaults/main.yml` | User configuration | Yes (easily) |
| `vars/main.yml` | Internal constants | Possible but discouraged |
| `vars/Debian.yml` | OS-specific values | No (internal) |

### defaults/main.yml Example

```yaml
# defaults/main.yml
---
# User-configurable options
docker_edition: "ce"
docker_service_state: started
docker_service_enabled: true
docker_users: []

# Feature toggles
docker_install_compose: true
docker_compose_version: "2.24.0"
```

### vars/Debian.yml Example

```yaml
# vars/Debian.yml
---
# OS-specific internal values (not for user override)
docker_package_name: docker-ce
docker_service_name: docker
docker_config_path: /etc/docker/daemon.json
```

### Loading OS-Specific Variables

Simple pattern:

```yaml
- name: Include OS-specific variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"
```

Advanced pattern with fallback:

```yaml
- name: Load OS-specific vars
  ansible.builtin.include_vars: "{{ lookup('first_found', params) }}"
  vars:
    params:
      files:
        - "{{ ansible_distribution }}.yml"
        - "{{ ansible_os_family }}.yml"
        - main.yml
      paths:
        - vars
```

## Variable Naming Convention

Prefix variables with role name:

```yaml
# Pattern: {role_name}_{feature}_{attribute}

# Examples
docker_edition: "ce"
docker_service_state: started
docker_compose_version: "2.24.0"
docker_users: []

# Grouped by feature
security_ssh_port: 22
security_ssh_password_auth: "no"
security_fail2ban_enabled: true
```

### Benefits

- Prevents conflicts with other roles
- Clear ownership of variables
- Easy to grep across codebase
- Self-documenting

## Handler Patterns

### Simple Handler Definitions

```yaml
# handlers/main.yml
---
- name: restart docker
  ansible.builtin.systemd:
    name: docker
    state: restarted

- name: reload nginx
  ansible.builtin.systemd:
    name: nginx
    state: reloaded
```

### Handler Naming

Use lowercase with action + service pattern:

```yaml
- name: restart ssh      # Not "Restart SSH Service"
- name: reload nginx     # Not "Reload Nginx Config"
- name: reload systemd   # For daemon-reload
```

### Throttled Handlers

For cluster operations, restart one node at a time:

```yaml
- name: restart pve-cluster
  ansible.builtin.systemd:
    name: pve-cluster
    state: restarted
  throttle: 1
```

## Template Organization

### When to Use Templates

Use `templates/` when:

- Configuration has conditional content
- Need variable substitution
- Complex multi-line configuration
- Users may need to extend/override

Use `lineinfile` when:

- Simple single-line changes
- Modifying existing system files

### Template Variables

Expose template paths as variables for user override:

```yaml
# defaults/main.yml
nginx_conf_template: nginx.conf.j2
nginx_vhost_template: vhost.j2
```

```yaml
# tasks/configure.yml
- name: Deploy nginx config
  ansible.builtin.template:
    src: "{{ nginx_conf_template }}"
    dest: /etc/nginx/nginx.conf
  notify: reload nginx
```

## Meta Configuration

### meta/main.yml Structure

```yaml
# meta/main.yml
---
galaxy_info:
  author: your_name
  description: Role description
  license: MIT
  min_ansible_version: "2.12"
  platforms:
    - name: Debian
      versions:
        - bullseye
        - bookworm
    - name: Ubuntu
      versions:
        - focal
        - jammy

dependencies:
  - role: common
  - role: geerlingguy.docker
    when: install_docker | default(false)
```

## Role Complexity Scaling

Based on geerlingguy role analysis:

| Role Complexity | Directories | Task Files | Examples |
|-----------------|-------------|------------|----------|
| Minimal | 3-4 | 1 (main.yml) | pip, git |
| Standard | 5-6 | 2-4 | security, docker |
| Complex | 7+ | 5-8 | postgresql, nginx |

### Minimal Role

```text
pip/
├── defaults/main.yml
├── tasks/main.yml
├── meta/main.yml
└── README.md
```

### Standard Role

```text
docker/
├── defaults/main.yml
├── vars/{Debian,RedHat}.yml
├── tasks/{main,install,configure}.yml
├── handlers/main.yml
├── meta/main.yml
└── README.md
```

### Complex Role

```text
postgresql/
├── defaults/main.yml
├── vars/{Debian,RedHat,Archlinux}.yml
├── tasks/{main,install,configure,users,databases}.yml
├── handlers/main.yml
├── templates/{postgresql.conf,pg_hba.conf}.j2
├── meta/main.yml
└── README.md
```

## Task Naming Convention

Start task names with action verbs:

```yaml
# GOOD
- name: Ensure Docker is installed
- name: Configure SSH security settings
- name: Add user to docker group

# BAD
- name: Docker installation
- name: SSH settings
- name: User docker group
```

## File Validation

Validate critical configuration files:

```yaml
- name: Update SSH configuration
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^PermitRootLogin"
    line: "PermitRootLogin no"
    validate: 'sshd -T -f %s'
  notify: restart ssh

- name: Update sudoers
  ansible.builtin.lineinfile:
    path: /etc/sudoers
    line: "{{ user }} ALL=(ALL) NOPASSWD: ALL"
    validate: 'visudo -cf %s'
```

## Documentation

Every role needs a README.md with:

1. **Description** - What the role does
2. **Requirements** - Prerequisites
3. **Role Variables** - All variables with defaults
4. **Dependencies** - Other roles needed
5. **Example Playbook** - How to use it

## Additional Resources

For detailed role design patterns and techniques, consult:

- **`references/role-structure-standards.md`** - Production role structure patterns from geerlingguy analysis
- **`references/handler-best-practices.md`** - Handler design, notification patterns, flush strategies
- **`references/meta-dependencies.md`** - Role dependencies, Galaxy metadata, platform support
- **`references/variable-management-patterns.md`** - Variable naming, scoping, precedence patterns
- **`references/documentation-templates.md`** - README templates and documentation standards

## Related Skills

- **ansible-playbook-design** - When to use roles vs playbooks
- **ansible-fundamentals** - Module selection and naming
- **ansible-testing** - Role testing with molecule
