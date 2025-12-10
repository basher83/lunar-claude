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

## Essential Tools

The `SlashCommand` tool allows Claude to execute custom slash commands
programmatically during a conversation.

The `Skill` tool allows Claude to execute skills programmatically during a
conversation. Pre-built Agent Skills extend Claude's capabilities with
specialized expertise.

**HINT**: Claude can load multiple skills at once via the `Skill` tool.

## Key Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Central plugin registry |
| `plugins/<cat>/<name>/.claude-plugin/plugin.json` | Plugin manifests |
| `mise.toml` | Developer tools and task automation |
| `./scripts/verify-structure.py` | Validate marketplace structure |

## Modular Rules

Path-specific rules are in `.claude/rules/`:

- `audit-protocol.md` - Audit agent invocation standards
- `python-scripts.md` - Python/uv script conventions
- `skill-development.md` - SKILL.md authoring standards
- `plugin-structure.md` - Plugin directory conventions
- `documentation.md` - Markdown and docs standards
