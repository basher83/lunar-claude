# Progressive Disclosure in Claude Code

Progressive disclosure is a context management pattern where information is loaded selectively and incrementally rather than all at once.

## Core Principle

**Don't load everything upfront. Load what you need, when you need it.**

> "A focused agent is a performant agent."

## The Problem with Static Context

Traditional approaches load everything into the context window immediately:

- **Static `CLAUDE.md` files** - Always loaded, regardless of relevance
- **All MCP servers enabled** - Can consume 24k+ tokens unnecessarily
- **Non-selective memory** - No control over what context is active

### Impact of Static Loading

```text
Static CLAUDE.md (23k tokens) + All MCP servers (24k tokens) = 47k tokens wasted
Result: Only ~75% of context window available for actual work
```

## Progressive Disclosure Patterns

### 1. Context Priming

**Replace static `CLAUDE.md` with selective `/prime` commands**

**Before:**
```markdown
CLAUDE.md (23,000 tokens)
├── Global instructions
├── Project structure
├── Coding standards
├── API documentation
└── Deployment procedures
```
Always loaded, whether relevant or not.

**After:**
```markdown
CLAUDE.md (minimal - 43 lines)
└── Only universal essentials

/prime commands (load on demand):
├── /prime           → General codebase context
├── /prime-cc        → Claude Code-specific context
├── /prime-feature   → Feature development context
└── /prime-chore     → Maintenance/refactoring context
```

**Key Rule:** CLAUDE.md should only contain what you're **100% sure** you want loaded **100% of the time**.

### 2. Selective MCP Server Loading

**Load MCP servers explicitly when needed, not by default**

```bash
# ❌ Bad: Default mcp.json loads all servers
# Always consuming 24k+ tokens

# ✅ Good: Load specific servers on demand
claude-mcp-config /path/to/specialized-mcp-4k.json

# ✅ Good: Override defaults explicitly
claude-mcp-config --strict /path/to/firecrawl-only.json
```

### 3. Context Bundles for Agent Handoff

**When context window explodes, bundle and transfer selectively**

Context bundles capture 60-70% of an agent's work without full replay:

```markdown
context-bundle-2025-01-05-14-30-<session-id>.md
├── Initial /prime command
├── Read operations (deduplicated)
├── User prompts (summarized)
└── Key findings

Excluded (to prevent overflow):
├── Full write operations
├── Detailed read contents
└── Tool execution details
```

**Usage:**
```bash
# Agent 1: Context window explodes at 180k tokens
# Save bundle automatically

# Agent 2: Fresh start
/loadbundle /path/to/context-bundle-<timestamp>.md
# Now has 70% context from Agent 1 in ~15k tokens
```

### 4. Sub-Agent Context Isolation

**Delegate work to sub-agents to keep primary context clean**

```text
Primary Agent (9k tokens)
├── Spawns Sub-Agent 1 (3k tokens) → Web scraping
├── Spawns Sub-Agent 2 (3k tokens) → Documentation fetch
└── Spawns Sub-Agent 3 (3k tokens) → Analysis

Total work: 18k tokens
Primary agent context: Only 9k tokens (50% reduction)
```

Sub-agents use **system prompts** (not user prompts), keeping their context isolated from the primary agent.

## The R&D Framework

Progressive disclosure implements the **R&D Framework** for context management:

### R - Reduce
- Minimize MCP servers to essentials
- Shrink CLAUDE.md to universal core
- Use context bundles for selective history

### D - Delegate
- Sub-agents for parallel work
- Primary agent delegation for specialized tasks
- Context isolation through system prompts

## Skill Levels and Progressive Context

Progressive disclosure maps to skill progression:

| Level | Technique | Context Strategy |
|-------|-----------|------------------|
| **Beginner** | MCP management | Remove unused servers |
| **Intermediate** | Context priming | `/prime` over static files |
| **Advanced** | Context bundles | Agent handoff without overflow |
| **Agentic** | Primary delegation | Multi-agent systems with `/background` |

## Implementation Examples

### Example 1: Shrink CLAUDE.md

**Before (2,300 lines):**
```markdown
# Project instructions
...500 lines of API docs...
...300 lines of deployment...
...1,500 lines of coding standards...
```

**After (43 lines):**
```markdown
# Universal essentials only
- Fenced code blocks MUST have language
- Use rg instead of grep
- ALWAYS use set -euo pipefail
```

**Context priming commands:**
```markdown
# .claude/commands/prime.md
Read README.md, understand structure, report key findings

# .claude/commands/prime-api.md
Read API documentation, understand endpoints

# .claude/commands/prime-deploy.md
Read deployment procedures, understand workflow
```

### Example 2: Selective MCP Loading

**Before:**
```json
// mcp.json (always loaded)
{
  "mcpServers": {
    "firecrawl": {...},
    "github": {...},
    "postgres": {...},
    "redis": {...}
  }
}
```
24k tokens always loaded.

**After:**
```bash
# Only load what you need
claude-mcp-config specialized-configs/firecrawl-4k.json

# For this session, only firecrawl (4k tokens)
# 20k tokens saved
```

### Example 3: Background Agent Delegation

```bash
# In-loop agent (you're waiting)
/task "Create implementation plan for feature X"

# Out-of-loop agent (delegated, you continue working)
/background "Create implementation plan for feature X" \
  --model opus \
  --report-file agents/background/plan-$(date +%s).md

# Result: Primary agent freed up immediately
# Background agent writes to report file when done
```

## Key Principles

1. **Conditional Loading** - Only load context if it's relevant to the current task
2. **Incremental Information** - Load in stages as needed, not all at once
3. **Context Hygiene** - Regularly clean up and reset agent context
4. **Focused Agents** - One purpose, minimal context, maximum performance
5. **Strategic Delegation** - Use sub-agents and background agents to isolate context

## Anti-Patterns to Avoid

❌ **Large static CLAUDE.md files** - Performance degradation and token waste

❌ **Default MCP loading** - Loading all servers regardless of task

❌ **Context accumulation** - Never resetting agents, letting context grow unbounded

❌ **Premature optimization** - Adding context management before you need it

## When to Use Progressive Disclosure

✅ Working on large codebases with multiple domains

✅ Context window approaching limits (>150k tokens)

✅ Running multiple specialized tasks in sequence

✅ Building multi-agent orchestration systems

✅ Need to switch between different work contexts frequently

## Measuring Success

Monitor context window usage with `/context` command:

```text
✅ Good: 85-90% context window free after agent startup
⚠️  Warning: 70-80% free (review what's loaded)
❌ Bad: <70% free (implement progressive disclosure immediately)
```

## Source Attribution

**Primary source:** Elite Context Engineering transcript
**Supporting concepts:** Claude Code documentation, R&D framework

## Related Patterns

- [Context Window Protection](../patterns/context-window-protection.md) - Preventing context overflow
- [Hooks Reference](hooks-reference.md) - Monitoring context usage via hooks
- [Core 4 Framework](core-4-framework.md) - Context as one of the four pillars

---

**Remember:** It's not about saving tokens. It's about spending them properly.
