# Decision Framework: claude-mem Toolset Strategy

**Decision Date:** 2025-11-10
**Context:** Claude isn't using claude-mem search skill proactively
**Question:** Should we improve current implementation or change the pattern?

---

## Problem Statement

**Observed behavior:** Claude doesn't invoke claude-mem search skill autonomously when users ask about past work, bug fixes, or implementation history.

**Expected behavior:** User asks "what did we do last session?" → Claude automatically uses search skill → Returns results

**Impact:** Users must explicitly invoke skill or don't know it exists → Underutilization of persistent memory

**Question:** Is this a:
1. Description quality issue? (Quick fix: Rewrite SKILL.md)
2. Progressive disclosure tradeoff? (Medium fix: Rebalance visibility)
3. Pattern limitation? (Hard fix: Change to MCP/CLI/Scripts)

---

## Root Cause Analysis

### Finding 1: Why Claude Doesn't Use claude-mem Proactively

**Most likely cause: Weak Description + Hidden Capabilities (Hypothesis A+B)**

**Confidence:** HIGH (70% A + 50% B = compound effect)

**Evidence from 4-approach analysis:**

1. **Trigger keyword comparison:**
   - **Kalshi skill (auto-invoked):** "prediction markets, Kalshi markets, betting odds, market prices, orderbooks, trades"
   - **claude-mem skill (not invoked):** "observations, previous work, history, past decisions"
   - **Gap:** Kalshi uses concrete nouns; claude-mem uses abstract terms

2. **Capability visibility comparison:**
   - **Kalshi:** All 10 scripts listed with "When to use" statements in SKILL.md (1-hop navigation)
   - **claude-mem:** 10 operations referenced as file paths; "When to use" hidden in operations/ (2-hop navigation)
   - **Gap:** claude-mem hides the wrong thing (usage patterns) vs right thing (implementation)

3. **Description specificity:**
   - **Kalshi:** "Use when the user asks about prediction markets, betting odds, market prices..."
   - **claude-mem:** "Use when answering questions about history, finding past decisions..."
   - **Gap:** claude-mem is too generic (many tools could match "history")

4. **Navigation depth:**
   - **Kalshi:** SKILL.md → execute script (1 decision)
   - **claude-mem:** SKILL.md → choose operation category → read operation doc → execute (2+ decisions)
   - **Gap:** Extra cognitive load reduces proactive usage

**Supporting evidence:**

- **MCP Server analysis:** Auto-invocation works via rich semantic descriptions + always-on visibility
- **File Scripts analysis:** Extreme progressive disclosure (hiding capabilities) = zero discovery
- **CLI analysis:** Manual prime required; no auto-discovery despite detailed docs

**Conclusion:** claude-mem's description is too weak AND capabilities are too hidden for reliable auto-invocation.

---

### Finding 2: Discoverability Mechanisms That Work

**From MCP Server:**
- ✅ Rich tool descriptions with semantic intent matching
- ✅ Parameter clarity (what inputs are needed)
- ✅ Always visible in system prompt
- ❌ But: 3,750 token overhead (not acceptable for claude-mem)

**From CLI:**
- ✅ Dual output modes (human/JSON)
- ✅ Single source of truth
- ✅ 50% token reduction vs MCP
- ❌ But: Manual invocation required (no auto-discovery)

**From File Scripts:**
- ✅ Progressive disclosure saves tokens (85% reduction)
- ✅ Tiered loading (prime → README → help → source)
- ✅ "When to use" descriptions
- ❌ But: Manual prime required (zero autonomous discovery)

**From Skill (Kalshi):**
- ✅ Auto-invocation through description matching
- ✅ Concrete trigger keywords
- ✅ Capabilities visible, implementation hidden
- ✅ Low token overhead (~250)
- ✅ Context preservation
- ⚠️ Needs proper implementation to work

**Key insight:** Autonomy comes from **semantic richness + selective visibility**, not protocol or architecture.

**Mechanisms that work:**
1. Concrete trigger keywords in description (nouns > abstractions)
2. Explicit "Use when..." clauses with user language examples
3. Visible capability list (operation names + "When to use")
4. Hidden implementation details (scripts, HTTP calls)
5. One-hop navigation (minimize decisions)

---

### Finding 3: Token Cost vs Autonomy Tradeoff

**The Fundamental Tension:**

```text
High Visibility → High Autonomy → High Tokens
Low Visibility  → Low Autonomy  → Low Tokens

MCP:          [████████] Visibility  [████████] Autonomy  [████████] Tokens (3,750)
Kalshi Skill: [██████  ] Visibility  [██████  ] Autonomy  [██      ] Tokens (250)
claude-mem:   [███     ] Visibility  [█       ] Autonomy  [███     ] Tokens (300)
File Scripts: [█       ] Visibility  [        ] Autonomy  [█       ] Tokens (300)
```

**The "sweet spot" is Kalshi's approach:**
- Moderate visibility (show capabilities, hide implementation)
- Moderate-high autonomy (auto-invocation claimed)
- Low tokens (250 vs 3,750 for MCP)

**Progressive disclosure becomes counterproductive when:**
- Capabilities are hidden so well they're never discovered
- File scripts prove the extreme: 300 tokens but zero autonomy

**claude-mem's current position:**
- Hiding too much (operations/ invisible)
- Triggers too weak (abstract terms)
- Result: Low autonomy despite reasonable token cost

**Opportunity:**
- Increase visibility slightly (+100-200 tokens)
- Gain significant autonomy (from 0% to 60-80% auto-invocation?)
- Net win: Better UX for minimal token cost

---

## Recommendations (Effort-Based)

### Option 1: Quick Fixes (2-4 Hours, Low Risk) ⭐ RECOMMENDED FIRST

**If root cause is:** Weak skill description + hidden capabilities

**Actions:**

#### 1. Rewrite SKILL.md Description (30 minutes)

**Current:**
```markdown
---
name: search
description: Search claude-mem persistent memory for past sessions, observations, bugs fixed, features implemented, decisions made, code changes, and previous work. Use when answering questions about history, finding past decisions, or researching previous implementations.
---
```

**Problems:**
- "observations" is abstract (what's an observation?)
- "previous work" is generic (too broad)
- "answering questions about history" matches many tools
- Missing concrete user language examples

**Recommended rewrite:**
```markdown
---
name: search
description: Search persistent memory for bug fixes, feature implementations, architectural decisions, code changes, and completed work. Use when user asks "what did we do before?", "did we fix this bug?", "how did we implement X?", or needs historical context about files, sessions, or decisions.
---
```

**Improvements:**
- Concrete nouns: "bug fixes" > "bugs fixed"
- Specific examples: "did we fix this bug?" (user language)
- Clear triggers: "how did we implement X?" (common question)

#### 2. Add Explicit Trigger Section (15 minutes)

**Add to SKILL.md after frontmatter:**

```markdown
## Auto-Invocation Triggers

This skill automatically activates when Claude detects user questions like:

- "What did we do last session?"
- "Did we fix this bug before?"
- "How did we implement authentication?"
- "What changes were made to auth/login.ts?"
- "What were we working on yesterday?"
- "Show me past decisions about database choice"
- "What bugs have we fixed recently?"
- "When did we add the search feature?"

**Trigger keywords:** past work, previous sessions, bug fix history, implementation details, architectural decisions, code change history, historical context, completed features
```

**Impact:** Explicit keyword list helps Claude match user queries to skill

#### 3. Inline "When to Use" Statements (60 minutes)

**Add to SKILL.md Available Operations section:**

```markdown
## Available Operations (Quick Reference)

### Full-Text Search
**Search Observations** - User asks: "How did we implement X?" or "What bugs did we fix?"
- Find observations by keyword across all types
- Example: "How did we implement JWT authentication?"

**Search Sessions** - User asks: "What did we accomplish last time?" or "What was the goal?"
- Search session summaries to understand completed work
- Example: "What did we work on yesterday afternoon?"

**Search Prompts** - User asks: "Did I ask about this before?" or "What did I request?"
- Find what users have requested in past sessions
- Example: "Have I asked about database migrations before?"

### Filtered Search
**Search by Type** - User asks: "Show me all bug fixes" or "List features we added"
- Filter by observation type: bugfix, feature, refactor, decision, discovery
- Example: "What features did we implement last month?"

**Search by Concept** - User asks: "What patterns did we discover?" or "Show gotchas"
- Find observations tagged with concepts
- Example: "Show me all 'gotchas' we've encountered"

**Search by File** - User asks: "What changes to auth.ts?" or "History of this file"
- Find all work related to specific file paths
- Example: "What changes have we made to src/auth/login.ts?"

### Context Retrieval
**Get Recent Context** - User asks: "What's been happening?" or "Catch me up"
- Get recent session summaries and observations
- Example: "Catch me up on the last 3 sessions"

**Get Timeline** - User asks: "What was happening around date X?" or "Show me context"
- Get chronological timeline around specific point in time
- Example: "What was happening when we added OAuth?"

**Timeline by Query** - User asks: "When did we implement auth?" (search + timeline)
- Search then get timeline around best match
- Example: "Show me the timeline around when we fixed the login bug"

For detailed usage of each operation, see operations/ directory.
```

**Impact:**
- Claude can route to correct operation without reading operations/ files
- Reduces navigation depth from 2 hops to 1 hop
- Clear mapping from user question to operation

#### 4. Simplify Quick Decision Guide (15 minutes)

**Replace current complex guide with:**

```markdown
## Quick Decision Guide

**What's the user asking about?**

1. **Recent work** (last few sessions) → [Get Recent Context](operations/recent-context.md)
2. **Specific topic/keyword** → [Search Observations](operations/observations.md)
3. **Specific file history** → [Search by File](operations/by-file.md)
4. **Timeline/chronology** → [Get Timeline](operations/timeline.md)
5. **Other/complex query** → Read operation list above

Most common: Use Search Observations for general questions about past work.
```

**Impact:** Reduces decision points from 10 to 5 common cases

**Effort:** 2-4 hours total
**Cost:** +100-200 tokens (still well under MCP's 3,750)
**Risk:** None (easily reversible, just markdown)

**Try this first:** ✅ **YES**

**Success criteria:**
- [ ] Claude invokes skill when user asks "what did we do last session?"
- [ ] Claude invokes skill when user asks "did we fix this bug before?"
- [ ] Claude invokes skill when user asks "how did we implement X?"
- [ ] Skill invocation happens WITHOUT explicit `/skill search` command
- [ ] Works across different query phrasings

**Measurement approach:**
1. Clear session (start fresh)
2. Ask 10 test questions (without mentioning "search" or "claude-mem")
3. Count: How many times does Claude auto-invoke skill?
4. Baseline (current): 0-10%
5. Target (improved): 60-80%

---

### Option 2: Pattern Improvements (1-2 Days, Medium Risk)

**If root cause is:** Progressive disclosure balance + execution path complexity

**Try this only if Option 1 doesn't achieve 60%+ auto-invocation rate**

#### 1. Adopt Executable Scripts Pattern (1-2 days)

**Current pattern:**
- Operations are documentation (*.md files)
- Claude reads doc → constructs HTTP call → executes

**Proposed pattern (Kalshi-style):**
- Operations are scripts (*.py files)
- Claude reads SKILL.md → runs script with `--help` → executes

**Example: scripts/search-observations.py**

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["click", "httpx"]
# ///
"""
Search claude-mem observations by keyword.

When to use: User asks "How did we implement X?" or "What bugs did we fix?"

Examples:
    uv run scripts/search-observations.py "authentication" --limit 10
    uv run scripts/search-observations.py "bug" --project myapp --format full
"""
import click
import httpx

@click.command()
@click.argument('query')
@click.option('--format', default='index', type=click.Choice(['index', 'full']))
@click.option('--limit', default=10)
@click.option('--project', default=None)
def search(query, format, limit, project):
    """Search observations by keyword"""
    params = {'query': query, 'format': format, 'limit': limit}
    if project:
        params['project'] = project

    response = httpx.get('http://localhost:37777/api/search/observations', params=params)
    click.echo(response.text)

if __name__ == '__main__':
    search()
```

**Benefits:**
- Reduces navigation depth (1 hop: SKILL.md → execute)
- Self-documenting (`--help` shows usage)
- Matches proven Kalshi pattern
- Easier for Claude to discover and use

**Effort:** 1-2 days (create 10 scripts + update SKILL.md)

**Trade-offs:**
- More code to maintain (10 scripts vs 10 docs)
- Code duplication (HTTP client in each script)
- But: Better autonomy and discoverability

#### 2. Rebalance Progressive Disclosure (1 day)

**Current approach:**
- SKILL.md shows meta-information (97 lines)
- operations/ shows usage patterns (hidden)

**Proposed approach:**
- SKILL.md shows usage patterns (150 lines)
- scripts/ shows implementation (hidden)

**Move INTO SKILL.md:**
- "When to use" for each operation (from operations/*.md) [+30 lines]
- Common example queries (from common-workflows.md) [+20 lines]
- Response format examples (from formatting.md) [+30 lines]
- Total: ~180 lines (~500 tokens)

**Move OUT of SKILL.md:**
- Technical notes (port, FTS5 details) [-15 lines]
- Performance tips (in scripts instead) [-10 lines]
- Error handling details (in scripts) [-10 lines]

**Net change:** +35 lines (~+100 tokens)

**Effort:** 1 day to reorganize

**Expected impact:**
- Higher visibility of capabilities
- Lower navigation depth
- Better autonomy

**Try if Option 1 fails:** ✅ Yes

**Success criteria:**
- Auto-invocation rate improves from Option 1 result to 80%+
- Token cost stays under 500 tokens
- User feedback: "Easier to use"

---

### Option 3: Pattern Change (2-3 Weeks, High Risk)

**If root cause is:** Fundamental skill pattern limitation

**Try only if Options 1 & 2 both fail to achieve 60%+ auto-invocation**

#### Option 3a: Switch to MCP Pattern

**Recommended pattern:** Bring back MCP Server (with improvements)

**Why:**
- MCP has proven auto-invocation (HIGH confidence)
- Protocol-level integration
- Could optimize to fewer tools (9→6?) to reduce tokens

**Implementation:**
1. Create MCP server with 6-9 tools (not 9 as before)
2. Consolidate operations (merge similar ones)
3. Rich tool descriptions with trigger keywords
4. Test auto-invocation rate

**Effort:** 2-3 weeks
**Cost:** ~1,500-2,250 tokens (6-9 tools × 250 tokens)
**Risk:** High (reverts architectural decision, adds complexity)

**Trade-offs:**
- ✅ Higher auto-invocation rate (likely 90%+)
- ✅ Proven pattern
- ❌ 1,500-2,250 token overhead
- ❌ Instant context loss per call
- ❌ Maintenance burden (server process)

#### Option 3b: Hybrid CLI + Skill Pattern

**Recommended pattern:** CLI for execution, Skill for discovery

**Implementation:**
1. Create Python CLI (claude-mem command with subcommands)
2. Keep Skill for auto-invocation
3. Skill instructions call CLI instead of HTTP directly
4. CLI provides structured JSON output

**Effort:** 1-2 weeks
**Cost:** ~2,000 token startup (prime + CLI)
**Risk:** Medium (new component, coordination complexity)

**Trade-offs:**
- ✅ Maintains autonomy (Skill auto-invokes)
- ✅ Reduces per-op tokens (CLI vs curl construction)
- ✅ Dual usage (humans can use CLI directly)
- ❌ Added complexity (3 layers: Skill → CLI → HTTP)
- ❌ Installation burden
- ❌ Version sync issues

**Try only if Options 1 & 2 fail:** ⚠️ Conditional

**Likelihood needed:** **LOW (10-20%)**

**Reasoning:**
- Quick wins (Option 1) should solve weak description issue
- Pattern improvements (Option 2) should solve progressive disclosure issue
- Pattern change only if skill pattern itself is broken
- Beyond-MCP evidence suggests skills CAN work with proper implementation

---

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
    │              └─→ ✅ Problem solved, no action needed
    │
    ▼
┌─────────────────────────────────────┐
│ Step 1: Try Quick Fixes             │
│ - Improve SKILL.md description      │
│ - Add trigger keywords section      │
│ - Inline "When to use" statements   │
│ - Simplify decision guide           │
│ Effort: 2-4 hours                   │
│ Expected: 60-80% auto-invocation    │
└──────────┬──────────────────────────┘
           │
    ┌──────┴───────┐
    │              │
 SUCCESS        PARTIAL (30-60%)
  (60%+)            │
    │              │
    │              ▼
    │      ┌─────────────────────────────────────┐
    │      │ Step 2: Pattern Improvements        │
    │      │ - Adopt executable scripts          │
    │      │ - Rebalance progressive disclosure  │
    │      │ - Effort: 1-2 days                  │
    │      │ Expected: 80%+ auto-invocation      │
    │      └──────────┬──────────────────────────┘
    │                 │
    │          ┌──────┴───────┐
    │          │              │
    │       SUCCESS       FAILURE (<60%)
    │       (80%+)            │
    │          │              │
    │          │              ▼
    │          │      ┌─────────────────────────────────────┐
    │          │      │ Step 3: Pattern Change              │
    │          │      │ - Consider MCP or CLI+Skill hybrid  │
    │          │      │ - Effort: 2-3 weeks                 │
    │          │      │ Expected: 90%+ auto-invocation      │
    │          │      └─────────────────────────────────────┘
    │          │
    └──────────┴─→ ✅ Done - Measure & Monitor

Monitor ongoing auto-invocation rate
Set baseline metrics
Track improvement over time
```

---

## Recommended Starting Point

### Action: Implement Quick Fixes (Option 1)

**Specific tasks:**

1. **Rewrite SKILL.md description** (30 min)
   - Replace abstract terms with concrete nouns
   - Add user language examples
   - See "Recommended rewrite" above

2. **Add Auto-Invocation Triggers section** (15 min)
   - List 8-10 example user questions
   - List explicit trigger keywords
   - See template above

3. **Inline "When to use" statements** (60 min)
   - Add to Available Operations section
   - One statement per operation
   - User question → Operation mapping

4. **Simplify Quick Decision Guide** (15 min)
   - Reduce from 10 options to 5 common cases
   - Clear routing logic

**Total time:** 2-4 hours

**Rationale:**

1. **Highest ROI:** Low effort (hours) vs high impact (0% → 60-80% auto-invocation)
2. **Low risk:** Just markdown changes, easily reversible
3. **Directly addresses root cause:** Weak description (70% confidence)
4. **Proven pattern:** Kalshi demonstrates this works
5. **No architectural changes:** Enhances existing pattern

**Success criteria:**

Test with these questions (without mentioning "search" or "claude-mem"):
1. "What did we do last session?"
2. "Did we fix this bug before?"
3. "How did we implement authentication?"
4. "What changes were made to auth/login.ts?"
5. "What were we working on yesterday?"

**Target:** Claude auto-invokes skill for 6+ out of 10 test questions

**Measurement:**
- Clear session, ask questions naturally
- Count auto-invocations
- Compare to baseline (currently 0-10%)

**Timeline:**
- Implementation: 2-4 hours
- Testing: 1 hour
- Measurement period: 1 week of real usage
- Decision point: If <60%, proceed to Option 2

**Next steps if this works:**
1. Document improvements
2. Monitor auto-invocation rate over time
3. Gather user feedback
4. Apply learnings to other skills

**Next steps if this fails:**
1. Analyze why (which test questions failed?)
2. Proceed to Option 2 (Pattern Improvements)
3. Timeline: +1-2 days
4. Re-test with same criteria

---

## Long-Term Strategy

### Recommended Approach: Skill Pattern (Enhanced)

**Pattern choice:** Skills with Kalshi-style implementation

**Why this pattern:**

1. **Proven autonomy:** Beyond-MCP demonstrates skills CAN auto-invoke
2. **Token efficient:** ~250-500 tokens vs ~3,750 for MCP
3. **Context preserving:** No instant loss (unlike MCP)
4. **Git-shareable:** Team collaboration via commits
5. **Claude Code aligned:** Matches ecosystem patterns

**Long-term improvements:**

1. **Standardize across all skills:**
   - Concrete trigger keywords (nouns > abstractions)
   - Explicit "Auto-Invocation Triggers" section
   - Inline "When to use" statements
   - One-hop navigation (SKILL.md → execute)

2. **Adopt executable scripts for complex operations:**
   - Self-documenting (`--help` flags)
   - Easier discovery
   - Better error messages

3. **Monitor auto-invocation metrics:**
   - Track which skills get used proactively
   - Identify weak descriptions
   - Continuous improvement

4. **Create skill templates:**
   - Standardize structure
   - Include trigger keywords section
   - Inline capability lists
   - Reduce learning curve for new skills

**Migration path:** None needed (enhance, don't replace)

**Trade-offs accepted:**
- Slightly higher token cost than extreme progressive disclosure (+100-200 tokens)
- More content in SKILL.md (150-180 lines vs 97)
- Worth it for autonomy improvement (0% → 60-80% auto-invocation)

**Success metrics:**
- Auto-invocation rate: 60-80% for natural user questions
- Token cost: <500 tokens per skill startup
- User satisfaction: "I don't have to remember to use search anymore"
- Team adoption: Other developers use enhanced skills

---

## Appendix A: Test Plan

### Baseline Testing (Before Changes)

**Test questions** (ask naturally, don't mention "search" or "claude-mem"):

1. "What did we do last session?"
2. "Did we fix this bug before?"
3. "How did we implement authentication?"
4. "What changes were made to auth/login.ts?"
5. "What were we working on yesterday?"
6. "Show me past decisions about database choice"
7. "What bugs have we fixed recently?"
8. "When did we add the search feature?"
9. "Have I asked about this before?"
10. "Catch me up on recent work"

**Record for each question:**
- ✅ Auto-invoked skill (Claude used search without prompting)
- ⚠️ Partial (Claude mentioned skill but didn't invoke)
- ❌ Manual needed (Had to explicitly say "use search skill")

**Expected baseline: 0-1 out of 10 auto-invocations**

### Post-Improvement Testing (After Option 1)

**Same 10 questions, fresh session**

**Expected result: 6-8 out of 10 auto-invocations**

**Decision criteria:**
- 6+ auto-invocations (60%+) = SUCCESS, monitor ongoing
- 3-5 auto-invocations (30-50%) = PARTIAL, proceed to Option 2
- 0-2 auto-invocations (0-20%) = FAILURE, investigate why

### Real-World Testing (1 Week)

**After achieving 60%+ in controlled testing:**

**Track in production usage:**
- Total user questions about history/past work
- Auto-invocations vs manual invocations
- User feedback (explicit and implicit)
- Token cost impact

**Target metrics:**
- Auto-invocation rate: 60-80%
- Token cost increase: <200 tokens average
- User satisfaction: Positive feedback
- No regressions: Other skills still work

---

## Appendix B: Rollback Plan

### If Quick Fixes Cause Issues

**Symptoms:**
- Token cost exceeds 500 tokens
- Claude gets confused (wrong operation selected)
- User feedback negative

**Rollback actions:**
1. Revert SKILL.md to previous version (git checkout)
2. Document what failed
3. Analyze root cause
4. Try alternative approach from Option 2

**Timeline:** 15 minutes to rollback

**Data to preserve:**
- Auto-invocation test results
- User feedback
- Token cost measurements
- Error patterns

### If Pattern Change Needed (Option 3)

**Before committing to MCP or CLI:**

1. Document why Options 1 & 2 failed
2. Gather empirical evidence (test results, logs)
3. Consult with team/users
4. Estimate true cost/benefit
5. Create proof-of-concept first

**Don't commit to Option 3 unless:**
- Clear evidence that skill pattern is broken
- User impact is significant
- Team agrees on direction
- Resource allocation approved (2-3 weeks)

---

## Appendix C: Alternative Hypotheses Considered

### Hypothesis: Claude Code Bug

**Theory:** Auto-invocation mechanism is broken in Claude Code

**Evidence against:**
- Beyond-MCP claims skills auto-invoke
- Anthropic publishes skill examples
- Other users likely report if broken

**Likelihood:** LOW (10%)

**Test:** Try Kalshi skill in same environment; if it auto-invokes, claude-mem is the issue

### Hypothesis: User Expectations Wrong

**Theory:** Skills were never meant to auto-invoke; users should explicitly call them

**Evidence against:**
- Beyond-MCP README explicitly claims "Model-invoked"
- Skills documentation mentions "automatic activation"
- MCP comparison suggests autonomy as key difference

**Likelihood:** LOW (5%)

**Test:** Consult official Claude Code documentation on skill triggering

### Hypothesis: Our Test Questions Too Vague

**Theory:** Test questions don't match trigger keywords closely enough

**Evidence for:**
- "What did we do?" is very generic
- Could match many tools, not just search

**Evidence against:**
- Should be exactly what triggers "past work, previous sessions" keywords
- Kalshi works with similar generic questions

**Likelihood:** MEDIUM (30%)

**Mitigation:** Include both generic and specific questions in test suite

---

**Document Version:** 1.0
**Date:** 2025-11-10
**Status:** Ready for implementation
**Recommended action:** Proceed with Option 1 (Quick Fixes)
**Estimated timeline:** 2-4 hours implementation + 1 week testing
**Expected outcome:** 60-80% auto-invocation rate for natural user questions
