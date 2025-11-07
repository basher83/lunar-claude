# Claude Docs Script Comparison

> Guide to choosing the right script for downloading Claude Code documentation

## Available Scripts

1. **jina_reader_docs.py** - Direct HTTP calls via Jina Reader API
2. **jina_mcp_docs.py** - Parallel operations via Jina MCP Server + SDK
3. **firecrawl_mcp_docs.py** - Robust scraping via Firecrawl MCP + SDK

## Quick Decision Guide

**Need speed for multiple pages?** → Use `jina_mcp_docs.py` (parallel batching, ~3x faster)

**Need simplicity and no MCP setup?** → Use `jina_reader_docs.py` (direct HTTP, works anywhere)

**Need production reliability?** → Use `firecrawl_mcp_docs.py` (robust error handling, rich metadata)

---

## Detailed Comparison

### jina_reader_docs.py - Direct HTTP Calls

**Method:** Direct HTTP requests to Jina Reader API using `requests` library

**Best for:**

- Scripts and automation without MCP setup
- Simple one-off downloads
- Environments where MCP is not available
- Direct control over HTTP requests

**Pros:**

- ✅ Simple setup (just needs `requests` library)
- ✅ Works anywhere (no MCP required)
- ✅ Free tier available (20 RPM without API key)
- ✅ Transparent HTTP control

**Cons:**

- ❌ Sequential only (no parallel operations)
- ❌ Slower for multiple pages
- ❌ Manual error handling required

**Prerequisites:**

- None (optional: JINA_API_KEY for higher rate limits)

**Usage:**

```bash
# Free tier (20 RPM)
./jina_reader_docs.py

# With API key (500 RPM)
export JINA_API_KEY="your-key"
./jina_reader_docs.py

# Custom output directory
./jina_reader_docs.py --output-dir ./docs
```

**Performance:**

- Single page: ~2-8 seconds
- 16 pages sequential: ~60-120 seconds
- Rate limits: 20 RPM (free) / 500 RPM (with key)

---

### jina_mcp_docs.py - Parallel Operations

**Method:** Claude Agent SDK orchestrating Jina MCP `parallel_read_url` tool

**Best for:**

- Research tasks requiring multiple sources
- Speed optimization (3-4x faster than sequential)
- Batch processing 3-4 URLs at a time
- MCP-enabled environments

**Pros:**

- ✅ Fast (parallel operations)
- ✅ Optimal batching (3-4 URLs per batch)
- ✅ ~3x faster than sequential
- ✅ SDK orchestration patterns

**Cons:**

- ❌ Requires MCP server setup
- ❌ Timeout risk with >5 URLs per batch
- ❌ More complex (SDK + async)

**Prerequisites:**

- Jina MCP server configured in Claude settings
- JINA_API_KEY environment variable
- claude-agent-sdk>=0.1.6

**Usage:**

```bash
# Default (optimal batch size: 3)
./jina_mcp_docs.py

# Custom batch size
./jina_mcp_docs.py --batch-size 4

# Custom output directory
./jina_mcp_docs.py --output-dir ./docs
```

**Performance:**

- Batch of 3 URLs: ~8-12 seconds (vs 24 seconds sequential)
- 16 pages in 6 batches: ~40-60 seconds
- **~3x faster** than sequential
- Optimal batch size: 3-4 URLs

---

### firecrawl_mcp_docs.py - Robust Scraping

**Method:** Claude Agent SDK using Firecrawl MCP `firecrawl_scrape` tool

**Best for:**

- Production web scraping
- Complex or large pages
- Need for rich metadata
- Reliability over speed

**Pros:**

- ✅ Robust (handles edge cases well)
- ✅ Rich metadata (cache status, credits, etc.)
- ✅ Better error handling
- ✅ Main content extraction

**Cons:**

- ❌ Sequential only (no parallel operations)
- ❌ Slower than parallel methods
- ❌ Uses Firecrawl credits
- ❌ Requires MCP setup

**Prerequisites:**

- Firecrawl MCP server configured in Claude settings
- FIRECRAWL_API_KEY environment variable
- claude-agent-sdk>=0.1.6

**Usage:**

```bash
# Default (main content only)
./firecrawl_mcp_docs.py

# Include navigation/footers
./firecrawl_mcp_docs.py --no-main-content-only

# Custom output directory
./firecrawl_mcp_docs.py --output-dir ./docs
```

**Performance:**

- Single page: ~3-10 seconds
- 16 pages sequential: ~60-150 seconds
- More reliable than faster methods
- Better for complex pages

---

## Performance Comparison

| Script | 16 Pages | Speed | Complexity | Reliability |
|--------|----------|-------|------------|-------------|
| jina_reader_docs.py | ~60-120s | Slow | Low | Good |
| jina_mcp_docs.py | ~40-60s | **Fast** | Medium | Good |
| firecrawl_mcp_docs.py | ~60-150s | Slow | Medium | **Excellent** |

**Winner for speed:** jina_mcp_docs.py (parallel batching)

**Winner for simplicity:** jina_reader_docs.py (no MCP setup)

**Winner for reliability:** firecrawl_mcp_docs.py (robust error handling)

---

## Use Case Examples

### Quick One-Time Download

**Recommended:** `jina_reader_docs.py`

```bash
./jina_reader_docs.py --output-dir ./temp-docs
```

**Why:** Simple, no setup, good enough for one-time use.

---

### Daily Documentation Sync

**Recommended:** `jina_mcp_docs.py`

```bash
./jina_mcp_docs.py --output-dir ~/docs/claude --batch-size 3
```

**Why:** Fast parallel downloads save time on regular updates.

---

### Production Documentation Pipeline

**Recommended:** `firecrawl_mcp_docs.py`

```bash
./firecrawl_mcp_docs.py --output-dir /var/docs/claude --main-content-only
```

**Why:** Reliable, handles edge cases, rich metadata for monitoring.

---

## Common Options (All Scripts)

All three scripts support:

- `--output-dir, -o` - Custom output directory
- `--format` - Output format (`rich` or `json`)
- `--retries, -r` - Retry attempts (jina_reader_docs.py only)
- `--batch-size` - Batch size (jina_mcp_docs.py only)
- `--main-content-only` - Content extraction (firecrawl_mcp_docs.py only)

---

## API Key Setup

### Jina Reader API

```bash
# Free tier (20 RPM)
# No setup needed

# With API key (500 RPM)
export JINA_API_KEY="your-jina-api-key"
```

Get your API key from: <https://jina.ai/reader>

### Firecrawl API

```bash
export FIRECRAWL_API_KEY="your-firecrawl-api-key"
```

Get your API key from: <https://firecrawl.dev>

---

## Troubleshooting

### "Module not found: claude_agent_sdk"

**Scripts affected:** jina_mcp_docs.py, firecrawl_mcp_docs.py

**Solution:** Install the SDK:

```bash
pip install claude-agent-sdk>=0.1.6
```

### "MCP server not configured"

**Scripts affected:** jina_mcp_docs.py, firecrawl_mcp_docs.py

**Solution:** Configure MCP servers in Claude settings:

```json
{
  "mcpServers": {
    "jina-mcp-server": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.jina.ai/sse"],
      "env": {"JINA_API_KEY": "your-key"}
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {"FIRECRAWL_API_KEY": "your-key"}
    }
  }
}
```

### Rate limit errors (429)

**Scripts affected:** jina_reader_docs.py

**Solution:** Use API key or reduce request rate:

```bash
export JINA_API_KEY="your-key"  # Increases limit to 500 RPM
```

### Timeout errors

**Scripts affected:** jina_mcp_docs.py

**Solution:** Reduce batch size:

```bash
./jina_mcp_docs.py --batch-size 3  # Safer than 5
```

### Permission errors

**Scripts affected:** All scripts

**Solution:** Make scripts executable:

```bash
chmod +x scripts/jina_reader_docs.py
chmod +x scripts/jina_mcp_docs.py
chmod +x scripts/firecrawl_mcp_docs.py
```

---

## POC Limitations

These scripts are proof-of-concept implementations demonstrating different web scraping approaches. Known limitations:

- **jina_mcp_docs.py**: Optimal batch size tested for 16 pages; larger datasets may require adjustment
- **firecrawl_mcp_docs.py**: Sequential processing only; no parallel implementation available
- All scripts target Claude Code documentation structure; may need adaptation for other sites

---

## Summary

**Choose based on your priorities:**

- **Speed** → jina_mcp_docs.py (parallel batching)
- **Simplicity** → jina_reader_docs.py (no MCP setup)
- **Reliability** → firecrawl_mcp_docs.py (robust scraping)

**All scripts successfully download Claude Code documentation.**
The choice depends on your environment, performance needs, and reliability requirements.

---

## Additional Resources

- [Web Scraping Methods Comparison](../../../docs/research/web-scraping-methods-comparison.md) - Comprehensive guide to web scraping approaches
- [Jina Reader API Documentation](https://jina.ai/reader)
- [Jina MCP Server](https://github.com/jina-ai/MCP)
- [Firecrawl Documentation](https://firecrawl.dev)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)

---

## Document History

Last updated: 2025-11-06
