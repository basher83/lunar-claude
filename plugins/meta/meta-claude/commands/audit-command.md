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

1. **Valid markdown structure**
   - Check markdown parses without errors
   - Check heading hierarchy (no skipping levels)
   - Pass: ✓ Valid markdown structure
   - Fail: ✗ Invalid markdown structure
     - Why: Proper markdown structure ensures readability
     - Fix: Correct markdown syntax errors
     - Reference: slash-commands.md

2. **Code blocks have language specified**
   - Find all fenced code blocks (```)
   - Check each has language identifier
   - Pass: ✓ All code blocks specify language
   - Fail: ✗ Code blocks missing language specification
     - Why: CLAUDE.md requires all fenced code blocks to have a language specified
     - Fix: Add language identifier after opening backticks (e.g., ```bash or```markdown)
     - Reference: CLAUDE.md line 3

3. **Blank lines around code blocks and lists**
   - Check code blocks surrounded by blank lines
   - Check lists surrounded by blank lines
   - Pass: ✓ Proper blank lines around code blocks and lists
   - Fail: ✗ Missing blank lines around code blocks or lists
     - Why: CLAUDE.md requires blank lines for proper formatting
     - Fix: Add blank lines before and after code blocks and lists
     - Reference: CLAUDE.md line 4

**Syntax Features Validation:**

1. **File references use @ syntax correctly**
   - Find patterns like `@path/to/file`
   - Check syntax is valid
   - Pass: ✓ File reference syntax correct
   - Fail: ✗ Invalid file reference syntax
     - Why: File references must use @ prefix for Claude to recognize them
     - Fix: Use @path/to/file format for file references
     - Reference: slash-commands.md line 161

2. **Bash execution uses ! prefix correctly**
   - Find bash execution patterns `!`command``
   - Check syntax: backticks and ! prefix
   - Pass: ✓ Bash execution syntax correct
   - Fail: ✗ Invalid bash execution syntax
     - Why: Bash commands must use !`command` format
     - Fix: Use !`command` format for bash execution
     - Reference: slash-commands.md line 139

3. **Argument placeholders are valid**
   - Find $ARGUMENTS or $1, $2, etc.
   - Check valid placeholder syntax
   - Pass: ✓ Valid argument placeholder syntax
   - Fail: ✗ Invalid argument placeholder: [placeholder]
     - Why: Only $ARGUMENTS or $1, $2, etc. are valid
     - Fix: Use $ARGUMENTS for all args or $1, $2 for positional
     - Reference: slash-commands.md line 103

4. **Bash execution permissions match allowed-tools**
   - If command uses !`bash command`, check frontmatter includes Bash in allowed-tools
   - Pass: ✓ Bash permissions match usage
   - Warn: ⚠ Bash execution without allowed-tools permission
     - Why: Command uses !`bash` but frontmatter doesn't include Bash in allowed-tools
     - Fix: Add to frontmatter: allowed-tools: Bash(command:*)
     - Reference: slash-commands.md line 139

### Step 4: Run Quality Practice Checks

**Description Quality:**

1. **Description is clear and descriptive**
   - Check description explains command purpose (not just filename)
   - Check description is informative
   - Pass: ✓ Description is clear and descriptive
   - Fail: ✗ Description unclear or not descriptive
     - Why: Description appears in /help and should clearly explain purpose
     - Fix: Revise description to explain what command does and when to use it
     - Reference: slash-commands.md line 186

2. **Description under 100 characters**
   - Check length of description field
   - Pass: ✓ Description under 100 characters
   - Warn: ⚠ Description exceeds 100 characters (currently: X chars)
     - Why: Long descriptions may be truncated in /help output
     - Fix: Shorten description to under 100 characters while keeping it clear
     - Reference: Best practice for /help display

**Instruction Clarity:**

1. **Instructions are clear and unambiguous**
   - Check for vague language ("handle this", "do that")
   - Check for clear action verbs
   - Pass: ✓ Instructions are clear and unambiguous
   - Fail: ✗ Instructions contain vague or ambiguous language
     - Why: Claude needs explicit instructions to execute correctly
     - Fix: Use specific action verbs and clear steps
     - Reference: command-creator SKILL.md line 89

2. **Instructions have structure (sections/steps)**
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

3. **Expected output format specified**
   - Check if command describes what output should look like
   - Pass: ✓ Output format specified
   - Warn: ⚠ Output format not specified
     - Why: Clear output expectations help Claude provide consistent results
     - Fix: Add section describing expected output format
     - Reference: command-creator SKILL.md line 75

4. **Written from Claude's perspective**
   - Check instructions say "You should..." not "The user should..."
   - Pass: ✓ Written from Claude's perspective
   - Fail: ✗ Instructions not from Claude's perspective
     - Why: Instructions should tell Claude what to do, not describe user actions
     - Fix: Rewrite as instructions to Claude: "You should..." "Your task is..."
     - Reference: command-creator SKILL.md line 23

**Tool Permission Hygiene:**

1. **allowed-tools grants only necessary permissions**
   - Compare allowed-tools to actual tool usage in instructions
   - Check for overly permissive grants (e.g., Bash(*:*))
   - Pass: ✓ Tool permissions match usage
   - Fail: ✗ Overly permissive tool permissions
     - Why: Granting more permissions than needed violates least privilege
     - Fix: Restrict allowed-tools to only what command actually uses
     - Reference: Best practice - principle of least privilege

2. **Permissions match actual command usage**
   - Check if command uses tools not in allowed-tools
   - Pass: ✓ All used tools have permissions
   - Fail: ✗ Command uses tools without permission: [tool name]
     - Why: Command will fail if it tries to use unpermitted tools
     - Fix: Add missing tool to allowed-tools field
     - Reference: slash-commands.md line 185

**File Reference Validation:**

1. **Static @ file references point to existing files**
   - Extract all @path/to/file references from command body
   - Check if each referenced file exists
   - Pass: ✓ All file references valid (@paths exist)
   - Fail: ✗ File reference points to non-existent file: [path]
     - Why: Command will fail when invoked if referenced files don't exist
     - Fix: Create the referenced file or correct the path
     - Reference: slash-commands.md line 161

**Documentation Completeness:**

1. **Examples provided for complex commands**
   - If command uses multiple arguments or has complex usage, check for examples
   - Pass: ✓ Examples provided for complex command
   - Warn: ⚠ Complex command missing usage examples
     - Why: Examples help users understand how to invoke the command correctly
     - Fix: Add ## Examples section with sample invocations and expected behavior
     - Reference: command-creator SKILL.md line 79

2. **Argument usage explained for positional parameters**
   - If command uses $1, $2, etc., check for explanation
   - Pass: ✓ Positional argument usage explained
   - Warn: ⚠ Positional arguments not explained
     - Why: Users need to know what each argument represents
     - Fix: Document what each $1, $2, etc. parameter means
     - Reference: slash-commands.md line 119

### Step 5: Run Architectural Standard Checks

**Design Principles:**

1. **Single, clear purpose**
   - Check if command has one well-defined purpose
   - Check for multiple unrelated functions
   - Pass: ✓ Single, clear purpose
   - Fail: ✗ Command has multiple unrelated purposes
     - Why: Each command should do one thing well
     - Fix: Split into separate commands if doing multiple unrelated things
     - Reference: ai_docs/continuous-improvement/rules.md (General Engineering Guidelines)

2. **Follows KISS principle (not over-engineered)**
   - Check for unnecessary complexity
   - Check for features that could be simpler
   - Pass: ✓ Follows KISS principle
   - Fail: ✗ Command is over-engineered
     - Why: Simplicity and reliability over cleverness
     - Fix: Simplify logic, remove unnecessary complexity
     - Reference: ai_docs/continuous-improvement/rules.md line 14

3. **Follows YAGNI principle (no unnecessary features)**
   - Check for unused options or features
   - Check for "just in case" functionality
   - Pass: ✓ Follows YAGNI principle
   - Fail: ✗ Violates YAGNI - includes unnecessary features
     - Why: Command includes features/options that aren't needed for stated purpose
     - Fix: Remove unused options/features, keep only what's necessary
     - Reference: ai_docs/continuous-improvement/rules.md line 16

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
