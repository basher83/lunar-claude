---
description: Summarize the current state of the git repository
allowed-tools: Bash(git:*)
model: haiku
---

# Git Status

Analyze and summarize the current state of the git repository.

## Repository State

- Current Status: !`git status`
- Current branch: !`git branch --show-current`
- Unstaged files: !`git diff --name-status`
- Staged files: !`git diff --cached --name-status`
- Unpushed commits: !`git log --oneline origin/$(git branch --show-current)..HEAD 2>/dev/null || echo "No upstream branch or no unpushed commits"`
- Untracked files: !`git ls-files --others --exclude-standard`

## Task

Provide a concise summary of the repository state including:

1. **Branch status**: Current branch and tracking information
2. **Working directory**: Summary of staged, unstaged, and untracked changes
3. **Sync status**: Commits ahead/behind remote
4. **Action items**: Suggested next steps based on current state
