# Git Workflow Plugin — Current State Inventory

Baseline inventory of the `plugins/devops/git-workflow/` plugin as it exists today,
ahead of the planned overhaul. Captures every component, its invocation surface,
delegation wiring, model assignment, and cross-references so nothing is lost when
redesigning. Pair with `research.md` for reference-implementation comparisons.

Validated against the full plugin tree (21 files) on 2026-06-08.

## Plugin Manifest

Declared at `.claude-plugin/plugin.json`.

- **Name**: `git-workflow`
- **Version**: `1.2.3`
- **Description**: Git workflow automation with fork-isolated skills for atomic
  commits, branch cleanup, conventional commit standards, and context-aware PR
  review
- **Keywords**: `git`, `commits`, `branches`, `workflow`, `automation`,
  `conventional-commits`, `review`, `pr-review`
- **Author**: `basher83` (`basher83@mail.spaceships.work`)
- **Repository**: `https://github.com/basher83/lunar-claude`
- **License**: MIT

### Marketplace Registration

Also declared in `.claude-plugin/marketplace.json` (category `devops`, version
`1.2.3`, author `name` only — no email). `./scripts/verify-structure.py` reports
an author-field conflict between marketplace and `plugin.json`.

## Complete File Surface

```text
plugins/devops/git-workflow/
├── .claude-plugin/plugin.json
├── README.md
├── agents/
│   ├── commit-craft.md
│   ├── code-reviewer.md
│   └── structural-reviewer.md
├── commands/
│   ├── codebase-health.md      # frontmatter name: sc-codebase-health
│   └── review-pr.md            # frontmatter name: sc-review-pr
├── docs/                       # 9 files — see Docs Directory
└── skills/
    ├── branch-cleanup/SKILL.md
    ├── generate-changelog/SKILL.md
    ├── git-commit/SKILL.md
    ├── git-status/SKILL.md
    └── git-workflow/SKILL.md
```

**Absent:** `hooks/`, `scripts/`, `references/`, `assets/` in any skill. Plugin
is entirely opt-in per invocation — no harness-level enforcement.

**Not present anywhere in this plugin:** `git-push`, `create-branch`, PR
creation, rebase, or conflict-resolution components. (Repo review docs elsewhere
reference a phantom `/git-workflow:create-branch` — that skill does not exist.)

## README (user-facing surface)

Primary entry point at `README.md`. Documents four fork skills + reference skill
+ `commit-craft`, dependencies, and headless invocation:

```bash
claude -p --agent git-workflow:commit-craft "make commits"
```

**Omissions:** README does not mention `review-pr`, `codebase-health`, or the
`code-reviewer` / `structural-reviewer` agents. Trigger phrases listed in README
differ from both `git-workflow` SKILL `when_to_use` and this inventory's earlier
wording.

## Structural Validation Failures

`./scripts/verify-structure.py` currently flags:

- **`agents/commit-craft.md`**: invalid YAML frontmatter — unquoted `context:
  fork` inside the `description` string breaks parsing
- **Author conflict**: marketplace entry vs `plugin.json` author shape mismatch

## Invocation Model

**Skills** (under `skills/`) are invoked via Skill tool auto-trigger
(`description` / `when_to_use`) or explicit skill load — **not** slash commands.
Only files under `commands/` become slash commands.

| Surface | How users/agents invoke it |
|---------|----------------------------|
| Workflow skills | Skill tool / auto-trigger → `context: fork` → agent |
| `commit-craft` | Fork from `git-commit`; or headless `--agent git-workflow:commit-craft` |
| Slash commands | `/git-workflow:sc-review-pr`, `/git-workflow:sc-codebase-health` (plugin-prefixed) |

## Component Matrix

| Component | Type | File | Model | Invocation | Delegates to |
|-----------|------|------|-------|------------|--------------|
| `git-workflow` | reference skill | `skills/git-workflow/SKILL.md` | none (inline) | Skill tool / auto-trigger | — |
| `git-commit` | skill (fork) | `skills/git-commit/SKILL.md` | via agent | Skill tool / auto-trigger | `git-workflow:commit-craft` |
| `git-status` | skill (fork) | `skills/git-status/SKILL.md` | `general-purpose` | Skill tool / auto-trigger | inline bash + agent summary |
| `branch-cleanup` | skill (fork) | `skills/branch-cleanup/SKILL.md` | `general-purpose` | Skill tool / auto-trigger | inline bash + agent workflow |
| `generate-changelog` | skill (fork) | `skills/generate-changelog/SKILL.md` | `general-purpose` | Skill tool / auto-trigger; `$ARGUMENTS` for action | git-cliff |
| `commit-craft` | agent | `agents/commit-craft.md` | `haiku` | fork from `git-commit`; headless `--agent` | loads `git-workflow` skill |
| `code-reviewer` | agent | `agents/code-reviewer.md` | inherited | `review-pr` Phase 3 only (not in README) | — |
| `structural-reviewer` | agent | `agents/structural-reviewer.md` | inherited | `review-pr` Phase 3 only (not in README) | — |
| `review-pr` | slash command | `commands/review-pr.md` | per-phase | `/git-workflow:sc-review-pr [PR#]` | 5-phase orchestration |
| `codebase-health` | slash command | `commands/codebase-health.md` | per-agent | `/git-workflow:sc-codebase-health [dir]` | 6× external `sc-refactor:*` agents |

## Skills

### `git-workflow` — reference knowledge

Central conventions document. Not fork-isolated; meant to be loaded into context
as reference.

**Triggers** (`description` + `when_to_use`): making commits, creating a branch,
organizing commits, generating a changelog, releasing/bumping a version; plus
phrases like "conventional commits", "commit format", "branch naming".

Covers:

- **Available Skills** index table (documents sibling fork skills)
- Conventional commit format (type, scope, subject, body, footer)
- **Eleven** commit types (`feat` through `chore`, plus `revert`)
- Subject/body/footer rules (subject: **lowercase** in canonical SKILL)
- Eight branch prefixes + kebab-case naming rules
- Atomic commit principles, what NOT to mix, pre-commit workflow
- Commit message heredoc template, quick reference (`git add -p`, etc.)
- **Pushing to Main** — solo work may commit/push directly to `main`; force-push
  to `main` acceptable with operator confirmation on solo repos
- Changelog generation pointer (`generate-changelog` actions)

Does **not** define a protected-branch enforcement list (that appears in
`branch-cleanup` delete-guardrails and `docs/branches.md` with conflicting policy).

Loaded as a dependency by `commit-craft` via `skills: ["git-workflow"]`
frontmatter key.

### `git-commit` — delegation shim

Thin skill that delegates to the `commit-craft` agent in a forked context.
Single body line: "Create clean, atomic commits for the current workspace
changes." All real logic lives in the agent.

`when_to_use` includes **one** `<example>` block (finished feature → commit-craft
invocation), plus prose triggers for explicit commit requests and post-refactor
work.

Frontmatter: `context: fork`, `agent: git-workflow:commit-craft`.

### `git-status` — lightweight summary

Fork-isolated skill with inline bash queries executed at skill-load time
(`!`...`` syntax). Inline queries gather: branch/sync (`git status -sb`), working
tree (`git status --short`), recent commits (last 5), stashes (`git stash list`).

Delegates summary generation to `general-purpose` with a **4-point output spec**:

1. Branch status (ahead/behind)
2. Working directory (staged/unstaged/untracked counts)
3. Recent activity
4. Action items (suggested next steps)

Stashes are queried inline but are **not** a required output dimension.

### `branch-cleanup` — multi-phase cleanup workflow

Fork-isolated skill that runs through five phases: analyze, confirm scope,
execute, optional remote cleanup, summary. Inline bash gathers branch state
before handoff.

Protected branch patterns (delete guardrails): `main`, `master`, `develop`,
`staging`, `production`, `release/*`, `renovate/*`, current branch, branches with
unpushed commits.

Four scope options: all safe, merged only, gone only, review each.

Records SHA before deletion (`git rev-parse <branch>`) and emits recovery
commands (`git checkout -b <branch> <sha>`) in the summary.

### `generate-changelog` — git-cliff wrapper

Fork-isolated skill. Action via `$ARGUMENTS`; if empty, prompts interactively.

- **preview**: shows `git-cliff --unreleased`, reports, stops
- **generate**: writes `CHANGELOG.md`, shows diff, commits as `docs: update
  changelog`
- **release**: analyzes commit types, runs `git-cliff --bump --bumped-version`
  for AI-recommended bump level, prompts user, generates with `--bump`, commits
  as `docs: update changelog for v<VERSION>`, tags as `v<VERSION>`

Pre-flight checks: warns on uncommitted changes (other than CHANGELOG.md),
stops if no conventional commits since last tag.

Summary section advises `git push` / `git push && git push --tags` — push is
**mentioned in prose**, not implemented as a workflow component.

## Agents

### `commit-craft` — atomic commit executor

Haiku-powered agent (green). Loads `git-workflow` skill for conventions.
Capabilities frontmatter lists four: pre-commit hook detection, workspace
analysis, atomic commit creation, conventional message drafting.

Tools: `TodoWrite`, `Read`, `Grep`, `Glob`, `Bash`.

**Analysis process (steps 0–8):**

0. Check CLAUDE.md for project-specific overrides
1. Detect `.pre-commit-config.yaml`, run `pre-commit run`, re-stage after
   formatter rewrites, stop on hard failures (no explicit retry cap on this
   pre-flight run)
2. Parallel workspace analysis: `git status`, `git diff --cached`, `git diff`,
   `git log --oneline -5`
3. Deep-dive per file if complex
4. Identify logical groupings (implementation + tests together, split infra vs
   app, isolate docs, keep lock files with manifests)
5. Build commit plan with TodoWrite, target <100 lines per commit
6. Draft conventional messages (72-char header line `type(scope): subject`,
   subject imperative, 72-char body wrap, `Fixes #N` footer,
   `BREAKING CHANGE:` footer where applicable)
7. Execute with heredoc; on hook re-modifications during commit, re-stage and
   **retry up to 2 times per commit group**
8. Verify with final `git status` + `git log --oneline -n`

Eleven documented edge cases: nothing to commit, sensitive files, lock files,
generated files, merge conflicts, detached HEAD, 100+ file changesets,
untracked-only, repeated hook failures, mixed staged/unstaged, blocked.

### `code-reviewer` — standards + bugs + security

Red. No model declared (inherits). Tools: `Bash`, `Read`, `Grep`, `Glob`,
`LS`, `TodoWrite`. Capabilities: `code-review`, `security-audit`,
`standards-compliance`.

**Agent definition scope:** by default reviews `git diff` unstaged changes.
Three core responsibilities: CLAUDE.md compliance, bug detection, code quality.
Confidence scoring 0–100, **only report ≥ 80**. Output grouped Critical vs
Important.

**In `review-pr` Phase 3:** spawned as `git-workflow:code-reviewer` (sonnet) with
a **narrowed prompt** — CLAUDE.md compliance only, quoting explicit rules. Bug
and security review in Phase 3 uses separate `general-purpose` opus agents, not
this agent's full definition.

### `structural-reviewer` — completeness and hygiene

Blue. No model declared. Tools: `Bash(rg:*)`, `Bash(fd:*)`, `Bash(git:*)`,
`Bash(gh pr view:*)`, `Bash(gh pr diff:*)`, `Bash(gh issue view:*)`, `Read`,
`Grep`, `Glob`, `LS`, `TodoWrite`. Capabilities: `structural-review`,
`dead-code-detection`, `change-completeness`.

Agent definition: structural integrity only — **no** functional correctness,
test quality, docs, or style. Five focus areas; five pass/fail rows plus
Critical Issues and Technical Debt lists.

**In `review-pr` Phase 3:** spawned prompt additionally asks for "Missing test
file additions/updates" — **broader than the agent's own scope statement**
(see Internal Contradictions).

## Commands

### `review-pr` (frontmatter name: `sc-review-pr`)

File: `commands/review-pr.md`. Invoked as `/git-workflow:sc-review-pr`.

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

### `codebase-health` (frontmatter name: `sc-codebase-health`)

File: `commands/codebase-health.md`. Invoked as `/git-workflow:sc-codebase-health`.

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

| File | Source content | Notes |
|------|---------------|-------|
| `components.md` | 6-line bullet list | Placeholder only |
| `branches.md` | Branch prefix + naming + protected-branch sections | Duplicates `git-workflow` SKILL; **conflicts** with SKILL "Pushing to Main" |
| `branch-cleanup.md` | Full body of `branch-cleanup` SKILL | Verbatim copy |
| `changelog.md` | Full body of `generate-changelog` SKILL | Verbatim copy |
| `git-status.md` | Full body of `git-status` SKILL | Verbatim copy |
| `git-commit.md` | Commit format + atomic principles + commit-craft body | Blend of SKILL and agent; **drift**: "Capitalize first letter" vs SKILL lowercase subject |
| `pre-commit.md` | Pre-commit workflow section | Duplicates `git-workflow` SKILL fragment |
| `research.md` | Overhaul analysis, inspiration sources, hook recommendations | **Design research** — not a verbatim excerpt |
| `inventory.md` | This file | Meta-inventory |

Seven of nine docs files are verbatim or near-verbatim copies of SKILL/agent
content. `research.md` and `inventory.md` are the exceptions. The overhaul
needs to decide whether `docs/` becomes design/architecture documentation or
user-facing deep dives that complement (not duplicate) the SKILL/agent surface.

## Internal Contradictions

Policy and scope conflicts across sources — agents may behave inconsistently
until unified:

| Topic | Source A | Source B |
|-------|----------|----------|
| Main-branch push policy | `git-workflow` SKILL "Pushing to Main": direct push OK for solo work | `docs/branches.md`: never force-push/commit to main; always use PRs |
| Subject line casing | `git-workflow` SKILL: lowercase subject | `docs/git-commit.md`: capitalize first letter |
| Structural review scope | `structural-reviewer` agent: no test quality review | `review-pr` Phase 3 prompt: check missing test file additions/updates |
| Protected branches | Documented in `branch-cleanup` + `docs/branches.md` only | No executor enforces; SKILL encourages direct-to-main for solo repos |

## Delegation Graph

```text
user input
  │
  ├── Skill: git-commit (auto / Skill tool) ──► commit-craft (haiku, fork)
  │                                              └─ loads skill: git-workflow
  │
  ├── Skill: git-status ──► general-purpose (fork, inline bash)
  │
  ├── Skill: branch-cleanup ──► general-purpose (fork, inline bash)
  │
  ├── Skill: generate-changelog [action] ──► general-purpose (fork, git-cliff)
  │
  ├── Skill: git-workflow ──► reference (inline, no fork)
  │
  ├── /git-workflow:sc-review-pr [PR] ──► 5-phase orchestration
  │                                        ├─ Phase 1: 3× general-purpose (haiku)
  │                                        ├─ Phase 2: general-purpose (sonnet)
  │                                        ├─ Phase 3: code-reviewer (sonnet)
  │                                        │          structural-reviewer (sonnet)
  │                                        │          2× general-purpose (opus)
  │                                        └─ Phase 4: N× general-purpose (opus)
  │
  └── /git-workflow:sc-codebase-health [dir] ──► 6× sc-refactor:* (BROKEN — see gaps)
```

Workflow skills do **not** hand off to each other (noted in `research.md`).
Lifecycle gap: commit → ??? → changelog; no composed push/PR path.

## Dependencies on External Tools

Declared in README:

- `git` (required)
- `pre-commit` (optional; consumed by `git-commit` / `commit-craft`)
- `git-cliff` (required for `generate-changelog`)
- `gh` (optional in README; required for `review-pr` and `structural-reviewer`)

Implicit additional deps used in practice:

- `fd` — used by `review-pr` Phase 1 and allowed for `structural-reviewer`
- `rg` — allowed for `structural-reviewer`

## Redundancies

1. **`docs/*.md` mirrors SKILL bodies.** Seven of nine docs files are verbatim
   or near-verbatim copies of the corresponding SKILL / agent content. Single
   source of truth is violated.
2. **Commit-format rules live in two places.** The `git-workflow` skill
   defines conventional commit format; `commit-craft` re-states it in prose
   while also declaring `skills: ["git-workflow"]`. The skill load should make
   the restatement unnecessary.
3. **Pre-commit handling lives in two places.** `commit-craft` has a
   detailed step for pre-commit; `git-workflow` skill has a briefer
   "Pre-Commit Workflow" section; `docs/pre-commit.md` copies the latter.
4. **Heredoc template appears three times.** In `git-workflow`, in
   `commit-craft`, and in `docs/git-commit.md`.
5. **`docs/git-commit.md` active drift.** Duplication plus contradictory
   subject-casing rule vs canonical SKILL.

## Gaps and Issues

1. **`codebase-health` references agents not in this plugin.** All six
   agents (`sc-refactor:sc-duplication-hunter`, `sc-abstraction-critic`,
   `sc-naming-auditor`, `sc-dead-code-detector`, `sc-test-organizer`, and
   `sc-refactor:sc-structural-reviewer`) live in a different namespace
   (`sc-refactor:`). This command will fail unless that plugin is also
   installed — and even then, the local `structural-reviewer` is not being
   used. Either wire to local agents or declare a hard dependency.
2. **Command naming carries `sc-` prefix hangover.** Both commands are named
   `sc-review-pr` and `sc-codebase-health` in frontmatter (filenames omit
   prefix), suggesting fork from a `sc-refactor` plugin. Inconsistent with
   plugin name `git-workflow`.
3. **No hook manager abstraction.** `commit-craft` assumes `pre-commit`
   (Python framework). Per repo-forge research, `hk` is the newer
   mise-integrated replacement. No support path for repos using `hk`,
   `husky`, `lefthook`, etc. No plugin `hooks/` directory at all.
4. **`code-reviewer` and `structural-reviewer` have no declared model.**
   They inherit from the caller. In `review-pr` Phase 3 they run on sonnet,
   but direct invocation would pick up whatever ambient model the user is on.
   Worth pinning explicitly.
5. **`git-status` and `branch-cleanup` could be slash commands, not
   skills.** They are pure bash inventory + user-prompt workflows; no
   "skill" heuristic is being applied. Distinction between skill (expertise)
   and command (procedure) is muddy here.
6. **No push/rebase/PR-creation executors.** No dedicated `git-push`,
   `rebase-interactive`, `pr-create`, `pr-update`, or conflict-resolution
   components. `generate-changelog` advises push in prose only. README
   describes "git workflow" broadly but executable scope stops at
   commit + changelog (+ PR review command).
7. **No protection against force-push or history-rewrite actions.** Delete
   guardrails exist in `branch-cleanup`; no executor refuses force-push.
   Policy sources **contradict** on whether direct-to-main is acceptable.
8. **`review-pr` hardcodes model names in inline prose.** Phase boundaries
   pin haiku/sonnet/opus literally. Model family names drift; a model map
   or single config point would age better.
9. **Missing lint/format/typecheck integration.** `commit-craft` only knows
   pre-commit; it does not invoke language-native tools directly
   (ruff/pyright/cargo fmt/cargo clippy/etc.) when hooks are absent.
10. **No full changelog preview before release commit/tag.** The release
    workflow computes bump version via `git-cliff --bump --bumped-version` but
    does not show the full proposed changelog body before commit/tag.
11. **`commit-craft` frontmatter fails structural validation.** Unquoted colon
    in description breaks YAML parse in `verify-structure.py`.
12. **Review surface orphaned from README and skill index.** Commands and
    review agents exist but are not documented in README; only reachable via
    slash command or manifest keywords.
13. **Skills do not reference each other.** No handoffs between commit,
    status, cleanup, and changelog (see `research.md`).
14. **Cross-plugin duplication at repo level.** `plugins/personal/blake-os/`
    implements a separate git skill stack; overhaul may need explicit
    boundary with that plugin.

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
  complement (not copy) the SKILL surface; resolve **internal contradictions**
  (main push policy, subject casing, structural vs test scope in PR flow).
- Fix `commit-craft` YAML frontmatter and marketplace author conflict so
  validation passes.
- Decide hook manager abstraction strategy (`pre-commit` vs `hk` vs others)
  and whether to add plugin `hooks/` for harness-level enforcement.
- Fix or rewire `codebase-health` — it references external agents.
- Rename `sc-*` command frontmatter names to plugin-consistent names; document
  in README alongside review agents.
- Pin models and scope tools on `code-reviewer` and `structural-reviewer`.
- Extend scope beyond commit+changelog into push/rebase/PR-creation **executors**
  if the plugin wants to own "git workflow" end-to-end; compose skill handoffs.
- Deduplicate conventional-commit rules so `git-workflow` skill is the sole
  source.
- Clarify boundary with `plugins/personal/blake-os/` git stack.
