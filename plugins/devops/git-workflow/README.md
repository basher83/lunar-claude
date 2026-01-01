# Git Workflow

Git workflow automation plugin for Claude Code with conventional commits, atomic commit
organization, and branch management.

## Overview

The git-workflow plugin provides tools for maintaining clean git history:

1. **git-workflow skill** - Best practices for conventional commits and branch naming
2. **commit-craft agent** - Creates clean, atomic commits from workspace changes
3. **4 workflow commands** - Status, commit, branch cleanup, and changelog generation

All commands use workflow-driven patterns with interactive prompts rather than command-line arguments.

## Commands

### /git-status

Quick repository status summary.

**What it shows:**

- Branch name and sync status with remote
- Working directory changes (staged/unstaged)
- Recent commits (last 5)
- Stash list

### /git-commit

Orchestrates pre-commit hooks and commit creation.

**Workflow:**

1. Shows branch status and pre-flight checks
2. Detects sensitive files (.env, credentials)
3. Runs pre-commit hooks
4. Invokes commit-craft agent for atomic commits

### /branch-cleanup

Interactive branch cleanup workflow.

**What it handles:**

- Merged branches (safe to delete)
- Branches with deleted remotes ([gone] status)
- Protected branch exclusion (main, master, develop, staging, production, release/*)
- Optional remote cleanup

### /generate-changelog

Changelog generation using git-cliff.

**Workflow options:**

- **Preview** - Show unreleased changes without writing
- **Generate** - Create/update CHANGELOG.md and commit
- **Release** - Generate changelog + create version tag (with AI-recommended bump level)

## Agent

### commit-craft

Creates clean, atomic commits from workspace changes.

**Capabilities:**

- Analyzes workspace changes and identifies logical groupings
- Creates atomic commits following conventional commit format
- Handles pre-commit hook failures gracefully
- Generates clear commit messages with proper scope and type

**Trigger phrases:** "create commits", "commit all changes", "organize commits", "make commits"

## Skill

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

## Installation

```bash
claude plugin install git-workflow@lunar-claude
```

Or for development:

```bash
cc --plugin-dir /path/to/git-workflow
```

## Dependencies

- `git` - Git version control (required)
- `pre-commit` - Pre-commit hooks (optional, for /git-commit)
- `git-cliff` - Changelog generator (required for /generate-changelog)
- `gh` - GitHub CLI (optional, for PR status)

## Use Cases

### After implementing a feature

```text
User: "I've finished the authentication module"
→ commit-craft agent triggers proactively
→ Analyzes changes, groups into atomic commits
→ Creates conventional commit messages
```

### Before a release

```text
/generate-changelog
→ Shows unreleased changes since last tag
→ Select "Release" workflow
→ AI recommends version bump (patch/minor/major)
→ Creates changelog + version tag
```

### Cleaning up branches

```text
/branch-cleanup
→ Shows merged and stale branches
→ Excludes protected branches
→ Interactive selection of cleanup scope
→ Shows recovery commands with commit SHAs
```

## Version

1.0.3

## Author

basher83

## License

MIT
