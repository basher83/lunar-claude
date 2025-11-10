# Quick Reference: Using claude-skill-auditor v2

## When to Use

✅ **ALWAYS use after:**
- Creating a new skill
- Modifying SKILL.md
- Adding/removing supporting files
- Before submitting for review
- Before distributing to team

## How to Invoke

### Basic Audit

```
Audit the [skill-name] skill
```

or

```
Please review plugins/meta/meta-claude/skills/multi-agent-composition/ for compliance
```

### Thorough Audit with Context

```
I just finished creating/updating the [skill-name] skill.
Please conduct a comprehensive audit against official skill-creator standards.
Pay special attention to:
- Forbidden files
- Content duplication
- Description triggers
```

## What the Auditor Will Do

### Automatic Steps (You Don't Need to Ask)

1. ✅ Reads `/mnt/skills/examples/skill-creator/SKILL.md`
2. ✅ Locates your skill directory
3. ✅ Reads all files in the skill
4. ✅ Runs bash verification commands
5. ✅ Checks all requirements systematically
6. ✅ Generates detailed report

## Reading the Report

### Status Indicators

- **✅ PASS** = 100% official requirements + 80%+ best practices
- **⚠️ NEEDS IMPROVEMENT** = 100% official requirements + <80% best practices
- **❌ FAIL** = Missing official requirements

### Issue Priorities

**❌ CRITICAL** = Must fix (violates skill-creator requirements)
- These block the skill from working correctly
- Fix these first before anything else

**⚠️ WARNING** = Should fix (violates best practices)
- These reduce skill effectiveness
- Fix after critical issues

**💡 SUGGESTION** = Nice to have (improvements)
- These enhance quality
- Optional, do if time permits

## Common Critical Issues

### 1. README.md Exists

**Why it's critical:** Explicitly forbidden by skill-creator

**How to fix:**
```bash
rm skill-directory/README.md
```

**What to do:** All content should be in SKILL.md or reference/ files, not README.md

---

### 2. Content Duplication

**Why it's critical:** Violates "information lives in either SKILL.md or references, not both"

**How to fix:**
1. Identify duplicated content
2. Keep detailed explanation ONLY in reference/ file
3. In SKILL.md, replace with: "See [reference/file.md](reference/file.md)"

**Example:**
```markdown
❌ WRONG:
# SKILL.md
## The Core 4 Framework
Context, Model, Prompt, Tools are the four pillars...
[500 words of explanation]

# reference/core-4.md
## The Core 4 Framework
Context, Model, Prompt, Tools are the four pillars...
[Same 500 words repeated]

✅ RIGHT:
# SKILL.md
## Quick Navigation
**The Core 4 Framework** → See [reference/core-4-framework.md](reference/core-4-framework.md)

# reference/core-4-framework.md
## The Core 4 Framework
Context, Model, Prompt, Tools are the four pillars...
[Full explanation here only]
```

---

### 3. Reserved Words in Name

**Why it's critical:** "claude" and "anthropic" are reserved

**How to fix:**
```bash
# Rename the skill
mv composing-claude-code multi-agent-composition

# Update SKILL.md frontmatter
name: multi-agent-composition  # not "composing-claude-code"
```

---

### 4. Invalid YAML Frontmatter

**Why it's critical:** Skill won't load without valid YAML

**Common mistakes:**
```yaml
❌ WRONG:
---
name: my-skill
description: This is great!
author: Me
tags: [cool, awesome]
---

✅ RIGHT:
---
name: my-skill
description: This is great!
---

# Only name and description (and optionally allowed-tools, license)
# No other fields allowed
```

---

### 5. Triggers Not in Description

**Why it's critical:** Body loads AFTER triggering, so triggers must be in description

**How to fix:**
```yaml
❌ WRONG:
description: Helps with document processing

# SKILL.md body
## When to Use
Use when creating Word documents, editing PDFs, or...

✅ RIGHT:
description: >
  Comprehensive document processing for Word and PDF files.
  Use when: (1) Creating Word documents, (2) Editing PDFs,
  (3) Converting between formats, (4) Extracting text from documents

# Body loads AFTER skill triggers, so it's too late
```

## Acting on the Report

### 1. Start with Critical Issues

```markdown
## Critical Issues ❌

### Issue 1: README.md exists
Fix: rm README.md

### Issue 2: Content duplication in SKILL.md
Fix: Move explanations to reference/ files
```

**Do these first.** Don't move to warnings until all critical issues are resolved.

### 2. Address Warnings

```markdown
## Warnings ⚠️

### Warning 1: SKILL.md over recommended size
Recommended: Split into reference files
```

**Fix these for quality.** The skill will work but won't be optimal.

### 3. Consider Suggestions

```markdown
## Suggestions 💡

### Suggestion 1: Could use gerund naming
Benefit: Follows convention
```

**Optional improvements.** Do if you have time and they make sense.

## Re-Auditing After Fixes

After fixing issues:

```
I've addressed the critical issues. Please re-audit the skill.
```

The auditor will run the same checks and generate a new report showing improvement.

## Quick Fixes Reference

| Issue | Quick Fix |
|-------|-----------|
| README.md exists | `rm README.md` |
| Backslashes in paths | Find/replace `\` with `/` |
| Name has "claude" | Rename skill to avoid reserved word |
| SKILL.md too long | Split content into reference/ files |
| Content duplication | Keep detailed content only in reference/ |
| Missing description triggers | Add "Use when: (1)... (2)... (3)..." to description |
| Not third person | Change "I can help" to "Provides..." |

## Getting Help

If the auditor finds issues you don't understand:

```
I don't understand issue #2 about content duplication.
Can you explain what needs to change and show me before/after examples?
```

The auditor can provide more detail and examples for any issue.

## Best Practices

✅ **DO:**
- Audit before submitting for review
- Fix critical issues immediately
- Re-audit after making changes
- Ask for clarification if needed

❌ **DON'T:**
- Skip critical issues to fix warnings first
- Ignore content duplication (very common mistake)
- Forget to check for README.md
- Assume v1 audit results are still valid

## Example Workflow

1. Create/update skill
2. Run auditor: "Audit the my-skill skill"
3. Review report, note critical issues
4. Fix critical issues first
5. Re-audit: "Re-audit my-skill"
6. Fix warnings if time permits
7. Re-audit one final time
8. When report shows ✅ PASS, skill is ready

## Common Questions

**Q: The auditor said my README.md must be deleted, but I need documentation for users!**

A: Skills are for AI agents, not humans. Put user documentation in your project's main README or docs folder, outside the skill directory. The skill itself should only contain what the AI agent needs.

**Q: I have the same concept in both SKILL.md and a reference file. Isn't that helpful?**

A: No - it's duplication that wastes tokens. Keep the full explanation ONLY in the reference file. SKILL.md should just link to it. Claude is smart enough to read the reference when needed.

**Q: My SKILL.md is 400 lines. The limit is 500, so why is it a warning?**

A: For knowledge base skills, SKILL.md should primarily be a navigation hub (~100-150 lines), not comprehensive documentation. If you're approaching 500 lines, content should be in reference files.

**Q: The old auditor said my skill was perfect. Why does v2 find issues?**

A: v2 reads the actual skill-creator documentation and checks for requirements v1 didn't know about (forbidden files, content duplication). The issues were always there; v1 just didn't catch them.

---

**Remember:** The auditor is your quality gate. Use it every time. "Trust but verify."
