<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** [path/to/command-file.md]
**Date:** [YYYY-MM-DD]
**Reviewer:** [Human/Agent Name]
**Command Type:** [Project/User/Plugin]

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

### VIOLATION #1: [Category] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Specific requirement from slash-commands.md with line
number]

**Severity:** [Critical/Major/Minor]

**Why this matters:** [Explain impact - does it break functionality, hurt
usability, or just miss best practice?]

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

### VIOLATION #2: [Category] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Specific requirement from slash-commands.md with line
number]

**Severity:** [Critical/Major/Minor]

**Why this matters:** [Explain impact]

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

[Continue for each violation...]

---

## Summary

**Total violations found:** [N]

**Breakdown by Severity:**

- Critical: [count] (blocks functionality)
- Major: [count] (significantly impacts usability)
- Minor: [count] (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: [count]
- YAML Frontmatter: [count]
- Markdown Content: [count]
- Argument Handling: [count]
- Bash Execution: [count]
- File References: [count]
- Command Content Quality: [count]
- Design Principles: [count]
- SlashCommand Tool Compatibility: [count]

**Overall Assessment:** [PASS / FAIL / WARNINGS]

- **PASS**: No critical or major violations
- **FAIL**: One or more critical violations present
- **WARNINGS**: Major violations but no critical issues

---

## Recommendations

### Critical Actions (Must Fix)

[List all Critical severity violations with specific fixes]

1. [Action item with reference to violation #]
2. [Action item with reference to violation #]

### Major Actions (Should Fix)

[List all Major severity violations with specific fixes]

1. [Action item with reference to violation #]
2. [Action item with reference to violation #]

### Minor Actions (Nice to Have)

[List all Minor severity violations with specific fixes]

1. [Action item with reference to violation #]
2. [Action item with reference to violation #]

---

## Severity Classification Guide

Use this guide when categorizing violations:

**Critical (Blocks Functionality):**

- Invalid YAML frontmatter syntax
- Invalid argument placeholders
- Missing bash permissions when bash used
- Invalid bash execution syntax
- Invalid file reference syntax

**Major (Significantly Impacts Usability):**

- Missing positional argument documentation
- Vague or ambiguous instructions
- Missing examples for complex commands
- Wrong command perspective
- Argument hint mismatch

**Minor (Improvement Opportunity):**

- Missing frontmatter description
- Overly broad bash permissions
- Missing blank lines
- Missing code block languages
- Non-existent static file references

---

## Notes

Use this section ONLY to provide feedback on the audit process itself. Document issues encountered during the audit workflow, not analysis of the command.

**Include Notes if:**
- Checklist was ambiguous or unclear
- Template formatting didn't fit edge case
- Standards document missing examples
- Difficulty determining severity
- Suggestions to improve audit process

**Do NOT include:**
- Git history or previous fixes
- Command best practices
- Implications of the command
- Analysis of what command does well

**If audit process ran smoothly:** Omit this section entirely.
