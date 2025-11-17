# Skill Review Content

Review content quality (clarity, completeness, usefulness) of a skill's SKILL.md file.

## Usage

```bash
/skill-review-content <skill-path>
```

## What This Does

Analyzes SKILL.md content for:

- **Clarity:** Instructions are clear, well-structured, and easy to follow
- **Completeness:** All necessary information is present and organized
- **Usefulness:** Content provides value for Claude's context
- **Examples:** Practical, accurate, and helpful examples are included
- **Actionability:** Instructions are specific and executable

## Instructions

Read and analyze the SKILL.md file at the provided path. Evaluate content across five quality dimensions:

### 1. Clarity Assessment

Check for:

- Clear, concise writing without unnecessary verbosity
- Logical structure with appropriate headings and sections
- Technical terms explained when necessary
- Consistent terminology throughout
- Proper markdown formatting (lists, code blocks, emphasis)

**Issues to flag:**

- Ambiguous or vague instructions
- Confusing organization or missing structure
- Unexplained jargon or acronyms
- Inconsistent terminology
- Poor markdown formatting

### 2. Completeness Assessment

Verify:

- Purpose and use cases clearly stated
- All necessary context provided
- Prerequisites or dependencies documented
- Edge cases and error handling covered
- Table of contents (if content is long)

**Issues to flag:**

- Missing purpose statement or unclear use cases
- Incomplete workflows or partial instructions
- Undocumented dependencies
- No error handling guidance
- Long content without navigation aids

### 3. Examples Assessment

Evaluate:

- Examples are practical and relevant
- Code examples have correct syntax
- Examples demonstrate real use cases
- Sufficient variety to cover common scenarios
- Examples are accurate and tested

**Issues to flag:**

- Missing examples for key workflows
- Incorrect or broken code examples
- Trivial examples that don't demonstrate value
- Insufficient coverage of use cases
- Outdated or inaccurate examples

### 4. Actionability Assessment

Confirm:

- Instructions are specific and executable
- Clear steps for workflows
- Commands or code ready to use
- Expected outcomes documented
- Success criteria defined

**Issues to flag:**

- Vague instructions without concrete steps
- Missing command syntax or parameters
- No expected output examples
- Unclear success criteria
- Abstract guidance without implementation details

### 5. Usefulness for Claude

Assess:

- Description triggers skill appropriately
- Content enhances Claude's capabilities
- Follows progressive disclosure principle
- Avoids redundant general knowledge
- Provides specialized context Claude lacks

**Issues to flag:**

- Description too narrow or too broad
- Content duplicates Claude's general knowledge
- Excessive verbosity wasting tokens
- Missing specialized knowledge
- Poor description for skill triggering

## Quality Report Format

Generate a structured report with the following sections:

```text
## Content Quality Review: <skill-name>

**Overall Status:** PASS | FAIL

### Summary

[1-2 sentence overview of quality assessment]

### Quality Scores

- Clarity: PASS | FAIL
- Completeness: PASS | FAIL
- Examples: PASS | FAIL
- Actionability: PASS | FAIL
- Usefulness: PASS | FAIL

### Issues Found

#### Tier 1 (Simple - Auto-fixable)
[Issues that can be automatically corrected]
- [ ] Issue description (e.g., "Missing blank lines around code blocks")

#### Tier 2 (Medium - Guided fixes)
[Issues requiring judgment but clear remediation]
- [ ] Issue description (e.g., "Add examples for error handling workflow")

#### Tier 3 (Complex - Manual review)
[Issues requiring significant rework or design decisions]
- [ ] Issue description (e.g., "Restructure content for better progressive disclosure")

### Recommendations

[Specific, actionable suggestions for improvement]

### Strengths

[Positive aspects worth highlighting]
```

## Error Handling

**If SKILL.md not found:**

```text
Error: SKILL.md not found at <skill-path>
```

Action: Verify path is correct or run `/skill-create` first

**If content passes review:**

- Report: "Content Quality Review: PASS"
- Highlight strengths
- Note minor suggestions if any
- Exit with success

**If content has issues:**

- Report: "Content Quality Review: FAIL"
- List all issues categorized by tier
- Provide specific recommendations
- Exit with failure

**Issue Categorization:**

- **Tier 1 (Auto-fix):** Formatting, spacing, markdown syntax
- **Tier 2 (Guided fix):** Missing sections, incomplete examples, unclear descriptions
- **Tier 3 (Complex):** Structural problems, fundamental clarity issues, major rewrites

## Pass Criteria

Content PASSES if:

- At least 4 of 5 quality dimensions pass
- No Tier 3 (complex) issues found
- Critical sections (description, purpose, examples) are adequate

Content FAILS if:

- 2 or more quality dimensions fail
- Any Tier 3 (complex) issues found
- Critical sections are missing or fundamentally flawed

## Examples

**High-quality skill:**

```bash
/skill-review-content plugins/meta/meta-claude/skills/skill-creator
# Output: Content Quality Review: PASS
# - All quality dimensions passed
# - Clear structure with progressive disclosure
# - Comprehensive examples and actionable guidance
```

**Skill needing improvement:**

```bash
/skill-review-content /path/to/draft-skill
# Output: Content Quality Review: FAIL
#
# Issues Found:
# Tier 2:
# - Add examples for error handling workflow
# - Clarify success criteria for validation step
# Tier 3:
# - Restructure content for better progressive disclosure
# - Description too broad, needs refinement for triggering
```

## Notes

- This review focuses on **content quality**, not technical compliance
- Technical validation (frontmatter, naming) is handled by `/skill-review-compliance`
- Be constructive: highlight strengths and provide actionable suggestions
- Content quality is subjective: use judgment and consider the skill's purpose
- Focus on whether Claude can effectively use the skill, not perfection
