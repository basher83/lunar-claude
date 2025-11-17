---
description: "Create a skill using the proven skill-creator workflow with research context"
allowed-tools: Bash(command:*)
argument-hint: SKILL_NAME RESEARCH_DIR
---

# Skill Create

Create a skill using the proven skill-creator workflow with research context.

## Arguments

- `skill-name` - Name of the skill to create (e.g., docker-master)
- `research-dir` - Path to directory containing research materials

## Usage

```bash
/skill-create <skill-name> <research-dir>
```

## Your Task

Your task is to invoke the skill-creator skill to guide through the complete creation workflow:

1. Understanding (uses research as context)
2. Planning skill contents
3. Initializing structure (init_skill.py)
4. Editing SKILL.md and resources
5. Packaging (package_skill.py)
6. Iteration

## Instructions

Invoke the skill-creator skill using the Skill tool. Use the following syntax:

```text
Skill(skill: "example-skills:skill-creator")
```

Then provide this instruction to the skill:

```text
I need to create a new skill called <skill-name>.

Research materials are available at: <research-dir>

Please guide me through the skill creation process using this research as context for:
- Understanding the skill's purpose and use cases
- Planning reusable resources (scripts, references, assets)
- Implementing SKILL.md with proper structure
- Creating supporting files if needed

Output location: plugins/meta/meta-claude/skills/<skill-name>/
```

If a custom output location is specified in the arguments (e.g., a different
plugin directory), replace the output location in the instruction with the
user-specified path.

## Expected Workflow

Your task is to guide through these phases using skill-creator:

1. **Understanding:** Review research to identify use cases
2. **Planning:** Determine scripts, references, assets needed
3. **Initializing:** Run init_skill.py to create structure
4. **Editing:** Implement SKILL.md and bundled resources
5. **Packaging:** Run package_skill.py for distribution
6. **Iteration:** Refine based on testing

## Error Handling

**If research-dir missing:**

- Report error: "Research directory not found at `<research-dir>`"
- Suggest: Run `/skill-research` first or provide correct path
- Exit with failure

**If skill-creator errors:**

- Report the specific error from skill-creator
- Preserve research materials
- Exit with failure

## Examples

**Create skill from research:**

```bash
/skill-create docker-master docs/research/skills/docker-master/
# Output: Skill created at plugins/meta/meta-claude/skills/docker-master/
```

**With custom output location:**

```bash
/skill-create coderabbit plugins/meta/claude-dev-sandbox/skills/coderabbit/ plugins/code-review/claude-dev-sandbox/skills/
# Note: When custom output path is provided as third argument, use it instead of default
# Output: Skill created at plugins/code-review/claude-dev-sandbox/skills/coderabbit/
```
