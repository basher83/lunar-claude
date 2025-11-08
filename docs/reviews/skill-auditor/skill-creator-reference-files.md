# Skill-Creator Reference Files

These are the reference files from `/mnt/skills/examples/skill-creator/references/` that you might not be able to access directly. They contain helpful patterns but **all critical requirements are in SKILL.md** - these are just best practices.

---

## File 1: workflows.md

**Source:** `/mnt/skills/examples/skill-creator/references/workflows.md`

### Workflow Patterns

#### Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

#### Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

---

## File 2: output-patterns.md

**Source:** `/mnt/skills/examples/skill-creator/references/output-patterns.md`

### Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

#### Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

#### Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```

feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

```text

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```

fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation

```text

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

---

## Usage Notes

**These are referenced in skill-creator SKILL.md at lines 286-289:**

```markdown
#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns
```

**Important:** These are **best practices**, not requirements. The auditor doesn't need to check these - they're just helpful patterns for writing better skills.

## What This Means for the Auditor

The auditor v2 now:

- ✅ **ONLY** requires reading `/mnt/skills/examples/skill-creator/SKILL.md`
- ❌ **DOES NOT** try to read these reference files (they might not be accessible)
- 💡 All critical requirements are in SKILL.md anyway

These reference files are useful for **human skill creators** to learn patterns, but not needed for **automated auditing**.
