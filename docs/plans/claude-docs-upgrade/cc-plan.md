# Create claude_docs.py Script Variations

## Task Context

**Original Request:**
Create variations of `claude_docs.py` based on research in `web-scraping-methods-comparison.md`

**Clarifying Questions & Answers:**

1. **Which variations to create?**
   - Answer: All three methods (Jina Reader API, Jina MCP parallel, Firecrawl MCP)

2. **Script structure?**
   - Answer: Separate standalone scripts

3. **Feature retention?**
   - Answer: Vary by method (each script optimized for its specific use case)

**Key Refinement:**

- Python scripts CAN call MCP tools through the Claude Agent SDK
- Use `@tool` decorator and `create_sdk_mcp_server()` to wrap external APIs
- Leverage SDK patterns from `claude-agent-sdk` skill
- Scripts using MCP should demonstrate SDK orchestration patterns

## Overview

Create three standalone scripts based on web scraping research, each optimized for different use cases. All scripts will download Claude Code documentation but use different methods and feature sets appropriate to their design goals.

## New Scripts to Create

### 1. `claude_docs_jina.py` - Simple Direct API Access

**Location**: `plugins/meta/claude-docs/scripts/claude_docs_jina.py`

**Method**: Direct HTTP calls to Jina Reader API (`https://r.jina.ai/{url}`)

**Features**:

- Sequential downloads with explicit rate limiting
- Simple retry logic with exponential backoff
- Basic progress output (Rich console)
- Lightweight caching (just timestamps and size)
- CLI options: `--output-dir`, `--retries`, `--all`, `--rate-limit` (RPM)

**Key Implementation Details**:

- Use `requests` library (add to dependencies)
- Rate limiter class from research doc best practices
- Simpler error handling than original
- No JSON output mode (keep it simple)
- Cache format: `{page: {timestamp, size}}`

**When to Use Note**: Best for simple automation, scripts, works anywhere without MCP

### 2. `claude_docs_jina_mcp.py` - Speed-Optimized Parallel

**Location**: `plugins/meta/claude-docs/scripts/claude_docs_jina_mcp.py`

**Method**: Jina MCP Server tools (`parallel_read_url`, `read_url`)

**Features**:

- Batch processing with optimal size (3-4 URLs per batch)
- Parallel downloads within batches
- Timeout handling and fallback to smaller batches
- Progress tracking per batch
- No caching (speed is priority)
- CLI options: `--output-dir`, `--all`, `--batch-size`

**Key Implementation Details**:

- Cannot actually call MCP tools from Python script - this will be a **documentation/reference script**
- Show how to use Jina MCP tools for this use case
- Include batch processing logic as reference
- Document optimal batch sizes (3-4 URLs)
- Include timeout handling patterns

**When to Use Note**: Best for research tasks, multiple sources, when speed matters (requires MCP-enabled environment)

### 3. `claude_docs_firecrawl.py` - Production-Grade Reliability

**Location**: `plugins/meta/claude-docs/scripts/claude_docs_firecrawl.py`

**Method**: Firecrawl MCP Server tools (`firecrawl_scrape`)

**Features**:

- Sequential downloads with robust error handling
- Rich metadata caching (ETags, status codes, credits used)
- Detailed progress with scrape metadata
- JSON and Rich output modes (like original)
- Retry logic for edge cases
- CLI options: `--output-dir`, `--retries`, `--all`, `--check`, `--format`, `--only-main-content`

**Key Implementation Details**:

- Similar to original but using Firecrawl patterns
- Cannot actually call MCP tools - will be **reference/documentation script**
- Cache includes: ETag, last-modified, credits, status, size
- Handle large file responses gracefully
- Show metadata in progress output

**When to Use Note**: Best for production use, complex pages, when reliability > speed (requires MCP-enabled environment)

## Script Comparison Matrix

Add to plugin README:

```markdown
## Script Variations

| Script | Method | Speed | Features | Best For |
|--------|--------|-------|----------|----------|
| `claude_docs.py` (original) | httpx | Medium | Full-featured | General use |
| `claude_docs_jina.py` | Jina Reader API | Fast | Simple, works anywhere | Automation, scripts |
| `claude_docs_jina_mcp.py` | Jina MCP parallel | Fastest | Speed-optimized | Research, batch processing |
| `claude_docs_firecrawl.py` | Firecrawl MCP | Slower but robust | Production-grade | Complex pages, reliability |
```

## Implementation Notes

### SDK MCP Server Approach

The Jina MCP and Firecrawl scripts will use the **Claude Agent SDK** to create in-process MCP servers that wrap external APIs:

1. **Use `@tool` decorator** to define tools that call Jina/Firecrawl APIs
2. **Use `create_sdk_mcp_server()`** to bundle tools into MCP servers
3. **Use `ClaudeSDKClient`** to have Claude orchestrate the downloads using these tools
4. **Demonstrate SDK patterns** from the claude-agent-sdk skill

This approach shows how to:

- Create custom MCP tools in Python
- Wrap external APIs as MCP tools
- Use Claude as an orchestrator for complex workflows
- Apply SDK best practices for tool design

### Dependencies

Update `claude_docs_jina.py` dependencies to include:

```python
# dependencies = [
#   "requests>=2.31.0",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
# ]
```

### Shared Constants

All scripts share:

- Same base URLs and page lists from original
- Same output directory default
- Same page name flattening logic

### README Updates

Add section comparing all four scripts with decision tree on when to use each.

## File Structure After Completion

```text
plugins/meta/claude-docs/
├── scripts/
│   ├── claude_docs.py              # Original (httpx)
│   ├── claude_docs_jina.py         # New: Jina Reader API
│   ├── claude_docs_jina_mcp.py     # New: Jina MCP reference
│   └── claude_docs_firecrawl.py    # New: Firecrawl MCP reference
├── README.md                        # Updated with script comparison
└── ...
```
