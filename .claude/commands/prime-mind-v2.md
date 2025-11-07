---
description: Essential workflow and architectural guidelines for working in lunar-claude repository
---

# Working Together in Lunar-Claude

Greetings! I'm basher83, and I prefer to be called by name rather than "user"—it feels more collaborative than transactional. This command establishes how we work together and the foundational system that makes our collaboration powerful.

## The Challenge We're Solving

The lunar-claude repository is unique: **we're building the very infrastructure** (plugins, skills, agents, hooks) that we need to reason about. This creates a compounding challenge:

- Each session builds on previous architectural decisions
- Without memory, we'd re-litigate the same composition decisions repeatedly
- We need consistent, informed decisions that compound over time

## Your First Steps (Start Here)

When beginning ANY task in this repository, follow this sequence:

1. **Search past conversations first** - Use `episodic-memory:remembering-conversations` to recover context and past decisions before starting new work
2. **Check for relevant skills** - Use `using-superpowers` to identify which skills apply to your current task
3. **Apply architectural frameworks** - When designing/building Claude Code components, use `multi-agent-composition` to make informed decisions

This creates a self-reinforcing cycle: **memory → discipline → good decisions → more learnings → better memory**.

## The Three Foundational Skills

These three skills work together to create the system:

### 1. episodic-memory:remembering-conversations

**What it does:** Recovers past decisions, patterns, and context from previous sessions

**When to use:** At the start of every task—search for related past work before beginning

**Why it matters:** Provides historical context that informs both finding the right skill AND making the right composition decisions

### 2. using-superpowers

**What it does:** Ensures we check for and use relevant skills, follow workflows, don't over-rationalize

**When to use:** Before starting work—check which skills apply to your task

**Why it matters:** The mandatory workflow layer that prevents us from rationalizing our way out of using established patterns

### 3. multi-agent-composition

**What it does:** Provides frameworks for deciding between skills/agents/hooks/commands when building components

**When to use:** When designing or building Claude Code components (plugins, skills, agents, hooks)

**Why it matters:** Helps make the right architectural choices about which component types to use

## How They Work Together

The workflow cycle:

1. **Memory** helps identify which skills apply and what patterns to follow
2. **Discipline** ensures we actually use those skills (don't skip steps)
3. **Architecture** guides making good compositional decisions
4. **All work gets archived** automatically, enriching future context

## Why This Compounds

Every conversation makes the next one smarter. For lunar-claude specifically:

- You're building infrastructure that you need to reason about
- Each session builds on previous architectural decisions
- Without memory, you'd re-litigate the same decisions repeatedly
- With memory + discipline + composition frameworks = consistent, informed decisions

The system compounds: every conversation makes the next one smarter.

## Deeper Context (Available When Ready)

If you find yourself wondering about:

- How this system emerged and why it works
- The metacognitive principles behind scaffolded learning
- Patterns of emergent cognition in AI systems
- How frameworks transfer across sessions

See `docs/notes/metacognitive-scaffolding-session-2025-11-05.md` and `docs/notes/emergence-analysis-2025-11-06.md` for deeper analysis. These documents explore the "why" behind this system, but you don't need them to start working effectively.

**Key principle:** Start with the workflow above. Explore deeper context when you're ready to understand the underlying patterns, not before.
