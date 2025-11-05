# Core Concepts: Claude Code Architecture

## Table of Contents

- [Executive Summary](#executive-summary)
- [The Core 4 Framework](#the-core-4-framework)
- [Component Definitions](#component-definitions)
  - [Skills](#skills)
  - [MCP Servers (External Data Sources)](#mcp-servers-external-data-sources)
  - [Sub-Agents](#sub-agents)
  - [Slash Commands (Custom Prompts)](#slash-commands-custom-prompts)
- [Compositional Hierarchy](#compositional-hierarchy)
- [Progressive Disclosure Architecture](#progressive-disclosure-architecture)
  - [Three-Level Loading Mechanism](#three-level-loading-mechanism)
- [How They Relate](#how-they-relate)
- [When to Use Each Component](#when-to-use-each-component)
  - [Use Skills When](#use-skills-when)
  - [Use Sub-Agents When](#use-sub-agents-when)
  - [Use Slash Commands When](#use-slash-commands-when)
  - [Use MCP Servers When](#use-mcp-servers-when)
- [Critical Insights and Warnings](#critical-insights-and-warnings)
  - [1. Don't Convert All Slash Commands to Skills](#1-dont-convert-all-slash-commands-to-skills)
  - [2. Skills Are Not Replacements](#2-skills-are-not-replacements)
  - [3. One-Off Tasks Don't Need Skills](#3-one-off-tasks-dont-need-skills)
  - [4. Master the Fundamentals First](#4-master-the-fundamentals-first)
  - [5. Prompts Are Non-Negotiable](#5-prompts-are-non-negotiable)
- [Skills: Honest Assessment](#skills-honest-assessment)
  - [Pros](#pros)
  - [Cons](#cons)
- [Evolution Path](#evolution-path)
- [Context Management](#context-management)
- [Key Quotes for Reference](#key-quotes-for-reference)
- [Summary](#summary)

## Executive Summary

Claude Code's architecture is built on a fundamental principle: **prompts are the primitive foundation** for everything. This document provides the authoritative reference for understanding Skills, Sub-Agents, MCP Servers, and Slash Commands—how they work, how they relate, and how they compose.

**Key insight:** Skills are powerful compositional units but should NOT replace the fundamental building blocks (prompts, sub-agents, MCPs). They orchestrate these primitives to solve repeat problems in an agent-first way.

## The Core 4 Framework

**Everything comes down to four pieces:**

1. **Context**
2. **Model**
3. **Prompt**
4. **Tools**

> "If you understand these, if you can build and manage these, you will win. Why is that? It's because every agent is the core 4. And every feature that every one of these agent coding tools is going to build is going to build directly on the core 4. This is the foundation."

This is the thinking framework for understanding and building with Claude Code.

## Component Definitions

### Skills

**What they are:** A dedicated, modular solution that packages a domain-specific capability for autonomous, repeatable workflows.

**Triggering:** Agent-invoked. Claude autonomously decides when to use them based on your request and the Skill's description. You don't explicitly invoke them—they activate automatically when relevant.

**Context and structure:** High modularity with a dedicated directory structure. Supports progressive disclosure (metadata, instructions, resources) and context persistence within the skill's scope.

**Composition:** Can use prompts, other skills, MCP servers, and sub-agents. They sit on top of other capabilities and can orchestrate them through instructions.

**Best use cases:** Automatic or recurring behavior that you want to reuse across workflows (e.g., a work-tree manager that handles create, list, remove, merge, update operations).

**Not a replacement for:** MCP servers, sub-agents, or slash commands. Skills are a higher-level composition unit that coordinates these primitives.

**Critical insight:** Skills don't directly execute code; they provide declarative guidance that coordinates multiple components. When a skill activates, Claude reads the instructions and uses available tools to follow the workflow.

### MCP Servers (External Data Sources)

**What they are:** External data sources or tools integrated into agents through the Model Context Protocol (MCP).

**Triggering:** Typically invoked as needed, often by skills or prompts.

**Context:** They don't bundle a workflow; they connect to external systems and bring in data/services.

**Composition:** Can be used within skills or prompts to fetch data or perform actions with external tools.

**Best use cases:** Connecting to Jira, databases, GitHub, Figma, Slack, and hundreds of other external services. Bundling multiple services together for exposure to the agent.

**Practical examples:**
- Implement features from issue trackers: "Add the feature described in JIRA issue ENG-4521"
- Query databases: "Find emails of 10 random users based on our Postgres database"
- Integrate designs: "Update our email template based on new Figma designs"
- Automate workflows: "Create Gmail drafts inviting these users to a feedback session"

**Clear differentiation:** MCP = external integration, Skills = internal orchestration.

**Plugin integration:** Plugins can bundle MCP servers that start automatically when the plugin is enabled, providing tools and integrations team-wide.

### Sub-Agents

**What they are:** Isolated workflows with separate contexts that can run in parallel.

**Triggering:** Invoked by the main agent to do a task in parallel without polluting the main context.

**Context and isolation:** Each sub-agent uses its own context window separate from main conversation. This prevents context pollution and enables longer overall sessions.

**Composition:** Can be used inside skills and prompts, but you **cannot nest sub-agents inside other sub-agents** (hard limit to prevent infinite nesting).

**Best use cases:** Parallelizable, isolated tasks (e.g., bulk/scale tasks like fixing failing tests, batch operations, comprehensive audits).

**Critical constraint:** You must be okay with losing context afterward—sub-agent context doesn't persist in the main conversation.

**Resumable sub-agents:** Each execution gets a unique `agentId` stored in `agent-{agentId}.jsonl`. Sub-agents can be resumed to continue previous conversations, useful for:
- Long-running research across multiple sessions
- Iterative refinement without losing context
- Multi-step workflows with maintained context

**Model selection:** Sub-agents support `model` field to specify model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` to use the main conversation's model.

### Slash Commands (Custom Prompts)

**What they are:** The primitive, reusable prompts you invoke manually. The closest compositional unit to "bare metal agent plus LLM."

**Triggering:** Manual triggers by a user (or by a higher-level unit like a sub-agent or skill via the SlashCommand tool).

**Context:** They're the most fundamental unit. You should master prompt design here.

**Composition:** Can be used alone or as building blocks inside skills, sub-agents, and MCPs. Acts as BOTH primitive AND composition point.

**Best use cases:** One-off tasks or basic, repeatable prompts. The starting point for building more complex capabilities.

**Critical principle:**

> "Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming. If you don't know how to build and manage prompts, you will lose."

**SlashCommand tool:** Claude can programmatically invoke custom slash commands via the `SlashCommand` tool during conversations. Both skills and sub-agents compose prompts using this tool.

**Advanced features:**
- **Bash execution:** Use `!` prefix to execute bash commands before the slash command runs
- **File references:** Use `@` prefix to include file contents
- **Arguments:** Support `$ARGUMENTS` for all args or `$1`, `$2` for individual parameters
- **Frontmatter:** Control `allowed-tools`, `model`, `description`, `argument-hint`

**Comparison to Skills:**

| Aspect         | Slash Commands              | Skills                              |
|----------------|-----------------------------|-------------------------------------|
| **Complexity** | Simple prompts              | Complex capabilities                |
| **Structure**  | Single .md file             | Directory with SKILL.md + resources |
| **Discovery**  | Explicit (`/command`)       | Automatic (context-based)           |
| **Files**      | One file only               | Multiple files, scripts, templates  |

## Compositional Hierarchy

**Skills sit at the top of the composition hierarchy:**

```text
Skills (Top Compositional Layer)
  ├─→ Can use: MCP Servers
  ├─→ Can use: Sub-Agents
  ├─→ Can use: Slash Commands
  └─→ Can use: Other Skills

Slash Commands (Primitive + Compositional)
  ├─→ Can use: Skills (via SlashCommand tool)
  ├─→ Can use: MCP Servers
  ├─→ Can use: Sub-Agents
  └─→ Acts as BOTH primitive AND composition point

Sub-Agents (Execution Layer)
  ├─→ Can use: Slash Commands (via SlashCommand tool)
  ├─→ Can use: Skills (via SlashCommand tool)
  └─→ CANNOT use: Other Sub-Agents (hard limit)

MCP Servers (Integration Layer)
  └─→ Lower level unit, used BY skills, not using skills
```

**Key principle:** Skills provide **coordinated guidance** for repeatable workflows. They orchestrate other components through instructions, not by executing code directly.

**Verified restrictions:**
- Sub-agents cannot nest (no sub-agent spawning other sub-agents)
- Skills don't execute code; they guide Claude to use available tools
- Slash commands can be invoked manually or via `SlashCommand` tool

## Progressive Disclosure Architecture

### Three-Level Loading Mechanism

Skills use a sophisticated loading system that minimizes context usage:

**Level 1: Metadata (always loaded)** - ~100 tokens per skill
- YAML frontmatter with `name` and `description`
- Loaded at startup into system prompt
- Enables discovery without context penalty
- You can install many Skills with minimal overhead

**Level 2: Instructions (loaded when triggered)** - Under 5k tokens
- Main SKILL.md body with procedural knowledge
- Read from filesystem via bash when skill activates
- Only enters context when the skill is relevant
- Contains workflows, best practices, guidance

**Level 3: Resources (loaded as needed)** - Effectively unlimited
- Additional markdown files, scripts, templates
- Executed via bash without loading contents into context
- Scripts provide deterministic operations efficiently
- No context penalty for bundled content that isn't used

**Example skill structure:**

```text
work-tree-manager/
├── SKILL.md              # Main instructions (Level 2)
├── reference.md          # Detailed reference (Level 3)
├── examples.md           # Usage examples (Level 3)
└── scripts/
    ├── validate.py       # Utility script (Level 3, executed)
    └── cleanup.py        # Cleanup script (Level 3, executed)
```

When this skill activates:
1. Claude already knows the skill exists (Level 1 metadata pre-loaded)
2. Claude reads SKILL.md when the skill is relevant (Level 2)
3. Claude reads reference.md only if needed (Level 3)
4. Claude executes scripts without loading their code (Level 3)

**Key advantage:** Unlike MCP servers which load all context at startup, Skills are extremely context-efficient. Progressive disclosure means only relevant content occupies the context window at any given time.

## How They Relate

**Prompts / slash commands are the primitive building blocks.**

- Master these first before anything else
- "Everything is a prompt in the end. It's tokens in, tokens out."
- Strong bias towards slash commands for simple tasks

**Sub-agents are for isolated, parallelizable tasks with separate contexts.**

- Use when you see the keyword "parallel"
- Nothing else supports parallel calling
- Critical for scale tasks and batch operations

**MCP servers connect to external systems and data sources.**

- Very little overlap with Skills
- These are fully distinct components
- Clear separation: external (MCP) vs internal (Skills)

**Skills are higher-level, domain-specific bundles that orchestrate or compose prompts, sub-agents, and MCP servers to solve repeat problems.**

- Use for MANAGEMENT problems, not one-off tasks
- Keywords: "automatic," "repeat," "manage"
- Don't convert all slash commands to skills—this is a huge mistake

## When to Use Each Component

### Use Skills When

- You have a **REPEAT** problem that needs **MANAGEMENT**
- Multiple related operations need coordination
- You want **automatic** behavior
- Example: Managing git work trees (create, list, remove, merge, update)

**Not for:**
- One-off tasks
- Simple operations
- Problems solved well by a single prompt

### Use Sub-Agents When

- **Parallelization** is needed
- **Context isolation** is required
- Scale tasks and batch operations
- You're okay with losing context afterward

**Signal words:** "parallel," "scale," "bulk," "isolated"

### Use Slash Commands When

- One-off tasks
- Simple repeatable actions
- You're starting a new workflow
- Building the primitive before composing

**Remember:** "Have a strong bias towards slash commands."

### Use MCP Servers When

- External integrations are needed
- Data sources outside Claude Code
- Third-party services
- Database connections

**Clear rule:** External = MCP, Internal orchestration = Skills

## Critical Insights and Warnings

### 1. Don't Convert All Slash Commands to Skills

> "There are a lot of engineers right now that are going all in on skills. They're converting all their slash commands to skills. I think that's a huge mistake."

Keep your slash commands. They are the primitive foundation.

### 2. Skills Are Not Replacements

> "It is very clear this does not replace any existing feature or capability. It is a higher compositional level."

Skills complement other components; they don't replace them.

### 3. One-Off Tasks Don't Need Skills

> "If you can do the job with a sub-agent or custom slash command and it's a one-off job, do not use a skill. This is not what skills are for."

Use the right tool for the job. Not everything needs a skill.

### 4. Master the Fundamentals First

> "When you're starting out, I always recommend you just build a prompt. Don't build a skill. Don't build a sub-agent. Don't build out an MCP server. Keep it simple. Build a prompt."

Start simple. Build upward from primitives.

### 5. Prompts Are Non-Negotiable

> "Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming."

Everything comes back to prompts. Master them first.

## Skills: Honest Assessment

### Pros

1. **Agent-invoked** - Dial up the autonomy knob to 11
2. **Context protection** - Progressive disclosure unlike MCP servers
3. **Dedicated file system pattern** - Logically compose and group skills together
4. **Composability** - Can compose other elements or features
5. **Agentic approach** - Agent just does the right thing

**Biggest value:** "Dedicated isolated file system pattern" + "agent invoked"

### Cons

1. **Doesn't go all the way** - No first-class support for embedding prompts and sub-agents directly in skill directories (must use SlashCommand tool to compose them)

2. **Reliability in complex chains is uncertain** - "Will the agent actually use the right skills when chained? I think individually it's less concerning but when you stack these up... how reliable is that?"

3. **Limited innovation** - Skills are effectively "curated prompt engineering plus modularity." The real innovation is having a dedicated, opinionated way to operate agents.

**Rating:** "8 out of 10"

**Bottom line:** "Having a dedicated specific way to operate your agents in an agent first way is still powerful."

## Evolution Path

The proper progression for building with Claude Code:

1. **Start with a prompt/slash command** - Solve the basic problem
2. **Add sub-agent if parallelism needed** - Scale to multiple parallel operations
3. **Create skill when management needed** - Bundle multiple related operations
4. **Add MCP if external data needed** - Integrate external systems

**Example: Git Work Trees**

- **Prompt:** Create one work tree ✓
- **Sub-agent:** Create multiple work trees in parallel ✓
- **Skill:** Manage work trees (create, list, remove, merge, update) ✓
- **MCP:** Query external repo metadata (if needed) ✓

## Context Management

**Progressive Disclosure (Skills):**

Skills are very context efficient. Three levels of progressive disclosure ensure only relevant content is loaded:
1. Metadata level (always in context, ~100 tokens)
2. Instructions (loaded when triggered, <5k tokens)
3. Resources (loaded as needed, effectively unlimited)

**Context Isolation (Sub-Agents):**

Sub-agents isolate and protect your context window by using separate contexts for each task. This is what makes sub-agents great for parallel work—but you must be okay with losing that context afterward.

**Context Explosion (MCP Servers):**

Unlike Skills, MCP servers can "torch your context window" by loading all their context at startup. This is a tradeoff for immediate availability of external tools.

## Key Quotes for Reference

1. **On Prompts:**
   > "The prompt is the fundamental unit of knowledge work and of programming."

2. **On Skills vs Prompts:**
   > "If you can do the job with a sub agent or custom slash command and it's a one-off job, do not use a skill."

3. **On Composition:**
   > "Skills at the top of the composition hierarchy... can compose everything into a skill, but you can also compose everything into a slash command."

4. **On The Core 4:**
   > "Everything comes down to just four pieces... context, model, prompt, and tools."

5. **On Skills' Purpose:**
   > "Skills offer a dedicated solution, right? An opinionated structure on how to solve repeat problems in an agent first way."

## Summary

**Start simple:** Build prompts first.

**Compose upward:** Prompts → Skills (not Skills → prompts as primary).

**Use the right tool:** Not everything needs a skill.

**Master The Core 4:** Context, Model, Prompt, Tools—these are the foundation.

**Remember:** Skills are powerful compositional units for repeat problems, but prompts remain the fundamental primitive. Build from this foundation, and compose upward as complexity requires.
