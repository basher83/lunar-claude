# Q&A Session Notes

## Questions

### Three Questions for the Original Author

#### 1. Progression and Decision Patterns

**Question:**

> "You mentioned starting with slash commands for simple tasks and progressing to
> skills for domain-specific problems. Could you walk through a real-world example
> where you started with a slash command and eventually evolved it into a full skill
> with sub-agents and MCP integrations? What were the specific pain points or
> thresholds that triggered each evolution step?"

**Why this matters:**

Understanding the progression from simple to complex would reveal:

- Practical decision criteria for when to upgrade from one component to another
- Real indicators that signal "this needs to be a skill now, not just a command"
- How complexity compounds and when orchestration becomes necessary

#### 2. Composition Strategies and Boundaries

**Question:**

> "When designing a skill that orchestrates multiple components (sub-agents, slash
> commands, MCP servers), how do you decide which logic belongs in the skill's
> instructions versus delegating to a sub-agent versus creating a separate slash
> command? Are there principles or patterns you follow to maintain clear boundaries?"

**Why this matters:**

This would clarify:

- Design principles for effective decomposition
- Where responsibilities should live in the architecture
- How to avoid over-engineering or under-engineering solutions
- Patterns for maintainable orchestration

#### 3. Anti-Patterns and Common Pitfalls

**Question:**

> "What are the most common mistakes or anti-patterns you've seen (or made yourself)
> when working with these components? For example, skills that try to do too much,
> sub-agents being used when a simple command would suffice, or MCP servers being
> chosen when a script would work better?"

**Why this matters:**

This would reveal:

- What not to do (often more valuable than what to do)
- Edge cases where the abstractions break down
- Real-world lessons learned from production use
- Guidance for avoiding common traps when architecting solutions

## Answers

### 1. Real-World Progression: Git Work Trees Management

Here's a real-world progression using the example of managing git work trees. The
concrete pain points pushed each evolution step.

#### Step 1: Slash Command (The Primitive)

**What I started with:**

A simple, one-off slash command to create a single git work tree and return the
result (branch name, path, ports, etc.).

**Why it made sense at first:**

It's the easiest path to get something done quickly. A single, repeatable task that
you can invoke manually.

**Pain points/thresholds that surfaced:**

- You begin repeating the same prompt logic for different tasks (branch naming, port
  assignment, environment setup) and it feels brittle
- You only solve one task at a time; you don't yet have a reusable workflow for
  multiple related steps
- No easy way to track or audit what happened across multiple runs or to reuse the
  pattern in other projects

**Takeaway:**

Prompts/slash commands are the right starting point for simple, one-off tasks.
You're still in "craft and ship" mode, not "scale and reuse."

#### Step 2: Introduce a Sub Agent for Parallelism and Isolation

**What changed:**

I split the work into parallelizable pieces and used a sub agent to run those pieces
in a separate context.

**Why this step made sense:**

When you start dealing with multiple work trees simultaneously, doing it in one main
context becomes risky (context window blows up, tangled results, and harder
debugging).

**Pain points/thresholds that surfaced:**

- **Need to scale the task:** You want to create/read/update/delete several work
  trees in one go, not just one
- **Context isolation becomes valuable:** You don't want the main agent's context to
  be polluted or to lose focus on the primary task
- **Parallel execution is desirable:** You want to run independent operations at the
  same time for speed

**What the sub agent buys you:**

- Separate context for each parallel task
- Ability to run in parallel without leaking state back into the main agent too early

**Takeaway:**

If you need parallelism and context isolation, a sub agent is the right next step.
It's still a single workflow, but now you can break it into parallel tasks.

#### Step 3: Move to an Orchestration Pattern with a Skill

**What changed:**

I wrapped the whole domain problem—the management of git work trees—into a dedicated
Skill. The Skill orchestrates multiple components: prompts/slash commands, sub
agents, and possibly MCP integrations.

**Why this step made sense:**

The problem becomes a reusable, domain-specific workflow rather than a single action.
You want to reuse the same pattern across projects, teams, or environments.

**Pain points/thresholds that surfaced:**

- **Repetition and maintenance:** I was duplicating the same orchestration logic for
  each new repo or project
- **Reusability:** I wanted a single, versioned unit I could ship, test, and update
  across different contexts
- **Orchestration over raw prompts:** The end-to-end flow now spans multiple steps
  (setup, creation, validation, cleanup, summary), not just a single task

**What the Skill provides:**

- A dedicated directory structure and a repeatable workflow for managing work trees
- The ability to compose multiple building blocks: prompts/slash commands for
  primitive tasks, sub agents for parallel work, and MCP servers if external
  tooling/data is needed
- A higher-level abstraction that encapsulates domain expertise (the "work-tree
  management" domain) and can be reused across projects

**Takeaway:**

When you have a domain-specific, repeatable problem, a Skill is the right container
to orchestrate the entire workflow, not just a single action or a single parallel
task.

#### Optional Evolution: MCP Integrations Within the Skill

**What could happen:**

If the domain requires external data or tools (e.g., querying a versioned repository
service, CI/CD data, or external metadata about repos), you can wire MCP servers into
the Skill.

**Why it helps:**

The Skill can now pull in external information or trigger external tooling as part of
the repeatable workflow, still orchestrated from the same domain-specific unit.

**Pain points/thresholds that trigger this:**

- Need for external context or actions that aren't available locally
- You want the Skill to present a unified, domain-specific API to your agent(s)
  without leaking external tool details into the main flow

#### Key Thresholds That Typically Trigger the Evolution

- **From slash command to sub agent:** When you need parallelism and isolation to
  scale the task beyond a single run
- **From sub agent to skill:** When the problem becomes domain-specific and
  repeatable, and you want a reusable, end-to-end workflow that can be composed from
  primitives (prompts, sub agents, MCPs) but managed as a single unit
- **From Skill to MCP within a Skill:** When you need external data or tools as part
  of the domain workflow, to keep the orchestration within the single reusable domain
  unit

#### How to Think About It in Practice

1. Start small with a slash command to prove the basic prompt works
2. If you find yourself needing to run multiple related tasks in parallel, introduce
   a sub agent for parallelism and context isolation
3. If you're repeatedly solving the same domain problem in multiple places, wrap it
   in a Skill to provide a reusable, orchestrated workflow
4. If you need external data or tools, integrate MCP servers inside the Skill to keep
   the domain workflow cohesive and reusable
5. Always design with the primitive building blocks in mind: prompts/slash commands
   are the base, sub agents add parallelism and isolation, MCPs add external
   capability, and Skills orchestrate the whole thing into repeatable domain-specific
   solutions

### 2. Composition Strategies and Boundaries

**Short answer:**

Follow a small set of practical boundaries that align with how the video describes
skills, sub-agents, and slash commands as building blocks. Use the primitive (slash
commands) for simple tasks, use sub-agents when you need parallelism or isolated
context, and use a Skill to orchestrate a domain-specific, repeatable workflow that
may combine those primitives (and MCP servers) into a coherent process.

#### Guiding Principles and Patterns

##### Start with the Primitive and Climb Only as Needed

- Use a slash command when you have a one-off task or a simple, repeatable action
- Treat it as the basic building block you'll compose from later

##### Use Sub-Agents to Solve Parallelism and Isolation Needs

- When you need to run multiple pieces of work in parallel or keep their contexts
  separate from the main agent, move to a sub-agent
- Sub-agents are ideal for scaling a task that would otherwise blow up the main
  context window or risk cross-contamination of state
- **Pattern:** Decompose the complex task into parallelizable subtasks, delegate each
  to a sub-agent, then aggregate results

##### Use a Skill to Encapsulate Domain-Specific, Repeatable Workflows

- When you find yourself solving the same, repeatable problem across multiple
  projects or contexts, wrap it in a Skill
- A Skill is a dedicated directory/structure that orchestrates multiple building
  blocks (prompts/slash commands, sub-agents, MCP servers) into a cohesive workflow
- **Pattern:** A domain-specific orchestration layer that composes primitives and/or
  other capabilities to deliver a repeatable outcome

##### Clear Boundaries for Each Type

- **Slash commands:** The primitive prompts you invoke manually. Minimal logic; focus
  on reliable, reusable prompts that can be invoked directly
- **Sub-agents:** Isolated, parallelizable tasks with separate contexts. Use them
  where parallelism and context isolation are required
- **MCP servers:** External data/tools integration. Use them when you need to fetch
  or act on external services/data as part of the workflow
- **Skills:** Orchestration of a domain-specific workflow. Use them when you want to
  reuse a multi-step, repeatable pattern that may leverage prompts, sub-agents, and
  MCPs

##### Boundary Criteria to Apply in Practice

- **Is the task simple and one-off?** Put it in a slash command or a single prompt
- **Do you need to run several related tasks in parallel with isolated contexts?** Put
  those in a sub-agent(s) and have the main flow orchestrate them
- **Is this a repeating, domain-specific process you want to reuse and version as a
  unit?** Encapsulate it in a Skill
- **Does the task require external tools/data as part of the workflow?** Integrate MCP
  servers within the Skill (or within subordinated building blocks) to keep the
  domain workflow cohesive

##### Composition Discipline

- Skills should orchestrate, not duplicate, the primitive logic. They should call
  prompts/slash commands, sub-agents, and MCPs as needed to deliver the end-to-end
  domain outcome
- Avoid moving all logic into a Skill if a single prompt or a small sub-agent
  suffices. Use the right tool for the job to keep maintenance simple

##### Evolution Guideline (From the Video)

- If a task grows beyond a single action and starts requiring multiple steps, results
  aggregation, or reuse across contexts, elevate it from a slash command to a Skill
- If the task demands parallel work or separate contexts, introduce or expand
  sub-agents within the Skill
- If external data/tools are needed, wire MCP integrations into the Skill so the
  domain workflow remains cohesive

#### Practical Decision Checklist

- **Is this a single, repeatable action?** → Slash command
- **Do I need parallelism or isolated contexts?** → Sub-agent
- **Is this a domain-specific, reusable workflow spanning multiple steps?** → Skill
- **Does it require external data/tools to complete?** → MCP server usage inside the
  Skill (or via components the Skill orchestrates)

### 3. Anti-Patterns and Common Pitfalls

Here are the common mistakes and anti-patterns I see (and some I've made) when
mixing slash commands, sub-agents, MCP servers, and skills. I've grouped them by
type and added quick remedies.

#### Skills Problems

##### Skill Tries to Do Everything

**Symptom:**

A single skill handles dozens of unrelated tasks (git work trees, video processing,
external data fetches, UI generation) in one place.

**Why it's bad:**

Hard to maintain, test, version, and reuse. Becomes a monolith.

**Remedy:**

Start with domain-specific scope. If you find yourself adding unrelated capabilities,
split into separate skills or create smaller, focused skills that can be composed.

##### Not Versioning or Documenting a Skill

**Symptom:**

A "magic" skill you edited in place without clear inputs/outputs or a changelog.

**Why it's bad:**

Hard for others to reuse or for you to audit changes.

**Remedy:**

Use a clear Skill.yaml or definition, version it, and document its inputs, outputs,
and dependencies.

##### Using a Skill to Wrap a Single Prompt

**Symptom:**

A skill that's essentially just a wrapper around one prompt with no orchestration.

**Why it's problematic:**

Misses the real value of skills (orchestration, reuse, domain structure).

**Remedy:**

If a single prompt suffices, keep it as a slash command or small sub-agent. Elevate
to a Skill only when you have a repeatable workflow.

#### Sub-Agents Anti-Patterns

##### Sub-Agents When a Simple Command Would Suffice

**Symptom:**

A single small task is put into a sub-agent, incurring context switching and
management overhead.

**Remedy:**

Use a slash command for simple tasks; reserve sub-agents for parallelizable or
context-isolated work.

##### Nesting Too Many Sub-Agents

**Symptom:**

A workflow creates sub-agents within sub-agents, leading to complex, hard-to-trace
execution traces.

**Remedy:**

Keep the nesting shallow. If you need more parallelism, consider restructuring as a
Skill orchestrating a smaller set of sub-agents.

##### Sub-Agent Results Leaking Into Main Context

**Symptom:**

You don't clearly aggregate or validate sub-agent outputs before continuing, causing
inconsistent state.

**Remedy:**

Define explicit aggregation/merge steps and fail-safes for sub-agent outputs.

#### MCP Servers Anti-Patterns

##### Using MCPs Where a Script Would Do

**Symptom:**

Calling external services for every small task rather than bundling logic locally.

**Remedy:**

Use MCP servers when you truly need external data/tools or when you want to expose
external capabilities as part of a reusable workflow. For simple tasks, a local
script or prompt is often cheaper and clearer.

##### Too Many External Calls Inside a Skill

**Symptom:**

A Skill that crawls multiple MCPs in sequence, slowing feedback or making offline
development hard.

**Remedy:**

Isolate external interactions behind clear interfaces; mock or stub MCP calls during
development; minimize external dependencies in early stages.

#### General Design and Boundary Issues

##### Blurring Boundaries Between Components

**Symptom:**

A single piece of logic that could live in a slash command, a sub-agent, and a skill
all at once, but ends up in all three in different places.

**Remedy:**

Map a clear boundary first: slash commands = primitive prompts; sub-agents =
parallel/isolated tasks; skills = domain-specific orchestration with optional MCPs.
Move logic to the lowest appropriate layer.

##### Not Thinking in Terms of Repeatable Domain Workflows

**Symptom:**

Building ad-hoc solutions for one project and duplicating code across teams.

**Remedy:**

Capture repeatable patterns as skills with a documented API and inputs/outputs.

##### Missing Versioning and Tests for Skills and Workflows

**Symptom:**

Breaking changes in a Skill break multiple dependent projects.

**Remedy:**

Version skills, write tests for orchestration paths, and document breaking changes.

##### Over-Reliance on Prompts as the Only "Logic"

**Symptom:**

All decisions, branching, and flow are encoded in prompts without clear structure.

**Remedy:**

Treat prompts as tokens-out, not as the sole logic; encapsulate branching/flow
decisions in sub-agents or Skill orchestrations with defined inputs/outputs.

##### Ignoring Observability

**Symptom:**

Little to no logging of which skill, sub-agent, or MCP was invoked, making debugging
hard.

**Remedy:**

Add structured logging, hooks, and output styles to trace which component ran and
what data it produced.

#### Practical Patterns to Avoid or Fix

##### Prefer Composition Over Duplication

Build a small primitive (slash command) and re-use it inside sub-agents and skills,
rather than duplicating the same prompt logic.

##### Align with the "Domain-First" Approach

If your goal is a repeatable workflow across projects, your boundary should be a
Skill. If it's a unique one-off task, keep it as a slash command or a small
sub-agent.

##### Use Explicit Interfaces

Define inputs/outputs for each component (slash command, sub-agent, MCP call, skill).
This makes orchestration predictable and testable.

##### Keep Parallelism Purposeful

Only introduce sub-agents for tasks that truly benefit from parallel execution or
isolated contexts. Otherwise, stick to a single prompt or a simple command to reduce
complexity.

##### Incremental Evolution

Start with a slash command → add a sub-agent if parallelism/isolation is needed →
create a Skill when you have a repeatable domain workflow → add MCPs inside the Skill
if external data/tools are required. Don't skip steps.

## Summary

### Key Capabilities and Distinctions

The speaker identifies four primary capabilities—skills, sub agents, slash commands,
and MCP servers—and contrasts their roles:

- **Skills:** Agent-triggered, context-efficient, with progressive disclosure
  (metadata, instructions, and resources). They are highly modular and best suited
  for automatic, repeatable behaviors that require a dedicated solution and a
  structured, reusable workflow.
- **Sub agents:** Excelling at parallelization and isolated contexts; ideal when you
  need to run tasks in parallel without preserving the broader agent context. They
  protect context windows but sacrifice persistence.
- **Custom slash commands:** Manual triggers, acting as the primitive unit of input
  and prompt construction. They are the foundational building blocks and emphasize
  prompt mastery as the core skill.
- **MCP servers:** External integrations that connect agents to external tools and
  data sources, suitable for bundling services and exposing capabilities to agents.

### Modularity and Composition

Skills claim a higher degree of modularity due to a dedicated directory structure,
enabling repeatable solutions that agents can invoke. However, they can be composed
with prompts, other skills, MCP servers, and sub agents, creating a complex but
powerful composition graph. Slash commands function as both primitives and
composition points since they can trigger skills, MCPs, and sub agents.

### Use-Case Mapping

The speaker provides heuristic mappings to decide which feature fits specific tasks:

- Automatically extract text/data from PDFs → **skill**
- Connect to Jira → **MCP server**
- Comprehensive security audit (scale, timed trigger) → **sub agent**
- Generalized, one-off tasks (e.g., a simple data fetch) → **slash command**
- Querying a database → **MCP server** (initial step)
- Detecting style violations → **skill** (repeatable pattern)
- Real-time weather data from APIs → **MCP server**
- Create a UI component → **simple slash command** (one-off)

### Parallelization Guidance

When parallelism is required, sub agents are the appropriate vehicle; otherwise, a
single prompt (or slash command) may suffice. Skills should not be treated as a
blanket replacement for sub agents or slash commands; instead, they serve as a
higher-level abstraction for repeatable workflows.

### Compositional Strategy

The speaker argues for a tiered approach: start with a prompt (the primitive), evolve
to a sub agent for parallelizable work, and consider a skill for scalable, repeatable
problem-domain solutions. Prompt mastery remains foundational; the prompt is the
essential instrument behind every feature.

### Reality Checks and Critiques

While acknowledging the value of skills, the speaker criticizes the tendency to
convert all slash commands into skills. They caution that prompts remain the most
vital unit of knowledge work, and reliability in orchestrating multiple skills in
sequence deserves more testing and clarity. The emotional verdict: skills are useful,
but they do not replace existing primitives; they organize and scale repeatable
patterns.

## Outro

### Guiding Recommendation

Maintain a bias toward custom slash commands for foundational work, and deploy sub
agents or skills when parallelization or repeatable domain expertise is required. Use
MCP servers for external data integration, and treat skills as an advanced
composition layer rather than a universal substitute.

### Final Takeaway

The prompt remains the core unit of action; understand context, model, prompt, and
tools, and compose them judiciously. A disciplined, modular approach—rooted in
prompts and escalated through sub agents and skills when warranted—will maximize
reliability and scalability in agent-driven development.
