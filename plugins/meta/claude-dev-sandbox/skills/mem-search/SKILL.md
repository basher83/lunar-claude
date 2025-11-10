---
name: mem-search
description: >
  Searches claude-mem's persistent memory system to retrieve historical context,
  past decisions, bugs, features, or observations. Use when gathering context
  from previous sessions, investigating past work, or understanding project
  history. Implements progressive disclosure and token-efficient search patterns
  for the 9 MCP search tools.
---

# Memory Search

## Overview

Claude-mem provides persistent memory across sessions through 9 specialized MCP
search tools. This skill teaches efficient use of these tools through progressive
disclosure, token optimization, and clear decision logic.

**Core Principle**: Find the smallest set of high-signal tokens first (index
format), then drill down to full details only for relevant items.

## Tool Selection Decision Tree

```bash
START: Need historical context?
  ↓
1. Know specific anchor point (observation ID, session ID, timestamp)?
   YES → Use get_context_timeline
   NO → Continue
   ↓
2. Want search + timeline in one step?
   YES → Use get_timeline_by_query (mode: "auto")
   NO → Continue
   ↓
3. Know specific concept tag (discovery, problem-solution, etc.)?
   YES → Use find_by_concept
   NO → Continue
   ↓
4. Know specific file path?
   YES → Use find_by_file
   NO → Continue
   ↓
5. Know specific observation type (decision, bugfix, feature)?
   YES → Use find_by_type
   NO → Continue
   ↓
6. Need recent project context?
   YES → Use get_recent_context
   NO → Continue
   ↓
7. Searching observations (past work)?
   YES → Use search_observations
   NO → Continue
   ↓
8. Searching session summaries?
   YES → Use search_sessions
   NO → Continue
   ↓
9. Searching raw user prompts?
   YES → Use search_user_prompts
   NO → Default to search_observations
```

## Progressive Disclosure Pattern (MANDATORY)

**Always follow this workflow to optimize tokens:**

### Step 1: Start with Index Format

```text
• Use format: "index" (default)
• Set limit: 3-5 (not 20)
• Review titles and dates ONLY
• Token cost: ~50-100 per result
```

### Step 2: Identify Relevant Items

```bash
• Scan index results for relevance
• Note which items need full details
• Discard irrelevant items
```

### Step 3: Request Full Details (Selectively)

```bash
• Use format: "full" ONLY for specific items of interest
• Token cost: ~500-1000 per result
• Load only what you need
```

### Step 4: Refine with Filters (If Needed)

```bash
• Use type, dateRange, concepts, files filters
• Narrow scope before requesting more results
• Use offset for pagination
```

## Token Efficiency Best Practices

**DO:**

- ✅ Start with `limit=3-5` in index format
- ✅ Use filters (type, dateRange, concepts) to narrow results
- ✅ Request full format ONLY for specific relevant items
- ✅ Use `offset` for pagination instead of large limits
- ✅ Leverage metadata (titles, dates) from index results

**DON'T:**

- ❌ Jump straight to full format
- ❌ Request `limit=20` without good reason
- ❌ Load full details for all results
- ❌ Skip index format to "save time"
- ❌ Ignore token warnings

**Token Budget Awareness:**

- Index result: ~50-100 tokens
- Full result: ~500-1000 tokens
- Start with 3-5 items to avoid MCP token limits
- Reduce limit if hitting token errors

## Common Search Patterns

### Pattern 1: Timeline Investigation

**Use case**: "What was happening when we fixed the auth bug?"

**Natural language:**

```text
Show me the timeline around when we fixed the authentication bug
```

**Explicit syntax:**

```text
get_timeline_by_query with query="authentication bug fix" and mode="auto" and depth_before=10 and depth_after=10
```

**Workflow:**

1. Review timeline context (before + after)
2. Load full details for specific relevant observations

### Pattern 2: Concept-Based Research

**Use case**: "Find all problem-solution patterns"

```bash
1. find_by_concept with concept="problem-solution" and limit=5 and format="index"
2. Review titles to identify relevant items
3. Request format="full" for specific observations of interest
```

### Pattern 3: File History

**Use case**: "What work was done on worker-service.ts?"

**Natural language:**

```bash
Find all work done on worker-service.ts
```

**Explicit syntax:**

```text
find_by_file with filePath="worker-service.ts" and format="index"
```

**Workflow:**

1. Scan results for relevant changes
2. Load full details for specific observations
3. Use get_context_timeline if need to understand surrounding context

### Pattern 4: Type-Specific Search

**Use case**: "Show recent decisions about the build system"

```bash
1. search_observations with query="build system" and type="decision" and format="index" and limit=5
2. Review titles and dates
3. Request full format for relevant decisions
```

### Pattern 5: Recent Context Loading

**Use case**: "What happened in recent sessions?"

**Natural language:**

```text
Get recent context to show me what we've been working on
```

**Explicit syntax:**

```text
get_recent_context with limit=3
```

**Workflow:**

1. Review session summaries
2. Use search tools to drill into specific observations if needed

### Pattern 6: User Intent Tracking

**Use case**: "What did the user actually ask for vs what was implemented?"

**Natural language:**

```bash
Search user prompts for authentication feature requests
```

**Explicit syntax:**

```text
search_user_prompts with query="authentication" and format="index" and limit=5
```

**Benefits:**

- See exact user requests (vs what was implemented)
- Detect patterns in repeated requests
- Debug miscommunications between intent and implementation
- Track feature evolution from original ask to final delivery

## Search Composition

Combine tools for powerful workflows:

**Search → Timeline:**

```text
1. search_observations to find relevant observation
2. get_context_timeline with anchor={observation_id} to see surrounding context
```

**Filter → Refine:**

```text
1. search_observations with broad query
2. Add type/concept filters to narrow
3. Use dateRange to focus on specific timeframe
```

**Recent → Deep Dive:**

```bash
1. get_recent_context for overview
2. search_observations for specific topics discovered
3. get_context_timeline for detailed investigation
```

## Available Concepts

Quick reference: discovery, problem-solution, what-changed, how-it-works, pattern, gotcha, change

Use with `find_by_concept` or as filter in `search_observations`.
See [references/mcp-search-tools.md](references/mcp-search-tools.md#4-find_by_concept)
for detailed descriptions.

## Available Observation Types

Quick reference: decision, bugfix, feature, refactor, discovery, change

Use with `find_by_type` or as filter in `search_observations`.
See [references/mcp-search-tools.md](references/mcp-search-tools.md#6-find_by_type)
for detailed descriptions.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Skipping Index Format

```bash
Bad:  search_observations with query="..." and format="full" and limit=20
Good: search_observations with query="..." and format="index" and limit=5
      → Review results → Request full for relevant items only
```

### Anti-Pattern 2: Over-requesting Results

```bash
Bad:  limit=20 without reviewing index first
Good: limit=3-5, review, paginate with offset if needed
```

### Anti-Pattern 3: Ignoring Tool Specialization

```bash
Bad:  search_observations for everything
Good: Use specialized tools (find_by_concept, find_by_file, find_by_type)
```

### Anti-Pattern 4: Loading Full Context Prematurely

```text
Bad:  Request full format before understanding what's relevant
Good: Index first → identify relevant → full details selectively
```

### Anti-Pattern 5: Not Using Timeline Tools

```bash
Bad:  Search for individual observations separately
Good: Use get_context_timeline or get_timeline_by_query for context around events
```

## Search Query Syntax

All search tools support FTS5 full-text search with operators like AND, OR,
NOT, phrase matching, and column-specific search. See
[references/mcp-search-tools.md](references/mcp-search-tools.md#fts5-query-syntax)
for complete syntax reference.

## Advanced Filtering

**Date Ranges:**

```json
dateRange: {start: "2025-10-01", end: "2025-10-31"}
# Or use epoch timestamps:
dateRange: {start: 1729449600, end: 1732128000}
```

**Multiple Types:**

```text
find_by_type with type=["decision", "feature", "refactor"]
```

**Multiple Concepts:**

```text
search_observations with query="database" and concepts=["architecture", "performance"]
```

**File Filtering:**

```text
search_observations with query="refactor" and files="worker-service.ts"
```

## Troubleshooting

### No Results Found

1. **Broaden query**: Start general, then narrow

   ```text
   Good: query="auth"
   Too specific: query="'exact JWT authentication implementation'"
   ```

2. **Remove filters**: Try without type/concept filters first

3. **Check database**: Verify data exists

   ```bash
   sqlite3 ~/.claude-mem/claude-mem.db "SELECT COUNT(*) FROM observations;"
   ```

### Token Limit Errors

1. **Use index format** (not full)
2. **Reduce limit**: Start with limit=3, not 20
3. **Paginate**: Use offset for additional results

   ```text
   # First batch
   search_observations with limit=5 and offset=0
   # Next batch
   search_observations with limit=5 and offset=5
   ```

### Search Too Slow

1. Add date range filters
2. Add type/concept filters
3. Use more specific query terms
4. Reduce result limit

## Quick Reference Table

| Need | Tool | Key Parameters |
|------|------|----------------|
| Recent context | get_recent_context | limit=3-5 |
| Timeline around event | get_context_timeline | anchor, depth_before, depth_after |
| Search + timeline | get_timeline_by_query | query, mode="auto" |
| Find by concept | find_by_concept | concept, format="index", limit=5 |
| Find by file | find_by_file | filePath, format="index" |
| Find by type | find_by_type | type, format="index", limit=5 |
| Search observations | search_observations | query, format="index", limit=5 |
| Search sessions | search_sessions | query, format="index", limit=5 |
| Search user prompts | search_user_prompts | query, format="index", limit=5 |

## Resources

### references/mcp-search-tools.md

Complete reference documentation for all 9 MCP search tools including:

- Detailed parameter descriptions
- Return format specifications
- Citation scheme (`claude-mem://` URIs)
- Advanced FTS5 query syntax

Read this file when needing specific details about tool parameters or query syntax.

## Context Engineering Alignment

This skill implements core context engineering principles:

- **Just-in-time context**: Load data dynamically at runtime
- **Progressive disclosure**: Lightweight identifiers (index) → full details as needed
- **Token efficiency**: Minimal high-signal tokens first, expand selectively
- **Attention budget**: Treat context as finite resource with diminishing returns

Always start with the smallest set of high-signal tokens that maximize likelihood of desired outcome.
