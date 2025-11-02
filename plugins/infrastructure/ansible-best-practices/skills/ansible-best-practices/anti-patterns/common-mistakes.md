# Common Ansible Anti-Patterns and Mistakes

## Overview

This guide catalogs common mistakes found in Ansible playbooks and provides corrected examples based on Virgo-Core
repository best practices.

## 1. Not Using `set -euo pipefail` in Shell Scripts

### ❌ Wrong

```yaml
- name: Run multi-line shell script
  ansible.builtin.shell: |
    command1
    command2 | grep something
    command3
```

**Problems:**

- Pipe failures ignored (grep returns no matches = rc 1, but shell continues)
- Undefined variables silently treated as empty strings
- First command failure doesn't stop execution

### ✅ Correct

```yaml
- name: Run multi-line shell script
  ansible.builtin.shell: |
    set -euo pipefail
    command1
    command2 | grep something
    command3
  args:
    executable: /bin/bash
```

**Benefits:**

- `-e`: Exit on first error
- `-u`: Treat undefined variables as errors
- `-o pipefail`: Pipe fails if any command in pipe fails
- `executable: /bin/bash`: Ensures bash (not sh) interprets the script

## 2. Using Shell When Command Suffices

### ❌ Wrong

```yaml
- name: List files
  ansible.builtin.shell: ls -la /tmp
```

**Problems:**

- Unnecessary shell overhead
- Shell injection risk if variables used
- Less portable

### ✅ Correct

```yaml
- name: List files
  ansible.builtin.command: ls -la /tmp
  changed_when: false
```

**Use `shell` ONLY when you need:**

- Pipes: `cat file | grep pattern`
- Redirects: `command > output.txt`
- Environment expansion: `echo $HOME`
- Shell built-ins: `source`, `cd`, etc.

## 3. Missing `changed_when` on Command/Shell

### ❌ Wrong

```yaml
- name: Check if VM exists
  ansible.builtin.command: qm status 101
```

**Problem:** Reports "changed" even though it's a read-only check

### ✅ Correct

```yaml
- name: Check if VM exists
  ansible.builtin.command: qm status 101
  register: vm_status
  changed_when: false
  failed_when: false
```

## 4. Missing `no_log` on Sensitive Tasks

### ❌ Wrong

```yaml
- name: Create user with password
  ansible.builtin.user:
    name: myuser
    password: "{{ user_password }}"
  # Password will appear in logs!
```

**Problem:** Sensitive data appears in Ansible logs

### ✅ Correct

```yaml
- name: Create user with password
  ansible.builtin.user:
    name: myuser
    password: "{{ user_password }}"
  no_log: true
```

**Always use `no_log: true` with:**

- Passwords
- API tokens
- SSH keys
- Certificates
- Any PII or sensitive data

## 5. Using Short Module Names

### ❌ Wrong

```yaml
- name: Copy file
  copy:
    src: file.txt
    dest: /tmp/file.txt

- name: Install package
  apt:
    name: nginx
    state: present
```

**Problem:** Short names are deprecated and will be removed

### ✅ Correct

```yaml
- name: Copy file
  ansible.builtin.copy:
    src: file.txt
    dest: /tmp/file.txt

- name: Install package
  ansible.builtin.apt:
    name: nginx
    state: present
```

**Use Fully Qualified Collection Names (FQCN):**

- `ansible.builtin.copy` not `copy`
- `ansible.builtin.command` not `command`
- `community.proxmox.proxmox_kvm` not `proxmox_kvm`

## 6. Hard-Coding Secrets

### ❌ Wrong

```yaml
- name: Configure database
  ansible.builtin.template:
    src: db-config.j2
    dest: /etc/app/db.yml
  vars:
    db_password: "MyPassword123"  # NEVER DO THIS!
```

**Problems:**

- Secrets in version control
- No audit trail
- Difficult to rotate
- Security violation

### ✅ Correct

```yaml
- name: Retrieve database password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'

- name: Configure database
  ansible.builtin.template:
    src: db-config.j2
    dest: /etc/app/db.yml
  vars:
    db_password: "{{ db_password }}"
  no_log: true
```

## 7. Not Handling "Already Exists" Gracefully

### ❌ Wrong

```yaml
- name: Create API token
  ansible.builtin.command: pveum user token add terraform@pam terraform-token
  # Fails if token already exists
```

**Problem:** Playbook not idempotent - fails on second run

### ✅ Correct

```yaml
- name: Create API token
  ansible.builtin.command: pveum user token add terraform@pam terraform-token
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
```

**Pattern from repository:** Handle expected errors gracefully

## 8. Missing Task Names

### ❌ Wrong

```yaml
- ansible.builtin.apt:
    name: nginx
    state: present

- ansible.builtin.systemd:
    name: nginx
    state: started
```

**Problem:** Hard to understand playbook output

### ✅ Correct

```yaml
- name: Install Nginx web server
  ansible.builtin.apt:
    name: nginx
    state: present

- name: Start Nginx service
  ansible.builtin.systemd:
    name: nginx
    state: started
    enabled: true
```

**ansible-lint will flag this:** `[name[missing]]`

## 9. Using `when` Instead of `failed_when`

### ❌ Wrong

```yaml
- name: Run command
  ansible.builtin.command: some-command
  register: result
  ignore_errors: true

- name: Fail if bad
  ansible.builtin.fail:
    msg: "Command failed"
  when: result.rc != 0 and 'acceptable error' not in result.stderr
```

**Problem:** Two tasks instead of one, less clear

### ✅ Correct

```yaml
- name: Run command
  ansible.builtin.command: some-command
  register: result
  failed_when:
    - result.rc != 0
    - "'acceptable error' not in result.stderr"
```

## 10. Ignoring Return Codes

### ❌ Wrong

```yaml
- name: Run deployment script
  ansible.builtin.command: /usr/local/bin/deploy.sh
  # No error checking at all
```

**Problem:** Failures go unnoticed

### ✅ Correct

```yaml
- name: Run deployment script
  ansible.builtin.command: /usr/local/bin/deploy.sh
  register: deploy_result

- name: Verify deployment succeeded
  ansible.builtin.assert:
    that:
      - deploy_result.rc == 0
      - "'SUCCESS' in deploy_result.stdout"
    fail_msg: "Deployment failed: {{ deploy_result.stderr }}"
```

## 11. Not Using Handlers for Service Restarts

### ❌ Wrong

```yaml
- name: Update Nginx config
  ansible.builtin.copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf

- name: Restart Nginx
  ansible.builtin.systemd:
    name: nginx
    state: restarted
  # Always restarts, even if config didn't change
```

**Problem:** Unnecessary service restarts

### ✅ Correct

```yaml
- name: Update Nginx config
  ansible.builtin.copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  notify: Restart Nginx

handlers:
  - name: Restart Nginx
    ansible.builtin.systemd:
      name: nginx
      state: restarted
```

**Benefits:**

- Only restarts if config changes
- Multiple tasks can trigger same handler
- Handler runs once at end

## 12. Using `with_items` Instead of `loop`

### ❌ Wrong (Deprecated)

```yaml
- name: Install packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  with_items:
    - nginx
    - docker.io
    - python3-pip
```

**Problem:** `with_items` is deprecated

### ✅ Correct

```yaml
- name: Install packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - docker.io
    - python3-pip
```

**Even better (single task):**

```yaml
- name: Install packages
  ansible.builtin.apt:
    name:
      - nginx
      - docker.io
      - python3-pip
    state: present
```

## 13. Not Validating Variables

### ❌ Wrong

```yaml
- name: Create VM
  community.proxmox.proxmox_kvm:
    vmid: "{{ vm_id }}"
    name: "{{ vm_name }}"
    # ... config ...
  # What if vm_id or vm_name is undefined?
```

**Problem:** Cryptic errors if variables missing

### ✅ Correct

```yaml
- name: Validate VM variables
  ansible.builtin.assert:
    that:
      - vm_id is defined
      - vm_id is number
      - vm_id >= 100
      - vm_name is defined
      - vm_name is match('^[a-z0-9-]+$')
    fail_msg: |
      Invalid VM configuration:
      vm_id: {{ vm_id | default('UNDEFINED') }}
      vm_name: {{ vm_name | default('UNDEFINED') }}

- name: Create VM
  community.proxmox.proxmox_kvm:
    vmid: "{{ vm_id }}"
    name: "{{ vm_name }}"
    # ... config ...
```

## 14. Mixing Logic and Data

### ❌ Wrong

```yaml
- name: Configure based on hostname
  ansible.builtin.template:
    src: app-config.j2
    dest: /etc/app/config.yml
  vars:
    db_host: "{{ 'prod-db' if inventory_hostname == 'prod-server' else 'dev-db' }}"
    # Logic in vars
```

**Problem:** Hard to maintain, not DRY

### ✅ Correct

**In `group_vars/prod.yml`:**

```yaml
db_host: prod-db
```

**In `group_vars/dev.yml`:**

```yaml
db_host: dev-db
```

**In playbook:**

```yaml
- name: Configure application
  ansible.builtin.template:
    src: app-config.j2
    dest: /etc/app/config.yml
```

## 15. Not Using Tags

### ❌ Wrong

```yaml
# No tags - must run entire playbook every time
- name: Install packages
  ansible.builtin.apt: ...

- name: Configure service
  ansible.builtin.template: ...

- name: Start service
  ansible.builtin.systemd: ...
```

### ✅ Correct

```yaml
- name: Install packages
  ansible.builtin.apt: ...
  tags: [install, packages]

- name: Configure service
  ansible.builtin.template: ...
  tags: [config]

- name: Start service
  ansible.builtin.systemd: ...
  tags: [service, start]
```

**Usage:**

```bash
# Only run config tasks
ansible-playbook playbook.yml --tags config

# Skip service start
ansible-playbook playbook.yml --skip-tags start
```

## 16. Using Bare Variables in Templates

### ❌ Wrong

```jinja
# templates/config.j2
database_host: {{ db_host }}
database_port: {{ db_port }}
```

**Problem:** YAML parsing errors if values contain special characters

### ✅ Correct

```jinja
# templates/config.j2
database_host: "{{ db_host }}"
database_port: {{ db_port }}
```

**Rule:** Always quote strings, don't quote numbers/booleans

## 17. Hardcoding Paths

### ❌ Wrong

```yaml
- name: Copy script
  ansible.builtin.copy:
    src: scripts/deploy.sh
    dest: /opt/myapp/deploy.sh
  # Assumes specific directory structure
```

### ✅ Correct

```yaml
- name: Copy script
  ansible.builtin.copy:
    src: "{{ playbook_dir }}/../scripts/deploy.sh"
    dest: "{{ app_install_dir }}/deploy.sh"
  vars:
    app_install_dir: /opt/myapp
```

## 18. Not Using Blocks for Related Tasks

### ❌ Wrong

```yaml
- name: Task 1
  ansible.builtin.command: task1
  when: deploy_mode == 'production'

- name: Task 2
  ansible.builtin.command: task2
  when: deploy_mode == 'production'

- name: Task 3
  ansible.builtin.command: task3
  when: deploy_mode == 'production'
```

**Problem:** Repetitive conditions

### ✅ Correct

```yaml
- name: Production deployment tasks
  block:
    - name: Task 1
      ansible.builtin.command: task1

    - name: Task 2
      ansible.builtin.command: task2

    - name: Task 3
      ansible.builtin.command: task3

  when: deploy_mode == 'production'
```

## 19. Using `sudo` Instead of `become`

### ❌ Wrong

```yaml
- name: Install package
  ansible.builtin.command: sudo apt install nginx
```

**Problems:**

- Bypasses Ansible's privilege escalation
- No become_user support
- Less portable

### ✅ Correct

```yaml
- name: Install package
  ansible.builtin.apt:
    name: nginx
    state: present
  become: true
```

## 20. Not Testing Playbooks

### ❌ Wrong

```bash
# Write playbook, run directly in production
ansible-playbook production.yml
```

### ✅ Correct

```bash
# 1. Syntax check
ansible-playbook playbook.yml --syntax-check

# 2. Lint
ansible-lint playbook.yml

# 3. Dry run (check mode)
ansible-playbook playbook.yml --check

# 4. Test in development
ansible-playbook playbook.yml -l dev

# 5. Limited rollout in production
ansible-playbook playbook.yml -l prod --limit 1

# 6. Full production deployment
ansible-playbook playbook.yml -l prod
```

## Quick Reference: Ansible-Lint Rules

Common rules flagged by ansible-lint:

| Rule ID | Description | Fix |
|---------|-------------|-----|
| `name[missing]` | Task missing name | Add `name:` field |
| `fqcn[action-core]` | Use FQCN for modules | `ansible.builtin.copy` not `copy` |
| `no-changed-when` | Command without `changed_when` | Add `changed_when:` |
| `risky-shell-pipe` | Shell pipe without `set -o pipefail` | Add `set -euo pipefail` |
| `no-log-password` | Password without `no_log` | Add `no_log: true` |

**Run ansible-lint:**

```bash
cd ansible
ansible-lint playbooks/my-playbook.yml
```

## Summary: Best Practices Checklist

- [ ] Use `set -euo pipefail` in all shell scripts
- [ ] Use `changed_when: false` for read-only commands
- [ ] Add `no_log: true` to sensitive tasks
- [ ] Use FQCN for all modules
- [ ] Handle "already exists" errors gracefully
- [ ] Add descriptive names to all tasks
- [ ] Validate variables with `assert`
- [ ] Use handlers for service restarts
- [ ] Store secrets in Infisical, not playbooks
- [ ] Test with ansible-lint before committing
- [ ] Use blocks to group related tasks
- [ ] Add tags for selective execution
- [ ] Verify critical operations after execution

## Further Reading

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible-Lint Rules](https://ansible-lint.readthedocs.io/rules/)
