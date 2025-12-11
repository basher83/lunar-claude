---
description: Run pre-commit hooks and create clean, logical commits
allowed-tools: TodoWrite, Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Git Commit Workflow

Orchestrate pre-commit hooks and invoke commit-craft agent for clean, logical commits.

## Current State

- Current Status: !`git status`
- Current branch: !`git branch --show-current`
- Check for merge/rebase: !`test -f .git/MERGE_HEAD && echo "MERGE IN PROGRESS" || test -d .git/rebase-merge && echo "REBASE IN PROGRESS" || echo "Clean"`
- Staged files: !`git diff --cached --name-only`
- Check for sensitive files: !`git diff --cached --name-only | grep -iE '\.(env|mcp\.json)$|secret|token|key|password' || echo "No sensitive files detected"`

## Workflow

### Step 1: Pre-flight Checks

Verify repository state:

- Ensure no merge or rebase in progress
- Check for sensitive files in staged changes
- If sensitive files detected, warn and ask for confirmation

### Step 2: Run Pre-commit Hooks

Execute pre-commit hooks to format and lint code:

!`pre-commit run --all-files 2>&1 || echo "Pre-commit completed (check output above)"`

If hooks modify files:

1. Review the changes made
2. Re-stage modified files
3. Continue to commit creation

### Step 3: Create Commits

Invoke the commit-craft agent to:

1. Analyze all workspace changes
2. Group related changes into atomic commits
3. Create conventional commit messages
4. Execute commits handling any additional hook runs

The commit-craft agent will organize changes intelligently and create well-structured commits following conventional commit format.
