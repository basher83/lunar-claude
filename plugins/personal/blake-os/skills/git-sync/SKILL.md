---
name: git-sync
description: Internal sync step for the blake-os git-ops router. Brings the current branch up to date with origin — fast-forwards when only behind, makes a merge commit when local and remote diverged, aborts and hands off on conflict; never rebases or force-pushes. Invoked by blake-os:git-ops — not a direct entry point. Trigger directly only on the exact request "git pull" or "git sync".
---

# Git Sync

Bring the local branch current with `origin`. Fast-forward when the branch is only behind; merge to integrate when local and remote have both moved. Never rebase, never force-push, never resolve conflicts automatically.

## When to run

- The router (`blake-os:git-ops`) sends a "get the latest" request
- As the integrate step of a full backup, **after** `git-commit` — a clean working
  tree is required (Step 3), which is why the router commits first
- Directly, only on the exact request "git pull" or "git sync"

## Workflow

### Step 1: Verify repo and remote

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && echo "in_repo: yes"
git remote get-url origin
git branch --show-current
```

If not a git repo, stop: "This directory is not a git repository."
If no `origin` remote, stop: "No remote configured." Do not invent one.

### Step 2: Fetch and measure state

```bash
git fetch origin
git rev-list --left-right --count @{u}...HEAD   # output: "<behind>	<ahead>"
git status --porcelain                          # any output = dirty working tree
```

If `git fetch` fails (network, auth), report the error verbatim and stop. Do not pull.

The `rev-list` line prints two numbers: **behind** (commits the remote has that the local branch doesn't) and **ahead** (local commits the remote doesn't have). These two numbers drive the decision in Step 3 — not error-message text. (If `@{u}` errors because no upstream is set, the branch has never been pushed; there is nothing to sync — tell the user to `git-push` to publish it.)

### Step 3: Act on the measured state

**`behind = 0`** — already current. If `ahead > 0`, note there are unpushed commits (run `git-push`). Done.

**`behind > 0` and `ahead = 0`** — simple fast-forward:

```bash
git pull --ff-only
```

On success, report how many commits were pulled. If it fails because the working tree is dirty (local changes would be overwritten), **stop** — list the blocking files and tell the user to commit them with `git-commit` or set them aside, then sync again. Do not stash.

**`behind > 0` and `ahead > 0`** — diverged; both sides committed. Integrate with a merge:

1. The working tree must be clean first. If `git status --porcelain` printed anything, **stop**: "You have uncommitted changes — commit them with `git-commit`, then sync to integrate." Do not stash, do not merge over a dirty tree.
2. With a clean tree, merge:

   ```bash
   git pull --no-rebase --no-edit
   ```

   `--no-edit` accepts the default merge-commit message so the command never stalls waiting on an editor.

   - **Clean merge:** report the merge commit and how many remote commits were integrated. Local is now `ahead N / behind 0` — tell the user to run `git-push`.
   - **Conflict** (the command exits non-zero, or `git status` shows unmerged `UU` paths): abort immediately and hand off —

     ```bash
     git merge --abort
     ```

     Then **stop**: list the conflicted files and report "Automatic merge hit conflicts; reverted to the pre-merge state. These need to be resolved by hand." Never edit files to resolve a conflict.

### Step 4: Confirm

```bash
git rev-list --left-right --count @{u}...HEAD
git status --short --branch
```

Report: branch, behind/ahead after sync, whether a merge commit was created, clean or dirty tree.

## Guardrails

- **Merge is the only integration method.** Never `git rebase`, never `git reset --hard`, never force-push.
- **Never auto-resolve conflicts** — `git merge --abort` and hand off to a human.
- **Never stash** unless the user explicitly asks.
- **Never create feature branches.**

## Order

Ordering across operations is owned by `blake-os:git-ops`.
