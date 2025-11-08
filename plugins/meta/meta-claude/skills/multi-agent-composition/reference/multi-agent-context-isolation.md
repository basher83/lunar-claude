# Context Isolation in Multi-Agent Systems

**Core principle:** Each agent operates in its own context window, enabling parallel execution and preventing context pollution.

---

## Why Context Isolation Matters

When orchestrating multiple agents, context isolation provides:

**Independent Operation**

- Each sub-agent has its own context window
- Agents can't access each other's conversation history
- Main agent's context remains clean during delegation

**Parallel Execution**

- Multiple agents run concurrently without interference
- No context sharing between parallel agents
- Results aggregate back to the orchestrator

**Focused Expertise**

- Each agent receives only the context it needs
- Specialized agents maintain narrow, relevant context
- Reduces token waste and improves accuracy

---

## How Sub-Agent Context Works

### Context Window Separation

```text
Main Agent (Context A: 15k tokens)
├── User conversation history
├── CLAUDE.md instructions  
├── Project context
└── Spawns Sub-Agent 1 (Context B: 0k tokens → grows independently)
    └── Only receives: Task prompt + necessary data
    └── Cannot see: Main agent's history, other agents
```

**Key behavior:**

- Sub-agent starts with empty context (just its prompt)
- Only the task prompt is sent to the sub-agent
- Sub-agent cannot ask follow-up questions to main agent
- Returns exactly ONE message with complete results
- Main agent receives only the final output (not full sub-agent history)

### Practical Example

```text
Main Agent (40k tokens used):
├── 30 messages of user conversation
├── Read 20 files from codebase
├── Generated implementation plan
└── Spawns Sub-Agent: "Review auth.py for security issues"

Sub-Agent (starts fresh):
├── Context: Only the prompt + any referenced files
├── Executes: Reads auth.py, analyzes, reports findings
└── Returns: JSON with findings (2k tokens)

Main Agent (now 42k tokens):
└── Receives only the final security report, not the sub-agent's full process
```

**Context savings:**

- Sub-agent's 2k result vs. 10k+ if main agent did it
- Main agent context grows minimally
- Sub-agent context disappears after completion

---

## Parallel Agent Execution

### Context Independence

When launching multiple agents concurrently, each operates in complete isolation:

```text
Main Agent orchestrates:

Agent 1: Search for authentication code
├── Context: Task prompt only
└── Executes independently

Agent 2: Search for database queries  
├── Context: Task prompt only
└── Executes independently

Agent 3: Search for API endpoints
├── Context: Task prompt only
└── Executes independently

All three run simultaneously with zero context sharing
Main agent receives three independent reports
```

### Launching Parallel Agents

Use multiple tool calls in a single message:

```python
# Main agent executes:
[
  Task(prompt="Agent 1: Find all authentication functions", description="Auth search"),
  Task(prompt="Agent 2: Find all database queries", description="DB search"),
  Task(prompt="Agent 3: Find all API endpoints", description="API search")
]

# All execute concurrently
# Each has isolated context
# Results return together
```

**Benefits:**

- 3x faster than sequential execution
- No context pollution between agents
- Main agent context grows by sum of results only, not full execution history

---

## Context-Efficient Agent Design

### Minimal Prompts

Design agent prompts to include only essential information:

**❌ Inefficient:**

```text
You are an expert security reviewer. You have 20 years of experience...
[500 words of background]

Our company uses Python 3.11 with FastAPI...
[200 words of tech stack details]

Review this file for security issues: auth.py
```

**✅ Efficient:**

```text
Review auth.py for security vulnerabilities:
- SQL injection
- Command injection  
- Weak cryptography
- Auth bypasses

Return JSON: {"findings": [...], "severity": "high/med/low"}
```

**Context savings:**

- Inefficient: ~800 tokens to start
- Efficient: ~100 tokens to start
- 8x reduction in baseline context

### Targeted Data Passing

Pass only the data each agent needs:

**❌ Wasteful:**

```text
Agent prompt:
Here are all 50 files in the codebase: [pastes everything]
Find the authentication logic.
```

**✅ Efficient:**

```text
Agent prompt:
Search for files containing "auth", "login", or "authenticate"
Read promising matches
Report authentication implementation locations
```

**Why:** Let the agent discover what it needs rather than front-loading everything.

### Stateless Design

Remember: Sub-agents are completely stateless.

**This means:**

- ✅ Include ALL necessary information in the prompt
- ✅ Specify exact output format required
- ✅ Handle edge cases explicitly in instructions
- ❌ Don't assume agent can ask clarifying questions
- ❌ Don't rely on agent remembering previous context

**Template:**

```text
[Role]: You are a [specific role]
[Task]: Your task is to [specific action]
[Inputs]: You have access to:
- File path: [path]
- Search criteria: [criteria]
[Output]: Return exactly this format:
{
  "field": "value",
  "results": [...]
}
```

---

## Result Aggregation Patterns

### Synthesizing Agent Outputs

Main agent aggregates results without bloating context:

**Pattern 1: Direct Summary**

```text
Sub-agents return:
- Agent 1: 50 security findings
- Agent 2: 30 security findings  
- Agent 3: 20 security findings

Main agent synthesizes:
"Found 100 total findings: 15 critical, 35 high, 50 medium.
Most critical: SQL injection in auth.py (line 42, 67)"

Context cost: ~200 tokens instead of full reports
```

**Pattern 2: Filtered Aggregation**

```text
Sub-agents return verbose results
Main agent extracts:
- Only critical/high severity items
- Deduplicates across agents
- Formats for user

Presents: "Top 5 issues requiring immediate action"
Stores: Full reports in files if needed
```

**Pattern 3: Progressive Refinement**

```text
Round 1: Agents do broad search (3 agents, parallel)
Main agent: Identifies most promising areas from results

Round 2: New agents deep-dive promising areas (2 agents, parallel)
Main agent: Synthesizes final recommendations

Context: Only decisions and final output, not full intermediate work
```

---

## When Context Isolation Is Critical

### Use Case 1: Parallel Research

```text
Task: Analyze entire codebase for patterns

Without isolation:
- Main agent reads 100 files sequentially
- Context explodes to 180k tokens
- Slows down, risks cutoff

With isolation:
- Spawn 5 agents, 20 files each
- Each agent context: ~40k tokens max
- Main agent context: ~10k baseline + 5 reports (2k each) = 20k total
- 9x more efficient
```

### Use Case 2: Specialized Analysis

```text
Task: Review codebase for security, performance, and architecture

Without isolation:
- One agent tries to do everything
- Context fills with mixed concerns
- Quality degrades as context grows

With isolation:
- Security agent: Only security patterns
- Performance agent: Only performance patterns  
- Architecture agent: Only structural patterns
- Each maintains focused, relevant context
- Higher quality results per domain
```

### Use Case 3: Long-Running Workflows

```text
Task: Complex refactoring with validation

Without isolation:
- Single agent context reaches 150k tokens
- Approaches limit, performance degrades
- Risk of important context being lost

With isolation:
- Main agent: Orchestrates steps (20k context)
- Sub-agent 1: Analysis phase (returns summary)
- Sub-agent 2: Implementation phase (returns changes)
- Sub-agent 3: Testing phase (returns results)
- Main agent stays lean throughout entire workflow
```

---

## Best Practices

### 1. Delegate Strategic Work to Sub-Agents

**Delegate:**

- ✅ File searches across large codebases
- ✅ Repetitive analysis tasks
- ✅ Parallel research streams
- ✅ Specialized domain reviews

**Keep in Main Agent:**

- ✅ User conversation and decision-making
- ✅ Workflow orchestration
- ✅ Result synthesis and presentation

### 2. Design for Statelessness

Every sub-agent prompt should be complete:

- All inputs specified
- All outputs defined
- All edge cases handled
- No assumptions about follow-up

### 3. Launch Agents in Parallel

When tasks are independent:

```text
❌ Sequential: 3 agents × 30 seconds = 90 seconds
✅ Parallel: 3 agents concurrent = 30 seconds
```

Use multiple tool calls in one message.

### 4. Keep Main Agent Context Clean

After receiving sub-agent results:

- Extract key findings only
- Summarize verbose outputs
- Store full reports in files if needed
- Don't copy entire results into conversation

### 5. Monitor Context Usage

Even with isolation, monitor your orchestrator:

- Check main agent context periodically
- Use /context command to see usage
- Compact if approaching limits

---

## Common Mistakes

### ❌ Over-Delegating Simple Tasks

```text
Bad: Spawn sub-agent to read one file
Cost: Tool call overhead + agent startup
Better: Main agent reads file directly
```

**Rule:** Only delegate if task complexity or isolation value justifies overhead.

### ❌ Passing Full Context to Sub-Agents

```text
Bad: "Here's everything, find X"
Better: "Search for X, report findings"
```

**Rule:** Let agents discover what they need, don't front-load.

### ❌ Creating Context Leaks

```text
Bad: Main agent re-reads all sub-agent work
Better: Main agent works from summaries only
```

**Rule:** Aggregate efficiently, don't duplicate sub-agent context.

### ❌ Sequential When Could Be Parallel

```text
Bad:
- Agent 1 finishes → Start Agent 2
- Agent 2 finishes → Start Agent 3

Better:
- Launch Agent 1, 2, 3 simultaneously
```

**Rule:** If tasks are independent, run them in parallel.

---

## Monitoring and Optimization

### Check Context Usage

Use the `/context` command to see current context:

```text
/context

Response shows:
- Total tokens used
- Messages in conversation
- System context (CLAUDE.md, etc.)
- Available capacity
```

**Target:** Main agent context should stay under 50k tokens for most workflows.

### Signs You Need Better Isolation

- Main agent context exceeds 100k tokens
- Performance degrades mid-workflow
- Agent seems to "forget" earlier context
- Same analysis repeated multiple times

**Solution:** Delegate more work to sub-agents.

### Measuring Efficiency Gains

**Before optimization:**

```text
Main agent context: 150k tokens
Task completion: 5 minutes
Context cutoff risk: High
```

**After sub-agent delegation:**

```text
Main agent context: 30k tokens
Task completion: 2 minutes (parallel)
Context cutoff risk: Low
```

**Calculation:** 5x context reduction, 2.5x speed improvement.

---

## Summary

**Context isolation in multi-agent systems provides:**

1. **Independent execution** - Each agent operates without interference
2. **Parallel scalability** - Multiple agents run concurrently  
3. **Context efficiency** - Main agent stays lean, sub-agents are ephemeral
4. **Focused expertise** - Each agent maintains narrow, relevant context
5. **Workflow resilience** - Reduced risk of context overflow

**Key principles:**

- Sub-agents have isolated context windows
- Launch multiple agents in parallel for independent tasks
- Design prompts to be complete and stateless
- Aggregate results efficiently without context duplication
- Monitor main agent context to ensure it stays manageable

**When to use sub-agents for context isolation:**

- ✅ Complex workflows with multiple independent steps
- ✅ Parallel research or analysis tasks
- ✅ Specialized domain work (security, performance, etc.)
- ✅ Large-scale operations (analyzing many files)
- ❌ Simple, single-file operations
- ❌ Tasks requiring main agent's conversation context

---

## References

**Official Documentation:**

- Sub-agents: docs.claude.com/en/docs/claude-code/subagents
- Task tool: Official Claude Code system prompt documentation
- Context management: docs.claude.com/en/docs/claude-code

**See Also:**

- [Agentic Prompt Template](agentic-prompt-template.md) - Complete guide for sub-agent prompt design
- [Multi-Agent Orchestration Patterns](multi-agent-patterns.md) - Advanced orchestration workflows

---

*All features described are official Claude Code capabilities. This document focuses exclusively on context isolation aspects relevant to multi-agent orchestration.*
