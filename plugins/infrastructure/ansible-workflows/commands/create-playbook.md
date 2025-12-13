---
description: Scaffold a state-based Ansible playbook with present/absent pattern
argument-hint: <playbook-name> [--hosts <target>]
allowed-tools: Write, Read
model: sonnet
---

Create a state-based Ansible playbook named `$1`.

Load the `ansible-playbook-design` and `ansible-fundamentals` skills first.

If no playbook name provided, ask for one.

**Playbook location:** `ansible/playbooks/$1.yml` (add .yml if missing)

**Target hosts:** Use `$2` if provided with --hosts, otherwise default to `all`

**Create state-based playbook supporting present/absent:**

```yaml
---
# Usage:
#   Create: uv run ansible-playbook playbooks/$1.yml
#   Remove: uv run ansible-playbook playbooks/$1.yml -e "resource_state=absent"

- name: [Descriptive play name]
  hosts: [target]
  become: true
  gather_facts: true

  vars:
    resource_state: present

  tasks:
    - name: Validate state variable
      ansible.builtin.assert:
        that:
          - resource_state in ['present', 'absent']
        fail_msg: "resource_state must be 'present' or 'absent'"

    # Main tasks here
```

After scaffolding, hand off to `ansible-generator` agent with playbook path and requirements.

Report: playbook path, state pattern implemented, usage commands.
