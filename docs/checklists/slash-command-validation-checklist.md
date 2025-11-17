# Slash Command Validation Checklist

This checklist validates slash command files against official Claude Code slash
command standards from
`plugins/meta/claude-docs/skills/official-docs/reference/slash-commands.md`.

## Quick Validation

Use this checklist when:

- Creating new slash commands
- Reviewing existing slash commands
- Auditing command quality
- Ensuring team commands follow standards
- Validating plugin-provided commands

---

## 1. File Structure & Location

### Required Checks

- [ ] **File is in correct location**
  - Project commands: `.claude/commands/` directory
  - User commands: `~/.claude/commands/` directory
  - Plugin commands: `commands/` directory within plugin
  - **Standard:** slash-commands.md lines 57-58, 71-72, 223
  - **Correct example:** `.claude/commands/optimize.md`
  - **Incorrect example:** `.claude/slash-commands/optimize.md`

- [ ] **File has markdown extension**
  - Must end with `.md` extension
  - **Standard:** slash-commands.md line 48 "derived from the Markdown filename"
  - **Correct example:** `review-pr.md`
  - **Incorrect example:** `review-pr.txt` or `review-pr`

- [ ] **Filename follows naming conventions**
  - Use lowercase letters and hyphens
  - No spaces, underscores (converted to hyphens in command name)
  - **Standard:** slash-commands.md lines 48, 85-90 (namespacing examples)
  - **Correct examples:** `fix-issue.md`, `review-pr.md`, `security-review.md`
  - **Incorrect examples:** `Fix_Issue.md`, `review pr.md`

---

## 2. YAML Frontmatter Validation

### Required Checks

- [ ] **YAML frontmatter syntax is valid (if present)**
  - Starts with `---` on first line
  - Ends with `---`
  - Valid YAML between markers
  - **Standard:** slash-commands.md lines 173-195 (Frontmatter section)
  - **Correct structure:** `---` followed by YAML, then closing `---`
  - **Incorrect structure:** Missing delimiters or invalid YAML syntax

- [ ] **`description` field format (if present)**
  - Must be a non-empty string
  - Brief description of what command does
  - **Standard:** slash-commands.md line 180 "Brief description of the command"
  - **Correct example:** `description: "Create a git commit"`
  - **Incorrect example:** `description:` (empty value)

- [ ] **`allowed-tools` field format (if present)**
  - Must be a string listing tool permissions
  - Format: `ToolName(pattern:*)` or comma-separated list
  - **Standard:** slash-commands.md lines 130, 136, 178
  - **Correct examples:** `allowed-tools: Bash(git add:*), Bash(git status:*)`
  - **Incorrect examples:** `allowed-tools: [Bash]` or `allowed-tools: bash`

- [ ] **`argument-hint` field format (if present)**
  - Must be a string describing expected arguments
  - **Standard:** slash-commands.md line 179 "arguments expected for the slash
    command"
  - **Correct examples:** `argument-hint: [message]`,
    `argument-hint: [pr-number] [priority] [assignee]`
  - **Incorrect example:** `argument-hint:` (empty value)

- [ ] **`model` field value (if present)**
  - Must be a valid model string
  - **Standard:** slash-commands.md line 181 "Specific model string"
  - **Correct example:** `model: claude-3-5-haiku-20241022`
  - **Incorrect example:** `model: gpt-4` (invalid model)

- [ ] **`disable-model-invocation` field (if present)**
  - Must be a boolean (true/false)
  - **Standard:** slash-commands.md line 182 "Whether to prevent SlashCommand
    tool"
  - **Correct example:** `disable-model-invocation: true`
  - **Incorrect example:** `disable-model-invocation: yes`

- [ ] **No invalid/unknown frontmatter fields**
  - Valid fields: description, allowed-tools, argument-hint, model,
    disable-model-invocation
  - **Standard:** slash-commands.md lines 176-182 (Frontmatter table)
  - **Correct example:** Only uses listed fields
  - **Incorrect example:** Custom field like `author: John`

---

## 3. Markdown Content Validation

### Required Checks

- [ ] **Valid markdown structure**
  - Valid CommonMark markdown syntax
  - Proper heading hierarchy (h1→h2→h3, no skipping)
  - No broken syntax
  - **Standard:** General markdown best practices (CLAUDE.md requirements)
  - **Correct example:** Proper heading progression
  - **Incorrect example:** h1 jumps to h3

- [ ] **Code blocks have language specified**
  - ALL fenced code blocks specify language on opening fence
  - **Standard:** CLAUDE.md requirement "Fenced code blocks MUST have a language
    specified"
  - **Correct example:** ` ```bash ` or ` ```python `
  - **Incorrect example:** ` ``` ` (no language)

- [ ] **Blank lines around code blocks**
  - Code blocks surrounded by blank lines
  - **Standard:** CLAUDE.md requirement "Fenced code blocks MUST be surrounded
    by blank lines"
  - **Correct example:** Blank line before and after each code block
  - **Incorrect example:** Code block immediately after text

- [ ] **Blank lines around lists**
  - Lists (ordered/unordered) surrounded by blank lines
  - **Standard:** CLAUDE.md requirement "Lists MUST be surrounded by blank
    lines"
  - **Correct example:** Blank line before and after list
  - **Incorrect example:** List immediately after paragraph

---

## 4. Argument Handling

### Required Checks

- [ ] **Argument placeholders are valid**
  - Only uses `$ARGUMENTS`, `$1`, `$2`, etc.
  - No custom variables like `$args` or `$input`
  - **Standard:** slash-commands.md lines 96-126 (Arguments section)
  - **Correct examples:** `$ARGUMENTS`, `$1`, `$2`
  - **Incorrect examples:** `$args`, `{argument}`, `$input`

- [ ] **`$ARGUMENTS` usage is correct (if used)**
  - Captures all arguments as single string
  - **Standard:** slash-commands.md lines 96-107
  - **Correct example:** `Fix issue #$ARGUMENTS`
  - **Incorrect usage:** Mixing `$ARGUMENTS` with `$1`, `$2`

- [ ] **Positional arguments documented (if `$1`, `$2`, etc. used)**
  - Each positional parameter explained
  - Users know argument order and meaning
  - **Standard:** slash-commands.md lines 109-126 (Individual arguments)
  - **Correct example:** Comment explaining "$1 - PR number, $2 - priority"
  - **Incorrect example:** Uses `$1`, `$2` without explanation

- [ ] **`argument-hint` matches actual usage (if present)**
  - Frontmatter hint reflects actual argument placeholders in content
  - **Standard:** slash-commands.md lines 179, 189, 201
  - **Correct example:** `argument-hint: [pr-number] [priority]` and content
    uses `$1`, `$2`
  - **Incorrect example:** Hint shows 3 args but content only uses `$ARGUMENTS`

---

## 5. Bash Execution

### Required Checks

- [ ] **Bash execution syntax is correct (if used)**
  - Uses `!` prefix for inline execution: `!`command``
  - **Standard:** slash-commands.md lines 129-150 (Bash command execution)
  - **Correct example:** `` !`git status` ``
  - **Incorrect example:** `` `git status` `` (missing `!` prefix)

- [ ] **`allowed-tools` includes Bash permission (if bash used)**
  - Frontmatter grants Bash tool permission
  - Can specify which bash commands: `Bash(git:*)`
  - **Standard:** slash-commands.md lines 130, 136
  - **Correct example:** `allowed-tools: Bash(git add:*), Bash(git status:*)`
  - **Incorrect example:** Uses bash but no `allowed-tools` field

- [ ] **Bash permissions are appropriately scoped**
  - Permissions limited to specific commands needed
  - Not overly permissive (`Bash(command:*)` only if necessary)
  - **Standard:** Least privilege principle + slash-commands.md line 136
  - **Correct example:** `Bash(git add:*)` for git-only command
  - **Incorrect example:** `Bash(command:*)` when only git is used

---

## 6. File References

### Required Checks

- [ ] **File reference syntax is correct (if used)**
  - Uses `@` prefix: `@path/to/file`
  - **Standard:** slash-commands.md lines 152-166 (File references)
  - **Correct example:** `Review @src/utils/helpers.js`
  - **Incorrect example:** `Review src/utils/helpers.js` (missing `@`)

- [ ] **Static file references exist (if hardcoded paths used)**
  - Files referenced with `@` actually exist
  - Does not apply to `$ARGUMENTS` paths (user-provided)
  - **Standard:** Best practice for reliability
  - **Correct example:** `@docs/README.md` exists in repository
  - **Incorrect example:** `@docs/MISSING.md` does not exist

---

## 7. Command Content Quality

### Required Checks

- [ ] **Instructions are clear and specific**
  - Uses specific action verbs
  - Avoids vague language ("handle", "process", "deal with")
  - **Standard:** Best practice for instruction clarity
  - **Correct example:** "Read file, extract functions, output as JSON"
  - **Incorrect example:** "Handle the file appropriately"

- [ ] **Instructions are written from Claude's perspective**
  - Addresses Claude directly ("You should...", "Your task is...")
  - Not third-person description
  - **Standard:** slash-commands.md lines 148-149, 205-206 (task framing)
  - **Correct example:** "Your task is to review PR #$1"
  - **Incorrect example:** "This command reviews PRs" (descriptive)

- [ ] **Expected output format specified (if applicable)**
  - Tells Claude what format to use (table, JSON, markdown, etc.)
  - **Standard:** Best practice for consistent results
  - **Correct example:** "Output as markdown table with columns: Name, Type"
  - **Incorrect example:** "Display the results" (no format specified)

- [ ] **Examples provided (for complex commands)**
  - Commands with multiple args or special syntax include usage examples
  - Shows expected invocation pattern
  - **Standard:** Best practice for usability
  - **Correct example:** ## Examples section with `/command arg1 arg2`
  - **Incorrect example:** Complex multi-arg command with no examples

---

## 8. Design Principles

### Required Checks

- [ ] **Command has single, clear purpose**
  - Does one thing well (Unix philosophy)
  - Not multiple unrelated functions bundled together
  - **Standard:** Best practice for maintainability
  - **Correct example:** "Generate commit message" (single purpose)
  - **Incorrect example:** "Generate commit, run tests, deploy" (multiple
    purposes)

- [ ] **Command follows KISS principle**
  - Simple and straightforward approach
  - No unnecessary complexity or abstraction
  - **Standard:** Best practice for reliability
  - **Correct example:** Direct approach with clear steps
  - **Incorrect example:** Complex meta-programming or unnecessary indirection

- [ ] **Command follows YAGNI principle**
  - Only includes features/options actually needed now
  - No "future-proof" features added "just in case"
  - **Standard:** Best practice for avoiding bloat
  - **Correct example:** Only includes options actually used
  - **Incorrect example:** Configurable parameters with no current use case

---

## 9. SlashCommand Tool Compatibility

### Optional Checks

- [ ] **`description` field present for tool discoverability**
  - Required for SlashCommand tool to invoke command
  - **Standard:** slash-commands.md line 346 "Have description frontmatter field
    populated"
  - **Correct example:** Has frontmatter `description:` field
  - **Note:** Without description, command won't be available via SlashCommand
    tool

- [ ] **Description under character budget**
  - Brief enough to fit in 15,000 character budget across all commands
  - **Standard:** slash-commands.md lines 377-388 (Character budget limit)
  - **Correct example:** Concise description under 100 characters
  - **Incorrect example:** 500 character description consuming budget

---

## Severity Classification

Use this guide when reporting violations:

### Critical (Blocks Functionality)

Issues that prevent command from working or executing correctly:

- Invalid YAML frontmatter syntax
- Invalid argument placeholders (e.g., `$args` instead of `$ARGUMENTS`)
- Missing `allowed-tools` when bash execution is used
- Invalid bash execution syntax (missing `!` prefix)
- Invalid file reference syntax (missing `@` prefix)

### Major (Significantly Impacts Usability)

Issues that make command difficult to use or understand:

- Missing positional argument documentation (when using `$1`, `$2`, etc.)
- Vague or ambiguous instructions
- Missing examples for complex commands
- Incorrect command perspective (third-person instead of Claude-directed)
- Argument hint doesn't match actual usage

### Minor (Improvement Opportunity)

Issues that are violations but have minimal practical impact:

- Missing frontmatter description (uses first line instead)
- Overly broad bash permissions (functional but less secure)
- Missing blank lines around code blocks (rendering issue)
- Missing language on code blocks (syntax highlighting issue)
- Static file reference that doesn't exist (may be intentional placeholder)

---

## Notes

- Frontmatter is **optional** - commands work without it (use defaults)
- If frontmatter is present, it must be valid YAML
- `description` field defaults to first line of prompt if omitted
- `allowed-tools` defaults to inheriting from conversation if omitted
- Not all checks apply to all commands (e.g., bash checks only apply if bash is
  used)
