# Claude Documentation Downloader

Downloads Claude Code documentation from docs.claude.com and saves it locally for offline reference and AI context enhancement.

## Features

The script fetches markdown documentation with intelligent caching. It checks ETag and Last-Modified headers to skip unchanged files, retries failed downloads with exponential backoff, and reports download statistics with performance analysis.

## Requirements

The script uses PEP 723 inline dependencies. Run it with `uv`:

```bash
uv run ./claude_docs.py
```

Dependencies (auto-installed):

- httpx ≥0.27.0
- rich ≥13.0.0
- typer ≥0.12.0

## Usage

### Quick Start

Download default pages to auto-detected ai_docs directory:

```bash
./claude_docs.py
```

### Custom Output Directory

```bash
./claude_docs.py --output-dir ./my-docs
```

### Download All Pages

Fetch all 70+ pages from the documentation map:

```bash
./claude_docs.py --all
```

### Interactive Selection

Choose specific pages interactively:

```bash
./claude_docs.py --interactive
```

### Check for Updates

See which pages need updating without downloading:

```bash
./claude_docs.py --check
```

### Configure Retries

Set maximum retry attempts per page:

```bash
./claude_docs.py --retries 5
```

## Output Location

The script auto-detects the output directory:

1. Uses `--output-dir` if provided
2. Creates `ai_docs/` relative to script location
3. Flattens nested paths: `agent-skills/overview` → `agent-skills-overview.md`

All files save directly to ai_docs/ without subdirectories.

## Caching System

The script maintains `.download_cache.json` in the output directory. This cache stores ETags, modification times, and file sizes. On subsequent runs, the script checks headers before downloading, skipping unchanged files.

## Default Pages

The script downloads these pages by default:

**Claude Code:**

- sub-agents
- plugins
- skills
- output-styles
- hooks-guide
- plugin-marketplaces
- settings
- statusline
- slash-commands
- hooks
- plugins-reference

**Agent Skills API:**

- agent-skills/overview
- agent-skills/quickstart
- agent-skills/best-practices

## Performance

The script downloads pages sequentially with retry logic. Performance metrics include:

- Download time per page
- Total transfer size
- Average speed
- Overhead analysis
- Parallel speedup estimates

Typical download time: 2-5 seconds for default pages (with cache).

## Exit Codes

- 0: Success
- 1: One or more downloads failed

## Examples

Download default pages with retry limit:

```bash
./claude_docs.py --retries 3
```

Check for updates without downloading:

```bash
./claude_docs.py --check
```

Download all pages to custom directory:

```bash
./claude_docs.py --all --output-dir ~/docs/claude
```

Interactive selection with custom output:

```bash
./claude_docs.py -i -o ./documentation
```
