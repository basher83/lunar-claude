# Decision Framework: claude-mem Toolset Strategy

## Problem Statement

Claude isn't using claude-mem search skill proactively.

**Question:** Should we improve current implementation or change the pattern?

**Context:**
- claude-mem uses Skills pattern (progressive disclosure)
- Removed MCP in v5.4.0 (saved 2,250 tokens)
- Current: ~96 token SKILL.md + ~680-730 tokens per operation
- Typical usage: 1-3 operations per session

---

## Root Cause Analysis

Based on 4 approach analyses comparing MCP, CLI, File System Scripts, and Skills:

### Finding 1: Why Claude Doesn't Use claude-mem Proactively

**Most likely cause:** **Weak skill description + hidden capabilities**

#### Evidence: Generic Triggers

**Current description:**
> "Search claude-mem persistent memory for past sessions, observations, bugs fixed, features implemented, decisions made, code changes, and previous work."

**Problem:** These triggers are generic and compete with Claude's native memory:
- "bugs fixed" - Claude already knows bugs from current conversation
- "features implemented" - Claude already knows features from current conversation
- "past sessions" - Vague; could mean "earlier today" or "last month"
- No unique identifiers like "claude-mem", "cross-session database", "persistent memory"

**Compare to Kalshi (successful pattern):**
> "Access Kalshi prediction market data including market prices, orderbooks, trades, events, and series information. Use when the user asks about prediction markets, Kalshi markets, betting odds..."

**Difference:**
- Kalshi: Domain-specific ("Kalshi", "prediction markets", "betting odds")
- Claude-mem: Generic ("bugs", "features", "history")

**When was the last time someone said "claude-mem" in a query?** Never. Because the trigger words don't include it.

#### Evidence: Hidden Capabilities

**Current pattern:**
- SKILL.md shows 9 operations as links: `[Search Observations](operations/observations.md)`
- Capabilities hidden behind two layers:
  1. Load SKILL.md (96 lines)
  2. Read operations/*.md (1.4-6.2k per file)

**Kalshi pattern:**
- SKILL.md lists all 10 scripts directly with purposes
- All capabilities visible in 71 lines
- One layer: Load SKILL.md → see everything

**The problem:**
- Claude loads SKILL.md
- Sees "operations/observations.md" link
- Doesn't know what observations.md can DO without reading it
- Decision fatigue: "should I read 9 more files?"

#### Evidence: Lacks Temporal Differentiation

**Critical gap:** Description doesn't clarify claude-mem is for PAST sessions (days/weeks/months ago) vs current conversation.

**User says:** "What did we do with authentication?"
**Claude thinks:** "I can answer from current conversation context. No need to check external memory."

**Missing trigger:** "NOT in current conversation", "previous sessions", "days/weeks/months ago"

**Confidence:** **High** - This is the root cause

### Finding 2: Discoverability Mechanisms That Work

**From MCP:**
- ✅ Tool descriptions loaded automatically (no routing decision)
- ✅ All tools visible immediately (no progressive disclosure)
- ✅ Semantic naming (`search_markets`, `get_status`)
- ❌ High token cost (~4,000 tokens for 13 tools)
- ❌ Context loss (stateless operations)

**From CLI:**
- ✅ Single source of truth (direct API implementation)
- ✅ Dual output modes (human + JSON)
- ❌ Requires manual prime prompt (not autonomous)
- ❌ Token overhead for startup (~2,582 tokens)

**From Scripts:**
- ✅ Progressive disclosure (low token cost per script)
- ✅ Self-contained execution (embedded HTTP client)
- ❌ Capabilities hidden by default ("don't read unless needed")
- ❌ Not discoverable proactively

**From Skills:**
- ✅ Trigger-based activation (can be autonomous)
- ✅ Progressive disclosure (token efficient)
- ✅ Context preservation (vs MCP statelessness)
- ❌ Probabilistic invocation (depends on LLM routing)
- ❌ Quality of description matters critically

**Key insight:** MCP is deterministic (always visible), Skills are probabilistic (depend on routing decision). Can't change pattern limitation, but CAN optimize probability.

### Finding 3: Token Cost vs Autonomy Tradeoff

**The Tension:**
- High visibility (MCP) → High tokens → Auto-invoked ✅ → Context loss ❌
- Low visibility (Skills) → Low tokens → Probabilistic ❌ → Context preserved ✅

**Sweet spot for claude-mem:**
- Use Skills (low tokens, context preservation)
- Maximize trigger quality (keyword specificity)
- Surface capabilities (list operations in SKILL.md)
- Accept probabilistic nature, optimize probability

**Why not MCP?**
- claude-mem removed MCP in v5.4.0 for good reasons
- Token overhead unacceptable (2,250 tokens saved)
- Context loss defeats memory system purpose

**Why not CLI?**
- Reduces autonomy (requires manual prime prompt)
- Only beneficial for 5+ operations per session
- Adds complexity without solving discoverability

**Why optimize Skills?**
- Already implemented (no migration risk)
- Token efficient for typical usage (1-3 ops)
- Can be dramatically improved with Quick Wins (hours not weeks)

---

## Recommendations (Effort-Based)

### Option 1: Quick Fixes (2-4 hours, Low Risk) ← START HERE

**If root cause is:** Weak skill description + hidden capabilities

**Actions:**

#### 1. Rewrite SKILL.md Description (1 hour)

**Current:**
```yaml
description: Search claude-mem persistent memory for past sessions, observations, bugs fixed, features implemented, decisions made, code changes, and previous work. Use when answering questions about history, finding past decisions, or researching previous implementations.
```

**Recommended:**
```yaml
description: Search claude-mem's persistent cross-session memory database to find work from previous conversations days, weeks, or months ago. Access past session summaries, bug fixes, feature implementations, and decisions that are NOT in the current conversation context. Use when user asks "did we already solve this?", "how did we do X last time?", or needs information from previous sessions stored in the PM2-managed database. Searches observations, session summaries, and user prompts across entire project history.
```

**Key improvements:**
- ✅ Add "claude-mem" (unique trigger)
- ✅ Add "cross-session memory database" (differentiates from current conversation)
- ✅ Add "NOT in current conversation context" (clear value prop)
- ✅ Add "days, weeks, or months ago" (temporal trigger)
- ✅ Add "did we already solve this?" (concrete user question)
- ✅ Add "previous sessions" (specific trigger phrase)
- ✅ Add "PM2-managed database" (shows it's a real system)

#### 2. Surface All Operations in SKILL.md (30 min)

**Current pattern:** Links like `[Search Observations](operations/observations.md)`

**Recommended pattern:** Direct listing like Kalshi:

```markdown
## Available Operations

### Search Operations
- **observations** - Full-text search across all observations (bugs, features, decisions, discoveries)
- **sessions** - Search session summaries to find what was accomplished when
- **prompts** - Find what users have asked about in previous sessions

### Filtered Search
- **by-type** - Filter by observation type (bugfix, feature, refactor, decision, discovery, change)
- **by-concept** - Find observations tagged with specific concepts (problem-solution, how-it-works, gotcha)
- **by-file** - Find all work related to a specific file path across all sessions

### Timeline & Context
- **recent-context** - Get last N sessions with summaries and observations
- **timeline** - Get chronological context around a specific point in time (before/after window)
- **timeline-by-query** - Search first, then get timeline context around best match

For detailed instructions on any operation, read operations/<operation-name>.md
```

**Benefits:**
- All capabilities visible immediately
- No link-clicking required to understand what's possible
- ~15 lines vs 9 separate files
- Matches Kalshi's successful pattern

#### 3. Add Concrete Trigger Phrases (30 min)

**Add to SKILL.md:**

```markdown
## Common Trigger Phrases

Use this skill when you see:
- "Did we already fix this bug?" or "Have we seen this error before?"
- "How did we solve X last time?" or "What approach did we take for X?"
- "What did we do in yesterday's/last week's session?"
- "Show me all authentication-related changes across all sessions"
- "What features did we add last month?"
- "Why did we choose this approach?" (for decisions made in past sessions, not current)
- "What files did we modify when we added X?" (across all sessions)
- "When did we last work on this?" or "What's the history of this file?"
```

**Benefits:**
- Concrete user language vs abstract categories
- Claude can pattern-match actual phrases
- Clear differentiation from current-session questions

**Effort:** 2-4 hours total
**Cost:** Zero (just markdown edits)
**Risk:** None (easily reversible)

**Try this first:** ✅ Yes
**Reasoning:** Highest ROI (impact/effort ratio), lowest risk, addresses root cause directly

**Success Criteria:**
- [ ] User asks "did we fix this before?" → Claude loads skill without prompting
- [ ] Maintains token efficiency (within 10% of current ~96 tokens)
- [ ] Works across different query types (bugs, features, history)
- [ ] Repeatable behavior (not one-off luck)

**Timeline:** Can be done today

**Next steps if this works:** Monitor usage, refine triggers based on actual queries

**Next steps if this fails:** Proceed to Option 2 (Medium Effort)

---

### Option 2: Pattern Improvements (4-8 hours, Medium Risk)

**If root cause is:** Progressive disclosure balance + execution complexity

**Actions:**

#### 1. Create Executable Script Wrappers (4-8 hours)

**Problem:** Current pattern requires:
1. Read operations/recent-context.md
2. Construct curl command with correct parameters
3. Execute bash
4. Parse JSON response

**Solution:** Pre-built executable scripts like Kalshi:

```bash
.claude/skills/search/scripts/
├── recent.sh          # uv run recent.sh --limit 5
├── search-obs.sh      # uv run search-obs.sh "authentication"
├── search-session.sh  # uv run search-session.sh "added login"
├── by-type.sh         # uv run by-type.sh --type bugfix --limit 10
├── by-file.sh         # uv run by-file.sh auth/login.ts
└── timeline.sh        # uv run timeline.sh --anchor 123 --depth 5
```

**Each script:**
- Wraps curl command construction
- Handles authentication/port
- Supports `--help` and `--json` flags
- Self-contained execution

**Benefits:**
- Single action vs multi-step process
- Matches Kalshi's successful pattern
- Reduces cognitive load
- Easier for Claude to execute

**Drawbacks:**
- More files to maintain
- Duplicates some logic from operations/*.md

**Implementation:**
```bash
#!/usr/bin/env bash
# scripts/search-obs.sh
set -euo pipefail

QUERY="${1:-}"
LIMIT="${2:-10}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: $0 <query> [limit]"
  exit 1
fi

curl -s "http://localhost:37777/api/observations/search?query=${QUERY}&limit=${LIMIT}&format=index" | jq
```

#### 2. Consolidate SKILL.md to <80 Lines (2-4 hours)

**Problem:** 96 lines with lots of sections dilutes signal

**Solution:** Move non-essential content to operations/

**Remove from SKILL.md:**
- Common Workflows (already in operations/common-workflows.md)
- Response Formatting (already in operations/formatting.md)
- Technical Notes → operations/help.md
- Performance Tips → operations/help.md
- Error Handling → operations/help.md

**Keep in SKILL.md:**
- Enhanced description
- When to Use (with concrete trigger phrases)
- Available Operations (expanded with purposes)
- Quick examples

**Target:** 70-75 lines (match Kalshi's 71-line pattern)

**Effort:** 4-8 hours total
**Cost:** Some reorganization
**Risk:** Low (can revert if worse)

**Try if Option 1 fails:** ✅ Yes
**Reasoning:** Addresses execution complexity, maintains Skills pattern

**Success Criteria:**
- [ ] Execution complexity reduced (fewer steps)
- [ ] Cognitive load lower for Claude
- [ ] Still maintains Skills autonomy
- [ ] Token cost similar or better

**Timeline:** Next week if Quick Wins don't work

**Next steps if this works:** Monitor usage, gather metrics

**Next steps if this fails:** Accept pattern limitation (Option 3)

---

### Option 3: Accept Pattern Limitation (0 hours, Reality Check)

**If root cause is:** Fundamental Skills pattern limitation

**Reality:**
- Skills are inherently probabilistic (depend on LLM routing)
- No evidence ANY skill reliably auto-invokes (even well-designed ones)
- MCP tools are deterministic; Skills require decision step
- Beyond-MCP claims are aspirational, not empirical

**Actions:**
1. Accept that Skills won't auto-invoke 100% of time
2. Optimize probability with Quick Wins
3. Document clear slash command for manual invocation
4. Consider this a documentation problem, not architecture problem

**When to accept:**
- Quick Wins tried and failed
- Medium Effort tried and failed
- Auto-invocation is "nice to have" not "must have"
- Current pattern is working for explicit requests

**Alternative approach:**
- Create `/search-mem` slash command for manual invocation
- Document trigger phrases for users
- Focus on making manual usage excellent
- Accept that proactive suggestions are bonus, not requirement

**Try this:** Only if Options 1 & 2 fail

**Reasoning:** Skills pattern is still optimal for claude-mem's use case (token efficiency, context preservation). Auto-invocation is bonus, not requirement.

---

### Nuclear Option: Pattern Change (2-4 weeks, High Risk) - NOT RECOMMENDED

**If root cause is:** Pattern limitation can't be fixed with optimization

**Recommended pattern:** MCP Server

**Actions:**
1. Re-implement MCP server wrapper around HTTP API (1-2 weeks)
2. Re-add to Claude Code configuration (1 hour)
3. Test all operations through MCP protocol (2-3 days)
4. Document migration for users (1 day)

**Effort:** 2-4 weeks
**Cost:** Token overhead (2,250+ tokens), context loss, breaking changes
**Risk:** High - may not solve problem, loses Skills benefits

**Why MCP?**
- Tools auto-invoked (no routing decision)
- Always visible to Claude
- Deterministic discovery

**Why NOT MCP?**
- ❌ High token cost (already removed in v5.4.0)
- ❌ Context loss (defeats memory system purpose)
- ❌ Breaking change for users
- ❌ Adds complexity (server management)
- ❌ No guarantee it works better for this use case

**Try only if:** Options 1, 2, and 3 all failed AND auto-invocation is critical requirement

**Recommendation:** ❌ **DO NOT DO THIS**

**Reasoning:**
- Quick Wins haven't been tried yet
- Pattern change won't necessarily solve discoverability
- Loses Skills benefits (context, token efficiency)
- High effort with uncertain payoff

---

## Decision Tree

```text
Start: Is claude-mem being used proactively?
├─ YES → ✅ Done, no action needed
└─ NO → Try Quick Fixes (2-4 hours)
    ├─ Rewrite description with unique triggers
    ├─ Surface all operations in SKILL.md
    └─ Add concrete trigger phrases
        ├─ WORKS → ✅ Done, monitor usage
        └─ DOESN'T WORK → Try Pattern Improvements (4-8 hours)
            ├─ Create executable script wrappers
            └─ Consolidate SKILL.md to <80 lines
                ├─ WORKS → ✅ Done, gather metrics
                └─ DOESN'T WORK → Accept Pattern Limitation
                    ├─ Skills are probabilistic (reality)
                    ├─ Document slash command for manual use
                    ├─ Optimize probability, not guarantee
                    └─ Nuclear option (MCP) NOT recommended
```

---

## Recommended Starting Point

### Action: Implement Quick Wins (Today: 2-4 hours)

**Specific tasks:**

1. **Edit `.claude/skills/search/SKILL.md`** (1 hour)
   - Replace frontmatter description with improved version
   - Add "claude-mem", "cross-session database", temporal triggers
   - Add "NOT in current conversation context"

2. **Expand operations listing** (30 min)
   - Replace links with direct descriptions
   - Show all 9 operations with one-line purposes
   - Keep "For details, read operations/<name>.md" at bottom

3. **Add trigger phrases section** (30 min)
   - List 8-10 concrete user questions
   - Use actual language patterns
   - Differentiate from current-session questions

**Test plan:**
1. Clear Claude session (start fresh)
2. Ask: "Did we already fix the authentication bug?"
3. Observe: Does Claude load search skill?
4. Ask: "What did we do last week with login?"
5. Observe: Does Claude use claude-mem or answer from current context?
6. Ask: "Show me all decisions about database schema"
7. Observe: Does Claude search or just say "I don't recall"?

**Success Criteria:**
- Claude loads skill for cross-session questions ✅
- Maintains token efficiency (within 10% of current) ✅
- Works for different query types (bugs, features, history) ✅
- Repeatable (not just once) ✅

**Timeline:** Can be implemented today

**Rationale:**
- Addresses root cause directly (weak description)
- Lowest effort/highest impact
- Zero risk (easily reversible)
- No breaking changes
- Can iterate based on results

**Next steps if this works:**
- Monitor actual usage patterns
- Refine triggers based on real queries
- Document success patterns
- Consider Quick Win successful

**Next steps if this fails:**
- Implement Pattern Improvements (Option 2)
- Or accept pattern limitation (Option 3)
- Do NOT jump to Nuclear Option

---

## Long-Term Strategy

Based on analysis, recommended approach for claude-mem toolset:

**Pattern:** Skills (current) with optimized discoverability

**Why:**
- Token efficient for typical usage (1-3 operations)
- Preserves conversation context (vs MCP statelessness)
- Progressive disclosure (load details on-demand)
- Already implemented (no migration risk)
- Can be significantly improved with Quick Wins

**Migration path:** N/A (keep current pattern)

**Improvements:**
1. ✅ Quick Wins (today: 2-4 hours)
2. ⚠️ Pattern Improvements if needed (next week: 4-8 hours)
3. ❌ Nuclear option NOT recommended

**Trade-offs accepted:**
- Skills are probabilistic (vs MCP's deterministic invocation)
- Depends on LLM routing quality
- May not auto-invoke 100% of time
- Acceptable because: token efficiency + context preservation > guaranteed discovery

**Monitoring plan:**
- Track skill invocation rate (before/after Quick Wins)
- Collect trigger patterns that work
- Refine description based on actual usage
- Iterate on trigger keywords

**Success definition:**
- Skill invoked for cross-session questions (50%+ of time)
- Token cost remains low (<200 tokens upfront)
- Context preservation maintained
- User experience improved

---

## Summary

**Don't change the pattern. Improve the description.**

**Key findings:**
1. Root cause: Weak description with generic triggers
2. Skills pattern is optimal for claude-mem's use case
3. Quick Wins can dramatically improve probability
4. MCP not recommended (token cost, context loss)
5. CLI not recommended (reduces autonomy)

**Recommended path:**
1. Try Quick Wins (today: 2-4 hours) ✅
2. If needed: Pattern Improvements (next week: 4-8 hours) ⚠️
3. If all fails: Accept probabilistic nature (reality check) ✅
4. Nuclear option: NOT recommended ❌

**Bottom line:** The Skills pattern is right for claude-mem. The description needs work. Start with Quick Wins today and see results within hours, not weeks.
