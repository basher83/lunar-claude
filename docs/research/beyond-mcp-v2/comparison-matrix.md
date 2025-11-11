# Beyond-MCP Approaches: Comparison Matrix

## Agent Autonomy (Primary Concern)

| Approach | Auto-Invoked | Discovery Mechanism | Evidence | Confidence |
|----------|--------------|---------------------|----------|------------|
| MCP Server | ✅ Yes | Tool descriptions loaded into context on session start; FastMCP exposes all tools immediately | README shows conversational queries triggering tools; comparison table explicitly states "Agent Invoked: Yes" | **High** |
| CLI | ❌ No | Manual prime prompt via slash command (`/prime_kalshi_cli_tools`) | README line 54 shows manual invocation; comparison table states "Agent Invoked: No" | **High** |
| Scripts | ❌ No | Agent must explicitly read scripts from filesystem | No protocol exposure; requires explicit Bash tool usage | **High** |
| Skill | ❓ Claimed but Unproven | Trigger keywords in description; requires LLM routing decision | README claims "model-invoked" but provides ZERO empirical evidence; no tests, metrics, or examples | **Low** |

### Critical Finding: Skills are Probabilistic, Not Deterministic

**MCP tools** appear in tool list automatically → No routing decision required → Deterministic invocation

**Skills** require extra steps:
1. User says something
2. Claude decides "should I load a skill?" ← **Critical decision point**
3. Claude searches available skills
4. Claude matches keywords
5. Claude invokes skill

Skills depend on winning step 2's routing lottery. Good keywords increase probability but don't guarantee invocation.

## Token Efficiency

| Approach | Startup Cost | Per-Operation | Scaling | vs claude-mem Current |
|----------|--------------|---------------|---------|----------------------|
| MCP Server | ~3,900-4,500 tokens (13 tools) | ~50-100 tokens | Linear: +250-350 tokens per tool | **Much worse** (claude-mem removed MCP, saved 2,250 tokens) |
| CLI | ~2,582 tokens (README + cli.py) | ~50-100 tokens | Constant: all commands in one file | **Break-even at 4-5 operations** (worse for typical short sessions) |
| Scripts | ~58 tokens (README only) | ~400-1,200 tokens per script read | Constant: load only needed scripts | **Better** (current pattern already uses this) |
| Skill | ~96-250 tokens (SKILL.md) | ~1,500-6,300 tokens (operations/*.md) | Progressive: load details on-demand | **Current baseline** (claude-mem already uses this) |

### Key Insights

**Token efficiency ranking:**
1. **Scripts/Skills** (progressive disclosure) - Best for low-operation sessions
2. **CLI** (prime once, cheap operations) - Best for high-operation sessions (5+)
3. **MCP** (expensive startup, cheap operations) - Only good for multi-session persistence

**claude-mem context:**
- Current: Skills pattern (~96 token SKILL.md + ~680-730 tokens per operation)
- Typical usage: 1-3 operations per session
- **Scripts/Skills pattern is optimal for current usage**

## Implementation Effort

| Approach | Complexity | Stack Alignment | Breaking Changes | Timeline |
|----------|------------|-----------------|------------------|----------|
| MCP Server | Medium-High | Requires server + PM2 management | ✅ Yes (removes Skills) | 2-4 weeks |
| CLI | Medium-High | Adds new CLI layer | ⚠️ Partial (can coexist with Skills) | 8-16 hours |
| Scripts | Low | Just Python scripts | ❌ No (enhancement to Skills) | 4-8 hours |
| Skill | N/A | Current implementation | N/A | N/A (already done) |

### Implementation Recommendations

**MCP Server:**
- ❌ **DO NOT adopt** - claude-mem removed MCP in v5.4.0 for good reasons
- Token overhead unacceptable
- Context loss defeats purpose of memory system

**CLI:**
- ❌ **DO NOT adopt** - reduces autonomy vs current Skills pattern
- Requires manual prime prompt
- Only beneficial for high-operation sessions (uncommon)

**Scripts Enhancement:**
- ✅ **CONSIDER** as Quick Win improvement
- Replace verbose operations/*.md with executable scripts/*.sh
- Matches Kalshi's successful pattern
- Preserves Skills autonomy while simplifying execution

**Skill Optimization:**
- ✅ **PRIORITY** - improve current implementation
- Rewrite SKILL.md description with unique triggers
- Surface all operations directly (no link indirection)
- Low effort, high impact

## Discoverability vs Token Cost Tradeoff

### The Core Tension

**High visibility** (MCP) → High tokens → Auto-invoked ✅ → Context loss ❌

**Low visibility** (Scripts/Skills) → Low tokens → Manual/Probabilistic ❌ → Context preserved ✅

### Sweet Spot Analysis

**MCP approach:**
- Maximum discoverability: Tools always visible
- Maximum token cost: ~4,000 tokens upfront
- Deterministic invocation: No routing decision
- **Tradeoff:** Pays token tax for guaranteed discovery

**Skills approach:**
- Moderate discoverability: Keywords must trigger routing
- Minimal token cost: ~96 tokens upfront
- Probabilistic invocation: Depends on LLM routing
- **Tradeoff:** Saves tokens but risks being ignored

**Optimal pattern for claude-mem:**
- Use Skills (low token cost, context preservation)
- Maximize trigger quality (keyword specificity, concrete examples)
- Surface capabilities (list all operations in SKILL.md)
- Accept probabilistic nature but optimize probability

### Why Progressive Disclosure Hurts Discoverability

**Evidence from File System Scripts:**
- SKILL.md line 13: "Don't read scripts unless absolutely needed"
- 2,000+ lines of implementation hidden by default
- Agent knows scripts EXIST but not detailed CAPABILITIES
- Works great for explicit requests; fails for proactive suggestions

**Evidence from claude-mem:**
- version-bump skill: 96 lines visible, 721 lines hidden
- Operations hidden behind links
- Same progressive disclosure tradeoff
- **Hypothesis confirmed:** This likely reduces proactive usage

**The Fix:**
- Keep progressive disclosure for IMPLEMENTATION (operations/*.md details)
- Improve visibility of CAPABILITIES (list all operations in SKILL.md)
- Balance: Show what's possible (low token cost), hide how it works (load on-demand)

## Key Findings Summary

### 1. Most Auto-Invoked Approach

**MCP Server** with **High confidence**

- Tool descriptions loaded into context automatically
- No routing decision required
- README and comparison table explicitly confirm autonomous invocation
- Evidence is clear and multi-sourced

### 2. Most Token Efficient

**Skills** (current pattern) for typical usage

- ~96 token startup vs ~3,900 (MCP) or ~2,582 (CLI)
- Progressive disclosure: load details only when needed
- Optimal for 1-3 operation sessions (typical for claude-mem)

**CLI** becomes better at 5+ operations per session (uncommon)

### 3. Best for claude-mem Context

**Skills pattern (current)** with improvements

**Why:**
- ✅ Token efficient for typical usage (1-3 operations)
- ✅ Preserves conversation context (vs MCP's statelessness)
- ✅ Already implemented (no migration risk)
- ✅ Can be optimized with Quick Wins (hours not weeks)

**Don't adopt:**
- ❌ MCP: Loses context, high tokens, already removed for good reasons
- ❌ CLI: Reduces autonomy, requires manual prime

### 4. Easiest to Implement

**Skill improvements** (Quick Wins: 2-4 hours)

1. Rewrite SKILL.md description with unique triggers (1 hour)
2. Surface all operations in SKILL.md directly (30 min)
3. Add concrete trigger phrase examples (30 min)

**Medium effort enhancement:**
- Add scripts/*.sh wrappers (4-8 hours)
- Simplifies execution vs reading operations/*.md then constructing curl

## Root Cause: Why Claude Doesn't Use claude-mem Proactively

### Primary Cause: Weak Description (Likelihood: HIGH)

**Problem:**
- Generic triggers: "bugs fixed, features implemented" applies to ANY dev work
- Competes with Claude's native memory: User asks "what did we do?" → Claude answers from current session
- Missing unique identifiers: No "claude-mem", "cross-session memory", "persistent database"
- No temporal differentiation: Doesn't clarify it's for PAST sessions (days/weeks/months ago)

**Evidence:**
- Kalshi: "prediction markets, Kalshi markets, betting odds" (unique domain)
- Claude-mem: "bugs, features, history" (generic, applies everywhere)
- When is the last time you heard someone say "claude-mem" in a query? Never.

**Fix:** Rewrite description with unique triggers (1 hour)

### Secondary Cause: Hidden Capabilities (Likelihood: MEDIUM)

**Problem:**
- 9 operations hidden behind links in operations/
- Kalshi shows all 10 scripts directly in 71-line SKILL.md
- Claude must read SKILL.md (96 lines) THEN operations/*.md (1.4-6.2k each) to understand capabilities
- Two-layer indirection vs one-layer visibility

**Evidence:**
- Kalshi pattern: All capabilities visible in main SKILL.md
- Claude-mem pattern: Operations listed as links, not descriptions
- Progressive disclosure saves tokens but hides what's possible

**Fix:** List all operations with one-line purposes in SKILL.md (30 min)

### Tertiary Cause: Pattern Limitation (Likelihood: MEDIUM)

**Problem:**
- Skills require LLM routing decision ("should I load this skill?")
- MCP tools bypass this decision (always visible)
- Skills are inherently probabilistic
- No evidence ANY skill reliably auto-invokes

**Evidence:**
- Beyond-MCP README claims "model-invoked" with ZERO evidence
- No tests, metrics, examples of auto-invocation
- Claims are aspirational, not empirical
- Skill pattern depends on winning routing lottery

**Fix:** Can't fix pattern limitation, but can optimize probability with better description

## Recommended Strategy

### Immediate Action (Today: 2-4 hours)

**Try Quick Wins first** - Low effort, high impact, easily reversible

1. ✅ Rewrite SKILL.md description (1 hour)
   - Add "claude-mem", "cross-session memory database", "persistent memory"
   - Add "NOT in current conversation context"
   - Add "days/weeks/months ago", "previous sessions"
   - Add concrete example: "did we already solve this?"

2. ✅ Surface all operations in SKILL.md (30 min)
   - List all 9 operations with one-line purposes
   - Match Kalshi's successful pattern
   - Remove link indirection

3. ✅ Add concrete trigger phrases (30 min)
   - "Did we already fix this bug?"
   - "How did we solve X last time?"
   - "What did we do in yesterday's session?"

**Success criteria:**
- User asks "did we fix this before?" → Claude loads skill
- Clear differentiation from current-session questions
- Capabilities visible without reading operations/*.md

**If this doesn't work:** Proceed to medium effort improvements

### Medium Effort (Next Week: 4-8 hours)

**If Quick Wins don't improve auto-invocation:**

1. ✅ Create scripts/*.sh wrappers (4-8 hours)
   - Wrap curl commands in executable scripts
   - Match Kalshi pattern: `./scripts/search-obs.sh --query "auth"`
   - Simpler than reading operations/*.md then constructing curl

2. ✅ Consolidate SKILL.md to <80 lines (2-4 hours)
   - Move technical notes, performance tips to operations/
   - Keep only essential trigger info in main SKILL.md
   - Faster load = higher probability of invocation

**Success criteria:**
- Execution complexity reduced
- Cognitive load lower (fewer steps)
- Still maintains Skills autonomy

**If this doesn't work:** Accept pattern limitation

### Nuclear Option (Only if Desperate: 2-4 weeks)

**Convert to MCP server** - Only if absolutely necessary

**When to consider:**
- Quick Wins tried and failed
- Medium effort tried and failed
- Auto-invocation is critical requirement
- Willing to accept token cost

**Why avoid:**
- Loses context preservation (defeats memory system purpose)
- High token cost (already removed in v5.4.0)
- Breaking change
- No guarantee MCP works better for this use case

**Recommendation:** Don't go nuclear. Accept that Skills are probabilistic and optimize the probability.

## Decision Tree

```text
┌─────────────────────────────────────┐
│ Is Claude using claude-mem          │
│ proactively?                        │
└──────────┬──────────────────────────┘
           │
    ┌──────┴───────┐
    │              │
   NO             YES
    │              │
    │              └─→ Problem solved, no action needed
    │
    ▼
┌─────────────────────────────────────┐
│ Step 1: Try Quick Wins (2-4 hours) │
│ - Rewrite description with unique  │
│   triggers                          │
│ - Surface all operations in         │
│   SKILL.md                          │
│ - Add concrete trigger phrases      │
└──────────┬──────────────────────────┘
           │
    ┌──────┴───────┐
    │              │
 WORKS         DOESN'T WORK
    │              │
    │              ▼
    │      ┌─────────────────────────────────────┐
    │      │ Step 2: Medium Effort (4-8 hours)  │
    │      │ - Create scripts/*.sh wrappers     │
    │      │ - Consolidate SKILL.md to <80 lines│
    │      └──────────┬──────────────────────────┘
    │                 │
    │          ┌──────┴───────┐
    │          │              │
    │       WORKS         DOESN'T WORK
    │          │              │
    │          │              ▼
    │          │      ┌─────────────────────────────────────┐
    │          │      │ Step 3: Accept Pattern Limitation  │
    │          │      │ - Skills are probabilistic         │
    │          │      │ - Optimize probability, not        │
    │          │      │   guarantee                        │
    │          │      │ - Consider MCP only if absolutely  │
    │          │      │   critical (NOT recommended)       │
    │          │      └─────────────────────────────────────┘
    │          │
    └──────────┴─→ Done ✅
```

## Conclusion

**Keep Skills pattern, optimize discoverability**

The analysis reveals that:

1. **MCP is most discoverable** but unacceptable for claude-mem (token cost, context loss)
2. **CLI reduces autonomy** vs current Skills pattern (requires manual prime)
3. **Scripts/Skills pattern is optimal** for claude-mem's usage (token efficient, context preserving)
4. **Problem is execution, not pattern** - Skills CAN work with better description
5. **Quick Wins are highest ROI** - 2-4 hours to significantly improve probability

**Don't change the pattern. Improve the description.**

Start with Quick Wins today. If claude-mem still isn't auto-invoked after improvements, accept that Skills are probabilistic and consider it a documentation/trigger optimization problem, not an architecture problem.
