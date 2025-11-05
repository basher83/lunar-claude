# Decision Framework: Choosing the Right Claude Code Component

This guide helps you choose the right Claude Code component for your specific task. **Always start with prompts**—master the primitive first before scaling to other components.

## The Decision Tree

Start here when deciding which component to use:

```text
1. START HERE: Build a Prompt (Slash Command)
   ↓
2. Need parallelization or isolated context?
   YES → Use Sub-Agent
   NO → Continue
   ↓
3. External data/service integration?
   YES → Use MCP Server
   NO → Continue
   ↓
4. One-off task (simple, direct)?
   YES → Use Slash Command
   NO → Continue
   ↓
5. Repeatable workflow (pattern detection)?
   YES → Use Agent Skill
   NO → Continue
   ↓
6. Lifecycle event automation?
   YES → Use Hook
   NO → Continue
   ↓
7. Sharing/distributing to team?
   YES → Use Plugin
   NO → Default to Slash Command (prompt)
```

**Critical Rule:** Always start with **Prompts** (implemented as Slash Commands). Master the primitive first before scaling to other components.

## Quick Reference: Decision Matrix

| Task Type | Component | Reason |
|-----------|-----------|---------|
| Repeatable pattern detection | Agent Skill | Domain-specific workflow |
| External data/service access | MCP Server | Integration point |
| Parallel/isolated work | Sub-Agent | Context isolation |
| Parallel workflow tasks | Sub-Agent | **Whenever you see "parallel", think sub-agents** |
| One-off task | Slash Command | Simple, direct |
| Lifecycle automation | Hook | Event-driven |
| Team distribution | Plugin | Packaging |

## When to Use Each Component

### Use Skills When

**Signal keywords:** "automatic," "repeat," "manage," "workflow"

**Criteria:**

- You have a **REPEAT** problem that needs **MANAGEMENT**
- Multiple related operations need coordination
- You want **automatic** behavior (agent-invoked)
- The problem domain requires orchestration of multiple components

**Example scenarios:**

- Managing git work trees (create, list, remove, merge, update)
- Detecting style guide violations across codebase
- Automatic PDF text extraction and processing
- Video processing workflows with multiple steps

**NOT for:**

- One-off tasks → Use Slash Command instead
- Simple operations → Use Slash Command instead
- Problems solved well by a single prompt → Don't over-engineer

**Remember:** Skills are for managing problem domains, not solving one-off tasks.

### Use Sub-Agents When

**Signal keywords:** "parallel," "scale," "bulk," "isolated," "batch"

**Criteria:**

- **Parallelization** is needed
- **Context isolation** is required
- Scale tasks and batch operations
- You're okay with losing context afterward
- Each task can run independently

**Example scenarios:**

- Comprehensive security audits
- Fix & debug tests at scale
- Parallel workflow tasks
- Bulk operations on multiple files
- Isolated research that doesn't pollute main context

**NOT for:**

- Tasks that need to share context → Use main conversation
- Sequential operations → Use Slash Command or Skill
- Tasks that need to spawn more sub-agents → Hard limit: no nesting

**Critical constraint:** You must be okay with losing context afterward. Sub-agent context doesn't persist in the main conversation (unless you use resumable sub-agents).

**Golden rule:** "Whenever you see parallel, you should always just think sub-agents. Nothing else supports parallel calling."

### Use Slash Commands When

**Signal keywords:** "one-off," "simple," "quick," "manual"

**Criteria:**

- One-off tasks
- Simple repeatable actions
- You're starting a new workflow
- Building the primitive before composing
- You want manual control over invocation

**Example scenarios:**

- Git commit messages (one at a time)
- Create UI component
- Run specific code generation
- Execute a well-defined task
- Quick transformations

**Philosophy:** "Have a strong bias towards slash commands. And then when you're thinking about composing many slash commands, sub-agents or MCPs, think about putting them in a skill."

**Remember:** Slash commands are the primitive foundation. Master these first before anything else.

### Use MCP Servers When

**Signal keywords:** "external," "database," "API," "service," "integration"

**Criteria:**

- External integrations are needed
- Data sources outside Claude Code
- Third-party services
- Database connections
- Real-time data access

**Example scenarios:**

- Connect to Jira
- Query databases (PostgreSQL, etc.)
- Fetch real-time weather data
- GitHub integration
- Slack integration
- Figma designs

**NOT for:**

- Internal orchestration → Use Skills instead
- Pure computation → Use Slash Command or Skill

**Clear rule:** External = MCP, Internal orchestration = Skills

**Context consideration:** MCP servers can "torch your context window" by loading all their context at startup, unlike Skills which use progressive disclosure.

### Use Hooks When

**Signal keywords:** "lifecycle," "event," "automation," "deterministic"

**Criteria:**

- Deterministic automation at lifecycle events
- Want to execute commands at specific moments
- Need to balance agent autonomy with deterministic control
- Workflow automation that should always happen

**Example scenarios:**

- Run linters before code submission
- Auto-format code after generation
- Trigger tests after file changes
- Capture context at specific points

**Philosophy:** "If you really want to scale, you need both" - agents AND deterministic workflows.

**Use for:** Adding determinism rather than always relying on the agent to decide.

### Use Plugins When

**Signal keywords:** "share," "distribute," "package," "team"

**Criteria:**

- Sharing/distributing to team
- Packaging multiple components together
- Reusable work across projects
- Team-wide extensions

**Example scenarios:**

- Distribute custom skills to team
- Bundle MCP servers for automatic start
- Share slash commands across projects
- Package hooks and configurations

**Philosophy:** "Plugins let you package and distribute these sets of work. This isn't super interesting. It's just a way to share and reuse cloud code extensions."

## Use Case Examples from the Field

Real examples with reasoning:

| Use Case | Component | Reasoning |
|----------|-----------|-----------|
| Automatic PDF text extraction | Agent Skill | Keyword "automatic", repeat behavior |
| Connect to Jira | MCP Server | External source |
| Comprehensive security audit | Sub-Agent | Scale, isolated context, not automatic |
| Generalized git commit messages | Slash Command | Simple one-step task |
| Query database | MCP Server | External data source (start here) |
| Fix/debug tests at scale | Sub-Agent | Parallel work, scale |
| Detect style guide violations | Agent Skill | Repeat behavior pattern |
| Fetch real-time weather | MCP Server | Third-party service integration |
| Create UI component | Slash Command | Simple one-off task |
| Parallel workflow tasks | Sub-Agent | Keyword "parallel" |

## Composition Rules and Boundaries

### What Can Compose What

**Skills (Top Compositional Layer):**

- ✅ Can use: MCP Servers
- ✅ Can use: Sub-Agents
- ✅ Can use: Slash Commands
- ✅ Can use: Other Skills
- ❌ Cannot: Nest sub-agents/prompts directly (must use SlashCommand tool)

**Slash Commands (Primitive + Compositional):**

- ✅ Can use: Skills (via SlashCommand tool)
- ✅ Can use: MCP Servers
- ✅ Can use: Sub-Agents
- ✅ Acts as: BOTH primitive AND composition point

**Sub-Agents (Execution Layer):**

- ✅ Can use: Slash Commands (via SlashCommand tool)
- ✅ Can use: Skills (via SlashCommand tool)
- ❌ CANNOT use: Other Sub-Agents (hard limit)

**MCP Servers (Integration Layer):**

- ℹ️ Lower level unit, used BY skills
- ℹ️ Not using skills
- ℹ️ Expose services to all components

### Critical Composition Rules

1. **Sub-Agents cannot nest** - No sub-agent spawning other sub-agents (prevents infinite nesting)
2. **Skills don't execute code** - They guide Claude to use available tools
3. **Slash commands can be invoked manually or via SlashCommand tool**
4. **Skills use the SlashCommand tool** to compose prompts and sub-agents
5. **No circular dependencies** - Skills can use other skills but cannot nest circularly

## The Proper Evolution Path

When building new capabilities, follow this progression:

### Stage 1: Start with a Prompt

**Goal:** Solve the basic problem

Create a simple prompt or slash command that accomplishes the core task.

**Example (Git Work Trees):** Create one work tree

```bash
/create-worktree feature-branch
```

**When to stay here:** The task is one-off or infrequent.

### Stage 2: Add Sub-Agent if Parallelism Needed

**Goal:** Scale to multiple parallel operations

If you need to do the same thing many times in parallel, use a sub-agent.

**Example (Git Work Trees):** Create multiple work trees in parallel

```bash
Use sub-agent to create work trees for: feature-a, feature-b, feature-c in parallel
```

**When to stay here:** Parallel execution is the only requirement, no orchestration needed.

### Stage 3: Create Skill When Management Needed

**Goal:** Bundle multiple related operations

When the problem grows to require management, create a skill.

**Example (Git Work Trees):** Manage work trees (create, list, remove, merge, update)

Now you have a cohesive work tree manager skill that:

- Creates new work trees
- Lists existing work trees
- Removes old work trees
- Merges work trees
- Updates work tree status

**When to stay here:** Most domain-specific workflows stop here.

### Stage 4: Add MCP if External Data Needed

**Goal:** Integrate external systems

Only add MCP servers when you need data from outside Claude Code.

**Example (Git Work Trees):** Query external repo metadata from GitHub API

Now your skill can query GitHub for:

- Branch protection rules
- CI/CD status
- Pull request information

**Final state:** Full-featured work tree manager with external integration.

## Common Decision Anti-Patterns

### ❌ Anti-Pattern 1: Converting All Slash Commands to Skills

**Mistake:** "I'm going to convert all my slash commands to skills because skills are better."

**Why wrong:** Skills are for repeatable workflows that need management, not simple one-off tasks. Slash commands are the primitive—you need them.

**Correct approach:** Keep slash commands for simple tasks. Only create a skill when you're managing a problem domain with multiple related operations.

### ❌ Anti-Pattern 2: Using Skills for One-Off Tasks

**Mistake:** "I need to create a UI component once, so I'll build a skill for it."

**Why wrong:** Skills are for repeat problems. One-off tasks should use slash commands.

**Correct approach:** Use a slash command for the one-off task. If you find yourself doing it repeatedly, then consider a skill.

### ❌ Anti-Pattern 3: Skipping the Primitive

**Mistake:** "I'm going to start by building a skill because it's more advanced."

**Why wrong:** If you don't master prompts, you can't build effective skills. Everything is prompts in the end.

**Correct approach:** Always start with a prompt. Build the primitive first. Scale up only when needed.

### ❌ Anti-Pattern 4: Using Sub-Agents When Context Matters

**Mistake:** "I'll use a sub-agent for this research task and then reference the findings later."

**Why wrong:** Sub-agent context is isolated. You lose it after the sub-agent finishes (unless using resumable sub-agents).

**Correct approach:** If you need the context later, do the work in the main conversation or use a resumable sub-agent.

### ❌ Anti-Pattern 5: Forgetting MCP is for External Only

**Mistake:** "I'll build an MCP server to orchestrate internal workflows."

**Why wrong:** MCP servers are for external integrations. Internal orchestration should use skills.

**Correct approach:** MCP = external, Skills = internal orchestration. Keep them separate.

## Decision Checklist

Before you start building, ask yourself:

**Basic Questions:**

- [ ] Have I started with a prompt? (Non-negotiable)
- [ ] Is this a one-off task or repeatable?
- [ ] Do I need external data or services?
- [ ] Is parallelization required?
- [ ] Am I okay losing context after execution?

**Composition Questions:**

- [ ] Am I trying to nest sub-agents? (Not allowed)
- [ ] Am I converting a simple slash command to a skill? (Probably wrong)
- [ ] Am I using MCP for internal orchestration? (Should use skills)
- [ ] Have I considered the evolution path? (Prompt → Sub-agent → Skill → MCP)

**Context Questions:**

- [ ] Will this torch my context window? (MCP consideration)
- [ ] Do I need progressive disclosure? (Skills benefit)
- [ ] Is context isolation critical? (Sub-agent benefit)
- [ ] Will I need this context later? (Don't use sub-agent)

## Summary: The Golden Rules

1. **Always start with prompts** - Master the primitive first
2. **"Parallel" keyword = Sub-Agents** - Nothing else supports parallel calling
3. **External = MCP, Internal = Skills** - Clear separation of concerns
4. **One-off = Slash Command** - Don't over-engineer
5. **Repeat + Management = Skill** - Only scale when needed
6. **Don't convert all slash commands to skills** - Huge mistake
7. **Skills compose upward, not downward** - Build from primitives

Remember The Core 4: Context, Model, Prompt, Tools. Master these fundamentals, and you'll master the compositional units.
