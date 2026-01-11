---
description: "Create a skill directory structure from scratch"
allowed-tools: Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Read, Write
argument-hint: [skill-name] [output-dir]
---

# Skill Create

Create a new skill directory with proper structure.

## Arguments

- `$1` - Name of the skill (kebab-case, e.g., terraform-helper)
- `$2` - (Optional) Output directory (defaults to current plugin's skills/)

## Instructions

Create the skill directory structure:

```bash
mkdir -p "${2:-plugins/meta/meta-claude/skills}/$1"/{references,scripts}
```

Then create a SKILL.md template with proper frontmatter:

```markdown
---
name: $1
description: >
  TODO: Add description. Include trigger phrases like "use when creating...",
  "building...", "validating...", or explicit feature keywords users might mention.
---

# [Skill Title]

TODO: Add skill content.

## When to Use

TODO: Describe when this skill should be invoked.

## Instructions

TODO: Add step-by-step instructions for Claude to follow.
```

## After Creation

Report results:

```text
✅ Skill created at <output-path>/$1/

Structure:
  SKILL.md      - Main skill definition (needs content)
  references/   - Supporting documentation
  scripts/      - Helper scripts

Next steps:
1. Edit SKILL.md with actual content
2. Add reference files if needed
3. Run /meta-claude:skill:review-compliance to validate
```

## Error Handling

**If skill already exists:**

```text
❌ Error: Skill directory already exists: <path>
```

Suggest: Delete existing or choose different name.

**If invalid name format:**

```text
❌ Error: Invalid skill name. Use kebab-case (lowercase, hyphens only).
```
