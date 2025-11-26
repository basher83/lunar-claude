# Scripts

This directory contains automation scripts for marketplace validation, documentation
processing, and development workflows.

## Marketplace and Plugin Management

**verify-structure.py** - Validates marketplace structure and plugin manifests against
Claude Code specifications. Checks marketplace.json syntax, plugin component placement,
frontmatter requirements, and hook configurations. Run with `--strict` flag to treat
warnings as errors in CI/CD pipelines.

**verify-pr.py** - Verifies pull request claims against actual implementation using
the Claude Agent SDK. Executes git commands and analyzes code changes to ensure PR
descriptions match reality. Requires `ANTHROPIC_API_KEY` and `gh` CLI.

## Documentation and Web Scraping

**firecrawl_scrape_url.py** - Generic single-URL scraper using Firecrawl. Fetches any
web page and converts to clean markdown. Supports full-page or main-content-only modes,
custom wait times for dynamic content, and configurable output paths. Adds source
attribution headers automatically. Requires `FIRECRAWL_API_KEY`.

**firecrawl_sdk_research.py** - Advanced web research tool using Firecrawl SDK.
Searches the web with optional category filtering (github, research, pdf), scrapes
content with combined API calls for efficiency, filters results by quality scoring,
and synthesizes into a single markdown document. Includes retry logic with exponential
backoff and quality indicators (⭐ for high-quality sources). Requires
`FIRECRAWL_API_KEY`.

**extract_docs_example.py** - Extracts and structures documentation for AI consumption
using Jina Reader. Adds metadata headers and organizes content by project and section.

**jina_reader_docs.py** - Downloads Claude Code documentation using direct HTTP calls to
Jina Reader API. Works without MCP setup, provides free tier access, and handles retry
logic. Best for simple automation and environments without MCP.

## Markdown Processing

**intelligent-markdown-lint.py** - Coordinates autonomous agents to fix markdown linting
errors. Dispatches investigator and fixer subagents using the Claude Agent SDK to
analyze and correct markdown issues.

**markdown_linter.py** - Standalone markdown linter using rumdl with custom MCP tools.
Provides rumdl_check, rumdl_fix, rumdl_statistics, and rumdl_diff tools for
intelligent linting workflows. Requires rumdl installed via cargo.

**markdown_formatter.py** - Fixes missing language tags and spacing issues in markdown
files. Detects programming languages in unlabeled code fences and adds appropriate
identifiers. Works as a Claude Code hook or standalone CLI tool.

**rumdl-parser.py** - Parses rumdl linting output into structured JSON. Identifies YAML
frontmatter, categorizes errors, and optionally distributes work across multiple
subagents.

**cleanup_bash_research.py** - Removes GitHub UI clutter and formatting artifacts from
scraped markdown files. Cleans navigation elements, redundant metadata, permalinks,
and HTML artifacts while preserving technical content.

**format_skill_research.py** - Generic markdown formatter for skill research files.
Removes GitHub UI elements and applies basic markdown formatting rules. Processes
all markdown files in a directory recursively.

## Development Tools

**skill-auditor.py** - Audits skills using deterministic Python extraction and Claude
analysis. Extracts metrics (quoted phrases, domain indicators, line count) and
validates against Claude Code skill specifications. Requires skill directory path.

**note_smith.py** - Interactive research assistant demonstrating Claude Agent SDK
features. Provides custom MCP tools for saving and searching notes, WebFetch integration
for URL summarization, and hook-based command safety.

**bash_command_validator_example.py** - PreToolUse hook example that validates bash
commands before execution. Suggests better alternatives like replacing `grep` with `rg`
(ripgrep) for improved performance.

## Usage Patterns

Most scripts use inline script dependencies (PEP 723) and run with `uv`:

```bash
./scripts/verify-structure.py
./scripts/verify-pr.py 7
./scripts/intelligent-markdown-lint.py --dry-run
```

Scripts requiring API keys check environment variables and exit with clear error messages when credentials are missing.
