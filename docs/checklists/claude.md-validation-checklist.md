# CLAUDE.md Validation Checklist

This checklist validates CLAUDE.md files against official Claude Code memory
standards from
`plugins/meta/claude-docs/skills/claude-code-documentation/reference/memory.md`.

## Quick Validation

Use this checklist when:

- Creating new CLAUDE.md files
- Reviewing project memory files
- Auditing CLAUDE.md for standards compliance
- Ensuring team documentation follows best practices

---

## 1. Structural Formatting

### Required Checks

- [ ] **All content formatted as bullet points**
  - Every instruction, command, or guidance item must be a bullet point (starts with `-` or numbered list)
  - Paragraphs of prose text are NOT allowed (except within code blocks)
  - **Standard:** memory.md line 102 - "Format each individual memory as a bullet point"
  - **Correct example:**
    - Content formatted as bullets with indented code blocks
    - Each command introduced by a bullet point
  - **Incorrect example:**
    - Paragraph prose before code blocks
    - Code blocks without bullet introduction

- [ ] **Related items grouped under descriptive headings**
  - Use markdown headings (##, ###) to organize related bullets
  - Heading names are descriptive and specific (not vague like "Misc" or "Other")
  - **Standard:** memory.md line 102 - "group related memories under descriptive markdown headings"
  - **Correct example:**

    ```markdown
    ## Testing Commands

    - Run unit tests
    - Run integration tests

    ## Build Commands

    - Build for production
    - Build for development
    ```

  - **Incorrect example:**
- All items grouped under single generic "Commands" heading
- No logical organization by category

- [ ] **No introductory paragraphs**
  - Do NOT include paragraphs explaining "This file provides guidance..."
  - Do NOT include meta-commentary about the CLAUDE.md file itself
  - Start directly with actionable content organized under headings
  - **Rationale:** CLAUDE.md purpose is self-evident; meta-text wastes token budget
  - **Incorrect example:**

    ```markdown
    # CLAUDE.md

    This file provides guidance to Claude Code when working with code in this repository.
    ```

  - **Correct example:**

    ```markdown
    # CLAUDE.md

    ## Project Overview

    - This is a Python web application using FastAPI
    - Database: PostgreSQL 15
    ```

- [ ] **Code blocks introduced with bullets**
  - Every code block must be introduced by a bullet point
  - Standalone code blocks without bullet introduction are NOT allowed
  - **Standard:** memory.md line 102 (implicit from "each individual memory as a bullet point")
  - **Correct example:**
    - Bullet point introduces the code block
    - Code block is indented under the bullet
  - **Incorrect example:**
    - Heading without bullet point
    - Standalone code block under heading

---

## 2. Content Specificity

### Required Checks

- [ ] **Instructions are specific, not vague**
  - Provide exact commands, values, and configurations
  - Avoid general advice like "format code properly" or "use best practices"
  - **Standard:** memory.md line 101 - "'Use 2-space indentation' is better than 'Format code properly'"
  - **Correct examples:**
    - "Use 2-space indentation for YAML files"
    - "Run `ruff check .` before committing"
    - "Maximum line length is 100 characters"
  - **Incorrect examples:**
    - "Format code properly"
    - "Follow best practices"
    - "Write clean code"

- [ ] **Commands include exact syntax**
  - Do NOT provide command descriptions without the actual command
  - Include all flags and arguments needed
  - **Correct example:**
    - Shows complete command with all flags: `pytest --cov=src --cov-report=html tests/`
  - **Incorrect example:**
    - Vague description: "use pytest with appropriate flags"

- [ ] **Configuration values are explicit**
  - Specify exact file paths, values, and settings
  - Do NOT use placeholders without showing actual values for the project
  - **Correct example:**
    - "Python version: 3.13", "Database: PostgreSQL 15"
  - **Incorrect example:**
    - "Use the correct Python version", "Configure the database appropriately"

---

## 3. Required Content Coverage

### Required Checks

- [ ] **Frequently used commands documented**
  - Build commands
  - Test commands
  - Lint/format commands
  - Run/start commands
  - **Standard:** memory.md line 79 - "Include frequently used commands (build, test, lint)"
  - **Example:**

    ```markdown
    ## Common Commands

    - Build project:
      ```bash
      npm run build
      ```

    - Run tests:

      ```bash
      npm test
      ```

    - Lint code:

      ```bash
      npm run lint
      ```

- [ ] **Code style preferences documented**
  - Language-specific formatting rules
  - Naming conventions (files, variables, functions, classes)
  - Indentation standards
  - Line length limits
  - **Standard:** memory.md line 80 - "Document code style preferences and naming conventions"
  - **Example:**

    ```markdown
    ## Code Style

    ### Python
    - Use snake_case for functions and variables
    - Use PascalCase for class names
    - Maximum line length: 100 characters
    - Use type hints for all function signatures

    ### JavaScript
    - Use camelCase for functions and variables
    - Use PascalCase for React components
    - Use 2-space indentation
    ```

- [ ] **Architectural patterns documented**
  - Project-specific patterns and conventions
  - Directory structure explanations
  - Component organization principles
  - **Standard:** memory.md line 81 - "Add important architectural patterns specific to your project"
  - **Example:**

    ```markdown
    ## Architecture

    - Use Repository pattern for data access (see `src/repositories/`)
    - Services contain business logic (see `src/services/`)
    - Controllers are thin, delegate to services
    - Each feature module contains: routes, services, repositories, models
    ```

---

## 4. Import Syntax (if used)

### Required Checks

- [ ] **Import syntax is correct**
  - Uses `@path/to/file` syntax
  - Both relative and absolute paths are valid
  - Home directory paths use `~` (e.g., `@~/.claude/my-instructions.md`)
  - **Standard:** memory.md lines 20-44
  - **Correct examples:**

    ```markdown
    - See @README.md for project overview
    - Git workflow: @docs/git-workflow.md
    - Personal preferences: @~/.claude/my-project-prefs.md
    ```

- [ ] **Imports not in code blocks**
  - Import syntax `@path` must NOT appear inside markdown code spans (``) or code blocks
  - **Standard:** memory.md line 38 - "imports are not evaluated inside markdown code
    spans and code blocks"
  - **Correct example:**

    ```markdown
    - See @package.json for available npm commands
    ```

  - **Incorrect example:**

    ```markdown
    - Run `npm` with scripts from `@package.json`
    ```

    (The `@package.json` inside backticks will NOT be imported)

- [ ] **Import depth limit respected**
  - Maximum 5 levels of nested imports
  - Imported files can import other files (recursive), but depth limited to 5
  - **Standard:** memory.md line 44 - "Imported files can recursively import
    additional files, with a max-depth of 5 hops"

---

## 5. File Location & Hierarchy Understanding

### Required Checks

- [ ] **File in correct location**
  - Project memory: `./CLAUDE.md` or `./.claude/CLAUDE.md`
  - User memory: `~/.claude/CLAUDE.md`
  - Enterprise policy: OS-specific paths
    - macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    - Linux: `/etc/claude-code/CLAUDE.md`
    - Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`
  - **Standard:** memory.md lines 7-18 (table)

- [ ] **Content appropriate for memory type**
  - **Project memory** (`./CLAUDE.md`): Team-shared, checked into source control
    - Project architecture, coding standards, team workflows
    - NO personal preferences (URLs, credentials, individual settings)
  - **User memory** (`~/.claude/CLAUDE.md`): Personal preferences across all projects
    - Code styling preferences, personal tooling shortcuts
    - NOT project-specific information
  - **Standard:** memory.md lines 11-16 (Purpose and Use Case columns)

- [ ] **Secrets not in project memory**
  - Do NOT include API keys, credentials, personal URLs in `./CLAUDE.md`
  - Use imports to reference personal files: `@~/.claude/my-secrets.md`
  - **Rationale:** Project CLAUDE.md is often checked into git

---

## 6. Best Practices Compliance

### Required Checks

- [ ] **No deprecated patterns**
  - Do NOT use `CLAUDE.local.md` (deprecated)
  - Use imports instead: `@~/.claude/project-local.md`
  - **Standard:** memory.md line 16 - "*(Deprecated, see below)*"

- [ ] **Organized for scannability**
  - Related items grouped together
  - Logical heading hierarchy (## for major sections, ### for subsections)
  - Most frequently accessed info near the top
  - **Standard:** memory.md line 102 - "Use structure to organize"

- [ ] **Content stays current**
  - No outdated commands or tool versions
  - Deprecated information removed (not just marked deprecated)
  - Reflects actual current project state
  - **Standard:** memory.md line 103 - "Review periodically: Update memories as your project evolves"

- [ ] **Token budget efficient**
  - Avoid unnecessary verbosity
  - Use bullet points (not long paragraphs)
  - No duplicate information
  - **Rationale:** CLAUDE.md is loaded into every Claude Code context

---

## 7. Section-by-Section Audit

### Required Checks

Use this checklist to audit each major section:

- [ ] **Section: Project Overview**
  - Uses bullet points (not paragraphs)
  - Specific information (tech stack, versions, key details)
  - No vague marketing-speak

- [ ] **Section: Commands (if present)**
  - All commands in code blocks
  - Each command introduced with bullet
  - Commands are complete (include all flags/args)

- [ ] **Section: Architecture (if present)**
  - Bullet points describing patterns
  - Specific to THIS project (not generic advice)
  - References actual directories/files

- [ ] **Section: Code Style (if present)**
  - Specific rules (not "follow best practices")
  - Organized by language/file type
  - Includes examples where helpful

- [ ] **Section: Development Workflow (if present)**
  - Step-by-step commands
  - Organized as bullets
  - Specific to project's actual workflow

---

## 8. Common Violations Quick Reference

### Automatic Failures

These patterns automatically fail validation:

❌ **Paragraphs of prose text** (except in code blocks)

```markdown
The project uses FastAPI for the web framework. It's a modern,
fast framework that supports async operations.
```

✅ **Correct (bullet points):**

```markdown
- Web framework: FastAPI (supports async operations)
```

---

❌ **Standalone code blocks** (no bullet introduction)

````markdown
## Build Command

```bash
npm run build
```
````

✅ **Correct (bullet + code block):**

````markdown
## Build Command

- Build for production:
  ```bash
  npm run build
  ```
````

---

❌ **Vague instructions**

```markdown
- Format code properly
- Use best practices
- Follow conventions
```

✅ **Correct (specific):**

```markdown
- Run `black .` to format Python code (line length: 100)
- Use type hints for all function signatures
- Name test files as `test_*.py`
```

---

❌ **Meta-commentary about CLAUDE.md itself**

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when
working with code in this repository.
```

✅ **Correct (start with actual content):**

```markdown
# CLAUDE.md

## Project Overview

- Python web application using Django 4.2
```

---

## Validation Workflow

### Step-by-Step Process

1. **Read entire CLAUDE.md file**
   - Note current structure and organization
   - Identify all sections present

2. **Check structural formatting (Section 1)**
   - Verify ALL content is bullet points
   - Confirm no standalone paragraphs exist
   - Ensure all code blocks have bullet introductions

3. **Check content specificity (Section 2)**
   - Verify commands are exact (not descriptions)
   - Confirm values are explicit (not vague)
   - Ensure no generic advice without specifics

4. **Check required content (Section 3)**
   - Commands section exists and is complete
   - Code style is documented
   - Architecture (if complex) is documented

5. **Check imports (Section 4)** (if file uses imports)
   - Syntax is correct
   - Not in code blocks
   - Depth limit respected

6. **Check location appropriateness (Section 5)**
   - File in correct location for its content
   - No secrets in project memory
   - Content matches memory type purpose

7. **Check best practices (Section 6)**
   - No deprecated patterns
   - Well organized and scannable
   - Content is current

8. **Section-by-section audit (Section 7)**
   - Each major section passes all criteria

9. **Check for common violations (Section 8)**
   - No automatic failures present

---

## Validation Summary Template

After reviewing, fill out this summary:

### ✅ Passed Checks

- [ ] Structural Formatting
- [ ] Content Specificity
- [ ] Required Content Coverage
- [ ] Import Syntax (if applicable)
- [ ] File Location & Hierarchy
- [ ] Best Practices Compliance
- [ ] Section-by-Section Audit
- [ ] No Common Violations

### ❌ Violations Found

**Format:** `[Section Name] Line X: [Violation description]`

Example violations:

- Structural Formatting, Lines 7-10: Paragraph prose instead of bullets
- Content Specificity, Line 45: Vague instruction "format code properly"
- Required Content, Missing: No code style section

### 🔧 Fixes Required

**Format:** `Line X: [Current] → [Fixed]`

Example fixes:

1. Lines 7-10: Convert paragraph to bullets
2. Line 45: Change "format code properly" → "Run `black .` to format Python code"
3. Add new section: ## Code Style

### 📊 Overall Assessment

- **Compliance rate:** [X violations / Y total checks] = Z% compliant
- **Severity:**
  - Critical: [count] (structural violations, missing required content)
  - Minor: [count] (organization, specificity improvements)
- **Production ready:** [Yes/No]

---

## Quick Reference

**Official Standard Source:**

- `plugins/meta/claude-docs/skills/claude-code-documentation/reference/memory.md`

**Key Standards:**

- Line 102: "Format each individual memory as a bullet point and group related
  memories under descriptive markdown headings"
- Line 101: "Be specific: 'Use 2-space indentation' is better than 'Format code properly'"
- Lines 79-82: Content recommendations (commands, code style, architecture)

**Zero-Context Validation:**
This checklist is designed for subagents with no prior context. Every criterion is:

- Objectively verifiable (yes/no answer)
- Specific (exact patterns to match/reject)
- Referenced (line numbers from source standard)
- Example-driven (correct vs incorrect shown)

**Usage with Subagents:**

```markdown
Task: Validate CLAUDE.md using docs/checklists/claude.md-validation-checklist.md

Instructions:
1. Read the checklist completely
2. Read the CLAUDE.md file being validated
3. Work through each numbered section sequentially
4. Mark each checkbox as pass/fail with justification
5. Fill out the Validation Summary Template
6. Report findings using the specified format
```
