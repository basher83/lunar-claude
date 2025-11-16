# claude-docs

Auto-syncs official Claude Code documentation as a skill with fresh reference
material.

## Features

- Provides the `official-docs` skill with documentation from docs.claude.com
- Updates documentation automatically via SessionStart hook
- Loads only relevant files through progressive disclosure
- Maintains 17 reference files covering plugins, skills, hooks, and commands

## Installation

```bash
/plugin marketplace add your-org/lunar-claude
/plugin install claude-docs@lunar-claude
```

Note: Plugin name is `claude-docs`. Skill name is `official-docs` (renamed to
comply with Anthropic requirements).

## Usage

Ask questions about Claude Code features. The skill activates automatically:

- "How do I create a plugin?"
- "What's the structure of SKILL.md?"
- "How do hooks work?"
- "How can I add a slash command?"

Claude accesses current official documentation and provides accurate answers.

## Architecture

### Components

**Skill** (`skills/official-docs/`) - Entry point with progressive disclosure
guidance

**Reference docs** (`skills/official-docs/reference/`) - 17 documentation files
downloaded from docs.claude.com

**SessionStart hook** (`hooks/hooks.json`) - Triggers documentation sync on
session start

**Update script** (`scripts/claude_docs.py`) - Downloads and caches
documentation using HTTP conditional requests

### Documentation Files

Plugins: plugins.md, plugins-reference.md, plugin-marketplaces.md

Skills: skills.md, agent-skills-overview.md, agent-skills-quickstart.md,
agent-skills-best-practices.md

Automation: slash-commands.md, hooks-guide.md, hooks.md

Configuration: settings.md, output-styles.md, statusline.md, sub-agents.md

Integration: mcp.md, code-execution-with-mcp.md, memory.md

### Auto-Update Mechanism

SessionStart hook executes `claude_docs.py --format json`:

1. Checks cached ETags for each file
2. Downloads only changed files via HTTP conditional requests
3. Completes in under 1 second when documentation is current
4. Updates `.download_cache.json` with ETags and timestamps

## Development

### Manual Updates

Run the script directly for detailed output:

```bash
./scripts/claude_docs.py              # Update curated pages
./scripts/claude_docs.py --all        # Download all 70+ pages
./scripts/claude_docs.py --check      # Check for updates without downloading
```

### Script Options

```bash
--output-dir DIR      # Custom output directory
--retries N           # Max retry attempts (default: 3)
--all                 # Download all pages from docs map
--check               # Dry-run mode
--format json|rich    # Output format (hook uses json, CLI uses rich)
```

### Testing

```bash
pytest plugins/meta/claude-docs/tests/
```

## License

MIT
