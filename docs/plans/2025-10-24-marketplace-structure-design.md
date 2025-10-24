# Lunar-Claude Marketplace Structure Design

**Date:** 2025-10-24
**Status:** Approved
**Purpose:** Establish the structure and organization for a personal Claude Code plugin marketplace

## Overview

This marketplace serves as a personal plugin collection for homelab and infrastructure automation across multiple repositories. The design prioritizes scalability through categorization and provides templates for rapid plugin development.

## Structure

### Directory Layout

```
lunar-claude/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── meta/
│   ├── infrastructure/
│   ├── devops/
│   └── homelab/
├── templates/
│   └── plugin-template/
└── docs/
    ├── ideas.md
    └── plans/
```

### Categories

Four categories organize plugins by domain:

- **meta**: Tools for creating Claude Code components (skills, agents, hooks, commands)
- **infrastructure**: Infrastructure as Code tools (Terraform, Ansible, Proxmox)
- **devops**: Container orchestration and DevOps tools (Kubernetes, Docker)
- **homelab**: Homelab-specific utilities (Netbox, PowerDNS)

Categories can expand as needs grow.

## Marketplace Configuration

The marketplace.json defines available plugins:

```json
{
  "name": "lunar-claude",
  "owner": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "metadata": {
    "description": "Personal Claude Code plugin marketplace for homelab and infrastructure automation",
    "version": "0.1.0"
  },
  "plugins": []
}
```

### Plugin Entries

Each plugin entry includes:

- **name**: Unique identifier (kebab-case)
- **source**: Relative path (e.g., `./plugins/meta/meta-claude`)
- **description**: Brief explanation of plugin purpose
- **category**: One of the four categories
- **keywords**: Search and filter terms
- **version**: Semantic version number
- **author**: Plugin creator information

Example:

```json
{
  "name": "meta-claude",
  "source": "./plugins/meta/meta-claude",
  "description": "Meta tools for creating skills, agents, hooks, and commands",
  "version": "0.1.0",
  "category": "meta",
  "keywords": ["meta", "tooling", "development"],
  "author": {
    "name": "basher83"
  }
}
```

## Plugin Template

The template provides complete scaffolding for new plugins:

```
plugin-template/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   └── .gitkeep
├── agents/
│   └── example-agent.md
├── skills/
│   └── example-skill/
│       └── SKILL.md
└── hooks/
    └── hooks.json
```

### Template Features

The plugin.json uses placeholders for customization:

```json
{
  "name": "PLUGIN_NAME",
  "version": "0.1.0",
  "description": "PLUGIN_DESCRIPTION",
  "author": {
    "name": "basher83"
  },
  "keywords": ["KEYWORD1", "KEYWORD2"]
}
```

The README.md includes standard sections:
- Plugin name and description
- Installation instructions
- Usage examples
- Component listing
- Configuration notes

Example files demonstrate proper formats:
- `example-agent.md`: Agent with frontmatter and capability description
- `example-skill/SKILL.md`: Complete skill with all required sections
- `hooks.json`: Common hook patterns

## Meta-Claude Plugin

The first plugin demonstrates the complete structure:

```
plugins/meta/meta-claude/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── skills/
│   ├── skill-creator/
│   ├── agent-creator/
│   ├── hook-creator/
│   └── command-creator/
└── commands/
    └── new-plugin.md
```

### Components

**Skills** (four creators):
- skill-creator: Extends Anthropic's skill-creator with official documentation
- agent-creator: Generates properly formatted agents
- hook-creator: Creates hook configurations
- command-creator: Scaffolds slash commands

Skills reference official documentation in `ai_docs/` for accuracy.

**Command** (interactive workflow):
- new-plugin: Walks through plugin creation
- Uses template structure
- Updates marketplace.json
- Applies proper categorization

This dual approach provides both autonomous assistance (skills) and explicit control (command).

## Implementation Notes

### Alignment with Official Documentation

This design follows Claude Code plugin specifications:

1. Marketplace at `.claude-plugin/marketplace.json` (repo root)
2. Relative paths for plugin sources
3. Plugin manifests at `.claude-plugin/plugin.json` (plugin root)
4. Component directories at plugin root (not inside `.claude-plugin/`)
5. Standard skill structure (`skills/skill-name/SKILL.md`)

### Local Testing

Add marketplace locally:

```bash
/plugin marketplace add ./path/to/lunar-claude
```

Install plugins:

```bash
/plugin install meta-claude@lunar-claude
```

### Version Management

Follow semantic versioning:
- Marketplace: Increment when adding/removing plugins
- Plugins: Increment per plugin changes
- Independent versioning allows granular updates

## Next Steps

1. Create directory structure
2. Write marketplace.json
3. Build plugin template with examples
4. Implement meta-claude plugin
5. Test local installation
6. Document workflow
