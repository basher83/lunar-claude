# Command Spec

A command is a Markdown file that defines a custom slash command users can invoke. Commands expand into prompts that Claude executes, with optional tool restrictions and argument handling.

## Command File Location

Commands can be placed in any of these directories:

```text
.claude/commands/           # Project-level (shared via git)
~/.claude/commands/         # User-level (personal)
<plugin-root>/commands/     # Plugin-level (bundled with plugin)
```

A minimal command is a single Markdown file:

```text
my-command.md
```

The filename (without `.md`) becomes the command name. For example, `commit.md` creates the `/commit` command.

## The Command File

The command file is a Markdown document with optional YAML frontmatter followed by the command's prompt template.

## YAML Frontmatter

All frontmatter properties are optional:

- `allowed-tools`
  - List of tools the command can use
  - If omitted, inherits tools from the conversation
  - Example: `allowed-tools: Bash(git add:*), Bash(git status:*)`
- `argument-hint`
  - Expected arguments shown in autocomplete
  - Example: `argument-hint: [message]` or `argument-hint: <branch-name>`
- `description`
  - Brief description of what the command does
  - If omitted, uses the first line from the prompt
  - Shown in autocomplete and help
- `model`
  - Specific model to use for this command
  - Example: `model: claude-3-5-haiku-20241022`
- `disable-model-invocation`
  - When `true`, prevents the SlashCommand tool from calling this command programmatically
  - Default: `false`

## Markdown Body

The Markdown body is the prompt template that Claude executes. It supports several special features:

### Arguments

- `$ARGUMENTS` - All arguments passed to the command as a single string
- `$1`, `$2`, etc. - Positional arguments

### Bash Execution

Lines starting with `!` execute as bash commands before the prompt runs:

```markdown
!git status
```

### File References

Use `@` prefix to include file contents:

```markdown
Review the changes in @src/main.ts
```

## Example

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit with the specified message
---

Create a git commit with the following message:

$ARGUMENTS

Follow conventional commit format. Stage all modified files first.
```

## Namespacing

Commands can be organized into subdirectories for namespacing:

```text
.claude/commands/
  frontend/
    component.md    # Invoked as /frontend:component
    test.md         # Invoked as /frontend:test
  backend/
    api.md          # Invoked as /backend:api
```

## Additional Information

- Commands are user-invoked (typed by user) unlike skills which are model-invoked
- Commands can trigger extended thinking via specific keywords in the prompt
- The SlashCommand tool allows Claude to invoke commands programmatically during a conversation

## Version History

- 1.0 (2025-10-16) Public Launch
