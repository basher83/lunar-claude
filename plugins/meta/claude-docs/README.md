# claude-docs

Auto-sync official Claude Code documentation as an Agent Skill with fresh
reference material.

## What it does

- **Provides a skill** with official Claude Code documentation from
  docs.claude.com
- **Auto-updates docs** via SessionStart hook to keep content fresh
- **Progressive disclosure** - loads only relevant docs to manage context
- **14 reference files** covering plugins, skills, hooks, commands, and more

## Installation

```bash
/plugin marketplace add your-org/lunar-claude
/plugin install claude-docs@lunar-claude
```

## Usage

The `claude-code-documentation` skill activates automatically when you ask
about Claude Code features:

- "How do I create a plugin?"
- "What's the structure of SKILL.md?"
- "How do hooks work?"
- "How can I add a slash command?"

Claude will use the skill to access up-to-date official documentation and
provide accurate answers.

## How it works

### Components

- **Skill** (`skills/claude-code-documentation/`) - Entry point with
  progressive disclosure guidance
- **Reference docs** (`skills/claude-code-documentation/reference/`) - 14
  official documentation files
- **SessionStart hook** (`hooks/hooks.json`) - Auto-updates docs on session
  start
- **Update script** (`scripts/claude_docs.py`) - Downloads and caches docs
  from docs.claude.com

### Documentation files

- plugins.md, plugins-reference.md, plugin-marketplaces.md
- skills.md, agent-skills-overview.md, agent-skills-quickstart.md,
  agent-skills-best-practices.md
- slash-commands.md
- hooks-guide.md, hooks.md
- settings.md, output-styles.md, statusline.md
- sub-agents.md

### Auto-update behavior

The SessionStart hook runs the update script in JSON mode, which:

1. Checks cached ETags for each documentation file
2. Downloads only changed files (using HTTP conditional requests)
3. Completes in <1 second when docs are fresh
4. Updates `.download_cache.json` with metadata

## Development

### Manual doc update

Run the script directly for rich output with performance metrics:

```bash
./scripts/claude_docs.py
./scripts/claude_docs.py --all        # Download all 70+ pages
./scripts/claude_docs.py --check      # Check for updates (dry-run)
```

### Script options

- `--output-dir DIR` - Custom output directory
- `--retries N` - Max retry attempts (default: 3)
- `--all` - Download all pages from docs map
- `--check` - Dry-run mode
- `--format json|rich` - Output format (hook uses json, user uses rich)

## License

MIT
