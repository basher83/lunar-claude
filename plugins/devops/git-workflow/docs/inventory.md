# Git Workflow Plugin — Current State Inventory

Baseline inventory of the `plugins/devops/git-workflow/` plugin as it exists today,
ahead of the planned overhaul. Captures every component, its invocation surface,
delegation wiring, model assignment, and cross-references so nothing is lost when
redesigning. Pair with `research.md` for reference-implementation comparisons.

## Plugin Manifest

Declared at `.claude-plugin/plugin.json`.

- **Name**: `git-workflow`
- **Version**: `1.2.3`
- **Description**: Git workflow automation with fork-isolated skills for atomic
  commits, branch cleanup, conventional commit standards, and context-aware PR
  review
- **Keywords**: `git`, `commits`, `branches`, `workflow`, `automation`,
  `conventional-commits`, `review`, `pr-review`

## Component Matrix

| Component | Type | File | Model | Invocation | Delegates to |
|-----------|------|------|-------|------------|--------------|
| `git-workflow` | reference skill | `skills/git-workflow/SKILL.md` | none (inline) | trigger phrases | — |
| `git-commit` | skill (fork) | `skills/git-commit/SKILL.md` | via agent | `/git-commit` or auto-trigger | `git-workflow:commit-craft` |
| `git-status` | skill (fork) | `skills/git-status/SKILL.md` | `general-purpose` | `/git-status` | bash queries |
| `branch-cleanup` | skill (fork) | `skills/branch-cleanup/SKILL.md` | `general-purpose` | `/branch-cleanup` | bash queries |
| `generate-changelog` | skill (fork) | `skills/generate-changelog/SKILL.md` | `general-purpose` | `/generate-changelog [preview\|generate\|release]` | git-cliff |
| `commit-craft` | agent | `agents/commit-craft.md` | `haiku` | fork-invoked from `git-commit` | loads `git-workflow` skill |
| `code-reviewer` | agent | `agents/code-reviewer.md` | inherited | spawned by `review-pr` Phase 3 | — |
| `structural-reviewer` | agent | `agents/structural-reviewer.md` | inherited | spawned by `review-pr` Phase 3 | — |
| `review-pr` | slash command | `commands/review-pr.md` | per-phase | `/sc-review-pr [PR#]` | spawns agents across 5 phases |
| `codebase-health` | slash command | `commands/codebase-health.md` | per-agent | `/sc-codebase-health [dir]` | spawns 6 parallel agents |

## Skills

### `git-workflow` — reference knowledge

Central conventions document. Not fork-isolated; meant to be loaded into context
as reference. Triggered by phrases like "conventional commits", "commit format",
"branch naming", "generating a changelog", "releasing a version", "bumping a
version".

Covers: conventional commit format (type, scope, subject, body, footer), ten
commit types with purposes, subject/body/footer rules, eight branch prefixes,
kebab-case naming rules, atomic commit principles, what NOT to mix, pre-commit
workflow, commit message heredoc template, protected branches, and a quick
reference section with staging and commit command snippets.

Loaded as a dependency by `commit-craft` via the `skills: ["git-workflow"]`
frontmatter key.

### `git-commit` — delegation shim

Thin skill that delegates to the `commit-craft` agent in a forked context.
Single body line: "Create clean, atomic commits for the current workspace
changes." All real logic lives in the agent. Four `when_to_use` examples cover:
finished feature, explicit "create commits" request, "let's commit all this",
large refactor.

Frontmatter: `context: fork`, `agent: git-workflow:commit-craft`.

### `git-status` — lightweight summary

Fork-isolated skill with inline bash queries executed at skill-load time
(`!`...`` syntax). Reports branch sync, working directory changes, recent
commits (last 5), and stashes. Delegates the summary generation to
`general-purpose` with a 4-point output spec.

### `branch-cleanup` — multi-phase cleanup workflow

Fork-isolated skill that runs through five phases: analyze, confirm scope,
execute, optional remote cleanup, summary. Inline bash gathers branch state
before handoff.

Protected branch patterns: `main`, `master`, `develop`, `staging`,
`production`, `release/*`, `renovate/*`, current branch, branches with
unpushed commits.

Four scope options: all safe, merged only, gone only, review each.

Records SHA before deletion (`git rev-parse <branch>`) and emits recovery
commands (`git checkout -b <branch> <sha>`) in the summary.

### `generate-changelog` — git-cliff wrapper

Fork-isolated skill with three actions passed via `$ARGUMENTS`:

- **preview**: shows `git-cliff --unreleased`, reports, stops
- **generate**: writes `CHANGELOG.md`, shows diff, commits as `docs: update
  changelog`
- **release**: analyzes commit types, runs `git-cliff --bump --bumped-version`
  for AI-recommended bump level, prompts user, generates with `--bump`, commits
  as `docs: update changelog for v<VERSION>`, tags as `v<VERSION>`

Pre-flight checks: warns on uncommitted changes (other than CHANGELOG.md),
stops if no conventional commits since last tag.

## Agents

### `commit-craft` — atomic commit executor

Haiku-powered agent (green). Loads `git-workflow` skill for conventions.
Capabilities frontmatter lists four: pre-commit hook detection, workspace
analysis, atomic commit creation, conventional message drafting.

Tools: `TodoWrite`, `Read`, `Grep`, `Glob`, `Bash`.

Eight-step process:

1. Check CLAUDE.md for project-specific overrides
2. Detect `.pre-commit-config.yaml`, run `pre-commit run`, re-stage after
   formatter rewrites, retry up to 2 times, stop on hard failures
3. Parallel workspace analysis: `git status`, `git diff --cached`, `git diff`,
   `git log --oneline -5`
4. Deep-dive per file if complex
5. Identify logical groupings (implementation + tests together, split infra vs
   app, isolate docs, keep lock files with manifests)
6. Build commit plan with TodoWrite, target <100 lines per commit
7. Draft conventional messages (72-char header line `type(scope): subject`,
   subject imperative, 72-char body wrap, `Fixes #N` footer,
   `BREAKING CHANGE:` footer where applicable)
8. Execute with heredoc, handle hook re-modifications, verify with final
   `git status` + `git log --oneline -n`

Eleven documented edge cases: nothing to commit, sensitive files, lock files,
generated files, merge conflicts, detached HEAD, 100+ file changesets,
untracked-only, repeated hook failures, mixed staged/unstaged, blocked.

### `code-reviewer` — standards + bugs + security

Red. No model declared (inherits). Tools: `Bash`, `Read`, `Grep`, `Glob`,
`LS`, `TodoWrite`. Capabilities: `code-review`, `security-audit`,
`standards-compliance`.

Scope: by default reviews `git diff` unstaged changes. Three core
responsibilities: CLAUDE.md compliance (explicit quoted rules only), bug
detection (logic errors, null handling, races, leaks, vulns, perf), code
quality (duplication, missing error handling, a11y, coverage).

Confidence scoring 0–100, with **only report ≥ 80** gate. Output grouped
Critical vs Important.

### `structural-reviewer` — completeness and hygiene

Blue. No model declared. Tools: `Bash(rg:*)`, `Bash(fd:*)`, `Bash(git:*)`,
`Bash(gh pr view:*)`, `Bash(gh pr diff:*)`, `Bash(gh issue view:*)`, `Read`,
`Grep`, `Glob`, `LS`, `TodoWrite`. Capabilities: `structural-review`,
`dead-code-detection`, `change-completeness`.

Explicitly scoped to structural integrity only — no functional correctness,
test quality, docs, or style. Five focus areas: dead code, change
completeness, development artifacts, dependency hygiene, configuration
consistency.

Output: five pass/fail rows plus Critical Issues (blocking builds/deploys) and
Technical Debt (future maintenance pain) lists.

## Commands

### `review-pr` (named `sc-review-pr`)

Argument: PR number, full URL, or empty (infer from current branch). Five
phases:

1. **Context Gathering** (haiku, parallel) — three agents: PR metadata via
   `gh pr view --json`, CLAUDE.md finder (uses `fd` to locate all CLAUDE.md in
   repo at any depth), ticket extractor (JIRA / GitHub issues / Linear
   patterns, fetches issue bodies via `gh issue view`)
2. **Intent Summary** (sonnet) — synthesizes metadata + CLAUDE.md + tickets
   into author intent, change summary, risk areas, review focus
3. **Parallel Review** (sonnet + opus) — four agents: CLAUDE.md compliance
   (→ `git-workflow:code-reviewer` sonnet), structural completeness (→
   `git-workflow:structural-reviewer` sonnet), bug detection (opus), security
   scanner (opus)
4. **Validation** (opus, parallel per finding) — for each finding with
   confidence ≥ 80, spawn a validator that reads the file, checks novelty
   against base branch via `git show origin/$BASE_BRANCH:$FILE`, and returns
   VALID/INVALID
5. **Report** — markdown report with PR context, validated findings by
   severity (Critical / Important / Structural), reviewed-against list

Hard constraints: no `run_in_background: true`, high-signal only, context-first
(intent before review), require TodoWrite checklist, explicit anti-patterns
list (pre-existing issues, style, theoretical risks, lint-catchable issues,
subjective, best-practice suggestions).

Edge cases handled: no tickets, no CLAUDE.md (skip Phase 3 Agent 1), empty PR
body, no issues found.

### `codebase-health` (named `sc-codebase-health`)

Argument: target directory (defaults to cwd). Four phases:

1. **Check Context** — looks for `context-packet-*.md` in `.agent-history/`,
   otherwise asks for focus areas
2. **Launch Analysis Agents** — six parallel agents, all
   `run_in_background: true`:
   - `sc-refactor:sc-structural-reviewer`
   - `sc-refactor:sc-duplication-hunter`
   - `sc-refactor:sc-abstraction-critic`
   - `sc-refactor:sc-naming-auditor`
   - `sc-refactor:sc-dead-code-detector`
   - `sc-refactor:sc-test-organizer`
3. **Collect and Synthesize** — report with Executive Summary, Quick Wins
   (< 30 min), Recommended Refactors, Tech Debt Backlog, Skip These
4. **User Choice** — AskUserQuestion with three options: generate fix plan,
   auto-fix quick wins (max 10 iterations, TodoWrite-driven), report-only

## Docs Directory (as currently written)

`docs/` presently contains literal excerpts copy-pasted from the SKILL.md and
agent files, not proper writeups. This is the content that needs replacing.

| File | Source content | Notes |
|------|---------------|-------|
| `components.md` | 6-line bullet list | Placeholder only |
| `branches.md` | Branch prefix + naming + protected-branch sections | Duplicates `git-workflow` SKILL |
| `branch-cleanup.md` | Full body of `branch-cleanup` SKILL | Verbatim copy |
| `changelog.md` | Full body of `generate-changelog` SKILL | Verbatim copy |
| `git-status.md` | Full body of `git-status` SKILL | Verbatim copy |
| `git-commit.md` | Commit format + atomic principles + commit-craft body | Blend of SKILL and agent content |
| `pre-commit.md` | Pre-commit workflow section | Duplicates `git-workflow` SKILL fragment |

Net: the docs folder does not add new information. The overhaul needs to
decide whether `docs/` becomes design/architecture documentation or user-facing
deep dives that complement (not duplicate) the SKILL/agent surface.

## Delegation Graph

```text
user input
  │
  ├── /git-commit  ──►  commit-craft (haiku, fork)
  │                       └─ loads skill: git-workflow
  │
  ├── /git-status  ──►  general-purpose (fork, inline bash)
  │
  ├── /branch-cleanup  ──►  general-purpose (fork, inline bash)
  │
  ├── /generate-changelog [action]  ──►  general-purpose (fork, git-cliff)
  │
  ├── /sc-review-pr [PR]  ──►  5-phase orchestration
  │                             ├─ Phase 1: 3× general-purpose (haiku)
  │                             ├─ Phase 2: general-purpose (sonnet)
  │                             ├─ Phase 3: code-reviewer (sonnet)
  │                             │          structural-reviewer (sonnet)
  │                             │          2× general-purpose (opus)
  │                             └─ Phase 4: N× general-purpose (opus)
  │
  └── /sc-codebase-health [dir]  ──►  6× sc-refactor:* (BROKEN — see gaps)

auto-triggered (by "trigger phrases" in SKILL frontmatter):
  git-workflow skill loads as reference knowledge
```

## Dependencies on External Tools

Declared in README:

- `git` (required)
- `pre-commit` (optional; consumed by `git-commit` / `commit-craft`)
- `git-cliff` (required for `generate-changelog`)
- `gh` (optional; required for `review-pr` and `structural-reviewer`)

Implicit additional deps used in practice:

- `fd` — used by `review-pr` Phase 1 and allowed for `structural-reviewer`
- `rg` — allowed for `structural-reviewer`

## Redundancies

1. **`docs/*.md` mirrors SKILL bodies.** Six of seven docs files are verbatim
   or near-verbatim copies of the corresponding SKILL / agent content. Single
   source of truth is violated.
2. **Commit-format rules live in two places.** The `git-workflow` skill
   defines conventional commit format; `commit-craft` re-states it in prose
   while also declaring `skills: ["git-workflow"]`. The skill load should make
   the restatement unnecessary.
3. **Pre-commit handling lives in two places.** `commit-craft` has a
   detailed step 1 for pre-commit; `git-workflow` skill has a briefer
   "Pre-Commit Workflow" section; `docs/pre-commit.md` copies the latter.
4. **Heredoc template appears three times.** In `git-workflow`, in
   `commit-craft`, and in `docs/git-commit.md`.

## Gaps and Issues

1. **`codebase-health` references agents not in this plugin.** All six
   agents (`sc-refactor:sc-duplication-hunter`, `sc-abstraction-critic`,
   `sc-naming-auditor`, `sc-dead-code-detector`, `sc-test-organizer`, and
   `sc-refactor:sc-structural-reviewer`) live in a different namespace
   (`sc-refactor:`). This command will fail unless that plugin is also
   installed — and even then, the local `structural-reviewer` is not being
   used. Either wire to local agents or declare a hard dependency.
2. **Command naming carries `sc-` prefix hangover.** Both commands are named
   `sc-review-pr` and `sc-codebase-health`, suggesting they were forked from
   a `sc-refactor` plugin. Inconsistent with plugin name `git-workflow`.
3. **No hook manager abstraction.** `commit-craft` assumes `pre-commit`
   (Python framework). Per repo-forge research, `hk` is the newer
   mise-integrated replacement. No support path for repos using `hk`,
   `husky`, `lefthook`, etc. This is the clearest candidate for an overhaul
   driver.
4. **`code-reviewer` and `structural-reviewer` have no declared model.**
   They inherit from the caller. In `review-pr` Phase 3 they run on sonnet,
   but direct invocation would pick up whatever ambient model the user is on.
   Worth pinning explicitly.
5. **`git-status` and `branch-cleanup` could be slash commands, not
   skills.** They are pure bash inventory + user-prompt workflows; no
   "skill" heuristic is being applied. Distinction between skill (expertise)
   and command (procedure) is muddy here.
6. **No push, fetch, rebase, or PR-creation surface.** The plugin's
   "git-workflow" scope stops at commit and changelog; there is no
   `git-push`, `rebase-interactive`, `pr-create`, `pr-update`, or conflict
   resolution path. README describes the plugin as covering "git workflow"
   but the workflow is truncated.
7. **No protection against force-push or history-rewrite actions.** Protected
   branches appear as documentation only; no executor refuses to act on them.
8. **`review-pr` hardcodes model names in inline prose.** Phase boundaries
   pin haiku/sonnet/opus literally. Model family names drift; a model map
   or single config point would age better.
9. **Missing lint/format/typecheck integration.** `commit-craft` only knows
   pre-commit; it does not invoke language-native tools directly
   (ruff/pyright/cargo fmt/cargo clippy/etc.) when hooks are absent.
10. **No integration with `git-cliff --bump --unreleased` preview in
    `generate-changelog release` path.** The release workflow computes the
    version but does not show the user the full proposed changelog body before
    the commit/tag step.

## Model and Color Allocation

| Component | Model | Color | Notes |
|-----------|-------|-------|-------|
| `commit-craft` | haiku | green | Explicit; appropriate for mechanical work |
| `code-reviewer` | inherited | red | Should be pinned |
| `structural-reviewer` | inherited | blue | Should be pinned |
| `review-pr` Phase 1 | haiku | — | Context-gathering |
| `review-pr` Phase 2 | sonnet | — | Synthesis |
| `review-pr` Phase 3 | sonnet (compliance, structural), opus (bugs, security) | — | Review |
| `review-pr` Phase 4 | opus | — | Validation |

## Tool Scope per Component

| Component | Tools |
|-----------|-------|
| `commit-craft` | TodoWrite, Read, Grep, Glob, Bash |
| `code-reviewer` | Bash, Read, Grep, Glob, LS, TodoWrite |
| `structural-reviewer` | Bash(rg:*), Bash(fd:*), Bash(git:*), Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh issue view:*), Read, Grep, Glob, LS, TodoWrite |
| `review-pr` | Task, Read, Bash, Grep, Glob, TodoWrite, AskUserQuestion, WebFetch |
| `codebase-health` | Task, Read, Bash, Grep, Glob, TodoWrite, AskUserQuestion, WebFetch |

`structural-reviewer` is the only component using allow-list bash scoping; the
rest allow general `Bash`. This is a hardening gap.

## Summary for the Overhaul

Biggest levers:

- Replace `docs/` fragments with real architecture/design writeups that
  complement (not copy) the SKILL surface.
- Decide hook manager abstraction strategy (`pre-commit` vs `hk` vs others)
  since `repo-forge` is standardizing on `hk`.
- Fix or rewire `codebase-health` — it references external agents.
- Rename `sc-*` commands to plugin-consistent names.
- Pin models and scope tools on `code-reviewer` and `structural-reviewer`.
- Extend scope beyond commit+changelog into push/rebase/PR-creation if the
  plugin wants to own "git workflow" end-to-end.
- Deduplicate conventional-commit rules so `git-workflow` skill is the sole
  source.
