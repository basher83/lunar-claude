---
description: Add, update, or review plugin-dev design considerations
allowed-tools: ["Read", "Edit", "Write", "AskUserQuestion"]
---

# Plugin-Dev Considerations Manager

Manage design considerations, decisions, and ideas in `.claude/plugin-dev-considerations.local.md`.

---

## Workflow

1. Check if `.claude/plugin-dev-considerations.local.md` exists
2. If not, create it with this structure:

```markdown
---
type: design-considerations
plugin: plugin-dev
last_updated: [today]
---

# Plugin-Dev Design Considerations

Tracking decisions, future ideas, and observations that emerge during development.

## Open Considerations

(none yet)

## Decisions Made

(none yet)

## Future Ideas

(none yet)
```

3. Read and show current state:
   - Count of open CON entries
   - Count of DEC entries
   - Count of IDEA entries

4. Ask user what to do:
   - Add consideration (CON)
   - Add decision (DEC)
   - Add idea (IDEA)
   - Update existing entry
   - Just reviewing (done)

5. Based on selection, gather needed info and add/update entry

6. Update `last_updated` in frontmatter

---

## Entry Formats

**CON (Consideration):**
```markdown
### CON-XXX: [title]

**Raised:** [date]
**Context:** [where this came up]
**Status:** Under consideration

**Observation:**
[what was noticed]

**Next action:** [what to do next]
```

**DEC (Decision):**
```markdown
### DEC-XXX: [title]

**Date:** [date]
**Context:** [what prompted this]

**Decision:** [what was decided]

**Rationale:** [why]
```

**IDEA (Future Idea):**
```markdown
### IDEA-XXX: [title]

[brief description]
```

---

## Numbering

Find highest existing number in each category and increment by 1.
