---
workflow: plugin-dev-bug-tracking
status: active
started: 2025-12-18
last_updated: 2025-12-18
---

# Plugin-Dev Bug Tracking

Tracking bugs discovered in the plugin-dev plugin during development.

## Open Bugs

### BUG-001: skill-development skill fails to load

**Discovered:** 2025-12-18
**Severity:** High
**Component:** `plugins/meta/plugin-dev/skills/skill-development/SKILL.md`

**Symptoms:**
```bash
Bash command failed for pattern "!` escape does NOT work.
zsh: command not found: escape
(eval):3: no matches found: **Good:**
```

**Root Cause:**
The skill-development SKILL.md contains examples of the `!` backtick dynamic bash pattern inside fenced code blocks. Due to GitHub issue #12781, the skill parser executes these patterns even inside code blocks.

**Affected Content:**
The skill documents the bug and shows "bad" examples that themselves trigger the bug:
```markdown
❌ **Bad:**
` ` `markdown
` ` `bash
# Example of dynamic execution
!`git status`
` ` `
` ` `
```

**Irony:** The skill that documents how to avoid this bug is itself broken by it.

**Workaround:**
- Read skill files directly with Read tool instead of using Skill tool
- Grep for specific content

**Fix Required:**
Replace `!` backtick examples in the skill with `$` shell notation or move to reference files.

**Related:** GitHub #12781 (dynamic bash pattern bug)

---

## Resolved Bugs

(none yet)
