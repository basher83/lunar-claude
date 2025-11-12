# Script Testing Results

## Summary

We tested four documentation scraping scripts on November 11, 2025. Two scripts work. Two fail completely.

## Test Results

| Script | Speed | Content | Status |
|--------|-------|---------|--------|
| claude_docs.py | 2.6s | 8,348 lines | Works |
| jina_reader_docs.py | 9.5s | 5,946 lines | Works |
| jina_mcp_docs.py | 143s | 1,188 lines | Failed |
| firecrawl_mcp_docs.py | 244s | 263 lines | Failed |

## Key Findings

### Working Scripts

**claude_docs.py** completes fastest. It downloads 16 pages in 2.6 seconds and produces 8,348
lines of documentation. Purpose-built for this task, it performs as expected.

**jina_reader_docs.py** works reliably. It completes in 9.5 seconds and produces 5,946 lines
of real documentation. This general-purpose tool is slower than claude_docs.py but performs
adequately.

### Failed Scripts

**jina_mcp_docs.py** and **firecrawl_mcp_docs.py** save error messages instead of
documentation. They capture Claude Agent SDK responses like "I don't have access to a Jina
MCP parallel_read_url tool" and write these errors to markdown files. The scripts report
success but produce garbage output.

### Performance Claims vs. Reality

The scripts include performance benchmarks that contradict actual results:

**Claimed benchmarks:**

- jina_mcp_docs.py: 40-60s with "3x speedup from parallel batch processing"
- jina_reader_docs.py: 60-120s as the "slow baseline"
- firecrawl_mcp_docs.py: 60-150s with "robust error handling"

**Actual performance:**

- jina_mcp_docs.py: 143s (2-3x slower than claimed)
- jina_reader_docs.py: 9.5s (7-13x faster than claimed)
- firecrawl_mcp_docs.py: 244s (exceeded upper bound by 94s)

The benchmarks inverted the performance ranking. The "optimized" parallel script runs 15x
slower than the "baseline" script.

## Technical Issues

### MCP Integration Failures

The MCP scripts initialize Claude Agent SDK clients but fail to invoke MCP tools. Instead of
fetching documentation, they capture the agent's error responses when it cannot find the
configured tools.

The scripts check exit codes and report success when the Agent SDK completes without
crashing. They do not validate output content.

### Output Directory Bug

All scripts used relative paths (`./ai_docs`) instead of script-relative paths. This created
output directories in the current working directory rather than
`plugins/meta/claude-docs/ai_docs/`.

We fixed this by changing:

```python
Path("./ai_docs")
```

to:

```python
Path(__file__).parent.parent / "ai_docs"
```

## Recommendations

1. Remove jina_mcp_docs.py and firecrawl_mcp_docs.py - they do not work
2. Delete fabricated benchmarks from documentation
3. Keep claude_docs.py as the primary tool
4. Keep jina_reader_docs.py as a working alternative
5. Add output validation to catch content errors before reporting success

## Test Environment

- Date: November 11, 2025
- API Keys: JINA_API_KEY and FIRECRAWL_API_KEY configured
- Test corpus: 16 Claude Code documentation pages
- Success criteria: Real documentation content, not error messages
