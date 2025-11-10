# Slash Command Audit System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `/audit-command` to validate slash commands against technical, quality, and architectural standards.

**Architecture:** Self-contained slash command with embedded validation rules, produces detailed reports with violations and fixes.

**Tech Stack:** Markdown/YAML (command format), Read tool, Grep tool (optional)

**Design Reference:** `docs/plans/2025-11-09-command-audit-design.md`

---

## Task 1: Create Command File Structure

**Files:**
- Create: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Create command file with frontmatter**

```markdown
---
description: Audit slash command compliance and adherence to standards
argument-hint: [slash-command-file-path]
allowed-tools: Read, Grep
---

# Slash Command Audit

You are auditing a slash command for compliance with technical, quality, and architectural standards.

## Input

You will receive a file path via `$ARGUMENTS` pointing to a slash command file to audit.

## Process

Read the command file and validate against comprehensive standards.

## Next Steps

Following tasks will implement the validation logic.
```

**Step 2: Verify command appears**

Run: `/help` and search for `audit-command`
Expected: Command appears in list with description

**Step 3: Test basic invocation**

Run: `/audit-command plugins/meta/meta-claude/commands/audit-command.md`
Expected: Command executes (even if incomplete)

**Step 4: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git commit -m "feat: add audit-command slash command structure

- Create command file with frontmatter
- Add basic structure for validation
- Command appears in /help

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Implement Technical Compliance Validation

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Add technical compliance section**

Update the command file to include technical validation logic:

```markdown
---
description: Audit slash command compliance and adherence to standards
argument-hint: [slash-command-file-path]
allowed-tools: Read, Grep
---

# Slash Command Audit

You are auditing a slash command for compliance with technical, quality, and architectural standards.

## Input

You will receive a file path via `$ARGUMENTS` pointing to a slash command file to audit.

## Execution Process

### Step 1: Read the Command File

Use Read tool to load the file at `$ARGUMENTS`.

Handle errors:
- File not found: "Error: File not found at [path]. Check path and try again."
- Permission denied: "Error: Cannot read file at [path]. Permission denied."

### Step 2: Parse Frontmatter and Content

Extract:
- Frontmatter (YAML between `---` markers)
- Markdown body content

Handle errors:
- Invalid YAML: "Error: YAML parsing failed: [error] at line X"
- Invalid markdown: "Error: Markdown parsing failed at line X: [error details]"

### Step 3: Run Technical Compliance Checks

**Frontmatter Validation:**

1. **Valid YAML syntax**
   - Check frontmatter parses without errors
   - Pass: ✓ Valid YAML frontmatter syntax
   - Fail: ✗ Invalid YAML syntax
     - Why: Frontmatter must be valid YAML between --- markers
     - Fix: Correct YAML syntax errors
     - Reference: slash-commands.md line 181

2. **Required 'description' field**
   - Check frontmatter contains `description:` key with non-empty value
   - Pass: ✓ Required 'description' field present
   - Fail: ✗ Missing required 'description' field
     - Why: Every command must have a description field that appears in /help output
     - Fix: Add to frontmatter:
       ```yaml
       ---
       description: Brief description of what this command does
       ---
       ```
     - Reference: slash-commands.md line 186

3. **Optional fields properly formatted**
   - If present, validate: `allowed-tools`, `model`, `argument-hint`, `disable-model-invocation`
   - Check types and format
   - Pass: ✓ Optional fields properly formatted
   - Fail: ✗ Invalid optional field format: [field name]
     - Why: Optional fields must follow correct format and types
     - Fix: See slash-commands.md lines 185-191 for field specifications
     - Reference: slash-commands.md line 185

4. **No invalid/unknown frontmatter fields**
   - Check for fields not in specification
   - Pass: ✓ No unknown frontmatter fields
   - Warn: ⚠ Unknown frontmatter field: [field name]
     - Why: Unknown fields may indicate typos or misunderstanding
     - Fix: Remove unknown field or check documentation for correct name
     - Reference: slash-commands.md line 181

**Markdown Format Validation:**

5. **Valid markdown structure**
   - Check markdown parses without errors
   - Check heading hierarchy (no skipping levels)
   - Pass: ✓ Valid markdown structure
   - Fail: ✗ Invalid markdown structure
     - Why: Proper markdown structure ensures readability
     - Fix: Correct markdown syntax errors
     - Reference: slash-commands.md

6. **Code blocks have language specified**
   - Find all fenced code blocks (```)
   - Check each has language identifier
   - Pass: ✓ All code blocks specify language
   - Fail: ✗ Code blocks missing language specification
     - Why: CLAUDE.md requires all fenced code blocks to have a language specified
     - Fix: Change ``` to ```bash or ```markdown or appropriate language
     - Reference: CLAUDE.md line 3

7. **Blank lines around code blocks and lists**
   - Check code blocks surrounded by blank lines
   - Check lists surrounded by blank lines
   - Pass: ✓ Proper blank lines around code blocks and lists
   - Fail: ✗ Missing blank lines around code blocks or lists
     - Why: CLAUDE.md requires blank lines for proper formatting
     - Fix: Add blank lines before and after code blocks and lists
     - Reference: CLAUDE.md line 4

**Syntax Features Validation:**

8. **File references use @ syntax correctly**
   - Find patterns like `@path/to/file`
   - Check syntax is valid
   - Pass: ✓ File reference syntax correct
   - Fail: ✗ Invalid file reference syntax
     - Why: File references must use @ prefix for Claude to recognize them
     - Fix: Use @path/to/file format for file references
     - Reference: slash-commands.md line 161

9. **Bash execution uses ! prefix correctly**
   - Find bash execution patterns `!`command``
   - Check syntax: backticks and ! prefix
   - Pass: ✓ Bash execution syntax correct
   - Fail: ✗ Invalid bash execution syntax
     - Why: Bash commands must use !`command` format
     - Fix: Use !`command` format for bash execution
     - Reference: slash-commands.md line 139

10. **Argument placeholders are valid**
    - Find $ARGUMENTS or $1, $2, etc.
    - Check valid placeholder syntax
    - Pass: ✓ Valid argument placeholder syntax
    - Fail: ✗ Invalid argument placeholder: [placeholder]
      - Why: Only $ARGUMENTS or $1, $2, etc. are valid
      - Fix: Use $ARGUMENTS for all args or $1, $2 for positional
      - Reference: slash-commands.md line 103

11. **Bash execution permissions match allowed-tools**
    - If command uses !`bash command`, check frontmatter includes Bash in allowed-tools
    - Pass: ✓ Bash permissions match usage
    - Warn: ⚠ Bash execution without allowed-tools permission
      - Why: Command uses !`bash` but frontmatter doesn't include Bash in allowed-tools
      - Fix: Add to frontmatter: allowed-tools: Bash(command:*)
      - Reference: slash-commands.md line 139

## Next Steps

Following tasks will implement quality and architectural validation.
```

**Step 2: Test on sample command**

Create test file `.claude/commands/test-sample.md`:

```markdown
---
description: Test command for validation
---

Test command without code blocks or special features.
```

Run: `/audit-command .claude/commands/test-sample.md`
Expected: Technical compliance section shows results

**Step 3: Test with violations**

Create test file `.claude/commands/test-bad.md`:

```markdown
---
badfield: invalid
---

No description field.

Code block without language:
```
code here
```text

File reference: path/to/file (missing @)
```

Run: `/audit-command .claude/commands/test-bad.md`
Expected: Multiple violations detected and reported

**Step 4: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git add .claude/commands/test-*.md
git commit -m "feat: implement technical compliance validation

- Add frontmatter validation checks
- Add markdown format validation
- Add syntax feature validation
- Include detailed error messages with fixes
- Add test samples for validation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Implement Quality Practices Validation

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Add quality practices section**

Add after Technical Compliance section:

```markdown
### Step 4: Run Quality Practice Checks

**Description Quality:**

12. **Description is clear and descriptive**
    - Check description explains command purpose (not just filename)
    - Check description is informative
    - Pass: ✓ Description is clear and descriptive
    - Fail: ✗ Description unclear or not descriptive
      - Why: Description appears in /help and should clearly explain purpose
      - Fix: Revise description to explain what command does and when to use it
      - Reference: slash-commands.md line 186

13. **Description under 100 characters**
    - Check length of description field
    - Pass: ✓ Description under 100 characters
    - Warn: ⚠ Description exceeds 100 characters (currently: X chars)
      - Why: Long descriptions may be truncated in /help output
      - Fix: Shorten description to under 100 characters while keeping it clear
      - Reference: Best practice for /help display

**Instruction Clarity:**

14. **Instructions are clear and unambiguous**
    - Check for vague language ("handle this", "do that")
    - Check for clear action verbs
    - Pass: ✓ Instructions are clear and unambiguous
    - Fail: ✗ Instructions contain vague or ambiguous language
      - Why: Claude needs explicit instructions to execute correctly
      - Fix: Use specific action verbs and clear steps
      - Reference: command-creator SKILL.md line 89

15. **Instructions have structure (sections/steps)**
    - Check for headings, numbered lists, or clear organization
    - Pass: ✓ Instructions have clear structure
    - Fail: ✗ Instructions lack structure
      - Why: Structured instructions are easier for Claude to follow
      - Fix: Add sections like:
        ```markdown
        ## Process
        1. First step
        2. Second step

        ## Output Format
        Describe expected output
        ```
      - Reference: command-creator SKILL.md lines 64-82

16. **Expected output format specified**
    - Check if command describes what output should look like
    - Pass: ✓ Output format specified
    - Warn: ⚠ Output format not specified
      - Why: Clear output expectations help Claude provide consistent results
      - Fix: Add section describing expected output format
      - Reference: command-creator SKILL.md line 75

17. **Written from Claude's perspective**
    - Check instructions say "You should..." not "The user should..."
    - Pass: ✓ Written from Claude's perspective
    - Fail: ✗ Instructions not from Claude's perspective
      - Why: Instructions should tell Claude what to do, not describe user actions
      - Fix: Rewrite as instructions to Claude: "You should..." "Your task is..."
      - Reference: command-creator SKILL.md line 23

**Tool Permission Hygiene:**

18. **allowed-tools grants only necessary permissions**
    - Compare allowed-tools to actual tool usage in instructions
    - Check for overly permissive grants (e.g., Bash(*:*))
    - Pass: ✓ Tool permissions match usage
    - Fail: ✗ Overly permissive tool permissions
      - Why: Granting more permissions than needed violates least privilege
      - Fix: Restrict allowed-tools to only what command actually uses
      - Reference: Best practice - principle of least privilege

19. **Permissions match actual command usage**
    - Check if command uses tools not in allowed-tools
    - Pass: ✓ All used tools have permissions
    - Fail: ✗ Command uses tools without permission: [tool name]
      - Why: Command will fail if it tries to use unpermitted tools
      - Fix: Add missing tool to allowed-tools field
      - Reference: slash-commands.md line 185

**File Reference Validation:**

20. **Static @ file references point to existing files**
    - Extract all @path/to/file references from command body
    - Check if each referenced file exists
    - Pass: ✓ All file references valid (@paths exist)
    - Fail: ✗ File reference points to non-existent file: [path]
      - Why: Command will fail when invoked if referenced files don't exist
      - Fix: Create the referenced file or correct the path
      - Reference: slash-commands.md line 161

**Documentation Completeness:**

21. **Examples provided for complex commands**
    - If command uses multiple arguments or has complex usage, check for examples
    - Pass: ✓ Examples provided for complex command
    - Warn: ⚠ Complex command missing usage examples
      - Why: Examples help users understand how to invoke the command correctly
      - Fix: Add ## Examples section with sample invocations and expected behavior
      - Reference: command-creator SKILL.md line 79

22. **Argument usage explained for positional parameters**
    - If command uses $1, $2, etc., check for explanation
    - Pass: ✓ Positional argument usage explained
    - Warn: ⚠ Positional arguments not explained
      - Why: Users need to know what each argument represents
      - Fix: Document what each $1, $2, etc. parameter means
      - Reference: slash-commands.md line 119

## Next Steps

Following task will implement architectural standards validation.
```

**Step 2: Test quality checks**

Update `.claude/commands/test-bad.md` to include quality violations:

```markdown
---
description: test
---

Handle the thing.

Do it.
```

Run: `/audit-command .claude/commands/test-bad.md`
Expected: Quality violations detected (short description, vague instructions, no structure)

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git add .claude/commands/test-bad.md
git commit -m "feat: implement quality practices validation

- Add description quality checks
- Add instruction clarity checks
- Add tool permission hygiene validation
- Add file reference validation
- Add documentation completeness checks
- Include detailed recommendations for each violation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 4: Implement Architectural Standards Validation

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Add architectural standards section**

Add after Quality Practices section:

```markdown
### Step 5: Run Architectural Standard Checks

**Design Principles:**

23. **Single, clear purpose**
    - Check if command has one well-defined purpose
    - Check for multiple unrelated functions
    - Pass: ✓ Single, clear purpose
    - Fail: ✗ Command has multiple unrelated purposes
      - Why: Each command should do one thing well
      - Fix: Split into separate commands if doing multiple unrelated things
      - Reference: ai_docs/continuous-improvement/rules.md (KISS principle)

24. **Follows KISS principle (not over-engineered)**
    - Check for unnecessary complexity
    - Check for features that could be simpler
    - Pass: ✓ Follows KISS principle
    - Fail: ✗ Command is over-engineered
      - Why: Simplicity and reliability over cleverness
      - Fix: Simplify logic, remove unnecessary complexity
      - Reference: ai_docs/continuous-improvement/rules.md line 15

25. **Follows YAGNI principle (no unnecessary features)**
    - Check for unused options or features
    - Check for "just in case" functionality
    - Pass: ✓ Follows YAGNI principle
    - Fail: ✗ Violates YAGNI - includes unnecessary features
      - Why: Command includes features/options that aren't needed for stated purpose
      - Fix: Remove unused options/features, keep only what's necessary
      - Reference: ai_docs/continuous-improvement/rules.md line 17

## Next Steps

Following task will implement report generation.
```

**Step 2: Test architectural checks**

Update `.claude/commands/test-bad.md`:

```markdown
---
description: Test command that does everything
---

This command:
1. Creates files
2. Runs tests
3. Deploys to production
4. Sends emails
5. Makes coffee

It has options for:
- --verbose (unused)
- --dry-run (unused)
- --future-feature (not implemented yet)
```

Run: `/audit-command .claude/commands/test-bad.md`
Expected: Architectural violations detected (multiple purposes, YAGNI violation)

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git add .claude/commands/test-bad.md
git commit -m "feat: implement architectural standards validation

- Add single purpose check
- Add KISS principle validation
- Add YAGNI principle validation
- Include references to engineering rules

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 5: Implement Report Generation

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Add report generation section**

Add after all validation sections:

```markdown
### Step 6: Generate Report

Count results:
- Total checks: 25
- Passed: Count of ✓
- Failed: Count of ✗
- Warnings: Count of ⚠

Determine overall status:
- If any failures: FAIL
- If warnings but no failures: WARNINGS
- If all passed: PASS

Format output as:

```text
# Slash Command Audit Report

Command: [filename from path]
Path: [full path from $ARGUMENTS]
Date: [current timestamp]

---

## Summary

✓ Passed: X checks
✗ Failed: Y checks
⚠ Warnings: Z checks

Overall: [PASS/FAIL/WARNINGS]

---

## Technical Compliance

[For each technical check 1-11, show result]
[For failures/warnings, include Why/Fix/Reference]

---

## Quality Practices

[For each quality check 12-22, show result]
[For failures/warnings, include Why/Fix/Reference]

---

## Architectural Standards

[For each architectural check 23-25, show result]
[For failures/warnings, include Why/Fix/Reference]

---

## Recommendations

Priority Actions:
[List all failures as [CRITICAL]]
[List all warnings as [IMPORTANT] or [OPTIONAL] based on severity]

Format:
1. [CRITICAL] [Action from failure]
2. [IMPORTANT] [Action from warning]
3. [OPTIONAL] [Suggestion for improvement]
```

Display this report to the user.

## Complete Execution

You have now audited the slash command file and provided a comprehensive report with:
- All validation results
- Specific violations identified
- Clear explanations of why each is important
- Actionable fixes with examples
- References to source documentation
- Prioritized recommendations

The user can now review the report and address any issues found.
```text

**Step 2: Test report generation**

Run: `/audit-command .claude/commands/test-bad.md`
Expected: Complete formatted report with:
- Summary section with counts
- All three validation categories
- Detailed violations with why/fix/reference
- Prioritized recommendations

Run: `/audit-command .claude/commands/test-sample.md`
Expected: Clean report showing mostly passed checks

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git commit -m "feat: implement report generation and formatting

- Add check counting logic
- Add overall status determination
- Add formatted report structure
- Include summary, categories, and recommendations
- Complete audit command implementation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 6: Implement Error Handling

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md`

**Step 1: Enhance error handling section**

Update Step 1 (Read the Command File) to be more comprehensive:

```markdown
### Step 1: Read the Command File

Use Read tool to load the file at `$ARGUMENTS`.

**Error Handling:**

**File not found:**
- Error: "Error: File not found at [path]. Check path and try again."
- Suggest: Check if path is correct, verify file exists
- Exit: Do not continue with audit

**Permission denied:**
- Error: "Error: Cannot read file at [path]. Permission denied."
- Suggest: Check file permissions
- Exit: Do not continue with audit

**Empty file:**
- Warning: "Warning: File is empty. Nothing to audit."
- Suggest: Add content to command file
- Exit: Do not continue with audit

**Invalid markdown:**
- Error: "Error: Markdown parsing failed at line X: [error details]"
- Note: This will be caught during validation
- Continue: Proceed with audit, report in technical compliance section

**Unparseable frontmatter:**
- Error: "Error: YAML parsing failed: [error] at line X"
- Note: This will be caught during validation
- Continue: Proceed with audit, report in technical compliance section

**Always complete full audit:** Even if some checks fail, report all findings in a single comprehensive output.
```

**Step 2: Test error handling**

Test file not found:
```bash
/audit-command .claude/commands/does-not-exist.md
```
Expected: Clear error message about file not found

Test empty file:
```bash
touch .claude/commands/empty.md
/audit-command .claude/commands/empty.md
```
Expected: Warning about empty file

Test invalid YAML:
```bash
echo "---
broken: yaml: invalid
---" > .claude/commands/broken-yaml.md
/audit-command .claude/commands/broken-yaml.md
```
Expected: Report YAML parsing error in technical compliance

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git add .claude/commands/empty.md .claude/commands/broken-yaml.md
git commit -m "feat: enhance error handling for edge cases

- Add comprehensive error messages
- Handle file not found gracefully
- Handle permission denied
- Handle empty files
- Handle YAML/markdown parsing errors
- Always complete full audit even with errors

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 7: Create Comprehensive Test Suite

**Files:**
- Create: `.claude/commands/test-audit-good.md` (passing all checks)
- Create: `.claude/commands/test-audit-mixed.md` (some violations)
- Create: `.claude/commands/test-audit-bad.md` (many violations)

**Step 1: Create good command test**

```markdown
---
description: Well-formed test command with all best practices
argument-hint: [input-file]
allowed-tools: Read, Write
---

# Test Good Command

You are a test command that demonstrates all best practices for slash command creation.

## Process

1. Read the input file at `$1`
2. Process the content
3. Write output

## Input

The command accepts one argument: the path to a file.

## Output Format

Present results in markdown format with clear sections.

## Examples

```bash
/test-audit-good data.txt
```

Expected output: Processed data in markdown format.

## Implementation

Read file content using Read tool, then write formatted output using Write tool.
```sql

**Step 2: Create mixed violations test**

```markdown
---
description: Test command with some violations
---

# Mixed Test

Process the input.

Do the thing with the data from the file at @nonexistent-reference.md.

Code block without language:
```

code here
```sql
```

**Step 3: Create bad command test**

```markdown
---
badfield: invalid
unknown: field
---

No description.

No structure. Just text. Do stuff. Handle things. Make it work.

Code:
```

more code
```text

Uses $INVALID placeholder.
```

**Step 4: Run full test suite**

```bash
# Test good command (should mostly pass)
/audit-command .claude/commands/test-audit-good.md

# Test mixed violations
/audit-command .claude/commands/test-audit-mixed.md

# Test bad command (many failures)
/audit-command .claude/commands/test-audit-bad.md
```

Expected results:
- Good: PASS or minor warnings
- Mixed: WARNINGS with specific issues
- Bad: FAIL with many violations

**Step 5: Commit**

```bash
git add .claude/commands/test-audit-*.md
git commit -m "test: add comprehensive test suite for audit command

- Create test-audit-good.md with best practices
- Create test-audit-mixed.md with some violations
- Create test-audit-bad.md with many violations
- Verify audit catches expected issues

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 8: Validation and Documentation

**Files:**
- Modify: `plugins/meta/meta-claude/commands/audit-command.md` (final review)
- Update: Design doc if needed

**Step 1: Run audit on real commands**

Test on actual project commands:

```bash
# Audit the audit command itself (meta!)
/audit-command plugins/meta/meta-claude/commands/audit-command.md

# Audit other meta-claude commands
/audit-command plugins/meta/meta-claude/commands/*.md

# Review results for any issues
```

Expected: Audit command should pass its own validation or have only minor warnings.

**Step 2: Review and refine validation logic**

Check for:
- False positives (valid commands flagged incorrectly)
- False negatives (invalid commands passing)
- Unclear error messages
- Missing edge cases

Make any necessary adjustments to validation rules.

**Step 3: Final verification**

Run complete test suite:
```bash
/audit-command .claude/commands/test-audit-good.md
/audit-command .claude/commands/test-audit-mixed.md
/audit-command .claude/commands/test-audit-bad.md
```

Verify:
- All checks execute correctly
- Report formatting is clear
- Recommendations are actionable
- References are accurate

**Step 4: Update design doc if needed**

If any significant changes were made during implementation:
- Update `docs/plans/2025-11-09-command-audit-design.md`
- Document any deviations from original plan
- Note lessons learned

**Step 5: Final commit**

```bash
git add plugins/meta/meta-claude/commands/audit-command.md
git commit -m "feat: finalize slash command audit system

- Complete all validation checks
- Verify on real project commands
- Refine error messages and recommendations
- Audit command validates itself successfully

Implements comprehensive validation for:
- Technical compliance (11 checks)
- Quality practices (11 checks)
- Architectural standards (3 checks)

Total: 25 validation checks with detailed reports

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Implementation Complete

The slash command audit system is now fully implemented with:

✅ **25 comprehensive validation checks**
- 11 technical compliance checks
- 11 quality practice checks
- 3 architectural standard checks

✅ **Detailed error reporting**
- What is wrong
- Why it matters
- How to fix it
- References to documentation

✅ **Robust error handling**
- File access errors
- Parsing errors
- Invalid syntax
- Edge cases

✅ **Complete test suite**
- Good command examples
- Mixed violation examples
- Bad command examples

✅ **Self-validating**
- Audit command passes its own validation

**Location:** `plugins/meta/meta-claude/commands/audit-command.md`

**Usage:** `/audit-command [path-to-command.md]`

**Output:** Comprehensive report displayed in conversation

---

## Notes for Engineer

**Key Implementation Details:**

1. **All standards embedded** - No external dependencies beyond Read tool
2. **Self-contained validation** - All rules hardcoded in command file
3. **Clear output format** - Structured report with categories
4. **Actionable recommendations** - Every failure includes fix steps
5. **Reference traceability** - Line numbers for documentation sources

**Testing Strategy:**

- Test on well-formed commands (should pass)
- Test on commands with violations (should catch all issues)
- Test on edge cases (empty, invalid YAML, missing files)
- Verify error messages are clear and helpful
- Ensure recommendations are actionable

**Quality Gates:**

- [ ] All 25 checks execute correctly
- [ ] Error handling covers all edge cases
- [ ] Report format is clear and readable
- [ ] Recommendations are specific and actionable
- [ ] References point to correct documentation
- [ ] Audit command validates itself successfully

**Commit Discipline:**

- One commit per task
- Clear commit messages
- Include 🤖 Generated with Claude Code footer
- Co-authored-by credit
