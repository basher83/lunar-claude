# Subagent Standards Compliance Review

**File:** [path/to/subagent-file.md]
**Date:** [YYYY-MM-DD]
**Reviewer:** [Human/Agent Name]
**Subagent Type:** [Project/User/Plugin]

---

## Standards Reference

**Source:**
`plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md`

**Key Requirements:**

**File Structure (Lines 76-81):**

- Project subagents: `.claude/agents/` (highest priority)
- User subagents: `~/.claude/agents/` (lower priority)
- Plugin subagents: `agents/` directory in plugin

**YAML Frontmatter (Lines 146-153):**

- `name`: Required, lowercase letters and hyphens only
- `description`: Required, natural language description of purpose
- `tools`: Optional, comma-separated list or omitted to inherit all
- `model`: Optional, values: `sonnet`/`opus`/`haiku`/`'inherit'` or omitted

**System Prompt (Lines 138-143):**

- Must be present after frontmatter
- Should include specific instructions, examples, and constraints
- Should clearly define role, capabilities, and approach

**Best Practices (Lines 384-394):**

- Single, clear responsibility (line 388)
- Detailed prompts (line 390)
- Limited tool access (line 392)
- Version control for project subagents (line 394)

---

## Violations Found

### VIOLATION #1: [Category] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Specific requirement from sub-agents.md with line number]

**Severity:** [Critical/Major/Minor]

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

### VIOLATION #2: [Category] - [Brief description]

**Current:**

```markdown
[Show the actual content that violates the standard]
```

**Standard violated:** [Specific requirement from sub-agents.md with line number]

**Severity:** [Critical/Major/Minor]

**Proposed fix:**

```markdown
[Show the corrected version]
```

---

[Continue for each violation...]

---

## Summary

**Total violations found:** [N]

**Breakdown by Category:**

- File Structure & Location: [count]
- YAML Frontmatter: [count]
- System Prompt Content: [count]
- Functional Effectiveness: [count]
- Best Practices Compliance: [count]
- Integration & Usage: [count]

**Breakdown by Severity:**

- **Critical:** [count] (must fix immediately)
- **Major:** [count] (should fix before use)
- **Minor:** [count] (consider improving)

**Compliance Status:**

- ✅ **Passed Checks:** [X/Y total checks]
- ❌ **Failed Checks:** [Z/Y total checks]
- **Compliance Rate:** [Percentage]%

**Production Readiness:**

- [ ] Ready for production use (all critical and major issues resolved)
- [ ] Needs fixes before production (critical/major issues present)
- [ ] Requires significant rework (multiple critical issues)

---

## Recommendation

[Overall assessment and recommended next steps]

### Priority Actions

1. [Highest priority fix - typically critical violations]
2. [Next priority fix - typically major violations]
3. [Additional improvements - typically minor violations]

### Long-term Improvements

- [Suggestions for enhancing subagent effectiveness]
- [Recommendations for better integration]
- [Ideas for expanding capabilities]

---

## Notes

### Template Instructions

**When creating a validation report:**

1. **Header Information:**
   - Fill in actual subagent file path
   - Use ISO date format (YYYY-MM-DD)
   - Specify reviewer name/agent
   - Indicate if project, user, or plugin subagent

2. **Violations Section:**
   - Number sequentially starting from 1
   - Include exact line numbers or section references
   - Show actual code/content that violates standard
   - Reference specific line numbers from sub-agents.md
   - Classify severity (Critical/Major/Minor)
   - Provide complete, actionable proposed fix

3. **Severity Classification:**
   - **Critical:** Prevents subagent from working (missing required fields, invalid
     syntax)
   - **Major:** Reduces effectiveness or violates best practices (vague description,
     inappropriate tools)
   - **Minor:** Could be improved but functional (missing proactive language,
     could be more detailed)

4. **Summary Statistics:**
   - Count total violations
   - Break down by category (matches checklist sections)
   - Break down by severity
   - Calculate compliance rate: `(passed_checks / total_checks) * 100`
   - Assess production readiness

5. **Recommendation:**
   - Provide clear next steps
   - Prioritize fixes by severity
   - Include both immediate actions and long-term improvements
   - Be specific and actionable

**Formatting Guidelines:**

- Use triple backticks with `markdown` or `yaml` language tags for code blocks
- Use consistent heading levels (## for major sections, ### for violations)
- Include line numbers in violation titles when applicable
- Keep proposed fixes complete enough to implement directly
- Use checkbox format for production readiness assessment

**Common Violation Categories:**

- **File Structure:** Wrong location, wrong extension, no frontmatter
- **YAML Issues:** Missing required fields, invalid naming, syntax errors
- **Content Issues:** Empty prompt, vague description, no role definition
- **Effectiveness Issues:** Too broad, inappropriate tools, wrong model
- **Integration Issues:** Naming conflicts, accessibility problems

**Output Location:**

Save completed reports to:
`docs/reviews/subagent-[subagent-name]-review-[YYYY-MM-DD].md`

Examples:

- `docs/reviews/subagent-code-reviewer-review-2025-11-04.md`
- `docs/reviews/subagent-test-runner-review-2025-11-04.md`

---

## Example Violations

### Example 1: Missing Required Field

**VIOLATION #X: YAML Frontmatter - Missing required `description` field**

**Current:**

```yaml
---
name: code-reviewer
tools: Read, Grep, Glob
---
```

**Standard violated:** sub-agents.md line 151 "`description` | Yes | Required"

**Severity:** Critical

**Proposed fix:**

```yaml
---
name: code-reviewer
description: Expert code review specialist. Use immediately after writing or
modifying code.
tools: Read, Grep, Glob
---
```

---

### Example 2: Invalid Naming Convention

**VIOLATION #X: YAML Frontmatter - Invalid `name` format uses uppercase**

**Current:**

```yaml
---
name: Code-Reviewer
description: Reviews code for quality
---
```

**Standard violated:** sub-agents.md line 150 "lowercase letters and hyphens"

**Severity:** Critical

**Proposed fix:**

```yaml
---
name: code-reviewer
description: Reviews code for quality
---
```

---

### Example 3: Insufficient System Prompt

**VIOLATION #X: System Prompt - Too brief, lacks specific instructions**

**Current:**

```markdown
---
name: debugger
description: Debugs code issues
---

You are a debugger. Fix bugs.
```

**Standard violated:** sub-agents.md line 390 "Include specific instructions,
examples, and constraints"

**Severity:** Major

**Proposed fix:**

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected
behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:

1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:

- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:

- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```

---

### Example 4: Overly Broad Responsibility

**VIOLATION #X: Functional Effectiveness - Subagent tries to do too much**

**Current:**

```markdown
---
name: developer-assistant
description: Helps with all development tasks
tools: Read, Write, Edit, Bash, Grep, Glob
---

You help with coding, testing, deployment, documentation, and code review.
```

**Standard violated:** sub-agents.md line 388 "single, clear responsibilities"

**Severity:** Major

**Proposed fix:**

Create separate focused subagents:

- `code-reviewer`: For code review only
- `test-runner`: For running and fixing tests
- `doc-writer`: For documentation tasks

Each with specific, focused system prompts and appropriate tool access.

---

## Cross-Reference

This template is used in conjunction with:

- **Checklist:** `docs/checklists/subagent-validation-checklist.md`
- **Best Practices:** `docs/notes/checklists-and-templates-best-practices.md`
- **Standard Source:**
  `plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md`
