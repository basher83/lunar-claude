<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/validate-runtime.md
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

### VIOLATION #1: File Structure - Missing frontmatter entirely

**Current:**

```markdown
# Skill Validate Runtime

Test skill by attempting to load it in Claude Code context (runtime validation).
```

**Standard violated:** While frontmatter is optional (slash-commands.md line 173), best practice recommends including `description` field for SlashCommand tool discoverability (slash-commands.md line 346 "Have description frontmatter field populated")

**Severity:** Minor

**Why this matters:** Without a `description` frontmatter field, this command will not be available via the SlashCommand tool. Claude cannot invoke this command programmatically. The command will only work with manual `/` invocation.

**Proposed fix:**

```markdown
---
description: Test skill by attempting to load it in Claude Code context (runtime validation)
---

# Skill Validate Runtime

Test skill by attempting to load it in Claude Code context (runtime validation).
```

---

### VIOLATION #2: Argument Handling - Missing argument-hint frontmatter

**Current:**

The command shows usage `<skill-path>` parameter but has no `argument-hint` frontmatter field.

**Standard violated:** Best practice recommends `argument-hint` frontmatter for commands that accept arguments (slash-commands.md line 179)

**Severity:** Minor

**Why this matters:** Without `argument-hint`, users won't see the expected argument format when auto-completing the slash command. The hint provides inline documentation about what arguments the command expects.

**Proposed fix:**

Add to frontmatter:

    ---
    description: Test skill by attempting to load it in Claude Code context (runtime validation)
    argument-hint: [skill-path]
    ---

---

### VIOLATION #3: Argument Handling - No documentation of positional argument

**Current:**

The command usage shows `<skill-path>` but there is no explanation in the command content that this argument should be referenced as `$ARGUMENTS` or `$1` in the instructions.

**Standard violated:** When using arguments, the command must document how to access them (slash-commands.md lines 96-126, specifically 109-126 for positional arguments)

**Severity:** Major

**Why this matters:** The command shows it expects an argument in the Usage section, but never tells Claude how to use that argument. The instructions say "at the provided path" but don't use `$ARGUMENTS` or `$1` placeholder to actually access the path value. This makes the argument handling ambiguous.

**Proposed fix:**

Update line 27 to use proper argument placeholder:

    ## Instructions

    Perform runtime validation checks on the skill at $ARGUMENTS.

Or use `$1` consistently throughout the command:

    ### Step 1: Verify Skill Structure

    Check that the skill directory contains a valid SKILL.md file:

    ```bash
    test -f $1/SKILL.md && echo "SKILL.md exists" || \
      echo "Error: SKILL.md not found"
    ```

---

### VIOLATION #4: Argument Handling - Invalid placeholder syntax in bash examples

**Current:**

Lines 34-36 use `<skill-path>`:

    ```bash
    test -f <skill-path>/SKILL.md && echo "SKILL.md exists" || \
      echo "Error: SKILL.md not found"
    ```

Lines 183-184 use `<skill-path>`:

    ```text
    Error: SKILL.md not found at <skill-path>
    ```

**Standard violated:** Must use valid argument placeholders (`$ARGUMENTS`, `$1`, `$2`, etc.), not custom syntax like `<skill-path>` (slash-commands.md lines 96-126)

**Severity:** Critical

**Why this matters:** `<skill-path>` is not a recognized argument placeholder. Claude will not substitute this with the actual argument value. The command will fail when executed because the literal string `<skill-path>` will be used instead of the user's provided path.

**Proposed fix:**

Replace all instances of `<skill-path>` with proper placeholder:

    test -f $ARGUMENTS/SKILL.md && echo "SKILL.md exists" || \
      echo "Error: SKILL.md not found"

    Error: SKILL.md not found at $ARGUMENTS

---

### VIOLATION #5: Command Content Quality - Instructions not written from Claude's perspective

**Current:**

Line 27:

    Perform runtime validation checks on the skill at the provided path.

Throughout the command (lines 29, 40, 57, 76, 100, 119, 131) uses imperative mood:

    ### Step 1: Verify Skill Structure
    ### Step 2: Validate Markdown Syntax
    ### Step 3: Parse Frontmatter
    ### Step 4: Test Description Triggering
    ### Step 5: Verify Progressive Disclosure
    ### Step 6: Test Context Loading
    ### Generate Runtime Test Report

**Standard violated:** Instructions should be written from Claude's perspective, addressing Claude directly (slash-commands.md lines 148-149, 205-206 showing "Your task is...")

**Severity:** Major

**Why this matters:** The command uses imperative mood as if giving orders to a tool, rather than collaborative instructions for Claude. This is less clear and doesn't follow the standard pattern of framing commands as Claude's task.

**Proposed fix:**

    ## Instructions

    Your task is to perform runtime validation checks on the skill at $ARGUMENTS.

    ### Step 1: Verify Skill Structure

    Check that the skill directory contains a valid SKILL.md file:

Alternative more Claude-directed framing:

    ## Your Task

    You will perform runtime validation checks on the skill at $ARGUMENTS. Follow these steps:

    ### 1. Verify Skill Structure

    First, check that the skill directory contains a valid SKILL.md file:

---

### VIOLATION #6: Markdown Content - Code blocks without language specified

**Current:**

Line 135 uses `text`:

    ```text
    ## Runtime Validation Report: <skill-name>
    ```

Lines 183, 229, 241, 256 all use `text` for output examples.

**Standard violated:** CLAUDE.md requirement "Fenced code blocks MUST have a language specified"

**Severity:** Minor

**Why this matters:** While `text` is technically a language specifier, the standard examples in slash-commands.md use proper language identifiers like `bash`, `markdown`, `yaml`. Using `text` is functional but doesn't follow the pattern shown in official examples which use specific languages.

**Proposed fix:**

For command examples showing bash output, use `bash`. For examples showing error messages or generic output, use `plaintext`. Or keep as `text` (this is actually valid and acceptable, so this violation could be downgraded to informational or removed).

---

## Summary

**Total violations found:** 6

**Breakdown by Severity:**

- Critical: 1 (blocks functionality)
- Major: 2 (significantly impacts usability)
- Minor: 3 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 1
- YAML Frontmatter: 0
- Markdown Content: 1
- Argument Handling: 3
- Bash Execution: 0
- File References: 0
- Command Content Quality: 1
- Design Principles: 0
- SlashCommand Tool Compatibility: 0

**Overall Assessment:** FAIL

- **FAIL**: One or more Critical violations present (invalid argument placeholder syntax)

---

## Recommendations

### Critical Actions (Must Fix)

1. **Fix argument placeholder syntax (Violation #4)**: Replace all instances of `<skill-path>` with valid placeholder `$ARGUMENTS` or `$1`. This is blocking functionality - the command will not work correctly until this is fixed.

### Major Actions (Should Fix)

1. **Document argument handling (Violation #3)**: Add clear documentation showing how to access the skill-path argument using `$ARGUMENTS` or `$1`. Update all references in the Instructions section to use the proper placeholder.

2. **Rewrite from Claude's perspective (Violation #5)**: Change imperative instructions ("Perform runtime validation...") to Claude-directed framing ("Your task is to...", "You will..."). This significantly improves clarity and follows official standards.

### Minor Actions (Nice to Have)

1. **Add frontmatter description (Violation #1)**: Include frontmatter with `description` field to enable SlashCommand tool discoverability. This allows Claude to invoke the command programmatically.

2. **Add argument-hint frontmatter (Violation #2)**: Include `argument-hint: [skill-path]` in frontmatter to provide inline documentation during auto-completion.

3. **Review code block language usage (Violation #6)**: Consider whether `text` is the most appropriate language identifier for output examples, or if `plaintext`, `bash`, or other identifiers would be more accurate. This is very minor and may not require action.

---
