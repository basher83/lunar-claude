# Playbook and Role Design Patterns

Best practices for structuring playbooks and roles based on production patterns from community roles like
`geerlingguy.docker` and this repository.

## Pattern 1: State-Based Playbooks (Not Separate Create/Delete)

### Anti-Pattern: Separate playbooks for each operation

```text
❌ BAD:
playbooks/
├── create-user.yml
└── delete-user.yml
```

### Best Practice: Single playbook with state variable

```text
✅ GOOD:
playbooks/
└── manage-user.yml   # Handles both create and delete via state variable
```

### Why This Pattern?

Following community role patterns (like `geerlingguy.docker`, `geerlingguy.postgresql`):

- **Single source of truth**: One playbook to maintain
- **Consistent interface**: Same variables, just change `state`
- **Less duplication**: Validation and logic shared
- **Familiar pattern**: Matches how Ansible modules work

### Implementation Example

**Role with state support** (`roles/system_user/tasks/main.yml`):

```yaml
---
- name: Create/update system users
  ansible.builtin.include_tasks: create_users.yml
  loop: "{{ system_users }}"
  when:
    - user_item.state | default('present') == 'present'

- name: Remove system users
  ansible.builtin.include_tasks: remove_users.yml
  loop: "{{ system_users }}"
  when:
    - user_item.state | default('present') == 'absent'
```

**Playbook using the role** (`playbooks/manage-admin-user.yml`):

```yaml
---
# Playbook: Manage Administrative User
# Usage:
#   # Create:
#   uv run ansible-playbook playbooks/manage-admin-user.yml \
#     -e "admin_name=myuser" -e "admin_ssh_key='ssh-ed25519 ...'"
#
#   # Remove:
#   uv run ansible-playbook playbooks/manage-admin-user.yml \
#     -e "admin_name=myuser" -e "admin_state=absent"

- name: Manage Administrative User
  hosts: "{{ target_cluster | default('all') }}"
  become: true

  pre_tasks:
    - name: Set default state
      ansible.builtin.set_fact:
        admin_state_value: "{{ admin_state | default('present') }}"

    - name: Validate variables
      ansible.builtin.assert:
        that:
          - admin_name is defined
          - (admin_state_value == 'absent') or (admin_ssh_key is defined)
        fail_msg: "admin_name required. admin_ssh_key required when state=present"

  roles:
    - role: system_user
      vars:
        system_users:
          - name: "{{ admin_name }}"
            state: "{{ admin_state_value }}"
            # Only include creation params when state=present
            ssh_keys: "{{ [] if admin_state_value == 'absent' else [admin_ssh_key] }}"
            sudo_nopasswd: "{{ false if admin_state_value == 'absent' else true }}"
```

### Key Design Decisions

1. **Default to `present`**: Makes common case (creation) easiest

   ```yaml
   admin_state_value: "{{ admin_state | default('present') }}"
   ```

2. **Conditional validation**: SSH key only required when creating

   ```yaml
   - (admin_state_value == 'absent') or (admin_ssh_key is defined)
   ```

3. **Conditional parameters**: Skip unnecessary vars when removing

   ```yaml
   ssh_keys: "{{ [] if admin_state_value == 'absent' else [admin_ssh_key] }}"
   ```

4. **State-specific messages**: Different post_tasks based on state

   ```yaml
   - name: Display success (created)
     when: admin_state_value == 'present'

   - name: Display success (removed)
     when: admin_state_value == 'absent'
   ```

## Pattern 2: Public API Variables (No Role Prefix)

**Role defaults** should use clean variable names (not prefixed):

```yaml
# roles/system_user/defaults/main.yml
---
# noqa: var-naming[no-role-prefix] - This is the role's public API
system_users: []
```

**Why?**

- Clean interface for users of the role
- Follows community role patterns (`docker_users`, not `geerlingguy_docker_users`)
- Internal variables should be prefixed (e.g., `system_user_create_result`)

## Pattern 3: Smart Variable Defaults in Playbooks

Use `set_fact` to handle defaults gracefully:

```yaml
pre_tasks:
  - name: Set default values for optional variables
    ansible.builtin.set_fact:
      admin_shell_value: "{{ admin_shell | default('/bin/bash') }}"
      admin_comment_value: "{{ admin_comment | default('System Administrator') }}"
    when: admin_state_value == 'present'
```

**Benefits:**

- Defaults set once, used everywhere
- Clear separation of user input vs computed values
- Conditional defaults (only when needed)

## Pattern 4: Comprehensive Pre-flight Validation

Validate early, fail fast:

```yaml
pre_tasks:
  - name: Validate required variables
    ansible.builtin.assert:
      that:
        - admin_name is defined
        - admin_name | length > 0
        # Conditional validation
        - (admin_state_value == 'absent') or (admin_ssh_key is defined)
      fail_msg: "Clear error message about what's missing"
      success_msg: "All required variables present"
```

**Why validate in playbook, not role?**

- Playbooks know the specific use case
- Roles should be flexible
- Better error messages with context

## Pattern 5: Documentation in Playbook Headers

Self-documenting playbooks with usage examples:

```yaml
---
# Playbook: Manage Administrative User
# Purpose: Create or remove admin users with SSH and sudo
# Role: ansible/roles/system_user
#
# Usage:
#   # Create user:
#   uv run ansible-playbook playbooks/manage-admin-user.yml \
#     -e "admin_name=alice" \
#     -e "admin_ssh_key='ssh-ed25519 ...'"
#
#   # Remove user:
#   uv run ansible-playbook playbooks/manage-admin-user.yml \
#     -e "admin_name=alice" \
#     -e "admin_state=absent"
#
# Variables:
#   admin_name (required): Username
#   admin_ssh_key (required for create): SSH public key
#   admin_state (optional): present or absent (default: present)
#   admin_shell (optional): User shell (default: /bin/bash)
```

## Pattern 6: Informative Output Messages

Context-aware success messages:

```yaml
post_tasks:
  - name: Display success message (user created)
    ansible.builtin.debug:
      msg: |
        ========================================
        User Creation Complete
        ========================================
        User '{{ admin_name }}' configured on {{ inventory_hostname }}

        Test SSH: ssh {{ admin_name }}@{{ inventory_hostname }}
        Test sudo: ssh {{ admin_name }}@{{ inventory_hostname }} sudo id
    when: admin_state_value == 'present'

  - name: Display success message (user removed)
    ansible.builtin.debug:
      msg: |
        ========================================
        User Removal Complete
        ========================================
        User '{{ admin_name }}' removed from {{ inventory_hostname }}

        Verify: ssh root@{{ inventory_hostname }} "id {{ admin_name }}"
    when: admin_state_value == 'absent'
```

**Benefits:**

- Users know what to do next
- Copy-paste ready commands
- Different messages per operation

## Testing the Pattern

### Idempotency Test

Both operations should be idempotent:

```bash
# Create - first run should change, second should not
uv run ansible-playbook playbooks/manage-user.yml -e "admin_name=test" -e "admin_ssh_key='...'"
# Result: changed=5

uv run ansible-playbook playbooks/manage-user.yml -e "admin_name=test" -e "admin_ssh_key='...'"
# Result: changed=0 ✅

# Remove - first run should change, second should not
uv run ansible-playbook playbooks/manage-user.yml -e "admin_name=test" -e "admin_state=absent"
# Result: changed=2

uv run ansible-playbook playbooks/manage-user.yml -e "admin_name=test" -e "admin_state=absent"
# Result: changed=0 ✅
```

## Real-World Example

From this repository: `ansible/playbooks/create-admin-user.yml` + `ansible/roles/system_user/`

**Features:**

- ✅ Single playbook for create and remove
- ✅ State defaults to `present`
- ✅ Conditional validation (SSH key only when creating)
- ✅ Conditional role variables
- ✅ State-specific output messages
- ✅ Fully idempotent (tested on production infrastructure)

**Usage:**

```bash
# Create admin user with full sudo
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/create-admin-user.yml \
  -e "admin_name=alice" \
  -e "admin_ssh_key='ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...'"

# Remove the user
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/create-admin-user.yml \
  -e "admin_name=alice" \
  -e "admin_state=absent"
```

## Comparison: Before and After

### Before (Anti-pattern)

```text
playbooks/
├── create-admin-user.yml      # 70 lines
└── delete-admin-user.yml      # 45 lines
                                # = 115 lines total
                                # = 2 files to maintain
                                # = Different interfaces
```

### After (Best practice)

```text
playbooks/
└── create-admin-user.yml      # 95 lines
                                # = 1 file to maintain
                                # = Consistent interface
                                # = Follows community patterns
```

## Related Patterns

- **Variable precedence**: See [reference/variable-precedence.md](../reference/variable-precedence.md)
- **Role structure**: See [reference/roles-vs-playbooks.md](../reference/roles-vs-playbooks.md)
- **Idempotency**: See [reference/idempotency-patterns.md](../reference/idempotency-patterns.md)

## Summary

✅ **Do:**

- Single playbook with `state` variable
- Default `state: present` for common case
- Conditional validation and parameters
- Public API variables without role prefix
- Comprehensive documentation in headers

❌ **Don't:**

- Create separate create/delete playbooks
- Require parameters for both create and delete
- Use role prefixes on public API variables
- Omit usage examples from playbooks
