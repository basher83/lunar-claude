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

- **skill-factory** - Production-grade skill creation with validation
- **multi-agent-composition** - Guides multi-component system design with decision
  frameworks for choosing skills, sub-agents, hooks, MCP servers, and slash
  commands; includes context management patterns, orchestrator workflows, and
  anti-patterns

## Usage

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
