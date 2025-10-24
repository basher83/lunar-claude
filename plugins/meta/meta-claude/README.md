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

```
"Help me create a skill for processing terraform configurations"
"I need an agent for kubernetes operations"
"Create a hook that runs tests after file edits"
```

Claude will automatically use the appropriate creator skill.

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

Creator skills reference official Claude Code documentation in `ai_docs/` to ensure generated components follow current specifications. This extends Anthropic's base skill-creator with plugin-specific knowledge.

## Version History

- 0.1.0 - Initial release with four creator skills and new-plugin command
