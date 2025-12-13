---
name: ansible-error-handling
description: >
  This skill should be used when implementing error handling in Ansible, using
  block/rescue/always patterns, creating retry logic with until/retries, handling
  expected failures gracefully, or providing clear error messages with assert and fail.
---

# Ansible Error Handling

Patterns for robust error handling in Ansible playbooks and roles.

## Block/Rescue/Always Pattern

Handle errors and perform cleanup:

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

### Execution Flow

- **block**: Main tasks execute sequentially
- **rescue**: Runs if ANY task in block fails
- **always**: Runs regardless of success/failure

## Retry with Until

Handle transient failures with retries:

```yaml
- name: Wait for service to be ready
  ansible.builtin.uri:
    url: http://localhost:8080/health
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 30
  delay: 10
  # Total wait: up to 5 minutes (30 * 10s)
```

### With Command Module

```yaml
- name: Wait for cluster to stabilize
  ansible.builtin.command: pvecm status
  register: cluster_status
  until: "'Quorate: Yes' in cluster_status.stdout"
  retries: 12
  delay: 5
  changed_when: false
```

### Retry Parameters

| Parameter | Description |
|-----------|-------------|
| `until` | Condition that must be true to stop retrying |
| `retries` | Maximum number of attempts |
| `delay` | Seconds between attempts |

## Assert for Validation

Validate inputs with clear error messages:

```yaml
- name: Validate required variables
  ansible.builtin.assert:
    that:
      - vm_name is defined
      - vm_name | length > 0
      - vm_memory >= 1024
      - vm_cores >= 1
    fail_msg: |
      Invalid VM configuration:
      - vm_name: {{ vm_name | default('NOT SET') }}
      - vm_memory: {{ vm_memory | default('NOT SET') }} (min: 1024)
      - vm_cores: {{ vm_cores | default('NOT SET') }} (min: 1)
    success_msg: "VM configuration validated"
    quiet: true
```

### Common Assertions

```yaml
# Variable defined and non-empty
- vm_name is defined and vm_name | trim | length > 0

# Numeric range
- vm_memory >= 1024 and vm_memory <= 65536

# Regex match
- vm_name is match('^[a-z0-9-]+$')

# List has items
- vm_networks | length > 0

# Value in allowed list
- vm_ostype in ['l26', 'win10', 'win11']
```

## Fail with Context

Provide actionable error messages:

```yaml
- name: Check prerequisites
  ansible.builtin.command: which docker
  register: docker_check
  changed_when: false
  failed_when: false

- name: Fail if Docker not installed
  ansible.builtin.fail:
    msg: |
      Docker is not installed on {{ inventory_hostname }}.

      To install Docker:
        sudo apt update
        sudo apt install docker.io

      Or use the docker role:
        ansible-playbook playbooks/install-docker.yml
  when: docker_check.rc != 0
```

## Graceful Failure Handling

Allow expected "failures":

```yaml
- name: Try to stop service
  ansible.builtin.systemd:
    name: myservice
    state: stopped
  register: stop_result
  failed_when:
    - stop_result.failed
    - "'not found' not in stop_result.msg"
  # Only fail if error is NOT "service not found"
```

### Multiple Acceptable Conditions

```yaml
- name: Join cluster
  ansible.builtin.command: pvecm add {{ primary_node }}
  register: cluster_join
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
    - "'cannot join' not in cluster_join.stderr"
  changed_when: cluster_join.rc == 0
```

## Check Before Fail

Separate checking from failing for better control:

```yaml
- name: Check if resource exists
  ansible.builtin.command: check-resource {{ resource_id }}
  register: resource_check
  changed_when: false
  failed_when: false  # Don't fail here

- name: Fail with context if missing
  ansible.builtin.fail:
    msg: |
      Resource {{ resource_id }} not found.
      Command output: {{ resource_check.stderr }}
      Hint: Ensure resource was created first.
  when: resource_check.rc != 0
```

## Error Recovery Pattern

Attempt operation, handle specific errors:

```yaml
- name: Attempt primary approach
  block:
    - name: Connect via primary endpoint
      ansible.builtin.uri:
        url: "https://{{ primary_host }}:8006/api2/json"
        validate_certs: true
      register: primary_result

  rescue:
    - name: Log primary failure
      ansible.builtin.debug:
        msg: "Primary endpoint failed: {{ primary_result.msg | default('unknown error') }}"

    - name: Try fallback endpoint
      ansible.builtin.uri:
        url: "https://{{ fallback_host }}:8006/api2/json"
        validate_certs: false
      register: fallback_result
```

## Delegate Error Handling

Run checks from controller for better error context:

```yaml
- name: Verify API endpoint from controller
  ansible.builtin.uri:
    url: "https://{{ inventory_hostname }}:8006/api2/json/version"
    validate_certs: false
  delegate_to: localhost
  register: api_check
  failed_when: false

- name: Report API status
  ansible.builtin.fail:
    msg: |
      Cannot reach Proxmox API on {{ inventory_hostname }}
      Status: {{ api_check.status | default('connection failed') }}
      Check: Network connectivity, firewall rules, pveproxy service
  when: api_check.status | default(0) != 200
```

## Ignore Errors (Use Sparingly)

```yaml
- name: Remove optional backup
  ansible.builtin.file:
    path: /backup/old-backup.tar.gz
    state: absent
  ignore_errors: true
  register: cleanup_result

- name: Report cleanup status
  ansible.builtin.debug:
    msg: "Cleanup {{ 'successful' if not cleanup_result.failed else 'skipped' }}"
```

### When ignore_errors is Acceptable

- Non-critical cleanup tasks
- Optional operations that shouldn't block playbook
- When the result is immediately checked anyway

### Prefer failed_when

```yaml
# BETTER than ignore_errors
- name: Remove backup
  ansible.builtin.file:
    path: /backup/old-backup.tar.gz
    state: absent
  register: cleanup_result
  failed_when:
    - cleanup_result.failed
    - "'does not exist' not in cleanup_result.msg | default('')"
```

## Complete Example

```yaml
---
- name: Deploy with comprehensive error handling
  hosts: app_servers
  become: true

  tasks:
    - name: Validate configuration
      ansible.builtin.assert:
        that:
          - app_version is defined
          - app_version is match('^\d+\.\d+\.\d+$')
        fail_msg: "Invalid app_version: {{ app_version | default('NOT SET') }}"

    - name: Deploy application
      block:
        - name: Download release
          ansible.builtin.get_url:
            url: "https://releases.example.com/{{ app_version }}.tar.gz"
            dest: /tmp/app.tar.gz
          register: download
          until: download is succeeded
          retries: 3
          delay: 5

        - name: Stop current version
          ansible.builtin.systemd:
            name: myapp
            state: stopped

        - name: Extract release
          ansible.builtin.unarchive:
            src: /tmp/app.tar.gz
            dest: /opt/myapp
            remote_src: true

        - name: Start new version
          ansible.builtin.systemd:
            name: myapp
            state: started

        - name: Verify health
          ansible.builtin.uri:
            url: http://localhost:8080/health
          register: health
          until: health.status == 200
          retries: 6
          delay: 10

      rescue:
        - name: Restore previous version
          ansible.builtin.copy:
            src: /opt/myapp-backup/
            dest: /opt/myapp/
            remote_src: true

        - name: Start previous version
          ansible.builtin.systemd:
            name: myapp
            state: started

        - name: Report deployment failure
          ansible.builtin.fail:
            msg: |
              Deployment of {{ app_version }} failed.
              Previous version restored.
              Check logs: journalctl -u myapp

      always:
        - name: Cleanup download
          ansible.builtin.file:
            path: /tmp/app.tar.gz
            state: absent
```

## Additional Resources

For detailed error handling patterns and techniques, consult:

- **`references/error-handling.md`** - Comprehensive error handling patterns, block/rescue/always examples, retry strategies

## Related Skills

- **ansible-idempotency** - changed_when/failed_when patterns
- **ansible-fundamentals** - Core Ansible concepts
