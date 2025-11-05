# Composing Claude Code

**Comprehensive knowledge base** for building multi-component Claude Code systems.

## Quick Start

**New to this content?** Start with **[SKILL.md](SKILL.md)** - the main entry point.

SKILL.md provides:

- Quick reference (The Core 4, component overview, composition hierarchy)
- Navigation to all supporting documentation
- When to use this knowledge

## Structure

This knowledge base follows the **Claude Code skills pattern** with progressive disclosure:

```text
composing-claude-code/
├── SKILL.md (START HERE - main entry point)
│
├── reference/          (What components are)
│   ├── architecture.md
│   └── hooks-reference.md
│
├── patterns/           (How to use components)
│   ├── decision-framework.md
│   └── practical-guide.md
│
├── anti-patterns/      (What to avoid)
│   └── common-mistakes.md
│
├── examples/           (Real-world case studies)
│   └── work-tree-manager.md
│
├── workflows/          (Visual guides)
│   └── visual-decision-trees.md
│
└── research-questions.md (Future research)
```

## For Humans

**Learning Claude Code?**

1. Read [SKILL.md](SKILL.md) for overview
2. Study [reference/architecture.md](reference/architecture.md) for component details
3. Use [patterns/decision-framework.md](patterns/decision-framework.md) for architectural decisions
4. Check [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md) to avoid pitfalls

**Making a decision?**

- Go straight to [patterns/decision-framework.md](patterns/decision-framework.md)
- Follow the decision tree
- Review relevant examples

**Building something?**

- Check [examples/work-tree-manager.md](examples/work-tree-manager.md) for evolution path
- Review [patterns/practical-guide.md](patterns/practical-guide.md) for Q&A
- Study [reference/hooks-reference.md](reference/hooks-reference.md) for observability

## For AI Assistants

When helping with Claude Code:

**Architecture questions** → [reference/architecture.md](reference/architecture.md)
**"Which component should I use?"** → [patterns/decision-framework.md](patterns/decision-framework.md)
**Hooks/observability** → [reference/hooks-reference.md](reference/hooks-reference.md)
**Common mistakes** → [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md)
**Real examples** → [examples/](examples/)
**Visual aids** → [workflows/visual-decision-trees.md](workflows/visual-decision-trees.md)

## Key Principles

### The Core 4 Framework

Every agent is built on:

1. **Context** - What information?
2. **Model** - What capability?
3. **Prompt** - What instruction?
4. **Tools** - What actions?

### Golden Rules

1. **Always start with prompts** - Master the primitive first
2. **"Parallel" = Sub-Agents** - Nothing else supports parallel execution
3. **External = MCP, Internal = Skills** - Clear separation
4. **One-off = Slash Command** - Don't over-engineer
5. **Repeat + Management = Skill** - Only scale when needed
6. **Don't convert all slash commands to skills** - Huge mistake

### The Progression

```text
Level 1: Base agents       → Use out of the box
Level 2: Better agents     → Customize prompts
Level 3: More agents       → Run multiple agents
Level 4: Custom agents     → Build specialized solutions
Level 5: Orchestration     → Manage fleets of agents
```

## Source Attribution

This knowledge synthesizes:

- Video presentations by Claude Code engineering team
- Official Claude Code documentation (docs.claude.com)
- Hands-on experimentation and validation
- Multi-agent orchestration patterns from the field

## Contributing

This is a living knowledge base. Content to be added:

- patterns/hooks-observability.md (implementation patterns)
- patterns/orchestrator-pattern.md (multi-agent orchestration)
- patterns/context-window-protection.md (managing context at scale)
- examples/multi-agent-case-studies.md (scout-builder patterns)

See [research-questions.md](research-questions.md) for unanswered questions.

---

**Remember:** Context, Model, Prompt, Tools. Master these four, and you master Claude Code.

**Start here:** [SKILL.md](SKILL.md)
