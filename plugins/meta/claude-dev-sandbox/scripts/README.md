# Scripts

Development scripts for the claude-dev-sandbox plugin.

## sync_docs.py

Hybrid Claude Code documentation synchronization script. Combines best practices from multiple implementations to provide comprehensive, efficient documentation syncing.

### Features

- **Hybrid Discovery**: Recursive crawling + llms.txt parsing for comprehensive coverage
- **Tiered Storage**: core/extended/full classification for context-aware loading
- **Intelligent Caching**: ETag → Last-Modified → MD5 change detection
- **Direct Markdown**: Fetches `.md` endpoints with HTML fallback
- **Rate Limited**: Polite crawling with configurable delays

### Requirements

Uses inline script dependencies (uv):

```text
httpx>=0.27.0
rich>=13.0.0
typer>=0.12.0
beautifulsoup4>=4.12.0
```

### Usage

```bash
# Sync core docs only (~28 files, fastest)
./sync_docs.py

# Include extended docs (~54 files)
./sync_docs.py --extended

# Full site mirror (~100 files)
./sync_docs.py --all

# Check for updates without downloading
./sync_docs.py --check

# Force re-download all (ignore cache)
./sync_docs.py --force

# Re-crawl site to discover new pages
./sync_docs.py --rediscover

# JSON output for automation
./sync_docs.py --format json
```

### Tier Classification

| Tier | Content | Use Case |
|------|---------|----------|
| core | Agent SDK, plugins, skills, hooks, commands | Plugin/skill development |
| extended | Tool use, MCP, prompt engineering | Advanced integrations |
| full | All documentation | Complete reference |

### Output Structure

Default output: `../skills/official_docs/references/`

```text
skills/official_docs/
├── SKILL.md            # Skill that references the docs
└── references/         # Synced documentation
    ├── .sync_cache.json    # Cache metadata
    ├── core/               # Essential docs (~28 files)
    │   ├── docs-agent-sdk-plugins.md
    │   ├── docs-agent-sdk-skills.md
    │   └── ...
    ├── extended/           # Supplementary docs
    │   └── ...
    └── full/               # Everything else
        └── ...
```

Override with `--output-dir` / `-o` flag.

### Cache Behavior

- Discovery results cached for 24 hours
- Per-page metadata tracks ETag, Last-Modified, MD5 hash
- Subsequent syncs use HEAD requests to detect changes
- `--force` bypasses all caching
- `--rediscover` forces fresh crawl but preserves page metadata
