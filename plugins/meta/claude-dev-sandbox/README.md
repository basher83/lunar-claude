# claude-dev-sandbox

**DEVELOPMENT ONLY** - This plugin is a sandbox environment for testing and prototyping Claude Code components.

## Purpose

This plugin provides an isolated workspace for:

- **Rapid prototyping** of hooks, skills, commands, and agents
- **Iterative testing** without affecting production plugins
- **Experimentation** with new ideas and patterns

Components developed here should be **promoted to appropriate production plugins** once stable and tested.

## Why Use This Sandbox?

1. **Isolation:** Test without breaking existing functionality
2. **Fast iteration:** No branch management needed for quick experiments
3. **Real context:** Test components in actual Claude Code environment
4. **Easy cleanup:** Delete failed experiments without cluttering production plugins

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install this plugin:

```bash
/plugin install claude-dev-sandbox@lunar-claude
```

## Workflow

### 1. Develop Component

Create your hook/skill/command/agent in the appropriate directory:

```bash
# Example: Testing a new hook
vim plugins/meta/claude-dev-sandbox/hooks/my-experimental-hook.json
```

### 2. Install & Test

```bash
/plugin uninstall claude-dev-sandbox@lunar-claude
/plugin install claude-dev-sandbox@lunar-claude

# Test your component
# (trigger hook, use skill, run command, etc.)
```

### 3. Iterate

Make changes and reinstall to test again.

### 4. Promote to Production

When stable, move component to appropriate plugin:

```bash
git checkout -b feature/new-component

# Move component
mv plugins/meta/claude-dev-sandbox/hooks/my-hook.json \
   plugins/target-plugin/hooks/

# Update target plugin if needed
# Commit and merge
```

## Active Components

Document what you're currently testing here:

### Commands

- (none yet - add as you develop)

### Agents

- (none yet - add as you develop)

### Skills

- **mcp-builder** - Experimental skill for MCP server development
- **video-processor** - Experimental video processing skill

### Hooks

- (none yet - add as you develop)

## Notes

- This plugin should **never be considered stable**
- Components here are **work-in-progress**
- Use git branches when promoting to production plugins
- Consider adding `.gitignore` rules if you want truly throwaway experiments

## Version History

- 0.1.0 - Initial sandbox setup
