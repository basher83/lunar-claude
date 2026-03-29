---
date: 2026-02-17
status: draft
tags:
  - design
  - mise
  - claude-code
  - operations
---

# Design: Mise Task Runner for Claude Code Operations

## Summary

A layered mise configuration that provides a unified operations layer for Claude Code workflows. Global tasks handle cross-cutting orchestration (session bootstrapping, cross-repo operations, git workflows). Per-project tasks handle repo-specific concerns. Tasks complement existing slash commands and wrap them for larger workflows, with mise owning the shell side and Claude Code owning the conversation side.

## Requirements

- Layered config: global `~/.mise.toml` for cross-cutting tasks, per-project `mise.toml` for local tasks
- Platform-quality conventions so adding new tasks is trivial (fill in a template, not design from scratch)
- Mise complements slash commands (no duplication) and wraps them via `claude --print` for larger workflows
- Covers four concerns: session bootstrapping, cross-repo orchestration, pre/post automation, discoverability
- `mise tasks` serves as a self-documenting operations menu

## Approach

### Namespace Taxonomy

Tasks use `namespace:verb` naming. Namespaces map to operational domains, verbs describe the action. This keeps `mise tasks` output grouped naturally since mise sorts alphabetically.

```yaml
cc:prime       # domain:action  (correct)
prime:cc       # action:domain  (wrong — scatters related tasks)
```

### Layer Strategy

Global tasks never assume a specific repo structure. They use environment variables or auto-detection. Per-project tasks reference local paths freely.

Global namespaces:

- `cc:` — Claude Code session operations
- `repo:` — Repository orchestration
- `git:` — Git workflow shortcuts

Per-project namespaces use the project's domain noun:

- `vault:` in TheMothership
- `cluster:` in omni-scale

### Relationship to Slash Commands

Mise and slash commands occupy different layers. Slash commands run inside a Claude Code session and operate on conversation context. Mise tasks run in the shell and orchestrate around sessions. When a mise task needs Claude, it invokes the CLI (`claude --print /some-command`). There is no overlap — mise never reimplements what a slash command already does.

## Conventions

### Naming

Every task follows `namespace:verb`. The namespace is a domain noun, the verb is an action. One task, one purpose.

### Descriptions

Every task includes a `description` field — one line answering "what does this do and when would I use it?" This is the discoverability layer.

### Environment

Shared environment variables centralize path knowledge in the global config:

```toml
[env]
MOTHERSHIP_ROOT = "~/dev/Vault/TheMothership"
OMNI_SCALE_ROOT = "~/dev/personal/lunar-claude/plugins/homelab/omni-scale"
LUNAR_CLAUDE_ROOT = "~/dev/personal/lunar-claude"
MANAGED_REPOS = "{{env.MOTHERSHIP_ROOT}}:{{env.OMNI_SCALE_ROOT}}:{{env.LUNAR_CLAUDE_ROOT}}"
```

Adding a new repo to the ecosystem means updating one variable.

### Output

Tasks producing status output use a consistent format: short summary line, then details. Tasks invoking Claude Code pass through Claude's output unmodified.

### Dependencies

Tasks declare `depends` for sequencing. Mise handles execution order. Example: `git:commit` depends on `repo:check`.

## Task Catalog

### Global: `cc:` — Claude Code Operations

#### `cc:prime`

Detect the current repo and run its appropriate prime command. TheMothership runs `claude --print /vault-prime`. Omni-scale runs `claude --print /omni-prime`. Falls back to a generic context dump if no prime command exists.

#### `cc:ask`

One-shot question to Claude without entering interactive mode. Wraps `claude --print` with preferred model flags.

Usage: `mise run cc:ask "what changed in the last 3 commits?"`

#### `cc:review`

Code review pass on staged changes. Wraps `claude --print` with a review prompt and pipes in `git diff --staged`.

### Global: `repo:` — Repository Orchestration

#### `repo:status`

Iterate over `$MANAGED_REPOS` and show git branch, dirty state, and ahead/behind for each. One-line-per-repo summary.

#### `repo:each`

Run an arbitrary command in every managed repo.

Usage: `mise run repo:each "git pull --rebase"`

#### `repo:sync`

Pull with rebase across all managed repos. Wraps `repo:each` with error handling and a summary.

### Global: `git:` — Git Workflow

#### `git:commit`

Full commit workflow via Claude. Two modes:

1. **Full** (default): invokes `/git-commit` slash command,
   which orchestrates the complete chain: pre-flight checks
   (merge/rebase detection, sensitive file scan),
   `pre-commit run -a`, re-stage modified files,
   then delegate to commit-craft agent via Task tool
2. **Quick** (`--quick`): invokes commit-craft agent directly,
   skipping the orchestration layer. Git's own pre-commit
   hooks still fire during `git commit` execution,
   but no sensitive file scan or merge detection occurs

Both modes are autonomous.
Depends on `repo:check` to verify repo state before starting.

Implementation is stubbed;
exact `claude` CLI invocations to be finalized after setup.

#### `git:clean`

Prune local branches merged or deleted on remote. Shows what it will delete, asks for confirmation.

### Per-Project Example: `vault:` (TheMothership)

#### `vault:triage`

Invoke Claude with the inbox-process command. Wraps `claude --print /inbox-process`.

#### `vault:scan`

Quick inbox scan without processing. Wraps `claude --print /inbox-scan`.

## File Structure

```text
~/.mise.toml                          # Global tasks (cc:, repo:, git:)
~/dev/Vault/TheMothership/mise.toml   # vault: namespace tasks
~/dev/personal/lunar-claude/plugins/homelab/omni-scale/mise.toml  # cluster: namespace (future)
```

## Implementation Notes: git-workflow Integration

The git-workflow plugin
(`lunar-claude/plugins/devops/git-workflow/`)
has specific ordering and tool constraints
that mise tasks must respect.

### Invocation Chain for Mode 1 (Full)

The `/git-commit` slash command executes this sequence:

1. Dynamic state collection at command load
   (`git status`, staged files, merge detection)
2. Pre-flight checks — halt on merge/rebase in progress,
   prompt on sensitive files (`.env`, secrets, tokens)
3. `pre-commit run -a` — runs all configured hooks
   against all files (not just staged)
4. Re-stage modified files — if pre-commit reformatted
   anything, runs `git add -u` before proceeding.
   This step is critical; without it commit-craft
   sees mismatched staging state
5. Delegate to commit-craft agent via `Task` tool
6. commit-craft analyzes, plans (via TodoWrite),
   groups, and executes atomic commits
7. Verification pass (`git status` + `git log`)

### Tool Permission Boundaries

The `/git-commit` command restricts itself to
`Bash(git:*)`, `Bash(pre-commit:*)`, `Bash(test:*)`,
`Task`, and `AskUserQuestion`.
It cannot run arbitrary shell commands.

The commit-craft agent has unrestricted `Bash`, `Read`,
`Grep`, `Glob`, and `TodoWrite`. It runs on `haiku` model.

### Silent Failure Risks

When wrapping these in mise tasks, watch for:

- `pre-commit run -a` modifies files outside staging.
  The re-stage step must happen before commit-craft starts.
  The `/git-commit` command handles this;
  a mise task that runs pre-commit separately must also
  handle it.
- commit-craft retries failed `git commit` twice
  (pre-commit hooks fire again at git level),
  then asks the user. In `--print` mode this interaction
  breaks — use interactive `claude` for commit workflows,
  not `claude --print`.
- `entire` session hooks fire on `Task` invocations.
  Non-blocking if `entire` isn't installed,
  but log noise is possible.

### Recommendation

Both modes can use `claude --print` if the slash command
and commit-craft agent are updated to handle edge cases
autonomously (auto-abort on merge state,
auto-unstage sensitive files, deterministic retry logic).
The current `AskUserQuestion` prompts are
a prompt engineering concern, not an architectural blocker.
Updating those commands to run headless
is a prerequisite for mise integration, not a limitation of it.

## Open Questions

- Should `cc:prime` auto-detect the repo via git remote, or use a lookup table mapping directory paths to prime commands?
- What flags should `cc:ask` set by default? Model selection, output format?
- Should `repo:each` support a `--filter` flag to run against a subset of managed repos?
- Should `git:commit --quick` default to interactive or
  `--print`? Interactive is safer but slower for
  simple changesets.
