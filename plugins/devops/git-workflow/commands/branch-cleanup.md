---
description: Clean up merged branches, stale remotes, and organize branch structure
argument-hint: "[--dry-run] | [--force] | [--remote-only] | [--local-only]"
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep
model: sonnet
---

# Git Branch Cleanup & Organization

Clean up merged branches and organize repository structure: $ARGUMENTS

## Current Repository State

- All branches: !`git branch -a`
- Recent branches: !`git for-each-ref --count=10 --sort=-committerdate refs/heads/ --format='%(refname:short) - %(committerdate:relative)'`
- Remote branches: !`git branch -r`
- Merged branches: !`git branch --merged main 2>/dev/null || git branch --merged master 2>/dev/null || echo "No main/master branch found"`
- Current branch: !`git branch --show-current`

## Task

Perform comprehensive branch cleanup and organization based on the repository state and provided arguments.

## Cleanup Operations

### 1. Identify Branches for Cleanup

- **Merged branches**: Find local branches already merged into main/master
- **Stale remote branches**: Identify remote-tracking branches that no longer exist
- **Old branches**: Detect branches with no recent activity (>30 days)

### 2. Safety Checks Before Deletion

- Verify branches are actually merged using `git merge-base`
- Check if branches have unpushed commits
- Confirm branches aren't the current working branch
- Validate against protected branch patterns

### 3. Protected Branches

Never delete branches matching these patterns:

- `main`, `master`, `develop`, `staging`, `production`
- `release/*` (unless explicitly confirmed)
- Current working branch
- Branches with unpushed commits (unless forced)

## Command Modes

### Default Mode (Interactive)

1. Show branch analysis with recommendations
2. Ask for confirmation before each deletion
3. Provide summary of actions taken

### Dry Run Mode (`--dry-run`)

1. Show what would be deleted without making changes
2. Display branch analysis and recommendations
3. Exit without modifying repository

### Force Mode (`--force`)

1. Delete merged branches without confirmation
2. Clean up stale remotes automatically
3. Provide summary of all actions taken

### Remote Only (`--remote-only`)

1. Only clean up remote-tracking branches
2. Synchronize with actual remote state using `git remote prune origin`
3. Keep all local branches intact

### Local Only (`--local-only`)

1. Only clean up local branches
2. Don't affect remote-tracking branches
3. Focus on local workspace organization

## Output

Provide cleanup summary:

```text
Branch Cleanup Summary:
✅ Deleted N merged feature branches
✅ Removed N stale remote references
⚠️  Found N unmerged branches requiring attention
📊 Repository now has N active branches (was M)
```

Include recovery commands for any deleted branches:

```text
git checkout -b branch-name SHA  # Recover branch
```
