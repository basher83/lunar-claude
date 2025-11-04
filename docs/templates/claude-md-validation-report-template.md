# CLAUDE.md Standards Compliance Review

**File:** [path/to/CLAUDE.md]
**Date:** [YYYY-MM-DD]
**Reviewer:** [Human/Agent Name]

---

## Standards Reference

**Source:** `plugins/meta/claude-docs/skills/claude-code-documentation/reference/memory.md`

**Standard 1 (Line 102):** "Use structure to organize: Format each individual memory as a bullet point and group related memories under descriptive markdown headings."

**Standard 2 (Line 101):** "Be specific: 'Use 2-space indentation' is better than 'Format code properly'."

**Standard 3 (Lines 79-82):** Content should include:

- Frequently used commands (build, test, lint)
- Code style preferences and naming conventions
- Important architectural patterns specific to your project

---

## Violations Found

### VIOLATION #1: Lines [X-Y] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Standard 1/2/3] ([specific aspect])

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

### VIOLATION #2: Lines [X-Y] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Standard 1/2/3] ([specific aspect])

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

[Continue for each violation...]

---

## Summary

**Total violations found:** [N]

**Breakdown:**

- [X] violations of Standard 1 (bullet formatting structure)
- [Y] violations of Standard 2 (specificity)
- [Z] violations of Standard 3 (required content coverage)

**Compliance rate:** [Percentage]% ([X] of [Y] sections have violations)

**Severity:**

- **Critical:** [count] (structural violations, missing required content)
- **Minor:** [count] (organization improvements, specificity enhancements)

---

## Recommendation

[Overall assessment and recommended next steps]

All violations should be addressed to achieve full compliance with memory.md standards. [Describe the primary issues and impact of fixing them.]

---

## Notes

### Template Instructions

**When creating a validation report:**

1. **File and Date:** Fill in the actual CLAUDE.md path and review date
2. **Violations:** Number sequentially, include:
   - Exact line numbers from the file
   - Actual code snippets (use proper markdown fencing)
   - Which specific standard was violated
   - Proposed fix showing corrected code
3. **Summary:** Calculate actual counts and percentages:
   - Count total violations
   - Group by standard type
   - Calculate compliance rate: `(total_sections - sections_with_violations) / total_sections * 100`
4. **Severity Classification:**
   - **Critical:** Structural violations (missing bullets, paragraphs instead of lists, missing required sections)
   - **Minor:** Improvements (better organization, more specific wording, enhanced clarity)

**Formatting Guidelines:**

- Use triple backticks with `markdown` language tag for code blocks showing CLAUDE.md content
- Use consistent heading levels (## for major sections, ### for violations)
- Include line numbers in violation titles for easy navigation
- Keep proposed fixes concise but complete enough to implement

**Output Location:**

- Save completed reports to: `docs/reviews/claude-md-compliance-review-[YYYY-MM-DD].md`
- Use ISO date format (YYYY-MM-DD) in filename
