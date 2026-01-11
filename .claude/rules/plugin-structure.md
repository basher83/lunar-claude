---
paths: plugins/**/*
---

# Plugin Structure Standards

## Required Plugin Layout

Every plugin must follow this structure:

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
│   └── hooks.json
└── README.md                # User documentation (required)
```

## Plugin Categories

- `meta/` - Tools for creating Claude Code components
- `infrastructure/` - Infrastructure as Code tools (Terraform, Ansible, Proxmox)
- `devops/` - Container orchestration and DevOps tools (Kubernetes, Docker)
- `homelab/` - Homelab-specific utilities (NetBox, PowerDNS)

## Plugin Manifest (plugin.json)

Required fields:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Brief description",
  "keywords": ["relevant", "tags"]
}
```

## Marketplace Registration

After creating a plugin:

1. Add entry to `.claude-plugin/marketplace.json`
2. Run `./scripts/verify-structure.py` to validate

## Creating New Plugins

```bash
# Create structure
mkdir -p plugins/<category>/<plugin-name>/{.claude-plugin,skills,commands,agents,hooks}

# Create plugin.json and README.md
# Add entry to .claude-plugin/marketplace.json
# Verify structure
./scripts/verify-structure.py
```
