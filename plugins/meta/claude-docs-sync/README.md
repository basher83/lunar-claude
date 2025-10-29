# claude-docs-sync

Automatically maintain fresh Claude Code documentation locally for AI context
enhancement.

## Features

- **SessionStart Hook**: Checks documentation staleness (default: 7 days)
- **Interactive Mode**: Prompts user when docs are stale
- **Auto Mode**: Silent background updates
- **Manual Control**: `/update-docs` command for on-demand updates
- **Smart Caching**: ETag and Last-Modified header checking
- **Format Adaptation**: Rich output for humans, JSON for automation

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install claude-docs-sync:

```bash
/plugin install claude-docs-sync@lunar-claude
```

## Usage

### First Install

On first session start, you'll be prompted to download documentation.

### Interactive Mode (Default)

When docs are >7 days old, you'll see:

```text
Claude Code documentation is 8 days old. Update now?
- Yes, update now
- No, skip
- Auto-update going forward
```

### Auto Mode

To enable automatic updates:

1. Select "Auto-update going forward" when prompted, or
2. Manually edit `hooks/check-docs-staleness.json` and set `mode: "auto"`

### Manual Updates

```bash
/update-docs              # Update default pages
/update-docs --all        # Download all 70+ pages
/update-docs --check      # Dry-run to see what needs updating
/update-docs --interactive # Choose specific pages
```

## Configuration

Edit `hooks/check-docs-staleness.json`:

```json
{
  "mode": "interactive",
  "staleness_days": 7
}
```

**Settings:**

- `mode`: "interactive" | "auto"
- `staleness_days`: Days before docs considered stale (default: 7)

## Components

- **Hook**: `check-docs-staleness.json` - SessionStart staleness detection
- **Command**: `update-docs.md` - Manual documentation updates
- **Skill**: `claude-code-documentation` - Doc awareness trigger
- **Script**: `tools/claude_docs.py` - Documentation downloader

## Version History

- 0.1.0 - Initial release with interactive/auto modes
