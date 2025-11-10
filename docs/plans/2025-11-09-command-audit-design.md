# Slash Command Audit System Design

**Date:** 2025-11-09

**Component Type:** Slash Command

**Location:** `plugins/meta/meta-claude/commands/audit-command.md`

## Purpose

Validate slash commands against comprehensive standards covering technical compliance, quality practices, and architectural principles. The audit produces detailed reports with violations, explanations, and actionable fixes.

## Architecture Decision

The multi-agent-composition decision framework determined this component should be a slash command:

- **Manual invocation:** User runs `/audit-command [path]` when needed
- **No parallelization:** Single command audit at a time
- **No external integration:** Internal standards checking only
- **Repeatable but not automatic:** Pattern suggests slash command, not skill

Integration into the meta-claude plugin positions this tool alongside command-creator, skill-creator, and agent-creator as part of the component creation and validation ecosystem.

## Command Structure

```markdown
---
description: Audit slash command compliance and adherence to standards
argument-hint: [slash-command-file-path]
allowed-tools: Read, Grep
---
```

**Invocation:** `/audit-command .claude/commands/my-command.md`

**Input:** Single file path to slash command

**Output:** Detailed report displayed in conversation (user can `/export` to save)

## Audit Categories

### Technical Compliance

**Frontmatter validation:**
- Valid YAML syntax
- Required field: `description` present and non-empty
- Optional fields properly formatted: `allowed-tools`, `model`, `argument-hint`, `disable-model-invocation`
- No invalid/unknown frontmatter fields

**Markdown format:**
- Valid markdown structure
- Proper heading hierarchy
- Code blocks specify language (CLAUDE.md requirement)
- Blank lines around code blocks and lists

**Syntax features:**
- File references use `@` syntax correctly
- Bash execution uses `!` prefix with backticks
- Argument placeholders valid: `$ARGUMENTS` or `$1`, `$2`, etc.
- Bash execution permissions match `allowed-tools`

### Quality Practices

**Description quality:**
- Clear and descriptive (not just filename)
- Explains command purpose
- Under 100 characters (appears in `/help`)

**Instruction clarity:**
- Clear, unambiguous instructions
- Structured with sections/steps
- Expected output format specified
- Written from Claude's perspective

**Tool permission hygiene:**
- `allowed-tools` grants only necessary permissions
- Permissions match actual command usage
- Not overly permissive

**File reference validation:**
- Static `@` file references point to existing files
- Paths resolve correctly

**Documentation completeness:**
- Examples provided for complex commands
- Argument usage explained for positional parameters

### Architectural Standards

**Design principles:**
- Single, clear purpose
- KISS principle (not over-engineered)
- YAGNI principle (no unnecessary features)

These checks validate the slash command follows good design principles without questioning whether it should be a different component type.

## Report Structure

```bash
# Slash Command Audit Report

Command: my-command.md
Path: .claude/commands/my-command.md
Date: 2025-11-09 03:45:00

---

## Summary

✓ Passed: 12 checks
✗ Failed: 3 checks
⚠ Warnings: 1 check

Overall: FAIL

---

## Technical Compliance

✓ Valid YAML frontmatter syntax
✗ Missing required 'description' field
  └─ Why: Every command must have a description field that appears in /help output
  └─ Fix: Add to frontmatter:
      ---
      description: Brief description of what this command does
      ---
  └─ Reference: slash-commands.md line 186

✓ Valid markdown structure
✗ Code blocks missing language specification
  └─ Why: CLAUDE.md requires all fenced code blocks to have a language specified
  └─ Fix: Change ```  to ```bash or ```markdown or appropriate language
  └─ Reference: CLAUDE.md line 3

---

## Quality Practices

✓ Description is clear and under 100 characters
✗ Instructions lack structure
  └─ Why: Instructions should be organized with clear sections/steps for Claude to follow
  └─ Fix: Add sections like:
      ## Process
      1. First step
      2. Second step

      ## Output Format
      Describe expected output
  └─ Reference: command-creator SKILL.md lines 64-82

✓ Tool permission hygiene (permissions match usage)
✓ File references valid (@paths exist)

---

## Architectural Standards

✓ Single, clear purpose
✓ Follows KISS principle
✗ Violates YAGNI - includes unnecessary features
  └─ Why: Command includes features/options that aren't needed for stated purpose
  └─ Fix: Remove unused options/features, keep only what's necessary
  └─ Reference: ai_docs/continuous-improvement/rules.md line 17

---

## Recommendations

Priority Actions:
1. [CRITICAL] Add required 'description' field to frontmatter
2. [CRITICAL] Specify language for all code blocks
3. [IMPORTANT] Add structure to instructions (sections/steps)
4. [IMPORTANT] Remove unnecessary features (YAGNI violation)
5. [OPTIONAL] Add examples section for better clarity
```

Each failure includes:
- **What:** Specific violation
- **Why:** Explanation of the requirement
- **Fix:** Actionable steps to correct
- **Reference:** Source documentation with line numbers

## Error Handling

**File not found:**
`Error: File not found at [path]. Check path and try again.`

**Invalid markdown:**
`Error: Markdown parsing failed at line X: [error details]`

**Unparseable frontmatter:**
`Error: YAML parsing failed: [error] at line X`

**Permission denied:**
`Error: Cannot read file at [path]. Permission denied.`

The audit completes fully even when some checks fail, reporting all findings in a single comprehensive output.

## Implementation Approach

1. Read command file using Read tool
2. Parse frontmatter (YAML) and markdown body
3. Run technical compliance checks
4. Run quality practice checks
5. Run architectural standard checks
6. Count passed/failed/warning checks
7. Format report with violations, explanations, and fixes
8. Display report in conversation

All validation rules, best practices, and standards are embedded directly in the command markdown. The command references official documentation (slash-commands.md, command-creator SKILL.md, rules.md, CLAUDE.md) with specific line numbers for traceability.

## Standards Source

All standards are hardcoded in the command file, organized into three categories (technical, quality, architectural). This keeps the command self-contained and ensures reliable operation without external dependencies.

The command works standalone once created, requiring only the Read tool to audit target commands.
