# The Checklist-Template-Subagent Pattern

**Created:** 2025-11-04
**Context:** Core insight connecting checklists, templates, and subagents into a reusable validation pattern

---

## The Core Insight

**Checklists and templates are not just documentation - they are decomposed system prompts that enable specialized validation subagents.**

When you create a checklist/template pair, you are creating the **instructions** that a fresh subagent can use to perform expert validation with zero prior context.

---

## The Pattern Explained

### What Each Component Does

**Checklist = The Methodology**
- Defines WHAT to validate
- Specifies HOW to verify each criterion
- Provides the step-by-step process
- Contains objective, verifiable criteria
- References authoritative sources

**Template = The Output Format**
- Defines HOW to structure findings
- Specifies required report sections
- Ensures consistent reporting
- Makes results actionable

**Subagent = The Executor**
- Follows the checklist methodology
- Produces output in template format
- Operates in isolated context
- Can be invoked on-demand

### How They Fit Together

```yaml
---
name: [thing]-validator
description: Validates [thing] against official standards. Use when reviewing any [thing].
tools: Read, Grep, Glob
model: sonnet
---

# Your Role
You are a [thing] validation specialist.

# Your Process
Follow docs/checklists/[thing]-validation-checklist.md exactly:
1. [Step 1 from checklist]
2. [Step 2 from checklist]
3. [Step 3 from checklist]
...

# Your Output
Report findings using docs/templates/[thing]-validation-report-template.md:
- [Section 1 from template]
- [Section 2 from template]
- [Section 3 from template]
...
```

The checklist and template **ARE** the subagent's system prompt - just externalized and reusable.

---

## Why "Zero-Context Friendly" Finally Makes Sense

When we said checklists must be **"usable by a fresh subagent with zero context"**, we meant it **literally**.

The checklist will BE the instructions for a subagent that:
- Has never seen this codebase
- Doesn't know the project context
- Has no memory of previous conversations
- Starts with a clean context window

That's why checklists must:

✅ **Reference exact line numbers** - Subagent can look them up
✅ **Provide complete examples** - Subagent has no prior context
✅ **Use objective criteria** - Subagent needs clear yes/no answers
✅ **Include workflow steps** - Subagent needs explicit process
✅ **Avoid nested code blocks** - Prevents technical/linting issues
✅ **Be self-contained** - No assumed knowledge

**The checklist IS the subagent's training manual.**

---

## The Reusable Design Pattern

### Pattern Template

```text
1. Identify something that needs validation (subagents, CLAUDE.md, skills, hooks, etc.)
2. Find the authoritative standard (official docs, spec, best practices)
3. Create validation checklist (extract objective criteria from standard)
4. Create report template (define how to present findings)
5. Create validation subagent (references checklist + template in system prompt)
6. Subagent can now validate ANY instance of that thing
```

### Concrete Examples

**Example 1: CLAUDE.md Validation**
- Standard: `plugins/meta/claude-docs/.../memory.md`
- Checklist: `docs/checklists/claude.md-validation-checklist.md`
- Template: `docs/templates/claude-md-validation-report-template.md`
- Subagent: `claude-md-validator` (uses checklist + template)
- Result: Can validate ANY CLAUDE.md file against official standards

**Example 2: Subagent Validation**
- Standard: `plugins/meta/claude-docs/.../sub-agents.md`
- Checklist: `docs/checklists/subagent-validation-checklist.md`
- Template: `docs/templates/subagent-validation-report-template.md`
- Subagent: `subagent-validator` (uses checklist + template)
- Result: Can validate ANY subagent file against official standards

**Example 3: Future Pattern**
- Standard: `plugins/meta/claude-docs/.../skills.md`
- Checklist: `docs/checklists/skill-validation-checklist.md` (to be created)
- Template: `docs/templates/skill-validation-report-template.md` (to be created)
- Subagent: `skill-validator` (to be created)
- Result: Could validate ANY skill against official standards

---

## The Complete Workflow

### Creating a New Validation System

**Step 1: Create Checklist**
```markdown
# [Thing] Validation Checklist

## 1. [Category Name]

- [ ] **[Specific criterion]**
  - How to verify it
  - **Standard:** [source file] line [X]
  - **Correct example:** [simple example]
  - **Incorrect example:** [simple example]
```

**Step 2: Create Template**
```markdown
# [Thing] Standards Compliance Review

**File:** [path]
**Date:** [YYYY-MM-DD]

## Violations Found

### VIOLATION #1: [Description]

**Current:** [code]
**Standard violated:** [standard] line [X]
**Proposed fix:** [code]
```

**Step 3: Create Subagent**
```yaml
---
name: [thing]-validator
description: Validates [thing] against official standards
tools: Read, Grep, Glob
model: sonnet
---

You are a [thing] validation specialist.

Follow docs/checklists/[thing]-validation-checklist.md
Report using docs/templates/[thing]-validation-report-template.md
```

**Step 4: Use the Subagent**
```bash
> Use the [thing]-validator subagent to review [file-path]
```

### Using an Existing Validation System

```bash
# Validate a CLAUDE.md file
> Use the claude-md-validator subagent to review ./CLAUDE.md

# Validate a subagent file
> Use the subagent-validator subagent to review .claude/agents/code-reviewer.md

# Validate multiple files
> Use the subagent-validator to review all subagents in .claude/agents/
```

---

## Why This Pattern Is Powerful

### 1. Reusability
- Create checklist/template once
- Use for infinite validations
- Works across projects
- Shareable with teams

### 2. Consistency
- Same criteria every time
- Same report format every time
- No drift in standards
- Objective evaluations

### 3. Scalability
- Validate 1 file or 1000 files
- Same quality of review
- No fatigue or inconsistency
- Parallelizable

### 4. Knowledge Codification
- Expert knowledge captured in checklist
- Best practices embedded in criteria
- Standards enforced automatically
- Transferable to any AI worker

### 5. Context Efficiency
- Subagent uses separate context window
- Main conversation stays focused
- Deep validation without pollution
- Can resume if needed

### 6. Continuous Improvement
- Update checklist → all future validations improve
- Update template → all future reports improve
- Update subagent → all future executions improve
- Version controlled for tracking changes

---

## Design Principles That Flow From This Understanding

### For Checklists

**Because checklists are system prompt components:**

1. **Must be completely objective** - Subagent can't make subjective judgments
2. **Must reference sources** - Subagent needs to verify criteria
3. **Must avoid nested code blocks** - Technical/linting issues break subagent workflow
4. **Must include examples** - Subagent has no prior knowledge
5. **Must be self-contained** - Subagent starts with zero context
6. **Must have clear workflow** - Subagent needs explicit process

### For Templates

**Because templates are output format specifications:**

1. **Must be standardized** - Ensures consistency across validations
2. **Must be actionable** - Report recipients need clear next steps
3. **Must include metadata** - Track what/when/who validated
4. **Must show violations clearly** - Current → Fixed transformation
5. **Must calculate metrics** - Compliance rates, severity breakdown
6. **Must include instructions** - For filling out the template correctly

### For Subagents Using These

**Because subagents execute checklist/template pairs:**

1. **Tools must match checklist needs** - If checklist says "read file", need Read tool
2. **Model must match complexity** - Complex validation needs sonnet/opus
3. **Description must trigger correctly** - Use "PROACTIVELY" or explicit invocation
4. **System prompt must reference both** - Checklist for process, template for output
5. **Focus must be single-purpose** - Validation only, not fixing

---

## Common Mistakes to Avoid

### Mistake 1: Making Checklists "Documentation"

❌ **Wrong Thinking:**
"This checklist is for human developers to read and understand the standards."

✅ **Right Thinking:**
"This checklist IS the executable instructions for an AI validation worker."

**Impact:** Vague criteria, missing references, assumed context → subagent fails

### Mistake 2: Subjective Criteria

❌ **Wrong:**
```markdown
- [ ] Code quality is good
- [ ] Documentation is adequate
```

✅ **Right:**
```markdown
- [ ] **Maximum line length is 100 characters**
  - Check each line length
  - **Standard:** PEP 8 line 15
  - **How to verify:** Count characters per line
```

**Impact:** Subagent can't verify subjective criteria → inconsistent results

### Mistake 3: Nesting Code Blocks in Examples

❌ **Wrong:**
````markdown
- **Correct example:**
  ```markdown
  ```bash
  npm test
  ```
  ```
````

✅ **Right:**
```markdown
- **Correct example:**
  - Command in code block: `npm test`
  - Or describe pattern without nesting
```

**Impact:** Linting fails, subagent gets confused → validation breaks

### Mistake 4: Not Referencing Standards

❌ **Wrong:**
```markdown
- [ ] Name should be lowercase with hyphens
```

✅ **Right:**
```markdown
- [ ] **Name uses lowercase letters and hyphens**
  - **Standard:** sub-agents.md line 150
```

**Impact:** Can't verify correctness, appears arbitrary → trust issues

### Mistake 5: Missing Workflow

❌ **Wrong:**
```markdown
Check these 20 things [bullet list]
```

✅ **Right:**
```markdown
## Validation Workflow

1. Read the file completely
2. Validate section 1 (frontmatter)
3. Validate section 2 (content)
4. Generate report using template
```

**Impact:** Subagent doesn't know order of operations → inefficient or incorrect

---

## Extending the Pattern

### New Validation Domains

This pattern works for ANY validation task:

**Potential Applications:**
- Skill validation (`skill-validation-checklist.md`)
- Hook validation (`hook-validation-checklist.md`)
- Slash command validation (`slash-command-validation-checklist.md`)
- Plugin validation (`plugin-validation-checklist.md`)
- Code quality validation (`code-quality-checklist.md`)
- Documentation validation (`docs-validation-checklist.md`)
- Security validation (`security-checklist.md`)

**The Pattern:**
1. Find authoritative standard
2. Extract objective criteria
3. Create checklist
4. Create template
5. Create subagent
6. Deploy

### Beyond Validation

The pattern extends to other "expert task execution" scenarios:

**Code Review Subagent:**
- Checklist: Code review best practices
- Template: Code review report format
- Subagent: Executes reviews consistently

**Debugging Subagent:**
- Checklist: Debugging methodology (isolate → hypothesize → test → fix)
- Template: Bug report format
- Subagent: Systematic debugging

**Documentation Subagent:**
- Checklist: Documentation standards
- Template: Documentation structure
- Subagent: Writes consistent docs

---

## Integration with Project Workflow

### When to Use This Pattern

**Creating New Standards:**
1. Write the standard/best practice doc
2. Create checklist from it
3. Create template for reporting
4. Create validation subagent

**Enforcing Existing Standards:**
1. Find official standard
2. Create checklist extracting criteria
3. Create template for findings
4. Create validation subagent

**Quality Gates:**
- Pre-commit: Validate changed files
- PR review: Validate new components
- Periodic audit: Validate entire codebase
- Onboarding: Validate team member work

### Example Project Integration

```bash
# In .claude/agents/validators/

# CLAUDE.md validator
.claude/agents/claude-md-validator.md

# Subagent validator
.claude/agents/subagent-validator.md

# Skill validator (future)
.claude/agents/skill-validator.md

# Hook validator (future)
.claude/agents/hook-validator.md
```

**Usage in workflow:**
```bash
# Before committing
> Use claude-md-validator to review ./CLAUDE.md

# Before PR
> Use subagent-validator to review all agents in .claude/agents/

# During review
> Use skill-validator to review new skills in .claude/skills/
```

---

## Maintenance and Evolution

### When to Update

**Update Checklist When:**
- Official standard changes
- New best practices discovered
- Edge cases found
- Criteria prove insufficient

**Update Template When:**
- Report format needs improvement
- Additional metadata needed
- Better presentation found
- Stakeholder requirements change

**Update Subagent When:**
- Tool requirements change
- Model selection needs adjustment
- Description needs tuning
- Integration points change

### Version Control Best Practices

```bash
# Track changes
git add docs/checklists/[thing]-validation-checklist.md
git add docs/templates/[thing]-validation-report-template.md
git add .claude/agents/[thing]-validator.md
git commit -m "feat: update [thing] validation for new standard v2"

# Document in changelog
# Note version in subagent description if needed
```

---

## Success Metrics

### How to Know the Pattern Is Working

**Checklist Quality:**
- ✅ Zero-context validator can use it successfully
- ✅ All criteria are objectively verifiable
- ✅ All standards referenced with line numbers
- ✅ Examples are clear and simple
- ✅ Workflow is complete and sequential

**Template Quality:**
- ✅ Reports are consistent across validations
- ✅ Findings are actionable
- ✅ Fixes are copy-paste ready
- ✅ Metrics are meaningful
- ✅ Format is professional

**Subagent Quality:**
- ✅ Produces correct validations
- ✅ Follows checklist exactly
- ✅ Outputs match template
- ✅ Finds all violations
- ✅ Proposes valid fixes

**Overall Pattern Success:**
- ✅ Validation is repeatable
- ✅ Results are consistent
- ✅ Quality improves over time
- ✅ Knowledge is preserved
- ✅ Onboarding is faster

---

## Key Takeaways

1. **Checklists are executable instructions** - Not just documentation
2. **Templates are output specifications** - Ensure consistency
3. **Together they form subagent prompts** - Decomposed and reusable
4. **Zero-context is literal** - Fresh subagent must succeed
5. **Objectivity is mandatory** - Subagents need verifiable criteria
6. **Pattern is infinitely reusable** - Works for any validation domain
7. **Knowledge is codified** - Expert practices become automated
8. **Context stays clean** - Subagent handles deep work separately

---

## Next Steps

**To Use This Pattern:**

1. Identify something needing validation
2. Read `docs/notes/checklists-and-templates-best-practices.md`
3. Create checklist following that guide
4. Create template following that guide
5. Create subagent referencing both
6. Test with real validation
7. Iterate based on results

**To Improve Existing Implementations:**

1. Review existing checklist against zero-context requirement
2. Review existing template against actionability requirement
3. Create or update corresponding subagent
4. Test validation workflow
5. Document learnings

---

## Related Documentation

- `docs/notes/checklists-and-templates-best-practices.md` - How to create checklist/template pairs
- `docs/checklists/` - All validation checklists
- `docs/templates/` - All report templates
- `plugins/meta/claude-docs/.../sub-agents.md` - Official subagent documentation
- `.claude/agents/` - Project subagents (including validators)

---

## Conclusion

The checklist-template-subagent pattern transforms validation from a manual, inconsistent process into an automated, reliable system.

**The core insight:** Checklists and templates are not supporting documentation for validation - they ARE the validation system itself, executed by specialized subagents.

When you write a checklist, you're programming an AI worker.
When you write a template, you're defining its output format.
When you create a subagent, you're deploying that worker.

This understanding changes everything about how we approach quality, consistency, and knowledge preservation in AI-assisted development.
