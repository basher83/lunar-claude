# MCP Server Approach Analysis

## 1. Discoverability Assessment

### Mechanism: Protocol-Level Tool Advertisement

When Claude connects to an MCP server, the server **advertises all available tools upfront** via JSON-RPC 2.0 protocol:

1. **Connection Handshake**: Claude Desktop connects to MCP server via stdio transport
2. **Tool Metadata Exchange**: Server sends complete tool catalog including:
   - Tool name and description
   - Parameter names, types, and descriptions
   - Return value specifications
   - Docstrings and documentation

**Example from server.py:**
```python
@mcp.tool()
def list_markets(
    limit: int = 10,
    status: str = "open",
    event_ticker: Optional[str] = None,
    series_ticker: Optional[str] = None,
    ...
) -> dict:
    """
    List Kalshi markets with various filters.

    Args:
        limit: Number of markets to return (1-1000, default: 10)
        status: Market status filter - 'open', 'closed', 'settled', or comma-separated
        ...
    """
```

### Visibility: Always-On System Prompt Injection

**MCP tools are injected into Claude's system prompt on EVERY message**, making them:
- ✅ **Visible**: Claude sees all 15 tools in every conversation turn
- ✅ **Structured**: Tool definitions include full type information
- ✅ **Searchable**: Claude can semantically match user intent to tool capabilities

### Trigger Pattern: Semantic Intent Matching

Claude auto-invokes MCP tools through:
1. **Semantic Analysis**: Compares user query meaning against tool descriptions
2. **Confidence Evaluation**: Determines if a tool will help answer the query
3. **Parameter Extraction**: Identifies relevant information to use as parameters
4. **Autonomous Execution**: Calls tool without explicit user instruction

**Evidence from README:**
```
"Show me 5 open markets about Bitcoin"
→ Calls search_markets(keyword="Bitcoin", limit=5)

"What's the current Kalshi exchange status?"
→ Calls get_exchange_status()
```

### Evidence of Proactive Usage: High

**From README.md Trade-off Comparison Table:**
- **"Agent Invoked"**: ✅ Yes
- **Description**: "MCP & Skills are automatically triggered by Claude based on context"
- **Contrast**: CLI & Scripts require "explicit agent decision to use"

The README explicitly confirms MCP tools are **autonomously invoked** without user prompting.

## 2. Token Cost Analysis

### Startup Cost: ~3,750 tokens (estimated)

**Per Tool Overhead:**
- Tool name: ~5 tokens
- Description: ~30-50 tokens
- Parameters (7 avg): ~100-150 tokens
- Docstring/types: ~50-80 tokens
- **Total per tool: ~200-250 tokens**

**For 15 MCP Tools:**
- 15 × 250 tokens = **3,750 tokens**

**Comparison to claude-mem:**
- Previous MCP: 9 tools × 250 tokens = 2,500 tokens
- Current Skills: ~250 tokens
- **Savings: 2,250 tokens per session**

### Per-Operation Cost: Tool Call + Response

**Each tool invocation:**
1. **Request**: ~50-100 tokens (tool name + parameters)
2. **Response**: Variable (100-5000+ tokens depending on data)
3. **Context Loss**: Conversational context NOT preserved across calls

**Key insight from README:**
> "MCP Servers come with a massive cost - **instant context loss**."

### Total Overhead Assessment: SIGNIFICANT

**Scaling characteristics:**
- **Linear growth**: Each additional tool adds ~250 tokens
- **Always loaded**: All tools present in every message
- **No progressive disclosure**: Can't defer loading until needed
- **Context window pressure**: 3,750 tokens is ~5% of an 80k context window

**From README Trade-off Table:**
- **Context Window Consumption**: High
- **Note**: "MCP & CLI consume full context on every tool call"

## 3. Architecture Pattern

### Implementation: CLI Wrapper via Subprocess

**From server.py:**
```python
def run_kalshi_cli(*args) -> dict:
    """Execute kalshi CLI command and return parsed JSON output."""
    cmd = ["uv", "run", "kalshi", *args, "--json"]
    result = subprocess.run(
        cmd,
        cwd=CLI_PATH,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)
```

**Tool Structure:**
```python
@mcp.tool()
def get_exchange_status() -> dict:
    """Get the current Kalshi exchange status."""
    return run_kalshi_cli("status")
```

### Integration: Layered Delegation

**Architecture Flow:**
```
Claude/LLM → MCP Protocol → FastMCP Server → subprocess → CLI → HTTP → Kalshi API
```

**Key characteristics:**
1. **One-to-One Mapping**: Each MCP tool = one CLI command
2. **No Direct HTTP**: Server delegates ALL API logic to CLI
3. **Stateless**: Each tool call is independent
4. **JSON Transport**: Structured data throughout

### Strengths: What It Does Well

1. **✅ Standardized Protocol**
   - Works with any MCP-compatible client (Claude Desktop, Claude Code, etc.)
   - No custom integration needed

2. **✅ Automatic Discovery**
   - Tools appear immediately upon connection
   - No manual registration or priming needed

3. **✅ Clean Separation**
   - MCP server focuses on protocol
   - CLI handles API logic
   - Single source of truth

4. **✅ Type Safety**
   - Python type hints → MCP schema
   - Parameter validation built-in

5. **✅ Autonomous Invocation**
   - Claude decides WHEN to use tools
   - Natural language → tool calls

### Weaknesses: Limitations

1. **❌ Instant Context Loss** (Major)
   - Every tool call loses conversational context
   - Can't reference previous messages
   - Requires re-stating context

2. **❌ Always-On Token Cost**
   - All 15 tools loaded in every message
   - 3,750 tokens regardless of usage
   - Can't defer or lazy-load

3. **❌ Subprocess Overhead**
   - Wraps CLI via subprocess
   - Extra process spawning latency
   - JSON serialization overhead

4. **❌ Not Customizable**
   - External MCP servers are black boxes
   - Can't modify unless you own/fork
   - Locked into server's decisions

5. **❌ Poor Portability**
   - Requires MCP client setup
   - Desktop app configuration
   - Not git-committable

## 4. Lessons for claude-mem

### Discoverability Techniques to Preserve:

1. **✅ Rich Descriptions**
   - Skills should have detailed `description:` fields
   - Explain WHEN to use, not just WHAT it does
   - Include trigger keywords

2. **✅ Semantic Intent Matching**
   - Write descriptions that match user language
   - Example: "Access Kalshi prediction market data... Use when the user asks about prediction markets, Kalshi markets, betting odds..."

3. **✅ Parameter Clarity**
   - Document what inputs are needed
   - Provide examples in instructions
   - Use `--help` flags for discovery

4. **✅ Progressive Instructions**
   - Don't front-load all information
   - Point to `--help` or `--json` flags
   - "Only load script you need - no unnecessary context"

### What NOT to Adopt:

1. **❌ Always-On Tool Loading**
   - **Reason**: 3,750 token overhead for 15 tools
   - **Better**: Skills load on-demand (250 tokens)
   - **Evidence**: claude-mem v5.4.0 saved 2,250 tokens by removing MCP

2. **❌ Protocol-Level Advertisement**
   - **Reason**: All tools visible always = context bloat
   - **Better**: Skill descriptions in marketplace = selective loading
   - **Evidence**: README confirms "MCP consume full context on every tool call"

3. **❌ Subprocess Wrapping**
   - **Reason**: Extra latency and complexity
   - **Better**: Direct execution or bash commands
   - **Note**: Only needed if separating concerns

4. **❌ Stateless Tool Calls**
   - **Reason**: "Instant context loss" = poor UX
   - **Better**: Skills maintain conversational context
   - **Evidence**: README calls this "a massive cost"

## 5. Agent Autonomy Assessment

### Auto-invoked: ✅ Yes

**Confidence: HIGH**

**Evidence:**

1. **Explicit Confirmation in README:**
   > "**Agent Invoked**: Yes"
   > "MCP & Skills are automatically triggered by Claude based on context"

2. **Usage Examples Show Zero Prompting:**
   ```
   "What's the current Kalshi exchange status?"
   → Calls get_exchange_status()

   "Show me 5 open markets about Bitcoin"
   → Calls search_markets(keyword="Bitcoin", limit=5)
   ```

   No `/` commands, no explicit tool invocation syntax needed.

3. **Contrasted with Non-Autonomous Approaches:**
   > "CLI & Scripts require explicit agent decision to use"

4. **Protocol Design:**
   - Tools injected into system prompt
   - Claude performs semantic intent matching
   - Autonomous parameter extraction and invocation

### Why: Protocol-Level Integration + Semantic Matching

**MCP is auto-invoked because:**

1. **System Prompt Injection**: All tools visible in every conversation turn
2. **Semantic Descriptions**: Rich documentation enables intent matching
3. **Type Information**: Claude knows what parameters are needed
4. **Client Support**: Claude Desktop/Code have built-in MCP support

**Key architectural difference from Skills:**
- MCP: Protocol-level (client handles tool exposure)
- Skills: File-level (agent must discover via marketplace)

## 6. Critical Insight: Discoverability vs Token Cost Trade-off

**MCP achieves autonomous invocation through:**
- ✅ Always-on visibility (system prompt injection)
- ✅ Rich semantic descriptions
- ✅ Protocol standardization

**But pays the price of:**
- ❌ 3,750 tokens per session (15 tools)
- ❌ Instant context loss per call
- ❌ No progressive disclosure

**Skills can preserve autonomy while reducing cost by:**
1. **Selective Loading**: Only load skill when description matches
2. **Rich Descriptions**: Mirror MCP's semantic clarity
3. **Progressive Disclosure**: Load instructions → scripts → data
4. **Context Preservation**: Maintain conversation state

**The claude-mem decision to remove MCP was correct:**
- Reduced startup cost from 2,500 → 250 tokens (90% savings)
- Maintained discoverability through skill descriptions
- Preserved conversational context

**Key lesson:** Autonomy comes from **semantic richness + visibility**, not protocol. Skills can achieve both with lower token cost through deferred loading.
