---
name: ansible-best-practices
description: Ansible playbook refactoring, role development, testing, and best practices. Covers role vs playbook organization, variable precedence, idempotency patterns (changed_when, failed_when), testing with molecule and ansible-lint, secrets management with Infisical, proper use of ansible.builtin vs community modules, and task complexity analysis. Use when refactoring Ansible playbooks, creating roles, improving idempotency, implementing Ansible testing, managing secrets with Infisical, analyzing playbook complexity, or following Ansible best practices.
---

# Ansible Playbook Best Practices

Expert guidance for writing maintainable, idempotent, and testable Ansible playbooks based on real-world patterns from this repository.

## Quick Start

### Common Tasks

**Lint Playbook:**

```bash
mise run ansible-lint
# Or: ./tools/lint-all.sh
```

**Analyze Playbook Complexity:**

```bash
./tools/analyze_playbook.py ansible/playbooks/my-playbook.yml
```

**Check Idempotency:**

```bash
./tools/check_idempotency.py ansible/playbooks/my-playbook.yml
```

**Run With Infisical Secrets:**

```bash
# Secrets loaded from Infisical vault
cd ansible && uv run ansible-playbook playbooks/my-playbook.yml
```

## When to Use This Skill

Activate this skill when:

- Refactoring existing Ansible playbooks
- Creating new roles or playbooks
- Improving idempotency of tasks
- Implementing proper error handling
- Managing secrets with Infisical
- Setting up Ansible testing (molecule, ansible-lint)
- Organizing variables and inventory
- Choosing between `ansible.builtin` and community modules
- Analyzing playbook complexity

## Core Patterns from This Repository

### 1. Infisical Secret Management

This repository uses **Infisical** for secrets management. See the reusable task:

[../../ansible/tasks/infisical-secret-lookup.yml](../../ansible/tasks/infisical-secret-lookup.yml)

**Usage Pattern:**

```yaml
- name: Retrieve Proxmox credentials
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    fallback_env_var: 'PROXMOX_PASSWORD'  # Optional fallback
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/doggos-cluster'
```

**Key Features:**

- Validates authentication (Universal Auth or fallback env)
- Proper `no_log` for security
- Fallback to environment variables
- Reusable across playbooks
- Clear error messages

See [patterns/secrets-management.md](patterns/secrets-management.md) for complete guide.

### 2. State-Based Playbooks (Not Separate Create/Delete)

**Pattern:** Single playbook handles both create and remove via `state` variable.

From [../../ansible/playbooks/create-admin-user.yml](../../ansible/playbooks/create-admin-user.yml) + [../../ansible/roles/system_user/](../../ansible/roles/system_user/):

```yaml
# Create user (default behavior)
uv run ansible-playbook playbooks/create-admin-user.yml \
  -e "admin_name=alice" \
  -e "admin_ssh_key='ssh-ed25519 ...'"

# Remove user (just add state=absent)
uv run ansible-playbook playbooks/create-admin-user.yml \
  -e "admin_name=alice" \
  -e "admin_state=absent"
```

**Why This Works:**

- Follows community role patterns (`geerlingguy.docker`, etc.)
- Single source of truth
- Consistent interface
- Less duplication

**Key Implementation Details:**

```yaml
- name: Manage Administrative User
  roles:
    - role: system_user
      vars:
        system_users:
          - name: "{{ admin_name }}"
            state: "{{ admin_state | default('present') }}"  # Default to create
            # Conditional parameters (only when creating)
            ssh_keys: "{{ [] if admin_state == 'absent' else [admin_ssh_key] }}"
```

See [patterns/playbook-role-patterns.md](patterns/playbook-role-patterns.md) for complete guide.

### 3. Hybrid Module Approach

From [../../ansible/playbooks/proxmox-create-terraform-user.yml](../../ansible/playbooks/proxmox-create-terraform-user.yml):

**Pattern:** Use native modules where available, fall back to `command` when needed.

```yaml
# GOOD: Use native module for user creation
- name: Create Linux system user
  ansible.builtin.user:
    name: "{{ system_username }}"
    shell: "{{ system_user_shell }}"
    comment: "{{ system_user_comment }}"
    state: present

# ACCEPTABLE: Use command when no native module exists
- name: Create Proxmox API token
  ansible.builtin.command: >
    pveum user token add {{ system_username }}@{{ proxmox_user_realm }}
    {{ proxmox_token_name }}
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
```

**Why This Works:**

- `changed_when` prevents false positives
- `failed_when` handles "already exists" gracefully
- Idempotent despite using `command` module

### 4. Proper Error Handling

**Pattern:**

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

**Anti-pattern:**

```yaml
# BAD: Using shell without proper controls
- name: Do something
  ansible.builtin.shell: some-command
  # Missing: changed_when, failed_when, register
```

### 5. Task Organization

**Reusable Tasks:**

- Extract common patterns to `tasks/` directory
- Use `include_tasks` with clear variable contracts
- Document required variables

**Example from repository:**

```yaml
# In playbook
- name: Get database password
  ansible.builtin.include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
```

See [patterns/reusable-tasks.md](patterns/reusable-tasks.md).

### 6. Network Automation with Community Modules

From [../../ansible/playbooks/proxmox-enable-vlan-bridging.yml](../../ansible/playbooks/proxmox-enable-vlan-bridging.yml):

**Pattern:** Use community.general.interfaces_file for network configuration.

```yaml
# GOOD: Use interfaces_file module for network config
- name: Enable VLAN-aware bridging on vmbr1
  community.general.interfaces_file:
    iface: vmbr1
    option: bridge-vlan-aware
    value: "yes"
    backup: true
    state: present
  notify: Reload network interfaces

# Handler for network changes
- name: Reload network interfaces
  ansible.builtin.command: ifreload -a
  changed_when: true
```

**Why This Works:**

- Declarative network configuration
- Automatic backup before changes
- Handler pattern for network reload
- Verification with `bridge vlan show`

See [patterns/network-automation.md](patterns/network-automation.md) for advanced patterns.

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
  when: vm_exists.rc != 0  # Only if doesn't exist
```

**Verify Operations:**

```yaml
- name: Verify template was created
  ansible.builtin.shell: |
    set -o pipefail
    qm list | grep "{{ template_id }}"
  args:
    executable: /bin/bash
  register: template_verify
  changed_when: false
  when: not dry_run
```

## Variable Organization

### Precedence (Highest to Lowest)

1. Extra vars (`-e` on command line)
2. Task vars
3. Block vars
4. Role vars (defined in role/vars/main.yml)
5. Include vars
6. Set_facts / Registered vars
7. Include_params
8. Role default vars (defined in role/defaults/main.yml)
9. Inventory file or script group vars
10. Inventory group_vars/all
11. Playbook group_vars/all
12. Inventory group_vars/*
13. Playbook group_vars/*
14. Inventory file or script host vars
15. Inventory host_vars/*
16. Playbook host_vars/*
17. Host facts / cached set_facts
18. Play vars
19. Play vars_prompt
20. Play vars_files
21. Role vars (defined in role/vars/main.yml)
22. Role defaults (defined in role/defaults/main.yml)

See [reference/variable-precedence.md](reference/variable-precedence.md) for details.

### Organization Strategy

```text
ansible/
├── group_vars/
│   ├── all.yml          # Variables for ALL hosts
│   └── proxmox.yml      # Variables for proxmox group
├── host_vars/
│   ├── foxtrot.yml      # Host-specific variables
│   ├── golf.yml
│   └── hotel.yml
└── playbooks/
    └── my-playbook.yml  # Use vars: for playbook-specific
```

## Module Selection

### Prefer `ansible.builtin`

**Always use fully qualified names:**

```yaml
# GOOD
- name: Ping hosts
  ansible.builtin.ping:

# BAD (deprecated short names)
- name: Ping hosts
  ping:
```

### When to Use Community Modules

**Use community.proxmox for Proxmox management:**

```yaml
- name: Create Proxmox user
  community.proxmox.proxmox_user:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
    userid: "terraform@pam"
    state: present
```

**Collections in use:**

- `community.general` - General utilities
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

**Common Issues to Fix:**

- Missing `name:` on tasks
- Using `shell` instead of `command` unnecessarily
- Not using `changed_when` with `command`/`shell`
- Deprecated module short names
- Missing `no_log` on sensitive tasks

### With Molecule

See [tools/molecule/](tools/molecule/) for test scenarios.

**Basic workflow:**

```bash
cd tools/molecule/default
molecule create    # Create test environment
molecule converge  # Run playbook
molecule verify    # Run tests
molecule destroy   # Clean up
```

See [reference/testing-guide.md](reference/testing-guide.md).

## Common Anti-Patterns

See [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md) for detailed list.

### 1. Not Using set -euo pipefail

**Bad:**

```yaml
- name: Run script
  ansible.builtin.shell: |
    command1
    command2
```

**Good:**

```yaml
- name: Run script
  ansible.builtin.shell: |
    set -euo pipefail
    command1
    command2
  args:
    executable: /bin/bash
```

### 2. Missing no_log on Secrets

**Bad:**

```yaml
- name: Set password
  ansible.builtin.command: set-password {{ password }}
  # Password visible in logs!
```

**Good:**

```yaml
- name: Set password
  ansible.builtin.command: set-password {{ password }}
  no_log: true
```

### 3. Using `shell` When `command` Suffices

**Bad:**

```yaml
- name: List files
  ansible.builtin.shell: ls -la
```

**Good:**

```yaml
- name: List files
  ansible.builtin.command: ls -la
```

Use `shell` ONLY when you need shell features (pipes, redirects, etc.).

## Tools Available

### Python Analysis Tools (uv)

**analyze_playbook.py** - Complexity metrics

```bash
./tools/analyze_playbook.py playbook.yml
# Shows: task count, role usage, variable complexity
```

**check_idempotency.py** - Find non-idempotent patterns

```bash
./tools/check_idempotency.py playbook.yml
# Detects: missing changed_when, shell without controls
```

**extract_variables.py** - Variable organization helper

```bash
./tools/extract_variables.py playbook.yml
# Suggests: where to move variables (defaults, group_vars, etc.)
```

### Linting

**lint-all.sh** - Run all linters

```bash
./tools/lint-all.sh
# Runs: ansible-lint, yamllint, with project config
```

### Testing

**molecule/** - Test scenarios

```bash
./tools/molecule/default/  # Default test scenario
```

## Best Practices Summary

1. **Use `uv run` prefix** - Always: `uv run ansible-playbook`
2. **Fully qualify modules** - `ansible.builtin.copy` not `copy`
3. **Secrets via Infisical** - Use reusable task pattern
4. **Control `command`/`shell`** - Always use `changed_when`, `failed_when`
5. **Use `set -euo pipefail`** - In all shell scripts
6. **Tag sensitive tasks** - Use `no_log: true`
7. **Extract reusable tasks** - Don't repeat yourself
8. **Test with ansible-lint** - Before committing
9. **Document variables** - Clear comments on required vars
10. **Idempotency first** - Check before create, verify after

## Progressive Disclosure

Start here, drill down as needed:

### Quick Reference (Read First)

- [Playbook & Role Patterns](patterns/playbook-role-patterns.md) - State-based playbooks, public API variables, validation patterns
- [Secrets management](patterns/secrets-management.md) - Infisical integration

### Deep Patterns (Read When Needed)

- [testing-comprehensive.md](patterns/testing-comprehensive.md) - Molecule, CI/CD, test strategies ✨ NEW
- [role-structure-standards.md](patterns/role-structure-standards.md) - Directory org, naming conventions ✨ NEW
- [documentation-templates.md](patterns/documentation-templates.md) - README structure, variable docs ✨ NEW
- [variable-management-patterns.md](patterns/variable-management-patterns.md) - defaults vs vars, naming ✨ NEW
- [handler-best-practices.md](patterns/handler-best-practices.md) - Handler usage patterns ✨ NEW
- [meta-dependencies.md](patterns/meta-dependencies.md) - galaxy_info, dependencies ✨ NEW

### Advanced Automation Patterns (from ProxSpray Analysis)

- [Cluster Automation](patterns/cluster-automation.md) - Proxmox cluster formation with idempotency
- [Network Automation](patterns/network-automation.md) - Declarative network configuration
- [CEPH Automation](patterns/ceph-automation.md) - Complete CEPH storage deployment

### Core Reference

- [Roles vs playbooks](reference/roles-vs-playbooks.md) - Organization patterns
- [Variable precedence](reference/variable-precedence.md) - Complete precedence rules
- [Idempotency patterns](reference/idempotency-patterns.md) - Advanced patterns
- [Module selection](reference/module-selection.md) - Builtin vs community
- [Testing guide](reference/testing-guide.md) - Molecule and ansible-lint
- [Collections guide](reference/collections-guide.md) - Using collections
- [production-repos.md](reference/production-repos.md) - Studied geerlingguy roles index ✨ NEW

### Patterns & Anti-Patterns

- [Error handling](patterns/error-handling.md) - Proper error handling
- [Task organization](patterns/task-organization.md) - Reusable tasks
- [Common mistakes](anti-patterns/common-mistakes.md) - What to avoid
- [Refactoring guide](anti-patterns/refactoring-guide.md) - How to improve

## Related Skills

- **Proxmox Infrastructure** - Playbooks for template creation and network config
- **NetBox + PowerDNS** - Dynamic inventory and secrets management patterns
