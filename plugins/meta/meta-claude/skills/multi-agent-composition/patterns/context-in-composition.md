# Context in Composition

**Strategic framework for managing context when composing multi-agent systems.**

## The Core Problem

Context window is your most precious resource when composing multiple agents. A focused agent is a performant agent.

**The Reality:**

```text
Single agent doing everything:
├── Context explodes to 150k+ tokens
├── Performance degrades
└── Eventually fails or times out

Multi-agent composition:
├── Each agent: <40k tokens
├── Main agent: Stays lean
└── Work completes successfully
```

## The R&D Framework

There are only two strategies for managing context in multi-agent systems:

**R - Reduce**

- Minimize what enters context windows
- Remove unused MCP servers (can consume 24k+ tokens)
- Shrink static CLAUDE.md files
- Use context priming instead of static loading

**D - Delegate**

- Move work to sub-agents' isolated contexts
- Use background agents for autonomous work
- Employ orchestrator sleep patterns
- Treat agents as deletable temporary resources

**Everything else is a tactic implementing R or D.**

## The Four Levels of Context Mastery

### Level 1: Beginner - Stop Wasting Tokens

**Focus:** Resource management

**Key Actions:**

- Remove unused MCP servers (reclaim 20k+ tokens)
- Minimize CLAUDE.md (<1k tokens)
- Disable autocompact buffer (reclaim 20%)

**Success Metric:** 85-90% context window free at startup

**Move to Level 2 when:** Resources cleaned but still rebuilding context for different tasks

---

### Level 2: Intermediate - Load Selectively

**Focus:** Dynamic context loading

**Key Actions:**

- Context priming (`/prime` commands vs. static files)
- Sub-agent delegation for parallel work
- Composable workflows (scout-plan-build)

**Success Metric:** 60-75% context window free during work

**Move to Level 3 when:** Managing multiple agents but struggling with handoffs

---

### Level 3: Advanced - Multi-Agent Handoff

**Focus:** Agent-to-agent context transfer

**Key Actions:**

- Context bundles (60-70% transfer in 10% tokens)
- Monitor context limits proactively
- Chain multiple agents without overflow

**Success Metric:** Per-agent context <60k tokens, successful handoffs

**Move to Level 4 when:** Need agents working autonomously while you do other work

---

### Level 4: Agentic - Out-of-Loop Systems

**Focus:** Fleet orchestration

**Key Actions:**

- Background agents (`/background` command)
- Dedicated agent environments
- Orchestrator sleep patterns
- Zero-touch execution

**Success Metric:** Agents ship work end-to-end without intervention

---

## When Context Becomes a Composition Issue

**Trigger 1: Single Agent Exceeds 150k Tokens**
→ Delegate to sub-agents with isolated contexts

**Trigger 2: Agent Reading >20 Files**
→ Use scout agents to identify relevant subset first

**Trigger 3: `/context` Shows >80% Used**
→ Start fresh agent, use context bundles for handoff

**Trigger 4: Performance Degrading Mid-Workflow**
→ Split workflow across multiple focused agents

**Trigger 5: Same Analysis Repeated Multiple Times**
→ Context overflow forcing re-reads; delegate earlier

## Composition Patterns by Level

**Beginner:** Single agent, minimal static context

**Intermediate:** Main agent + sub-agents for parallel work

**Advanced:** Agent chains with context bundles for handoff

**Agentic:** Orchestrator + fleet of specialized agents

## Key Principles

1. **Focused agents perform better** - Single purpose, minimal context
2. **Agents are deletable** - Free context by removing completed agents
3. **200k is plenty** - Context explosions are design problems, not capacity problems
4. **Orchestrators must sleep** - Don't observe all sub-agent work
5. **Context bundles over full replay** - 70% context in 10% tokens

## Implementation Details

For practical patterns, see:

- [Multi-Agent Context Isolation](../reference/multi-agent-context-isolation.md) - Parallel execution, context bundling
- [Orchestrator Pattern](orchestrator-pattern.md) - Sleep patterns, fleet management
- [Decision Framework](decision-framework.md) - When to use each component

## Source Attribution

Primary: Elite Context Engineering, Claude 2.0 transcripts
Supporting: One Agent to Rule Them All, Sub-Agents documentation

---

**Remember:** Context is the first pillar of the Core 4. Master context strategy, and you can scale infinitely with focused agents.
