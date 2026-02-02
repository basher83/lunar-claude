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

## Commands

```bash
# Environment setup
mise install                          # Install all tools (Python, ruff, uv, etc.)
uv sync --group dev                   # Install Python dependencies
mise run hooks-install                # Install pre-commit + infisical hooks

# Code quality
ruff check .                          # Lint Python
ruff format .                         # Format Python
pyright                               # Type check (strict mode)
mise run pre-commit-run               # Run all pre-commit hooks

# Testing
pytest tests/                         # Run all tests
pytest tests/test_verify_structure.py # Run single test file

# Validation
./scripts/verify-structure.py         # Validate plugin/marketplace structure
mise run markdown-lint                # Lint markdown (rumdl)
mise run link-check                   # Check links in markdown (lychee)

# Changelog
mise run changelog                    # Update CHANGELOG.md
mise run changelog-bump <version>     # Release with version bump
```

## Code Quality

- **Python >=3.13** managed via mise + uv
- **Formatter/Linter**: ruff (config in `ruff.toml`)
- **Type checker**: pyright strict mode (`pyrightconfig.json`)
- **Standalone scripts**: Use PEP 723 inline metadata with `#!/usr/bin/env -S uv run`

## Claude Tools

Use the `Skill` tool to load pre-built agent skills (can load multiple at once).
Use `SlashCommand` to execute custom slash commands programmatically.

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
