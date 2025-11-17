# Skill Validate Runtime

Test skill by attempting to load it in Claude Code context (runtime validation).

## Usage

```bash
/skill-validate-runtime <skill-path>
```

## What This Does

Validates that the skill actually loads and functions in Claude Code runtime:

- **Syntax Check:** Verifies SKILL.md markdown syntax is valid
- **Frontmatter Parsing:** Ensures YAML frontmatter parses correctly
- **Description Triggering:** Tests if description would trigger the skill
  appropriately
- **Progressive Disclosure:** Confirms skill content loads without errors
- **Context Loading:** Verifies skill can be loaded into Claude's context

**Note:** This is runtime validation - it tests actual loading behavior,
not just static analysis.

## Instructions

Perform runtime validation checks on the skill at the provided path.

### Step 1: Verify Skill Structure

Check that the skill directory contains a valid SKILL.md file:

```bash
test -f <skill-path>/SKILL.md && echo "SKILL.md exists" || \
  echo "Error: SKILL.md not found"
```

If SKILL.md does not exist, report error and exit.

### Step 2: Validate Markdown Syntax

Read the SKILL.md file and check for markdown syntax issues:

- Verify all code blocks are properly fenced with language identifiers
- Check for balanced heading levels (no missing hierarchy)
- Ensure lists are properly formatted
- Look for malformed markdown that could break rendering

**Common syntax issues to detect:**

- Unclosed code blocks (odd number of triple backticks)
- Code blocks without language specifiers
- Broken links with malformed syntax
- Improperly nested lists
- Invalid YAML frontmatter structure

### Step 3: Parse Frontmatter

Extract and parse the YAML frontmatter block:

```yaml
---
name: skill-name
description: Skill description text
---
```

**Validation checks:**

- Frontmatter block exists and is properly delimited with `---`
- YAML syntax is valid (no parsing errors)
- Required fields present: `name`, `description`
- Field values are non-empty strings
- No special characters that could break parsing

### Step 4: Test Description Triggering

Evaluate whether the skill description would trigger appropriately:

**Check for:**

- Description is specific enough to trigger the skill (not too broad)
- Description is general enough to be useful (not too narrow)
- Description clearly indicates when to use the skill
- Description uses action-oriented language
- No misleading or ambiguous phrasing

**Example good descriptions:**

- "Deploy applications to Kubernetes clusters using Helm charts"
- "Analyze Docker container security and generate compliance reports"

**Example poor descriptions:**

- "General Kubernetes tasks" (too broad)
- "Deploy myapp version 2.3.1 to production cluster" (too narrow)
- "Kubernetes" (unclear when to trigger)

### Step 5: Verify Progressive Disclosure

Check that the skill content follows progressive disclosure principles:

**Key aspects:**

- Essential information is presented first
- Content is organized in logical sections
- Detailed information is nested under appropriate headings
- Examples and advanced usage are clearly separated
- Skill doesn't front-load unnecessary details

**Warning signs:**

- Giant wall of text at the top
- No clear section structure
- Examples mixed with core instructions
- Edge cases presented before main workflow
- Overwhelming amount of information at once

### Step 6: Test Context Loading

Simulate loading the skill content to verify it would work in Claude's context:

**Checks:**

- Total skill content size is reasonable (not exceeding token limits)
- Content can be parsed and structured properly
- No circular references or broken internal links
- Skill references only valid tools/commands
- File paths and code examples are well-formed

### Generate Runtime Test Report

Create a structured report with the following format:

```text
## Runtime Validation Report: <skill-name>

**Overall Status:** PASS | FAIL

### Summary

[1-2 sentence overview of runtime validation results]

### Test Results

- Markdown Syntax: PASS | FAIL
- Frontmatter Parsing: PASS | FAIL
- Description Triggering: PASS | FAIL
- Progressive Disclosure: PASS | FAIL
- Context Loading: PASS | FAIL

### Issues Found

#### Critical (Must Fix)
[Issues that prevent skill from loading]
- [ ] Issue description with specific location

#### Warning (Should Fix)
[Issues that could cause problems]
- [ ] Issue description with specific location

#### Info (Consider Fixing)
[Minor issues or suggestions]
- [ ] Issue description

### Details

[Specific details about each test, including:]
- File size: X KB
- Frontmatter fields: name, description, [other fields]
- Content sections: [list of main sections]
- Code blocks: [count and languages]

### Recommendations

[Specific, actionable suggestions for fixing issues]
```

## Error Handling

**If SKILL.md not found:**

```text
Error: SKILL.md not found at <skill-path>
```

Action: Verify path is correct or run `/skill-create` first

**If runtime validation passes:**

- Report: "Runtime Validation: PASS"
- Show test results summary
- Note any info-level suggestions
- Exit with success

**If runtime validation fails:**

- Report: "Runtime Validation: FAIL"
- List all issues categorized by severity
- Provide specific fix recommendations
- Exit with failure

**Issue Severity Levels:**

- **Critical:** Skill cannot load (syntax errors, invalid YAML, missing
  required fields)
- **Warning:** Skill loads but may have problems (poor description, unclear structure)
- **Info:** Skill works but could be improved (minor formatting, suggestions)

## Pass Criteria

Runtime validation PASSES if:

- All critical tests pass (syntax, frontmatter, context loading)
- No critical issues found
- Skill can be loaded into Claude's context without errors

Runtime validation FAILS if:

- Any critical test fails
- Skill cannot be loaded due to syntax or parsing errors
- Description is fundamentally unusable for triggering
- Content structure breaks progressive disclosure

## Examples

**Valid skill with good runtime characteristics:**

```bash
/skill-validate-runtime plugins/meta/meta-claude/skills/skill-creator
# Output: Runtime Validation: PASS
# - All syntax checks passed
# - Frontmatter parsed successfully
# - Description triggers appropriately
# - Progressive disclosure structure confirmed
# - Skill loads into context successfully
```

**Skill with runtime issues:**

```bash
/skill-validate-runtime /path/to/broken-skill
# Output: Runtime Validation: FAIL
#
# Issues Found:
# Critical:
# - YAML frontmatter has syntax error on line 3 (unclosed string)
# - Code block at line 47 is unclosed (missing closing backticks)
# Warning:
# - Description is too broad: "General development tasks"
# - Progressive disclosure violated: 200 lines before first heading
```

**Skill with minor warnings:**

```bash
/skill-validate-runtime /path/to/working-skill
# Output: Runtime Validation: PASS
#
# Info:
# - Consider adding language identifier to code block at line 89
# - Description could be more specific about trigger conditions
```

## Notes

- This validation tests **runtime behavior**, not just static compliance
- Focus on whether the skill actually loads and functions in Claude Code
- Unlike `/skill-review-compliance` (static validation), this tests live
  loading
- Runtime validation should be run after compliance validation passes
- Tests simulate how Claude Code will interact with the skill at runtime
- Check for issues that only appear when trying to load the skill
