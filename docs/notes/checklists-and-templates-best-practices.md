# Checklists and Templates: Best Practices

**Created:** 2025-11-04
**Context:** Lessons learned from creating claude.md-validation-checklist.md and claude-md-validation-report-template.md

---

## Core Principle

**Checklists and templates are complementary but separate artifacts that should always be created together.**

- **Checklist** = The validation criteria and process (WHAT to check, HOW to validate)
- **Template** = The output format for reporting findings (HOW to report results)

---

## The Checklist

### Purpose

A checklist defines:

- **WHAT** to validate (specific criteria)
- **HOW** to validate it (methods, tools, references)
- **WHERE** to find the authoritative standard (line numbers, source files)
- **WHY** it matters (rationale, context)

### Key Characteristics

1. **Process-oriented** - Step-by-step validation workflow
2. **Zero-context friendly** - Can be given to a fresh subagent with no prior knowledge
3. **Objective** - Every criterion is verifiable (yes/no answer)
4. **Referenced** - Points to authoritative sources (line numbers, official docs)
5. **Example-driven** - Shows correct vs incorrect patterns
6. **Tool-agnostic** - Focuses on criteria, not implementation details

### Structure Guidelines

```markdown
# [Thing Being Validated] Validation Checklist

## Quick Validation
- When to use this checklist
- Who should use it

## 1. [Category Name]

### Required Checks

- [ ] **[Specific criterion]**
  - What to check
  - How to verify it
  - **Standard:** [source reference with line number]
  - **Correct example:** [brief, no nested code blocks]
  - **Incorrect example:** [brief, no nested code blocks]

## Validation Workflow

### Step-by-Step Process
1. Read [authoritative source]
2. Check [specific aspect]
3. Verify [specific aspect]
...

## Validation Summary Template

[Format for reporting results - points to the actual template file]

## Quick Reference

- Source documentation links
- Tool commands
- Usage instructions
```

### Do's

✅ **DO:**

- Make every check objectively verifiable
- Reference exact line numbers from source standards
- Provide simple examples (avoid nested code blocks)
- Group related checks under logical categories
- Include clear workflow steps
- Make it usable by someone with zero context
- Use checkbox format `- [ ]` for trackable items
- Include both positive (correct) and negative (incorrect) examples
- Specify tool versions or commands where relevant
- Document edge cases and exceptions

### Don'ts

❌ **DON'T:**

- Nest code blocks in examples (causes linting issues)
- Use vague criteria ("code should be good")
- Skip referencing source standards
- Assume prior knowledge or context
- Mix validation criteria with output formatting
- Include the full template in the checklist
- Make subjective judgments without clear criteria
- Create examples that are too complex
- Forget to specify "when NOT to use this checklist"

### Common Pitfalls

**Pitfall 1: Nested Code Blocks**

❌ **Wrong:**

````markdown
- **Correct example:**
  ```markdown
  - Run command:
    ```bash
    npm test
    ```
  ```
````

✅ **Right:**

```markdown
- **Correct example:**
  - Bullet point introduces the command
  - Code block is indented under the bullet
```

**Pitfall 2: Vague Criteria**

❌ **Wrong:**

```markdown
- [ ] Code follows best practices
```

✅ **Right:**

```markdown
- [ ] **Type hints present**
  - All function signatures include type hints
  - Return types specified for all functions
  - **Standard:** PEP 484 type hints
```

**Pitfall 3: Missing References**

❌ **Wrong:**

```markdown
- [ ] Use proper formatting
```

✅ **Right:**

```markdown
- [ ] **Use 2-space indentation for YAML**
  - **Standard:** memory.md line 101 - "Be specific: 'Use 2-space indentation' is better than 'Format code properly'"
```

---

## The Template

### Purpose

A template defines:

- **HOW** to structure the output report
- **WHAT** information to include in findings
- **WHERE** to save the completed report
- **FORMAT** for presenting violations and fixes

### Key Characteristics

1. **Output-oriented** - Focuses on reporting, not validation process
2. **Actionable** - Provides enough detail to implement fixes
3. **Standardized** - Ensures consistency across multiple reviews
4. **Complete** - Includes all necessary sections for decision-making
5. **Reusable** - Can be copied and filled in for each new review

### Structure Guidelines

```markdown
# [Thing Being Validated] Compliance Review

**File:** [path]
**Date:** [YYYY-MM-DD]
**Reviewer:** [name/agent]

---

## Standards Reference

[Brief summary of standards being checked]

---

## Violations Found

### VIOLATION #1: Lines [X-Y] - [Description]

**Current:**
[Show actual code with issue]

**Standard violated:** [Which standard and why]

**Proposed fix:**
[Show corrected code]

---

## Summary

**Total violations found:** [N]
**Breakdown:** [By category]
**Compliance rate:** [Percentage]

---

## Recommendation

[Next steps and overall assessment]

---

## Notes

### Template Instructions
[How to fill out this template]
```

### Do's

✅ **DO:**

- Include file metadata (path, date, reviewer)
- Show actual code snippets for violations
- Provide complete proposed fixes
- Calculate compliance percentages
- Include severity classification
- Add instructions for using the template
- Specify output file naming convention
- Use consistent markdown formatting
- Make fixes copy-paste ready
- Include summary statistics

### Don'ts

❌ **DON'T:**

- Include validation criteria (that's the checklist's job)
- Make the template itself validate (it's just a format)
- Skip proposed fixes
- Use vague descriptions ("line 5 has a problem")
- Forget to number violations sequentially
- Mix multiple issues in one violation entry
- Skip the summary section
- Omit line numbers for violations
- Use inconsistent formatting between violations

### Common Pitfalls

**Pitfall 1: Template Includes Validation Logic**

❌ **Wrong:**

```markdown
## How to Validate

1. Read the file
2. Check for bullets
3. Verify formatting
```

✅ **Right:**

```markdown
## Notes

### Template Instructions

When creating a validation report:
1. Fill in file path and date
2. List violations with line numbers
3. Include proposed fixes
```

**Pitfall 2: Vague Violation Descriptions**

❌ **Wrong:**

```markdown
### VIOLATION #1: Bad formatting

**Current:** Some code that's wrong

**Fix:** Make it better
```

✅ **Right:**

```markdown
### VIOLATION #1: Lines 23-26 - Paragraph not formatted as bullets

**Current:**
```markdown
This is a paragraph of text explaining something.
```

**Standard violated:** Standard 1 (bullet formatting)

**Proposed fix:**
```markdown
- This is a bullet point explaining something
```
```text

**Pitfall 3: Missing Metadata**

❌ **Wrong:**

```markdown
# Review Results

Here are the problems...
```

✅ **Right:**

```markdown
# CLAUDE.md Standards Compliance Review

**File:** `/workspaces/project/CLAUDE.md`
**Date:** 2025-11-04
**Reviewer:** Claude Code Agent

---
```

---

## Creating Checklist + Template Pairs

### Workflow

When you need to create validation materials for something:

1. **Identify the authoritative source**
   - Official documentation
   - Standards specification
   - Best practices guide

2. **Create the checklist first**
   - Extract objective criteria from source
   - Organize into logical categories
   - Add examples and references
   - Make it zero-context friendly
   - Test with a subagent if possible

3. **Create the template second**
   - Define output format based on checklist categories
   - Include sections for each type of finding
   - Add metadata fields
   - Provide usage instructions
   - Make it actionable

4. **Cross-reference them**
   - Checklist should mention the template exists
   - Template should reference the checklist
   - Both should point to the same authoritative source

5. **Test the pair**
   - Run a validation using the checklist
   - Fill out the template with findings
   - Verify the output is complete and actionable
   - Adjust both if needed

### File Naming Conventions

**Checklists:**

- Location: `docs/checklists/`
- Format: `[thing]-validation-checklist.md`
- Examples:
  - `claude.md-validation-checklist.md`
  - `sdk-validation-checklist.md`
  - `skill-validation-checklist.md`

**Templates:**

- Location: `docs/templates/`
- Format: `[thing]-validation-report-template.md`
- Examples:
  - `claude-md-validation-report-template.md`
  - `sdk-validation-report-template.md`
  - `skill-validation-report-template.md`

**Completed Reports:**

- Location: `docs/reviews/`
- Format: `[thing]-compliance-review-[YYYY-MM-DD].md`
- Examples:
  - `claude-md-compliance-review-2025-11-04.md`
  - `sdk-compliance-review-2025-11-04.md`

### Cross-Reference Pattern

**In the checklist:**

```markdown
## Validation Summary Template

After reviewing, use the standard report template:
`docs/templates/[thing]-validation-report-template.md`
```

**In the template:**

```markdown
## Notes

This template is used in conjunction with:
`docs/checklists/[thing]-validation-checklist.md`
```

---

## Real-World Example

### Scenario: Validating CLAUDE.md files

**Checklist:** `docs/checklists/claude.md-validation-checklist.md`

- Contains 8 sections with specific validation criteria
- Each criterion references memory.md line numbers
- Includes workflow for step-by-step validation
- Zero-context friendly for subagents
- Examples avoid nested code blocks

**Template:** `docs/templates/claude-md-validation-report-template.md`

- Defines standard report structure
- Shows how to format violations
- Includes metadata fields
- Provides usage instructions
- Specifies where to save completed reports

**Completed Report:** `docs/reviews/claude-md-compliance-review-2025-11-04.md`

- Follows template structure exactly
- Lists 15 specific violations
- Includes proposed fixes for each
- Calculates compliance rate: 32%
- Provides actionable recommendations

---

## Validation Checklist

Use this meta-checklist when creating new checklist/template pairs:

### Checklist Quality

- [ ] Every criterion is objectively verifiable
- [ ] All criteria reference authoritative sources with line numbers
- [ ] Examples are simple and avoid nested code blocks
- [ ] Can be used by someone with zero context
- [ ] Includes both correct and incorrect examples
- [ ] Has clear step-by-step workflow
- [ ] Groups related checks logically
- [ ] Specifies when to use (and when NOT to use)

### Template Quality

- [ ] Includes file metadata section
- [ ] Has standardized violation format
- [ ] Shows how to present proposed fixes
- [ ] Includes summary/statistics section
- [ ] Contains usage instructions
- [ ] Specifies output file naming
- [ ] Uses consistent markdown formatting
- [ ] Makes findings actionable

### Pair Integration

- [ ] Checklist mentions template exists
- [ ] Template references checklist
- [ ] Both point to same authoritative source
- [ ] File naming is consistent
- [ ] Locations follow conventions
- [ ] Cross-references are accurate

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Checklist as Template

**Problem:** Including the full output format in the checklist

**Why it's bad:** Confuses validation criteria with reporting format

**Solution:** Keep them separate, link to template from checklist

### Anti-Pattern 2: Template as Checklist

**Problem:** Including validation instructions in the template

**Why it's bad:** Template becomes too complex and loses focus

**Solution:** Template provides format only, links to checklist for criteria

### Anti-Pattern 3: Subjective Criteria

**Problem:** "Code should be clean and well-written"

**Why it's bad:** Not verifiable, different interpretations

**Solution:** "Maximum line length: 100 characters (PEP 8 line 15)"

### Anti-Pattern 4: Missing Source References

**Problem:** Criteria without authoritative source

**Why it's bad:** Can't verify correctness, appears arbitrary

**Solution:** Always cite official docs with line numbers

### Anti-Pattern 5: Overly Complex Examples

**Problem:** Nested code blocks, long multi-file examples

**Why it's bad:** Causes linting issues, hard to understand

**Solution:** Use simple bullet-point descriptions or single-level examples

---

## Evolution and Maintenance

### When to Update

**Checklist:**

- Authoritative source changes (new standard version)
- Discovered edge cases need coverage
- Better validation methods emerge
- Tool versions change

**Template:**

- Output format needs improvement
- Additional metadata becomes necessary
- Better presentation methods found
- Stakeholder requirements change

### Version Control

- Track changes in git commits
- Reference checklist/template version in reports
- Document significant changes in CHANGELOG.md
- Archive old versions if standards change substantially

---

## Key Takeaways

1. **Always create in pairs** - Checklist + Template work together
2. **Separate concerns** - Validation ≠ Reporting
3. **Reference sources** - Always cite authoritative standards
4. **Be objective** - Every criterion must be verifiable
5. **Avoid nesting** - Keep examples simple
6. **Zero-context ready** - Fresh subagent should succeed
7. **Make actionable** - Reports should enable immediate fixes
8. **Stay consistent** - Follow naming and location conventions
9. **Cross-reference** - Link checklist ↔ template
10. **Test thoroughly** - Validate the validators

---

## Quick Reference

**File Locations:**

- Checklists: `docs/checklists/[thing]-validation-checklist.md`
- Templates: `docs/templates/[thing]-validation-report-template.md`
- Reports: `docs/reviews/[thing]-compliance-review-[YYYY-MM-DD].md`

**Essential Elements:**

- **Checklist:** Criteria, references, examples, workflow
- **Template:** Metadata, violations, summary, instructions
- **Report:** Filled template with actual findings

**Golden Rules:**

1. Checklist = WHAT/HOW to validate
2. Template = HOW to report
3. Always cite sources
4. Keep examples simple
5. Make everything objective
