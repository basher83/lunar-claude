<!-- markdownlint-disable MD052 MD041 -->

# Slash Command Standards Compliance Review

**File:** plugins/meta/meta-claude/commands/skill/validate-integration.md
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

### VIOLATION #1: Bash Execution - Missing allowed-tools frontmatter

**Current:**

```markdown
# Skill Validate Integration

Test skill integration with Claude Code ecosystem (conflict detection and compatibility).
```

(No frontmatter present)

**Standard violated:** Bash command execution requires `allowed-tools: Bash(pattern:*)` in frontmatter (slash-commands.md lines 130, 136)

**Severity:** Critical

**Why this matters:** The command contains bash execution examples (lines 31-34, 64-66, 133-135) but lacks the required `allowed-tools` frontmatter field. Without this permission, Claude cannot execute the bash commands shown in the instructions, preventing the command from functioning as designed.

**Proposed fix:**

Add frontmatter with bash permissions:

```markdown
---
allowed-tools: Bash(test:*), Bash(find:*), Bash(git:*)
description: Test skill integration with Claude Code ecosystem (conflict detection and compatibility)
---
```

---

### VIOLATION #2: Argument Handling - Invalid argument placeholder syntax

**Current:**

```markdown
/meta-claude:skill:validate-integration <skill-path>
```

(Line 8)

**Standard violated:** Only `$ARGUMENTS` and `$1`, `$2`, etc. are recognized argument placeholders (slash-commands.md lines 96-126)

**Severity:** Critical

**Why this matters:** The command uses `<skill-path>` placeholder syntax which is not recognized by Claude Code's argument substitution system. This will cause the argument to not be passed correctly to the command, breaking functionality.

**Proposed fix:**

Use valid placeholder:

```markdown
/meta-claude:skill:validate-integration $1
```

Then add to frontmatter:

```yaml
argument-hint: [skill-path]
```

---

### VIOLATION #3: Argument Handling - Invalid placeholder in instructions

**Current:**

```bash
test -f <skill-path>/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```

(Lines 31-33)

**Standard violated:** Only `$ARGUMENTS` and `$1`, `$2`, etc. are recognized argument placeholders (slash-commands.md lines 96-126)

**Severity:** Critical

**Why this matters:** The instructions use `<skill-path>` throughout (lines 32, 98, 134, 245-248) instead of valid placeholders like `$1`. Claude will not substitute these with actual argument values, causing all commands to fail.

**Proposed fix:**

Replace all instances of `<skill-path>` with `$1`:

```bash
test -f $1/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```

---

### VIOLATION #4: Markdown Content - Missing language on code blocks

**Current:**

```text
Check that the skill directory contains a valid SKILL.md file:

```

test -f <skill-path>/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```bash
```

(Lines 29-34)

**Standard violated:** CLAUDE.md requirement "Fenced code blocks MUST have a language specified"

**Severity:** Minor

**Why this matters:** Code blocks without language specifications lack syntax highlighting and may not render properly in some markdown parsers. This affects readability and user experience.

**Proposed fix:**

Add language to all code blocks. Found violations at lines:
- Line 31: Add `bash` language
- Line 63: Add `bash` language
- Line 133: Add `bash` language
- Line 245: Add `text` language
- Line 296: Add `bash` language
- Line 307: Add `bash` language
- Line 320: Add `bash` language
- Line 334: Add `bash` language

Example fix for line 31:

```markdown
Check that the skill directory contains a valid SKILL.md file:

```bash
test -f $1/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```

```text

---

### VIOLATION #5: Bash Execution - Missing inline execution syntax

**Current:**

```bash
test -f <skill-path>/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```

(Lines 31-33)

**Standard violated:** Bash command execution requires `!` prefix for inline execution: `` !`command` `` (slash-commands.md lines 129-150)

**Severity:** Major

**Why this matters:** The command shows bash examples as code blocks (lines 31-34, 64-66, 133-135) but they appear to be intended as examples for Claude to execute, not just documentation. If these are meant to execute during command invocation, they need the `!` prefix. If they're just examples, this is a documentation clarity issue.

**Proposed fix:**

If bash commands should execute during command invocation, use inline execution:

```markdown
Check that the skill directory contains a valid SKILL.md file:

!`test -f $1/SKILL.md && echo "SKILL.md exists" || echo "Error: SKILL.md not found"`
```

If they're just examples for documentation, clarify this is example syntax:

```markdown
**Example validation:**

```bash
test -f $1/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```
```text

---

### VIOLATION #6: Command Content Quality - Third-person perspective

**Current:**

```markdown
## Instructions

Perform integration validation checks on the skill at the provided path.

### Step 1: Verify Skill Exists

Check that the skill directory contains a valid SKILL.md file:
```

(Lines 23-29)

**Standard violated:** Instructions should be written from Claude's perspective using direct address (slash-commands.md lines 148-149, 205-206)

**Severity:** Major

**Why this matters:** The command uses third-person imperative ("Perform validation checks", "Check that the skill...") rather than direct address to Claude. This is less clear than Claude-directed instructions and doesn't follow the official pattern for slash commands.

**Proposed fix:**

Rewrite in Claude-directed perspective:

```markdown
## Instructions

Your task is to perform integration validation checks on the skill at the provided path.

### Step 1: Verify Skill Exists

Verify that the skill directory contains a valid SKILL.md file:
```

Apply this pattern throughout:
- "Perform" → "Your task is to perform"
- "Check that" → "Verify that"
- "Create a structured report" → "Your task is to create a structured report"
- "Extract" → "Extract" (already imperative, acceptable)

---

### VIOLATION #7: SlashCommand Tool Compatibility - Missing description field

**Current:**

```markdown
# Skill Validate Integration

Test skill integration with Claude Code ecosystem (conflict detection and compatibility).
```

(No frontmatter)

**Standard violated:** SlashCommand tool requires `description` frontmatter field for command discoverability (slash-commands.md line 346)

**Severity:** Minor

**Why this matters:** Without a frontmatter `description` field, the command won't be available for Claude to invoke programmatically via the SlashCommand tool. The command will still work when invoked manually, but lacks programmatic discoverability. The description defaults to the first line, but explicit frontmatter is best practice for tool compatibility.

**Proposed fix:**

Add frontmatter with description:

```markdown
---
allowed-tools: Bash(test:*), Bash(find:*), Bash(git:*)
description: Test skill integration with Claude Code ecosystem (conflict detection and compatibility)
argument-hint: [skill-path]
---
```

---

### VIOLATION #8: Argument Handling - Missing positional argument documentation

**Current:**

```markdown
## Usage

```bash
/meta-claude:skill:validate-integration <skill-path>
```
```text

(Lines 5-9)

**Standard violated:** Positional arguments should be documented so users know argument order and meaning (slash-commands.md lines 109-126)

**Severity:** Major

**Why this matters:** The command uses a positional argument but doesn't explain what `skill-path` should be (absolute path? relative? directory or file?). Users need clear guidance on what to pass.

**Proposed fix:**

Add argument documentation:

```markdown
## Usage

```bash
/meta-claude:skill:validate-integration [skill-path]
```

**Arguments:**

- `skill-path`: Path to the skill directory to validate (can be absolute or relative)

**Example:**

```bash
/meta-claude:skill:validate-integration plugins/meta/meta-claude/skills/docker-security
```
```

---

## Summary

**Total violations found:** 8

**Breakdown by Severity:**

- Critical: 3 (blocks functionality)
- Major: 3 (significantly impacts usability)
- Minor: 2 (improvement opportunities)

**Breakdown by Category:**

- File Structure & Location: 0
- YAML Frontmatter: 1
- Markdown Content: 1
- Argument Handling: 3
- Bash Execution: 2
- File References: 0
- Command Content Quality: 1
- Design Principles: 0
- SlashCommand Tool Compatibility: 1

**Overall Assessment:** FAIL

- **FAIL**: Three critical violations present
  1. Missing required `allowed-tools` frontmatter for bash execution
  2. Invalid argument placeholder syntax in usage example
  3. Invalid argument placeholders throughout instructions

---

## Recommendations

### Critical Actions (Must Fix)

1. **Fix Violation #1**: Add frontmatter with required bash permissions
   ```yaml
   ---
   allowed-tools: Bash(test:*), Bash(find:*), Bash(git:*)
   description: Test skill integration with Claude Code ecosystem (conflict detection and compatibility)
   argument-hint: [skill-path]
   ---
   ```

2. **Fix Violation #2**: Replace `<skill-path>` with `$1` in usage example (line 8)

3. **Fix Violation #3**: Replace all `<skill-path>` instances with `$1` throughout instructions (lines 32, 98, 134, 245-248)

### Major Actions (Should Fix)

4. **Fix Violation #5**: Clarify bash execution intent - use `!` prefix for inline execution or clearly mark as example syntax

5. **Fix Violation #6**: Rewrite instructions in Claude-directed perspective ("Your task is to...", "Verify that...")

6. **Fix Violation #8**: Add argument documentation explaining what `skill-path` parameter expects

### Minor Actions (Nice to Have)

7. **Fix Violation #4**: Add language specifications to all code blocks (8 instances found)

8. **Fix Violation #7**: Add explicit frontmatter `description` field for SlashCommand tool compatibility (already addressed in Critical Action #1)

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
