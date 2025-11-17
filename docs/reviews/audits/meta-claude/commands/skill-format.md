<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/format.md
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

### VIOLATION #1: Argument Handling - argument-hint format doesn't match official style

**Current:**

```markdown
argument-hint: [research-dir]
```

**Standard violated:** argument-hint should use lowercase-with-hyphens format for all arguments (slash-commands.md line 179 with examples at lines 189, 201)

**Severity:** Minor

**Why this matters:** The current format uses a hyphenated argument name in the hint, which is consistent with official examples. However, examining the official examples more closely:

- Line 189: `argument-hint: [message]` (single word, lowercase)
- Line 201: `argument-hint: [pr-number] [priority] [assignee]` (multi-word uses hyphens)

The current usage `[research-dir]` actually matches the pattern correctly. Upon re-examination, this is NOT a violation.

**Proposed fix:**

No fix needed - current format is correct.

---

### VIOLATION #2: Bash Execution - Overly permissive bash permissions

**Current:**

```yaml
allowed-tools: Bash(command:*)
```

**Standard violated:** Bash permissions should be appropriately scoped to specific commands needed, not overly permissive (slash-commands.md line 136, least privilege principle)

**Severity:** Minor

**Why this matters:** The command uses `Bash(command:*)` which grants permission to execute any bash command. However, examining the actual bash usage in the command (line 40), it only calls the Python script `format_skill_research.py`. The broad permission is functional but less secure than scoping to specific commands needed. That said, the command does need flexibility to run the Python script and the test command for directory verification.

**Proposed fix:**

Consider scoping to specific commands if possible:

```yaml
allowed-tools: Bash(test:*), Bash(python*:*)
```

Or keep as-is if the command needs flexibility for directory operations and script execution.

---

### VIOLATION #3: Argument Handling - Using $ARGUMENTS in bash context without clear documentation

**Current:**

Line 34: `Extract the research directory path from $ARGUMENTS (provided by user as research directory)`

Line 40:
```bash
${CLAUDE_PLUGIN_ROOT}/../../scripts/format_skill_research.py "$ARGUMENTS"
```

**Standard violated:** When using `$ARGUMENTS`, usage should be clear and consistent (slash-commands.md lines 96-107)

**Severity:** Minor

**Why this matters:** The command uses `$ARGUMENTS` in two contexts - once in instructions asking Claude to extract it, and once directly in a bash command. The instructions suggest Claude should "extract" the path from $ARGUMENTS, but then the bash command uses $ARGUMENTS directly. This could be confusing - if Claude is meant to extract it, why pass $ARGUMENTS directly to the script?

However, upon closer examination, the bash command block (lines 39-41) is showing Claude what command to run, and Claude will substitute $ARGUMENTS when executing. The instruction on line 34 is telling Claude to understand what $ARGUMENTS contains. This is actually clear enough.

**Proposed fix:**

No fix needed - the usage is clear in context.

---

## Summary

**Total violations found:** 1

**Breakdown by Severity:**

- Critical: 0 (blocks functionality)
- Major: 0 (significantly impacts usability)
- Minor: 1 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 0
- YAML Frontmatter: 0
- Markdown Content: 0
- Argument Handling: 0
- Bash Execution: 1
- File References: 0
- Command Content Quality: 0
- Design Principles: 0
- SlashCommand Tool Compatibility: 0

**Overall Assessment:** PASS

- No critical or major violations present
- One minor improvement opportunity identified
- Command is functional and follows standards

---

## Recommendations

### Critical Actions (Must Fix)

None.

### Major Actions (Should Fix)

None.

### Minor Actions (Nice to Have)

1. **Violation #2 - Scope bash permissions**: Consider scoping `allowed-tools` from `Bash(command:*)` to specific commands needed (`Bash(test:*), Bash(python*:*)`). Current permission is functional but broader than necessary. This improves security posture by following least privilege principle.

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
