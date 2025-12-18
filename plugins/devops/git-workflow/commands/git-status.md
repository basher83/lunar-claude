---
description: Summarize the current state of the git repository
allowed-tools: Bash(git:*)
model: haiku
---

# Git Status

Summarize the current state of the git repository.

## Repository State

Branch and sync status: !`git status -sb`

Working directory: !`git status --short`

Recent commits: !`git log --oneline -5`

Stashes: !`git stash list`

## Task

Provide a concise summary including:

1. **Branch status**: Current branch and ahead/behind remote
2. **Working directory**: Count of staged, unstaged, and untracked changes
3. **Recent activity**: Brief summary of recent commits
4. **Action items**: Suggested next steps based on current state
