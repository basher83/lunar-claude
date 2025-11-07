# Create Variations of claude_docs.py: Scripts + MCP Tools

## Task Context

### Original Request
Create variations of `claude_docs.py` based on research in `web-scraping-methods-comparison.md`. The research compares different web scraping methods including:
- Web Search Results (context-provided)
- curl + Jina Reader API (direct HTTP calls)
- Jina MCP Server (parallel operations)
- Firecrawl MCP Server (advanced scraping)

### Requirements & Decisions

**1. Script Structure**
- **Decision**: Separate standalone scripts (not flags/variations in one script)
- **Rationale**: Each script is independent and optimized for its specific method

**2. Feature Parity**
- **Decision**: Method-specific optimizations (not full feature parity)
- **Rationale**: Each script leverages its method's strengths:
  - Jina: Parallel batch processing (3-4 URLs optimal)
  - Firecrawl: Enhanced reliability and error handling

**3. Primary Goals**
- **Decision**: All of the above
- **Goals**:
  - Speed (parallel downloads for Jina)
  - Reliability (better error handling for Firecrawl)
  - Alternative methods (Jina/Firecrawl as fallbacks or alternatives)

**4. API Key Handling**
- **Decision**: Auto-detect from environment with optional override
- **Implementation**:
  - Auto-detect: `JINA_API_KEY` and `FIRECRAWL_API_KEY` from environment
  - Optional override: `--api-key` CLI argument
  - Graceful fallback: Allow free tier usage when API key not available (Jina)

**5. Code Organization**
- **Decision**: Standalone scripts (no shared module structure)
- **Rationale**: Each script is completely self-contained for maximum portability

**6. Implementation Approach**
- **Decision**: Both standalone scripts (for hooks) AND MCP servers (for Claude agents)
- **Rationale**:
  - **Scripts**: Required for hook compatibility (hooks execute scripts directly)
  - **MCP Servers**: Enable Claude agents to call tools directly for better integration
  - **Both**: Provides flexibility - scripts for automation/hooks, MCP tools for agent workflows

### Research-Based Insights

From `web-scraping-methods-comparison.md`:
- **Jina Reader API**: Best for speed with parallel operations (3-4 URLs optimal, ~10s for 3 URLs vs ~15s sequential)
- **Firecrawl API**: Best for reliability and production scraping (handles large/complex pages well)
- **Rate Limits**: Jina (20 RPM free, 500 RPM with API key), Firecrawl (varies by plan)
- **Performance**: Jina MCP parallel operations are fastest for batches ≤4 URLs

## Overview

Create both standalone scripts (for hooks) and MCP servers (for Claude agents) using different web scraping methods:

- **Jina**: Parallel batch processing (3-4 URLs optimal)
- **Firecrawl**: Enhanced reliability and error handling

## Implementation Plan

### Part 1: Standalone Scripts (for Hooks)

#### 1.1 Create Jina Reader API Script

**File**: `plugins/meta/claude-docs/scripts/claude_docs_jina.py`

**Key Features**:

- Uses Jina Reader API (`r.jina.ai/{url}`) instead of direct HTTP
- **Parallel batch processing**: Process 3-4 URLs simultaneously (optimal per research)
- **Rate limiting**: Built-in rate limiter (500 RPM with API key, 20 RPM without)
- **Auto-detect API key**: `JINA_API_KEY` from environment, `--api-key` override
- Same CLI interface as original (for hook compatibility)
- **Standalone**: All code self-contained

**Method-Specific Optimizations**:

- Batch URLs into groups of 3-4 for parallel processing
- Use `concurrent.futures.ThreadPoolExecutor` for parallel downloads
- Rate limiter class to respect Jina API limits
- Exponential backoff on rate limit errors (429)
- Clean markdown output (Jina Reader's strength)
- URL transformation: `https://docs.claude.com/...` → `<https://r.jina.ai/https://docs.claude.com/>...`

**Dependencies**: `httpx>=0.27.0`, `rich>=13.0.0`, `typer>=0.12.0`

#### 1.2 Create Firecrawl API Script

**File**: `plugins/meta/claude-docs/scripts/claude_docs_firecrawl.py`

**Key Features**:

- Uses Firecrawl API for web scraping
- **Enhanced reliability**: Better error handling, retry logic
- **Metadata extraction**: Leverage Firecrawl's rich metadata
- **Auto-detect API key**: `FIRECRAWL_API_KEY` from environment, `--api-key` override
- Same CLI interface as original (for hook compatibility)
- **Standalone**: All code self-contained

**Method-Specific Optimizations**:

- Robust retry logic with exponential backoff
- Better handling of large/complex pages
- Extract and store metadata (status, cache info, credits used)
- Handle Firecrawl-specific error responses
- Support for `onlyMainContent` option to reduce size
- Sequential processing (Firecrawl's strength is reliability, not parallelism)

**Dependencies**: `httpx>=0.27.0`, `rich>=13.0.0`, `typer>=0.12.0`

**Note**: Research Firecrawl HTTP API endpoint (likely `https://api.firecrawl.dev/v0/scrape`). If only MCP available, document limitation.

### Part 2: MCP Servers (for Claude Agents)

#### 2.1 Create Jina Docs MCP Server

**File**: `plugins/meta/claude-docs/mcp/jina_docs_mcp.py`

**Server Name**: `jina_docs_mcp`

**Tools to Implement**:

1. `jina_docs_download_page` - Download single documentation page using Jina Reader
2. `jina_docs_download_batch` - Download multiple pages in parallel (3-4 optimal)
3. `jina_docs_check_updates` - Check which pages need updating (HEAD requests)
4. `jina_docs_list_available` - List all available documentation pages

**Key Features**:

- Uses FastMCP framework (`mcp.server.fastmcp`)
- Pydantic models for input validation
- Async/await for all network operations
- Parallel batch processing for multiple URLs
- Rate limiting built-in
- Auto-detect API key from environment

**Tool Structure**:

```python
@mcp.tool(
    name="jina_docs_download_batch",
    annotations={
        "title": "Download Claude Docs (Batch)",
        "readOnlyHint": False,  # Downloads files
        "destructiveHint": False,
        "idempotentHint": True,  # Re-downloading is safe
        "openWorldHint": True  # Accesses external URLs
    }
)
async def jina_docs_download_batch(params: DownloadBatchInput) -> str:
    '''Download multiple Claude Code documentation pages in parallel using Jina Reader API.

    Optimized for batch operations with 3-4 URLs processed simultaneously.
    '''
```

**Dependencies**: `mcp>=1.0.0`, `httpx>=0.27.0`, `pydantic>=2.0.0`

#### 2.2 Create Firecrawl Docs MCP Server

**File**: `plugins/meta/claude-docs/mcp/firecrawl_docs_mcp.py`

**Server Name**: `firecrawl_docs_mcp`

**Tools to Implement**:

1. `firecrawl_docs_scrape_page` - Scrape single documentation page with Firecrawl
2. `firecrawl_docs_check_updates` - Check which pages need updating
3. `firecrawl_docs_list_available` - List all available documentation pages
4. `firecrawl_docs_extract_metadata` - Extract structured metadata from pages

**Key Features**:

- Uses FastMCP framework
- Pydantic models for input validation
- Enhanced error handling and retry logic
- Metadata extraction capabilities
- Sequential processing (reliability over speed)
- Auto-detect API key from environment

**Dependencies**: `mcp>=1.0.0`, `httpx>=0.27.0`, `pydantic>=2.0.0`

**Note**: If Firecrawl only provides MCP (not HTTP API), this server may wrap the existing Firecrawl MCP server or document that agents should use Firecrawl MCP directly.

### Part 3: MCP Configuration

#### 3.1 Create MCP Configuration Files

**Files**:

- `plugins/meta/claude-docs/.mcp.json` - MCP server configuration for both servers

**Configuration Structure**:

```json
{
  "mcpServers": {
    "jina-docs": {
      "command": "uv",
      "args": [
        "run",
        "--script",
        "${CLAUDE_PLUGIN_ROOT}/mcp/jina_docs_mcp.py"
      ],
      "env": {
        "JINA_API_KEY": "${JINA_API_KEY}"
      }
    },
    "firecrawl-docs": {
      "command": "uv",
      "args": [
        "run",
        "--script",
        "${CLAUDE_PLUGIN_ROOT}/mcp/firecrawl_docs_mcp.py"
      ],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

### Part 4: Documentation Updates

**File**: `plugins/meta/claude-docs/README.md`

Add sections explaining:

- **Scripts**: When to use each script variation (hooks, CLI)
- **MCP Servers**: When to use MCP tools (Claude agents)
- **Performance characteristics**: Based on research findings
- **API key requirements**: For each method
- **Usage examples**: For both scripts and MCP tools
- **Comparison table**: Scripts vs MCP servers

## Technical Details

### Best Practices from python-tools Skills

1. **Environment Variable Handling**: Use `os.getenv()` with optional fallback, don't exit if missing (allow free tier)
2. **Error Handling**: Specific handling for `httpx.HTTPStatusError` (401, 404, 429, 500+) and `httpx.RequestError`
3. **Timeout**: Always set timeout (10.0 seconds default, 30.0 for downloads)
4. **Client Context**: Use `with httpx.Client()` for multiple requests (scripts) or `async with httpx.AsyncClient()` (MCP)
5. **Exit Codes**: Use `sys.exit(0)` for success, `sys.exit(1)` for errors (scripts only)
6. **Type Hints**: Include type hints throughout
7. **Docstrings**: Include docstrings for all functions
8. **Rich Console**: Use `rich.console.Console` for output (scripts only)

### Script Implementation Details

**Jina Script**:

- Parallel Processing: `ThreadPoolExecutor` with max_workers=3-4
- Rate Limiter: Track requests per minute, sleep when needed
- URL Transformation: Prepend `https://r.jina.ai/` to target URLs
- Headers: `X-Return-Format: markdown`, `Authorization: Bearer {key}` if available
- Error Handling: Handle 429 with exponential backoff, 401 for invalid keys

**Firecrawl Script**:

- API Endpoint: `https://api.firecrawl.dev/v0/scrape` (research required)
- Request Format: POST with JSON body
- Sequential: Process URLs one at a time
- Error Handling: Robust retry logic, handle Firecrawl-specific errors

### MCP Server Implementation Details

**FastMCP Patterns**:

- Server naming: `jina_docs_mcp`, `firecrawl_docs_mcp`
- Tool naming: `jina_docs_*`, `firecrawl_docs_*` (prefixed to avoid conflicts)
- Pydantic models: All inputs validated with BaseModel and Field()
- Async operations: All network calls use async/await
- Error handling: Consistent error formatting across tools
- Response formats: Support both markdown and JSON output

**Jina MCP Server**:

- Parallel batch tool: Process 3-4 URLs simultaneously
- Rate limiting: Built into tool implementation
- Progress reporting: Use Context for long operations

**Firecrawl MCP Server**:

- Sequential processing: One URL at a time for reliability
- Metadata extraction: Return structured metadata
- Error recovery: Enhanced retry logic

### CLI Compatibility (Scripts Only)

All scripts must support:

- `--output-dir` / `-o`
- `--retries` / `-r`
- `--all`
- `--check`
- `--interactive` / `-i`
- `--format` (rich/json)
- `--api-key` (new, optional override for environment variable)

## Files to Create/Modify

### Scripts (Standalone)

1. `plugins/meta/claude-docs/scripts/claude_docs_jina.py` (new)
2. `plugins/meta/claude-docs/scripts/claude_docs_firecrawl.py` (new)
3. `plugins/meta/claude-docs/scripts/claude_docs.py` (unchanged)

### MCP Servers

1. `plugins/meta/claude-docs/mcp/jina_docs_mcp.py` (new)
2. `plugins/meta/claude-docs/mcp/firecrawl_docs_mcp.py` (new)
3. `plugins/meta/claude-docs/.mcp.json` (new)

### Documentation

1. `plugins/meta/claude-docs/README.md` (update)

## Testing Considerations

### Scripts

- Test parallel processing with 3-4 URLs (Jina script)
- Test rate limiting behavior (Jina script)
- Test API key detection (env var vs CLI arg) for both scripts
- Test fallback when API key not available (Jina free tier)
- Verify hook compatibility (JSON output mode)
- Test Firecrawl API endpoint availability and response format

### MCP Servers

- Test tool registration and discovery
- Test input validation with Pydantic models
- Test parallel batch operations (Jina MCP)
- Test error handling and retry logic
- Test API key detection from environment
- Verify MCP server can be started and tools are callable
