---
description: Scaffold a state-based Ansible playbook with present/absent pattern
argument-hint: <playbook-name> [--hosts <target>]
allowed-tools: ["Write", "Read", "Bash"]
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

**After scaffolding, initialize the pipeline:**

1. Create the `.claude/` directory if it doesn't exist:
   ```bash
   mkdir -p "$CLAUDE_PROJECT_DIR/.claude"
   ```

2. Ensure `.gitignore` contains ansible-workflows patterns (append if missing):
```text
# Ansible Workflows plugin state (auto-added)
.claude/ansible-workflows.local.md
.claude/ansible-workflows.*.bundle.md
```

3. Write state file `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.local.md`:
```yaml
---
active: true
pipeline_phase: generating
target_path: ansible/playbooks/$1.yml
current_agent: ansible-generator
started_at: "[ISO timestamp]"
validation_attempts: 0
last_validation_passed: true
---

# Ansible Workflows Pipeline

Target: ansible/playbooks/$1.yml
Type: playbook
```

4. Write scaffolding bundle `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.scaffolding.bundle.md`:
```yaml
---
source_agent: create-playbook
target_agent: ansible-generator
timestamp: "[ISO timestamp]"
target_path: ansible/playbooks/$1.yml
target_type: playbook
---

# Scaffolding Bundle

## Target Path
ansible/playbooks/$1.yml

## User Requirements
[Capture any user-specified requirements, hosts, or context]

## Files Created
- ansible/playbooks/$1.yml (scaffolded)

## Next Steps
Implement the playbook tasks based on user requirements.
```

5. Hand off to `ansible-generator` agent with the playbook path

Report: playbook path, state pattern implemented, pipeline initialized.
