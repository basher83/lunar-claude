---
name: skill-creator
description: Creates Agent Skills with proper structure, referencing official Claude Code documentation for accuracy
---

# Skill Creator

## Overview

Creates properly formatted Agent Skills for Claude Code plugins. Extends Anthropic's base skill-creator with official plugin documentation references.

**When to use:** User asks to create a skill, wants to add a skill to a plugin, or needs help structuring skill documentation.

**References:** Consult `ai_docs/plugins-referance.md` and official skill documentation for current specifications.

## Skill Structure Requirements

Every skill MUST include:

1. **Frontmatter** with `name` and `description`
2. **Overview** section explaining purpose and usage
3. **Process** or workflow sections
4. **Examples** showing concrete usage
5. Located in `skills/skill-name/SKILL.md`

## Creation Process

### Step 1: Gather Requirements

Ask the user:
- What task should this skill help with?
- When should Claude invoke this skill?
- What are the key steps or phases?

### Step 2: Determine Skill Name

Create kebab-case name from purpose:
- "code review" → `code-reviewer`
- "terraform planning" → `terraform-planner`
- "test generation" → `test-generator`

### Step 3: Structure the Skill

Use this template structure:

```markdown
---
name: skill-name
description: One-line description of what this skill does
---

# Skill Title

## Overview

Brief explanation of the skill's purpose and when Claude should use it.

## Quick Reference (if applicable)

Table or list of key phases/steps.

## Process

### Phase 1: [Name]

Detailed steps for this phase.

### Phase 2: [Name]

Detailed steps for this phase.

## Key Principles

- Important guidelines
- Best practices
- Common pitfalls to avoid

## Examples

Concrete usage examples showing input → process → output.
```

### Step 4: Reference Official Docs

Before finalizing, check:
- `ai_docs/plugins-referance.md` for skill structure requirements
- Official Claude Code docs for latest patterns
- Existing skills in superpowers plugin for proven patterns

### Step 5: Create Skill File

Place skill at: `skills/[skill-name]/SKILL.md`

## Key Principles

- **Clarity**: Skills must clearly state when Claude should use them
- **Completeness**: Include all information needed to execute the task
- **Concreteness**: Provide specific examples, not abstract guidance
- **Consistency**: Follow established patterns from official documentation

## Examples

**Example 1: Creating a Code Review Skill**

User: "Help me create a skill for reviewing code changes"

Process:
1. Gather: Review should check style, logic, tests, documentation
2. Name: `code-reviewer`
3. Structure: Include phases for analysis, feedback, verification
4. Reference: Check official docs for review best practices
5. Create: Write SKILL.md with complete review process

Output: `skills/code-reviewer/SKILL.md` with structured review workflow

**Example 2: Creating a Database Migration Skill**

User: "I need a skill for creating database migrations"

Process:
1. Gather: Should generate migration files, validate schema, handle rollback
2. Name: `migration-creator`
3. Structure: Phases for schema analysis, migration generation, testing
4. Reference: Check database and migration patterns
5. Create: Write SKILL.md with migration workflow

Output: `skills/migration-creator/SKILL.md` with migration process
