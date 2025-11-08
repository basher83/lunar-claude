# The Orchestrator Pattern

> "The rate at which you can create and command your agents becomes the constraint of your engineering output. When your agents are slow, you're slow."

The orchestrator pattern is **Level 5** of agentic engineering: managing fleets of agents through a single interface.

## The Journey to Orchestration

```text
Level 1: Base agents       → Use agents out of the box
Level 2: Better agents     → Customize prompts and workflows
Level 3: More agents       → Run multiple agents
Level 4: Custom agents     → Build specialized solutions
Level 5: Orchestration     → Manage fleets of agents ← You are here
```

**Key realization:** Single agents hit context window limits. You need orchestration to scale beyond one agent.

## The Three Pillars

Multi-agent orchestration requires three components working together:

```text
┌─────────────────────────────────────────────────────────┐
│              1. ORCHESTRATOR AGENT                      │
│         (Single interface to your fleet)                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              2. CRUD FOR AGENTS                          │
│    (Create, Read, Update, Delete agents at scale)       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              3. OBSERVABILITY                            │
│    (Monitor performance, costs, and results)             │
└─────────────────────────────────────────────────────────┘
```

Without all three, orchestration fails. You need:

- **Orchestrator** to command agents
- **CRUD** to manage agent lifecycle
- **Observability** to understand what agents are doing

## Core Principle: The Orchestrator Sleeps

> "Our orchestrator has stopped doing work. Its orchestration tasks are completed. It has created and commanded our agents. Now, our agents are doing the work."

**The pattern:**

```text
1. User prompts Orchestrator
2. Orchestrator creates specialized agents
3. Orchestrator commands agents with detailed prompts
4. Orchestrator SLEEPS (stops consuming context)
5. Agents work autonomously
6. Orchestrator wakes periodically to check status
7. Orchestrator reports results to user
8. Agents are deleted
```

**Why orchestrator sleeps:**

- Protects its context window
- Avoids observing all agent work (too much information)
- Only wakes when needed to check status or command agents

**Example orchestrator sleep pattern:**

```python
# Orchestrator commands agents
orchestrator.create_agent("scout", task="Find relevant files")
orchestrator.create_agent("builder", task="Implement changes")

# Orchestrator sleeps, checking status every 15s
while not all_agents_complete():
    orchestrator.sleep(15)  # Not consuming context
    status = orchestrator.check_agent_status()
    orchestrator.log(status)

# Wake up to collect results
results = orchestrator.get_agent_results()
orchestrator.summarize_to_user(results)
```

## Orchestration Patterns

### Pattern 1: Scout-Plan-Build (Sequential Chaining)

**Use case:** Complex tasks requiring multiple specialized steps

**Flow:**

```text
User: "Migrate codebase to new SDK"
  ↓
Orchestrator creates Scout agents (4 parallel)
  ├→ Scout 1: Search with Gemini
  ├→ Scout 2: Search with CodeX
  ├→ Scout 3: Search with Haiku
  └→ Scout 4: Search with Flash
  ↓
Scouts output: relevant-files.md with exact locations
  ↓
Orchestrator creates Planner agent
  ├→ Reads relevant-files.md
  ├→ Scrapes documentation
  └→ Outputs: detailed-plan.md
  ↓
Orchestrator creates Builder agent
  ├→ Reads detailed-plan.md
  ├→ Executes implementation
  └→ Tests and validates
```

**Why this works:**

- **Scout step offloads searching from Planner** (R&D framework: Reduce + Delegate)
- **Multiple scout models** provide diverse perspectives
- **Planner only sees relevant files**, not entire codebase
- **Builder focused on execution**, not planning

**Implementation:**

```bash
# Composable slash commands
/scout-plan-build "Migrate to new Claude Agent SDK"

# Internally runs:
/scout "Find files needing SDK migration"
/plan-with-docs docs=https://agent-sdk-docs.com
/build plan=agents/plans/sdk-migration.md
```

**Context savings:**

```text
Without scouts:
├── Planner searches entire codebase: 50k tokens
├── Planner reads irrelevant files: 30k tokens
└── Total wasted: 80k tokens

With scouts:
├── 4 scouts search in parallel (isolated contexts)
├── Planner reads only relevant-files.md: 5k tokens
└── Savings: 75k tokens (94% reduction)
```

### Pattern 2: Plan-Build-Review-Ship (Task Board)

**Use case:** Structured development lifecycle with quality gates

**Flow:**

```text
User: "Update HTML titles across application"
  ↓
Task created → PLAN column
  ↓
Orchestrator creates Planner agent
  ├→ Analyzes requirements
  ├→ Creates implementation plan
  └→ Moves task to BUILD
  ↓
Orchestrator creates Builder agent
  ├→ Reads plan
  ├→ Implements changes
  ├→ Runs tests
  └→ Moves task to REVIEW
  ↓
Orchestrator creates Reviewer agent
  ├→ Checks implementation against plan
  ├→ Validates tests pass
  └→ Moves task to SHIP
  ↓
Orchestrator creates Shipper agent
  ├→ Creates git commit
  ├→ Pushes to remote
  └→ Task complete
```

**Why this works:**

- **Clear phases** with distinct responsibilities
- **Each agent focused** on single phase
- **Quality gates** between phases
- **Failure isolation** - if builder fails, planner work preserved

**Visual representation:**

```text
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  PLAN   │→ │  BUILD  │→ │ REVIEW  │→ │  SHIP   │
├─────────┤  ├─────────┤  ├─────────┤  ├─────────┤
│ Task A  │  │         │  │         │  │         │
│         │  │         │  │         │  │         │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
```

**Agent handoff:**

```python
# Orchestrator manages task board state
task = {
    "id": "update-titles",
    "status": "planning",
    "assigned_agent": "planner-001",
    "artifacts": []
}

# Planner completes
task["status"] = "building"
task["artifacts"].append("plan.md")
task["assigned_agent"] = "builder-001"

# Orchestrator hands off to builder
orchestrator.command_agent(
    "builder-001",
    f"Implement plan from {task['artifacts'][0]}"
)
```

### Pattern 3: Scout-Builder (Two-Stage)

**Use case:** UI changes, targeted modifications

**Flow:**

```text
User: "Create gray pills for app header information"
  ↓
Orchestrator creates Scout
  ├→ Locates exact files and line numbers
  ├→ Identifies patterns and conventions
  └→ Outputs: scout-report.md
  ↓
Orchestrator creates Builder
  ├→ Reads scout-report.md
  ├→ Implements precise changes
  └→ Outputs: modified files
  ↓
Orchestrator wakes, verifies, reports
```

**Orchestrator sleep pattern:**

```python
# Orchestrator creates scout
orchestrator.create_agent("scout-header", task="Find header UI components")

# Orchestrator sleeps, checking every 15s
orchestrator.sleep_with_status_checks(interval=15)

# Scout completes, orchestrator wakes
scout_output = orchestrator.get_agent_output("scout-header")

# Orchestrator creates builder with scout's output
orchestrator.create_agent(
    "builder-ui",
    task=f"Create gray pills based on scout findings: {scout_output}"
)

# Orchestrator sleeps again
orchestrator.sleep_with_status_checks(interval=15)
```

## Context Window Protection

> "200k context window is plenty. You're just stuffing a single agent with too much work. Don't force your agent to context switch."

**The problem:** Single agent doing everything explodes context window

```text
Single Agent Approach:
├── Search codebase: 40k tokens
├── Read files: 60k tokens
├── Plan changes: 20k tokens
├── Implement: 30k tokens
├── Test: 15k tokens
└── Total: 165k tokens (83% used!)
```

**The solution:** Specialized agents with focused context

```text
Orchestrator Approach:
├── Orchestrator: 10k tokens (coordinates)
├── Scout 1: 15k tokens (searches)
├── Scout 2: 15k tokens (searches)
├── Planner: 25k tokens (plans using scout output)
├── Builder: 35k tokens (implements)
└── Total per agent: <35k tokens (max 18% per agent)
```

**Key principle:** Agents are deletable temporary resources

```text
1. Create agent for specific task
2. Agent completes task
3. DELETE agent (free memory)
4. Create new agent for next task
5. Repeat
```

**Example:**

```bash
# User: "Build documentation for frontend and backend"

# Orchestrator creates 3 agents
/create-agent frontend-docs "Document frontend components"
/create-agent backend-docs "Document backend APIs"
/create-agent qa-docs "Combine and QA both docs"

# Work completes...

# Delete all agents when done
/delete-all-agents

# Result: All agents gone, context freed
```

**Why delete agents:**

- Frees context windows for new work
- Prevents context accumulation
- Enforces single-purpose design
- Matches engineering principle: "The best code is no code at all"

## CRUD for Agents

Orchestrator needs full agent lifecycle control:

**Create:**

```python
agent_id = orchestrator.create_agent(
    name="scout-api",
    task="Find all API endpoints",
    model="haiku",  # Fast, cheap for search
    max_tokens=100000
)
```

**Read:**

```python
# Check agent status
status = orchestrator.get_agent_status(agent_id)
# => {"status": "working", "progress": "60%", "context_used": "15k tokens"}

# Read agent output
output = orchestrator.get_agent_output(agent_id)
# => {"files_consumed": [...], "files_produced": [...]}
```

**Update:**

```python
# Command existing agent with new task
orchestrator.command_agent(
    agent_id,
    "Now implement the changes based on your findings"
)
```

**Delete:**

```python
# Single agent
orchestrator.delete_agent(agent_id)

# All agents
orchestrator.delete_all_agents()
```

## Observability Requirements

Without observability, orchestration is blind. You need:

### 1. Agent-Level Visibility

```text
For each agent, track:
├── Name and ID
├── Status (creating, working, complete, failed)
├── Context window usage
├── Model and cost
├── Files consumed
├── Files produced
└── Tool calls executed
```

### 2. Cross-Agent Visibility

```text
Fleet overview:
├── Total agents active
├── Total context consumed
├── Total cost
├── Agent dependencies (who's waiting on whom)
└── Bottlenecks (slow agents blocking others)
```

### 3. Real-Time Streaming

```text
User sees:
├── Agent creation events
├── Tool calls as they happen
├── Progress updates
├── Completion notifications
└── Error alerts
```

**Implementation:** See [Hooks for Observability](hooks-observability.md) for complete architecture

## Information Flow in Orchestrated Systems

```text
User
 ↓ (prompts)
Orchestrator
 ↓ (creates & commands)
Agent 1 → Agent 2 → Agent 3
 ↓         ↓         ↓
(results flow back up)
 ↓
Orchestrator (summarizes)
 ↓
User
```

**Critical understanding:** Agents never talk directly to user. They report to orchestrator.

**Example:**

```python
# User prompts orchestrator
user: "Summarize codebase"

# Orchestrator creates agent with detailed instructions
orchestrator → agent: """
Read all files in src/
Create markdown summary with:
- Architecture overview
- Key components
- File structure
- Tech stack

Report results back to orchestrator (not user!)
"""

# Agent completes, reports to orchestrator
agent → orchestrator: "Summary complete at docs/summary.md"

# Orchestrator reports to user
orchestrator → user: "Codebase summary created with 3 main sections: architecture, components, and tech stack"
```

## When to Use Orchestration

### Use orchestration when

✅ **Task requires 3+ specialized agents**

- Example: Scout + Plan + Build

✅ **Context window exploding in single agent**

- Single agent using >150k tokens

✅ **Need parallel execution**

- Multiple independent subtasks

✅ **Quality gates required**

- Plan → Build → Review → Ship

✅ **Long-running autonomous work**

- Agents work while you're AFK

### Don't use orchestration when

❌ **Simple one-off task**

- Single agent sufficient

❌ **Learning/prototyping**

- Orchestration adds complexity

❌ **No observability infrastructure**

- You'll be blind to agent behavior

❌ **Haven't mastered custom agents**

- Level 5 requires Level 4 foundation

## Practical Implementation

### Minimal Orchestrator Agent

```python
# orchestrator-agent.md (sub-agent definition)

---
name: orchestrator
description: Manages fleet of agents for complex multi-step tasks
---

# Orchestrator Agent

You are an orchestrator agent managing a fleet of specialized agents.

## Your Tools

- create_agent(name, task, model): Create new agent
- command_agent(agent_id, task): Send task to existing agent
- get_agent_status(agent_id): Check agent progress
- get_agent_output(agent_id): Retrieve agent results
- delete_agent(agent_id): Remove completed agent
- delete_all_agents(): Clean up all agents

## Your Responsibilities

1. **Break down user requests** into specialized subtasks
2. **Create focused agents** for each subtask
3. **Command agents** with detailed instructions
4. **Monitor progress** without micromanaging
5. **Collect results** and synthesize for user
6. **Delete agents** when work is complete

## Orchestrator Sleep Pattern

After creating and commanding agents:
1. **SLEEP** - Stop consuming context
2. **Wake every 15-30s** to check agent status
3. **SLEEP again** if agents still working
4. **Wake when all complete** to collect results

DO NOT observe all agent work. This explodes your context window.

## Example Workflow

```

User: "Migrate codebase to new SDK"

You:

1. Create scout agents (parallel search)
2. Command scouts to find SDK usage
3. SLEEP (check status every 15s)
4. Wake when scouts complete
5. Create planner agent
6. Command planner with scout results
7. SLEEP (check status every 15s)
8. Wake when planner completes
9. Create builder agent
10. Command builder with plan
11. SLEEP (check status every 15s)
12. Wake when builder completes
13. Summarize results for user
14. Delete all agents

```bash

## Key Principles

- **One agent, one task** - Don't overload agents
- **Sleep between phases** - Protect your context
- **Delete when done** - Treat agents as temporary
- **Detailed commands** - Don't assume agents know context
- **Results-oriented** - Every agent must produce concrete output
```

### Orchestrator Tools (SDK)

```python
# create_agent tool
@mcptool(
    name="create_agent",
    description="Create a new specialized agent"
)
def create_agent(params: dict) -> dict:
    name = params["name"]
    task = params["task"]
    model = params.get("model", "sonnet")

    agent_id = agent_manager.create(
        name=name,
        system_prompt=task,
        model=model
    )

    return {
        "agent_id": agent_id,
        "status": "created",
        "message": f"Agent {name} created"
    }

# command_agent tool
@mcptool(
    name="command_agent",
    description="Send task to existing agent"
)
def command_agent(params: dict) -> dict:
    agent_id = params["agent_id"]
    task = params["task"]

    result = agent_manager.prompt(agent_id, task)

    return {
        "agent_id": agent_id,
        "status": "commanded",
        "message": f"Agent received task"
    }
```

## Trade-offs

### Benefits

- ✅ Scales beyond single agent limits
- ✅ Parallel execution (3x-10x speedup)
- ✅ Context window protection
- ✅ Specialized agent focus
- ✅ Quality gates between phases
- ✅ Autonomous out-of-loop work

### Costs

- ❌ Upfront investment to build
- ❌ Infrastructure complexity (database, WebSocket)
- ❌ More moving parts to manage
- ❌ Requires observability
- ❌ Orchestrator agent needs careful prompting
- ❌ Not worth it for simple tasks

## Key Quotes

> "The orchestrator agent is the first pattern where I felt the perfect combination of observability, customizability, and agents at scale."
>
> "Treat your agents as deletable temporary resources that serve a single purpose."
>
> "Our orchestrator has stopped doing work. Its orchestration tasks are completed. Now, our agents are doing the work."
>
> "200k context window is plenty. You're just stuffing a single agent with too much work."

## Source Attribution

**Primary source:** One Agent to Rule Them All (orchestrator architecture, three pillars, sleep pattern, CRUD)

**Supporting sources:**

- Claude 2.0 (scout-plan-build workflow, composable prompts)
- Custom Agents (plan-build-review-ship task board)
- Sub-Agents (information flow, delegation patterns)

## Related Documentation

- [Hooks for Observability](hooks-observability.md) - Required for orchestration
- [Context Window Protection](context-window-protection.md) - Why orchestration matters
- [Multi-Agent Case Studies](../examples/multi-agent-case-studies.md) - Real orchestration systems

---

**Remember:** Orchestration is Level 5. Master Levels 1-4 first. Then build your fleet.
