# Claude-Mem MCP Tools: Comprehensive Usage Guide

**For:** Future Claude Code sessions
**Purpose:** Effective use of claude-mem search tools based on hands-on exploration
**Date:** 2025-11-05

---

## Executive Summary

Claude-mem provides 7 MCP search tools for querying project history. This guide documents effective usage patterns, common mistakes, and architectural insights discovered through systematic testing.

**Key Takeaway:** Start broad with index format, use predefined taxonomies, understand the progressive disclosure philosophy.

---

## Quick Reference

### The 7 Search Tools

| Tool | Best For | Token Cost |
|------|----------|------------|
| `search_observations` | Full-text search across all observations | 50-100 (index), 500-1000 (full) |
| `search_sessions` | Search high-level session summaries | 50-100 (index), 500-1000 (full) |
| `search_user_prompts` | Find what user actually said/requested | 50-100 (index), 500-1000 (full) |
| `find_by_file` | Everything related to specific files | 50-100 (index), 500-1000 (full) |
| `find_by_type` | Filter by observation type | 50-100 (index), 500-1000 (full) |
| `find_by_concept` | Filter by concept taxonomy | 50-100 (index), 500-1000 (full) |
| `get_recent_context` | Auto-loaded at session start | Variable (3-10 sessions) |

---

## Critical Knowledge: Taxonomies

### Valid Observation Types (6 total)

These are the **ONLY** valid types:

```text
✅ bugfix     - Something was broken, now fixed
✅ feature    - New capability added
✅ refactor   - Code restructured, behavior unchanged
✅ change     - Generic modification (docs, config, misc)
✅ discovery  - Learning about existing system
✅ decision   - Architectural/design choice with rationale
```

**Common Mistake:** Using "gotcha" as a type (it's a concept, not a type!)

### Valid Concepts (7 total)

These are the **ONLY** valid concepts:

```text
✅ how-it-works      - Understanding mechanisms
✅ why-it-exists     - Purpose or rationale
✅ what-changed      - Modifications made
✅ problem-solution  - Issues and their fixes
✅ gotcha            - Traps or edge cases
✅ pattern           - Reusable approach
✅ trade-off         - Pros/cons of a decision
```

**Common Mistake:** Searching for "documentation", "architecture", "testing" as concepts (not in taxonomy!)

---

## Search Strategy: The Right Way

### 1. Always Start with Index Format

```text
❌ BAD:  search_observations with query="authentication" and format="full"
✅ GOOD: search_observations with query="authentication" and format="index"
```

**Why:** Index format uses ~10x fewer tokens. See what exists, then fetch details selectively.

### 2. Start Broad, Then Narrow

```text
❌ BAD:  search_observations with query="broken file reference"
✅ GOOD: search_observations with query="file reference"
✅ BETTER: search_observations with query="file" and type="decision"
```

**Why:** Search is literal FTS5 text matching, not semantic. Exact phrases often fail.

### 3. Use Filters to Narrow Results

```bash
# Broad search first
search_observations with query="authentication" and format="index"

# Review results, then narrow
search_observations with query="authentication" and type="decision" and format="index"

# Fetch full details on specific results
search_observations with query="JWT authentication" and format="full" and limit=1
```

### 4. Use the Right Tool for the Job

**File-specific questions:**
```text
find_by_file with filePath="SKILL.md"  # Fast and accurate
```

**Type-specific questions:**
```text
find_by_type with type="decision"  # Shows all architectural decisions
find_by_type with type=["decision", "feature"]  # Multiple types
```

**User intent tracing:**
```bash
search_user_prompts with query="audit"  # What did user actually ask for?
```

---

## Common Mistakes and Fixes

### Mistake 1: Using Invalid Concepts

```text
❌ find_by_concept with concept="documentation"
❌ find_by_concept with concept="architecture"
❌ find_by_concept with concept="testing"
```

**Fix:** Use valid concepts from the 7-item taxonomy:
```text
✅ find_by_concept with concept="problem-solution"
✅ find_by_concept with concept="trade-off"
✅ find_by_concept with concept="gotcha"
```

### Mistake 2: Using "gotcha" as Type

```text
❌ find_by_type with type="gotcha"
```

**Fix:** "gotcha" is a concept, not a type:
```text
✅ find_by_concept with concept="gotcha"
```

### Mistake 3: Overly Specific Queries

```text
❌ search_observations with query="'exact JWT authentication implementation with RS256'"
```

**Fix:** Start broad, use filters:
```text
✅ search_observations with query="JWT authentication" and type="feature"
```

### Mistake 4: Fetching Full Format First

```text
❌ search_observations with query="build" and format="full" and limit=20
   # Uses 10,000-20,000 tokens!
```

**Fix:** Index first, full later:
```bash
✅ search_observations with query="build" and format="index" and limit=20
   # Uses 1,000-2,000 tokens
   # Review results, then fetch specific items in full format
```

### Mistake 5: Large Limits Without Review

```text
❌ search_observations with query="test" and limit=50
   # May exceed MCP token limits
```

**Fix:** Start small, paginate:
```bash
✅ search_observations with query="test" and limit=5
   # Then use offset for pagination if needed
```

---

## Advanced Techniques

### FTS5 Query Syntax

Claude-mem uses SQLite FTS5 for search. Supports boolean operators:

```text
# AND operator (both required)
search_observations with query="error AND handling"

# OR operator (either term)
search_observations with query="bug OR fix"

# NOT operator (exclude term)
search_observations with query="bug NOT feature"

# Phrase search (exact match)
search_observations with query="'exact phrase'"

# Column-specific search
search_observations with query="title:authentication"
search_observations with query="narrative:bug fix"
```

### Date Range Filtering

```json
search_observations with query="deployment" and dateRange={
  "start": "2025-10-01",
  "end": "2025-10-31"
}
```

### Multiple Filters

```text
search_observations with query="authentication"
  and type="decision"
  and concepts=["problem-solution", "trade-off"]
  and dateRange={"start": "2025-10-20", "end": "2025-11-05"}
```

### Pagination

```text
# Page 1
search_observations with query="refactor" and limit=10 and offset=0

# Page 2
search_observations with query="refactor" and limit=10 and offset=10

# Page 3
search_observations with query="refactor" and limit=10 and offset=20
```

---

## Progressive Disclosure Philosophy

Claude-mem implements a 3-layer architecture mirroring human memory:

### Layer 1: Index (What Exists)

**Automatically injected at session start**

```text
Found 10 observation(s) matching "skill audit":

1. [change] Audit Log Development Tasks Completed
   Date: 11/5/2025, 3:09:05 AM
   Source: claude-mem://observation/675

2. [bugfix] Multi-Agent Composition Skill Achieved 100% Compliance
   Date: 11/5/2025, 3:15:20 AM
   Source: claude-mem://observation/679
```

**Token Cost:** ~50-100 tokens per result
**Purpose:** Know what's available without details
**Includes:** Token counts for informed fetch decisions

### Layer 2: Full Details (On-Demand)

**Fetched via MCP when needed**

```text
## Multi-Agent Composition Skill Achieved 100% Compliance
*Source: claude-mem://observation/679*

**Fixed critical naming violation by renaming skill from composing-claude-code to multi-agent-composition.**

---
Type: bugfix | Facts: Skill renamed to avoid reserved word...;
Re-audit showed 100% compliance...; All critical issues resolved...
Concepts: problem-solution, what-changed
---
```

**Token Cost:** ~500-1000 tokens per result
**Purpose:** Full context with rich metadata
**Includes:** Facts, narrative, concepts, files

### Layer 3: Perfect Recall (Source Code)

**Read actual files when needed**

```text
Read /path/to/SKILL.md
```

**Token Cost:** Varies by file size
**Purpose:** Ground truth, perfect recall
**When:** Need exact code/configuration

### Why This Works

1. **Token Efficiency:** Index format prevents context overflow
2. **Smart Decisions:** Token counts help Claude choose layer 2 vs layer 3
3. **Human-Like:** Mirrors how humans remember (vague → specific → perfect recall)
4. **Visual Cues:** Type indicators (🔴 gotcha, 🟤 decision, 🔵 discovery) for priority scanning

---

## Practical Workflows

### Workflow 1: Debugging an Issue

```bash
# Step 1: Search for related problems
search_observations with query="error database" and type="bugfix" and format="index"

# Step 2: Review index, identify relevant observations

# Step 3: Fetch full details on 1-2 most relevant
search_observations with query="database connection error" and format="full" and limit=1

# Step 4: If needed, read actual source files
Read /path/to/file/mentioned/in/observation
```

### Workflow 2: Understanding Past Decisions

```bash
# Step 1: Find all architectural decisions
find_by_type with type="decision" and format="index"

# Step 2: Search for specific decision
search_observations with query="authentication strategy" and type="decision" and format="full"

# Step 3: Check related concepts
find_by_concept with concept="trade-off" and format="index"
```

### Workflow 3: File Archaeology

```text
# Step 1: Find all work on a file
find_by_file with filePath="worker-service.ts" and format="index"

# Step 2: Review timeline of changes

# Step 3: Fetch details on significant changes
search_observations with query="worker service" and type=["refactor", "feature"] and format="full"
```

### Workflow 4: Feature History Tracing

```bash
# Step 1: What did user originally ask for?
search_user_prompts with query="authentication feature" and format="index"

# Step 2: What was implemented?
search_sessions with query="authentication" and format="index"

# Step 3: What specific changes were made?
search_observations with query="authentication" and type="feature" and format="full"
```

### Workflow 5: Context Recovery After Time Away

```bash
# Step 1: Get recent context (auto-loaded, but can request more)
get_recent_context with limit=5

# Step 2: Search for specific project work
search_sessions with query="[PROJECT NAME]" and orderBy="date_desc" and format="index"

# Step 3: Review key decisions made
find_by_type with type="decision" and limit=10 and format="index"
```

---

## Token Management

### Token Estimates by Format

| Format | Tokens Per Result | 20 Results Total |
|--------|-------------------|------------------|
| Index  | 50-100           | 1,000-2,000      |
| Full   | 500-1000         | 10,000-20,000    |

### Token Efficiency Tips

1. **Start with index:** Always use `format="index"` first
2. **Small limits:** Start with 3-5 results, not 20
3. **Apply filters early:** Narrow before searching, not after
4. **Paginate:** Use `offset` to browse in batches
5. **Be selective:** Only fetch full format for truly relevant items

### Avoiding MCP Token Limits

```bash
# ❌ This may hit limits:
search_observations with query="test" and format="full" and limit=20

# ✅ This won't:
search_observations with query="test" and format="index" and limit=20
# Review, then:
search_observations with query="specific test case" and format="full" and limit=3
```

---

## Architecture Insights

### How Claude-Mem Works

```bash
Session Start → Inject last 10 sessions' context (Layer 1)
     ↓
User Prompts → Save prompts to database
     ↓
Tool Executions → Capture Read/Write/Edit operations
     ↓
Worker Service → Claude Agent SDK processes observations
     ↓              (port 37777, managed by PM2)
     ↓
Observations Extracted → Structured XML with types/concepts/facts
     ↓
Session End → Generate summary, ready for next session
```

### What Gets Observed

**Captured:**
- Tool executions (Read, Write, Edit, Bash, etc.)
- User prompts (raw text)
- Session outcomes (what was built/fixed/deployed)

**Not Captured:**
- Claude's internal reasoning
- Routine operations (ls, package installs with no errors)
- Empty status checks

### How Concepts Are Tagged

Concepts are **not automatically extracted** - they're explicitly tagged by the Claude Agent SDK worker using the 7-keyword taxonomy defined in `src/sdk/prompts.ts`:

```typescript
// The agent is instructed to use ONLY these concepts:
- how-it-works
- why-it-exists
- what-changed
- problem-solution
- gotcha
- pattern
- trade-off
```

This explains why arbitrary concepts like "documentation" don't exist - they're not in the taxonomy!

---

## Troubleshooting

### No Results Found

**Problem:** Search returns zero results

**Diagnosis:**
```bash
# Check database has data
sqlite3 ~/.claude-mem/claude-mem.db "SELECT COUNT(*) FROM observations;"
```

**Fixes:**
1. **Query too specific:** Try broader terms
   ```text
   ❌ "broken file reference with incorrect path"
   ✅ "file reference"
   ```

2. **Wrong filters:** Remove filters and try again
   ```text
   # Start broad
   search_observations with query="auth"

   # Then add filters
   search_observations with query="auth" and type="decision"
   ```

3. **Invalid concept/type:** Check against valid taxonomies
   ```text
   ❌ find_by_concept with concept="documentation"
   ✅ find_by_concept with concept="problem-solution"
   ```

### Token Limit Errors

**Problem:** "Response exceeds token limit"

**Fixes:**
1. Use index format: `format="index"`
2. Reduce limit: `limit=3` instead of `limit=20`
3. Paginate: Use `offset` to browse
4. Add filters: Narrow before fetching

### Search Too Slow

**Problem:** Queries take too long

**Fixes:**
1. More specific queries (fewer results to process)
2. Date range filters (limit time window)
3. Type/concept filters (narrow scope)
4. Smaller result limits

---

## Best Practices Summary

### DO ✅

- **Start with index format** for overview
- **Use small limits** (3-5) initially
- **Search broadly** first, then narrow
- **Use valid types** from the 6-type taxonomy
- **Use valid concepts** from the 7-concept taxonomy
- **Filter early** to reduce result sets
- **Fetch full selectively** only for relevant items
- **Use find_by_file** for file-specific questions
- **Use search_user_prompts** to trace original intent
- **Paginate** with offset for large result sets

### DON'T ❌

- **Don't start with full format** (wastes tokens)
- **Don't use large limits** (20+) without reviewing index
- **Don't search for invalid concepts** (documentation, architecture, testing)
- **Don't use gotcha as a type** (it's a concept!)
- **Don't use overly specific queries** (exact phrases often fail)
- **Don't ignore the taxonomies** (6 types, 7 concepts - these are fixed!)
- **Don't fetch everything at once** (progressive disclosure exists for a reason)

---

## Real-World Examples

### Example 1: Understanding Skill Audit Results

```text
# What I tried first (worked well):
search_observations with query="skill audit" and format="index"

# Found 10 results immediately, reviewed titles

# Fetched details on most relevant:
search_observations with query="skill audit" and format="full" and limit=1

# Result: Found audit completion observation with all details
```

### Example 2: File History Investigation

```text
# What I tried (worked perfectly):
find_by_file with filePath="SKILL.md" and format="index"

# Found 10 results showing timeline of SKILL.md changes

# Result: Clear history of skill development and audits
```

### Example 3: Searching for Concepts (Failed First)

```bash
# What I tried first (failed):
find_by_concept with concept="documentation"
# Result: No observations found

# Why it failed: "documentation" not in 7-concept taxonomy

# What worked:
find_by_concept with concept="problem-solution"
# Result: No results (but that's because observations aren't tagged with this)
```

### Example 4: Understanding User Intent

```text
# What I tried (very useful):
search_user_prompts with query="audit" and format="index"

# Found exact user requests:
# - "lets have @claude-skill-auditor audit plugins/..."
# - "log results to docs/reviews/skill-audit-log.md"

# Result: Clear trace from user request to implementation
```

---

## Key Architectural Decisions

### Why Fixed Taxonomies?

**Design Choice:** 6 types, 7 concepts - fixed, not dynamic

**Benefits:**
- Predictable search results
- Consistent categorization
- Efficient indexing
- Clear semantics

**Trade-off:** Can't tag arbitrary concepts, but ensures consistency

### Why Literal Search (Not Semantic)?

**Design Choice:** SQLite FTS5 full-text search

**Benefits:**
- Fast and efficient
- Predictable results
- No ML/embedding overhead
- Works offline

**Trade-off:** Must search for actual terms used, not similar concepts

### Why Progressive Disclosure?

**Design Choice:** 3-layer architecture (index → full → source)

**Benefits:**
- Token efficiency (10x difference)
- Informed fetch decisions
- Scales to large histories
- Human-like memory pattern

**Trade-off:** Requires two-step process (index → full), but worth it

---

## Future Claude Sessions: Quick Start

If you're a future Claude Code session reading this:

1. **Always start with index format:** `format="index"`
2. **Check valid taxonomies:** 6 types, 7 concepts (see above)
3. **Start broad:** "auth" not "JWT RS256 implementation"
4. **Use filters to narrow:** `type="decision"` after broad search
5. **Fetch selectively:** Only use `format="full"` on relevant items
6. **Use specialized tools:** `find_by_file`, `find_by_type`, `search_user_prompts`
7. **Remember token costs:** Index = 50-100, Full = 500-1000 per result

**Most Common Mistake:** Searching for concepts that don't exist in the taxonomy. Always check against the valid 7 concepts first!

---

## References

- **Source Code:** `/Users/basher8383/.claude/plugins/marketplaces/thedotmack/`
- **Documentation:** `~/.claude/plugins/marketplaces/thedotmack/docs/`
- **Key Files:**
  - `src/sdk/prompts.ts` - Defines taxonomies and extraction prompts
  - `src/services/sqlite/SessionSearch.ts` - Search implementation
  - `src/servers/search-server.ts` - MCP server
  - `docs/usage/search-tools.mdx` - User guide
  - `docs/architecture/mcp-search.mdx` - Technical details

---

**Document Created:** 2025-11-05
**Created By:** Claude Code session exploring claude-mem
**Purpose:** Help future sessions use claude-mem effectively
**Status:** Comprehensive guide based on hands-on testing
