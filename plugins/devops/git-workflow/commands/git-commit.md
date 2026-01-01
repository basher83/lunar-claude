---
description: Run pre-commit hooks and create clean, logical commits
allowed-tools: Bash(git:*), Bash(pre-commit:*), Bash(test:*), Task, AskUserQuestion
---

# Git Commit Workflow

Orchestrate pre-commit hooks and invoke commit-craft agent for clean, logical commits.

## Current State

- Branch and status: !`git status -sb`
- Working directory: !`git status --short`
- Merge/rebase state: !`test -f .git/MERGE_HEAD && echo "MERGE IN PROGRESS" || test -d .git/rebase-merge && echo "REBASE IN PROGRESS" || echo "Clean"`
- Staged files: !`git diff --cached --name-only`
- Sensitive files check: !`git diff --cached --name-only | grep -iE '\.(env|mcp\.json)$|secret|token|key|password' || echo "None detected"`

## Workflow

### Step 1: Pre-flight Checks

Verify repository state:

1. If merge or rebase in progress, stop and inform user
2. If sensitive files detected, use AskUserQuestion:
   - header: "Sensitive"
   - question: "Sensitive files detected in staged changes. Proceed with commit?"
   - options:
     - Continue (I understand the risk, proceed)
     - Unstage (Remove sensitive files from staging)
     - Abort (Cancel commit workflow)

### Step 2: Run Pre-commit Hooks

Execute pre-commit hooks:

!`pre-commit run -a`

Analyze the output:

- If hooks pass: Continue to Step 3
- If hooks fail with errors: Report errors and stop
- If hooks modify files (formatting, etc.):
  1. Show which files were modified
  2. Re-stage modified files: `git add -u`
  3. Continue to Step 3

### Step 3: Create Commits

Use the Task tool to invoke the commit-craft agent:

- subagent_type: "commit-craft"
- prompt: "Create clean, atomic commits for the current workspace changes"

The commit-craft agent will:

1. Analyze all workspace changes
2. Group related changes into atomic commits
3. Create conventional commit messages
4. Execute commits handling any additional hook runs
