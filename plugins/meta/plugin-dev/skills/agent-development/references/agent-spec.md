# Agent Spec

An agent is a Markdown file that defines a specialized subagent Claude can invoke to handle specific tasks. Agents have their own system prompt, tool access, and optional model configuration. They are discovered by Claude based on their description.

## Agent File Location

Agents can be placed in any of these directories:

```text
.claude/agents/           # Project-level (shared via git)
~/.claude/agents/         # User-level (personal)
<plugin-root>/agents/     # Plugin-level (bundled with plugin)
```

A minimal agent is a single Markdown file:

```text
my-agent.md
```

## The Agent File

The agent file is a Markdown document with YAML frontmatter followed by the agent's system prompt.

## YAML Frontmatter

The YAML frontmatter has 2 required properties:

- `name`
  - Unique identifier for the agent
  - Restricted to lowercase letters and hyphens
- `description`
  - Natural language description of what the agent does and when Claude should invoke it
  - Critical for discovery - Claude uses this to decide when to spawn the agent

There are 6 optional properties:

- `tools`
  - Comma-separated list of specific tools the agent can use
  - If omitted, the agent inherits all tools from the main conversation
  - Example: `tools: Read, Grep, Glob, Bash`
- `model`
  - Model alias to use: `sonnet`, `opus`, `haiku`, or `inherit`
  - If omitted, defaults to the configured subagent model
- `permissionMode`
  - Controls how permissions are handled
  - Values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`
- `skills`
  - Comma-separated list of skill names to auto-load when the agent starts
  - Example: `skills: debugging, code-review`
- `color`
  - Display color for the agent in the CLI status line
  - Values: `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`
  - Note: Undocumented feature, not in official docs
- `capabilities`
  - Array of specific tasks or capabilities the agent excels at
  - Used for plugin agents to describe specializations
  - Example: `capabilities: ["code review", "security analysis", "refactoring"]`

## Markdown Body

The Markdown body becomes the agent's system prompt. It should describe:

- The agent's role and expertise
- How to approach tasks
- Expected output format
- Any constraints or guidelines

## Example

```markdown
---
name: code-reviewer
description: Use this agent to review code changes for style, bugs, and best practices
tools: Read, Grep, Glob
model: sonnet
color: cyan
capabilities: ["style review", "bug detection", "security analysis"]
---

# Code Reviewer

You are an expert code reviewer. Analyze code for:

1. Style and formatting issues
2. Potential bugs or edge cases
3. Performance concerns
4. Security vulnerabilities

Provide actionable feedback with specific line references.
```

## Additional Information

- Agents run in isolation and cannot communicate back to the main conversation except through their final report
- Each agent invocation is stateless - they don't retain memory between calls
- Agents can be invoked via the Task tool with `subagent_type` matching the agent name

## Version History

- 1.0 (2025-10-16) Public Launch
