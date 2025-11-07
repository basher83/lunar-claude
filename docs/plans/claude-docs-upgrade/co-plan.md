# Claude Docs Scraper Variations

## Summary

Create three standalone scripts alongside `claude_docs.py` that demonstrate key scraping approaches from `web-scraping-methods-comparison.md`, plus supporting docs describing when to use each script.

## Steps

1. Baseline Review

- Re-read `plugins/meta/claude-docs/scripts/claude_docs.py` to map the current workflow and note elements each variant should adapt.
- Confirm each new script remains fully standalone with no shared modules, duplicating helper logic when it helps clarity.
- Review `plugins/devops/python-tools/skills/claude-agent-sdk/` for integration patterns we might echo, especially around MCP tooling.

1. Jina Reader Variant (`claude_docs_jina_reader.py`)

- Implement a Typer CLI that uses direct HTTP calls to `https://r.jina.ai/{url}` with optional API key, sequential downloads, and rate limiting per research best practices.
- Highlight CLI options for batch size, rate limiting, and retries according to “curl + Jina” recommendations.

1. Jina MCP Variant (`claude_docs_jina_mcp.py`)

- Build a CLI that leverages MCP client bindings (or thin wrappers) to call `parallel_read_url` with optimal batch sizes (3-4 URLs), handling timeouts and fallbacks.
- Include optional search step (`parallel_search_web`) for discovering new doc pages when desired.

1. Firecrawl Variant (`claude_docs_firecrawl.py`)

- Create a script using Firecrawl MCP APIs (`firecrawl_scrape`) with flags for metadata, structured extraction, and crawl depth, emphasizing reliability features.
- Ensure clear handling of API key env vars and sequential download flow with informative summaries.

1. Documentation Update

- Add or extend markdown (e.g., new README under `plugins/meta/claude-docs/scripts/` or update existing docs) summarizing each script’s intent, setup, and when to use it, referencing the comparison research.
