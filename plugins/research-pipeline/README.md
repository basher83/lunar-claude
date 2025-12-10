# research-pipeline

Multi-agent research pipeline with parallel researchers and synthesis.

## Overview

Orchestrates 4 specialized researcher agents (GitHub, Tavily, DeepWiki, Exa) to gather information from multiple sources, then synthesizes findings with source authority hierarchy.

## Installation

```bash
/plugin install research-pipeline@lunar-claude
```

## Usage

```bash
/research-pipeline:lunar-research "your research query"
```

## Features

- **4 Parallel Researchers**: GitHub (code/repos), Tavily (web/tutorials), DeepWiki (official docs), Exa (semantic search)
- **Synthesizer Agent**: Combines findings using authority hierarchy (official docs > community > code > semantic)
- **Knowledge Base Caching**: 30-day TTL cache shared across projects
- **Schema Validation**: JSON Schema for standardized report format

## Components

### Command

- `lunar-research` - Main orchestrator command

### Agents

| Agent | Purpose | MCP Tools |
|-------|---------|-----------|
| `github-researcher` | Find repositories and code patterns | GitHub MCP |
| `tavily-researcher` | Find tutorials and community content | Tavily MCP |
| `deepwiki-researcher` | Find official documentation | DeepWiki MCP |
| `exa-researcher` | Semantic search for related content | Exa MCP |
| `synthesizer-agent` | Combine findings into synthesis | None |

### Schemas

- `research-report.schema.json` - JSON Schema for researcher output format

### Scripts

- `validate_research_report.py` - Validate reports against schema

## Cache Structure

Research results are cached at plugin level, shared across all projects:

```text
${CLAUDE_PLUGIN_ROOT}/cache/
├── index.json                    # Knowledge base index (tracked in git)
└── [normalized-query]/           # Per-query cache (gitignored)
    ├── github-report.json
    ├── tavily-report.json
    ├── deepwiki-report.json
    ├── exa-report.json
    └── synthesis.md
```

## Prerequisites

Requires MCP servers configured for:

- GitHub (`mcp__github__*`)
- Tavily (`mcp__tavily__*`)
- DeepWiki (`mcp__deepwiki__*`)
- Exa (`mcp__exa__*`)
