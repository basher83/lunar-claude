# git-workflow

Git workflow automation plugin for Claude Code.

## Features

- **git-workflow skill**: Best practices for conventional commits and branch naming
- **commit-craft agent**: Creates clean, atomic commits following conventional commit standards
- **branch-cleanup command**: Comprehensive branch cleanup with multiple modes (dry-run, force, remote-only, local-only)
- **git-commit command**: Orchestrates pre-commit hooks and invokes commit-craft
- **git-status command**: Quick git repository status summary
- **generate-changelog command**: Generate CHANGELOG.md using git-cliff with optional version tagging

## Installation

```bash
claude plugin install git-workflow@lunar-claude
```

## Usage

### Commands

All commands use workflow-driven patterns with interactive prompts.

```bash
/git-status          # Repository status summary
/git-commit          # Pre-commit hooks + commit-craft agent
/branch-cleanup      # Interactive branch cleanup workflow
/generate-changelog  # Changelog generation with Preview/Generate/Release options
```

### Agent

The `commit-craft` agent can be invoked directly or via `/git-commit`:

- Analyzes workspace changes
- Groups related changes into atomic commits
- Follows conventional commit format
- Handles pre-commit hook failures gracefully

## Dependencies

- `git` - Git version control
- `gh` - GitHub CLI (optional, for PR status checks)
- `pre-commit` - Pre-commit hooks (optional)
- `git-cliff` - Changelog generator (for /generate-changelog)

## License

MIT
