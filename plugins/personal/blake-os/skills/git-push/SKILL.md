---
name: git-push
description: Internal push step for the blake-os git-ops router. Publishes local commits to origin only when the branch is current, after verifying it is not behind; never force-pushes. Invoked by blake-os:git-ops — not a direct entry point. Trigger directly only on the exact request "git push".
---

# Git Push

Publish local commits to `origin` — but only when the branch is current with the remote. If the remote moved, integrate first with `git-sync`, then push. A push is never forced.

## Prerequisites

Commit first. If the working tree has uncommitted changes, run **git-commit** or report what is still dirty.

## Workflow

### Step 1: Verify repo and remote

```bash
git remote get-url origin
git branch --show-current
```

If no `origin` remote, stop: "No remote configured. Add one with: git remote add origin <url>"

### Step 2: Fetch and measure state

```bash
git fetch origin
git rev-list --left-right --count @{u}...HEAD   # output: "<behind>	<ahead>"
```

The `rev-list` line prints **behind** then **ahead**. Decide on the numbers:

- **`behind = 0`, `ahead = 0`** — stop: "Already up to date with remote — nothing to push." (If `@{u}` errors because no upstream is set, the branch is new — go straight to Step 3, which sets the upstream.)
- **`behind > 0`** (the remote has commits the local branch doesn't, whether or not it is also ahead) — **stop and do not push.** Report: "Remote has N commits you don't have. Run **git-sync** first to integrate them (it will fast-forward or merge), then push." A push now would be rejected — do not attempt it.
- **`behind = 0`, `ahead > 0`** — clear to push. Continue to Step 3.

### Step 3: Push

If the branch has no upstream:

```bash
git push -u origin HEAD
```

If an upstream exists:

```bash
git push
```

**Never** `git push --force` or `--force-with-lease`.

### Step 4: Verify

```bash
git fetch origin && git rev-list --left-right --count @{u}...HEAD
```

Confirm `behind = 0, ahead = 0` — local matches remote. Report: branch, remote URL, number of commits pushed.

## Guardrails

- **Never force-push.**
- **Never push while behind** — integrate via `git-sync` first.
- **Never push secrets** — if `.env` or credential files appear in the outgoing commits, stop and warn.
- If the push is rejected for another reason (auth, pre-receive hook), report the error verbatim. Do not force.

## Order

Ordering across operations is owned by `blake-os:git-ops`.
