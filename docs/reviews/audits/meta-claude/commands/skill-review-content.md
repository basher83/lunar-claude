<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/review-content.md
**Date:** 2025-11-17
**Reviewer:** command-audit Agent
**Command Type:** Plugin

---

## Standards Reference

**Source:**
`plugins/meta/claude-docs/skills/official-docs/reference/slash-commands.md`

**Key Requirements:**

**File Location (Lines 57-58, 71-72, 223):**

- Project commands: `.claude/commands/` directory
- User commands: `~/.claude/commands/` directory
- Plugin commands: `commands/` directory in plugin root

**Frontmatter Fields (Lines 176-182):**

- `description`: Brief description (optional, defaults to first line)
- `allowed-tools`: Tool permissions (optional, inherits from conversation)
- `argument-hint`: Expected arguments (optional)
- `model`: Specific model (optional, inherits from conversation)
- `disable-model-invocation`: Prevent SlashCommand tool (optional, default
  false)

**Arguments (Lines 96-126):**

- `$ARGUMENTS`: All arguments as single string
- `$1`, `$2`, etc.: Individual positional arguments

**Bash Execution (Lines 129-150):**

- Inline execution uses `!` prefix: `` !`command` ``
- Requires `allowed-tools: Bash(pattern:*)`

**File References (Lines 152-166):**

- Use `@` prefix: `@path/to/file`

**Best Practices:**

- Clear, specific instructions (not vague language)
- Written from Claude's perspective ("Your task is...")
- Examples for complex commands
- Single, clear purpose (Unix philosophy)
- KISS principle (Keep It Simple)
- YAGNI principle (You Aren't Gonna Need It)

---

## Violations Found

### VIOLATION #1: Argument Handling - Invalid argument placeholder

**Current:**

```markdown
/meta-claude:skill:review-content <skill-path>
```

**Standard violated:** Only `$ARGUMENTS` and `$1`, `$2`, etc. are recognized argument placeholders (slash-commands.md lines 96-126)

**Severity:** Critical

**Why this matters:** The placeholder `<skill-path>` is not a valid argument placeholder in Claude Code slash commands. Commands must use `$ARGUMENTS` for all arguments or `$1`, `$2`, etc. for positional arguments. Without valid placeholders, the command cannot receive user-provided values at runtime.

**Proposed fix:**

```markdown
/meta-claude:skill:review-content $ARGUMENTS
```

---

### VIOLATION #2: File References - File reference syntax incorrect

**Current:**

Line 226:
```markdown
/meta-claude:skill:review-content plugins/meta/meta-claude/skills/skill-creator
```

**Standard violated:** File references must use `@` prefix: `@path/to/file` (slash-commands.md lines 152-166)

**Severity:** Critical

**Why this matters:** Without the `@` prefix, Claude Code will not recognize this as a file reference and will not read the file contents. The command will receive the literal string instead of the file being loaded into context.

**Proposed fix:**

```markdown
/meta-claude:skill:review-content @plugins/meta/meta-claude/skills/skill-creator
```

---

### VIOLATION #3: File References - File reference syntax incorrect

**Current:**

Line 235:
```markdown
/meta-claude:skill:review-content /path/to/draft-skill
```

**Standard violated:** File references must use `@` prefix: `@path/to/file` (slash-commands.md lines 152-166)

**Severity:** Critical

**Why this matters:** Without the `@` prefix, Claude Code will not recognize this as a file reference and will not read the file contents. The command will receive the literal string instead of the file being loaded into context.

**Proposed fix:**

```markdown
/meta-claude:skill:review-content @/path/to/draft-skill
```

---

## Summary

**Total violations found:** 3

**Breakdown by Severity:**

- Critical: 3 (blocks functionality)
- Major: 0 (significantly impacts usability)
- Minor: 0 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 0
- YAML Frontmatter: 0
- Markdown Content: 0
- Argument Handling: 1
- Bash Execution: 0
- File References: 2
- Command Content Quality: 0
- Design Principles: 0
- SlashCommand Tool Compatibility: 0

**Overall Assessment:** FAIL

- **FAIL**: One or more critical violations present

---

## Recommendations

### Critical Actions (Must Fix)

1. **Fix Violation #1 - Invalid argument placeholder**:
   Replace `<skill-path>` with valid placeholder syntax. Change to `$ARGUMENTS` on line 8.

2. **Fix Violation #2 - Missing @ prefix for file reference**:
   Add `@` prefix to file path in example on line 226. Change `plugins/meta/meta-claude/skills/skill-creator` to `@plugins/meta/meta-claude/skills/skill-creator`.

3. **Fix Violation #3 - Missing @ prefix for file reference**:
   Add `@` prefix to file path in example on line 235. Change `/path/to/draft-skill` to `@/path/to/draft-skill`.

### Major Actions (Should Fix)

None.

### Minor Actions (Nice to Have)

None.

---
