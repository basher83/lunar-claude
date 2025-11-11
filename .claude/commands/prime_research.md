# Prime Research: Beyond-MCP Architecture Analysis

**Purpose:** Analyze 4 approaches for building reusable AI agent toolsets to determine if claude-mem's current skills-based approach is optimal for proactive agent usage.

**Decision Context:** claude-mem uses skills but Claude isn't using them proactively. Should we improve the current implementation or change the pattern entirely?

**Repository:** `/Users/basher8383/dev/cloned/beyond-mcp/`

---

## Orchestrator Pattern: Parallel Verification + Synthesis

### Phase 1: Setup (Orchestrator)

1. Create output directory: `docs/research/beyond-mcp-v2/`
2. Read beyond-mcp README.md for baseline understanding
3. Read claude-mem search skill for comparison: `/Users/basher8383/dev/forked/claude-mem/plugin/skills/mem-search/SKILL.md`

### Phase 2: Spawn 4 Parallel Sub-Agents

Each sub-agent analyzes one approach focusing on **agent autonomy and discoverability**.

---

## Sub-Agent 1: MCP Server Analysis

**Analyze:** `/Users/basher8383/dev/cloned/beyond-mcp/apps/1_mcp_server/`

**Primary Files:**
- `server.py` - FastMCP implementation
- `README.md` - Section on MCP approach

**Analysis Mode: Discovery**

Your goal: Understand why MCP gets auto-invoked by Claude and what makes it discoverable.

### Key Questions

1. **Discoverability Mechanism**
   - How does Claude discover MCP tools exist?
   - What triggers MCP tool usage?
   - How visible are capabilities to the agent?

2. **Token Cost Analysis**
   - Estimate startup context load (tool descriptions)
   - How many tools are exposed?
   - Total estimated token overhead

3. **Auto-Invocation Pattern**
   - Does README provide evidence of proactive usage?
   - What makes MCP "agent-invoked" vs manual?
   - Success rate or patterns mentioned?

4. **Architecture Pattern**
   - How does server.py wrap the CLI?
   - What's the integration pattern?
   - Any relevant technical details?

### claude-mem Context

Claude-mem **removed MCP in v5.4.0** for token efficiency:
- Previous: 9 MCP tools × 250 tokens = 2,500 tokens
- Current: Skills = 250 tokens
- Savings: 2,250 tokens per session

**We won't re-add MCP**, but need to understand its discoverability mechanism.

### Analysis Template

```markdown
# MCP Server Approach Analysis

## 1. Discoverability Assessment
- **Mechanism:** [How Claude discovers tools]
- **Visibility:** [How capabilities are exposed]
- **Trigger pattern:** [What causes auto-invocation]
- **Evidence of proactive usage:** [From README or code]

## 2. Token Cost Analysis
- **Startup cost:** ~X tokens (estimated)
- **Per-operation cost:** ~X tokens
- **Total overhead:** [Assessment]
- **Scaling:** [How it grows]

## 3. Architecture Pattern
- **Implementation:** [Key technical details]
- **Integration:** [How it connects to backend]
- **Strengths:** [What it does well]
- **Weaknesses:** [Limitations]

## 4. Lessons for claude-mem
**Discoverability techniques to preserve:**
- [Technique 1]
- [Technique 2]

**What NOT to adopt:**
- [Reason 1: Token overhead]
- [Reason 2: Other issues]

## 5. Agent Autonomy Assessment
**Auto-invoked:** ✅ Yes / ❌ No
**Why:** [Explanation]
**Confidence:** [High/Medium/Low based on evidence]
```

**Output:** `docs/research/beyond-mcp/01-mcp-server.md`

---

## Sub-Agent 2: CLI Analysis

**Analyze:** `/Users/basher8383/dev/cloned/beyond-mcp/apps/2_cli/`

**Primary Files:**
- `kalshi_cli/cli.py` - Main CLI implementation (553 lines)
- `kalshi_cli/modules/client.py` - HTTP client
- `README.md` - Section on CLI approach

**Analysis Mode: Verification + Pattern Extraction**

Your goal: Understand if CLI improves agent autonomy and whether it could enhance claude-mem's current pattern.

### Key Questions

1. **Agent Autonomy**
   - Can CLI be auto-invoked by Claude?
   - Does README mention "prime prompt" pattern? (line ~54)
   - How does Claude discover CLI commands exist?
   - Manual vs automatic usage pattern?

2. **Token Efficiency**
   - README claims "half context vs MCP" - verify this
   - Estimate token cost when Claude uses CLI
   - Progressive disclosure possible with CLI?

3. **Integration Pattern**
   - How does CLI wrap the API?
   - Single source of truth architecture?
   - Dual output modes (human + JSON)?

4. **Hybrid Potential**
   - README mentions CLI + Skills hybrid
   - Could this improve claude-mem's current pattern?
   - What would integration look like?

### claude-mem Context

Current pattern:
- Skills use curl + Bash to call HTTP API
- Each operation constructs curl from documentation
- Estimated ~680-730 tokens per search operation

Question: Would CLI reduce overhead or improve autonomy?

### Analysis Template

```markdown
# CLI Approach Analysis

## 1. Agent Autonomy Assessment
- **Auto-invoked:** ✅/❌ [Evidence from README/code]
- **Discovery mechanism:** [How Claude learns about CLI]
- **Prime prompt pattern:** [If mentioned, how it works]
- **Manual vs automatic:** [Classification]

## 2. Token Efficiency
- **Startup cost:** ~X tokens
- **Per-operation cost:** ~X tokens
- **vs MCP comparison:** [README claims verified?]
- **Progressive disclosure:** [Possible/Not possible]

## 3. Implementation Pattern
- **Architecture:** [How it wraps API]
- **Commands:** [How many, structure]
- **Output modes:** [Human/JSON details]
- **Single source of truth:** [How maintained]

## 4. claude-mem Integration Analysis
**Current:** Skills + curl + Bash (manual HTTP construction)

**With CLI:**
- Would it improve autonomy? [Assessment]
- Token cost impact? [Better/Worse/Same]
- Implementation effort? [Estimate]
- Worth it? [Yes/No with reasoning]

## 5. Hybrid Pattern Assessment
**CLI + Skills approach:**
- How would it work? [Description]
- Benefits over current? [List]
- Drawbacks? [List]
- Recommendation? [Yes/No with reasoning]

## 6. Agent Autonomy Assessment
**Auto-invoked:** ✅ Yes / ❌ No
**Why:** [Explanation]
**Confidence:** [High/Medium/Low based on evidence]
```

**Output:** `docs/research/beyond-mcp/02-cli.md`

---

## Sub-Agent 3: File System Scripts Analysis

**Analyze:** `/Users/basher8383/dev/cloned/beyond-mcp/apps/3_file_system_scripts/`

**Primary Files:**
- `scripts/status.py` - Example script (157 lines)
- `scripts/search.py` - Search with caching (465 lines)
- `scripts/markets.py` - Browse markets (254 lines)
- `README.md` - Section on scripts approach

**Analysis Mode: Pattern Extraction + Discoverability Analysis**

Your goal: Understand progressive disclosure vs discoverability tradeoff.

### Key Questions

1. **Progressive Disclosure Mechanism**
   - How many scripts total? (~10)
   - Lines per script? (~200-300 claimed)
   - How does Claude load only what's needed?
   - Token cost per script?

2. **Discoverability Challenge**
   - How does Claude know scripts exist?
   - Does low context load hurt auto-invocation?
   - Hidden capabilities problem?

3. **Implementation Pattern**
   - Self-contained scripts (no dependencies)?
   - Code duplication? (claimed in README)
   - HTTP client embedded in each?

4. **Agent Autonomy**
   - Can scripts be auto-invoked?
   - Or always manual (agent must choose to read)?
   - Evidence of usage pattern?

### claude-mem Context

Claude-mem already uses progressive disclosure:
- Skills have operation docs (~200 tokens each)
- Only loaded when needed
- Question: Is this WHY Claude doesn't use it proactively?

**Critical question:** Does hiding capabilities reduce discoverability?

### Analysis Template

```markdown
# File System Scripts Approach Analysis

## 1. Progressive Disclosure Pattern
- **Script count:** [Number]
- **Lines per script:** [Measured from samples]
- **Token cost per script:** ~X tokens (estimated)
- **Loading mechanism:** [How Claude loads them]

## 2. Discoverability vs Token Tradeoff
**The Core Tension:**
- Low context load = token efficient ✅
- Hidden capabilities = low discoverability ❌

**Assessment:**
- Can Claude discover scripts proactively? [Yes/No/Partial]
- Evidence: [From README or implementation]
- Tradeoff worth it? [Analysis]

## 3. Implementation Details
- **Self-contained:** [Verified from code]
- **Code duplication:** [Extent, examples]
- **HTTP client:** [How embedded]
- **Dependencies:** [Listed in scripts]

## 4. claude-mem Comparison
**Current claude-mem pattern:**
- Skills with operations/ docs
- Progressive disclosure active
- Claude loads operations on-demand

**Scripts pattern:**
- Similar progressive disclosure
- Executable vs documentation
- Token cost comparison

**Key difference:** [What stands out]

## 5. Discoverability Problem Hypothesis
**Theory:** Progressive disclosure reduces proactive usage

**Evidence:**
- [From scripts approach]
- [From claude-mem current behavior]

**Conclusion:** [Is this the root cause?]

## 6. Agent Autonomy Assessment
**Auto-invoked:** ✅ Yes / ❌ No
**Why:** [Explanation]
**Confidence:** [High/Medium/Low based on evidence]
```

**Output:** `docs/research/beyond-mcp/03-file-scripts.md`

---

## Sub-Agent 4: Skill Analysis (CRITICAL)

**Analyze:** `/Users/basher8383/dev/cloned/beyond-mcp/apps/4_skill/`

**Primary Files:**
- `.claude/skills/kalshi-markets/SKILL.md` - Skill definition (72 lines)
- `.claude/skills/kalshi-markets/scripts/*.py` - Embedded scripts
- `README.md` - Section on Skills approach

**Compare to:**
- `/Users/basher8383/dev/forked/claude-mem/plugin/skills/search/SKILL.md` - Current implementation

**Analysis Mode: Comparative Analysis**

Your goal: Identify why one skill might be auto-invoked while another isn't.

### Key Questions

1. **Skill Description Quality**
   - Kalshi-markets triggers: What keywords?
   - Claude-mem triggers: What keywords?
   - Capability visibility comparison
   - Which is more discoverable?

2. **Implementation Pattern**
   - Kalshi uses embedded scripts (10 scripts)
   - Claude-mem uses operations docs
   - Which approach is better for autonomy?

3. **Auto-Invocation Evidence**
   - README claims: "Model-invoked" - evidence?
   - How does "description triggers automatic activation"?
   - Success rate? Usage patterns?

4. **Progressive Disclosure Balance**
   - How much to show in SKILL.md frontmatter?
   - How much to hide in subdirectories?
   - Sweet spot for discoverability?

### Critical Comparison Task

**Read both skills. Answer:**
1. Is claude-mem description too vague?
2. Are trigger keywords missing?
3. Is capability visibility too low?
4. What specific improvements would help?

### Analysis Template

```markdown
# Skill Approach Analysis

## 1. Skill Description Comparison

### Kalshi-Markets Skill (beyond-mcp)
**Description:** [Quote from SKILL.md]
**Trigger keywords:** [List identified]
**Capability visibility:** [High/Medium/Low]
**Lines in SKILL.md:** [Count]

### Claude-Mem Search Skill (current)
**Description:** [Quote from SKILL.md]
**Trigger keywords:** [List identified]
**Capability visibility:** [High/Medium/Low]
**Lines in SKILL.md:** [Count]

### Comparison
**Winner for discoverability:** [Which and why]
**Key differences:** [List]
**Missing from claude-mem:** [Specific gaps]

## 2. Implementation Pattern Analysis

**Kalshi pattern:**
- SKILL.md structure: [Overview]
- Scripts approach: [How integrated]
- Progressive disclosure: [How balanced]

**Claude-mem pattern:**
- SKILL.md structure: [Overview]
- Operations docs: [How organized]
- Progressive disclosure: [How balanced]

**Better for autonomy:** [Which and why]

## 3. Auto-Invocation Evidence

**README claims:** "Model-invoked" and "Claude autonomously decides"

**Evidence found:**
- [Specific examples from README]
- [Code patterns that support this]
- [Or lack of evidence]

**Confidence in claim:** [High/Medium/Low]

## 4. Root Cause Analysis: Why Claude Doesn't Use claude-mem

### Hypothesis A: Weak Description
**Evidence:** [Specific description issues]
**Fix effort:** [Low - rewrite SKILL.md]
**Likelihood:** [High/Medium/Low]

### Hypothesis B: Progressive Disclosure Tradeoff
**Evidence:** [Too much hidden]
**Fix effort:** [Medium - rebalance visibility]
**Likelihood:** [High/Medium/Low]

### Hypothesis C: Pattern Limitation
**Evidence:** [Skills inherently limited]
**Fix effort:** [High - change pattern]
**Likelihood:** [High/Medium/Low]

**Most likely root cause:** [A/B/C with reasoning]

## 5. Specific Recommendations for claude-mem

### Quick Wins (Hours)
- [ ] Improve trigger keywords: [Specific suggestions]
- [ ] Enhance description: [Specific wording]
- [ ] Surface capabilities: [What to make visible]

### Medium Effort (Days)
- [ ] Adopt scripts pattern: [How]
- [ ] Rebalance progressive disclosure: [What to change]

### Large Changes (Weeks)
- [ ] Change pattern entirely to [X]

**Recommended starting point:** [Specific action]

## 6. Agent Autonomy Assessment
**Auto-invoked:** ✅ Yes / ❌ No
**Why:** [Explanation based on README evidence]
**Confidence:** [High/Medium/Low based on evidence]
```

**Output:** `docs/research/beyond-mcp/04-skill.md`

---

## Phase 3: Monitor Completion

**Orchestrator action:**
- Check every 15 seconds for file completion
- When all 4 analysis files exist, proceed to synthesis

**Status messages:**
```bash
[15s] Waiting for sub-agents... (0/4 complete)
[30s] Waiting for sub-agents... (2/4 complete)
[45s] All sub-agents complete. Beginning synthesis...
```

---

## Phase 4: Synthesis (Orchestrator Reads + Compares)

### Read All 4 Reports

1. Read `docs/research/beyond-mcp/01-mcp-server.md`
2. Read `docs/research/beyond-mcp/02-cli.md`
3. Read `docs/research/beyond-mcp/03-file-scripts.md`
4. Read `docs/research/beyond-mcp/04-skill.md`

### Create Comparison Matrix

**File:** `docs/research/beyond-mcp/comparison-matrix.md`

**Structure:**

```markdown
# Beyond-MCP Approaches: Comparison Matrix

## Agent Autonomy (Primary Concern)

| Approach | Auto-Invoked | Discovery Mechanism | Evidence | Confidence |
|----------|--------------|---------------------|----------|------------|
| MCP Server | [From analysis] | [How] | [Evidence] | [H/M/L] |
| CLI | [From analysis] | [How] | [Evidence] | [H/M/L] |
| Scripts | [From analysis] | [How] | [Evidence] | [H/M/L] |
| Skill | [From analysis] | [How] | [Evidence] | [H/M/L] |

## Token Efficiency

| Approach | Startup Cost | Per-Operation | Scaling | vs claude-mem Current |
|----------|--------------|---------------|---------|----------------------|
| MCP Server | ~X tokens | ~X tokens | [Pattern] | [Comparison] |
| CLI | ~X tokens | ~X tokens | [Pattern] | [Comparison] |
| Scripts | ~X tokens | ~X tokens | [Pattern] | [Comparison] |
| Skill | ~X tokens | ~X tokens | [Pattern] | [Comparison] |

## Implementation Effort

| Approach | Complexity | Stack Alignment | Breaking Changes | Timeline |
|----------|------------|-----------------|------------------|----------|
| MCP Server | [H/M/L] | [Assessment] | [Yes/No] | [Estimate] |
| CLI | [H/M/L] | [Assessment] | [Yes/No] | [Estimate] |
| Scripts | [H/M/L] | [Assessment] | [Yes/No] | [Estimate] |
| Skill | [H/M/L] | [Assessment] | [Yes/No] | [Estimate] |

## Discoverability vs Token Cost Tradeoff

[Analysis of the core tension between being visible to Claude vs token efficiency]

## Key Findings Summary

1. **Most auto-invoked approach:** [Which] because [reasons]
2. **Most token efficient:** [Which] because [reasons]
3. **Best for claude-mem context:** [Which] because [reasons]
4. **Easiest to implement:** [Which] because [reasons]
```

---

## Phase 5: Decision Framework

**File:** `docs/research/beyond-mcp/decision-framework.md`

**Structure:**

```markdown
# Decision Framework: claude-mem Toolset Strategy

## Problem Statement

Claude isn't using claude-mem search skill proactively.

**Question:** Should we improve current implementation or change the pattern?

---

## Root Cause Analysis

Based on 4 approach analyses:

### Finding 1: Why Claude Doesn't Use claude-mem Proactively

**Most likely cause:** [From synthesis]

**Evidence:**
- [From Sub-Agent 4 comparison]
- [From other approaches]
- [Pattern identified]

**Confidence:** [High/Medium/Low]

### Finding 2: Discoverability Mechanisms That Work

**From MCP:** [Lessons learned]
**From CLI:** [Lessons learned]
**From Scripts:** [Lessons learned]
**From Skills:** [Lessons learned]

**Key insight:** [What makes approaches discoverable]

### Finding 3: Token Cost vs Autonomy Tradeoff

**The Tension:**
- High visibility → High tokens → Auto-invoked ✅
- Low visibility → Low tokens → Manual only ❌

**Sweet spot:** [Where is it?]

---

## Recommendations (Effort-Based)

### Option 1: Quick Fixes (Hours, Low Risk)

**If root cause is:** Weak skill description

**Actions:**
1. Rewrite claude-mem SKILL.md description
   - Add trigger keywords: [Specific suggestions from analysis]
   - Increase capability visibility: [Specific changes]
   - Example improvements: [Concrete wording]

2. Test proactive usage
   - Clear session, try relevant prompts
   - Measure: Does Claude invoke skill?

**Effort:** 1-2 hours
**Cost:** Zero (just markdown)
**Risk:** None (easily reversible)

**Try this first:** ✅ Yes / ❌ No
**Reasoning:** [From analysis]

### Option 2: Pattern Improvements (Days, Medium Risk)

**If root cause is:** Progressive disclosure balance

**Actions:**
1. Surface more capabilities in SKILL.md
   - Reduce hidden content
   - Increase frontmatter visibility
   - Specific changes: [From analysis]

2. Adopt [scripts/other pattern] elements
   - [Specific recommendations]
   - Integration approach: [Details]

**Effort:** 2-3 days
**Cost:** Some token overhead
**Risk:** May reduce token efficiency gains

**Try if Option 1 fails:** ✅ Yes / ❌ No
**Reasoning:** [From analysis]

### Option 3: Pattern Change (Weeks, High Risk)

**If root cause is:** Fundamental pattern limitation

**Recommended pattern:** [From analysis - which approach]

**Actions:**
1. [Specific implementation steps]
2. [Migration plan]
3. [Testing approach]

**Effort:** 2-3 weeks
**Cost:** [Token impact, maintenance burden]
**Risk:** Breaking changes, may not solve problem

**Try only if Options 1 & 2 fail:** ✅ Yes / ❌ No
**Reasoning:** [From analysis]

---

## Decision Tree

```
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
│ Step 1: Try Quick Fixes             │
│ - Improve SKILL.md description      │
│ - Add trigger keywords              │
│ - Effort: Hours                     │
└──────────┬──────────────────────────┘
           │
    ┌──────┴───────┐
    │              │
 WORKS         DOESN'T WORK
    │              │
    │              ▼
    │      ┌─────────────────────────────────────┐
    │      │ Step 2: Pattern Improvements        │
    │      │ - Rebalance progressive disclosure  │
    │      │ - Adopt elements from [approach]    │
    │      │ - Effort: Days                      │
    │      └──────────┬──────────────────────────┘
    │                 │
    │          ┌──────┴───────┐
    │          │              │
    │       WORKS         DOESN'T WORK
    │          │              │
    │          │              ▼
    │          │      ┌─────────────────────────────────────┐
    │          │      │ Step 3: Pattern Change              │
    │          │      │ - Implement [approach] from scratch │
    │          │      │ - Effort: Weeks                     │
    │          │      └─────────────────────────────────────┘
    │          │
    └──────────┴─→ Done ✅
```bash

---

## Recommended Starting Point

**Action:** [Specific recommendation from analysis]

**Rationale:** [Why this is best first step]

**Success Criteria:**
- [ ] Claude invokes skill without explicit prompting
- [ ] Maintains token efficiency (within X% of current)
- [ ] Works across different query types
- [ ] Repeatable behavior

**Timeline:** [Estimate]

**Next steps if this works:** [Follow-up actions]

**Next steps if this fails:** [Escalation path]

---

## Long-Term Strategy

Based on analysis, recommended approach for claude-mem toolset:

**Pattern:** [Which approach from beyond-mcp]

**Why:** [Reasoning from analyses]

**Migration path:** [If different from current]

**Trade-offs accepted:** [Token cost, maintenance, etc.]
```

---

## Phase 6: Report to User

**Orchestrator final message:**

```bash
✅ Analysis complete.

📊 Files created:
   - docs/research/beyond-mcp/01-mcp-server.md
   - docs/research/beyond-mcp/02-cli.md
   - docs/research/beyond-mcp/03-file-scripts.md
   - docs/research/beyond-mcp/04-skill.md
   - docs/research/beyond-mcp/comparison-matrix.md
   - docs/research/beyond-mcp/decision-framework.md

🎯 Key Findings:
   - Root cause identified: [Summary from decision-framework.md]
   - Recommended action: [Quick wins / Pattern change / Keep current]
   - Effort estimate: [Hours / Days / Weeks]

📋 Next Steps:
   1. Review decision-framework.md for detailed recommendations
   2. Try suggested quick fixes first (if applicable)
   3. Measure: Does Claude use skill more proactively?

Decision framework ready for your review.
```

---

## Orchestrator Execution Notes

**Context Management:**
- Orchestrator stays awake throughout (maintains context)
- Peak context: ~35k tokens (after reading 4 reports + synthesis)
- Well within limits ✅

**Parallel Execution:**
- All 4 sub-agents run simultaneously
- Estimated completion: 3-5 minutes
- No dependencies between agents

**Output Quality:**
- Each analysis follows template for consistency
- Comparable structure enables synthesis
- Decision-focused (not just informational)

**Error Handling:**
- If sub-agent fails: Note gap, proceed with 3 analyses
- If file missing: Report partial results
- If synthesis fails: Return individual analyses

---

## Success Criteria

Analysis is successful if it answers:

1. ✅ Why isn't Claude using claude-mem proactively?
2. ✅ Which approach from beyond-mcp has best autonomy?
3. ✅ Should we improve current pattern or change it?
4. ✅ What's the lowest-effort fix to try first?
5. ✅ Is the effort worth the potential improvement?

**Ready to execute:** This command is fully autonomous. Run `/prime_research` to begin analysis.
