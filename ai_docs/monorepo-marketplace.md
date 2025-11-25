# Monorepo Marketplace Structure

A Claude Code marketplace configured as a monorepo contains multiple plugins in a single repository.

## Required Files

### Marketplace Registry

Create `.claude-plugin/marketplace.json` at the repository root:

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Team Name",
    "email": "contact@example.com"
  },
  "plugins": []
}
```

**Required fields:**

- `name` - Marketplace identifier (kebab-case)
- `owner` - Maintainer information
- `plugins` - Array of plugin entries

**Optional fields:**

- `metadata.description` - Marketplace description
- `metadata.version` - Version number
- `metadata.pluginRoot` - Base path for relative sources

### Plugin Manifest

Each plugin requires `.claude-plugin/plugin.json` unless `strict: false`:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name"
  }
}
```

## Directory Structure

```text
repository-root/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── category-one/
│   │   └── first-plugin/
│   │       ├── .claude-plugin/
│   │       │   └── plugin.json
│   │       ├── skills/
│   │       ├── commands/
│   │       ├── agents/
│   │       ├── hooks/
│   │       └── README.md
│   └── category-two/
│       └── second-plugin/
│           └── ...
└── README.md
```

## Plugin Entries

Add plugins to the `plugins` array in `marketplace.json`.

### Minimal Entry

```json
{
  "name": "plugin-name",
  "source": "./plugins/category/plugin-name"
}
```

**Required:**

- `name` - Plugin identifier (kebab-case)
- `source` - Location of plugin files

### Complete Entry

```json
{
  "name": "plugin-name",
  "source": "./plugins/category/plugin-name",
  "description": "What the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/org/repo",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "category": "productivity"
}
```

**Optional fields:**

- `description` - Brief description
- `version` - Version number
- `author` - Author information
- `homepage` - Documentation URL
- `repository` - Source code URL
- `license` - SPDX identifier
- `keywords` - Discovery tags
- `category` - Organization category
- `tags` - Additional tags
- `strict` - Require plugin.json (default: true)

## Plugin Sources

### Relative Paths

Use relative paths for plugins in the same repository:

```json
{
  "name": "my-plugin",
  "source": "./plugins/category/my-plugin"
}
```

Paths resolve relative to `marketplace.json` location.

### GitHub Repositories

Reference external GitHub repositories:

```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repository"
  }
}
```

### Git URLs

Reference any git repository:

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/org/plugin.git"
  }
}
```

## Component Configuration

Override default component locations in plugin entries:

```json
{
  "name": "custom-plugin",
  "source": "./plugins/custom",
  "commands": [
    "./commands/core/",
    "./commands/extra/special.md"
  ],
  "agents": [
    "./agents/reviewer.md"
  ],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

**Component fields:**

- `commands` - String or array of command paths
- `agents` - String or array of agent file paths
- `hooks` - Object or path to hooks configuration
- `mcpServers` - Object or path to MCP configuration

The `${CLAUDE_PLUGIN_ROOT}` variable resolves to the plugin installation directory.

## Strict Mode

The `strict` field controls plugin.json requirements:

**Default (`strict: true`):**

- Plugin must contain `.claude-plugin/plugin.json`
- Marketplace entry supplements plugin manifest
- Plugin manifest takes precedence

**Relaxed (`strict: false`):**

- Plugin.json is optional
- Marketplace entry serves as complete manifest
- Use when plugin has no manifest file

```json
{
  "name": "no-manifest-plugin",
  "source": "./plugins/simple",
  "description": "Complete definition in marketplace",
  "version": "1.0.0",
  "strict": false
}
```

## Distribution

Users add the marketplace by repository location:

**GitHub:**

```text
/plugin marketplace add owner/repository
```

**Git URL:**

```text
/plugin marketplace add https://git.example.com/org/plugins.git
```

**Local path:**

```text
/plugin marketplace add /path/to/marketplace
```

Once added, users install plugins:

```text
/plugin install plugin-name@marketplace-name
```

## Validation

Verify structure before distribution:

```bash
claude plugin validate .
```

Test locally before publishing:

```bash
/plugin marketplace add ./local-marketplace
/plugin install test-plugin@local-marketplace
```
