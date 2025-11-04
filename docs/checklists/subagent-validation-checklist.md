# Subagent Validation Checklist

This checklist validates subagent files against official Claude Code subagent
standards from
`plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md`.

## Quick Validation

Use this checklist when:

- Creating new subagents
- Reviewing existing subagents
- Auditing subagent quality
- Ensuring team subagents follow standards
- Validating plugin-provided subagents

---

## 1. File Structure & Location

### Required Checks

- [ ] **File is in correct location**
  - Project subagents: `.claude/agents/` directory
  - User subagents: `~/.claude/agents/` directory
  - Plugin subagents: `agents/` directory within plugin
  - **Standard:** sub-agents.md lines 76-81 (File locations table)
  - **Correct example:** `.claude/agents/code-reviewer.md`
  - **Incorrect example:** `.claude/subagents/code-reviewer.md` or `agents.md`

- [ ] **File has markdown extension**
  - Must end with `.md` extension
  - **Standard:** sub-agents.md line 76 "stored as Markdown files"
  - **Correct example:** `test-runner.md`
  - **Incorrect example:** `test-runner.txt` or `test-runner`

- [ ] **File contains YAML frontmatter**
  - Must start with `---` on first line
  - YAML block must end with `---`
  - **Standard:** sub-agents.md line 76 "Markdown files with YAML frontmatter"
  - **Correct structure:** First line is `---`, followed by YAML, then closing `---`
  - **Incorrect structure:** Missing opening or closing `---` delimiters

---

## 2. YAML Frontmatter Validation

### Required Checks

- [ ] **`name` field is present**
  - Field must exist in YAML frontmatter
  - **Standard:** sub-agents.md line 150 "`name` | Yes | Required"
  - **Correct example:** `name: code-reviewer`
  - **Incorrect example:** Missing `name` field entirely

- [ ] **`name` field follows naming conventions**
  - Uses only lowercase letters and hyphens
  - No spaces, underscores, or special characters
  - **Standard:** sub-agents.md line 150 "lowercase letters and hyphens"
  - **Correct examples:** `code-reviewer`, `test-runner`, `data-scientist`
  - **Incorrect examples:** `Code-Reviewer`, `test_runner`, `data scientist`

- [ ] **`description` field is present**
  - Field must exist in YAML frontmatter
  - **Standard:** sub-agents.md line 151 "`description` | Yes | Required"
  - **Correct example:** `description: Expert code reviewer for quality and security`
  - **Incorrect example:** Missing `description` field entirely

- [ ] **`description` is meaningful and action-oriented**
  - Describes WHEN the subagent should be used
  - Written in natural language
  - **Standard:** sub-agents.md line 151 "Natural language description of purpose"
  - **Correct example:**
    "Expert code review specialist. Use immediately after writing code."
  - **Incorrect example:** "Reviews code" (too vague)

- [ ] **`tools` field format is correct (if present)**
  - Comma-separated list of tool names
  - OR field is omitted entirely (inherits all tools)
  - No invalid formatting
  - **Standard:** sub-agents.md line 152 "Comma-separated list"
  - **Correct examples:** `tools: Read, Grep, Glob` OR field omitted
  - **Incorrect examples:** `tools: [Read, Grep]` or `tools: "Read Grep"`

- [ ] **`model` field value is valid (if present)**
  - Must be one of: `sonnet`, `opus`, `haiku`, or `'inherit'`
  - OR field is omitted (defaults to configured subagent model)
  - **Standard:** sub-agents.md lines 153, 159-161
  - **Correct examples:** `model: sonnet`, `model: 'inherit'`, or field omitted
  - **Incorrect examples:** `model: gpt-4`, `model: claude-3`

---

## 3. System Prompt Content

### Required Checks

- [ ] **System prompt exists after frontmatter**
  - Content must be present after closing `---`
  - Cannot be empty or whitespace only
  - **Standard:** sub-agents.md line 138 "Your subagent's system prompt goes here"
  - **Correct example:** Frontmatter followed by multi-paragraph prompt
  - **Incorrect example:** File ends after `---` with no content

- [ ] **System prompt is detailed and specific**
  - Includes specific instructions for the subagent
  - Not just a one-sentence description
  - **Standard:** sub-agents.md line 390 "Include specific instructions, examples,
    and constraints"
  - **Correct example:** Multiple paragraphs with role definition, process steps,
    and guidelines
  - **Incorrect example:** "You are a code reviewer." (too brief)

- [ ] **System prompt defines the subagent's role**
  - Clearly states what the subagent is/does
  - **Standard:** sub-agents.md line 139 "clearly define the subagent's role"
  - **Correct example:** "You are a senior code reviewer ensuring high standards..."
  - **Incorrect example:** Jumps into instructions without defining role

- [ ] **System prompt includes approach or methodology**
  - Describes HOW the subagent should work
  - May include step-by-step process
  - **Standard:** sub-agents.md line 139 "capabilities, and approach to solving
    problems"
  - **Correct example:** "When invoked: 1. Run git diff 2. Focus on modified
    files..."
  - **Incorrect example:** No methodology or process described

- [ ] **System prompt includes constraints or guidelines**
  - Specifies what the subagent should/shouldn't do
  - May include checklists, best practices, or focus areas
  - **Standard:** sub-agents.md lines 142-143 "constraints the subagent should follow"
  - **Correct example:** Review checklist with specific items to check
  - **Incorrect example:** No boundaries or guidelines provided

---

## 4. Functional Effectiveness

### Required Checks

- [ ] **Subagent has single, clear responsibility**
  - Focused on one specific task or domain
  - Not trying to do everything
  - **Standard:** sub-agents.md line 388 "single, clear responsibilities"
  - **Correct example:** Code review specialist (focused)
  - **Incorrect example:** "Does code review, testing, documentation, and
    deployment" (too broad)

- [ ] **Tool access is appropriately limited**
  - Only includes tools necessary for the task
  - OR inherits all tools with justification
  - **Standard:** sub-agents.md line 392 "Only grant tools that are necessary"
  - **Correct examples:**
    - Code reviewer: `Read, Grep, Glob, Bash` (no Write/Edit)
    - Test runner: `Read, Bash` (needs to run tests)
  - **Incorrect example:** Test analyzer with `Edit, Write` (doesn't need to modify)

- [ ] **Description encourages proactive use (if intended)**
  - Includes phrases like "use PROACTIVELY" or "use immediately"
  - OR is clearly for explicit invocation only
  - **Standard:** sub-agents.md line 231 "include phrases like 'use PROACTIVELY'"
  - **Correct examples:**
    - "Use PROACTIVELY after code changes"
    - "Use immediately after writing code"
  - **Incorrect example:** Intended to be proactive but missing trigger language

- [ ] **Model selection is appropriate for task**
  - Complex analysis tasks use `sonnet` or `opus`
  - Simple tasks can use `haiku`
  - Consistency needs use `'inherit'`
  - **Standard:** sub-agents.md lines 157-165 (Model selection)
  - **Correct examples:**
    - Code review: `sonnet` (needs analysis)
    - Quick formatter: `haiku` (simple task)
  - **Incorrect example:** Complex security audit with `haiku`

---

## 5. Best Practices Compliance

### Required Checks

- [ ] **Subagent follows naming best practices**
  - Name is descriptive of function
  - Uses standard naming pattern (noun or role-based)
  - **Standard:** sub-agents.md line 150 (implicitly from examples)
  - **Correct examples:** `code-reviewer`, `debugger`, `data-scientist`
  - **Incorrect examples:** `agent1`, `helper`, `do-stuff`

- [ ] **System prompt follows example patterns**
  - Uses clear structure similar to official examples
  - Includes "When invoked" or "You are" sections
  - **Standard:** sub-agents.md lines 277-382 (Example subagents)
  - **Correct structure:** Role definition → Process → Guidelines/Checklist
  - **Incorrect structure:** Unstructured wall of text

- [ ] **Appropriate for version control (project subagents)**
  - No personal paths or credentials
  - No machine-specific configurations
  - **Standard:** sub-agents.md line 394 "Check project subagents into version
    control"
  - **Correct example:** Generic tool references, no hardcoded paths
  - **Incorrect example:** Contains `/home/username/` paths

---

## 6. Integration & Usage Validation

### Required Checks

- [ ] **File is accessible in expected location**
  - For project: `.claude/agents/` directory exists and contains file
  - For user: `~/.claude/agents/` directory exists and contains file
  - File has read permissions
  - **Standard:** sub-agents.md lines 76-81 (File locations)
  - **How to verify:** Check file exists at specified path

- [ ] **No conflicting subagent names at same or higher priority**
  - Project subagents don't conflict with each other
  - Check for duplicate names that would cause conflicts
  - **Standard:** sub-agents.md line 83 "project-level subagents take precedence"
  - **How to verify:** List all `.md` files in `.claude/agents/` and check for
    duplicate `name` fields

- [ ] **YAML is valid and parseable**
  - YAML syntax is correct
  - No indentation errors
  - All values are properly quoted if needed
  - **Standard:** sub-agents.md implicit from "YAML frontmatter" requirement
  - **How to verify:** Parse YAML with a YAML parser, check for errors

- [ ] **Content is well-formatted markdown**
  - System prompt uses valid markdown
  - No broken syntax that would affect rendering
  - **Standard:** sub-agents.md line 76 "Markdown files"
  - **How to verify:** Render markdown, check for parsing errors

---

## Validation Workflow

### Step-by-Step Process

1. **Locate the subagent file**
   - Identify which type: project (`.claude/agents/`), user (`~/.claude/agents/`),
     or plugin
   - Verify file exists at expected location

2. **Read the entire file**
   - Open the file and read complete contents
   - Identify YAML frontmatter section and system prompt section

3. **Validate YAML frontmatter (Section 2)**
   - Check for opening and closing `---` delimiters
   - Verify `name` field exists and follows naming conventions
   - Verify `description` field exists and is meaningful
   - If `tools` field present, verify comma-separated format
   - If `model` field present, verify valid value

4. **Validate system prompt content (Section 3)**
   - Verify prompt exists after frontmatter
   - Check for detailed instructions
   - Verify role definition present
   - Check for methodology/approach
   - Verify constraints or guidelines included

5. **Assess functional effectiveness (Section 4)**
   - Evaluate if subagent has single, clear responsibility
   - Check if tool access is appropriately limited
   - Verify description includes proactive language (if intended)
   - Assess if model choice is appropriate for task complexity

6. **Check best practices compliance (Section 5)**
   - Verify naming follows conventions
   - Check system prompt structure against examples
   - For project subagents, verify no personal/machine-specific content

7. **Verify integration (Section 6)**
   - Confirm file is accessible
   - Check for conflicting names at same priority level
   - Validate YAML parseability
   - Check markdown formatting

8. **Fill out validation report**
   - Use template: `docs/templates/subagent-validation-report-template.md`
   - Document all findings
   - Provide proposed fixes for violations

---

## Validation Summary Template

After reviewing, use the standard report template:

`docs/templates/subagent-validation-report-template.md`

The report should include:

- **✅ Passed Checks:** Categories that fully comply
- **❌ Violations Found:** Specific issues with line references
- **🔧 Fixes Required:** Proposed corrections
- **📊 Overall Assessment:** Compliance rate and readiness

---

## Quick Reference

**Official Standard Source:**

- `plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md`

**Key Standards:**

- Lines 76-81: File locations and priority
- Line 150: `name` field requirements (required, lowercase with hyphens)
- Line 151: `description` field requirements (required, natural language)
- Line 152: `tools` field format (optional, comma-separated)
- Line 153: `model` field values (optional, sonnet/opus/haiku/'inherit')
- Lines 139-143: System prompt content requirements
- Line 388: Single, clear responsibility
- Line 390: Detailed prompts with instructions, examples, constraints
- Line 392: Limited tool access

**Valid Model Values:**

- `sonnet` - Claude Sonnet model
- `opus` - Claude Opus model
- `haiku` - Claude Haiku model
- `'inherit'` - Use main conversation's model
- Omitted - Uses default configured subagent model

**Example Subagents:**

- Lines 279-312: Code reviewer example
- Lines 314-347: Debugger example
- Lines 349-382: Data scientist example

**Common Tool Combinations:**

- Read-only analysis: `Read, Grep, Glob, Bash`
- Code modification: `Read, Edit, Bash`
- Testing: `Read, Bash`
- Data analysis: `Bash, Read, Write`

---

## Zero-Context Validation

This checklist is designed for validators with no prior context. Every criterion is:

- **Objectively verifiable** - Clear yes/no answer
- **Specifically referenced** - Points to exact lines in sub-agents.md
- **Example-driven** - Shows correct and incorrect patterns
- **Self-contained** - All information needed to validate is included

**Usage with Subagents:**

```markdown
Task: Validate subagent file using docs/checklists/subagent-validation-checklist.md

Instructions:

1. Read the entire checklist document
2. Read the subagent file being validated
3. Work through each section (1-6) sequentially
4. Mark each checkbox as pass/fail with evidence
5. Fill out validation report using the template
6. Report findings in standardized format
```

---

## Edge Cases & Exceptions

### CLI-Defined Subagents

- Defined via `--agents` flag instead of file
- Different validation: check JSON structure instead of file/YAML
- Priority: Between project and user level
- **Reference:** sub-agents.md lines 100-124

### Plugin-Provided Subagents

- Located in plugin's `agents/` directory
- May have plugin-specific conventions
- Should still follow core standards (name, description, etc.)
- **Reference:** sub-agents.md lines 85-98

### Built-in Subagents

- Cannot be modified (system-provided)
- Only need to verify they exist and are accessible
- Example: Plan subagent
- **Reference:** sub-agents.md lines 244-275

### Resumable Subagents

- Validation focuses on initial definition, not resume behavior
- Resume functionality is runtime, not file-structure concern
- **Reference:** sub-agents.md lines 410-467

---

## Common Violations Quick Reference

### Automatic Failures

These patterns automatically fail validation:

❌ **Missing required field**

- No `name` field in YAML frontmatter
- No `description` field in YAML frontmatter

❌ **Invalid naming**

- `name: Code-Reviewer` (uppercase)
- `name: test_runner` (underscore)
- `name: my agent` (spaces)

❌ **Empty system prompt**

- YAML frontmatter followed by whitespace only
- No content after closing `---`

❌ **Invalid model value**

- `model: claude-3-opus` (should be just `opus`)
- `model: gpt-4` (wrong model family)

❌ **Malformed YAML**

- Missing opening or closing `---`
- Indentation errors
- Syntax errors

---

## Severity Classification

When reporting violations, classify by severity:

**Critical (Must Fix):**

- Missing required fields (`name`, `description`)
- Invalid YAML syntax (unparseable)
- Empty system prompt
- File not in correct location
- Invalid `name` format
- Invalid `model` value

**Major (Should Fix):**

- Vague or insufficient description
- Missing role definition in system prompt
- Inappropriate tool access (too permissive)
- No methodology/approach in prompt
- Overly broad responsibility

**Minor (Consider Improving):**

- Missing proactive language (if intended to be proactive)
- Could be more detailed in system prompt
- Naming could be more descriptive
- Model choice could be optimized
