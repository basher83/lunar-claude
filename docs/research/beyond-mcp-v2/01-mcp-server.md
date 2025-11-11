# MCP Server Approach Analysis

## 1. Discoverability Assessment

- **Mechanism:** Tool descriptions are injected into Claude's context on every session start via MCP protocol. FastMCP's `@mcp.tool()` decorator automatically exposes each function as a tool with its docstring as the description.

- **Visibility:** All 13 MCP tools are immediately visible to Claude at session initialization. The server declares itself with: `"Access Kalshi prediction market data including markets, events, series, trades, and more. All data is read-only and requires no authentication."` Each individual tool includes a detailed docstring explaining parameters and return values.

- **Trigger pattern:** Claude autonomously decides when to invoke tools based on:
  1. Server-level instructions in FastMCP initialization
  2. Tool names (e.g., `get_exchange_status`, `search_markets`, `list_events`)
  3. Docstring descriptions loaded into context

  Example from README shows natural language triggers auto-invocation:
  ```text
  "What's the current Kalshi exchange status?"
  → Calls get_exchange_status()

  "Show me 5 open markets about Bitcoin"
  → Calls search_markets(keyword="Bitcoin", limit=5)
  ```

- **Evidence of proactive usage:**
  - README explicitly shows questions that trigger automatic tool calls
  - Comparison table in main README states: **"Agent Invoked: Yes"** for MCP approach
  - Tools designed with semantic names that match natural language queries
  - No slash commands or explicit invocation syntax required - just conversational queries

## 2. Token Cost Analysis

- **Startup cost:** ~3,250-4,500 tokens (estimated)
  - Server instructions: ~50 tokens
  - 13 tool definitions with docstrings: 250-350 tokens each
  - Total: 13 × 300 (avg) = ~3,900 tokens + overhead

- **Per-operation cost:** Minimal - just the tool call JSON and response
  - Tool invocation: ~50-100 tokens
  - Response parsing: Varies by data size

- **Total overhead:** **HIGH on initialization, LOW per operation**
  - Every session pays the ~4,000 token startup cost upfront
  - Main README explicitly calls this out: "MCP Servers come with a massive cost - **instant context loss**"

- **Scaling:** Linear with number of tools
  - Beyond-MCP evolved from 15 tools to 13 tools
  - Each additional tool adds ~250-350 tokens
  - At scale (50-100 tools), this becomes prohibitive

## 3. Architecture Pattern

- **Implementation:**
  - FastMCP server wraps a CLI via subprocess
  - Each `@mcp.tool()` decorated function builds a command like: `uv run kalshi <command> --json`
  - Executes via `subprocess.run()` in the CLI directory
  - Parses JSON stdout and returns structured data
  - Error handling via try/except for subprocess failures and JSON parsing

- **Integration:** Two-layer delegation pattern
  ```text
  Claude → MCP Protocol → FastMCP Server → subprocess → CLI → HTTP API
  ```

  - MCP server intentionally **does not** make direct HTTP calls
  - CLI is the "single source of truth" for API logic
  - MCP provides the standardized protocol layer

- **Strengths:**
  1. **Automatic discoverability** - Tools appear instantly to Claude without manual priming
  2. **Standardized protocol** - Works with any MCP-compatible client (Claude Desktop, CLI, etc.)
  3. **Clean separation** - Server layer doesn't duplicate API logic
  4. **Type safety** - FastMCP validates parameters against function signatures
  5. **Semantic naming** - Tool names naturally trigger from conversational queries

- **Weaknesses:**
  1. **High token startup cost** - ~4,000 tokens per session for 13 tools
  2. **Stateless** - Each tool call loses conversational context (main README's "instant context loss")
  3. **Subprocess overhead** - Extra process spawn for every operation
  4. **Not customizable** - Unless you own/fork the server, you can't modify behavior
  5. **Scales poorly** - Adding more tools linearly increases token cost

## 4. Lessons for claude-mem

**Discoverability techniques to preserve:**

- **Semantic naming convention** - Tool names that match natural language queries (e.g., `search_observations`, `find_by_concept`)
- **Clear descriptions** - Server-level instructions that explain when to use the tool ("Access Kalshi prediction market data...")
- **Comprehensive docstrings** - Each tool's purpose, parameters, and return values clearly documented
- **Natural language examples** - Show example queries that trigger the tool (like "Show me 5 open markets about Bitcoin")
- **Category grouping** - Tools organized by domain (Exchange, Markets, Events, Series) helps Claude understand scope

**What NOT to adopt:**

- **Reason 1: Token overhead** - MCP's ~4,000 token startup cost for 13 tools is exactly what claude-mem v5.4.0 eliminated (saved 2,250 tokens by removing 9 MCP tools). Beyond-MCP's main thesis confirms: "MCP Servers come with a massive cost - instant context loss."

- **Reason 2: Statelessness** - MCP's protocol requires each tool call to be independent, losing conversation context. Skills maintain session continuity.

- **Reason 3: Wrapper complexity** - The subprocess→CLI→API delegation adds latency and failure points. Direct implementation is simpler.

- **Reason 4: Poor scaling** - Linear token growth per tool. claude-mem needs efficient access to many search capabilities (observations, sessions, files, concepts, timelines).

## 5. Agent Autonomy Assessment

**Auto-invoked:** ✅ Yes

**Why:**
1. README explicitly demonstrates conversational queries triggering tool calls without slash commands or manual invocation
2. Comparison table states "Agent Invoked: Yes" for MCP approach
3. Tool descriptions loaded into context enable Claude to match user queries to appropriate tools
4. FastMCP framework exposes all tools at session start, making them immediately available for autonomous invocation
5. Example patterns show semantic matching: "What's the current..." → `get_exchange_status()`, "Show me...about Bitcoin" → `search_markets(keyword="Bitcoin")`

**Confidence:** **High**

Evidence is explicit and multi-sourced:
- Direct quotes from main README about agent invocation
- Working example prompts showing auto-triggering
- Architecture designed for autonomous discovery
- Comparison against CLI/Scripts approaches which are "Agent Invoked: No"
