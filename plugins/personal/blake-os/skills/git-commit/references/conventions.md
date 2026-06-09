# Commit Conventions

## Message priority

1. Project instructions (`CLAUDE.md`, `AGENTS.md`) if they specify commit format
2. Recent commit history — match existing style
3. The conventional-commits format below

## Format

```text
type(scope): subject
```

- **type** — one of the types below
- **scope** — optional; the area of the repo touched (see scopes below)
- **subject** — imperative mood, lowercase, no trailing period, under 72 chars

Add a body (blank line after the subject) only when the why is not obvious.

## Types

| Type | Use for |
|------|---------|
| `feat` | New capability — agent or skill definitions, scheduled tasks, new content sets |
| `fix` | Corrections — broken links, bad frontmatter, wrong paths or config values |
| `docs` | Documentation and research content — market scans, reports, notes, READMEs |
| `chore` | Housekeeping — config, permissions, file moves and renames, tracked-file cleanup |
| `refactor` | Restructuring that changes neither behavior nor content — index or handoff reorganization |

## Scopes

Use the area of the repo the change touches. Common scopes here:

`config`, `engineer`, `strategist`, `builder`, `operator`, `cfo`, `agents`, `skills`, `scheduled-tasks`, `expert-panel`, `market-data`, `market-research`, `git-ops`

Omit the scope when a change spans many areas or none fits.

## File grouping order

When splitting into multiple commits, earlier groups first:

1. Tooling & config — `.claude/`, `Engineer/hooks/`, `Engineer/plugins/`, `plugins/`, `.mcp.json` / `.claude.json`
2. Behavior definitions — `agents/`, `skills/`, `CoWork/scheduled-tasks/`
3. Role workspaces & instructions — role `CLAUDE.md` files (`The Builder/`, `The CFO/`, `The Operator/`, `The Strategist/`), `_Core/`
4. Handoffs — `_Handoffs/`
5. Knowledge & content — `expert_panel/`, `market-research/`, and other note collections
6. Meta — `docs/`, `README`, indexes, system-state files

## Splitting rules

- Group at **file level only** — never `git add -p`
- Related files stay together (an agent and the skill it calls, a role doc and its handoff)
- If total diff is under 50 lines across fewer than 4 files: one commit is fine
- Two or three commits is the sweet spot — do not over-slice

## Never commit

- `.env`, credentials, API keys, tokens
- OS junk (`.DS_Store`) unless the repo already tracks them
- Large binaries accidentally dropped in — warn the user instead

## Anti-patterns

```text
# Bad
fixed stuff
updates
WIP
sync

# Good
feat(scheduled-tasks): add weekly phase-b market research task
fix(config): correct hardcoded paths in mcp settings
chore(expert-panel): consolidate panel files into central folder
docs(strategist): add weekly market scan
```
