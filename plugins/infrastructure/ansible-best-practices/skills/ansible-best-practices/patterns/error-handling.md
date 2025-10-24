# Error Handling Patterns

## Overview

Proper error handling in Ansible ensures playbooks are robust, idempotent, and provide clear failure messages. This guide covers patterns from the Virgo-Core repository.

## Core Concepts

### changed_when

Controls when Ansible reports a task as "changed". Critical for idempotency with `command` and `shell` modules.

**Syntax:**

```yaml
changed_when: <boolean expression>
```

### failed_when

Controls when Ansible considers a task as failed. Allows graceful handling of expected errors.

**Syntax:**

```yaml
failed_when: <boolean expression>
```

### register

Captures task output for later inspection and conditional logic.

**Syntax:**

```yaml
register: variable_name
```

## Pattern 1: Idempotent Command Execution

### Problem

`command` and `shell` modules always report "changed" even if nothing changed.

### Solution

Use `changed_when` to detect actual changes:

**Example from repository:**

```yaml
- name: Create Proxmox API token
  ansible.builtin.command: >
    pveum user token add {{ system_username }}@{{ proxmox_user_realm }}
    {{ proxmox_token_name }}
  register: token_result
  changed_when: "'already exists' not in token_result.stderr"
  failed_when:
    - token_result.rc != 0
    - "'already exists' not in token_result.stderr"
  no_log: true
```

**Explanation:**

1. `register: token_result` - Captures command output
2. `changed_when: "'already exists' not in token_result.stderr"` - Only report "changed" if token didn't already exist
3. `failed_when` - Don't fail if token already exists (expected scenario)

## Pattern 2: Check Before Create

### Problem

Creating resources that may already exist causes unnecessary errors.

### Solution

Check for existence first, create conditionally:

**Example:**

```yaml
- name: Check if VM template exists
  ansible.builtin.shell: |
    set -o pipefail
    qm list | awk '{print $1}' | grep -q "^{{ template_id }}$"
  args:
    executable: /bin/bash
  register: template_exists
  changed_when: false  # Checking doesn't change anything
  failed_when: false   # Don't fail if template not found

- name: Create VM template
  ansible.builtin.command: >
    qm create {{ template_id }}
    --name {{ template_name }}
    --memory 2048
    --cores 2
  when: template_exists.rc != 0  # Only create if check failed (doesn't exist)
  register: create_result
```

**Key points:**

- `changed_when: false` - Read-only operation
- `failed_when: false` - Expected that template might not exist
- `when: template_exists.rc != 0` - Conditional creation

## Pattern 3: Verify After Create

### Problem

Resource creation appears to succeed but may have failed silently.

### Solution

Verify resource exists after creation:

**Example:**

```yaml
- name: Create VM
  ansible.builtin.command: >
    qm create {{ vmid }}
    --name {{ vm_name }}
    --memory 4096
  register: create_result

- name: Verify VM was created
  ansible.builtin.shell: |
    set -o pipefail
    qm list | grep "{{ vmid }}"
  args:
    executable: /bin/bash
  register: verify_result
  changed_when: false
  failed_when: verify_result.rc != 0
```

## Pattern 4: Graceful Failure Handling

### Problem

Task failures may be expected in certain scenarios.

### Solution

Use `failed_when` with specific conditions:

**Example:**

```yaml
- name: Try to stop service
  ansible.builtin.systemd:
    name: myservice
    state: stopped
  register: stop_result
  failed_when:
    - stop_result.failed
    - "'not found' not in stop_result.msg"
  # Allow failure if service doesn't exist
```

**Multiple failure conditions:**

```yaml
- name: Run migration
  ansible.builtin.command: /usr/bin/migrate-database
  register: migrate_result
  failed_when:
    - migrate_result.rc != 0
    - "'already applied' not in migrate_result.stdout"
    - "'no changes' not in migrate_result.stdout"
  # Success if: rc=0, OR "already applied", OR "no changes"
```

## Pattern 5: Block with Rescue

### Problem

Need to handle failures and perform cleanup.

### Solution

Use `block`/`rescue`/`always`:

**Example:**

```yaml
- name: Deploy application
  block:
    - name: Stop application
      ansible.builtin.systemd:
        name: myapp
        state: stopped

    - name: Deploy new version
      ansible.builtin.copy:
        src: myapp-v2.0
        dest: /usr/bin/myapp

    - name: Start application
      ansible.builtin.systemd:
        name: myapp
        state: started

  rescue:
    - name: Rollback to previous version
      ansible.builtin.copy:
        src: myapp-backup
        dest: /usr/bin/myapp

    - name: Start application (rollback)
      ansible.builtin.systemd:
        name: myapp
        state: started

    - name: Report failure
      ansible.builtin.fail:
        msg: "Deployment failed, rolled back to previous version"

  always:
    - name: Cleanup temp files
      ansible.builtin.file:
        path: /tmp/deploy-*
        state: absent
```

**Explanation:**

- `block:` - Main tasks
- `rescue:` - Runs if any task in block fails
- `always:` - Runs regardless of success/failure

## Pattern 6: Retry with Until

### Problem

Transient failures need retries before giving up.

### Solution

Use `until`, `retries`, `delay`:

**Example:**

```yaml
- name: Wait for service to be ready
  ansible.builtin.uri:
    url: http://localhost:8080/health
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 30
  delay: 10
  # Retry every 10 seconds, up to 30 times (5 minutes total)
```

**With command:**

```yaml
- name: Wait for VM to get IP address
  ansible.builtin.command: qm agent {{ vmid }} network-get-interfaces
  register: vm_network
  until: vm_network.rc == 0
  retries: 12
  delay: 5
  changed_when: false
```

## Pattern 7: Conditional Failure Messages

### Problem

Generic failure messages don't help with troubleshooting.

### Solution

Use `ansible.builtin.fail` with conditional messages:

**Example:**

```yaml
- name: Check prerequisites
  ansible.builtin.command: which docker
  register: docker_check
  changed_when: false
  failed_when: false

- name: Fail if Docker not installed
  ansible.builtin.fail:
    msg: |
      Docker is not installed on {{ inventory_hostname }}
      Please install Docker before running this playbook.
      Installation: sudo apt install docker.io
  when: docker_check.rc != 0

- name: Check Docker version
  ansible.builtin.command: docker --version
  register: docker_version
  changed_when: false

- name: Validate Docker version
  ansible.builtin.fail:
    msg: |
      Docker version is too old: {{ docker_version.stdout }}
      Minimum required version: 20.10
  when: docker_version.stdout is version('20.10', '<')
```

## Pattern 8: Assert for Validation

### Problem

Need to validate multiple conditions with clear error messages.

### Solution

Use `ansible.builtin.assert`:

**Example from repository:**

```yaml
- name: Validate required variables
  ansible.builtin.assert:
    that:
      - secret_name is defined and secret_name|trim|length > 0
      - secret_var_name is defined and secret_var_name|trim|length > 0
    fail_msg: "secret_name and secret_var_name must be provided and non-empty"
    success_msg: "All required variables present"
    quiet: true
  no_log: true
```

**Multiple assertions:**

```yaml
- name: Validate VM configuration
  ansible.builtin.assert:
    that:
      - vm_memory >= 2048
      - vm_cores >= 2
      - vm_disk_size >= 20
      - vm_name is match('^[a-z0-9-]+$')
    fail_msg: |
      Invalid VM configuration:
      - Memory must be >= 2048 MB (got: {{ vm_memory }})
      - Cores must be >= 2 (got: {{ vm_cores }})
      - Disk must be >= 20 GB (got: {{ vm_disk_size }})
      - Name must be lowercase alphanumeric with hyphens (got: {{ vm_name }})
```

## Pattern 9: Ignore Errors Temporarily

### Problem

Task may fail but playbook should continue.

### Solution

Use `ignore_errors` (sparingly!):

**Example:**

```yaml
- name: Try to remove old backup
  ansible.builtin.file:
    path: /backup/old-backup.tar.gz
    state: absent
  ignore_errors: true  # OK if file doesn't exist
  register: cleanup_result

- name: Report cleanup result
  ansible.builtin.debug:
    msg: "Cleanup {{ 'successful' if not cleanup_result.failed else 'skipped (file not found)' }}"
```

**Better approach with failed_when:**

```yaml
- name: Remove old backup
  ansible.builtin.file:
    path: /backup/old-backup.tar.gz
    state: absent
  register: cleanup_result
  failed_when:
    - cleanup_result.failed
    - "'does not exist' not in cleanup_result.msg"
```

## Pattern 10: Task Delegation

### Problem

Need to run task locally or on a different host.

### Solution

Use `delegate_to`:

**Example:**

```yaml
- name: Check API endpoint from controller
  ansible.builtin.uri:
    url: "https://{{ inventory_hostname }}:8006/api2/json/version"
    validate_certs: false
  delegate_to: localhost
  register: api_check
  failed_when: api_check.status != 200
```

## Complete Example: Robust VM Creation

**Combining multiple patterns:**

```yaml
---
- name: Create Proxmox VM with robust error handling
  hosts: proxmox_nodes
  gather_facts: false

  vars:
    vmid: 101
    vm_name: docker-01-nexus

  tasks:
    - name: Validate VM configuration
      ansible.builtin.assert:
        that:
          - vmid is defined and vmid >= 100
          - vm_name is match('^[a-z0-9-]+$')
        fail_msg: "Invalid VM configuration"

    - name: Check if VM already exists
      ansible.builtin.shell: |
        set -o pipefail
        qm list | awk '{print $1}' | grep -q "^{{ vmid }}$"
      args:
        executable: /bin/bash
      register: vm_exists
      changed_when: false
      failed_when: false

    - name: Create VM
      block:
        - name: Clone template
          ansible.builtin.command: >
            qm clone 9000 {{ vmid }}
            --name {{ vm_name }}
            --full
            --storage local-lvm
          when: vm_exists.rc != 0
          register: clone_result
          changed_when: true

        - name: Wait for clone to complete
          ansible.builtin.pause:
            seconds: 5
          when: clone_result is changed

        - name: Verify VM exists
          ansible.builtin.shell: |
            set -o pipefail
            qm list | grep "{{ vmid }}"
          args:
            executable: /bin/bash
          register: verify_vm
          changed_when: false
          failed_when: verify_vm.rc != 0
          retries: 3
          delay: 5
          until: verify_vm.rc == 0

        - name: Configure VM
          ansible.builtin.command: >
            qm set {{ vmid }}
            --memory 4096
            --cores 4
            --ipconfig0 ip=192.168.1.100/24,gw=192.168.1.1
          register: config_result
          changed_when: true

        - name: Start VM
          ansible.builtin.command: qm start {{ vmid }}
          register: start_result
          changed_when: true

      rescue:
        - name: Cleanup failed VM
          ansible.builtin.command: qm destroy {{ vmid }}
          when: vm_exists.rc != 0  # Only destroy if we created it
          ignore_errors: true

        - name: Report failure
          ansible.builtin.fail:
            msg: |
              Failed to create VM {{ vmid }}
              Clone result: {{ clone_result.stderr | default('N/A') }}
              Config result: {{ config_result.stderr | default('N/A') }}
              Start result: {{ start_result.stderr | default('N/A') }}

    - name: Report success
      ansible.builtin.debug:
        msg: "VM {{ vmid }} ({{ vm_name }}) created successfully"
      when: vm_exists.rc != 0
```

## Best Practices Summary

1. **Use `changed_when: false` for checks** - Read-only operations don't change state
2. **Use `failed_when` for expected errors** - Don't fail on "already exists" scenarios
3. **Always `register` command output** - Needed for `changed_when` and `failed_when`
4. **Use `set -euo pipefail` in shell** - Catch errors in pipes
5. **Validate inputs with assert** - Clear failure messages for bad config
6. **Use blocks for complex operations** - Enable rollback with rescue
7. **Add retries for transient failures** - Network calls, service startup
8. **Verify critical operations** - Check resource exists after creation
9. **Use `no_log` with secrets** - Never log sensitive data
10. **Provide clear error messages** - Help troubleshooting with context

## Anti-Patterns to Avoid

### ❌ Bad: Silent Failures

```yaml
- name: Important task
  ansible.builtin.command: critical-operation
  ignore_errors: true  # Hides failures!
```

### ❌ Bad: No Error Context

```yaml
- name: Deploy
  ansible.builtin.command: deploy.sh
  # No register, no error handling, no context
```

### ❌ Bad: Always Changed

```yaml
- name: Check if exists
  ansible.builtin.command: check-resource
  # Missing: changed_when: false
```

### ✅ Good: Explicit Error Handling

```yaml
- name: Critical operation
  ansible.builtin.command: critical-operation
  register: result
  changed_when: "'created' in result.stdout"
  failed_when:
    - result.rc != 0
    - "'already exists' not in result.stderr"

- name: Verify operation
  ansible.builtin.command: verify-operation
  changed_when: false
  failed_when: false
  register: verify

- name: Report result
  ansible.builtin.fail:
    msg: "Operation failed: {{ result.stderr }}"
  when: verify.rc != 0
```

## Further Reading

- [Ansible Error Handling](https://docs.ansible.com/ansible/latest/user_guide/playbooks_error_handling.html)
- [Ansible Conditionals](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
- [Ansible Blocks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_blocks.html)
