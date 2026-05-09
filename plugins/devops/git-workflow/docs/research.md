Here's what the corpus turned up, framed against what's incoherent in your current plugin.

## Diagnosis of your current plugin

Reading `lunar-claude/plugins/devops/git-workflow`, the pieces don't compose into a lifecycle:

- **Four skills that don't reference each other.** `git-status`, `git-commit`, `branch-cleanup`, `generate-changelog` each stand alone. No skill hands off to another.
- **Reference doc vs. executable skill collision.** `skills/git-workflow/SKILL.md` is a reference document (conventional commit cheatsheet), but it lives in the same shape as the executable skills. The loadout tax is the same for both, so conventions get reloaded every session.
- **Commands sit orphaned from skills.** `review-pr.md` and `codebase-health.md` are commands, but the review agents they dispatch (`code-reviewer`, `structural-reviewer`) aren't referenced from any skill or plugin docs.
- **No PR-creation path.** Commit → ??? → changelog. There's a gap where `commit-push-pr` should live.
- **Prose state machines in commit-craft.** Steps 1-8 narrate the workflow, which the corpus warns against specifically for git (below).
- **Zero hooks.** The plugin is entirely opt-in per invocation.

## Top inspiration sources (file paths for you to read directly)

### compound-engineering-plugin — the strongest cohesion model in the corpus

- `compound-engineering-plugin/plugins/compound-engineering/skills/git-commit/SKILL.md`
- `compound-engineering-plugin/plugins/compound-engineering/skills/git-commit-push-pr/SKILL.md`
- `compound-engineering-plugin/plugins/compound-engineering/skills/ce-pr-description/SKILL.md`
- `compound-engineering-plugin/plugins/compound-engineering/docs/solutions/skill-design/git-workflow-skills-need-explicit-state-machines-2026-03-27.md` ← **read this one first**

Key patterns worth stealing:

1. **Explicit state machines, not prose.** That `docs/solutions/` file above is a post-mortem documenting why prose-based git workflows regress. Use `git status` as source of truth (covers staged+modified+untracked), re-read branch state after every mutation, split "upstream exists" from "unpushed commits" as distinct checks, gate detached-HEAD before any push path.

2. **Decoupled generation from application.** `ce-pr-description` returns `{title, body}` — does NOT call `gh pr create` or `gh pr edit`. The caller composes. This lets the same skill be reused by `git-commit-push-pr`, by `ce-pr-stack`, and by the user directly.

3. **Namespace-prefixed commands create plugin identity.** `/ce:brainstorm`, `/ce:plan`, `/ce:work`, `/ce:review`, `/ce:compound` — the prefix makes them read as a coordinated loop, not disparate tools. You could use `/gw:` or `/git:`.

4. **Lazy-loaded `references/` for schemas and templates.** Each skill has a `references/` subdirectory with `schema.yaml` and template docs. Subagents read these on demand via backtick paths, so they don't inflate skill loadout tokens.

### SimpleClaude sc-review-pr — your review-pr.md is already a port of this

- `SimpleClaude/plugins/sc-refactor/commands/sc-review-pr.md`

You've already adopted this command (per your memory: confirmed as preferred PR review tool). The 5-phase pipeline is good — context gathering → intent synthesis → parallel reviewers → per-finding validation → report. The **validation phase** (re-check each ≥80 confidence finding against the base branch to eliminate pre-existing noise) is the secret weapon and worth preserving.

### everything-claude-code — hook-level enforcement

- `everything-claude-code/scripts/hooks/block-no-verify.js` — blocks `--no-verify` flags on commit/push/merge/rebase. This is the hook your plugin is missing.
- `everything-claude-code/scripts/hooks/pre-bash-commit-quality.js` — runs staged-file linting, secret detection, commit message format validation BEFORE `git commit` executes. Hook-level, not skill-level.
- `everything-claude-code/scripts/hooks/post-bash-pr-created.js` — detects PR creation from `gh pr create` output, logs the URL and review command.

These are PreToolUse/PostToolUse Bash hooks — they fire regardless of whether the user invoked your skill. This is the "automation without opt-in" you don't currently have.

### claude-plugins-official/commit-commands — minimal reference

- `claude-code/plugins/commit-commands/commands/commit.md`
- `claude-code/plugins/commit-commands/commands/commit-push-pr.md`
- `claude-code/plugins/commit-commands/commands/clean_gone.md` — exactly your `branch-cleanup` but also removes associated worktrees before deleting branches. You're missing the worktree consideration.

### claude-skills/engineering/changelog-generator — stronger than your generate-changelog

- `claude-skills/engineering/changelog-generator/SKILL.md`

Ships with a `commit_linter.py` that validates conventional commit format. Blocks merge on invalid commits. JSON output for CI. Monorepo scope filtering. Your `generate-changelog` skill wraps `git-cliff` but doesn't lint inputs — garbage in, garbage out.

## Concrete recommendations for restructuring

Pick from these — they compound but each stands alone:

1. **Define the loop.** Name it explicitly in the README: `status → commit → push+pr → review → changelog → cleanup`. Today your skills read as a menu. Make them read as a pipeline.

2. **Add `git-commit-push-pr` skill.** The missing middle. Composes `git-commit` + branch-safety check + `gh pr create` + a new `pr-description` skill. Model on compound-engineering's version.

3. **Split `pr-description` out of the commit agent.** New skill that returns structured `{title, body}`. Callable standalone OR by `git-commit-push-pr`. This is the cohesion multiplier.

4. **Convert `commit-craft` agent prose steps into a state machine.** Read that `git-workflow-skills-need-explicit-state-machines` post-mortem and rewrite Analysis Process steps 1-8 as explicit state → transition → check, not narrative. The edge cases you already list (detached HEAD, merge conflicts, etc.) are the states — make them first-class.

5. **Move `skills/git-workflow/SKILL.md` content into `references/conventions.md`** and have the executable skills reference it lazily. Stop paying loadout cost for a cheatsheet.

6. **Add a `hooks/` directory.** Port `block-no-verify.js` as table stakes. Add commit-message-format validation as PreToolUse. That moves enforcement from "hope the user invoked the skill" to "the harness enforces it."

7. **Namespace the commands.** `/gw:review-pr`, `/gw:codebase-health`, `/gw:commit`, `/gw:push-pr`. Signals plugin membership at the command surface.

8. **Surface `code-reviewer` and `structural-reviewer` agents in README.** They exist, they're good, they're invisible today because only `review-pr.md` mentions them.

Want me to go deeper on any of these — sketch the state machine for commit-craft, draft a `git-commit-push-pr` SKILL.md against your existing conventions, or evaluate compound-engineering's review persona design against your `review-pr` command?

---

The gstack deep dive hit paydirt. Here's what's genuinely new beyond the first round.

## gstack — the transferable DNA

Don't port gstack's git commands — port its **infrastructure for skill cohesion**. Six patterns that would transform your plugin from a menu into a system:

### 1. Preamble tiers (the single biggest architectural win)

`gstack/scripts/resolvers/preamble.ts` — every skill runs one bash block at start that collects: current branch, session count, config flags, recent learnings, cross-session artifacts. The `preamble-tier` frontmatter field (1-4) controls which prose sections get injected. Tier 1 = minimal utility skills. Tier 4 = full (Voice, Context Recovery, Completeness, Operational Self-Improvement).

**For you:** `git-status` is tier 1. `git-commit` / `review-pr` / `push-pr` are tier 4. Stop paying full-preamble cost on lightweight skills. Define the preamble once as a resolver, inject per-tier.

### 2. `{{INVOKE_SKILL:name}}` composition via prose

`gstack/scripts/resolvers/composition.ts` — when skill A needs skill B's workflow, it emits prose: "Read `/B/SKILL.md`, follow instructions top to bottom, SKIP these sections (already handled): Preamble, AskUserQuestion Format, Completeness, Telemetry." Zero runtime orchestration infrastructure. Just prose contracts.

**For you:** This is how `git-commit-push-pr` composes `git-commit` + `pr-description` without duplication. And how `review-pr` could invoke `code-reviewer` + `structural-reviewer` cleanly instead of embedding the whole review agent definition inline.

### 3. Learnings as append-only JSONL with decay-at-read

`~/.gstack/projects/{slug}/learnings.jsonl` — schema: `{skill, type, key, insight, confidence, source, files, ts, branch, commit}`. Decay: observed/inferred lose 1 confidence point per 30 days at read time (never rewrite). Dedup: latest winner per `key|type`. Preamble auto-surfaces top 3 when count > 5.

**For you:** Your plugin has no memory. Every commit session forgets the last one. A git-workflow `learnings.jsonl` would capture: "This repo's `test:fast` is flaky on clean checkouts" / "CHANGELOG.md requires manual section headers" / "Default branch is `trunk` not `main`." Per-project, append-only, loaded into `git-commit` preamble.

### 4. CLAUDE.md routing injection (self-bootstrapping)

`preamble.ts` `generateRoutingInjection()` — on first run per project, checks if CLAUDE.md has `## Skill routing`. If not, offers to append ~15 lines of routing rules and commit them. The skill teaches the project how to use the skill.

**For you:** First time your plugin runs in a repo, offer to add git-workflow routing to that repo's CLAUDE.md: "User asks to commit → invoke `/gw:commit`. User asks to review PR → invoke `/gw:review-pr`." Persistent routing without you maintaining per-repo config.

### 5. Review Readiness Dashboard

`~/.gstack/reviews/review-log.jsonl` + `gstack-review-log` binary. Tracks which reviews ran when, against which commit hash. Staleness detection via commit comparison — shows a table before merge: "code-review ran 2 commits ago, structural-review ran against current HEAD, security-review NOT RUN."

**For you:** Port this exactly. Before `git push` or `gh pr create`, show a dashboard of which review agents have run against the current HEAD. Catches the "I ran the review 5 commits ago" problem.

### 6. Project-declares-its-own-config

`gstack/CLAUDE.md` lines 152-160: skills MUST NOT hardcode framework commands. Pattern: read CLAUDE.md for project config → if missing, `AskUserQuestion` → persist the answer to CLAUDE.md. The `generateDeployBootstrap` resolver (utility.ts lines 52-87) shows this in action.

**For you:** Your `generate-changelog` skill hardcodes `git-cliff`. Your commit skill assumes conventional commits. A repo using commitlint + standard-version, or raw semver, or monorepo-scoped changelog — breaks. Ask once, persist answer to repo's CLAUDE.md under `## Git Workflow Config`.

## mattpocock/skills — the hook-level piece you're missing

### `git-guardrails-claude-code` — port this verbatim

`skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh` + `SKILL.md`. **PreToolUse** hook that blocks: `git push`, `reset --hard`, `clean -f*`, `branch -D`, `checkout .`, `restore .`. Declarative SKILL.md for installation, executable bash for enforcement. Project-scoped (`.claude/hooks/`) or global (`~/.claude/hooks/`).

This is exactly the gap I called out last round — your plugin has zero harness-level enforcement. This is a drop-in solution written for Claude Code hooks specifically.

### `setup-pre-commit` — Husky orchestration skill

`skills/setup-pre-commit/` — detects package manager, installs husky + lint-staged, wires `.husky/pre-commit` → `prettier/typecheck/test`. Not what commit-craft does (which is runtime pre-commit hook *handling*). This is one-time *setup*. Different skill, different phase.

**For you:** Consider adding `setup-git-hooks` as a separate skill for bootstrapping new repos. commit-craft handles runtime; setup handles provisioning.

### The AGENT-BRIEF pattern (mattpocock's durability principle)

`skills/github-triage/AGENT-BRIEF.md` — template + principles for specifications that survive radical refactors. Rule: describe interfaces/contracts/behaviors, NEVER file paths or line numbers. "Tests/issues should survive radical refactors."

**For you:** Your `pr-description` skill should produce durable PR bodies that don't reference `src/foo.ts:42`. They reference the feature and the contract. This is a writing discipline your skill should encode.

### Reference separation standard

`skills/write-a-skill/SKILL.md` defines the canonical layout:
```
skill-name/
├── SKILL.md           # <100 lines, invocation-time triggers
├── REFERENCE.md       # detailed docs loaded on demand
├── AGENT-BRIEF.md     # durable spec format
└── scripts/           # deterministic utilities
```

**For you:** Your `docs/` directory (`branch-cleanup.md`, `branches.md`, `changelog.md`, etc.) should be restructured as per-skill `REFERENCE.md` files, loaded lazily via backtick paths. Right now those docs are orphaned — nothing in the skills points at them.

## ai-that-works — one specific pattern worth stealing

The repo is mostly educational content, but **Episode #35 (git worktrees for parallel agent work)** and the **12-factor agents** framework are relevant:

- `2025-04-22-twelve-factor-agents/` — "state machines over chains" is exactly the gstack doctrine and the compound-engineering `git-workflow-skills-need-explicit-state-machines` post-mortem. Third independent confirmation of the same pattern.
- **Ralph Wiggum loop** (`2025-10-28-ralph-wiggum-coding-agent-power-tools/`): one-step loops with tests/type-check/build as back-pressure gates. For commit-craft: after each atomic commit, re-run the quality check. Don't batch.

## zeespec — one novel idea, not a whole framework

Skip most of zeespec (it's spec authoring, not workflow). But the **"cross-dimensional intersection as constraint"** pattern is genuinely novel:

> Defining WHO can force-push: useful. Defining WHERE force-push happens: useful. Defining WHEN it's allowed: useful. The constraint is the **intersection**: "force-push on `feature/*` branches, by PR author, with audit log."

**For you:** Your `git-workflow` reference skill defines commit types, branch prefixes, protected branches as independent lists. The real rules are intersections: "`fix/*` branches → require `fix:` or `hotfix:` commits → cannot merge to `main` without review." Encode the intersections, not just the axes.

## Revised priority stack (combining both rounds)

Ranked by leverage:

1. **Port `git-guardrails-claude-code` PreToolUse hook** — cheap, immediate safety gain, sets the precedent for harness-level enforcement
2. **Add per-project `learnings.jsonl`** (gstack pattern) — the thing that makes the plugin *get smarter over time*
3. **Define preamble tiers + `{{INVOKE_SKILL}}` composition resolver** — unlocks clean skill chaining without duplication
4. **Rewrite commit-craft as an explicit state machine** (not prose) — compound-engineering + ai-that-works both independently warn about this
5. **Add `git-commit-push-pr` skill + split `pr-description` out** — the missing middle of your lifecycle
6. **Review Readiness Dashboard** (gstack) — show review staleness before `gh pr create`
7. **CLAUDE.md routing injection + project-config-first** (gstack) — self-bootstrapping, repo-adaptive
8. **Restructure docs/ into per-skill REFERENCE.md** (mattpocock) — lazy load, kill orphans
9. **Namespace commands as `/gw:*`** — plugin identity at command surface
10. **Intersection constraints in conventions** (zeespec) — encode compound rules, not axes

The gstack preamble system is the highest-impact architectural change. Everything else is tactical. Want me to sketch the preamble resolver design for your plugin, or draft the `git-commit-push-pr` SKILL.md as a state machine against gstack's composition conventions?
