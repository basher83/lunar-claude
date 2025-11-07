# claude-docs

Auto-sync official Claude Code documentation as an Agent Skill with fresh
reference material.

## What it does

- **Provides a skill** with official Claude Code documentation from
  docs.claude.com
- **Auto-updates docs** via SessionStart hook to keep content fresh
- **Progressive disclosure** - loads only relevant docs to manage context
- **14 reference files** covering plugins, skills, hooks, commands, and more

## Installation

```bash
/plugin marketplace add your-org/lunar-claude
/plugin install claude-docs@lunar-claude
```

## Usage

The `claude-docs` skill activates automatically when you ask about Claude
Code features:

- "How do I create a plugin?"
- "What's the structure of SKILL.md?"
- "How do hooks work?"
- "How can I add a slash command?"

Claude will use the skill to access up-to-date official documentation and
provide accurate answers.

## How it works

### Components

- **Skill** (`skills/claude-docs/`) - Entry point with progressive disclosure
  guidance
- **Reference docs** (`skills/claude-docs/reference/`) - 14 official
  documentation files
- **SessionStart hook** (`hooks/hooks.json`) - Auto-updates docs on session
  start
- **Update scripts** (`scripts/`) - Multiple scripts for different scraping methods:
  - `claude_docs.py` - Original direct HTTP method
  - `claude_docs_jina.py` - Jina Reader API with parallel batch processing
  - `claude_docs_firecrawl.py` - Firecrawl API with enhanced reliability
- **MCP Servers** (`mcp/`) - MCP tools for Claude agents:
  - `jina_docs_mcp.py` - Jina-based MCP server
  - `firecrawl_docs_mcp.py` - Firecrawl-based MCP server

### Documentation files

- plugins.md, plugins-reference.md, plugin-marketplaces.md
- skills.md, agent-skills-overview.md, agent-skills-quickstart.md,
  agent-skills-best-practices.md
- slash-commands.md
- hooks-guide.md, hooks.md
- settings.md, output-styles.md, statusline.md
- sub-agents.md

### Auto-update behavior

The SessionStart hook runs the update script in JSON mode, which:

1. Checks cached ETags for each documentation file
2. Downloads only changed files (using HTTP conditional requests)
3. Completes in <1 second when docs are fresh
4. Updates `.download_cache.json` with metadata

## Development

### Scripts (for Hooks and CLI)

Three standalone scripts are available, each optimized for different use cases:

#### 1. Original Script (`claude_docs.py`)

Direct HTTP method - simple and reliable:

```bash
./scripts/claude_docs.py
./scripts/claude_docs.py --all        # Download all 70+ pages
./scripts/claude_docs.py --check      # Check for updates (dry-run)
```

#### 2. Jina Reader Script (`claude_docs_jina.py`)

**Best for:** Speed with parallel batch processing (3-4 URLs optimal)

- Uses Jina Reader API (`r.jina.ai`) for clean markdown extraction
- Parallel batch processing (3-4 URLs simultaneously)
- Rate limiting: 500 RPM with API key, 20 RPM free tier
- Auto-detects `JINA_API_KEY` from environment

```bash
./scripts/claude_docs_jina.py
./scripts/claude_docs_jina.py --api-key YOUR_KEY  # Override env var
./scripts/claude_docs_jina.py --all               # Download all pages
```

**Performance:** ~10s for 3 URLs (parallel) vs ~15s sequential

#### 3. Firecrawl Script (`claude_docs_firecrawl.py`)

**Best for:** Reliability and production scraping

- Enhanced error handling and retry logic
- Better handling of large/complex pages
- Metadata extraction (status, credits used)
- Requires `FIRECRAWL_API_KEY` environment variable

```bash
export FIRECRAWL_API_KEY=your_key
./scripts/claude_docs_firecrawl.py
./scripts/claude_docs_firecrawl.py --api-key YOUR_KEY  # Override env var
./scripts/claude_docs_firecrawl.py --all               # Download all pages
```

### Script Options (All Scripts)

All scripts support the same CLI interface for hook compatibility:

- `--output-dir DIR` - Custom output directory
- `--retries N` - Max retry attempts (default: 3)
- `--all` - Download all pages from docs map
- `--check` - Dry-run mode (check only, don't download)
- `--interactive, -i` - Interactively select pages
- `--format json|rich` - Output format (hook uses json, user uses rich)
- `--api-key KEY` - Override API key environment variable (Jina/Firecrawl scripts)

### MCP Servers (for Claude Agents)

MCP servers enable Claude agents to call tools directly for better integration:

#### Jina Docs MCP Server

**Server:** `jina-docs`  
**File:** `mcp/jina_docs_mcp.py`

**Tools:**
- `jina_docs_download_page` - Download single page using Jina Reader
- `jina_docs_download_batch` - Download multiple pages in parallel (3-4 optimal)
- `jina_docs_check_updates` - Check which pages need updating
- `jina_docs_list_available` - List all available documentation pages

**Configuration:** Set `JINA_API_KEY` environment variable (optional, free tier available)

#### Firecrawl Docs MCP Server

**Server:** `firecrawl-docs`  
**File:** `mcp/firecrawl_docs_mcp.py`

**Tools:**
- `firecrawl_docs_scrape_page` - Scrape single page with Firecrawl
- `firecrawl_docs_check_updates` - Check which pages need updating
- `firecrawl_docs_list_available` - List all available documentation pages
- `firecrawl_docs_extract_metadata` - Extract structured metadata from pages

**Configuration:** Set `FIRECRAWL_API_KEY` environment variable (required)

### MCP Configuration

The plugin includes `.mcp.json` configuration file that registers both MCP servers:

```json
{
  "mcpServers": {
    "jina-docs": {
      "command": "uv",
      "args": ["run", "--script", "${CLAUDE_PLUGIN_ROOT}/mcp/jina_docs_mcp.py"],
      "env": {
        "JINA_API_KEY": "${JINA_API_KEY}"
      }
    },
    "firecrawl-docs": {
      "command": "uv",
      "args": ["run", "--script", "${CLAUDE_PLUGIN_ROOT}/mcp/firecrawl_docs_mcp.py"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

### When to Use Each Method

| Method | Use Case | Speed | Reliability | API Key Required |
|--------|----------|-------|-------------|------------------|
| **Original Script** | Simple, direct downloads | Medium | Good | No |
| **Jina Script** | Fast batch downloads (3-4 URLs) | Fastest | Good | Optional (free tier available) |
| **Firecrawl Script** | Production, complex pages | Medium | Best | Yes |
| **Jina MCP** | Agent workflows needing parallel downloads | Fastest | Good | Optional |
| **Firecrawl MCP** | Agent workflows needing reliability | Medium | Best | Yes |

### Performance Characteristics

Based on research findings:

- **Jina Reader API**: Best for speed with parallel operations (3-4 URLs optimal, ~10s for 3 URLs vs ~15s sequential)
- **Firecrawl API**: Best for reliability and production scraping (handles large/complex pages well)
- **Rate Limits**: 
  - Jina: 20 RPM free, 500 RPM with API key
  - Firecrawl: Varies by plan

## License

MIT
