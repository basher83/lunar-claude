---
description: Run technical compliance validation on a skill using quick_validate.py
argument-hint: [skill-path]
---

# Skill Review Compliance

Your task is to run technical compliance validation on a skill using quick_validate.py and report the results.

## Usage

```bash
/meta-claude:skill:review-compliance /path/to/skill
```

## What This Does

Validates:

- SKILL.md file exists
- YAML frontmatter is valid
- Required fields present (name, description)
- Name follows hyphen-case convention (max 64 chars)
- Description has no angle brackets (max 1024 chars)
- No unexpected frontmatter properties

## Instructions

Run the quick_validate.py script from skill-creator with the skill path provided by the user:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/skill-creator/scripts/quick_validate.py $ARGUMENTS
```

Where `$ARGUMENTS` is the skill path provided by the user.

**Expected output if valid:**

```text
Skill is valid!
```

**Expected output if invalid:**

```text
[Specific error message describing the violation]
```

## Error Handling

**If validation passes:**

- Report: "✅ Compliance validation passed"
- Exit with success

**If validation fails:**

- Report the specific violation
- Include categorization in output: "This is a Tier 1 (auto-fix)" or "This is a Tier 3 (manual fix)"
- Exit with failure

**Tier 1 (Auto-fix) examples:**

- Missing description → Add generic description
- Invalid YAML → Fix YAML syntax
- Name formatting → Convert to hyphen-case

**Tier 3 (Manual fix) examples:**

- Invalid name characters
- Description too long
- Unexpected frontmatter keys

## Examples

**Valid skill:**

```bash
/meta-claude:skill:review-compliance plugins/meta/meta-claude/skills/skill-creator
# Output: Skill is valid!
```

**Invalid skill:**

```bash
/meta-claude:skill:review-compliance plugins/example/broken-skill
# Output: Missing 'description' in frontmatter. This is a Tier 1 (auto-fix)
```
