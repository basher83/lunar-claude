---
name: ansible-best-practices
description: >
  Ansible playbook and role patterns using ansible.builtin modules, community.general,
  community.proxmox, ansible.posix collections, molecule testing, ansible-lint validation,
  and Infisical secrets management. Covers idempotency patterns (changed_when, failed_when,
  register), YAML playbook structure, Jinja2 templating, handler patterns, and variable
  precedence rules. This skill should be used when writing Ansible playbooks, developing
  Ansible roles, testing with molecule/ansible-lint, managing secrets with Infisical,
  implementing idempotent task patterns with changed_when/failed_when directives, or
  configuring Proxmox/network automation.
---

# Ansible Playbook Best Practices

Expert guidance for writing maintainable, idempotent, and testable Ansible playbooks based on
real-world patterns from this repository.

## Quick Reference

### Pattern Decision Guide

| Need | Use Pattern | Details |
|------|-------------|---------|
| **Use secrets?** | Infisical Secret Management | [patterns/secrets-management.md](patterns/secrets-management.md) |
| **Resource management?** | State-Based Playbooks | [patterns/playbook-role-patterns.md](patterns/playbook-role-patterns.md) |
| **No native module?** | Hybrid Module Approach | See Hybrid Module section below |
| **Task failing?** | Proper Error Handling | [patterns/error-handling.md](patterns/error-handling.md) |
| **Repeating blocks?** | Task Organization | [patterns/task-organization.md](patterns/task-organization.md) |
| **Network config?** | Network Automation | [patterns/network-automation.md](patterns/network-automation.md) |
| **Tasks show 'changed'?** | Idempotency Patterns | [reference/idempotency-patterns.md](reference/idempotency-patterns.md) |

### Golden Rules

1. **Use `uv run` prefix** - Always: `uv run ansible-playbook`
2. **Fully qualify modules** - `ansible.builtin.copy` not `copy`
3. **Secrets via Infisical** - Use reusable task pattern
4. **Control `command`/`shell`** - Always use `changed_when`, `failed_when`
5. **Use `set -euo pipefail`** - In all shell scripts
6. **Tag sensitive tasks** - Use `no_log: true`
7. **Idempotency first** - Check before create, verify after

### Common Commands

```bash
# Lint
mise run ansible-lint

# Analyze complexity
./tools/analyze_playbook.py ansible/playbooks/my-playbook.yml

# Check idempotency
./tools/check_idempotency.py ansible/playbooks/my-playbook.yml

# Run with secrets
cd ansible && uv run ansible-playbook playbooks/my-playbook.yml
```

## Core Patterns from This Repository

### 1. Infisical Secret Management

This repository uses **Infisical** for centralized secrets management.

**Quick Pattern:**

```yaml
- name: Retrieve Proxmox credentials
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    fallback_env_var: 'PROXMOX_PASSWORD'  # Optional
```

**Key Features:** Validates authentication, proper `no_log`, fallback to env vars, reusable across playbooks.

See [patterns/secrets-management.md](patterns/secrets-management.md) for complete guide including
authentication methods, security best practices, and CI/CD integration.

### 2. State-Based Playbooks

**Pattern:** Single playbook handles both create and remove via `state` variable.

```yaml
# Create user (default)
uv run ansible-playbook playbooks/create-admin-user.yml \
  -e "admin_name=alice" -e "admin_ssh_key='ssh-ed25519 ...'"

# Remove user (add state=absent)
uv run ansible-playbook playbooks/create-admin-user.yml \
  -e "admin_name=alice" -e "admin_state=absent"
```

**Why:** Follows community role patterns, single source of truth, consistent interface, less duplication.

See [patterns/playbook-role-patterns.md](patterns/playbook-role-patterns.md) for complete implementation details and advanced patterns.

### 3. Hybrid Module Approach

**Pattern:** Use native modules where available, fall back to `command` when needed.

```yaml
# GOOD: Native module
- name: Create Linux system user
  ansible.builtin.user:
    name: "{{ system_username }}"
    state: present

# ACCEPTABLE: Command when no native module exists
- name: Create Proxmox API token
  ansible.builtin.command: >
    pveum user token add {{ system_username }}@{{ proxmox_user_realm }}
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
```

**Key:** `changed_when` and `failed_when` make `command` module idempotent.

### 4. Proper Error Handling

```yaml
- name: Check if resource exists
  ansible.builtin.command: check-resource {{ resource_id }}
  register: resource_check
  changed_when: false  # Read-only operation
  failed_when: false   # Don't fail, check in next task

- name: Fail if resource missing
  ansible.builtin.fail:
    msg: "Resource {{ resource_id }} not found"
  when: resource_check.rc != 0
```

See [patterns/error-handling.md](patterns/error-handling.md) for comprehensive patterns.

### 5. Task Organization

**Reusable Tasks Pattern:**

```yaml
# In playbook
- name: Get database password
  ansible.builtin.include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
```

Extract common patterns to `tasks/` directory, use `include_tasks` with clear variable contracts.

See [patterns/task-organization.md](patterns/task-organization.md) and [patterns/reusable-tasks.md](patterns/reusable-tasks.md).

### 6. Network Automation

**Pattern:** Use `community.general.interfaces_file` for network configuration.

```yaml
- name: Enable VLAN-aware bridging
  community.general.interfaces_file:
    iface: vmbr1
    option: bridge-vlan-aware
    value: "yes"
    backup: true
    state: present
  notify: Reload network interfaces
```

Declarative config, automatic backup, handler pattern for reload.

See [patterns/network-automation.md](patterns/network-automation.md) for advanced patterns including VLAN, bonding, and verification.

### 7. Idempotency Patterns

**Use `changed_when` and `failed_when`:**

```yaml
# Check before create
- name: Check if VM exists
  ansible.builtin.shell: |
    set -o pipefail
    qm list | awk '{print $1}' | grep -q "^{{ template_id }}$"
  args:
    executable: /bin/bash
  register: vm_exists
  changed_when: false  # Checking doesn't change anything
  failed_when: false   # Don't fail if not found

# Conditional create
- name: Create VM
  ansible.builtin.command: qm create {{ template_id }} ...
  when: vm_exists.rc != 0
```

See [reference/idempotency-patterns.md](reference/idempotency-patterns.md) for comprehensive patterns.

## Variable Organization

### Quick Summary

**Precedence:** Extra vars (`-e`) > Role vars > Defaults

**Organization:**

```text
ansible/
├── group_vars/all.yml      # Variables for ALL hosts
├── group_vars/proxmox.yml  # Group-specific
├── host_vars/foxtrot.yml   # Host-specific
└── playbooks/
    └── my-playbook.yml     # Use vars: for playbook-specific
```

**Key principle:** Use `defaults/main.yml` for configurable options, `vars/main.yml` for constants.

See [reference/variable-precedence.md](reference/variable-precedence.md) for complete precedence
rules (22 levels) and
[patterns/variable-management-patterns.md](patterns/variable-management-patterns.md) for
advanced patterns.

## Module Selection

### Prefer ansible.builtin

**Always use fully qualified collection names (FQCN):**

```yaml
# GOOD
- name: Ping hosts
  ansible.builtin.ping:

# BAD (deprecated short names)
- name: Ping hosts
  ping:
```

### Community Collections in Use

- `community.general` - General utilities (interfaces_file, etc.)
- `community.proxmox` - Proxmox VE management
- `infisical.vault` - Secrets management
- `ansible.posix` - POSIX system management
- `community.docker` - Docker management

See [../../ansible/requirements.yml](../../ansible/requirements.yml) and [reference/collections-guide.md](reference/collections-guide.md).

## Testing

### With ansible-lint

```bash
# Run all linters
mise run lint-all

# Just Ansible
mise run ansible-lint
```

**Common Issues:** Missing `name:` on tasks, using `shell` instead of `command`, not using
`changed_when`, deprecated short names, missing `no_log` on sensitive tasks.

### With Molecule

```bash
cd tools/molecule/default
molecule create    # Create test environment
molecule converge  # Run playbook
molecule verify    # Run tests
molecule destroy   # Clean up
```

See [reference/testing-guide.md](reference/testing-guide.md) and [patterns/testing-comprehensive.md](patterns/testing-comprehensive.md) for CI/CD integration.

## Common Anti-Patterns

See [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md) for detailed examples.

### Quick List

**1. Not Using `set -euo pipefail`**

```yaml
# GOOD
- name: Run script
  ansible.builtin.shell: |
    set -euo pipefail
    command1 | command2
  args:
    executable: /bin/bash
```

**2. Missing `no_log` on Secrets**

```yaml
# GOOD
- name: Set password
  ansible.builtin.command: set-password {{ password }}
  no_log: true
```

**3. Using `shell` When `command` Suffices**

Use `shell` ONLY when you need shell features (pipes, redirects, etc.).

```yaml
# GOOD: No shell features needed
- name: List files
  ansible.builtin.command: ls -la
```

See [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md) for complete list and
[anti-patterns/refactoring-guide.md](anti-patterns/refactoring-guide.md) for improvement
strategies.

## Tools Available

### Python Analysis Tools (uv)

```bash
# Complexity metrics
./tools/analyze_playbook.py playbook.yml

# Find non-idempotent patterns
./tools/check_idempotency.py playbook.yml

# Variable organization helper
./tools/extract_variables.py playbook.yml
```

### Linting

```bash
# Run all linters
./tools/lint-all.sh
```

### Testing

```bash
# Molecule test scenarios
./tools/molecule/default/
```

## Progressive Disclosure

Start here, drill down as needed:

### Quick Reference (Read First)

- [Playbook & Role Patterns](patterns/playbook-role-patterns.md) - State-based playbooks, public API variables, validation
- [Secrets Management](patterns/secrets-management.md) - Infisical integration, authentication, security

### Deep Patterns (Read When Needed)

- [Testing Comprehensive](patterns/testing-comprehensive.md) - Molecule, CI/CD, test strategies
- [Role Structure Standards](patterns/role-structure-standards.md) - Directory org, naming conventions
- [Documentation Templates](patterns/documentation-templates.md) - README structure, variable docs
- [Variable Management Patterns](patterns/variable-management-patterns.md) - defaults vs vars, naming
- [Handler Best Practices](patterns/handler-best-practices.md) - Handler usage patterns
- [Meta Dependencies](patterns/meta-dependencies.md) - galaxy_info, dependencies

### Advanced Automation (from ProxSpray Analysis)

- [Cluster Automation](patterns/cluster-automation.md) - Proxmox cluster formation with idempotency
- [Network Automation](patterns/network-automation.md) - Declarative network configuration
- [CEPH Automation](patterns/ceph-automation.md) - Complete CEPH storage deployment

### Core Reference

- [Roles vs Playbooks](reference/roles-vs-playbooks.md) - Organization patterns
- [Variable Precedence](reference/variable-precedence.md) - Complete precedence rules (22 levels)
- [Idempotency Patterns](reference/idempotency-patterns.md) - Advanced idempotency techniques
- [Module Selection](reference/module-selection.md) - Builtin vs community decision guide
- [Testing Guide](reference/testing-guide.md) - Molecule and ansible-lint deep dive
- [Collections Guide](reference/collections-guide.md) - Using and managing collections
- [Production Repos](reference/production-repos.md) - Studied geerlingguy roles index

### Patterns & Anti-Patterns

- [Error Handling](patterns/error-handling.md) - Proper error handling patterns
- [Task Organization](patterns/task-organization.md) - Reusable tasks and includes
- [Common Mistakes](anti-patterns/common-mistakes.md) - What to avoid
- [Refactoring Guide](anti-patterns/refactoring-guide.md) - How to improve existing playbooks

## Related Skills

- **Proxmox Infrastructure** - Playbooks for template creation and network config
- **NetBox + PowerDNS** - Dynamic inventory and secrets management patterns
