---
name: git-commit
description: Internal commit step for the blake-os git-ops router. Stages explicit file paths and creates atomic commits on the current branch, matching the repo's existing message style and scanning for secrets before staging. Invoked by blake-os:git-ops — not a direct entry point. Trigger directly only on the exact request "git commit".
---

# Git Commit

Create one or more atomic commits from the working tree. Autonomous by default — execute without asking unless the user says "show plan first" or "confirm before commit".

## Metadata

Run from repo root:

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/git-commit/scripts/git-changes.mjs"
echo "---recent-subjects---"
git log --pretty=%s -n 20 2>/dev/null || true
```

If `in_repo: no`, stop: "This directory is not a git repository."

If status shows clean working tree, stop: "Nothing to commit."

## Workflow

### Step 1: Check remote state (does NOT block committing)

Measure whether the remote moved while work was in progress. This is informational — it never stops the commit. Committing while behind is fine; the merge happens later in `git-sync`.

```bash
git fetch origin 2>/dev/null || true
git rev-list --left-right --count @{u}...HEAD 2>/dev/null   # output: "<behind>	<ahead>"
```

Remember the **behind** number (the first one) — surface it in Step 6. Do not run `git pull` here, and do not skip committing for any remote state.

### Step 2: Analyze changes

Use the Metadata block (`---status---`, `---diffstat---`, `---recent-subjects---`).

- For small changes (≲5 lines per file in diffstat), infer intent from path + counts — skip full `git diff`
- Run `git diff <path>` only when intent is unclear from filename and diffstat
- For untracked directories (`?? path/`), treat contents as the change unless the directory is huge

### Step 3: Plan commit groups

Scan for distinct concerns. Split when obvious; one commit when ambiguous.

Apply the grouping rules in [references/conventions.md](references/conventions.md) — file-level groups, file-type ordering across multiple commits, small diffs to a single commit.

Draft messages matching `---recent-subjects---` style. If history is empty or mixed, use the default types from [references/conventions.md](references/conventions.md).

### Step 4: Safety check

Before staging, scan paths for secrets: `.env`, `credentials`, `*.pem`, `*.key`, token files. Exclude them and warn if present.

Never stage with `git add -A` or `git add .`. Stage explicit file paths only.

### Step 5: Commit

Commit on the **current branch**. Do not create feature branches; commits go straight to wherever HEAD is (typically `main`).

For each group:

```bash
git add path/to/file1 path/to/file2 && git commit -m "$(cat <<'EOF'
type: subject line

Optional body explaining why.
EOF
)"
```

### Step 6: Confirm

```bash
git log --oneline -n <number-of-commits-created>
git status --short --branch
```

Report: commit hash(es), subject line(s), files per commit.

If the **behind** count from Step 1 was greater than 0, the local branch is now diverged from the remote. Add a line: "⚠ The remote advanced by N commits while you worked — run **git-sync** to merge them in before **git-push**." Do not push a diverged branch.

## Authorship

- Never add co-author trailers or AI attribution
- Write messages as if the user wrote them

## Optional confirmation mode

Only when user explicitly requests review: present the plan (files per commit + messages) and wait for approval before Step 5.

## Guardrails

- Stage explicit file paths only — never `git add -A` or `git add .`.
- Never stage `.env`, credentials, `*.pem`, `*.key`, or token files; warn if present.
- Never create feature branches — commit to the current branch.
- Never push a diverged branch — if the remote advanced, `git-sync` integrates first.

## Order

Ordering across operations is owned by `blake-os:git-ops`.
