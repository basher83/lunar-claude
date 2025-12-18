---
description: Comprehensive git branch cleanup and organization
allowed-tools: Bash(git:*), Bash(gh:*), AskUserQuestion
---

# Comprehensive Git Branch Cleanup

Perform a complete cleanup of local and remote branches after working on multiple PRs.

## Current State

- Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"`
- Current branch: !`git branch --show-current`
- Fetch latest: !`git fetch --all --prune 2>&1`

## Branch Inventory

### All Branches

Local branches with tracking status:

!`git branch --format='%(refname:short) %(upstream:track)' | sort`

Recent branches by activity:

!`git for-each-ref --count=15 --sort=-committerdate refs/heads/ --format='%(refname:short) - %(committerdate:relative)'`

Remote branches:

!`git branch -r --format='%(refname:short)' | grep -v HEAD | sort`

### Cleanup Candidates

Merged into default branch:

!`git branch --merged $(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main") --format='%(refname:short)' | grep -v -E "^(main|master|develop|staging|production)$" | grep -v -E "^(release|renovate)/" | sort`

Branches with gone remotes:

!`git branch -vv | grep ': gone]' | awk '{print $1}' | sort`

Stale remote-tracking refs (would be pruned):

!`git remote prune origin --dry-run 2>&1 | grep '\[would prune\]' | awk '{print $NF}' || echo "None"`

## Protected Branches

Never delete branches matching these patterns:

- `main`, `master`, `develop`, `staging`, `production`
- `release/*` branches (unless explicitly confirmed via AskUserQuestion)
- `renovate/*` branches (managed by Renovate bot)
- Current working branch
- Branches with unpushed commits (use AskUserQuestion to confirm)

## Cleanup Workflow

### Phase 1: Analyze

1. Review the branch inventory above
2. Identify the default branch (protect from deletion)
3. Categorize branches:
   - **Safe to delete**: Merged branches and branches with gone remotes (excluding protected)
   - **Needs confirmation**: `release/*` branches, branches with unpushed commits
   - **Protected**: All protected branch patterns and current branch

### Phase 2: Confirm Cleanup Plan

Before deleting anything, present the cleanup plan and use AskUserQuestion:

**Question: Cleanup scope**
- header: "Cleanup"
- question: "Which branches should be deleted?"
- multiSelect: false
- options:
  - All safe (Delete all merged and gone-remote branches)
  - Merged only (Delete only branches merged into default)
  - Gone only (Delete only branches with deleted remotes)
  - Review each (Confirm each branch individually)

If user selects "Review each", iterate through each candidate branch with:

**Question: Per-branch confirmation**
- header: "Delete?"
- question: "Delete branch '[branch-name]'? ([merged/gone], last commit: [date])"
- options:
  - Yes (Delete this branch)
  - No (Keep this branch)
  - Stop (Abort remaining cleanup)

### Phase 3: Execute Cleanup

After user confirmation, execute in order:

1. **Prune stale remote-tracking refs**: `git remote prune origin`
2. **Delete merged local branches**: `git branch -d [branch-name]`
3. **Delete gone-remote branches**: `git branch -D [branch-name]`

For each deletion, record the branch name and SHA before deleting:
`git rev-parse [branch-name]`

**If deletion fails**, use AskUserQuestion:

- header: "Failed"
- question: "Failed to delete '[branch-name]': [error]. What should we do?"
- options:
  - Force (Use git branch -D to force delete)
  - Skip (Leave this branch, continue with others)
  - Abort (Stop cleanup, keep remaining branches)

### Phase 4: Remote Cleanup (Optional)

After local cleanup, use AskUserQuestion:

- header: "Remotes"
- question: "Delete corresponding remote branches on origin?"
- options:
  - Yes (Run git push origin --delete for each deleted local branch)
  - No (Keep remote branches, only cleaned up locally)

### Phase 5: Summary

Provide cleanup summary:

```text
Branch Cleanup Summary:
- Deleted N merged feature branches
- Removed N branches with gone remotes
- Pruned N stale remote references
- Repository now has N active branches (was M)

Recovery Commands:
```

For each deleted branch, output:
`git checkout -b [branch-name] [sha]`

Final branch state:

!`git branch --format='%(refname:short)'`
