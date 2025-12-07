# Plugin Spec

A plugin is a directory containing a `plugin.json` manifest and optional components (commands, agents, skills, hooks, MCP servers). Plugins bundle related functionality for distribution and installation.

## Plugin Directory Layout

A minimal plugin looks like this:

```text
my-plugin/
  - plugin.json
```

A complete plugin can include any combination of components:

```text
my-plugin/
  - plugin.json         # Required manifest
  - commands/           # Slash commands
      - deploy.md
      - test.md
  - agents/             # Subagents
      - reviewer.md
  - skills/             # Skills
      - debugging/
          - SKILL.md
  - hooks/              # Automation hooks
      - hooks.json
  - .mcp.json           # MCP server configuration
  - README.md           # Documentation
```

## The plugin.json File

The plugin manifest is a JSON file that defines the plugin's metadata and component locations.

## Required Properties

- `name`
  - Unique identifier for the plugin
  - Restricted to lowercase letters, numbers, and hyphens (kebab-case)
  - Example: `"name": "code-review-toolkit"`

## Optional Properties

### Metadata

- `version`
  - Semantic version string
  - Example: `"version": "1.2.0"`
- `description`
  - Brief description of the plugin's purpose
  - Example: `"description": "Tools for automated code review"`
- `author`
  - Author information object
  - Example: `"author": {"name": "Jane Doe", "email": "jane@example.com"}`
- `homepage`
  - URL to the plugin's homepage or documentation
- `repository`
  - URL to the source code repository
- `license`
  - SPDX license identifier
  - Example: `"license": "MIT"`
- `keywords`
  - Array of keywords for discovery
  - Example: `"keywords": ["code-review", "linting", "quality"]`

### Component Paths

- `commands`
  - Path to commands directory or array of specific command files
  - Default: `./commands/` (auto-discovered)
  - Example: `"commands": "./custom/commands/"` or `"commands": ["./cmd/deploy.md"]`
- `agents`
  - Path to agents directory or array of specific agent files
  - Default: `./agents/` (auto-discovered)
  - Example: `"agents": "./custom/agents/"`
- `skills`
  - Path to skills directory or array of specific skill directories
  - Default: `./skills/` (auto-discovered)
  - Example: `"skills": "./custom/skills/"`
- `hooks`
  - Path to hooks configuration file
  - Example: `"hooks": "./config/hooks.json"`
- `mcpServers`
  - Path to MCP server configuration file
  - Example: `"mcpServers": "./.mcp.json"`

## Example

```json
{
  "name": "code-review-toolkit",
  "version": "1.0.0",
  "description": "Comprehensive code review automation tools",
  "author": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "license": "MIT",
  "keywords": ["code-review", "linting", "automation"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks.json"
}
```

## Component Auto-Discovery

If component paths are not specified in `plugin.json`, Claude Code automatically discovers components in standard directories:

| Component | Default Path | File Pattern |
|-----------|--------------|--------------|
| Commands  | `./commands/` | `*.md` |
| Agents    | `./agents/` | `*.md` |
| Skills    | `./skills/` | `*/SKILL.md` |

## Plugin Variable

Use `${CLAUDE_PLUGIN_ROOT}` in component files to reference the plugin's root directory. This enables portable paths that work regardless of where the plugin is installed.

## Additional Information

- Plugins are installed via the `/install-plugin` command or by adding to settings
- All plugin components are namespaced with the plugin name (e.g., `/my-plugin:command`)
- Plugin hooks, agents, and skills integrate seamlessly with user-defined components

## Version History

- 1.0 (2025-10-16) Public Launch
