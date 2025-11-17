<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/validate-audit.md
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

### VIOLATION #1: Argument Handling - Missing positional argument documentation

**Current:**

The command shows usage with `<skill-path>` argument:

    ## Usage

    ```bash
    /meta-claude:skill:validate-audit <skill-path>
    ```

But the Instructions section never uses `$ARGUMENTS` or `$1` to capture this value.

**Standard violated:** When using positional arguments (`$1`, `$2`, etc.), each positional parameter must be explained so users know argument order and meaning (slash-commands.md lines 109-126)

**Severity:** Major

**Why this matters:** The command expects a `<skill-path>` argument but never uses `$ARGUMENTS` or `$1` placeholder to capture it in the instructions. Users won't know how to pass the skill path, and Claude won't have access to the value.

**Proposed fix:**

Update the Instructions section to use the positional argument:

    ## Instructions

    Use the Task tool to invoke the skill-auditor agent:

    ```text
    I need to audit the skill at $ARGUMENTS for compliance with official Claude Code specifications.

    Please review:
    - SKILL.md structure and organization
    - Frontmatter quality and completeness
    - Progressive disclosure patterns
    - Content clarity and usefulness
    - Adherence to best practices

    Provide a detailed audit report with recommendations.
    ```

---

### VIOLATION #2: Command Content Quality - Vague instructions using forbidden tool

**Current:**

    Use the Task tool to invoke the skill-auditor agent:

**Standard violated:** Instructions must be clear and specific, using specific action verbs and avoiding vague language like "handle", "process", or "deal with" (checklist section 7)

**Severity:** Major

**Why this matters:** The command references "Task tool" which is not a standard Claude Code tool. This creates confusion about what action Claude should take. The instructions should directly tell Claude what to do, not reference non-existent tools.

**Proposed fix:**

Replace vague tool reference with direct, actionable instructions:

    ## Instructions

    Invoke the skill-auditor agent (located at plugins/meta/meta-claude/agents/skill-auditor.md) to perform comprehensive analysis:

    1. Read the skill at $ARGUMENTS
    2. Evaluate against official Claude Code specifications:
       - SKILL.md structure and organization
       - Frontmatter quality and completeness
       - Progressive disclosure patterns
       - Content clarity and usefulness
       - Adherence to best practices
    3. Generate a detailed audit report with specific recommendations

---

### VIOLATION #3: Command Content Quality - Third-person perspective instead of Claude-directed

**Current:**

    Run comprehensive skill audit using skill-auditor agent (non-blocking).

**Standard violated:** Instructions must be written from Claude's perspective, addressing Claude directly ("You should...", "Your task is..."), not third-person description (slash-commands.md lines 148-149, 205-206)

**Severity:** Major

**Why this matters:** Commands should directly instruct Claude on what to do, not describe what the command does. Third-person descriptions reduce clarity and effectiveness.

**Proposed fix:**

Rewrite first line to address Claude directly:

    # Skill Validate Audit

    Your task is to run a comprehensive skill audit using the skill-auditor agent (non-blocking validation).

---

### VIOLATION #4: Argument Handling - Missing argument-hint frontmatter

**Current:**

No frontmatter present in the command file.

**Standard violated:** When a command expects arguments, the `argument-hint` frontmatter field should be present to show users what arguments are expected (slash-commands.md line 179, examples at lines 189, 201)

**Severity:** Minor

**Why this matters:** Without `argument-hint`, users won't see autocomplete hints when typing the command. This makes the command less discoverable and harder to use correctly.

**Proposed fix:**

Add frontmatter with argument hint:

    ---
    argument-hint: [skill-path]
    description: Run comprehensive skill audit using skill-auditor agent (non-blocking)
    ---

---

### VIOLATION #5: SlashCommand Tool Compatibility - Missing description frontmatter for tool discoverability

**Current:**

No frontmatter present in the command file.

**Standard violated:** Commands should have a `description` frontmatter field for SlashCommand tool discoverability (slash-commands.md line 346)

**Severity:** Minor

**Why this matters:** Without a `description` field, the command won't be available via the SlashCommand tool, limiting Claude's ability to invoke it programmatically when appropriate.

**Proposed fix:**

Add frontmatter with description:

    ---
    argument-hint: [skill-path]
    description: Run comprehensive skill audit using skill-auditor agent (non-blocking)
    ---

---

## Summary

**Total violations found:** 5

**Breakdown by Severity:**

- Critical: 0 (blocks functionality)
- Major: 3 (significantly impacts usability)
- Minor: 2 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 0
- YAML Frontmatter: 0
- Markdown Content: 0
- Argument Handling: 2
- Bash Execution: 0
- File References: 0
- Command Content Quality: 2
- Design Principles: 0
- SlashCommand Tool Compatibility: 1

**Overall Assessment:** WARNINGS

- **PASS**: No critical or major violations
- **FAIL**: One or more critical violations present
- **WARNINGS**: Major violations but no critical issues ✓

---

## Recommendations

### Critical Actions (Must Fix)

None.

### Major Actions (Should Fix)

1. **Fix argument handling (Violation #1)**: Add `$ARGUMENTS` placeholder in the Instructions section to capture the skill path argument. Without this, the command cannot access the user-provided skill path.

2. **Clarify instructions and remove Task tool reference (Violation #2)**: Replace the vague "Use the Task tool" instruction with direct, actionable steps telling Claude exactly what to do. The Task tool is not a standard Claude Code tool.

3. **Rewrite in Claude-directed perspective (Violation #3)**: Change the first line from third-person description to second-person instructions addressing Claude directly.

### Minor Actions (Nice to Have)

1. **Add frontmatter with argument-hint (Violation #4)**: Include `argument-hint: [skill-path]` in frontmatter to provide autocomplete hints for users.

2. **Add frontmatter with description (Violation #5)**: Include `description` field in frontmatter to enable SlashCommand tool discoverability.

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
