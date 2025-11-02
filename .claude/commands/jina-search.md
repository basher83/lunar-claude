---
description: Search web and arXiv using Jina MCP tools with automatic URL reading
allowed-tools:
  - mcp__jina__search_web
  - mcp__jina__search_arxiv
  - mcp__jina__read_url
  - mcp__jina__parallel_read_url
argument-hint: [query]
---

# Jina Search Command

Search the web and academic sources using Jina MCP tools and automatically read results.

## Instructions

Use Jina MCP tools to search and read best practices and latest information:

1. **Web Search**: Use `search_web` for general queries
2. **Academic Search**: Use `search_arxiv` for theoretical deep learning or
   algorithm details
3. **Always Read Results**: `search_web` and `search_arxiv` cannot be used
   alone - always combine with `read_url` or `parallel_read_url` to read
   source content
4. **Efficiency**: Use `parallel_*` versions of search and read when
   processing multiple sources

## Query

Search for: $ARGUMENTS

## Workflow

1. Execute appropriate search (web or arXiv based on query)
2. Read returned URLs using `read_url` or `parallel_read_url`
3. Synthesize findings from multiple sources
4. Provide comprehensive answer with source citations

## Output

Create a comprehensive markdown file in `docs/research/` with your findings:

- **Rank findings by relevance** - Most important information first
- **Remove duplicate information** - Consolidate similar points
- **Target audience: Developers** - Technical depth appropriate for engineering teams
- **Include actionable insights** - Practical recommendations developers can implement
- **Cite all sources** - Link back to original URLs for verification
