---
name: git-status
description: Summarize the current state of the git repository
context: fork
---

Summarize the current state of the git repository.

Run the following commands to gather state:

```bash
$ git status -sb
$ git status --short
$ git log --oneline -5
$ git stash list
```

Provide a concise summary including:

1. **Branch status**: Current branch and ahead/behind remote
2. **Working directory**: Count of staged, unstaged, and untracked changes
3. **Recent activity**: Brief summary of recent commits
4. **Action items**: Suggested next steps based on current state
