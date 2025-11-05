# Meta-Claude

Meta tools for creating Claude Code components including skills, agents, hooks, and commands.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install meta-claude:

```bash
/plugin install meta-claude@lunar-claude
```

## Components

### Skills

Meta-claude provides five skills that Claude invokes automatically:

**Creator Skills:**
- **skill-creator** - Creates new Agent Skills with proper structure and official documentation references
- **agent-creator** - Generates properly formatted subagent definitions
- **hook-creator** - Creates hook configurations following Claude Code patterns
- **command-creator** - Scaffolds slash commands with frontmatter and examples

**Architectural Guidance:**
- **multi-agent-composition** - Comprehensive knowledge base for composing multi-component agentic systems. Provides decision frameworks for choosing between skills/sub-agents/hooks/MCP/slash-commands, context management patterns, orchestrator workflows, and anti-patterns to avoid

### Commands

- `/new-plugin` - Interactive plugin creation wizard that uses the template structure

## Usage

### Autonomous Mode (Skills)

Simply ask Claude to create components or make architectural decisions:

**Creating components:**
```text
"Help me create a skill for processing terraform configurations"
"I need an agent for kubernetes operations"
"Create a hook that runs tests after file edits"
```

**Architectural guidance:**
```text
"Should I use a skill or sub-agent for this task?"
"How do I implement multi-agent orchestration?"
"What's the best way to add observability with hooks?"
"What are common mistakes when composing Claude Code components?"
```

Claude will automatically use the appropriate skill based on your request.

### Interactive Mode (Command)

For structured plugin creation:

```bash
/new-plugin
```

Walks through:

1. Plugin name and description
2. Category selection (meta, infrastructure, devops, homelab)
3. Component selection (skills, agents, hooks, commands)
4. Template application
5. Marketplace.json update

## How It Works

Creator skills reference official Claude Code documentation in `ai_docs/` to ensure
generated components follow current specifications. This extends Anthropic's base
skill-creator with plugin-specific knowledge.

## Version History

- 0.2.0 - Added multi-agent-composition skill for architectural guidance and multi-component system design
- 0.1.0 - Initial release with four creator skills and new-plugin command
