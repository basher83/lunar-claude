---
description: Add, update, or review plugin-dev design considerations
argument-hint: [add|update|list] [CON|DEC|IDEA] [title]
allowed-tools: ["Read", "Edit", "Write", "AskUserQuestion"]
---

# Plugin-Dev Considerations Manager

Manage design considerations, decisions, and ideas in `.claude/plugin-dev-considerations.local.md`.

**Arguments:** $ARGUMENTS

---

## Workflow

### If no arguments or "list":

1. Read `.claude/plugin-dev-considerations.local.md`
2. Show summary:
   - Open considerations (CON-XXX) with status
   - Recent decisions (DEC-XXX)
   - Ideas backlog (IDEA-XXX)
3. Ask: "What would you like to do?"
   - Add new entry
   - Update existing entry
   - Mark consideration as decided

### If "add CON [title]":

1. Find next CON number
2. Ask for:
   - Context (where this came up)
   - Observation (what was noticed)
   - Options (if any)
3. Add entry using template:

```markdown
### CON-XXX: [title]

**Raised:** [today's date]
**Context:** [user input]
**Status:** Under consideration

**Observation:**
[user input]

**Options:**
[user input or "To be determined"]

**Next action:** [user input or "Evaluate further"]
```

4. Update `last_updated` in frontmatter

### If "add DEC [title]":

1. Find next DEC number
2. Ask for:
   - Context (what prompted this)
   - Decision (what was decided)
   - Rationale (why)
   - Implementation (how, if applicable)
3. Add entry using template:

```markdown
### DEC-XXX: [title]

**Date:** [today's date]
**Context:** [user input]

**Decision:** [user input]

**Rationale:** [user input]

**Implementation:** [user input or "Pending"]
```

4. Update `last_updated` in frontmatter

### If "add IDEA [title]":

1. Find next IDEA number
2. Ask for brief description
3. Add to Future Ideas section:

```markdown
### IDEA-XXX: [title]

[description]
```

4. Update `last_updated` in frontmatter

### If "update [ID]":

1. Read current entry
2. Show current state
3. Ask what to update:
   - Status (for CON entries)
   - Add implementation details (for DEC entries)
   - Convert CON to DEC (decision made)
4. Apply changes
5. Update `last_updated` in frontmatter

---

## Quick Examples

```bash
/plugin-dev:consider                           # List all
/plugin-dev:consider add CON skill conversion  # New consideration
/plugin-dev:consider add DEC state file pattern # New decision
/plugin-dev:consider add IDEA audit command    # New idea
/plugin-dev:consider update CON-001            # Update entry
```

---

## File Location

State file: `.claude/plugin-dev-considerations.local.md`

If file doesn't exist, create it with template from plugin-dev.
