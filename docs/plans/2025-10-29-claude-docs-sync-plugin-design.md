# Claude Docs Sync Plugin Design

**Date:** 2025-10-29
**Plugin Name:** `claude-docs-sync`
**Category:** meta
**Status:** Design Phase

## Purpose

Automatically maintain fresh Claude Code documentation locally for AI context
enhancement. The plugin checks documentation staleness at session start, prompts
for updates when needed, and provides both manual and automatic update modes.

## Architecture Overview

### Plugin Structure

```text
plugins/meta/claude-docs-sync/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── documentation-awareness/
│       └── SKILL.md
├── commands/
│   └── update-docs.md
├── hooks/
│   └── check-docs-staleness.json
├── tools/
│   └── claude_docs.py
└── README.md
```

## Components

### 1. SessionStart Hook

**File:** `hooks/check-docs-staleness.json`

**Configuration:**

```json
{
  "name": "check-docs-staleness",
  "trigger": "SessionStart",
  "config": {
    "mode": "interactive",
    "staleness_days": 7
  }
}
```

**Modes:**

**Interactive (default):**

- Checks cache age at session start
- If documentation >7 days old, uses AskUserQuestion tool
- Presents options: "Yes, update now" | "No, skip" | "Auto-update going forward"
- On "Yes" → Executes `/update-docs --format json`
- On "Auto-update going forward" → Updates hook config to `mode: "auto"`
- Fast execution (<100ms for staleness check)

**Auto:**

- Checks cache age at session start
- If documentation >7 days old, runs `/update-docs --format json` silently
- Displays brief status: "✓ Docs updated (11 pages, 3.2s)"
- No user prompt required

### 2. Slash Command

**File:** `commands/update-docs.md`

**Signature:**

```bash
/update-docs [--all] [--check] [--interactive] [--format json|rich]
```

**Options:**

- `--all`: Download all 70+ pages from docs map (default: curated 14 pages)
- `--check`: Dry-run, show what needs updating
- `--interactive`: Prompt for page selection
- `--format json|rich`: Output format (auto-detected based on caller)

**Behavior:**

- Invokes `tools/claude_docs.py` with specified options
- Auto-detects format: hook calls → json, user calls → rich
- Returns execution status to Claude for parsing

### 3. Skill

**File:** `skills/claude-code-documentation/SKILL.md`

**Purpose:**

Minimal skill that triggers when users ask about Claude Code features. Reminds
Claude to check ai_docs/ for fresh official documentation instead of relying on
potentially outdated training data.

**Content (≈40 tokens):**

```markdown
---
name: claude-code-documentation
description: Official Claude Code documentation in ai_docs/. Use when user
asks about plugins, skills, agents, hooks, commands, settings, or Claude Code
features.
---

# Claude Code Documentation

Official Claude Code documentation is in `ai_docs/`.

**Discovery**: `ls ai_docs/` to see available docs
**Usage**: Read relevant files for current task

Updated automatically by claude-docs-sync plugin.
```

**Design Rationale:**

- Activation trigger, not content provider
- Progressive disclosure: Claude discovers docs via `ls`, reads on-demand
- Minimal token cost (~40 tokens)
- High freedom: Claude decides which docs to read based on task

### 4. Script

**File:** `tools/claude_docs.py`

**Enhancements Required:**

Add `--format` flag with two output modes:

**Rich Format (default):**

- Colorful progress bars via rich library
- Performance tables and analytics
- Speed optimization tips
- Human-friendly presentation

**JSON Format:**

- Machine-readable structured output
- Compact, single-line result
- Used by hooks and Claude for parsing

**Output Schema (JSON):**

```json
{
  "status": "success",
  "downloaded": 11,
  "skipped": 2,
  "failed": 0,
  "duration_seconds": 3.2,
  "timestamp": "2025-10-29T14:32:11Z"
}
```

## Data Flow

### Interactive Mode Flow

```text
Session Start
    ↓
Hook checks cache timestamp
    ↓
Age > 7 days?
    ├─ No → Continue session
    └─ Yes → AskUserQuestion
        ├─ "Yes, update now"
        │   └─ /update-docs --format json
        │       └─ Show status: "✓ Docs updated"
        ├─ "No, skip"
        │   └─ Continue session
        └─ "Auto-update going forward"
            └─ Update hook config to mode: "auto"
            └─ /update-docs --format json
            └─ Show status: "✓ Docs updated, auto-mode enabled"
```

### Auto Mode Flow

```text
Session Start
    ↓
Hook checks cache timestamp
    ↓
Age > 7 days?
    ├─ No → Continue session
    └─ Yes → /update-docs --format json
        └─ Show status: "✓ Docs updated (11 pages, 3.2s)"
```

## Configuration

### Hook Config File

Users can manually edit hook config:

```json
{
  "mode": "interactive",
  "staleness_days": 7
}
```

**Settings:**

- `mode`: "interactive" | "auto"
- `staleness_days`: Integer (days before docs considered stale)

## User Experience

### First Install

1. User installs plugin
2. On first session start: Hook detects no cache
3. AskUserQuestion: "No Claude Code documentation found locally. Download now?"
4. User confirms → Downloads default pages
5. Session continues with fresh docs available

### Typical Usage (Interactive Mode)

1. User starts session 10 days after last update
2. Hook prompts: "Claude Code documentation is 10 days old. Update now?"
3. User selects "Yes, update now"
4. Brief status appears: "✓ Docs updated (11 pages, 3.2s)"
5. Session continues

### Typical Usage (Auto Mode)

1. User starts session 10 days after last update
2. Hook silently updates documentation
3. Brief status appears: "✓ Docs updated (11 pages, 3.2s)"
4. Session continues

### Manual Updates

User can always run manually:

```bash
/update-docs              # Update with defaults
/update-docs --all        # Download all pages
/update-docs --check      # See what's stale
/update-docs --interactive # Choose specific pages
```

## Implementation Notes

### Script Modifications

1. Add `--format` argument to `claude_docs.py`
2. Implement JSON output mode with structured schema
3. Keep rich output as default for backward compatibility
4. Ensure JSON output is single-line for easy parsing

### Hook Implementation

1. Check for `.download_cache.json` in auto-detected ai_docs directory
2. Parse cache file to get `downloaded_at` timestamp
3. Calculate age in days
4. If age > `staleness_days`, trigger appropriate action based on mode
5. Store hook config in hook JSON file for persistence

### Command Wrapper

1. Create markdown command file that shells out to script
2. Pass through all arguments to underlying Python script
3. Detect caller context (hook vs user) for format auto-detection
4. Return exit code and output to Claude

## Testing Strategy

1. **First install:** Verify prompt appears when no cache exists
2. **Staleness check:** Manually age cache file, verify prompt triggers
3. **Mode switching:** Test "Auto-update going forward" persists config
4. **Auto mode:** Verify silent updates work without prompts
5. **Manual command:** Test all flag combinations
6. **Output formats:** Validate JSON schema, verify rich output renders
   correctly

## Success Criteria

- Hook adds <100ms to session start time
- Documentation updates complete in <5 seconds for default pages
- JSON output parses correctly in all scenarios
- Mode switching persists across sessions
- Users can easily switch between interactive and auto modes
- Manual command works identically to standalone script usage

## Future Enhancements

- Configurable page lists (custom curated sets)
- Multiple documentation sources (not just Claude Code)
- Notification preferences (verbose, quiet, silent)
- Update scheduling (daily, weekly, monthly)
- Version tracking (compare doc versions, show what changed)
