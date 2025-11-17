<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/research.md
**Date:** 2025-11-17
**Reviewer:** Command Audit Agent
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

This command file fully complies with official Claude Code slash command
standards.

---

## Compliance Highlights

The command demonstrates excellent adherence to standards:

### File Structure & Location

- ✓ Correctly placed in `plugins/meta/meta-claude/commands/skill/` directory
- ✓ Uses `.md` extension
- ✓ Filename follows naming conventions (lowercase with hyphens)

### YAML Frontmatter

- ✓ Valid YAML syntax
- ✓ Contains `description` field for SlashCommand tool discoverability
- ✓ `argument-hint` uses correct lowercase bracket format: `[skill-name] [sources]`
- ✓ `allowed-tools` appropriately scoped to specific commands needed:
  - `Bash(python:*)` - for research scripts
  - `Bash(mkdir:*)` - for directory creation
  - `Bash(ls:*)` - for output verification
  - `Bash(echo:*)` - for status messages
  - `Read, Write, AskUserQuestion` - for file operations and user interaction

### Markdown Content

- ✓ Valid markdown structure with proper heading hierarchy
- ✓ All code blocks specify language (verified via automated check)
- ✓ Blank lines around code blocks (verified via rumdl - no MD031/MD032 violations)
- ✓ Clear, well-organized sections

### Argument Handling

- ✓ Uses only valid `$ARGUMENTS` placeholder
- ✓ Documents argument parsing clearly in "Inputs" and "Step 1" sections
- ✓ `argument-hint` matches actual usage (`[skill-name] [sources]`)

### Command Content Quality

- ✓ Instructions are clear and specific with detailed workflows
- ✓ Written from Claude's perspective ("Your task is to...", "Your task is to parse...")
- ✓ Expected output format well-specified (directory structure, file naming)
- ✓ Comprehensive examples section with 4 detailed scenarios

### Design Principles

- ✓ Single, clear purpose: Automated research gathering for skill creation
- ✓ KISS principle: Straightforward approach with clear decision logic
- ✓ YAGNI principle: Only includes features needed for research automation

### SlashCommand Tool Compatibility

- ✓ `description` field present for tool discoverability
- ✓ Description is concise (53 characters - well under budget)

---

## Recommendations

**No actions required.** This command file serves as an excellent example of
slash command standards compliance.

---

## Notes

- This command was audited after recent fixes applied to other meta-claude
  skill commands
- All previous violations have been successfully resolved
- Command demonstrates best practices for:
  - Bash permission scoping
  - Argument documentation
  - Example quality
  - Error handling documentation
