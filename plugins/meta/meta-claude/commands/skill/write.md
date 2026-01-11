---
description: "Write SKILL.md content by synthesizing references into actionable guidance"
allowed-tools: Read, Edit, Glob, Bash(ls:*)
argument-hint: skill-path
---

# Skill Write

Write the SKILL.md content for an initialized skill by synthesizing its references into actionable guidance.

## Arguments

- `$1` - Path to the skill directory (e.g., `plugins/meta/meta-claude/skills/coderabbit`)

## Usage

```bash
# Write content for an initialized skill
/meta-claude:skill:write plugins/meta/meta-claude/skills/coderabbit
```

## Prerequisites

The skill must already be initialized with:

- `SKILL.md` file (even if template with TODOs)
- `references/` directory with source materials

If not initialized, run `/meta-claude:skill:create` first.

## Instructions

### Step 1: Inventory the Skill

List the skill contents:

```bash
ls -la $1/
ls -la $1/references/
```

Read the current SKILL.md to understand the template structure.

### Step 2: Read All References

Read every file in `references/` to understand the domain:

- What is this skill about?
- What are the key concepts, commands, configurations?
- What workflows or processes does it enable?
- What are common use cases and examples?

### Step 3: Write the Frontmatter

The frontmatter is the **most critical part** - it determines when the skill triggers.

```yaml
---
name: <skill-name>
description: >
  <What the skill does>. Use when <specific triggers>: (1) <trigger 1>,
  (2) <trigger 2>, (3) <trigger 3>, or <other contexts>.
---
```

**Description requirements:**

- Include BOTH what the skill does AND when to use it
- List specific trigger phrases users might say
- Include file types, tools, or contexts that should activate this skill
- Be comprehensive - the body is only loaded AFTER triggering

**Example:**

```yaml
description: >
  Configure and use CodeRabbit for automated code reviews. Use when setting up
  .coderabbit.yaml, configuring review rules, understanding CodeRabbit commands,
  or integrating CodeRabbit with CI/CD pipelines.
```

### Step 4: Write the Body

Structure the body with these sections (adapt as needed):

```markdown
# <Skill Name>

<1-2 sentence overview of what this skill enables>

## Quick Start

<Most common use case with concrete example>

## Key Concepts

<Essential concepts extracted from references - only what Claude doesn't know>

## Common Workflows

<Step-by-step workflows for primary use cases>

## Configuration

<Key configuration options with examples>

## References

<Links to reference files for detailed documentation>
```

**Writing principles:**

1. **Concise is key** - Claude is smart. Only add what Claude doesn't already know.
2. **Prefer examples over explanations** - Show, don't tell.
3. **Use imperative form** - "Configure X" not "You can configure X"
4. **Progressive disclosure** - Essential info first, details in references
5. **Actionable content** - Every section should help Claude DO something

### Step 5: Validate Content

After writing, self-check:

- [ ] Description includes trigger phrases?
- [ ] Quick Start has a concrete, runnable example?
- [ ] Content is domain-specific (not general knowledge)?
- [ ] References are linked appropriately?
- [ ] No placeholder TODOs remain?

## Output

After writing the content, report:

```text
✅ SKILL.md content written for <skill-name>

Summary:
- Description: <brief summary of triggers>
- Sections: <list of main sections added>
- References linked: <count>

Next: Run /meta-claude:skill:review-content to validate quality
```

## Error Handling

**If SKILL.md not found:**

```text
❌ Error: SKILL.md not found at <skill-path>
Run /meta-claude:skill:create first to initialize the skill.
```

**If no references found:**

```text
⚠️ Warning: No references found in <skill-path>/references/
Writing content from general knowledge only.
Consider running /meta-claude:skill:research to gather source materials.
```

**If references are empty/minimal:**

```text
⚠️ Warning: References contain minimal content.
Content quality may be limited. Consider adding more research materials.
```

## Examples

**Write content for coderabbit skill:**

```bash
/meta-claude:skill:write plugins/meta/claude-dev-sandbox/skills/coderabbit

# Reads all references in references/
# Synthesizes into comprehensive SKILL.md
# Reports completion with summary
```

## Notes

- This command performs the "write content" step in the skill-factory workflow
- Focus on synthesizing references, not copying them verbatim
- The goal is actionable guidance that helps Claude accomplish tasks
- Reference files remain available for detailed lookups
