# Work Tree Manager: Evolution Path Example

**Real-world case study** showing the proper progression from prompt → sub-agent → skill.

## The Problem

Managing git work trees across a project requires multiple related operations:

- Creating new work trees
- Listing existing work trees
- Removing old work trees
- Merging work tree changes
- Updating work tree status

## Stage 1: Start with a Prompt

**Goal:** Solve the basic problem

Create a simple slash command that creates one work tree:

```bash
/create-worktree feature-branch
```

**Implementation:**

```markdown
# .claude/commands/create-worktree.md

Create a new git worktree for the specified branch.

Steps:
1. Check if branch exists
2. Create worktree directory
3. Initialize worktree
4. Report success
```

**When to stay here:** The task is infrequent or one-off.

**Signal to advance:** You find yourself creating work trees regularly.

## Stage 2: Add Sub-Agent for Parallelism

**Goal:** Scale to multiple parallel operations

When you need to create multiple work trees at once, use a sub-agent:

```bash
Use sub-agent to create work trees for: feature-a, feature-b, feature-c in parallel
```

**Why sub-agent:**

- **Parallelization** - Create 3 work trees simultaneously
- **Context isolation** - Each creation is independent
- **Speed** - 3x faster than sequential

**Sub-agent prompt:**

```markdown
Create work trees for the following branches in parallel:
- feature-a
- feature-b
- feature-c

For each branch:
1. Verify branch exists
2. Create worktree directory
3. Initialize worktree
4. Report status

Use the /create-worktree command for each.
```

**When to stay here:** Parallel creation is the only requirement.

**Signal to advance:** You need to **manage** work trees (not just create them).

## Stage 3: Create Skill for Management

**Goal:** Bundle multiple related operations

The problem has grown beyond creation—you need comprehensive work tree **management**:

```text
skills/work-tree-manager/
├── SKILL.md
├── scripts/
│   ├── validate.py
│   └── cleanup.py
└── reference/
    └── git-worktree-commands.md
```

**SKILL.md:**

```markdown
---
name: work-tree-manager
description: Manage git worktrees - create, list, remove, merge, and update across projects. Use when working with git worktrees or when managing multiple branches simultaneously.
---

# Work Tree Manager

## Operations

### Create
Use /create-worktree command for single operations.
For parallel creation, delegate to sub-agent.

### List
Run: `git worktree list`
Parse output and present in readable format.

### Remove
1. Check if work tree is clean
2. Remove work tree directory
3. Prune references

### Merge
1. Fetch latest changes
2. Merge work tree branch to target
3. Clean up if merge successful

### Update
1. Check status of all work trees
2. Pull latest changes
3. Report any conflicts

## Validation

Before any destructive operation, run:
```bash
python scripts/validate.py <worktree-path>
```

## Cleanup

Periodically run cleanup to remove stale work trees:

```bash
python scripts/cleanup.py --dry-run
```


```bash

**Why skill:**

- **Multiple related operations** - Create, list, remove, merge, update
- **Repeat problem** - Managing work trees is ongoing
- **Domain-specific** - Specialized knowledge about git worktrees
- **Orchestration** - Coordinates slash commands, sub-agents, and scripts

**When to stay here:** Most workflows stop here.

**Signal to advance:** Need external data (GitHub API, CI/CD status).

## Stage 4: Add MCP for External Data

**Goal:** Integrate external systems

Add MCP server to query external repo metadata:

```

skills/work-tree-manager/
├── SKILL.md (updated)
└── ... (existing files)

# Now references GitHub MCP for:
# - Branch protection rules
# - CI/CD status
# - Pull request information

```bash

**Updated SKILL.md section:**
```markdown
## External Integration

Before creating work tree, check GitHub status:
- Use GitHub MCP to query branch protection
- Check if CI is passing
- Verify no open blocking PRs

Query: `GitHub:get_branch_status <branch-name>`
```

**Why MCP:**

- **External data** - Information lives outside Claude Code
- **Real-time** - CI/CD status changes frequently
- **Third-party** - GitHub API integration

## Final State

```

```text
Prompt (Slash Command)
  └─→ Creates single work tree

Sub-Agent
  └─→ Creates multiple work trees in parallel

Skill
  ├─→ Orchestrates: Create, list, remove, merge, update
  ├─→ Uses: Slash commands for primitives
  ├─→ Uses: Sub-agents for parallel operations
  └─→ Uses: Scripts for validation

MCP Server (GitHub)
  └─→ Provides: Branch status, CI/CD info, PR data

Skill + MCP
  └─→ Full-featured work tree manager with external integration
```

## Key Takeaways

### Progression Signals

**Prompt → Sub-Agent:**

- Signal: Need parallelization
- Keyword: "multiple," "parallel," "batch"

**Sub-Agent → Skill:**

- Signal: Need management, not just execution
- Keywords: "manage," "coordinate," "workflow"
- Multiple related operations emerge

**Skill → Skill + MCP:**

- Signal: Need external data or services
- Keywords: "GitHub," "API," "real-time," "status"

### Common Mistakes

❌ **Skipping the prompt**

- Starting with a skill for simple creation

❌ **Overusing sub-agents**

- Using sub-agents when main conversation would work

❌ **Skill too early**

- Creating skill before understanding the full problem domain

✅ **Correct approach**

- Build from bottom up
- Add complexity only when needed
- Each stage solves a real problem

### Decision Checklist

Before advancing to next stage:

**Prompt → Sub-Agent:**

- [ ] Do I need parallelization?
- [ ] Are operations truly independent?
- [ ] Am I okay losing context after?

**Sub-Agent → Skill:**

- [ ] Am I doing this repeatedly (3+ times)?
- [ ] Do I have multiple related operations?
- [ ] Is this a management problem, not just execution?
- [ ] Would orchestration add real value?

**Skill → Skill + MCP:**

- [ ] Do I need external data?
- [ ] Is the data outside Claude Code's control?
- [ ] Would real-time info improve the workflow?

## Real Usage

### Scenario 1: Quick One-Off

**Task:** Create one work tree for hotfix

**Solution:** Slash command

```bash
/create-worktree hotfix-urgent-bug
```

**Why:** Simple, direct, one-time task.

### Scenario 2: Feature Development Sprint

**Task:** Create work trees for 5 feature branches

**Solution:** Sub-agent

```bash
Create work trees in parallel for sprint features:
feature-auth, feature-api, feature-ui, feature-tests, feature-docs
```

**Why:** Parallel execution, independent operations.

### Scenario 3: Ongoing Project

**Task:** Manage all work trees across development lifecycle

**Solution:** Skill

```text
List all work trees, check status, merge completed features, clean up stale ones
```

**Why:** Multiple operations, repeat problem, management need.

### Scenario 4: CI/CD Integration

**Task:** Only create work trees for branches passing CI

**Solution:** Skill + MCP

```bash
Create work trees for features that:
- Have passing CI (check via GitHub MCP)
- Are approved by reviewers
- Have no merge conflicts
```

**Why:** Need external data from GitHub API.

## Summary

The work tree manager evolution demonstrates:

1. **Start simple** - Slash command for basic operation
2. **Scale for parallelism** - Sub-agent for batch operations
3. **Manage complexity** - Skill for full workflow orchestration
4. **Integrate externally** - MCP for real-time external data

**The principle:** Each stage solves a real problem. Don't advance until you hit the limitation of your current approach.

> "When you're starting out, I always recommend you just build a prompt. Everything is a prompt in the end."

Build from the foundation upward.
