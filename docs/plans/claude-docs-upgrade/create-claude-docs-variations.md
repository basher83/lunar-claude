---
description: Create three standalone scripts alongside claude_docs.py that demonstrate key scraping approaches from web-scraping-methods-comparison.md, plus supporting docs describing when to use each script
---

Create variations of `claude_docs.py` based on research in `web-scraping-methods-comparison.md`. The research compares different web scraping methods including:

- Web Search Results (context-provided)
- curl + Jina Reader API (direct HTTP calls)
- Jina MCP Server (parallel operations)
- Firecrawl MCP Server (advanced scraping)

## Script Structure

Create separate standalone scripts (not flags/variations in one script). Each script is independent and optimized for its specific method.

## Feature Parity

Use method-specific optimizations (not full feature parity). Each script leverages its method's strengths:

- Jina: Parallel batch processing (3-4 URLs optimal)
- Firecrawl: Enhanced reliability and error handling

## Primary Goals

- Speed (parallel downloads for Jina)
- Reliability (better error handling for Firecrawl)
- Alternative methods (Jina/Firecrawl as fallbacks or alternatives)

## API Key Handling

Auto-detect from environment with optional override:

- Auto-detect: `JINA_API_KEY` and `FIRECRAWL_API_KEY` from environment
- Optional override: `--api-key` CLI argument
- Graceful fallback: Allow free tier usage when API key not available (Jina)

## Code Organization

Create standalone scripts (no shared module structure). Each script is completely self-contained for maximum portability.

## Implementation Approach

Create both standalone scripts (for hooks) AND MCP servers (for Claude agents):

- **Scripts**: Required for hook compatibility (hooks execute scripts directly)
- **MCP Servers**: Enable Claude agents to call tools directly for better integration
- **Both**: Provides flexibility - scripts for automation/hooks, MCP tools for agent workflows

## Variations to Create

Create all three methods:

1. Jina Reader API (direct HTTP calls)
2. Jina MCP parallel (parallel operations)
3. Firecrawl MCP (advanced scraping)

## SDK Patterns

Python scripts CAN call MCP tools through the Claude Agent SDK:

- Use `@tool` decorator and `create_sdk_mcp_server()` to wrap external APIs
- Leverage SDK patterns from `claude-agent-sdk` skill
- Scripts using MCP should demonstrate SDK orchestration patterns

## Supporting Documentation

Create supporting docs describing when to use each script.
