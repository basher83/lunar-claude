# Multi-Agent Case Studies

Real-world examples of multi-agent systems in production, drawn from field experience.

## Case Study Index

| # | Name | Pattern | Agents | Key Lesson |
|---|------|---------|--------|------------|
| 1 | AI Docs Loader | Sub-agent delegation | 8-10 | Parallel work without context pollution |
| 2 | SDK Migration | Scout-plan-build | 6 | Search + plan + implement workflow |
| 3 | Codebase Summarization | Orchestrator + QA | 3 | Divide and conquer with synthesis |
| 4 | UI Component Creation | Scout-builder | 2 | Precise targeting before building |
| 5 | PLAN-BUILD-REVIEW-SHIP | Task board lifecycle | 4 | Quality gates between phases |
| 6 | Meta-Agent System | Agent building agents | Variable | Recursive agent creation |
| 7 | Observability Dashboard | Fleet monitoring | 5-10+ | Real-time multi-agent visibility |
| 8 | AFK Agent Device | Autonomous background work | 3-5 | Out-of-loop while you sleep |

---

## Case Study 1: AI Docs Loader

**Pattern:** Sub-agent delegation for parallel work

**Problem:** Loading 10 documentation URLs consumes 30k+ tokens per scrape. Single agent would hit 150k+ tokens.

**Solution:** Delegate each scrape to isolated sub-agent

**Architecture:**

```text
Primary Agent (9k tokens)
├→ Sub-Agent 1: Scrape doc 1 (3k tokens, isolated)
├→ Sub-Agent 2: Scrape doc 2 (3k tokens, isolated)
├→ Sub-Agent 3: Scrape doc 3 (3k tokens, isolated)
...
└→ Sub-Agent 10: Scrape doc 10 (3k tokens, isolated)

Total work: 39k tokens
Primary agent: Only 9k tokens ✅
Context protected: 30k tokens kept out of primary
```

**Implementation:**

```bash
# Single command
/load-ai-docs

# Agent reads list from ai-docs/README.md
# For each URL older than 24 hours:
#   - Spawn sub-agent
#   - Sub-agent scrapes URL
#   - Sub-agent saves to file
#   - Sub-agent reports completion
# Primary agent never sees scrape content
```

**Key techniques:**

- **Sub-agents for isolation** - Each scrape in separate context
- **Parallel execution** - All 10 scrapes run simultaneously
- **Context delegation** - 30k tokens stay out of primary

**Results:**

- **Time:** 10 scrapes in parallel vs. sequential (10x faster)
- **Context:** Primary agent stays at 9k tokens throughout
- **Scalability:** Can handle 50+ URLs without primary context issues

**Source:** Elite Context Engineering transcript

---

## Case Study 2: SDK Migration

**Pattern:** Scout-plan-build with multiple perspectives

**Problem:** Migrating codebase to new Claude Agent SDK across 8 applications

**Challenge:**

- 100+ files potentially affected
- Agent reading everything = 150k+ tokens
- Planning without full context = mistakes

**Solution:** Three-phase workflow with delegation

**Phase 1: Scout (Reduce context for planner)**

```text
Orchestrator spawns 4 scout agents (parallel):
├→ Scout 1: Gemini Lightning (fast, different perspective)
├→ Scout 2: CodeX (specialized for code search)
├→ Scout 3: Gemini Flash Preview
└→ Scout 4: Haiku (cheap, fast)

Each scout:
- Searches codebase for SDK usage
- Identifies exact files and line numbers
- Notes patterns (e.g., "system prompt now explicit")

Output: relevant-files.md (5k tokens)
├── File paths
├── Line number offsets
├── Character ranges
└── Relevant code snippets
```

**Why multiple models?** Diverse perspectives catch edge cases single model might miss.

**Phase 2: Plan (Focus on relevant subset)**

```text
Planner agent (new instance):
├── Reads relevant-files.md (5k tokens)
├── Scrapes SDK documentation (8k tokens)
├── Analyzes migration patterns
└── Creates detailed-plan.md (3k tokens)

Context used: 16k tokens
vs. 150k if reading entire codebase
Savings: 89% reduction
```

**Phase 3: Build (Execute plan)**

```text
Builder agent (new instance):
├── Reads detailed-plan.md (3k tokens)
├── Implements changes across 8 apps
├── Updates system prompts
├── Tests each application
└── Reports completion

Context used: ~80k tokens
Still within safe limits
```

**Final context analysis:**

```text
If single agent:
├── Search: 40k tokens
├── Read files: 60k tokens
├── Plan: 20k tokens
├── Implement: 30k tokens
└── Total: 150k tokens (75% used)

With scout-plan-build:
├── Primary orchestrator: 10k tokens
├── 4 scouts (parallel, isolated): 4 × 15k = 60k total, 0k in primary
├── Planner (new agent): 16k tokens
├── Builder (new agent): 80k tokens
└── Max per agent: 80k tokens (40% per agent)
```

**Key techniques:**

- **Composable workflows** - Chain /scout, /plan, /build
- **Multiple scout models** - Diverse perspectives
- **Context offloading** - Scouts protect planner's context
- **Fresh agents per phase** - No context accumulation

**Results:**

- **8 applications migrated** successfully
- **51% context used** in builder phase (safe margins)
- **No context explosions** across entire workflow
- **Completed in single session** (~30 minutes)

**Near miss:** "We were 14% away from exploding our context" due to autocompact buffer

**Lesson:** Disable autocompact buffer. That 22% matters at scale.

**Source:** Claude 2.0 transcript

---

## Case Study 3: Codebase Summarization

**Pattern:** Orchestrator with specialized QA agents

**Problem:** Summarize large codebase (frontend + backend) with architecture docs

**Approach:** Divide and conquer with synthesis

**Architecture:**

```text
Orchestrator Agent
├→ Creates Frontend QA Agent
│  ├─ Summarizes frontend components
│  └─ Outputs: frontend-summary.md
├→ Creates Backend QA Agent
│  ├─ Summarizes backend APIs
│  └─ Outputs: backend-summary.md
└→ Creates Primary QA Agent
   ├─ Reads both summaries
   ├─ Synthesizes unified view
   └─ Outputs: codebase-overview.md
```

**Orchestrator behavior:**

```text
1. Parse user request: "Summarize codebase"
2. Create 3 agents with specialized tasks
3. Command each agent with detailed prompts
4. SLEEP (not observing their work)
5. Wake every 15s to check status
6. Agents complete → Orchestrator wakes
7. Collect results (read produced files)
8. Summarize for user
9. Delete all 3 agents
```

**Prompts from orchestrator:**

```markdown
Frontend QA Agent:
"Analyze all files in src/frontend/. Create markdown summary with:
- Key components and their responsibilities
- State management approach
- Routing structure
- Technology stack
Output to docs/frontend-summary.md"

Backend QA Agent:
"Analyze all files in src/backend/. Create markdown summary with:
- API endpoints and their purposes
- Database schema
- Authentication/authorization
- External integrations
Output to docs/backend-summary.md"

Primary QA Agent:
"Read frontend-summary.md and backend-summary.md. Create unified overview with:
- High-level architecture
- How components interact
- Data flow
- Key technologies
Output to docs/codebase-overview.md"
```

**Observability interface shows:**

```text
[Agent 1] Frontend QA
├── Status: Complete ✅
├── Context: 28k tokens used
├── Files consumed: 15 files
├── Files produced: frontend-summary.md
└── Time: 45 seconds

[Agent 2] Backend QA
├── Status: Complete ✅
├── Context: 32k tokens used
├── Files consumed: 12 files
├── Files produced: backend-summary.md
└── Time: 52 seconds

[Agent 3] Primary QA
├── Status: Complete ✅
├── Context: 18k tokens used
├── Files consumed: 2 files (summaries)
├── Files produced: codebase-overview.md
└── Time: 30 seconds

Orchestrator:
├── Context: 12k tokens (commands only, not observing work)
├── Total time: 52 seconds (parallel execution)
└── All agents deleted after completion
```

**Key techniques:**

- **Parallel frontend/backend** - 2x speedup
- **Orchestrator sleeps** - Protects its context
- **Synthesis agent** - Combines perspectives
- **Deletable agents** - Freed after use

**Results:**

- **3 comprehensive docs** created
- **Max context per agent:** 32k tokens (16%)
- **Orchestrator context:** 12k tokens (6%)
- **Time:** 52 seconds (vs. 2+ minutes sequential)

**Source:** One Agent to Rule Them All transcript

---

## Case Study 4: UI Component Creation

**Pattern:** Scout-builder two-stage

**Problem:** Create gray pills for app header information display

**Challenge:** Codebase has specific conventions. Need to find exact files and follow patterns.

**Solution:** Scout locates, builder implements

**Phase 1: Scout**

```text
Scout Agent:
├── Task: "Find header UI component files"
├── Searches for: header, display, pills, info components
├── Identifies patterns: existing pill styles, color conventions
├── Locates exact files:
│   ├── src/components/AppHeader.vue
│   ├── src/styles/pills.css
│   └── src/utils/formatters.ts
└── Outputs: scout-header-report.md with:
    ├── File locations
    ├── Line numbers for modifications
    ├── Existing patterns to follow
    └── Recommended approach
```

**Phase 2: Builder**

```text
Builder Agent:
├── Reads scout-header-report.md
├── Follows identified patterns
├── Creates gray pill components
├── Applies consistent styling
├── Outputs modified files with exact changes
└── Context: Only 30k tokens (vs. 80k+ without scout)
```

**Orchestrator involvement:**

```text
1. User prompts: "Create gray pills for header"
2. Orchestrator creates Scout
3. Orchestrator SLEEPS (checks every 15s)
4. Scout completes → Orchestrator wakes
5. Orchestrator reads scout output
6. Orchestrator creates Builder with detailed instructions
7. Orchestrator SLEEPS again
8. Builder completes → Orchestrator wakes
9. Orchestrator reports results
10. Orchestrator deletes both agents
```

**Key techniques:**

- **Scout reduces uncertainty** - Builder knows exactly where to work
- **Pattern following** - Scout identifies conventions
- **Orchestrator sleep** - Two phases, minimal orchestrator context
- **Precise targeting** - No wasted reads

**Results:**

- **Scout:** 15k tokens, 20 seconds
- **Builder:** 30k tokens, 35 seconds
- **Orchestrator:** 8k tokens final
- **Total time:** 55 seconds
- **Feature shipped** correctly on first try

**Source:** One Agent to Rule Them All transcript

---

## Case Study 5: PLAN-BUILD-REVIEW-SHIP Task Board

**Pattern:** Structured lifecycle with quality gates

**Problem:** Ensure all changes go through proper review before shipping

**Architecture:**

```text
Task Board Columns:
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  PLAN   │→ │  BUILD  │→ │ REVIEW  │→ │  SHIP   │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
```

**Example task: "Update HTML titles"**

**Column 1: PLAN**

```text
Planner Agent:
├── Analyzes requirement
├── Identifies affected files:
│   ├── index.html
│   └── src/App.tsx (has <title> in render)
├── Creates implementation plan:
│   1. Update index.html <title>
│   2. Update App.tsx header component
│   3. Test both pages load correctly
└── Moves task to BUILD column
```

**Column 2: BUILD**

```text
Builder Agent:
├── Reads plan from PLAN column
├── Implements changes:
│   ├── index.html: "Plan Build Review Ship"
│   └── App.tsx: header="Plan Build Review Ship"
├── Runs tests: All passing ✅
└── Moves task to REVIEW column
```

**Column 3: REVIEW**

```text
Reviewer Agent:
├── Reads plan and implementation
├── Checks:
│   ├── Plan followed? ✅
│   ├── Tests passing? ✅
│   ├── Code quality? ✅
│   └── No security issues? ✅
├── Approves changes
└── Moves task to SHIP column
```

**Column 4: SHIP**

```text
Shipper Agent:
├── Creates git commit
├── Pushes to remote
├── Updates deployment
└── Marks task complete
```

**Orchestrator's role:**

```text
- NOT micromanaging each step
- Responding to user commands like "Move task to next phase"
- Tracking task state in database
- Providing UI showing current phase
- Can intervene if phase fails (e.g., tests fail in BUILD)
```

**UI representation:**

```text
Task: Update Titles
├── Status: REVIEW
├── Assigned: reviewer-agent-003
├── History:
│   ├── PLAN: planner-001 (completed 2m ago)
│   ├── BUILD: builder-002 (completed 1m ago)
│   └── REVIEW: reviewer-003 (in progress)
└── Files modified: 2
```

**Key techniques:**

- **Clear phases** - No ambiguity about current state
- **Quality gates** - Can't skip to SHIP without REVIEW
- **Agent specialization** - Each agent expert in its phase
- **Failure isolation** - If BUILD fails, PLAN preserved

**Results:**

- **Zero shipping untested code** (REVIEW gate catches issues)
- **Clear audit trail** (who did what in which phase)
- **Parallel tasks** (multiple agents in different columns)
- **Single interface** (user sees all tasks across all phases)

**Source:** Custom Agents transcript

---

## Case Study 6: Meta-Agent System

**Pattern:** Agents building agents

**Problem:** Need new specialized agent but don't want to hand-write configuration

**Solution:** Meta-agent that builds other agents

**Meta-agent prompt:**

```markdown
# meta-agent.md

You are a meta-agent that builds new sub-agents from user descriptions.

When user says "build a new sub-agent":
1. Ask what the agent should do
2. Fetch Claude Code sub-agent documentation
3. Design system prompt for new agent
4. Create agent configuration file
5. Test agent with sample prompts
6. Report usage examples

Output: .claude/agents/<agent-name>.md with complete configuration
```

**Example: Building TTS summary agent**

**User:** "Build agent that summarizes what my code does using text-to-speech"

**Meta-agent process:**

```text
Step 1: Understand requirements
├── Parse: "summarize code" + "text-to-speech"
├── Infer: Needs code reading + TTS API access
└── Clarify: Voice provider? (user chooses 11Labs)

Step 2: Fetch documentation
├── Reads Claude Code sub-agent docs
├── Reads 11Labs API docs
└── Understands agent configuration format

Step 3: Design system prompt
├── Purpose: Concise code summaries via voice
├── Tools needed: read files, 11Labs TTS
├── Response format: Audio file output
└── Trigger: "use TTS summary"

Step 4: Create configuration
Writes .claude/agents/tts-summary.md:
---
name: tts-summary
description: Concisely summarizes code with text-to-speech. Trigger: "TTS summary"
---
Purpose: Review user's code and provide 1-sentence summary via 11Labs voice
[... full system prompt ...]

Step 5: Test
├── Runs test prompt: "TTS summary for hooks.py"
├── Agent reads file, generates summary
├── Outputs audio with summary
└── Validates: Works correctly ✅

Step 6: Report
├── Explains how to use new agent
├── Shows example prompts
└── Notes: Can adjust voice, length, etc.
```

**Result:** Fully functional TTS summary agent created from natural language description

**Recursion depth:**

```text
Level 0: Human user
  └→ Level 1: Meta-agent (builds agents)
      └→ Level 2: TTS summary agent (built by meta-agent)
          └→ Level 3: Sub-agents (if TTS agent spawns any)
```

**Key techniques:**

- **Documentation fetching** - Meta-agent reads official docs
- **Template following** - Follows agent configuration patterns
- **Validation loop** - Tests before declaring success
- **Recursive creation** - Agents can build agents

**Challenges:**

- **Dependency coupling** - New agent depends on meta-agent's understanding
- **Debugging difficulty** - If generated agent fails, hard to trace
- **Version drift** - Meta-agent's docs knowledge may become outdated

**Results:**

- **New agent in ~2 minutes** vs. 15+ minutes manually
- **Follows best practices** automatically
- **Tested before delivery**
- **Documented usage**

**Source:** Sub-Agents transcript

---

## Case Study 7: Observability Dashboard

**Pattern:** Real-time multi-agent monitoring

**Problem:** Running 5-10 agents simultaneously. Can't see what they're doing.

**Solution:** Centralized observability system

**Architecture:**

```text
┌──────────────────── Multiple Agents ────────────────────┐
│  Agent 1    Agent 2    Agent 3    Agent 4    Agent 5    │
│    ↓          ↓          ↓          ↓          ↓        │
│             pre/post-tool-use hooks                      │
│                        ↓                                 │
└──────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────── Bun Server ─────────────────────────┐
│  POST /events endpoint                                   │
│         ├→ Store in SQLite (persistence)                 │
│         └→ Broadcast via WebSocket (real-time)           │
└──────────────────────────────────────────────────────────┘
                         ↓
┌──────────────────── Web Client ─────────────────────────┐
│  ┌─────────────────────────────────────────────────┐    │
│  │ Live Activity Pulse (1min/3min/5min windows)    │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Event Stream (filtered by app/session/type)     │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Event Details (with AI-generated summaries)     │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

**Hook implementation:**

```python
# .claude/hooks/post-tool-use.py
import sys, json, subprocess

def main():
    event = json.load(sys.stdin)

    # Send to observability server (with AI summary)
    subprocess.run([
        "uv", "run",
        ".claude/hooks/utils/send-event.py",
        "my-codebase",          # App name
        "post-tool-use",        # Event type
        "--summarize"           # Generate Haiku summary
    ], input=json.dumps(event), text=True)

if __name__ == "__main__":
    main()
```

**What user sees:**

```text
┌─────────────── Live Activity Pulse ───────────────┐
│ ▂▄▆█▆▄▂▁ Agent A (very active)                    │
│ ▁▁▂▂▃▃▂▂ Agent B (moderate activity)              │
│ ▂▂▂▂▂▂▂▂ Agent C (steady work)                    │
│ ▁▁▁█▁▁▁▁ Agent D (spike, then quiet)              │
└────────────────────────────────────────────────────┘

┌─────────────── Event Stream ──────────────────────┐
│ [Agent A] post-tool-use                            │
│   Summary: "Wrote authentication logic to user.py"│
│   Time: 2s ago                                     │
├────────────────────────────────────────────────────┤
│ [Agent B] sub-agent-stop                           │
│   Summary: "Completed documentation scrape"        │
│   Time: 5s ago                                     │
├────────────────────────────────────────────────────┤
│ [Agent C] notification                             │
│   Summary: "Needs approval for rm command"         │
│   Time: 8s ago                                     │
└────────────────────────────────────────────────────┘
```

**Filtering:**

```text
Filters available:
├── By app (codebase-1, codebase-2, etc.)
├── By agent session ID
├── By event type (pre-tool, post-tool, stop, etc.)
└── By time window (1min, 3min, 5min)
```

**Event summarization:**

```python
# Each event summarized by Haiku ($0.0002 per event)
Event: post-tool-use for Write tool
Input: {file: "auth.py", content: "...500 lines..."}
Output: Success

Summary generated:
"Implemented JWT authentication with refresh tokens in auth.py"

Cost: $0.0002
Human value: Instant understanding without reading 500 lines
```

**Key techniques:**

- **One-way data stream** - Simple, fast, scalable
- **Edge summarization** - AI summaries generated at hook time
- **Dual storage** - SQLite (history) + WebSocket (real-time)
- **Color coding** - Consistent colors per agent session

**Results:**

- **5-10 agents monitored** simultaneously
- **Thousands of events logged** (cost: ~$0.20)
- **Real-time visibility** into all agent work
- **Historical analysis** via SQLite queries

**Business value:**

- **Catch errors fast** (notification events = agent blocked)
- **Optimize workflows** (which tools used most?)
- **Debug issues** (what happened before failure?)
- **Scale confidence** (can observe 10+ agents easily)

**Source:** Multi-Agent Observability transcript

---

## Case Study 8: AFK Agent Device

**Pattern:** Autonomous background work while you're away

**Problem:** Long-running tasks block your terminal. You want to work on something else.

**Solution:** Dedicated device running agent fleet

**Architecture:**

```text
Your Device (interactive):
├── Claude Code session
├── Send job to agent device
└── Monitor status updates

Agent Device (autonomous):
├── Picks up job from queue
├── Executes: Scout → Plan → Build → Ship
├── Reports status every 60s
└── Ships results to git
```

**Workflow:**

```bash
# From your device
/afk-agents \
  --prompt "Build 3 OpenAI SDK agents: basic, with-tools, realtime-voice" \
  --adw "plan-build-ship" \
  --docs "https://openai-agent-sdk.com/docs"

# Job sent to dedicated device
# You continue working on your device
# Background: Agent device executes workflow
```

**Agent device execution:**

```text
[00:00] Job received: Build 3 SDK agents
[00:05] Planner agent created
[00:45] Plan complete: 3 agents specified
[01:00] Builder agent 1 created (basic agent)
[02:30] Builder agent 1 complete: basic-agent.py ✅
[02:35] Builder agent 2 created (with tools)
[04:15] Builder agent 2 complete: agent-with-tools.py ✅
[04:20] Builder agent 3 created (realtime voice)
[07:45] Builder agent 3 partial: needs audio libraries
[08:00] Builder agent 3 complete: realtime-agent.py ⚠️ (partial)
[08:05] Shipper agent created
[08:20] Git commit created
[08:25] Pushed to remote
[08:30] Job complete ✅
```

**Status updates (every 60s):**

```text
Your device shows:

[60s] Status: Planning agents...
[120s] Status: Building agent 1 of 3...
[180s] Status: Building agent 2 of 3...
[240s] Status: Building agent 3 of 3...
[300s] Status: Testing agents...
[360s] Status: Shipping to git...
[420s] Status: Complete ✅

Click to view: results/sdk-agents-20250105/
```

**What you do:**

```text
1. Send job (10 seconds)
2. Go AFK (work on something else)
3. Get notified when complete (7 minutes later)
4. Review results
```

**Key techniques:**

- **Job queue** - Agents pick up work from queue
- **Async status** - Reports back periodically
- **Autonomous execution** - No human in the loop
- **Git integration** - Results automatically committed

**Results:**

- **3 SDK agents built** in 7 minutes
- **You worked on other things** during that time
- **Autonomous end-to-end** - plan + build + test + ship
- **Code review** - Quick glance confirms quality

**Infrastructure required:**

- Dedicated machine (M4 Mac Mini, cloud VM, etc.)
- Agent queue system
- Job scheduler
- Status reporting

**Use cases:**

- Long-running builds
- Overnight work
- Prototyping experiments
- Documentation generation
- Codebase refactors

**Source:** Claude 2.0 transcript

---

## Cross-Cutting Patterns

### Pattern: Context Window as Resource Constraint

**Appears in:**

- Case 1: Sub-agent delegation protects primary
- Case 2: Scout-plan-build reduces planner context
- Case 3: Orchestrator sleeps to protect its context
- Case 8: Fresh agents for each phase (no accumulation)

**Lesson:** Context is precious. Protect it aggressively.

### Pattern: Specialized Agents Over General

**Appears in:**

- Case 3: Frontend/Backend/QA agents vs. one do-everything agent
- Case 4: Scout finds, builder builds (not one agent doing both)
- Case 5: Planner/builder/reviewer/shipper (4 specialists)
- Case 6: Meta-agent only builds, doesn't execute

**Lesson:** "A focused agent is a performant agent."

### Pattern: Observability Enables Scale

**Appears in:**

- Case 3: Orchestrator tracks agent status
- Case 5: Task board shows current phase
- Case 7: Real-time dashboard for all agents
- Case 8: Status updates every 60s

**Lesson:** "If you can't measure it, you can't scale it."

### Pattern: Deletable Temporary Resources

**Appears in:**

- Case 3: All 3 agents deleted after completion
- Case 4: Scout and builder deleted
- Case 5: Each phase agent deleted after task moves
- Case 8: Builder agents deleted after shipping

**Lesson:** "The best agent is a deleted agent."

## Performance Comparisons

### Single Agent vs. Multi-Agent

| Task | Single Agent | Multi-Agent | Speedup |
|------|--------------|-------------|---------|
| Load 10 docs | 150k tokens, 5min | 30k primary, 2min | 2.5x faster, 80% less context |
| SDK migration | Fails (overflow) | 80k max/agent, 30min | Completes vs. fails |
| Codebase summary | 120k tokens, 3min | 32k max/agent, 52s | 3.5x faster |
| UI components | 80k tokens, 2min | 30k max, 55s | 2.2x faster |

### With vs. Without Orchestration

| Metric | Manual (no orchestrator) | With Orchestrator |
|--------|-------------------------|-------------------|
| Commands per task | 8-12 manual prompts | 1 prompt to orchestrator |
| Context management | Manual (forget limits) | Automatic (orchestrator sleeps) |
| Error recovery | Start over | Retry failed phase only |
| Observability | Terminal logs | Real-time dashboard |

## Common Failure Modes

### Failure: Context Explosion

**Scenario:** Case 2 without scouts

- Single agent reads 100+ files
- Context hits 180k tokens
- Agent slows down, makes mistakes
- Eventually fails or times out

**Fix:** Add scout phase to filter files first

### Failure: Orchestrator Watching Everything

**Scenario:** Case 3 with observing orchestrator

- Orchestrator watches all agent work
- Orchestrator context grows to 100k+
- Can't coordinate more than 2-3 agents
- System doesn't scale

**Fix:** Implement orchestrator sleep pattern

### Failure: No Observability

**Scenario:** Case 7 without dashboard

- 5 agents running
- One agent stuck on permission request
- No way to know which agent needs attention
- Entire workflow blocked

**Fix:** Add hooks + observability system

### Failure: Agent Accumulation

**Scenario:** Case 5 not deleting agents

- 20 tasks completed
- 80 agents still running (4 per task)
- System resources exhausted
- New agents can't start

**Fix:** Delete agents after task completion

## Key Takeaways

1. **Parallelization = Sub-agents** - Nothing else runs agents in parallel

2. **Context protection = Specialization** - Focused agents use less context

3. **Orchestration = Scale** - Single interface manages fleet

4. **Observability = Confidence** - Can't scale what you can't see

5. **Deletable = Sustainable** - Free resources for next task

6. **Multi-agent is Level 5** - Requires mastering Levels 1-4 first

## When to Use Multi-Agent Patterns

Use multi-agent when:

- ✅ Task naturally divides into parallel subtasks
- ✅ Single agent context approaching limits
- ✅ Need quality gates between phases
- ✅ Want to work on other things while agents execute
- ✅ Have observability infrastructure

Don't use multi-agent when:

- ❌ Simple one-off task
- ❌ Learning/prototyping phase
- ❌ No way to monitor agents
- ❌ Task requires tight human-in-loop feedback

## Source Attribution

All case studies drawn from field experience documented in 8 source transcripts:

1. Elite Context Engineering - Case 1 (AI docs loader)
2. Claude 2.0 - Case 2 (SDK migration), Case 8 (AFK device)
3. Custom Agents - Case 5 (task board)
4. Sub-Agents - Case 6 (meta-agent)
5. Multi-Agent Observability - Case 7 (dashboard)
6. Hooked - Supporting patterns
7. One Agent to Rule Them All - Case 3 (summarization), Case 4 (UI components)
8. (Transcript 8 name not specified in context)

## Related Documentation

- [Orchestrator Pattern](../patterns/orchestrator-pattern.md) - Multi-agent coordination
- [Hooks for Observability](../patterns/hooks-observability.md) - Monitoring implementation
- [Context Window Protection](../patterns/context-window-protection.md) - Resource management
- [Evolution Path](../workflows/evolution-path.md) - Progression to multi-agent mastery

---

**Remember:** These are real systems in production. Start simple, add complexity only when needed.
