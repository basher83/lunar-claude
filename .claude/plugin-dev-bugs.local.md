---
workflow: plugin-dev-bug-tracking
status: active
started: 2025-12-18
last_updated: 2025-12-28
---

# Plugin-Dev Bug Tracking

Tracking bugs discovered in the plugin-dev plugin during development.

## Open Bugs

(none currently)

---

## Resolved Bugs

### BUG-001: skill-development skill fails to load

**Discovered:** 2025-12-18
**Resolved:** 2025-12-28
**Severity:** High
**Component:** `plugins/meta/plugin-dev/skills/skill-development/SKILL.md`

**Symptoms:**
```bash
# Original (2025-12-18):
Bash command failed for pattern "!` escape does NOT work.
zsh: command not found: escape

# Recurrence (2025-12-28):
Bash command failed for pattern "!` backtick patterns and `"
zsh: command not found: backtick
```

**Root Cause:**
The skill-development SKILL.md contained references to the exclamation-backtick dynamic bash pattern that triggered the parser. Due to GitHub issue #12781, the skill parser executes these patterns even inside fenced code blocks or inline code.

**Affected Content:**
Two locations triggered the bug:
1. Code block examples showing "bad" patterns (fixed 2025-12-18)
2. Line 650: `` `!` backtick patterns `` in prose text (fixed 2025-12-28)

**Resolution:**
1. Replaced code block examples with `$` shell notation
2. Changed `` `!` backtick patterns `` to `exclamation-backtick patterns` in prose

**Related:** GitHub #12781 (dynamic bash pattern bug)
