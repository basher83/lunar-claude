---
name: branch-cleanup
description: Comprehensive git branch cleanup and organization
context: fork
---

Perform a complete cleanup of local and remote branches after working on multiple PRs.

## Phase 1: Analyze

Gather branch inventory:

```bash
$ git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"
$ git branch --show-current
$ git fetch --all --prune 2>&1
```

List all branches:

```bash
$ git branch --format='%(refname:short) %(upstream:track)' | sort
$ git for-each-ref --count=15 --sort=-committerdate refs/heads/ --format='%(refname:short) - %(committerdate:relative)'
$ git branch -r --format='%(refname:short)' | grep -v HEAD | sort
```

Identify cleanup candidates:

```bash
$ git branch --merged
$ git branch -vv | grep ': gone]' | awk '{print $1}' | sort
```

Categorize branches:

- **Safe to delete**: Merged branches and branches with gone remotes (excluding protected)
- **Needs confirmation**: `release/*` branches, branches with unpushed commits
- **Protected**: `main`, `master`, `develop`, `staging`, `production`, `release/*`, `renovate/*`, current branch

## Phase 2: Confirm Cleanup Plan

Present the cleanup plan and ask the user to select scope:

- **All safe**: Delete all merged and gone-remote branches
- **Merged only**: Delete only branches merged into default
- **Gone only**: Delete only branches with deleted remotes
- **Review each**: Confirm each branch individually

If "Review each" is selected, iterate through candidates asking per-branch confirmation.

## Phase 3: Execute Cleanup

After confirmation, execute in order:

1. Prune stale remote-tracking refs: `git remote prune origin`
2. Delete merged local branches: `git branch -d <branch>`
3. Delete gone-remote branches: `git branch -D <branch>`

Record each branch name and SHA before deleting: `git rev-parse <branch>`

If deletion fails, ask user: Force delete, Skip, or Abort.

## Phase 4: Remote Cleanup (Optional)

Ask whether to delete corresponding remote branches on origin.

## Phase 5: Summary

Report:

- Count of deleted branches by category
- Repository branch count (before and after)
- Recovery commands with commit SHAs for each deleted branch: `git checkout -b <branch> <sha>`
