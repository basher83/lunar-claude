# Git Workflow

Git workflow automation plugin for Claude Code with conventional commits, atomic commit
organization, and branch management.

## Overview

The git-workflow plugin provides fork-isolated skills for maintaining clean git history:

1. **git-workflow skill** - Best practices for conventional commits and branch naming
2. **commit-craft agent** - Creates clean, atomic commits (invoked through git-commit skill)
3. **4 workflow skills** - Status, commit, branch cleanup, and changelog generation

All workflow skills use `context: fork` for delegation isolation. The commit skill delegates
to the commit-craft agent, which handles the full commit workflow including pre-commit hook
detection, execution, and failure recovery.

## Skills

### git-commit

Create clean, atomic commits with pre-commit hook handling.

**How it works:**

1. Invokes commit-craft agent in a fork-isolated context
2. commit-craft detects and runs pre-commit hooks
3. Analyzes changes, groups into atomic commits
4. Creates conventional commit messages
5. Handles hook failures with re-staging and retry

### git-status

Quick repository status summary.

**What it shows:**

- Branch name and sync status with remote
- Working directory changes (staged/unstaged)
- Recent commits (last 5)
- Stash list

### branch-cleanup

Interactive branch cleanup workflow.

**What it handles:**

- Merged branches (safe to delete)
- Branches with deleted remotes ([gone] status)
- Protected branch exclusion (main, master, develop, staging, production, release/*)
- Optional remote cleanup

### generate-changelog

Changelog generation using git-cliff. Accepts an optional action argument.

**Actions:**

- **preview** - Show unreleased changes without writing
- **generate** - Create/update CHANGELOG.md and commit
- **release** - Generate changelog + create version tag (with AI-recommended bump level)

## Agent

### commit-craft

Creates clean, atomic commits from workspace changes. Invoked through the git-commit skill
with `context: fork` for delegation isolation — not invoked directly.

**Capabilities:**

- Detects and handles pre-commit hooks (execution, formatter re-staging, failure recovery)
- Analyzes workspace changes and identifies logical groupings
- Creates atomic commits following conventional commit format
- Generates clear commit messages with proper scope and type

## Reference Skill

### git-workflow

Best practices for conventional commits and branch naming.

**Trigger phrases:** "conventional commits", "commit format", "branch naming", "commit types"

**What it covers:**

- Conventional commit format (type, scope, subject, body, footer)
- Commit types (feat, fix, docs, style, refactor, perf, test, build, ci, chore)
- Branch naming conventions (feature/, fix/, hotfix/, release/, docs/)
- Atomic commit principles
- Pre-commit workflow

**Note:** Project-specific CLAUDE.md conventions take precedence over skill defaults.

## Dependencies

- `git` - Git version control (required)
- `pre-commit` - Pre-commit hooks (optional, for git-commit)
- `git-cliff` - Changelog generator (required for generate-changelog)
- `gh` - GitHub CLI (optional, for PR status)

## License

MIT
