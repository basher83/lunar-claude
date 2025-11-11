# CLI Approach Analysis

## 1. Agent Autonomy Assessment

**Auto-invoked:** ❌ No

**Why:** The CLI approach requires manual invocation through a "prime prompt" pattern. Evidence:
- README line 54 shows: `prompt: "/prime_kalshi_cli_tools"` - This is a manual slash command
- The prime prompt `/prime_kalshi_cli_tools` explicitly instructs: "Read ONLY @apps/2_cli/README.md and @apps/2_cli/kalshi_cli/cli.py"
- After priming, the agent must manually decide to call CLI commands via subprocess
- No automatic trigger mechanism like Skills (which use description-based triggering)

**Discovery mechanism:** Manual prime prompt
- User or agent must invoke `/prime_kalshi_cli_tools` slash command
- This loads 709 lines of context (25 line prime + 131 line README + 553 line cli.py)
- Agent then knows CLI exists and how to use it
- Subsequent usage requires explicit `uv run kalshi <command>` calls

**Prime prompt pattern:** ✅ Yes, explicitly documented
- Location: `.claude/commands/prime_kalshi_cli_tools.md` (26 lines)
- Purpose: Load CLI documentation and usage instructions into context
- Workflow:
  1. Read README.md and cli.py
  2. Report understanding of toolset
  3. Use CLI commands via subprocess as needed
- Instructions emphasize `--json` flag for all commands

**Manual vs automatic:** Manual
- Requires explicit prime command invocation
- Agent must consciously choose to use CLI over other tools
- No automatic activation based on user request content

**Confidence:** High (based on direct evidence from prime prompt file and README)

## 2. Token Efficiency

**Startup cost:** ~709 lines of context
- Prime prompt: 26 lines
- README.md: 131 lines
- cli.py: 553 lines
- Total: ~1,700-2,000 tokens (estimated 3 tokens/line average)

**Per-operation cost:** ~50-200 tokens
- Subprocess overhead: Command construction + JSON parsing
- Example: `uv run kalshi status --json`
- Output is pure JSON (no debug noise when `--json` used)
- Agent must parse JSON and format for user if needed

**vs MCP comparison:** README claims verified
- README states: "✅ **Improved Context** - Agent reads ~half as much context as the MCP Server"
- MCP Server: 15 tools with full schema = ~3,000-4,000 tokens per startup
- CLI: 13 commands in single file = ~2,000 tokens (prime + README + cli.py)
- **Verdict:** ~50% reduction in startup context is accurate

**Progressive disclosure:** ❌ Not possible
- All 13 commands loaded at once via cli.py (553 lines)
- Cannot selectively load individual commands
- Trade-off: Single source of truth vs progressive loading
- Contrast with file system scripts: Each script ~150-200 lines, loaded on-demand

## 3. Implementation Pattern

**Architecture:** CLI wraps HTTP API with Click framework
- **HTTP Layer:** `kalshi_cli/modules/client.py` (615 lines)
  - Direct httpx-based HTTP client
  - All API logic centralized in KalshiClient class
  - Methods: get_markets(), get_market(), get_events(), etc.
- **CLI Layer:** `kalshi_cli/cli.py` (553 lines)
  - Click command group with 13 commands
  - Each command: Thin wrapper calling client methods
  - Dual output: Human-readable (default) or `--json` flag
- **Cache Layer:** KalshiSearchCache class (client.py)
  - Pandas-based search with 6-hour TTL
  - First run: 2-5 min to build cache
  - Subsequent: Instant searches

**Commands:** 13 total, structured by domain
1. **Core:** status, search
2. **Markets:** markets, market, orderbook, trades, market-candles
3. **Events:** events, event, multivariate, event-candles
4. **Series:** series-list, series

**Output modes:** Dual mode via `--json` flag
- **Human mode:** Formatted tables, colors, emojis (default)
- **JSON mode:** Pure JSON to stdout, clean for automation
  - `quiet=True` passed to suppress debug messages
  - Example: `kalshi search "bitcoin" --json` returns clean array
- **Key insight:** Single codebase serves both humans and agents

**Single source of truth:** ✅ Maintained through HTTP client
- All API logic in `client.py` KalshiClient class
- CLI commands delegate to client methods
- MCP server (app 1) wraps CLI via subprocess
- Scripts (app 3) duplicate HTTP logic per-file (trade-off for isolation)
- **Pattern:** API Client → CLI → MCP (if needed)

## 4. claude-mem Integration Analysis

**Current:** Skills + curl + Bash (manual HTTP construction)
- Each claude-mem skill operation constructs curl commands from scratch
- Estimated ~680-730 tokens per search operation (based on parent analysis)
- Skills invoke curl via Bash tool
- No caching, no reusable HTTP client

**With CLI:**
- **Would it improve autonomy?** ❌ No
  - CLI requires manual prime prompt invocation
  - Current skill pattern auto-triggers on description match
  - **Verdict:** Switching to CLI would reduce autonomy

- **Token cost impact?** ⚠️ Mixed
  - **Startup:** ~2,000 tokens (prime + README + cli.py) vs current skill ~100-200 tokens
  - **Per-operation:** ~50-200 tokens (subprocess + JSON) vs current ~680-730 tokens (curl construction)
  - **Net effect:** Higher upfront, lower per-operation
  - **Break-even:** After ~3-4 operations, CLI becomes more efficient

- **Implementation effort?** Medium
  - Create Python CLI mirroring MCP tools (13 commands for claude-mem)
  - Write prime prompt command
  - Update skills to call CLI instead of curl
  - Estimated: 3-5 hours for initial implementation

- **Worth it?** ❌ No, for claude-mem specifically
  - **Reason:** Loss of autonomy outweighs token savings
  - Skills auto-trigger on keywords like "search claude-mem"
  - CLI requires manual `/prime_claude_mem` invocation first
  - Users expect immediate search capability, not two-step prime→use
  - **Exception:** Could be worth it for high-frequency batch operations (10+ calls/session)

## 5. Hybrid Pattern Assessment

**CLI + Skills approach:**
README mentions this but doesn't implement it. Theoretical pattern:
1. **Skill description** triggers automatic activation
2. **Skill instructions** call CLI commands via subprocess
3. **CLI** provides clean JSON output
4. **Skill** formats output for user

**How would it work?**
```markdown
# claude-mem skill (SKILL.md)
description: Search claude-mem memory...

# Instructions
1. Ensure CLI is installed: Check for `claude-mem` CLI
2. Use CLI for operations: `uv run claude-mem search "query" --json`
3. Parse JSON and present results

# Available via:
- search: claude-mem search
- get context: claude-mem context
- etc.
```

**Benefits over current?**
- ✅ Maintains auto-trigger autonomy (via skill description)
- ✅ Reduces per-operation token cost (CLI vs curl construction)
- ✅ Single source of truth (CLI wraps MCP/HTTP)
- ✅ Dual usage: Humans can use CLI directly, agents via skills

**Drawbacks?**
- ❌ Added complexity: Three layers (Skill → CLI → MCP/HTTP)
- ❌ Installation burden: Must install CLI first
- ❌ Version sync: Skill and CLI must stay coordinated
- ❌ Debugging difficulty: Harder to trace skill→CLI→HTTP issues
- ❌ Not truly "self-contained" like current pattern

**Recommendation?** ⚠️ Only if building ecosystem
- **Yes, if:** Building multi-tool suite (10+ tools) for team reuse
  - CLI serves humans and multiple agent contexts
  - Worth the coordination overhead at scale
- **No, if:** Single-purpose tool like claude-mem
  - Current skill+curl pattern simpler, equally effective
  - Direct HTTP calls easier to debug and maintain

## 6. Agent Autonomy Assessment (Summary)

**Auto-invoked:** ❌ No

**Why:**
- CLI is a passive tool requiring manual activation
- Prime prompt pattern: User must invoke `/prime_kalshi_cli_tools` first
- No automatic discovery mechanism
- Agent must be explicitly told "use this CLI" before knowing it exists
- Contrast with Skills: Auto-trigger when description matches user request

**Key distinction:**
- **MCP/Skills:** "Agent discovers and invokes automatically"
- **CLI:** "Agent uses when told to use it"

**Confidence:** High

## Summary & Recommendations

### For claude-mem specifically:

**Recommendation:** ❌ Do not adopt CLI pattern

**Reasoning:**
1. **Autonomy loss is critical:** Users expect "search claude-mem for X" to just work
2. **Token savings insufficient:** Per-op savings (~500 tokens) don't justify startup cost
3. **Complexity not warranted:** Current skill+curl pattern is simple, debuggable, self-contained
4. **No team reuse case:** claude-mem is single-purpose memory tool, not multi-tool suite

### CLI pattern is valuable for:

✅ **Multi-tool ecosystems** (10+ related commands)
- Shared by humans and agents
- High-frequency usage (10+ ops/session)
- Team collaboration via standardized CLI

✅ **Dual-use cases** (human + agent)
- CLI for direct human use
- Same CLI for agent automation via skills
- Single source of truth architecture

❌ **Not valuable for:**
- Single-purpose tools (like claude-mem)
- Auto-trigger priority (skills better)
- Low-frequency usage (<5 ops/session)

### Key insight from beyond-mcp:

The CLI approach trades **autonomy** for **efficiency** and **reusability**.

For claude-mem:
- We need autonomy (auto-trigger on memory searches)
- Current efficiency is acceptable (~680 tokens/op)
- Reusability is not a priority (single-purpose tool)

**Verdict:** Current skill+curl pattern is optimal for claude-mem's use case.
