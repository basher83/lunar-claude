---
description: "Create a skill from research materials or from scratch"
allowed-tools: Bash(command:*)
argument-hint: [skill-name] [research-dir] [output-dir]
---

# Skill Create

Create a new skill, optionally from research materials.

## Arguments

- `$1` - Name of the skill to create (e.g., coderabbit)
- `$2` - (Optional) Path to research materials directory
- `$3` - (Optional) Output directory (defaults to plugins/meta/meta-claude/skills/)

## Usage

```bash
# Create skill from research
/meta-claude:skill:create coderabbit docs/research/coderabbit/

# Create skill with custom output location
/meta-claude:skill:create coderabbit docs/research/coderabbit/ plugins/code-review/skills/

# Create empty skill (no research)
/meta-claude:skill:create my-skill
```

## Instructions

Run the init_skill.py script to create the skill structure:

### With Research Materials

```bash
${CLAUDE_PLUGIN_ROOT}/skills/skill-creator/scripts/init_skill.py $1 \
    --path ${3:-plugins/meta/meta-claude/skills/} \
    --research-dir $2
```

### Without Research (Empty Skill)

```bash
${CLAUDE_PLUGIN_ROOT}/skills/skill-creator/scripts/init_skill.py $1 \
    --path ${3:-plugins/meta/meta-claude/skills/}
```

## What the Script Does

**With research (`--research-dir`):**

1. Creates skill directory at output path
2. Copies all `.md` files from research to `references/`
3. Generates SKILL.md with links to all references
4. Flattens nested paths (e.g., `cli/commands.md` → `cli-commands.md`)

**Without research:**

1. Creates skill directory with basic template
2. Creates empty `scripts/`, `references/`, `assets/` directories
3. Generates SKILL.md with TODOs

## After Creation

Report the results and remind the user:

```text
✅ Skill created at <output-path>

Next steps:
1. Edit SKILL.md - complete description and add content
2. Review references/ - remove unnecessary files
3. Run /meta-claude:skill:review-content to validate
```

## Error Handling

**If skill already exists:**

```text
❌ Error: Skill directory already exists: <path>
```

Suggest: Delete existing or choose different name

**If research directory not found:**

```text
❌ Error: Research directory not found: <path>
```

Suggest: Check path or run `/meta-claude:skill:research` first

## Examples

**Create skill from research:**

```bash
/meta-claude:skill:create coderabbit docs/research/coderabbit/
# Creates: plugins/meta/meta-claude/skills/coderabbit/
# With references from research
```

**Create empty skill:**

```bash
/meta-claude:skill:create my-helper
# Creates: plugins/meta/meta-claude/skills/my-helper/
# With template SKILL.md and empty directories
```
