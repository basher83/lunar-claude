# Claude Docs Sync Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement
this plan task-by-task.

**Goal:** Build a plugin that automatically maintains fresh Claude Code
documentation locally with intelligent staleness detection and multiple update
modes.

**Architecture:** SessionStart hook checks cache age and prompts user via
AskUserQuestion (interactive mode) or auto-updates (auto mode). Slash command
provides manual control. Minimal skill triggers doc awareness. Enhanced Python
script supports JSON/rich output formats.

**Tech Stack:** Python 3.11+ (PEP 723), httpx, rich, typer, Claude Code plugin
system (hooks, commands, skills)

---

## Task 1: Create Plugin Directory Structure

**Files:**

- Create: `plugins/meta/claude-docs-sync/.claude-plugin/plugin.json`
- Create: `plugins/meta/claude-docs-sync/README.md`

**Step 1: Create plugin directory**

```bash
mkdir -p plugins/meta/claude-docs-sync/.claude-plugin
mkdir -p plugins/meta/claude-docs-sync/skills/claude-code-documentation
mkdir -p plugins/meta/claude-docs-sync/commands
mkdir -p plugins/meta/claude-docs-sync/hooks
mkdir -p plugins/meta/claude-docs-sync/tools
```

**Step 2: Create plugin.json**

Create: `plugins/meta/claude-docs-sync/.claude-plugin/plugin.json`

```json
{
  "name": "claude-docs-sync",
  "version": "0.1.0",
  "description": "Automatically sync Claude Code documentation for fresh AI context",
  "author": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "keywords": ["documentation", "sync", "meta", "automation"],
  "license": "MIT"
}
```

**Step 3: Create README.md**

Create: `plugins/meta/claude-docs-sync/README.md`

```markdown
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

```
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
```

**Step 4: Commit plugin structure**

```bash
git add plugins/meta/claude-docs-sync/
git commit -m "feat(claude-docs-sync): create plugin structure and README"
```

---

## Task 2: Move and Enhance Script with JSON Output

**Files:**

- Move: `plugins/meta/claude-dev-sandbox/scripts/claude_docs.py` →
  `plugins/meta/claude-docs-sync/tools/claude_docs.py`
- Modify: `plugins/meta/claude-docs-sync/tools/claude_docs.py`

**Step 1: Copy script to new location**

```bash
cp plugins/meta/claude-dev-sandbox/scripts/claude_docs.py \
   plugins/meta/claude-docs-sync/tools/claude_docs.py
```

**Step 2: Add JSON output format support**

Modify: `plugins/meta/claude-docs-sync/tools/claude_docs.py`

Add after the imports section (around line 35):

```python
@dataclass
class DownloadResult:
    """Result of documentation download operation."""
    status: str  # "success" or "error"
    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    duration_seconds: float = 0.0
    timestamp: str = ""
```

Add format parameter to main function (around line 357):

```python
def main(
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Directory to save downloaded documentation files (default: auto-detect or create ai_docs/)",
        dir_okay=True,
        file_okay=False,
    ),
    retries: int = typer.Option(
        3,
        "--retries", "-r",
        help="Maximum number of retry attempts per page",
        min=1,
        max=10,
    ),
    all_pages: bool = typer.Option(
        False,
        "--all",
        help="Download all 70+ pages from the docs map",
    ),
    check_only: bool = typer.Option(
        False,
        "--check",
        help="Only check for updates, don't download (dry-run)",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive", "-i",
        help="Interactively select which pages to download",
    ),
    format: str = typer.Option(
        "rich",
        "--format",
        help="Output format: 'rich' for human-readable or 'json' for machine-readable",
    ),
) -> None:
```

Add JSON output logic at the end of main (replace summary table section):

```python
    # Save updated cache
    save_cache(cache_file, cache)

    total_time = time.time() - start_time

    # Prepare result data
    result = DownloadResult(
        status="success" if failed_count == 0 else "error",
        downloaded=success_count,
        skipped=skipped_count,
        failed=failed_count,
        duration_seconds=round(total_time, 2),
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )

    # Output based on format
    if format == "json":
        # Machine-readable JSON output (single line)
        import json
        output = {
            "status": result.status,
            "downloaded": result.downloaded,
            "skipped": result.skipped,
            "failed": result.failed,
            "duration_seconds": result.duration_seconds,
            "timestamp": result.timestamp
        }
        print(json.dumps(output))
    else:
        # Rich format (existing table output)
        console.print()
        summary_title = "Update Check Summary" if check_only else "Download Summary"
        table = Table(title=summary_title,
                      show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Pages", str(len(pages)))

        if check_only:
            table.add_row("↻ Updates Available", f"[yellow]{success_count}[/yellow]")
        else:
            table.add_row("✓ Downloaded", f"[green]{success_count}[/green]")

        if skipped_count > 0:
            table.add_row("⊙ Up-to-date", f"[dim]{skipped_count}[/dim]")
        if failed_count > 0:
            table.add_row("✗ Failed", f"[red]{failed_count}[/red]")

        table.add_row("Total Size", f"{total_bytes / 1024:.1f} KB")
        table.add_row("Total Time", f"{total_time:.2f}s")

        if download_times:
            avg_time = sum(download_times) / len(download_times)
            table.add_row("Avg Time/Page", f"{avg_time:.2f}s")
            table.add_row("Overall Speed",
                          f"{(total_bytes / 1024) / total_time:.1f} KB/s")

        console.print(table)

        # Performance analysis (rich format only)
        if not check_only and download_times and len(download_times) > 1:
            total_download_time = sum(download_times)
            console.print()
            console.print("[bold]Performance Analysis:[/bold]")
            console.print(
                f"  • Sequential download time: {total_download_time:.2f}s")
            console.print(f"  • Actual wall clock time: {total_time:.2f}s")
            console.print(f"  • Overhead: {total_time - total_download_time:.2f}s")

            # Estimate parallel speedup
            if avg_time > 0:
                # longest download + overhead
                estimated_parallel_time = max(download_times) + 1.0
                potential_speedup = total_time / estimated_parallel_time
                if potential_speedup > 1.5:
                    console.print(
                        f"\n[yellow]💡 Tip:[/yellow] Parallel downloads could reduce time to ~{estimated_parallel_time:.1f}s "
                        f"(~{potential_speedup:.1f}x faster)"
                    )

    # Exit with error if any downloads failed
    if failed_count > 0:
        raise typer.Exit(code=1)
```

**Step 3: Test JSON output format**

```bash
cd plugins/meta/claude-docs-sync
./tools/claude_docs.py --format json --check
```

Expected output (single-line JSON):

```json
{"status":"success","downloaded":0,"skipped":14,"failed":0,"duration_seconds":2.5,"timestamp":"2025-10-29T22:30:15Z"}
```

**Step 4: Test rich output format (default)**

```bash
./tools/claude_docs.py --format rich --check
```

Expected: Colorful table output with performance analysis

**Step 5: Commit script enhancements**

```bash
git add plugins/meta/claude-docs-sync/tools/claude_docs.py
git commit -m "feat(claude-docs-sync): add JSON output format to script"
```

---

## Task 3: Create Minimal Skill

**Files:**

- Create: `plugins/meta/claude-docs-sync/skills/claude-code-documentation/SKILL.md`

**Step 1: Create skill file**

Create:
`plugins/meta/claude-docs-sync/skills/claude-code-documentation/SKILL.md`

```markdown
---
name: claude-code-documentation
description: Official Claude Code documentation in ai_docs/. Use when user asks
about plugins, skills, agents, hooks, commands, settings, or Claude Code features.
---

# Claude Code Documentation

Official Claude Code documentation is in `ai_docs/`.

**Discovery**: `ls ai_docs/` to see available docs
**Usage**: Read relevant files for current task

Updated automatically by claude-docs-sync plugin.
```

**Step 2: Verify skill structure**

```bash
cd plugins/meta/claude-docs-sync
head -20 skills/claude-code-documentation/SKILL.md
```

Expected: Valid YAML frontmatter and markdown content

**Step 3: Commit skill**

```bash
git add plugins/meta/claude-docs-sync/skills/
git commit -m "feat(claude-docs-sync): add minimal documentation awareness skill"
```

---

## Task 4: Create Slash Command

**Files:**

- Create: `plugins/meta/claude-docs-sync/commands/update-docs.md`

**Step 1: Create command file**

Create: `plugins/meta/claude-docs-sync/commands/update-docs.md`

```markdown
---
name: update-docs
description: Update Claude Code documentation from docs.claude.com
---

# Update Documentation Command

Downloads fresh Claude Code documentation to ai_docs/.

## Usage

```bash
/update-docs              # Update default pages
/update-docs --all        # Download all 70+ pages
/update-docs --check      # Check what needs updating (dry-run)
/update-docs --interactive # Choose specific pages
```

## Implementation

Executes the claude_docs.py script with appropriate format:

- **User invocation**: Rich format (colorful tables, performance analysis)
- **Hook invocation**: JSON format (machine-readable, compact)

The script auto-detects context and selects format accordingly.
```

**Step 2: Verify command structure**

```bash
head -10 plugins/meta/claude-docs-sync/commands/update-docs.md
```

Expected: Valid YAML frontmatter

**Step 3: Commit command**

```bash
git add plugins/meta/claude-docs-sync/commands/
git commit -m "feat(claude-docs-sync): add update-docs slash command"
```

---

## Task 5: Create SessionStart Hook

**Files:**

- Create: `plugins/meta/claude-docs-sync/hooks/check-docs-staleness.json`

**Step 1: Create hook configuration**

Create: `plugins/meta/claude-docs-sync/hooks/check-docs-staleness.json`

```json
{
  "name": "check-docs-staleness",
  "description": "Check if Claude Code documentation is stale and prompt for updates",
  "trigger": "SessionStart",
  "enabled": true,
  "config": {
    "mode": "interactive",
    "staleness_days": 7
  },
  "script": "#!/usr/bin/env bash\nset -euo pipefail\n\n# Load config\nMODE=$(jq -r '.config.mode // \"interactive\"' < \"$HOOK_CONFIG_FILE\")\nSTALENESS_DAYS=$(jq -r '.config.staleness_days // 7' < \"$HOOK_CONFIG_FILE\")\n\n# Find ai_docs directory (auto-detect like script does)\nSCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\nPLUGIN_DIR=\"$(dirname \"$SCRIPT_DIR\")\"\nAI_DOCS_DIR=\"$PLUGIN_DIR/ai_docs\"\n\n# Check if cache file exists\nCACHE_FILE=\"$AI_DOCS_DIR/.download_cache.json\"\n\nif [ ! -f \"$CACHE_FILE\" ]; then\n  # No cache exists - docs never downloaded\n  if [ \"$MODE\" = \"auto\" ]; then\n    # Auto mode: download silently\n    \"$PLUGIN_DIR/tools/claude_docs.py\" --format json\n  else\n    # Interactive mode: ask user\n    # Use AskUserQuestion tool to prompt\n    cat <<EOF\n{\n  \"tool\": \"AskUserQuestion\",\n  \"params\": {\n    \"questions\": [{\n      \"question\": \"No Claude Code documentation found locally. Download now?\",\n      \"header\": \"Docs Setup\",\n      \"multiSelect\": false,\n      \"options\": [\n        {\n          \"label\": \"Yes, download now\",\n          \"description\": \"Download default documentation pages (~14 pages, ~3-5 seconds)\"\n        },\n        {\n          \"label\": \"No, skip\",\n          \"description\": \"Continue without updating documentation\"\n        },\n        {\n          \"label\": \"Auto-update going forward\",\n          \"description\": \"Download now and enable automatic updates in the future\"\n        }\n      ]\n    }]\n  }\n}\nEOF\n    \n    # Wait for user response (injected by hook system)\n    RESPONSE=\"${HOOK_USER_RESPONSE:-}\"\n    \n    if [[ \"$RESPONSE\" == *\"Yes\"* ]]; then\n      \"$PLUGIN_DIR/tools/claude_docs.py\" --format json\n    elif [[ \"$RESPONSE\" == *\"Auto-update\"* ]]; then\n      # Enable auto mode\n      jq '.config.mode = \"auto\"' < \"$HOOK_CONFIG_FILE\" > \"${HOOK_CONFIG_FILE}.tmp\"\n      mv \"${HOOK_CONFIG_FILE}.tmp\" \"$HOOK_CONFIG_FILE\"\n      \"$PLUGIN_DIR/tools/claude_docs.py\" --format json\n    fi\n  fi\n  exit 0\nfi\n\n# Cache exists - check staleness\nLAST_UPDATE=$(jq -r '[.[] | .downloaded_at] | max' < \"$CACHE_FILE\")\nCURRENT_TIME=$(date +%s)\nAGE_SECONDS=$((CURRENT_TIME - ${LAST_UPDATE:-0}))\nAGE_DAYS=$((AGE_SECONDS / 86400))\n\nif [ \"$AGE_DAYS\" -lt \"$STALENESS_DAYS\" ]; then\n  # Docs are fresh\n  exit 0\nfi\n\n# Docs are stale\nif [ \"$MODE\" = \"auto\" ]; then\n  # Auto mode: update silently\n  RESULT=$(\"$PLUGIN_DIR/tools/claude_docs.py\" --format json)\n  # Parse JSON result and show brief status\n  DOWNLOADED=$(echo \"$RESULT\" | jq -r '.downloaded')\n  DURATION=$(echo \"$RESULT\" | jq -r '.duration_seconds')\n  echo \"✓ Docs updated ($DOWNLOADED pages, ${DURATION}s)\"\nelse\n  # Interactive mode: ask user\n  cat <<EOF\n{\n  \"tool\": \"AskUserQuestion\",\n  \"params\": {\n    \"questions\": [{\n      \"question\": \"Claude Code documentation is $AGE_DAYS days old. Update now?\",\n      \"header\": \"Docs Stale\",\n      \"multiSelect\": false,\n      \"options\": [\n        {\n          \"label\": \"Yes, update now\",\n          \"description\": \"Download latest documentation (~3-5 seconds)\"\n        },\n        {\n          \"label\": \"No, skip\",\n          \"description\": \"Continue with current documentation\"\n        },\n        {\n          \"label\": \"Auto-update going forward\",\n          \"description\": \"Update now and enable automatic updates\"\n        }\n      ]\n    }]\n  }\n}\nEOF\n  \n  # Wait for user response\n  RESPONSE=\"${HOOK_USER_RESPONSE:-}\"\n  \n  if [[ \"$RESPONSE\" == *\"Yes\"* ]]; then\n    RESULT=$(\"$PLUGIN_DIR/tools/claude_docs.py\" --format json)\n    DOWNLOADED=$(echo \"$RESULT\" | jq -r '.downloaded')\n    DURATION=$(echo \"$RESULT\" | jq -r '.duration_seconds')\n    echo \"✓ Docs updated ($DOWNLOADED pages, ${DURATION}s)\"\n  elif [[ \"$RESPONSE\" == *\"Auto-update\"* ]]; then\n    # Enable auto mode\n    jq '.config.mode = \"auto\"' < \"$HOOK_CONFIG_FILE\" > \"${HOOK_CONFIG_FILE}.tmp\"\n    mv \"${HOOK_CONFIG_FILE}.tmp\" \"$HOOK_CONFIG_FILE\"\n    RESULT=$(\"$PLUGIN_DIR/tools/claude_docs.py\" --format json)\n    DOWNLOADED=$(echo \"$RESULT\" | jq -r '.downloaded')\n    DURATION=$(echo \"$RESULT\" | jq -r '.duration_seconds')\n    echo \"✓ Docs updated, auto-mode enabled ($DOWNLOADED pages, ${DURATION}s)\"\n  fi\nfi\n"
}
```

**Step 2: Verify hook JSON is valid**

```bash
jq . < plugins/meta/claude-docs-sync/hooks/check-docs-staleness.json
```

Expected: Valid JSON output

**Step 3: Extract and verify script syntax**

```bash
cd plugins/meta/claude-docs-sync
jq -r '.script' < hooks/check-docs-staleness.json > /tmp/test-hook.sh
bash -n /tmp/test-hook.sh
```

Expected: No syntax errors

**Step 4: Commit hook**

```bash
git add plugins/meta/claude-docs-sync/hooks/
git commit -m "feat(claude-docs-sync): add SessionStart staleness check hook"
```

---

## Task 6: Update Marketplace Registry

**Files:**

- Modify: `.claude-plugin/marketplace.json`

**Step 1: Add plugin to marketplace registry**

Modify: `.claude-plugin/marketplace.json`

Add to `plugins` array:

```json
    {
      "name": "claude-docs-sync",
      "source": "./plugins/meta/claude-docs-sync",
      "description": "Automatically sync Claude Code documentation for fresh AI context",
      "version": "0.1.0",
      "category": "meta",
      "keywords": ["documentation", "sync", "meta", "automation", "hooks"],
      "author": {
        "name": "basher83"
      }
    }
```

**Step 2: Verify JSON is valid**

```bash
jq . < .claude-plugin/marketplace.json
```

Expected: Valid JSON output with new plugin entry

**Step 3: Verify plugin structure**

```bash
./scripts/verify-structure.py
```

Expected: All validation checks pass

**Step 4: Commit marketplace update**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(marketplace): add claude-docs-sync plugin to registry"
```

---

## Task 7: End-to-End Testing

**Files:**

- Test: Full plugin installation and functionality

**Step 1: Test plugin installation in main repo**

```bash
cd /Users/basher8383/dev/personal/lunar-claude
/plugin uninstall claude-docs-sync@lunar-claude
/plugin install claude-docs-sync@lunar-claude
```

Expected: Plugin installs successfully

**Step 2: Test slash command**

```bash
/update-docs --check
```

Expected: Rich format output showing what needs updating

**Step 3: Test JSON format**

```bash
cd plugins/meta/claude-docs-sync
./tools/claude_docs.py --format json --check
```

Expected: Single-line JSON output

**Step 4: Test skill activation**

Ask Claude: "How do I create a new hook for Claude Code?"

Expected: Skill activates, Claude runs `ls ai_docs/`, reads relevant docs

**Step 5: Test hook manually (simulate SessionStart)**

```bash
cd plugins/meta/claude-docs-sync
bash -c "$(jq -r '.script' < hooks/check-docs-staleness.json)"
```

Expected: If docs >7 days old, sees AskUserQuestion prompt

**Step 6: Create final commit**

```bash
git status
```

If any uncommitted changes, commit them:

```bash
git add -A
git commit -m "feat(claude-docs-sync): complete plugin implementation"
```

**Step 7: Verify commit history**

```bash
git log --oneline feature/claude-docs-sync-plugin
```

Expected: Clean commit history with descriptive messages

---

## Completion Checklist

- [ ] Plugin structure created with proper plugin.json
- [ ] Script enhanced with JSON output format
- [ ] Minimal skill created and validated
- [ ] Slash command created
- [ ] SessionStart hook created and tested
- [ ] Marketplace registry updated
- [ ] End-to-end testing completed
- [ ] All commits follow conventional commit format
- [ ] Ready for PR or merge

**Next Steps:**

Use @superpowers:finishing-a-development-branch to:

1. Review implementation against design
2. Choose merge strategy (merge, PR, or cleanup)
3. Clean up worktree
