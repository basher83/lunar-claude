# Context Window Protection

> "200k context window is plenty. You're just stuffing a single agent with too much work. Don't force your agent to context switch."

Context window protection is about managing your agent's most precious resource: attention. A focused agent is a performant agent.

## The Core Problem

**Every engineer hits this wall:**

```text
Agent starts:  10k tokens (5% used)
           ↓
After exploration:  80k tokens (40% used)
           ↓
After planning:  120k tokens (60% used)
           ↓
During implementation:  170k tokens (85% used) ⚠️
           ↓
Context explodes:  195k tokens (98% used) ❌
           ↓
Agent performance degrades, fails, or times out
```

**The realization:** More context ≠ better performance. Too much context = cognitive overload.

## The R&D Framework

There are only two ways to manage your context window:

```text
R - REDUCE
└─→ Minimize what enters the context window

D - DELEGATE
└─→ Move work to other agents' context windows
```

**Everything else is a tactic implementing R or D.**

## The Four Levels of Context Protection

### Level 1: Beginner - Reduce Waste

**Focus:** Stop wasting tokens on unused resources

#### Tactic 1: Eliminate Default MCP Servers

**Problem:**

```bash
# Default mcp.json
{
  "mcpServers": {
    "firecrawl": {...},   # 6k tokens
    "github": {...},      # 8k tokens
    "postgres": {...},    # 5k tokens
    "redis": {...}        # 5k tokens
  }
}
# Total: 24k tokens always loaded (12% of 200k window!)
```

**Solution:**

```bash
# Option 1: Delete default mcp.json entirely
rm .claude/mcp.json

# Option 2: Load selectively
claude-mcp-config --strict specialized-configs/firecrawl-only.json
# Result: 4k tokens instead of 24k (83% reduction)
```

#### Tactic 2: Minimize CLAUDE.md

**Before:**

```markdown
# CLAUDE.md (23,000 tokens = 11.5% of window)
- 500 lines of API documentation
- 300 lines of deployment procedures
- 1,500 lines of coding standards
- Architecture diagrams
- Always loaded, whether relevant or not
```

**After:**

```markdown
# CLAUDE.md (500 tokens = 0.25% of window)
# Only universal essentials

- Fenced code blocks MUST have language
- Use rg instead of grep
- ALWAYS use set -euo pipefail
```

**Rule:** Only include what you're 100% sure you want loaded 100% of the time.

#### Tactic 3: Disable Autocompact Buffer

**Problem:**

```bash
/context

# Output:
autocompact buffer: 22%  ⚠️ (44k tokens gone!)
messages: 51%
system_tools: 8%
---
Total available: 78% (should be 100%)
```

**Solution:**

```bash
/config
# Set: autocompact = false

# Now:
/context
# Output:
messages: 51%
system_tools: 8%
custom_agents: 2%
---
Total available: 91% ✅ (reclaimed 22%!)
```

**Impact:** Reclaims 40k+ tokens immediately.

### Level 2: Intermediate - Dynamic Loading

**Focus:** Load what you need, when you need it

#### Tactic 4: Context Priming

**Replace static CLAUDE.md with task-specific `/prime` commands**

```markdown
# .claude/commands/prime.md
# General codebase context (2k tokens)
Read README, understand structure, report findings

# .claude/commands/prime-feature.md
# Feature development context (3k tokens)
Read feature requirements, understand dependencies, plan implementation

# .claude/commands/prime-api.md
# API work context (4k tokens)
Read API docs, understand endpoints, review integration patterns
```

**Usage pattern:**

```bash
# Starting feature work
/prime-feature

# vs. having 23k tokens always loaded
```

**Savings:** 20k tokens (87% reduction)

#### Tactic 5: Sub-Agent Delegation

**Problem:** Primary agent doing parallel work fills its own context

```text
Primary Agent tries to do:
├── Web scraping (15k tokens)
├── Documentation fetch (12k tokens)
├── Data analysis (10k tokens)
└── Synthesis (5k tokens)
= 42k tokens in one agent
```

**Solution:** Delegate to sub-agents with isolated contexts

```text
Primary Agent (9k tokens):
├→ Sub-Agent 1: Web scraping (15k tokens, isolated)
├→ Sub-Agent 2: Docs fetch (12k tokens, isolated)
└→ Sub-Agent 3: Analysis (10k tokens, isolated)

Total work: 46k tokens
Primary agent context: Only 9k tokens ✅
```

**Example:**

```bash
/load-ai-docs

# Agent spawns 10 sub-agents for web scraping
# Each scrape: ~3k tokens
# Total work: 30k tokens
# Primary agent context: Still only 9k tokens
# Savings: 21k tokens protected
```

**Key insight:** Sub-agents use system prompts (not user prompts), keeping their context isolated from primary.

### Level 3: Advanced - Multi-Agent Handoff

**Focus:** Chain agents together without context explosion

#### Tactic 6: Context Bundles

**Problem:** Agent 1's context explodes (180k tokens). Need to hand off to fresh Agent 2 without full replay.

**Solution:** Bundle 60-70% of essential context

```markdown
# context-bundle-2025-01-05-<session-id>.md

## Context Bundle
Created: 2025-01-05 14:30
Source Agent: agent-abc123

## Initial Setup
/prime-feature

## Read Operations (deduplicated)
- src/api/endpoints.ts
- src/components/Auth.tsx
- config/env.ts

## Key Findings
- Auth system uses JWT
- API has 15 endpoints
- Config needs migration

## User Prompts (summarized)
1. "Implement OAuth2 flow"
2. "Add refresh token logic"

[Excluded: full write operations, detailed read contents, tool execution details]
```

**Usage:**

```bash
# Agent 1: Context exploding at 180k
# Automatic bundle saved

# Agent 2: Fresh start (10k base)
/loadbundle /path/to/context-bundle-<timestamp>.md
# Agent 2 now has 70% of Agent 1's context in ~15k tokens

# Total: 25k tokens vs. 180k (86% reduction)
```

#### Tactic 7: Composable Workflows (Scout-Plan-Build)

**Problem:** Single agent searching + planning + building = context explosion

```text
Monolithic Agent:
├── Search codebase: 40k tokens
├── Read files: 60k tokens
├── Plan changes: 20k tokens
├── Implement: 30k tokens
├── Test: 15k tokens
└── Total: 165k tokens (83% used!)
```

**Solution:** Break into composable steps that delegate

```text
/scout-plan-build workflow:

Step 1: /scout (delegates to 4 parallel sub-agents)
├→ Sub-agents search codebase: 4 × 15k = 60k total
├→ Output: relevant-files.md (5k tokens)
└→ Primary agent context: unchanged

Step 2: /plan-with-docs
├→ Reads relevant-files.md: 5k tokens
├→ Scrapes docs: 8k tokens
├→ Creates plan: 3k tokens
└→ Total added: 16k tokens

Step 3: /build
├→ Reads plan: 3k tokens
├→ Implements: 30k tokens
└→ Total added: 33k tokens

Final primary agent context: 10k + 16k + 33k = 59k tokens
Savings: 106k tokens (64% reduction)
```

**Why this works:** Scout step offloads searching from planner (R&D: Reduce + Delegate)

### Level 4: Agentic - Out-of-Loop Systems

**Focus:** Agents working autonomously while you're AFK

#### Tactic 8: Focused Agents (One Agent, One Task)

**Anti-pattern:**

```text
Super Agent (trying to do everything):
├── API development
├── UI implementation
├── Database migrations
├── Testing
├── Documentation
├── Deployment
└── Context: 170k tokens (85% used)
```

**Pattern:**

```text
Focused Agent Fleet:
├── Agent 1: API only (30k tokens)
├── Agent 2: UI only (35k tokens)
├── Agent 3: DB only (20k tokens)
├── Agent 4: Tests only (25k tokens)
├── Agent 5: Docs only (15k tokens)
└── Each agent: <35k tokens (max 18% per agent)
```

**Principle:** "A focused engineer is a performant engineer. A focused agent is a performant agent."

#### Tactic 9: Deletable Agents

**Pattern:**

```bash
# Create agent for specific task
/create-agent docs-writer "Document frontend components"

# Agent completes task (used 30k tokens)

# DELETE agent immediately
/delete-agent docs-writer

# Result: 30k tokens freed for next agent
```

**Lifecycle:**

```text
1. Create agent → Task-specific context loaded
2. Agent works → Context grows to completion
3. Agent completes → Context maxed out
4. DELETE agent → Context freed
5. Create new agent → Fresh start
6. Repeat
```

**Engineering analogy:** "The best code is no code at all. The best agent is a deleted agent."

#### Tactic 10: Background Agent Delegation

**Problem:** You're in the loop, waiting for agent to finish long task

**Solution:** Delegate to background agent, continue working

```bash
# In-loop (you wait, your context stays open)
/implement-feature "Build auth system"
# Your terminal blocked for 20 minutes
# Context accumulates: 150k tokens

# Out-of-loop (you continue working)
/background "Build auth system" \
  --model opus \
  --report agents/auth-report.md

# Background agent works independently
# Your terminal freed immediately
# Background agent context isolated
# You get notified when complete
```

**Context protection:**

- Primary agent: 10k tokens (just manages job queue)
- Background agent: 150k tokens (isolated, will be deleted)
- Your interactive session: 10k tokens (protected)

#### Tactic 11: Orchestrator Sleep Pattern

**Problem:** Orchestrator observing all agent work = context explosion

```text
Orchestrator watches everything:
├── Scout 1 work: 15k tokens observed
├── Scout 2 work: 15k tokens observed
├── Scout 3 work: 15k tokens observed
├── Planner work: 25k tokens observed
├── Builder work: 35k tokens observed
└── Orchestrator context: 105k tokens
```

**Solution:** Orchestrator sleeps while agents work

```text
Orchestrator pattern:
1. Create scouts → 3k tokens (commands only)
2. SLEEP (not observing)
3. Wake every 15s, check status → 1k tokens
4. Scouts complete, read outputs → 5k tokens
5. Create planner → 2k tokens
6. SLEEP (not observing)
7. Wake every 15s, check status → 1k tokens
8. Planner completes, read output → 3k tokens
9. Create builder → 2k tokens
10. SLEEP (not observing)

Orchestrator final context: 17k tokens ✅
vs. 105k if watching everything (84% reduction)
```

**Key principle:** Orchestrator wakes to coordinate, sleeps while agents work.

## Monitoring Context Health

### The /context Command

```bash
/context

# Healthy agent (beginner level):
messages: 8%
system_tools: 5%
custom_agents: 2%
---
Total used: 15%  ✅ (85% free)

# Warning (intermediate):
messages: 45%
mcp_tools: 18%
system_tools: 5%
---
Total used: 68%  ⚠️ (32% free, approaching limits)

# Danger (needs intervention):
messages: 72%
mcp_tools: 24%
system_tools: 5%
---
Total used: 101%  ❌ (context overflow!)
```

### Success Metrics by Level

| Level | Target Context Free | What This Enables |
|-------|---------------------|-------------------|
| Beginner | 85-90% | Basic tasks without running out |
| Intermediate | 60-75% | Complex tasks with breathing room |
| Advanced | 40-60% | Multi-step workflows without overflow |
| Agentic | Per-agent 60-80% | Fleet of focused agents |

### Warning Signs

**Your context window is in danger when:**

❌ **Single agent exceeds 150k tokens**

- Solution: Split work across multiple agents

❌ **Agent needs to read >20 files**

- Solution: Use scout agents to find relevant subset

❌ **`/context` shows >80% used**

- Solution: Start fresh agent, use context bundles

❌ **Agent gets slower/less accurate**

- Solution: Check context usage, delegate to sub-agents

❌ **Autocompact buffer active**

- Solution: Disable it, reclaim 20%+ tokens

## Context Window Hard Limits

> "Context window is a hard limit. We have to respect this and work around it."

### The Reality

```text
Claude Opus 200k limit:
├── System prompt: ~8k tokens (4%)
├── Available tools: ~5k tokens (2.5%)
├── MCP servers: 0-24k tokens (0-12%)
├── CLAUDE.md: 0-23k tokens (0-11.5%)
├── Custom agents: ~2k tokens (1%)
└── Available for work: 138-185k tokens (69-92.5%)

Best case (optimized): 185k available
Worst case (unoptimized): 138k available
Difference: 47k tokens (25% of total capacity!)
```

### Real Example from the Field

> "We were 14% away from exploding our context in our scout-plan-build workflow."

```text
Scout-Plan-Build execution:
├── Base context: 15k tokens
├── Scout work (4 sub-agents): +40k tokens
├── Planner work: +35k tokens
├── Builder work: +80k tokens
└── Total: 170k tokens

With autocompact buffer (22%):
170k / 0.78 = 218k tokens
❌ Exceeds 200k limit by 18k (9% overflow)

Without autocompact buffer:
170k / 1.0 = 170k tokens
✅ Within limits with 30k buffer (15% free)
```

**Lesson:** Every percentage point matters when approaching limits.

## Common Context Explosion Patterns

### Pattern 1: The Sponge Agent

**Symptoms:**

- Agent reads entire codebase
- Opens 50+ files
- Context grows 10k tokens every few minutes

**Cause:** No filtering strategy

**Fix:**

```bash
# Before: Agent reads everything
Agent: "Analyzing codebase..."
[reads 100 files = 150k tokens]

# After: Scout first
/scout "Find files related to authentication"
# Scout outputs: 5 relevant files
Agent reads only those 5 files = 8k tokens
```

### Pattern 2: The Accumulator

**Symptoms:**

- Long conversation
- Many tool calls
- Context steadily grows to limit

**Cause:** Not resetting agent between phases

**Fix:**

```bash
# Phase 1: Exploration
[Agent explores, context hits 120k]

# Phase 2: Implementation
# ❌ Bad: Continue same agent (will overflow)
# ✅ Good: New agent with context bundle

/loadbundle context-from-phase-1.md
# Fresh agent (15k) + bundle (20k) = 35k tokens
# Ready for implementation without overflow
```

### Pattern 3: The Observer

**Symptoms:**

- Orchestrator context growing rapidly
- Watching all sub-agent work
- Can't coordinate more than 2-3 agents

**Cause:** Not using sleep pattern

**Fix:**

```python
# ❌ Bad: Orchestrator watches everything
for agent in agents:
    result = orchestrator.watch_agent_work(agent)  # Observes all work
    orchestrator.context += result  # Context explodes

# ✅ Good: Orchestrator sleeps
for agent in agents:
    orchestrator.create_and_command(agent)
    orchestrator.sleep()  # Not observing

orchestrator.wake_and_check_status()  # Only reads summaries
```

## The "200k is Plenty" Principle

> "I'm super excited for larger effective context windows, but 200k context window is plenty. You're just stuffing a single agent with too much work."

**The mindset shift:**

```text
Beginner thinking:
"I need a bigger context window"
"If only I had 500k tokens..."
"My task is too complex for 200k"

Expert thinking:
"I need better context management"
"I'm overloading a single agent"
"I should split this across focused agents"
```

**The truth:** Most context explosions are design problems, not capacity problems.

### Why 200k is Sufficient

**With proper protection:**

```text
Task: Refactor authentication across 50-file codebase

Approach 1 (Single Agent - fails):
├── Agent reads 50 files: 75k tokens
├── Agent plans changes: 20k tokens
├── Agent implements: 80k tokens
├── Agent tests: 30k tokens
└── Total: 205k tokens ❌ (overflow by 5k)

Approach 2 (Multi-Agent - succeeds):
├── Scout finds relevant 10 files: 15k tokens
├── Planner creates strategy: 20k tokens (new agent)
├── Builder 1 (auth logic): 35k tokens (new agent)
├── Builder 2 (UI changes): 30k tokens (new agent)
├── Tester verifies: 25k tokens (new agent)
└── Max per agent: 35k tokens ✅ (all within limits)
```

## Integration with Other Patterns

Context window protection enables:

**Progressive Disclosure:**

- Reduces: Minimal static context
- Enables: Dynamic loading via priming

**Core 4 Management:**

- Protects: Context (pillar #1)
- Enables: Better model/prompt/tools choices

**Orchestration:**

- Requires: Context protection (orchestrator sleep)
- Enables: Fleet management without overflow

**Observability:**

- Monitors: Context usage via hooks
- Prevents: Unnoticed context explosion

## Key Principles

1. **Reduce and Delegate** - The only two strategies that matter

2. **A focused agent is a performant agent** - Single-purpose beats multi-purpose

3. **Agents are deletable** - Free context by removing completed agents

4. **200k is plenty** - Context explosions are design problems

5. **Monitor constantly** - `/context` command is your best friend

6. **Orchestrators must sleep** - Don't observe all agent work

7. **Context bundles over full replay** - 70% of context in 10% of tokens

## Source Attribution

**Primary sources:**

- Elite Context Engineering (R&D framework, 4 levels, all tactics)
- Claude 2.0 (autocompact buffer, hard limits, scout-plan-build)

**Supporting sources:**

- One Agent to Rule Them All (orchestrator sleep, 200k principle, deletable agents)
- Sub-Agents (sub-agent delegation, context isolation)

**Key quotes:**

- "200k context window is plenty. You're just stuffing a single agent with too much work." (One Agent)
- "A focused agent is a performant agent." (Elite Context Engineering)
- "We were 14% away from exploding our context." (Claude 2.0)
- "There are only two ways to manage your context window: R and D." (Elite Context Engineering)

## Related Documentation

- [Progressive Disclosure](../reference/progressive-disclosure.md) - Context loading strategies
- [Orchestrator Pattern](orchestrator-pattern.md) - Fleet management requiring protection
- [Evolution Path](../workflows/evolution-path.md) - Progression through protection levels
- [Core 4 Framework](../reference/core-4-framework.md) - Context as first pillar

---

**Remember:** Context window management separates beginners from experts. Master it, and you can scale infinitely with focused agents.
