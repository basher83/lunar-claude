# /improve Command

Analyzes recent Claude Code sessions to identify failures and generate improvement reports.

## Usage

```bash
# Search last 7 days (default)
/improve

# Search last 14 days
/improve 14
```

## What It Does

The command searches claude-mem for incidents where things went wrong, then
generates a dated report in `ai_docs/continuous-improvement/`.

**Search strategies:**

1. **User corrections** - Prompts containing "wrong", "stop", "why did you", "not what I asked", "no", "what are you"
2. **Problem-solution patterns** - Observations tagged with concept: "problem-solution"
3. **Bug fixes** - Observations of type: "bugfix"

**Output:** `ai_docs/continuous-improvement/lessons-learned-YYYY-MM-DD.md`

## Report Format

Each report includes:

- Search period and date range
- Total incidents found
- Detailed incident listings with:
  - Timestamp
  - Source (claude-mem URI)
  - User correction (exact quote if applicable)
  - Context (what happened, what went wrong)
- Results summary by search strategy

## Design Principles

**Simple primitive** - Slash command only. No agent composition yet.

**Manual control** - You decide when to run and what to do with results.

**No deduplication** - Shows all incidents in the time window. Manual reconciliation required.

**Evolvable** - Clear paths to sub-agents, skills, or hooks when needed.

## Evolution Path

### Stay at slash command level when

- You run it manually once a week or month
- Report generation takes under 2 minutes
- Results are manageable (fewer than 20 incidents per run)
- Manual reconciliation is acceptable

### Consider sub-agents when

- Search strategies become slow (over 2 minutes)
- You need parallel analysis of different time periods
- You want to process multiple projects simultaneously

### Consider creating a skill when

- You run `/improve` multiple times per week
- You need additional workflows: `/improve-analyze`, `/improve-update-rules`, `/improve-fix`
- You want automatic behavior (skill triggers on patterns)
- You're managing a broader continuous improvement domain

### Consider adding hooks when

- You want automatic report generation after every N sessions
- You need real-time incident capture (SessionEnd hook)
- You prefer deterministic automation over manual invocation

## Architecture

**Component:** Slash command (Stage 1: Prompt primitive)

**Data source:** claude-mem MCP server

**Dependencies:**

- `mcp__plugin_claude-mem_claude-mem-search__search_user_prompts`
- `mcp__plugin_claude-mem_claude-mem-search__find_by_concept`
- `mcp__plugin_claude-mem_claude-mem-search__find_by_type`

**Philosophy:** Master the primitive first. Scale when requirements demand it.

## Related

- Multi-Agent Composition skill - Decision framework for evolving to sub-agents or skills
- `ai_docs/continuous-improvement/` - Report storage location
- `ai_docs/continuous-improvement/rules.md` - Engineering rules derived from incidents
