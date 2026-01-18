---
description: Create a new slash command
argument-hint: Optional command description
allowed-tools: Read, Grep, Write
---

# Create Slash Command

## Phase 1: Skill Requirements Extraction (BLOCKING)

Read these files NOW before proceeding:

1. `${CLAUDE_PLUGIN_ROOT}/skills/command-development/SKILL.md`
2. `${CLAUDE_PLUGIN_ROOT}/skills/command-development/references/testing-strategies.md`

After reading, output a **Requirements Summary** with these exact sections:

### Frontmatter Fields

| Field | Purpose | Valid Values |
|-------|---------|--------------|
| [extract each field from skill] | | |

### Argument Syntax Rules

- $ARGUMENTS: [when/how to use]
- Positional ($1, $2): [when/how to use]
- argument-hint: [format requirement]

### File Reference Syntax

- @ syntax: [correct usage]
- Static vs dynamic: [difference]

### Bash Execution Syntax

- Inline execution syntax: [exact format from skill]
- allowed-tools requirement: [pattern]

### Command Location Rules

- Project commands: [path]
- Personal commands: [path]
- Plugin commands: [path]

### Anti-Patterns (from "Critical: Commands are Instructions FOR Claude")

- Incorrect approach: [what to avoid]
- Correct approach: [what to do]

**Do not proceed until this summary is complete with skill-specific content.**

---

## Phase 2: Command Specification

**Command name:**
**Purpose:**
**Location:** [project/personal/plugin]
**Arguments (if any):**
**Tools needed (if any):**
**File references (if any):**

---

## Phase 3: Implementation

Create the command file applying ALL requirements from Phase 1.

---

## Phase 4: Testing Plan (from testing-strategies.md)

Generate a testing checklist for this specific command:

### Level 1-2: Structural Validation

```bash
# [generate validation commands for this command]
```

### Level 4: Argument Testing

| Test Case | Command | Expected |
|-----------|---------|----------|
| [generate test matrix for this command's arguments] |  |  |

### Edge Cases

- [list 3-5 edge cases specific to this command]

---

## Phase 5: Self-Verification

| Skill Requirement | Implemented? | Evidence |
|-------------------|--------------|----------|
| Instructions written FOR Claude (not TO user) | | |
| description < 60 chars | | |
| argument-hint matches actual arguments | | |
| allowed-tools if bash used | | |
| @ syntax correct for file refs | | |
| Single responsibility | | |

If any row is NO, fix before presenting final command.
