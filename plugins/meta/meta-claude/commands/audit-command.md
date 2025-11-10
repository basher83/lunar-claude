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

## Next Steps

Following tasks will implement quality and architectural validation.
