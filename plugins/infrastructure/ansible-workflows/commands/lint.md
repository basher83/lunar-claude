---
description: Run ansible-lint with guidance on fixing issues
argument-hint: [path]
allowed-tools: Bash, Read
model: haiku
---

Run ansible-lint on `$ARGUMENTS` (or `ansible/` if no path provided).

Execute: `uv run ansible-lint $ARGUMENTS 2>&1 || true`

Parse results and categorize:
- **Errors:** Must fix
- **Warnings:** Should fix
- **Info:** Optional

For each issue, explain:
1. What the rule checks
2. How to fix it

**Common fixes:**

| Rule | Fix |
|------|-----|
| fqcn[action-core] | Use `ansible.builtin.module` not `module` |
| no-changed-when | Add `changed_when: false` to command tasks |
| name[missing] | Add `name:` to all tasks |

Report: total issues, by severity, top issues, fix suggestions.
