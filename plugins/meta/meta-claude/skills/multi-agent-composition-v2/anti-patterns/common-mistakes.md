# Common Anti-Patterns in Claude Code

**Critical mistakes to avoid** when building with Claude Code components.

## Table of Contents

- [The Fatal Five](#the-fatal-five)
  - [1. Converting All Slash Commands to Skills](#1-converting-all-slash-commands-to-skills)
  - [2. Using Skills for One-Off Tasks](#2-using-skills-for-one-off-tasks)
  - [3. Skipping the Primitive (Not Mastering Prompts First)](#3-skipping-the-primitive-not-mastering-prompts-first)
  - [4. Forcing Single Agents to Do Too Much (Context Explosion)](#4-forcing-single-agents-to-do-too-much-context-explosion)
  - [5. Using Sub-Agents When Context Matters](#5-using-sub-agents-when-context-matters)
- [Secondary Anti-Patterns](#secondary-anti-patterns)
  - [6. Confusing MCP with Internal Orchestration](#6-confusing-mcp-with-internal-orchestration)
  - [7. Forgetting the Core Four](#7-forgetting-the-core-four)
  - [8. No Observability (Can't Measure, Can't Improve)](#8-no-observability-cant-measure-cant-improve)
  - [9. Nesting Sub-Agents](#9-nesting-sub-agents)
  - [10. Over-Engineering Simple Problems](#10-over-engineering-simple-problems)
  - [11. Agent Dependency Coupling](#11-agent-dependency-coupling)
- [Anti-Pattern Detection Checklist](#anti-pattern-detection-checklist)
- [Recovery Strategies](#recovery-strategies)
- [Remember](#remember)

## The Fatal Five

These are the most common and damaging mistakes engineers make:

### 1. Converting All Slash Commands to Skills

**The Mistake:**
> "There are a lot of engineers right now that are going all in on skills. They're converting all their slash commands to skills. I think that's a huge mistake."

**Why it's wrong:**

- Skills are for **repeat problems that need management**, not simple one-off tasks
- Slash commands are the **primitive foundation** - you need them
- You're adding unnecessary complexity and context overhead
- Skills should **complement** slash commands, not replace them

**Correct approach:**

- Keep slash commands for simple, direct tasks
- Only create a skill when you're **managing a problem domain** with multiple related operations
- Have a strong bias toward slash commands

**Example:**

- ❌ Wrong: Create a skill for generating a single commit message
- ✅ Right: Use a slash command for one-off commit messages; create a skill only if managing an entire git workflow system

---

### 2. Using Skills for One-Off Tasks

**The Mistake:**
> "If you can do the job with a sub-agent or custom slash command and it's a one-off job, do not use a skill. This is not what skills are for."

**Why it's wrong:**

- Skills have overhead (metadata, loading, management)
- One-off tasks don't benefit from reuse
- You're over-engineering a simple problem

**Signal words that indicate you DON'T need a skill:**

- "One time"
- "Quick"
- "Just need to..."
- "Simple task"

**Correct approach:**

- Use a slash command for one-off tasks
- If you find yourself doing it repeatedly (3+ times), **then** consider a skill

**Example:**

- ❌ Wrong: Build a skill to create one UI component
- ✅ Right: Use a slash command; upgrade to skill only after creating components repeatedly

---

### 3. Skipping the Primitive (Not Mastering Prompts First)

**The Mistake:**
> "When you're starting out, I always recommend you just build a prompt. Don't build a skill. Don't build a sub-agent. Don't build out an MCP server. Keep it simple. Build a prompt."

**Why it's wrong:**

- If you don't master prompts, you can't build effective skills
- Everything is prompts in the end (tokens in, tokens out)
- You're building on a weak foundation

**The fundamental truth:**
> "Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming. If you don't know how to build and manage prompts, you will lose."

**Correct approach:**

1. Always start with a prompt/slash command
2. Master the primitive first
3. Scale up only when needed
4. Build from the foundation upward

**Example:**

- ❌ Wrong: "I'm going to start by building a skill because it's more advanced"
- ✅ Right: "I'll write a prompt first, see if it works, then consider scaling to a skill"

---

### 4. Forcing Single Agents to Do Too Much (Context Explosion)

**The Mistake:**
> "200k context window is plenty. You're just stuffing a single agent with too much work, just like your boss did to you at your last job. Don't force your agent to context switch."

**Why it's wrong:**

- Context explosion leads to poor performance
- Agent loses focus across too many unrelated tasks
- You're treating your agent like an overworked employee
- Results degrade as context window fills

**Correct approach:**

- Create **focused agents** with single purposes
- Use **sub-agents** for parallel, isolated work
- **Delete agents** when their task is complete
- Treat agents as **temporary, deletable resources**

**Example:**

- ❌ Wrong: One agent that reads codebase, writes tests, updates docs, and deploys
- ✅ Right: Four focused agents - one for reading, one for tests, one for docs, one for deployment

---

### 5. Using Sub-Agents When Context Matters

**The Mistake:**
> "Sub-agents isolate and protect your context window... But of course, you have to be okay with losing that context afterward because it will be lost."

**Why it's wrong:**

- Sub-agent context is **isolated**
- You can't reference sub-agent work later without resumable sub-agents
- You lose the conversation history

**Correct approach:**

- Use sub-agents when:
  - You need **parallelization**
  - Context **isolation** is desired
  - You're okay **losing context** after
- Use main conversation when:
  - You need context later
  - Work builds on previous steps
  - Conversation continuity matters

**Example:**

- ❌ Wrong: Use sub-agent for research task, then try to reference findings 10 prompts later
- ✅ Right: Do research in main conversation if you'll need it later; use sub-agent only for isolated batch work

---

## Secondary Anti-Patterns

### 6. Confusing MCP with Internal Orchestration

**The Mistake:** Using MCP servers for internal workflows instead of external integrations.

**Why it's wrong:**
> "To me, there is very very little overlap here between agent skills and MCP servers. These are fully distinct."

**Clear rule:** External = MCP, Internal orchestration = Skills

**Example:**

- ❌ Wrong: Build MCP server to orchestrate your internal test suite
- ✅ Right: Build a skill for internal test orchestration; use MCP to connect to external CI/CD service

---

### 7. Forgetting the Core Four

**The Mistake:** Not monitoring Context, Model, Prompt, and Tools at critical moments.

**Why it's wrong:**
> "Context, model, prompt, tools. Do you know what these four leverage points are at every critical moment? This is the foundation."

**Correct approach:**

- Always know the state of the Core Four for your agents
- Monitor context window usage
- Understand which model is active
- Track what prompts are being used
- Know what tools are available

---

### 8. No Observability (Can't Measure, Can't Improve)

**The Mistake:** Running agents without logging, monitoring, or hooks.

**Why it's wrong:**
> "When it comes to agentic coding, observability is everything. If you can't measure it, you can't improve it. And if you can't measure it, you can't scale it."

**Correct approach:**

- Implement hooks for logging (post-tool-use, stop)
- Track agent performance and costs
- Monitor what files are read/written
- Capture chat transcripts
- Review agent behavior to improve prompts

---

### 9. Nesting Sub-Agents

**The Mistake:** Trying to spawn sub-agents from within other sub-agents.

**Why it's wrong:**

- Hard limit in Claude Code architecture
- Prevents infinite nesting
- Not supported by the system

**The restriction:**
> "Sub-agents cannot spawn other sub-agents. This prevents infinite nesting while still allowing Claude to gather necessary context."

**Correct approach:**

- Use orchestrator pattern instead
- Flatten your agent hierarchy
- Have main agent create all sub-agents

---

### 10. Over-Engineering Simple Problems

**The Mistake:** Building complex multi-agent orchestration for tasks that could be a single prompt.

**Why it's wrong:**

- Unnecessary complexity
- Maintenance burden
- Slower execution
- Higher costs

**The principle:** Start simple, scale only when needed.

**Decision checklist before scaling:**

- [ ] Have I tried solving this with a single prompt?
- [ ] Is this actually a repeat problem?
- [ ] Will the added complexity pay off?
- [ ] Am I solving a real problem or just playing with new features?

---

### 11. Agent Dependency Coupling

**The Mistake:** Creating agents that depend on the exact output format of other agents.

**Why it's wrong:**

- Creates **brittle coupling** between agents
- Changes to one agent's output **break downstream agents**
- Makes the system **hard to maintain** and evolve
- Creates a **hidden dependency graph** that's not explicit

**The problem:**
When Agent B expects Agent A to return data in a specific format (e.g., JSON with specific field names, or markdown with specific structure), you create tight coupling. If Agent A's output changes, Agent B silently breaks.

**Warning signs:**

- Agents parsing other agents' string outputs
- Hard-coded field names or output structure assumptions
- Agents that "expect" data in a certain format without validation
- No explicit contracts between agents

**Correct approach:**

**1. Use explicit contracts:**

```text
Agent A prompt:
"Return JSON with these exact fields: {id, name, status, created_at}"

Agent B prompt:
"You will receive JSON with fields: {id, name, status, created_at}
Validate the structure before processing."
```

**2. Use structured data formats:**

- Define JSON schemas explicitly
- Document expected fields
- Validate inputs before processing
- Handle missing or malformed data gracefully

**3. Minimize agent-to-agent communication:**

- Prefer orchestrator pattern (main agent coordinates)
- Pass data through orchestrator, not agent-to-agent
- Keep sub-agents independent when possible

**4. Version your agent contracts:**

```text
Agent output format v2:
{
  "version": "2.0",
  "data": {...},
  "metadata": {...}
}
```

**Example:**

❌ **Wrong (Brittle Coupling):**

```text
Agent A: "Analyze files and report findings"
[Returns: "Found 3 issues in foo.py and 2 in bar.py"]

Agent B: "Parse Agent A's output and fix the issues"
[Expects: "Found N issues in X and Y in Z" format]
```

**Problem:** If Agent A changes its output format, Agent B breaks silently.

✅ **Right (Explicit Contract):**

```text
Agent A: "Analyze files and return JSON:
{
  'files_analyzed': [...],
  'findings': [
    {'file': 'foo.py', 'line': 10, 'issue': '...'},
    {'file': 'bar.py', 'line': 20, 'issue': '...'}
  ]
}"

Agent B: "You will receive JSON with fields: {files_analyzed, findings}.
First validate the structure. Then fix each issue in findings array."
```

**Better (Orchestrator Pattern):**

```text
Main Agent:
1. Spawn Agent A to analyze files
2. Parse Agent A's JSON output
3. Transform to format Agent B needs
4. Spawn Agent B with explicit data structure
5. Agent B doesn't need to know about Agent A
```

**Best practice:** The orchestrator (main agent) owns the contracts and data transformations. Sub-agents are independent and don't depend on each other's formats.

---

## Anti-Pattern Detection Checklist

Ask yourself these questions:

**Before creating a skill:**

- [ ] Is this a **repeat problem** that needs **management**?
- [ ] Have I solved this with a prompt/slash command first?
- [ ] Am I avoiding the mistake of converting simple commands to skills?

**Before using a sub-agent:**

- [ ] Do I need **parallelization** or **context isolation**?
- [ ] Am I okay **losing this context** afterward?
- [ ] Could this be done in the main conversation instead?

**Before using MCP:**

- [ ] Is this for **external** data/services?
- [ ] Am I not confusing this with internal orchestration?

**Before scaling to multi-agent orchestration:**

- [ ] Have I mastered custom agents first?
- [ ] Do I have observability in place?
- [ ] Am I solving a real scale problem?

---

## Recovery Strategies

**If you've fallen into these anti-patterns:**

1. **Converted slash commands to skills?**
   - Evaluate each skill: Is it truly a repeat management problem?
   - Downgrade skills that are just one-off tasks back to slash commands
   - Keep your slash command library strong

2. **Context explosion in single agent?**
   - Split work across focused sub-agents
   - Use orchestrator pattern for complex workflows
   - Delete agents when tasks complete

3. **No observability?**
   - Add hooks immediately (start with stop and post-tool-use)
   - Log chat transcripts
   - Track tool usage
   - Monitor costs

4. **Lost in complexity?**
   - Step back to basics: What's the simplest solution?
   - Remove unnecessary abstractions
   - Return to prompts/slash commands
   - Scale up only when proven necessary

---

## Remember

> "Have a strong bias towards slash commands. And then when you're thinking about composing many slash commands, sub-agents or MCPs, think about putting them in a skill."
>
> "If you can do the job with a sub-agent or custom slash command and it's a one-off job, do not use a skill."
>
> "Context, model, prompt, tools. This never goes away."

**The golden path:** Start with prompts → Scale thoughtfully → Add observability → Manage complexity
