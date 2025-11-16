# Meta-Claude

Create Claude Code skills, agents, hooks, and commands with automated tooling and architectural guidance.

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

Five skills guide component creation and system architecture:

**Creator Skills:**

- **skill-creator** - Creates Agent Skills with proper structure and official documentation
- **agent-creator** - Generates formatted subagent definitions
- **hook-creator** - Creates hook configurations following Claude Code patterns
- **command-creator** - Scaffolds slash commands with frontmatter and examples

**Architectural Guidance:**

- **multi-agent-composition** - Guides multi-component system design with decision
  frameworks for choosing skills, sub-agents, hooks, MCP servers, and slash
  commands; includes context management patterns, orchestrator workflows, and
  anti-patterns

### Commands

- `/new-plugin` - Interactive wizard creates plugins using the template structure

## Usage

### Autonomous Mode (Skills)

Ask Claude to create components or provide architectural guidance:

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

Claude invokes the appropriate skill automatically.

### Interactive Mode (Command)

Create structured plugins with the wizard:

```bash
/new-plugin
```

The wizard walks you through:

1. Plugin name and description
2. Category selection (meta, infrastructure, devops, homelab)
3. Component selection (skills, agents, hooks, commands)
4. Template application
5. Marketplace.json update

## How It Works

Creator skills reference official Claude Code documentation to generate
components that follow current specifications. This extends Anthropic's base
skill-creator with plugin-specific knowledge.

## Version History

- 0.3.0 - Added comprehensive test suite, .gitignore; improved README clarity;
  fixed agent frontmatter compliance; clarified plugin vs user agent
  distinction in agent-creator skill
- 0.2.0 - Added multi-agent-composition skill for architectural guidance
- 0.1.0 - Initial release with four creator skills and new-plugin command
