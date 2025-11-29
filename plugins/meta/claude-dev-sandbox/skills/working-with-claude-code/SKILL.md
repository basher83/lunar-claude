---
name: working-with-claude-code
description: >
  Use when working with Claude Code CLI, plugins, hooks, MCP servers, skills,
  configuration, or any Claude Code feature. Provides tiered official
  documentation with auto-discovery and incremental sync.
---

# Working with Claude Code

## Overview

This skill provides official documentation for Claude Code from docs.claude.com,
organized into tiers for efficient context usage. Instead of guessing about
configuration paths or feature capabilities, load the relevant tier of docs.

## Tiered Documentation

Documentation is organized by relevance to plugin/skill development:

```text
references/
├── core/           # Essential docs (~25 files) - always load first
│   ├── plugins.md
│   ├── skills.md
│   ├── hooks.md
│   └── ...
├── extended/       # Additional docs (~40 files) - load on demand
│   ├── github-actions.md
│   ├── prompt-engineering/
│   └── ...
└── full/           # Complete site mirror (~150 files) - rarely needed
    ├── security.md
    ├── iam.md
    └── ...
```

## Loading Strategy

**Start with core docs** - they cover 90% of development needs:

| Task | Core File |
|------|-----------|
| Create a plugin | `core/docs-plugins.md`, `core/docs-plugins-reference.md` |
| Write a skill | `core/docs-skills.md` |
| Configure hooks | `core/docs-hooks.md`, `core/docs-hooks-guide.md` |
| Slash commands | `core/docs-slash-commands.md` |
| Subagents | `core/docs-sub-agents.md` |
| MCP servers | `core/docs-mcp.md` |
| Settings | `core/docs-settings.md` |

**Load extended docs** for specialized topics:

- Agent Skills API: `extended/docs-agents-and-tools-agent-skills-*`
- Prompt engineering: `extended/docs-build-with-claude-prompt-engineering-*`

**Load full docs** only when needed:

- Enterprise features: `full/docs-iam.md`, `full/docs-security.md`
- CI/CD: `full/docs-github-actions.md`, `full/docs-gitlab-ci-cd.md`

## Workflow

### For Specific Questions

1. Identify the relevant file from the tier tables
2. Load using Read tool: `references/core/docs-plugins.md`
3. Apply the solution from official documentation

### For Uncertain Topics

Search across all tiers:

```bash
rg "search term" references/
```

Or search within a specific tier:

```bash
rg "hook" references/core/
```

## Syncing Documentation

The skill includes `scripts/sync_docs.py` - a hybrid sync tool that combines:

- Recursive crawling (discovers all pages)
- llms.txt parsing (fast supplementary source)
- ETag + MD5 change detection (only downloads changed files)
- Direct .md fetching with HTML fallback

### Sync Commands

```bash
# Sync core docs only (~25 files, fast, recommended)
./scripts/sync_docs.py

# Include extended docs (~65 files)
./scripts/sync_docs.py --extended

# Full site mirror (~200+ files)
./scripts/sync_docs.py --all

# Check for updates without downloading (dry-run)
./scripts/sync_docs.py --check

# Force re-download everything
./scripts/sync_docs.py --force

# Re-discover pages (re-crawl site)
./scripts/sync_docs.py --rediscover

# JSON output for scripting
./scripts/sync_docs.py --format json
```

### When to Sync

- After Claude Code releases new features
- When documentation seems outdated
- Weekly for active development projects

## Quick Reference by Tier

### Core Tier (Always Relevant)

| File | Description |
|------|-------------|
| `docs-plugins.md` | Plugin development fundamentals |
| `docs-plugins-reference.md` | Complete plugin API specs |
| `docs-plugin-marketplaces.md` | Marketplace creation |
| `docs-skills.md` | Skill authoring guide |
| `docs-hooks.md` | Hooks overview |
| `docs-hooks-guide.md` | Hook implementation patterns |
| `docs-slash-commands.md` | Command development |
| `docs-sub-agents.md` | Subagent capabilities |
| `docs-settings.md` | Configuration reference |
| `docs-mcp.md` | MCP server integration |
| `docs-memory.md` | Memory management |
| `docs-output-styles.md` | Output formatting |
| `docs-statusline.md` | Status bar config |

### Extended Tier (On Demand)

| File | Description |
|------|-------------|
| `docs-agents-and-tools-agent-skills-overview.md` | Agent Skills architecture |
| `docs-agents-and-tools-agent-skills-quickstart.md` | Agent Skills getting started |
| `docs-agents-and-tools-agent-skills-best-practices.md` | Agent Skills guidelines |
| `docs-build-with-claude-prompt-engineering-*.md` | Prompt engineering guides |

### Full Tier (Specialized)

| Category | Files |
|----------|-------|
| Enterprise | `docs-iam.md`, `docs-security.md`, `docs-llm-gateway.md` |
| CI/CD | `docs-github-actions.md`, `docs-gitlab-ci-cd.md` |
| Cloud | `docs-amazon-bedrock.md`, `docs-google-vertex-ai.md` |
| IDE | `docs-vs-code.md`, `docs-jetbrains.md` |
| Setup | `docs-quickstart.md`, `docs-setup.md`, `docs-migration-guide.md` |

## Red Flags

If you find yourself:

- Guessing about config paths → Load `core/docs-settings.md`
- Speculating about APIs → Load relevant reference doc
- Unsure about hook events → Load `core/docs-hooks.md`
- Making feature assumptions → Search docs first

**Always consult official documentation before guessing.**

## What This Skill Does NOT Do

- This skill provides **documentation access**, not step-by-step tutorials
- For **how to build** workflows, combine this with domain-specific skills
- This is a **reference library** - read the specific file you need
