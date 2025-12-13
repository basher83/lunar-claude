---
name: ansible-fundamentals
description: >
  This skill should be used when writing Ansible playbooks, creating Ansible tasks,
  running ansible-playbook commands, selecting Ansible modules, or working with
  Ansible collections. Provides golden rules, FQCN requirements, module selection
  guidance, and execution patterns using uv run.
---

# Ansible Fundamentals

Core principles and golden rules for writing production-quality Ansible automation.

## Golden Rules

These rules apply to ALL Ansible code in this repository:

1. **Use `uv run` prefix** - Execute all Ansible commands through uv:

   ```bash
   uv run ansible-playbook playbooks/my-playbook.yml
   uv run ansible-lint
   uv run ansible-galaxy collection install -r requirements.yml
   ```

2. **Fully Qualified Collection Names (FQCN)** - Avoid short module names:

   ```yaml
   # CORRECT
   - name: Install package
     ansible.builtin.apt:
       name: nginx
       state: present

   # WRONG - deprecated short names
   - name: Install package
     apt:
       name: nginx
   ```

3. **Control command/shell modules** - Add `changed_when` and `failed_when`:

   ```yaml
   - name: Check if service exists
     ansible.builtin.command: systemctl status myservice
     register: service_check
     changed_when: false
     failed_when: false
   ```

4. **Use `set -euo pipefail`** - In all shell scripts and shell module calls:

   ```yaml
   - name: Run pipeline command
     ansible.builtin.shell: |
       set -euo pipefail
       cat file.txt | grep pattern | wc -l
     args:
       executable: /bin/bash
   ```

5. **Tag sensitive tasks** - Use `no_log: true` for secrets:

   ```yaml
   - name: Set database password
     ansible.builtin.command: set-password {{ db_password }}
     no_log: true
   ```

6. **Idempotency first** - Check before create, verify after.

7. **Descriptive task names** - Start with action verbs (Ensure, Configure, Install, Create).

## Module Selection Guide

### Decision Matrix

| Need | Use | Why |
|------|-----|-----|
| Install packages | `ansible.builtin.apt/yum/dnf` | Native modules handle state |
| Manage files | `ansible.builtin.copy/template/file` | Idempotent by default |
| Edit config lines | `ansible.builtin.lineinfile` | Surgical edits, not full replace |
| Run commands | `ansible.builtin.command` | When no native module exists |
| Need shell features | `ansible.builtin.shell` | Pipes, redirects, globs |
| Manage services | `ansible.builtin.systemd/service` | State management built-in |
| Manage users | `ansible.builtin.user` | Cross-platform, idempotent |

### Prefer Native Modules

Native modules provide:

- Built-in idempotency (no need for `changed_when`)
- Better error handling
- Cross-platform compatibility
- Clear documentation

```yaml
# PREFER native module
- name: Create user
  ansible.builtin.user:
    name: deploy
    groups: docker
    state: present

# AVOID command when module exists
- name: Create user
  ansible.builtin.command: useradd -G docker deploy
  # Requires: changed_when, failed_when, idempotency logic
```

### When Command/Shell is Acceptable

Use `command` or `shell` modules when:

1. No native module exists for the operation
2. Interacting with vendor CLI tools (pvecm, pveceph, kubectl)
3. Running one-off scripts

Add proper controls:

```yaml
- name: Create Proxmox API token
  ansible.builtin.command: >
    pveum user token add {{ username }}@pam {{ token_name }}
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
  no_log: true
```

## Collections in Use

This repository uses these Ansible collections:

| Collection | Purpose | Example Modules |
|------------|---------|-----------------|
| `ansible.builtin` | Core functionality | copy, template, command, user |
| `ansible.posix` | POSIX systems | authorized_key, synchronize |
| `community.general` | General utilities | interfaces_file, ini_file |
| `community.proxmox` | Proxmox VE | proxmox_vm, proxmox_kvm |
| `infisical.vault` | Secrets management | read_secrets |
| `community.docker` | Docker management | docker_container, docker_image |

### Installing Collections

```bash
# Install from requirements
cd ansible && uv run ansible-galaxy collection install -r requirements.yml

# Install specific collection
uv run ansible-galaxy collection install community.proxmox
```

## Common Execution Patterns

### Running Playbooks

```bash
# Basic execution
uv run ansible-playbook playbooks/my-playbook.yml

# With extra variables
uv run ansible-playbook playbooks/create-vm.yml \
  -e "vm_name=docker-01" \
  -e "vm_memory=4096"

# Limit to specific hosts
uv run ansible-playbook playbooks/update.yml --limit proxmox

# Check mode (dry run)
uv run ansible-playbook playbooks/deploy.yml --check --diff

# With tags
uv run ansible-playbook playbooks/setup.yml --tags "network,storage"
```

### Linting

```bash
# Run ansible-lint
mise run ansible-lint

# Or directly
uv run ansible-lint ansible/playbooks/
```

## Task Naming Conventions

Use descriptive names with action verbs:

| Verb | Use When |
|------|----------|
| Ensure | Verifying state exists |
| Configure | Modifying settings |
| Install | Adding packages |
| Create | Making new resources |
| Remove | Deleting resources |
| Deploy | Releasing applications |
| Update | Modifying existing resources |

Examples:

```yaml
- name: Ensure Docker is installed
- name: Configure SSH security settings
- name: Create admin user account
- name: Deploy application configuration
```

## Variable Naming

Use snake_case with descriptive names:

```yaml
# GOOD - clear, descriptive
proxmox_api_user: terraform@pam
docker_compose_version: "2.24.0"
vm_memory_mb: 4096

# BAD - vague, abbreviated
pve_usr: terraform@pam
dc_ver: "2.24.0"
mem: 4096
```

## Quick Reference Commands

```bash
# Lint all Ansible files
mise run ansible-lint

# Run playbook with secrets from Infisical
cd ansible && uv run ansible-playbook playbooks/my-playbook.yml

# Check syntax
uv run ansible-playbook --syntax-check playbooks/my-playbook.yml

# List hosts in inventory
uv run ansible-inventory --list

# Test connection
uv run ansible all -m ping
```

## Common Anti-Patterns

### Missing FQCN

```yaml
# BAD
- name: Copy file
  copy:
    src: file.txt
    dest: /tmp/

# GOOD
- name: Copy file
  ansible.builtin.copy:
    src: file.txt
    dest: /tmp/
```

### Uncontrolled Commands

```yaml
# BAD - always shows changed, no error handling
- name: Check status
  ansible.builtin.command: systemctl status app

# GOOD
- name: Check status
  ansible.builtin.command: systemctl status app
  register: status_check
  changed_when: false
  failed_when: false
```

### Using shell When command Suffices

```yaml
# BAD - shell not needed
- name: List files
  ansible.builtin.shell: ls -la /tmp

# GOOD - command is sufficient
- name: List files
  ansible.builtin.command: ls -la /tmp
  changed_when: false
```

### Missing no_log on Secrets

```yaml
# BAD - password in logs
- name: Set password
  ansible.builtin.command: set-password {{ password }}

# GOOD
- name: Set password
  ansible.builtin.command: set-password {{ password }}
  no_log: true
```

## Related Skills

- **ansible-idempotency** - Detailed changed_when/failed_when patterns
- **ansible-secrets** - Infisical integration and security
- **ansible-proxmox** - Proxmox-specific module selection
- **ansible-error-handling** - Block/rescue, retry patterns
