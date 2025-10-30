# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

**lunar-claude** is a personal Claude Code plugin marketplace for homelab and
infrastructure automation. It provides reusable AI-powered tools organized into
a structured plugin ecosystem.

**Plugin Categories:**

- `meta/` - Tools for creating Claude Code components
- `infrastructure/` - Infrastructure as Code tools (Terraform, Ansible, Proxmox)
- `devops/` - Container orchestration and DevOps tools (Kubernetes, Docker)
- `homelab/` - Homelab-specific utilities (NetBox, PowerDNS)

## Development Commands

### Environment Setup

- See `mise.toml` for developer tools and tasks.

### Common Tasks

**Note**: See [docs/git-cliff-configuration.md](docs/git-cliff-configuration.md)
for detailed information about changelog configuration, commit message
conventions, and release workflow.

### Structure Verification

```bash
# Verify marketplace and plugin structure (validates plugin.json schema)
./scripts/verify-structure.py
```

### Local Plugin Testing

```bash
# Add marketplace locally
/plugin marketplace add /workspaces/lunar-claude

# Install a plugin for testing
/plugin install plugin-name@lunar-claude

# Uninstall plugin
/plugin uninstall plugin-name@lunar-claude
```

## Architecture

### Plugin Marketplace System

The marketplace uses a **central registry pattern**:

1. **Registry:** `.claude-plugin/marketplace.json` defines all plugins and
   maps them to source directories
2. **Plugin Manifests:** Each plugin has `.claude-plugin/plugin.json` with
   metadata
3. **Plugin Components:** Skills, commands, agents, and hooks reside in
   standard directories within each plugin

### Plugin Structure

Every plugin follows this structure:

```text
plugins/<category>/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (required)
├── skills/                  # AI-powered guidance (optional)
│   └── <skill-name>/
│       └── SKILL.md
├── commands/                # Slash commands (optional)
│   └── <command>.md
├── agents/                  # Subagent definitions (optional)
│   └── <agent>.md
├── hooks/                   # Automation hooks (optional)
│   └── <hook>.json
└── README.md                # User documentation (required)
```

### Component Interaction Flow

```text
User Request → Claude Code CLI → marketplace.json → Plugin Components
                                                    ↓
                                    Skills/Commands/Agents/Hooks
                                                    ↓
                                        Claude Execution Context
```

### Skills Architecture Pattern

Skills use a **layered documentation approach** for comprehensive AI context:

```text
skills/<skill-name>/
├── SKILL.md                 # Main skill definition (injected into Claude context)
├── patterns/                # Production-ready implementation patterns
├── reference/               # Technical references and API docs
├── anti-patterns/           # Common mistakes to avoid
├── examples/                # Real-world implementations
├── workflows/               # Process and workflow documentation
└── tools/                   # Helper scripts (Python/shell)
```

This structure allows skills to provide deep, structured knowledge without
overwhelming the main SKILL.md file.

## Creating New Plugins

### Using meta-claude Plugin

```bash
# Install meta-claude if not already installed
/plugin install meta-claude@lunar-claude

# Interactive plugin creation
/new-plugin
```

### Manual Creation

```bash
# 1. Copy template
cp -r templates/plugin-template/ plugins/<category>/<plugin-name>/

# 2. Customize plugin metadata
# Edit: plugins/<category>/<plugin-name>/.claude-plugin/plugin.json

# 3. Add to marketplace registry
# Edit: .claude-plugin/marketplace.json
# Add entry to "plugins" array

# 4. Verify structure
./scripts/verify-structure.py
```

## Key Files

### Marketplace Registry

- **Location:** `.claude-plugin/marketplace.json`
- **Purpose:** Central registry of all plugins with metadata
- **Update when:** Adding/removing plugins or changing plugin metadata

### Plugin Manifests

- **Location:** `plugins/<category>/<plugin-name>/.claude-plugin/plugin.json`
- **Purpose:** Individual plugin metadata
- **Update when:** Changing plugin version, description, or keywords

### Tool Configuration

- **Location:** `mise.toml`
- **Purpose:** Development tool versions and task automation
- **Tools:** Python 3.13, uv, pre-commit, markdownlint-cli2, git-cliff, shellcheck, and more

## Important Patterns

### SKILL.md Frontmatter

All skills must include YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description of what the skill does
---

# Skill Title
...
```

## Release Process

```bash
# 1. Update CHANGELOG.md
mise run changelog-bump 0.1.4

# 2. Review CHANGELOG.md changes

# 3. Update version in relevant files
# - .claude-plugin/marketplace.json (marketplace version)
# - plugins/<category>/<plugin-name>/.claude-plugin/plugin.json (plugin version)

# 4. Commit changes
git add CHANGELOG.md .claude-plugin/marketplace.json
git commit -m "chore: release v0.1.4"

# 5. Tag release
git tag -a v0.1.4 -m "Release v0.1.4"

# 6. Push to GitHub
git push && git push --tags
```

## Working with Skills

When creating or modifying skills:

1. **Structure:** Use SKILL.md as the main entry point
2. **Supporting docs:** Place detailed patterns/references in
   subdirectories
3. **Frontmatter:** Always include `name` and `description`
4. **Triggers:** Document "When to Use This Skill" section clearly
5. **Examples:** Provide real-world examples from actual
   infrastructure

When Claude activates a skill, it reads SKILL.md and referenced documentation
to provide expert guidance.

## Design Philosophy

- **Modularity:** Each plugin is independent and self-contained
- **Reusability:** Skills provide context for solving similar problems repeatedly
- **Production-focused:** Patterns come from real homelab/infrastructure experience
- **Documentation-first:** Extensive supporting materials ensure AI can provide expert guidance
- **Template-driven:** Plugin template ensures consistency across the marketplace
