<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/research.md
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

**No violations found.**

This command file fully complies with all slash command standards.

---

## Summary

**Total violations found:** 0

**Breakdown by Severity:**

- Critical: 0 (blocks functionality)
- Major: 0 (significantly impacts usability)
- Minor: 0 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 0
- YAML Frontmatter: 0
- Markdown Content: 0
- Argument Handling: 0
- Bash Execution: 0
- File References: 0
- Command Content Quality: 0
- Design Principles: 0
- SlashCommand Tool Compatibility: 0

**Overall Assessment:** PASS

- **PASS**: No critical or major violations

---

## Recommendations

### Critical Actions (Must Fix)

None.

### Major Actions (Should Fix)

None.

### Minor Actions (Nice to Have)

None.

---

## Compliance Highlights

This command demonstrates excellent adherence to standards:

**File Structure:**

- Correctly located in plugin commands directory
- Proper naming convention (lowercase with hyphens)
- Valid markdown extension

**Frontmatter:**

- Well-structured YAML frontmatter
- Includes helpful `description` field for discoverability
- Correctly formatted `argument-hint` field using `[lowercase-with-hyphens]` pattern
- Appropriately scoped `allowed-tools` permissions (python, mkdir, ls, echo)

**Argument Handling:**

- Properly uses `$ARGUMENTS` placeholder
- Documents both required and optional arguments
- `argument-hint` matches actual usage pattern

**Bash Permissions:**

- Grants bash permissions for specific commands Claude needs during execution
- Does not use inline bash execution (`` !`command` ``), which is correct for this use case
- Permissions are scoped to specific commands (python, mkdir, ls, echo) following least privilege

**Content Quality:**

- Clear, specific instructions throughout
- Written from Claude's perspective ("Your task is...")
- Comprehensive examples section (4 detailed examples)
- Well-organized with logical sections
- Expected output format clearly specified
- Error handling section with specific guidance

**Design:**

- Single clear purpose: Automated research gathering for skill creation
- Follows KISS principle with straightforward workflow
- Follows YAGNI principle - no unnecessary features

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
