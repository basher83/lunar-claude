---
name: slash-command-creator
description: >
  Create custom slash commands for Claude Code with complete frontmatter, arguments, and
  advanced features. Use when creating /commands, writing command .md files, configuring
  allowed-tools, adding argument placeholders ($ARGUMENTS, $1, $2), embedding bash execution
  with !`command`, using file references with @path, setting up plugin commands with namespacing,
  or deciding between slash commands vs skills.
---

# Slash Command Creator

Create custom slash commands for Claude Code - from simple prompts to advanced commands with
bash execution, file references, and tool restrictions.

## Quick Start

Create a simple command:

```bash
mkdir -p .claude/commands
cat > .claude/commands/review.md << 'EOF'
---
description: Review code for bugs and improvements
---

Review the provided code for:

- Logic errors and bugs
- Performance issues
- Security vulnerabilities
- Code style violations

Provide actionable feedback with specific line references.
EOF
```

Invoke with: `/review`

## Command Locations

| Location | Scope | Description Label |
|----------|-------|-------------------|
| `.claude/commands/` | Project | `(project)` |
| `~/.claude/commands/` | Personal | `(user)` |
| `plugins/<name>/commands/` | Plugin | `(plugin:<name>)` |

## Frontmatter Reference

All frontmatter fields:

```yaml
---
description: Brief description shown in /help
argument-hint: [file] [options]
allowed-tools: Bash(git:*), Read, Write
model: claude-sonnet-4-20250514
disable-model-invocation: false
---
```

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Shown in `/help` and SlashCommand tool context | First line of content |
| `argument-hint` | Autocomplete hint for arguments | None |
| `allowed-tools` | Restrict available tools | Inherits from conversation |
| `model` | Override model for this command | Inherits from conversation |
| `disable-model-invocation` | Prevent SlashCommand tool from calling | `false` |

## Arguments

### Capture All: `$ARGUMENTS`

```markdown
---
description: Fix GitHub issue
---

Fix issue #$ARGUMENTS following project coding standards.
```

Usage: `/fix-issue 123 high-priority` → `$ARGUMENTS` = `"123 high-priority"`

### Positional: `$1`, `$2`, `$3`

```markdown
---
description: Review PR with priority
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

Usage: `/review-pr 456 high alice` → `$1`=`456`, `$2`=`high`, `$3`=`alice`

## Bash Execution

Execute commands before prompt expansion using `!`backtick` syntax.
**Requires** `allowed-tools: Bash(...)` in frontmatter.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current status: !`git status`
- Staged diff: !`git diff --cached`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Task

Based on the staged changes above, create a commit with a descriptive message.
```

## File References

Include file contents using `@path` syntax:

```markdown
Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

## Namespacing

Subdirectories organize commands and appear in descriptions:

| File Location | Command | Description |
|---------------|---------|-------------|
| `.claude/commands/deploy.md` | `/deploy` | `(project)` |
| `.claude/commands/frontend/build.md` | `/build` | `(project:frontend)` |
| `~/.claude/commands/utils/format.md` | `/format` | `(user:utils)` |

**Note:** Subdirectories don't affect command names, only descriptions.

## Plugin Commands

Plugin commands live in `commands/` directory of plugin root:

```text
plugins/my-plugin/
├── commands/
│   ├── deploy.md
│   └── test/
│       └── run.md
└── plugin.json
```

Invocation patterns:

```bash
/deploy                    # Direct (if no conflicts)
/my-plugin:deploy          # Namespaced (for disambiguation)
/my-plugin:run             # Subdirectory command
```

## SlashCommand Tool

Claude can invoke custom commands programmatically. Commands must have `description` field to be available.

### Permission Rules

```text
SlashCommand:/commit        # Exact match (no arguments)
SlashCommand:/review-pr:*   # Prefix match (any arguments)
```

### Disable for Specific Command

```yaml
---
description: Sensitive command
disable-model-invocation: true
---
```

### Character Budget

Default: 15,000 characters for all command metadata.
Override: `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

## Thinking Mode

Commands can trigger extended thinking by including keywords like "think deeply",
"step by step", or "analyze thoroughly" in the command content.

## Slash Commands vs Skills

| Aspect | Slash Commands | Skills |
|--------|----------------|--------|
| **Complexity** | Simple prompts | Complex capabilities |
| **Structure** | Single `.md` file | Directory with `SKILL.md` + resources |
| **Discovery** | Explicit (`/command`) | Automatic (context-based) |
| **Files** | One file only | Multiple files, scripts, templates |

**Use slash commands when:**

- Prompt fits in a single file
- You invoke it repeatedly with explicit control
- Simple, focused task

**Use skills when:**

- Multiple reference files or scripts needed
- Claude should auto-discover capability
- Complex workflows with validation steps

## Common Patterns

### Git Commit Command

```markdown
---
allowed-tools: Bash(git:*)
description: Create atomic git commit
argument-hint: [message]
---

## Context

!`git status`
!`git diff --cached`

## Task

Create a git commit. If $ARGUMENTS provided, use as message.
Otherwise, generate descriptive message from diff.
```

### Code Generator Command

```markdown
---
description: Generate boilerplate code
argument-hint: [type] [name]
---

Generate $1 boilerplate named $2.

Supported types: component, hook, service, util

Follow project conventions in @src/templates/
```

### Review with Tool Restrictions

```markdown
---
allowed-tools: Read, Grep, Glob
description: Read-only code review
---

Review the codebase for the issue described.
DO NOT modify any files - this is a read-only review.

Provide analysis and recommendations only.
```

## Validation Checklist

Before finalizing a command:

- [ ] `description` frontmatter is present and descriptive
- [ ] `argument-hint` matches actual argument usage
- [ ] `allowed-tools` restricts to necessary tools only
- [ ] Bash execution has matching tool permissions
- [ ] File references use valid relative paths
- [ ] Command name is kebab-case and descriptive

## References

- **Official Docs:** See [references/slash-commands.md](references/slash-commands.md)
- **Anthropic Source:** See [references/anthropic-slash-commands.md](references/anthropic-slash-commands.md)
- **Plugins Guide:** See [references/plugins.md](references/plugins.md)
- **Skills Comparison:** See [references/skills.md](references/skills.md)
