# Lunar-Claude Marketplace Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement categorized plugin marketplace structure with template and meta-claude example plugin.

**Architecture:** Create four-category plugin structure (meta, infrastructure, devops, homelab) with reusable template and meta-claude as reference implementation. Uses official Claude Code plugin format with relative path sources.

**Tech Stack:** JSON (marketplace manifest), Markdown (skills, commands, agents, README), Claude Code plugin system.

---

## Task 1: Create Core Directory Structure

**Files:**

- Create: `plugins/meta/`
- Create: `plugins/infrastructure/`
- Create: `plugins/devops/`
- Create: `plugins/homelab/`
- Create: `templates/plugin-template/`

**Step 1: Create category directories**

```bash
mkdir -p plugins/meta
mkdir -p plugins/infrastructure
mkdir -p plugins/devops
mkdir -p plugins/homelab
```

**Step 2: Create template directory**

```bash
mkdir -p templates/plugin-template
```

**Step 3: Verify structure**

Run: `tree -L 2 plugins/ templates/`

Expected output:

```text
plugins/
├── devops
├── homelab
├── infrastructure
└── meta
templates/
└── plugin-template
```

**Step 4: Commit**

```bash
git add plugins/ templates/
git commit -m "feat: create marketplace category and template directories

Add four plugin categories: meta, infrastructure, devops, homelab
Add template directory for plugin scaffolding

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Create New Marketplace Manifest

**Files:**

- Modify: `.claude-plugin/marketplace.json`

**Step 1: Back up existing marketplace.json**

```bash
cp .claude-plugin/marketplace.json .claude-plugin/marketplace.json.backup
```

**Step 2: Write clean marketplace.json**

Complete file content for `.claude-plugin/marketplace.json`:

```json
{
  "name": "lunar-claude",
  "owner": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "metadata": {
    "description": "Personal Claude Code plugin marketplace for homelab and infrastructure automation",
    "version": "0.1.0"
  },
  "plugins": []
}
```

**Step 3: Validate JSON**

Run: `cat .claude-plugin/marketplace.json | jq .`

Expected: JSON parses successfully with no errors

**Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: create clean marketplace manifest

Replace existing marketplace.json with categorized structure
Initial version 0.1.0 with empty plugins array

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Create Plugin Template Structure

**Files:**

- Create: `templates/plugin-template/.claude-plugin/`
- Create: `templates/plugin-template/commands/`
- Create: `templates/plugin-template/agents/`
- Create: `templates/plugin-template/skills/`
- Create: `templates/plugin-template/hooks/`

**Step 1: Create template directories**

```bash
mkdir -p templates/plugin-template/.claude-plugin
mkdir -p templates/plugin-template/commands
mkdir -p templates/plugin-template/agents
mkdir -p templates/plugin-template/skills/example-skill
mkdir -p templates/plugin-template/hooks
```

**Step 2: Add .gitkeep to preserve empty directories**

```bash
touch templates/plugin-template/commands/.gitkeep
```

**Step 3: Verify template structure**

Run: `tree templates/plugin-template/`

Expected:

```text
templates/plugin-template/
├── .claude-plugin
├── agents
├── commands
│   └── .gitkeep
├── hooks
└── skills
    └── example-skill
```

**Step 4: Commit**

```bash
git add templates/plugin-template/
git commit -m "feat: create plugin template directory structure

Add standard Claude Code plugin directories
Include example-skill subdirectory structure

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 4: Create Template Plugin Manifest

**Files:**

- Create: `templates/plugin-template/.claude-plugin/plugin.json`

**Step 1: Write template plugin.json**

Complete file content for `templates/plugin-template/.claude-plugin/plugin.json`:

```json
{
  "name": "PLUGIN_NAME",
  "version": "0.1.0",
  "description": "PLUGIN_DESCRIPTION",
  "author": {
    "name": "basher83"
  },
  "keywords": ["KEYWORD1", "KEYWORD2"]
}
```

**Step 2: Validate JSON**

Run: `cat templates/plugin-template/.claude-plugin/plugin.json | jq .`

Expected: JSON parses successfully

**Step 3: Commit**

```bash
git add templates/plugin-template/.claude-plugin/plugin.json
git commit -m "feat: add template plugin manifest

Template includes placeholders for customization
Standard fields: name, version, description, author, keywords

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 5: Create Template README

**Files:**

- Create: `templates/plugin-template/README.md`

**Step 1: Write template README.md**

Complete file content for `templates/plugin-template/README.md`:

```markdown
# PLUGIN_NAME

PLUGIN_DESCRIPTION

## Installation

Add the lunar-claude marketplace:

\`\`\`bash
/plugin marketplace add owner/lunar-claude
\`\`\`

Install this plugin:

\`\`\`bash
/plugin install PLUGIN_NAME@lunar-claude
\`\`\`

## Components

### Commands

- `/command-name` - Command description

### Agents

- agent-name - Agent description

### Skills

- skill-name - Skill description

### Hooks

- Hook description

## Configuration

Any special configuration notes go here.

## Usage Examples

\`\`\`bash
# Example usage
/command-name argument
\`\`\`

## Version History

- 0.1.0 - Initial release
```

**Step 2: Verify README renders correctly**

Run: `cat templates/plugin-template/README.md`

Expected: Markdown displays with placeholders

**Step 3: Commit**

```bash
git add templates/plugin-template/README.md
git commit -m "feat: add template README with standard sections

Include installation, components, configuration, usage
Placeholders match plugin.json template

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 6: Create Template Example Agent

**Files:**

- Create: `templates/plugin-template/agents/example-agent.md`

**Step 1: Write example agent**

Complete file content for `templates/plugin-template/agents/example-agent.md`:

```markdown
---
description: Example agent demonstrating proper structure
capabilities: ["task-type-1", "task-type-2", "task-type-3"]
---

# Example Agent

This agent demonstrates the proper structure for Claude Code agents. Replace this content with your agent's actual purpose and capabilities.

## Capabilities

- **Task Type 1**: Describe what this agent does for this task type
- **Task Type 2**: Another capability this agent provides
- **Task Type 3**: A third specialized capability

## When to Use This Agent

Claude should invoke this agent when:
- User requests task type 1
- Project needs task type 2 functionality
- Specific problem matches task type 3 patterns

## Context and Examples

Provide concrete examples of when this agent should be used:

**Example 1: Scenario Name**

User asks: "Help me with X"

This agent provides: Specific assistance with X using its capabilities

**Example 2: Another Scenario**

When project has Y characteristic, this agent can help by doing Z.
```

**Step 2: Verify frontmatter**

Run: `head -n 5 templates/plugin-template/agents/example-agent.md`

Expected: Shows YAML frontmatter with description and capabilities

**Step 3: Commit**

```bash
git add templates/plugin-template/agents/example-agent.md
git commit -m "feat: add example agent template

Demonstrates proper frontmatter and structure
Includes capabilities array and usage examples

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 7: Create Template Example Skill

**Files:**

- Create: `templates/plugin-template/skills/example-skill/SKILL.md`

**Step 1: Write example skill**

Complete file content for `templates/plugin-template/skills/example-skill/SKILL.md`:

```markdown
---
name: example-skill
description: Example skill demonstrating proper structure - replace with your skill's purpose
---

# Example Skill

## Overview

This skill demonstrates the proper structure for Claude Code skills. Skills are model-invoked—Claude uses them autonomously based on task context.

**When to use:** Describe when Claude should invoke this skill

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **1. Setup** | Initial preparation | Setup complete |
| **2. Execution** | Main task execution | Task results |
| **3. Validation** | Verify results | Validated output |

## Process

### Phase 1: Setup

Steps for initial setup:
1. Verify prerequisites
2. Gather required information
3. Prepare workspace

### Phase 2: Execution

Main execution steps:
1. Execute primary task
2. Handle edge cases
3. Process results

### Phase 3: Validation

Verification steps:
1. Check output quality
2. Verify completeness
3. Confirm success criteria

## Key Principles

- **Principle 1**: Explanation of first principle
- **Principle 2**: Explanation of second principle
- **Principle 3**: Explanation of third principle

## Examples

**Example 1: Common Use Case**

Input: User requests X
Process: Skill does Y
Output: Result Z

**Example 2: Edge Case**

Input: User requests A with constraint B
Process: Skill adapts by doing C
Output: Modified result D
```

**Step 2: Verify skill structure**

Run: `head -n 10 templates/plugin-template/skills/example-skill/SKILL.md`

Expected: Shows frontmatter with name and description

**Step 3: Commit**

```bash
git add templates/plugin-template/skills/example-skill/
git commit -m "feat: add example skill template

Demonstrates skill frontmatter and process structure
Includes phases, principles, and examples sections

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 8: Create Template Hooks Configuration

**Files:**

- Create: `templates/plugin-template/hooks/hooks.json`

**Step 1: Write hooks.json**

Complete file content for `templates/plugin-template/hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Plugin PLUGIN_NAME loaded'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/example-hook.sh"
          }
        ]
      }
    ]
  }
}
```

**Step 2: Validate JSON**

Run: `cat templates/plugin-template/hooks/hooks.json | jq .`

Expected: JSON parses successfully

**Step 3: Commit**

```bash
git add templates/plugin-template/hooks/hooks.json
git commit -m "feat: add example hooks configuration

Demonstrates SessionStart and PostToolUse hooks
Uses CLAUDE_PLUGIN_ROOT environment variable

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 9: Create Meta-Claude Plugin Structure

**Files:**

- Create: `plugins/meta/meta-claude/.claude-plugin/`
- Create: `plugins/meta/meta-claude/commands/`
- Create: `plugins/meta/meta-claude/skills/`

**Step 1: Create meta-claude directories**

```bash
mkdir -p plugins/meta/meta-claude/.claude-plugin
mkdir -p plugins/meta/meta-claude/commands
mkdir -p plugins/meta/meta-claude/skills/skill-creator
mkdir -p plugins/meta/meta-claude/skills/agent-creator
mkdir -p plugins/meta/meta-claude/skills/hook-creator
mkdir -p plugins/meta/meta-claude/skills/command-creator
```

**Step 2: Verify structure**

Run: `tree plugins/meta/meta-claude/`

Expected:

```text
plugins/meta/meta-claude/
├── .claude-plugin
├── commands
└── skills
    ├── agent-creator
    ├── command-creator
    ├── hook-creator
    └── skill-creator
```

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/
git commit -m "feat: create meta-claude plugin structure

Add directories for four creator skills
Add commands directory for interactive plugin creation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 10: Create Meta-Claude Plugin Manifest

**Files:**

- Create: `plugins/meta/meta-claude/.claude-plugin/plugin.json`

**Step 1: Write meta-claude plugin.json**

Complete file content for `plugins/meta/meta-claude/.claude-plugin/plugin.json`:

```json
{
  "name": "meta-claude",
  "version": "0.1.0",
  "description": "Meta tools for creating Claude Code skills, agents, hooks, and commands",
  "author": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "keywords": ["meta", "tooling", "development", "creator"],
  "homepage": "https://github.com/basher83/lunar-claude"
}
```

**Step 2: Validate JSON**

Run: `cat plugins/meta/meta-claude/.claude-plugin/plugin.json | jq .`

Expected: JSON parses successfully

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/.claude-plugin/plugin.json
git commit -m "feat: add meta-claude plugin manifest

Version 0.1.0 with complete metadata
Keywords optimized for meta tooling discovery

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 11: Create Meta-Claude README

**Files:**

- Create: `plugins/meta/meta-claude/README.md`

**Step 1: Write README**

Complete file content for `plugins/meta/meta-claude/README.md`:

```markdown
# Meta-Claude

Meta tools for creating Claude Code components including skills, agents, hooks, and commands.

## Installation

Add the lunar-claude marketplace:

\`\`\`bash
/plugin marketplace add basher83/lunar-claude
\`\`\`

Install meta-claude:

\`\`\`bash
/plugin install meta-claude@lunar-claude
\`\`\`

## Components

### Skills

Meta-claude provides four creator skills that Claude invokes automatically:

- **skill-creator** - Creates new Agent Skills with proper structure and official documentation references
- **agent-creator** - Generates properly formatted subagent definitions
- **hook-creator** - Creates hook configurations following Claude Code patterns
- **command-creator** - Scaffolds slash commands with frontmatter and examples

### Commands

- `/new-plugin` - Interactive plugin creation wizard that uses the template structure

## Usage

### Autonomous Mode (Skills)

Simply ask Claude to create components:

\`\`\`
"Help me create a skill for processing terraform configurations"
"I need an agent for kubernetes operations"
"Create a hook that runs tests after file edits"
\`\`\`

Claude will automatically use the appropriate creator skill.

### Interactive Mode (Command)

For structured plugin creation:

\`\`\`bash
/new-plugin
\`\`\`

Walks through:
1. Plugin name and description
2. Category selection (meta, infrastructure, devops, homelab)
3. Component selection (skills, agents, hooks, commands)
4. Template application
5. Marketplace.json update

## How It Works

Creator skills reference official Claude Code documentation in `ai_docs/` to ensure generated components follow current specifications. This extends Anthropic's base skill-creator with plugin-specific knowledge.

## Version History

- 0.1.0 - Initial release with four creator skills and new-plugin command
```

**Step 2: Verify README**

Run: `cat plugins/meta/meta-claude/README.md | head -n 20`

Expected: Shows title, description, and installation sections

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/README.md
git commit -m "docs: add meta-claude README

Document skills, commands, and usage patterns
Explain autonomous vs interactive modes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 12: Create Skill-Creator Skill

**Files:**

- Create: `plugins/meta/meta-claude/skills/skill-creator/SKILL.md`

**Step 1: Write skill-creator skill**

Complete file content for `plugins/meta/meta-claude/skills/skill-creator/SKILL.md`:

```markdown
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

\`\`\`markdown
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
\`\`\`

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
```

**Step 2: Verify frontmatter**

Run: `head -n 5 plugins/meta/meta-claude/skills/skill-creator/SKILL.md`

Expected: Shows valid YAML frontmatter

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/skills/skill-creator/
git commit -m "feat: add skill-creator skill

References official docs for accuracy
Provides template structure and examples
Extends Anthropic's base skill-creator

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 13: Create Agent-Creator Skill

**Files:**

- Create: `plugins/meta/meta-claude/skills/agent-creator/SKILL.md`

**Step 1: Write agent-creator skill**

Complete file content for `plugins/meta/meta-claude/skills/agent-creator/SKILL.md`:

```markdown
---
name: agent-creator
description: Generates properly formatted Claude Code subagent definitions with capabilities and usage patterns
---

# Agent Creator

## Overview

Creates subagent definitions for Claude Code plugins. Subagents are specialized assistants that Claude can invoke for specific tasks.

**When to use:** User requests an agent, wants to add specialized subagent to plugin, or needs agent structure guidance.

**References:** Consult `ai_docs/plugins-referance.md` for agent specifications.

## Agent Structure Requirements

Every agent MUST include:

1. **Frontmatter** with `description` and `capabilities` array
2. **Agent title** as h1
3. **Capabilities** section explaining what agent does
4. **When to Use** section with invocation criteria
5. **Context and Examples** with concrete scenarios
6. Located in `agents/agent-name.md`

## Creation Process

### Step 1: Define Agent Purpose

Ask the user:
- What specialized task does this agent handle?
- What capabilities distinguish it from other agents?
- When should Claude invoke this vs doing work directly?

### Step 2: Determine Agent Name

Create descriptive kebab-case name:
- "security review" → `security-reviewer`
- "performance testing" → `performance-tester`
- "API documentation" → `api-documenter`

### Step 3: List Capabilities

Identify 3-5 specific capabilities:
- Concrete actions the agent performs
- Specialized knowledge it applies
- Outputs it generates

### Step 4: Structure the Agent

Use this template:

\`\`\`markdown
---
description: One-line agent description
capabilities: ["capability-1", "capability-2", "capability-3"]
---

# Agent Name

Detailed description of agent's role and expertise.

## Capabilities

- **Capability 1**: What this enables
- **Capability 2**: What this enables
- **Capability 3**: What this enables

## When to Use This Agent

Claude should invoke when:
- Specific condition 1
- Specific condition 2
- Specific condition 3

## Context and Examples

**Example 1: Scenario Name**

User requests: "Help with X"
Agent provides: Specific assistance using capabilities

**Example 2: Another Scenario**

When Y happens, agent does Z.
\`\`\`

### Step 5: Verify Against Official Docs

Check `ai_docs/plugins-referance.md` for current agent specification.

## Key Principles

- **Specialization**: Agents should have focused expertise
- **Clear Invocation**: Claude must know when to use this agent
- **Concrete Capabilities**: List specific things agent can do
- **Examples**: Show real scenarios where agent helps

## Examples

**Example 1: Security Reviewer Agent**

User: "Create an agent for security reviews"

Process:
1. Purpose: Reviews code for security vulnerabilities
2. Name: `security-reviewer`
3. Capabilities: ["vulnerability detection", "security best practices", "threat modeling"]
4. Structure: Include when to invoke, examples of security issues
5. Create: `agents/security-reviewer.md`

Output: Agent that Claude invokes for security-related code review

**Example 2: Performance Tester Agent**

User: "I need an agent for performance testing"

Process:
1. Purpose: Designs and analyzes performance tests
2. Name: `performance-tester`
3. Capabilities: ["load testing", "benchmark design", "performance analysis"]
4. Structure: When to use for optimization vs testing
5. Create: `agents/performance-tester.md`

Output: Agent that Claude invokes for performance concerns
```

**Step 2: Verify structure**

Run: `head -n 10 plugins/meta/meta-claude/skills/agent-creator/SKILL.md`

Expected: Shows frontmatter and overview

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/skills/agent-creator/
git commit -m "feat: add agent-creator skill

Generates subagent definitions with capabilities
Includes template and real-world examples
References official agent specifications

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 14: Create Hook-Creator Skill

**Files:**

- Create: `plugins/meta/meta-claude/skills/hook-creator/SKILL.md`

**Step 1: Write hook-creator skill**

Complete file content for `plugins/meta/meta-claude/skills/hook-creator/SKILL.md`:

```markdown
---
name: hook-creator
description: Creates hook configurations following Claude Code event handling patterns and best practices
---

# Hook Creator

## Overview

Creates hook configurations that respond to Claude Code events automatically. Hooks enable automation like formatting on save, running tests after edits, or custom session initialization.

**When to use:** User wants to automate workflows, needs event-driven behavior, or requests hooks for their plugin.

**References:** Consult `ai_docs/plugins-referance.md` for hook specifications and available events.

## Hook Structure Requirements

Hooks are defined in `hooks/hooks.json` with:

1. **Event type** (SessionStart, PostToolUse, etc.)
2. **Matcher** (optional, for filtering which tool uses trigger hook)
3. **Hook actions** (command, validation, notification)
4. **Proper use of** `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths

## Available Events

From official documentation:

- `PreToolUse` - Before Claude uses any tool
- `PostToolUse` - After Claude uses any tool
- `UserPromptSubmit` - When user submits a prompt
- `Notification` - When Claude Code sends notifications
- `Stop` - When Claude attempts to stop
- `SubagentStop` - When subagent attempts to stop
- `SessionStart` - At session beginning
- `SessionEnd` - At session end
- `PreCompact` - Before conversation history compaction

## Creation Process

### Step 1: Identify Event and Purpose

Ask the user:
- What should happen automatically?
- When should it happen (which event)?
- What tool uses should trigger it (if PostToolUse)?

### Step 2: Choose Hook Type

Three hook types:

- **command**: Execute shell commands/scripts
- **validation**: Validate file contents or project state
- **notification**: Send alerts or status updates

### Step 3: Write Hook Configuration

Structure for `hooks/hooks.json`:

\`\`\`json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName1|ToolName2",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/script.sh"
          }
        ]
      }
    ]
  }
}
\`\`\`

### Step 4: Create Associated Scripts

If using command hooks:
1. Create script in plugin's `scripts/` directory
2. Make executable: `chmod +x scripts/script.sh`
3. Use `${CLAUDE_PLUGIN_ROOT}` for paths

### Step 5: Verify Against Official Docs

Check `ai_docs/plugins-referance.md` for:
- Current event names
- Hook configuration schema
- Environment variable usage

## Key Principles

- **Event Selection**: Choose most specific event for the need
- **Matcher Precision**: Use matchers to avoid unnecessary executions
- **Script Paths**: Always use `${CLAUDE_PLUGIN_ROOT}` for portability
- **Error Handling**: Scripts should handle errors gracefully

## Examples

**Example 1: Code Formatting Hook**

User: "Auto-format code after I edit files"

Hook configuration:

\`\`\`json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
\`\`\`

Creates `scripts/format-code.sh` that runs formatter on modified files.

**Example 2: Session Welcome Message**

User: "Show a message when Claude starts"

Hook configuration:

\`\`\`json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Welcome! Plugin loaded successfully.'"
          }
        ]
      }
    ]
  }
}
\`\`\`

Simple command hook, no external script needed.

**Example 3: Test Runner Hook**

User: "Run tests after I modify test files"

Hook configuration:

\`\`\`json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh"
          }
        ]
      }
    ]
  }
}
\`\`\`

Creates `scripts/run-tests.sh` that detects test file changes and runs relevant tests.
```

**Step 2: Validate structure**

Run: `cat plugins/meta/meta-claude/skills/hook-creator/SKILL.md | head -n 20`

Expected: Shows frontmatter and overview

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/skills/hook-creator/
git commit -m "feat: add hook-creator skill

Documents all available events and hook types
Provides complete JSON examples
Uses CLAUDE_PLUGIN_ROOT correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 15: Create Command-Creator Skill

**Files:**

- Create: `plugins/meta/meta-claude/skills/command-creator/SKILL.md`

**Step 1: Write command-creator skill**

Complete file content for `plugins/meta/meta-claude/skills/command-creator/SKILL.md`:

```markdown
---
name: command-creator
description: Scaffolds slash commands with proper frontmatter, structure, and usage examples
---

# Command Creator

## Overview

Creates slash commands for Claude Code plugins. Commands are user-invoked prompts that expand into detailed instructions for Claude.

**When to use:** User wants to create a command, add command to plugin, or needs command structure help.

**References:** See `ai_docs/plugins-referance.md` for command specifications.

## Command Structure Requirements

Every command MUST:

1. Be a `.md` file in `commands/` directory
2. Include frontmatter with `description`
3. Contain clear instructions for Claude
4. Use descriptive kebab-case filename
5. Instructions written from Claude's perspective

## Creation Process

### Step 1: Define Command Purpose

Ask the user:
- What should this command do?
- What inputs/context does it need?
- What should Claude produce?

### Step 2: Choose Command Name

Create concise kebab-case name:
- "generate tests" → `generate-tests.md`
- "review pr" → `review-pr.md`
- "deploy app" → `deploy-app.md`

Name becomes the command: `/generate-tests`

### Step 3: Write Frontmatter

Required frontmatter:

\`\`\`markdown
---
description: Brief description of what command does
---
\`\`\`

### Step 4: Write Instructions

Write clear instructions for Claude:

\`\`\`markdown
# Command Title

Detailed instructions telling Claude exactly what to do when this command is invoked.

## Steps

1. First action Claude should take
2. Second action
3. Final action

## Output Format

Describe how Claude should present results.

## Examples

Show example scenarios if helpful.
\`\`\`

### Step 5: Verify Against Official Docs

Check `ai_docs/plugins-referance.md` for command specifications.

## Key Principles

- **Clarity**: Instructions must be unambiguous
- **Completeness**: Include all steps Claude needs
- **Perspective**: Write as if instructing Claude directly
- **Frontmatter**: Always include description

## Examples

**Example 1: Test Generator Command**

User: "Create command to generate tests for a file"

Command file `commands/generate-tests.md`:

\`\`\`markdown
---
description: Generate comprehensive tests for a source file
---

# Generate Tests

Generate test cases for the file provided by the user.

## Process

1. Read and analyze the source file
2. Identify testable functions and methods
3. Determine test scenarios (happy path, edge cases, errors)
4. Write tests using the project's testing framework
5. Ensure tests are comprehensive and follow best practices

## Test Structure

- One test file per source file
- Clear test names describing what's tested
- Arrange-Act-Assert pattern
- Cover edge cases and error conditions

## Output

Present the generated tests and explain coverage.
\`\`\`

Invoked with: `/generate-tests`

**Example 2: PR Review Command**

User: "Create command for reviewing pull requests"

Command file `commands/review-pr.md`:

\`\`\`markdown
---
description: Conduct thorough code review of a pull request
---

# Review PR

Review the specified pull request for code quality, correctness, and best practices.

## Review Process

1. Fetch PR changes using git or gh CLI
2. Analyze changed files for:
   - Code correctness and logic errors
   - Style and formatting issues
   - Test coverage
   - Documentation completeness
   - Security concerns
   - Performance implications
3. Provide structured feedback

## Feedback Format

**Summary**: Brief overview of PR

**Strengths**: What's done well

**Issues**: Categorized by severity
- Critical: Must fix
- Important: Should fix
- Minor: Nice to have

**Suggestions**: Specific improvements with examples

## Usage

\`/review-pr <pr-number>\` or provide PR URL
\`\`\`

Invoked with: `/review-pr 123`
```

**Step 2: Verify frontmatter**

Run: `head -n 5 plugins/meta/meta-claude/skills/command-creator/SKILL.md`

Expected: Shows valid frontmatter

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/skills/command-creator/
git commit -m "feat: add command-creator skill

Explains slash command structure and frontmatter
Provides complete command examples
Emphasizes clarity and completeness

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 16: Create New-Plugin Command

**Files:**

- Create: `plugins/meta/meta-claude/commands/new-plugin.md`

**Step 1: Write new-plugin command**

Complete file content for `plugins/meta/meta-claude/commands/new-plugin.md`:

```markdown
---
description: Interactive wizard for creating new plugins in lunar-claude marketplace
---

# New Plugin

Create a new plugin in the lunar-claude marketplace using the template structure.

## Process

Follow these steps to create a properly structured plugin:

### Step 1: Gather Plugin Information

Ask the user for:
- **Plugin name** (kebab-case, no spaces)
- **Description** (one-line summary)
- **Category** (meta, infrastructure, devops, or homelab)
- **Keywords** (comma-separated for searchability)
- **Components needed** (skills, agents, hooks, commands)

### Step 2: Validate Plugin Name

Check that:
- Name uses kebab-case format
- Name is unique (not in current marketplace.json)
- Name is descriptive and clear

### Step 3: Create Plugin Directory

1. Copy template to appropriate category:
   ```bash
   cp -r templates/plugin-template/ plugins/<category>/<plugin-name>/
   ```

2. Navigate to new plugin directory

### Step 4: Customize Plugin Files

1. Update `.claude-plugin/plugin.json`:
   - Replace `PLUGIN_NAME` with actual name
   - Replace `PLUGIN_DESCRIPTION` with description
   - Replace `KEYWORD1`, `KEYWORD2` with actual keywords

2. Update `README.md`:
   - Replace all `PLUGIN_NAME` placeholders
   - Replace `PLUGIN_DESCRIPTION`
   - Remove component sections not being used

3. Remove unused component directories:
   - If not using agents, remove `agents/`
   - If not using skills, remove `skills/`
   - If not using hooks, remove `hooks/`
   - Always keep `commands/` (can be empty with .gitkeep)

### Step 5: Update Marketplace Manifest

1. Read current `.claude-plugin/marketplace.json`

2. Add new plugin entry to `plugins` array:

   ```json
   {
     "name": "plugin-name",
     "source": "./plugins/<category>/<plugin-name>",
     "description": "plugin description",
     "version": "0.1.0",
     "category": "category-name",
     "keywords": ["keyword1", "keyword2"],
     "author": {
       "name": "basher83"
     }
   }
   ```

3. Write updated marketplace.json

4. Validate JSON syntax with `jq`

### Step 6: Create Initial Commit

```bash
git add plugins/<category>/<plugin-name>/
git add .claude-plugin/marketplace.json
git commit -m "feat: add <plugin-name> plugin

Create new <category> plugin: <description>
Initial version 0.1.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 7: Provide Next Steps

Tell the user:

**Plugin created successfully!**

Location: `plugins/<category>/<plugin-name>/`

Next steps:
1. Add your components (skills, agents, hooks, commands)
2. Update README.md with usage examples
3. Test locally: `/plugin marketplace add .`
4. Install: `/plugin install <plugin-name>@lunar-claude`

## Examples

**Example: Creating infrastructure plugin**

User input:
- Name: terraform-tools
- Description: Terraform and OpenTofu helpers
- Category: infrastructure
- Keywords: terraform, opentofu, iac
- Components: skills, commands

Result:
- Created `plugins/infrastructure/terraform-tools/`
- Added to marketplace.json under infrastructure category
- Ready for component development

**Example: Creating homelab plugin**

User input:
- Name: proxmox-ops
- Description: Proxmox cluster operations
- Category: homelab
- Keywords: proxmox, virtualization, homelab
- Components: agents, commands

Result:
- Created `plugins/homelab/proxmox-ops/`
- Added to marketplace.json under homelab category
- Removed unused skills and hooks directories

```text

**Step 2: Verify command structure**

Run: `head -n 10 plugins/meta/meta-claude/commands/new-plugin.md`

Expected: Shows frontmatter and title

**Step 3: Commit**

```bash
git add plugins/meta/meta-claude/commands/new-plugin.md
git commit -m "feat: add new-plugin command

Interactive wizard for plugin creation
Uses template structure and updates marketplace.json
Provides step-by-step guidance

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 17: Add Meta-Claude to Marketplace

**Files:**

- Modify: `.claude-plugin/marketplace.json`

**Step 1: Read current marketplace.json**

Run: `cat .claude-plugin/marketplace.json`

**Step 2: Add meta-claude entry**

Update `.claude-plugin/marketplace.json` to add meta-claude to plugins array:

```json
{
  "name": "lunar-claude",
  "owner": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "metadata": {
    "description": "Personal Claude Code plugin marketplace for homelab and infrastructure automation",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "meta-claude",
      "source": "./plugins/meta/meta-claude",
      "description": "Meta tools for creating skills, agents, hooks, and commands",
      "version": "0.1.0",
      "category": "meta",
      "keywords": ["meta", "tooling", "development", "creator"],
      "author": {
        "name": "basher83"
      }
    }
  ]
}
```

**Step 3: Validate JSON**

Run: `cat .claude-plugin/marketplace.json | jq .`

Expected: JSON parses successfully

**Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: add meta-claude to marketplace

Register meta-claude plugin in marketplace manifest
First plugin in the lunar-claude collection

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 18: Test Local Installation

**Files:**

- No file changes

**Step 1: Add marketplace locally**

Run: `/plugin marketplace add /Users/basher8383/dev/personal/lunar-claude`

Expected: Marketplace added successfully

**Step 2: Verify marketplace is recognized**

Run: `/plugin marketplace list`

Expected: Shows `lunar-claude` in the list

**Step 3: Browse available plugins**

Run: `/plugin`

Expected: Shows meta-claude plugin available for installation

**Step 4: Install meta-claude**

Run: `/plugin install meta-claude@lunar-claude`

Expected: Installation succeeds, plugin components available

**Step 5: Verify installation**

Check:

- `/help` shows `/new-plugin` command
- Skills are loaded (check via skill list if available)

**Step 6: Document test results**

Create verification notes (not committed):

```bash
echo "Marketplace test completed successfully" > /tmp/test-results.txt
echo "Date: $(date)" >> /tmp/test-results.txt
echo "Meta-claude plugin installed and verified" >> /tmp/test-results.txt
```

---

## Task 19: Create Verification Script

**Files:**

- Create: `scripts/verify-structure.sh`

**Step 1: Create scripts directory**

```bash
mkdir -p scripts
```

**Step 2: Write verification script**

Complete file content for `scripts/verify-structure.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Verify lunar-claude marketplace structure

echo "Verifying lunar-claude marketplace structure..."

# Check core directories
echo "✓ Checking core directories..."
[[ -d "plugins/meta" ]] || { echo "✗ Missing plugins/meta"; exit 1; }
[[ -d "plugins/infrastructure" ]] || { echo "✗ Missing plugins/infrastructure"; exit 1; }
[[ -d "plugins/devops" ]] || { echo "✗ Missing plugins/devops"; exit 1; }
[[ -d "plugins/homelab" ]] || { echo "✗ Missing plugins/homelab"; exit 1; }
[[ -d "templates/plugin-template" ]] || { echo "✗ Missing templates/plugin-template"; exit 1; }

# Check marketplace.json
echo "✓ Checking marketplace.json..."
[[ -f ".claude-plugin/marketplace.json" ]] || { echo "✗ Missing marketplace.json"; exit 1; }
jq empty .claude-plugin/marketplace.json || { echo "✗ Invalid JSON in marketplace.json"; exit 1; }

# Check template structure
echo "✓ Checking template structure..."
[[ -f "templates/plugin-template/.claude-plugin/plugin.json" ]] || { echo "✗ Missing template plugin.json"; exit 1; }
[[ -f "templates/plugin-template/README.md" ]] || { echo "✗ Missing template README"; exit 1; }
[[ -f "templates/plugin-template/agents/example-agent.md" ]] || { echo "✗ Missing example agent"; exit 1; }
[[ -f "templates/plugin-template/skills/example-skill/SKILL.md" ]] || { echo "✗ Missing example skill"; exit 1; }

# Check meta-claude plugin
echo "✓ Checking meta-claude plugin..."
[[ -d "plugins/meta/meta-claude" ]] || { echo "✗ Missing meta-claude plugin"; exit 1; }
[[ -f "plugins/meta/meta-claude/.claude-plugin/plugin.json" ]] || { echo "✗ Missing meta-claude manifest"; exit 1; }

# Check meta-claude skills
echo "✓ Checking meta-claude skills..."
[[ -f "plugins/meta/meta-claude/skills/skill-creator/SKILL.md" ]] || { echo "✗ Missing skill-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/agent-creator/SKILL.md" ]] || { echo "✗ Missing agent-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/hook-creator/SKILL.md" ]] || { echo "✗ Missing hook-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/command-creator/SKILL.md" ]] || { echo "✗ Missing command-creator"; exit 1; }

# Check meta-claude command
echo "✓ Checking meta-claude command..."
[[ -f "plugins/meta/meta-claude/commands/new-plugin.md" ]] || { echo "✗ Missing new-plugin command"; exit 1; }

# Verify marketplace contains meta-claude
echo "✓ Checking marketplace registration..."
jq -e '.plugins[] | select(.name == "meta-claude")' .claude-plugin/marketplace.json > /dev/null || { echo "✗ meta-claude not in marketplace"; exit 1; }

echo ""
echo "✅ All verification checks passed!"
echo "Marketplace structure is valid and complete."
```

**Step 3: Make script executable**

```bash
chmod +x scripts/verify-structure.sh
```

**Step 4: Run verification**

Run: `./scripts/verify-structure.sh`

Expected: All checks pass

**Step 5: Commit**

```bash
git add scripts/verify-structure.sh
git commit -m "feat: add structure verification script

Validates directory structure and file presence
Checks JSON validity and marketplace registration
Useful for CI or manual verification

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 20: Final Verification and Documentation

**Files:**

- Modify: `README.md`

**Step 1: Run final verification**

Run: `./scripts/verify-structure.sh`

Expected: All checks pass

**Step 2: Update main README**

Update `/Users/basher8383/dev/personal/lunar-claude/README.md` to replace old content with:

```markdown
# lunar-claude

Personal Claude Code plugin marketplace for homelab and infrastructure automation.

## Structure

This marketplace organizes plugins into four categories:

- **meta** - Tools for creating Claude Code components
- **infrastructure** - Infrastructure as Code tools (Terraform, Ansible, Proxmox)
- **devops** - Container orchestration and DevOps tools (Kubernetes, Docker)
- **homelab** - Homelab-specific utilities (Netbox, PowerDNS)

## Installation

Add this marketplace:

\`\`\`bash
/plugin marketplace add basher83/lunar-claude
\`\`\`

## Available Plugins

### meta-claude

Meta tools for creating skills, agents, hooks, and commands.

**Install:**
\`\`\`bash
/plugin install meta-claude@lunar-claude
\`\`\`

**Features:**
- Four creator skills (skill-creator, agent-creator, hook-creator, command-creator)
- Interactive `/new-plugin` command
- References official Claude Code documentation

See [plugins/meta/meta-claude/README.md](plugins/meta/meta-claude/README.md) for details.

## Development

### Creating New Plugins

Use the meta-claude plugin:

\`\`\`bash
/new-plugin
\`\`\`

Or manually:

1. Copy template: \`cp -r templates/plugin-template/ plugins/<category>/<name>/\`
2. Customize plugin.json and README.md
3. Add to .claude-plugin/marketplace.json
4. Commit changes

### Template Structure

The plugin template includes:
- Complete plugin.json with placeholders
- README.md with standard sections
- Example agent, skill, and hooks
- All required directories

### Verification

Run structure verification:

\`\`\`bash
./scripts/verify-structure.sh
\`\`\`

### Local Testing

\`\`\`bash
# Add marketplace
/plugin marketplace add /path/to/lunar-claude

# Install plugin
/plugin install plugin-name@lunar-claude
\`\`\`

## Design Documentation

See [docs/plans/](docs/plans/) for detailed design and implementation documentation.

## Version History

- 0.1.0 - Initial marketplace with meta-claude plugin
```

**Step 3: Commit README update**

```

```bash
git add README.md
git commit -m "docs: update README with marketplace documentation

Document structure, installation, and usage
Explain development workflow and available plugins
Add verification and testing instructions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Step 4: Verify git history**

Run: `git log --oneline | head -n 25`

Expected: Shows all commits from implementation

**Step 5: Final verification**

Run all checks:

```bash
./scripts/verify-structure.sh
jq empty .claude-plugin/marketplace.json
tree -L 3 plugins/
```

Expected: All commands succeed, structure is valid

---

## Implementation Complete

You have successfully implemented:

✅ Four-category directory structure (meta, infrastructure, devops, homelab)
✅ Clean marketplace.json manifest
✅ Complete plugin template with examples
✅ Meta-claude plugin with four creator skills
✅ Interactive new-plugin command
✅ Verification script
✅ Updated documentation

The marketplace is ready for:

- Local testing and installation
- Adding new plugins via template
- Using meta-claude tools for development

Next steps:

- Test meta-claude skills by creating components
- Add infrastructure/devops/homelab plugins as needed
- Share marketplace or keep private for personal use
