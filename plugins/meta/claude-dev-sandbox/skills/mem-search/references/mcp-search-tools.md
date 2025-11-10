# MCP Search Server - Complete Reference

> **Note**: This is detailed reference documentation. Read only when you need specifics about a particular tool or query syntax. For quick guidance, refer to SKILL.md.

## Table of Contents

- [Tool Catalog](#tool-catalog)
  - [1. search_observations](#1-search_observations)
  - [2. search_sessions](#2-search_sessions)
  - [3. search_user_prompts](#3-search_user_prompts)
  - [4. find_by_concept](#4-find_by_concept)
  - [5. find_by_file](#5-find_by_file)
  - [6. find_by_type](#6-find_by_type)
  - [7. get_recent_context](#7-get_recent_context)
  - [8. get_context_timeline](#8-get_context_timeline)
  - [9. get_timeline_by_query](#9-get_timeline_by_query)
- [Output Formats](#output-formats)
- [FTS5 Query Syntax](#fts5-query-syntax)
- [Citation Scheme](#citation-scheme)

## Tool Catalog

### 1. search_observations

Full-text search across observation titles, narratives, facts, and concepts.

**Parameters**:

- `query` (required): Search query for FTS5 full-text search
- `type`: Filter by observation type(s) (decision, bugfix, feature, refactor, discovery, change)
- `concepts`: Filter by concept tags
- `files`: Filter by file paths (partial match)
- `project`: Filter by project name
- `dateRange`: Filter by date range (`{start, end}`)
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" for titles/dates only, "full" for complete details)

### 2. search_sessions

Full-text search across session summaries, requests, and learnings.

**Parameters**:

- `query` (required): Search query for FTS5 full-text search
- `project`: Filter by project name
- `dateRange`: Filter by date range
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" or "full")

### 3. search_user_prompts

Search raw user prompts with full-text search. Use this to find what the user
actually said/requested across all sessions.

**Parameters**:

- `query` (required): Search query for FTS5 full-text search
- `project`: Filter by project name
- `dateRange`: Filter by date range
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" for truncated prompts/dates, "full" for complete prompt text)

### 4. find_by_concept

Find observations tagged with specific concepts.

**Available Concepts**: discovery, problem-solution, what-changed, how-it-works, pattern, gotcha, change

**Parameters**:

- `concept` (required): Concept tag to search for
- `project`: Filter by project name
- `dateRange`: Filter by date range
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" or "full")

### 5. find_by_file

Find observations and sessions that reference specific file paths.

**Parameters**:

- `filePath` (required): File path to search for (supports partial matching)
- `project`: Filter by project name
- `dateRange`: Filter by date range
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" or "full")

### 6. find_by_type

Find observations by type (decision, bugfix, feature, refactor, discovery, change).

**Parameters**:

- `type` (required): Observation type(s) to filter by (single type or array)
- `project`: Filter by project name
- `dateRange`: Filter by date range
- `orderBy`: Sort order (relevance, date_desc, date_asc)
- `limit`: Maximum results (default: 20, max: 100)
- `offset`: Number of results to skip
- `format`: Output format ("index" or "full")

### 7. get_recent_context

Get recent session context including summaries and observations for a project.

**Parameters**:

- `project`: Project name (defaults to current working directory basename)
- `limit`: Number of recent sessions to retrieve (default: 3, max: 10)

### 8. get_context_timeline

Get a unified timeline of context (observations, sessions, and prompts) around a specific point in time.

**Parameters**:

- `anchor` (required): Anchor point - observation ID, session ID (e.g., "S123"), or ISO timestamp
- `depth_before` (default: 10): Number of records to retrieve before anchor (max: 50)
- `depth_after` (default: 10): Number of records to retrieve after anchor (max: 50)
- `project`: Filter by project name

**Returns**: `depth_before` records + anchor + `depth_after` records, all interleaved chronologically.

**Use Case**: Understanding "what was happening when X occurred"

### 9. get_timeline_by_query

Search for observations using natural language and get timeline context around the best match.

**Parameters**:

- `query` (required): Natural language search query to find relevant observations
- `mode` (default: "auto"): Operation mode
  - `"auto"`: Automatically use top search result as timeline anchor
  - `"interactive"`: Return top N search results for manual anchor selection
- `depth_before` (default: 10): Number of timeline records before anchor (max: 50)
- `depth_after` (default: 10): Number of timeline records after anchor (max: 50)
- `limit` (default: 5): For interactive mode - number of top search results to display (max: 20)
- `project`: Filter by project name

**Use Case**: Faster context discovery - "show me what happened around when we fixed the authentication bug"

## Output Formats

### Index Format (Default)

Returns titles, dates, and source URIs only. Uses ~10x fewer tokens than full format.

**Token cost**: ~50-100 tokens per result

### Full Format

Returns complete observation/summary details including narrative, facts, concepts, files, etc.

**Token cost**: ~500-1000 tokens per result

## FTS5 Query Syntax

The `query` parameter supports SQLite FTS5 full-text search syntax:

- **Simple**: `"error handling"`
- **AND**: `"error" AND "handling"`
- **OR**: `"bug" OR "fix"`
- **NOT**: `"bug" NOT "feature"`
- **Phrase**: `"'exact phrase'"`
- **Column**: `title:"authentication"`

## Citation Scheme

All search results use the `claude-mem://` URI scheme:

- `claude-mem://observation/{id}` - References specific observations
- `claude-mem://session/{id}` - References specific sessions
- `claude-mem://user-prompt/{id}` - References specific user prompts
