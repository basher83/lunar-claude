# Scripts

This directory contains automation scripts for marketplace validation, documentation
processing, and development workflows.

## Marketplace and Plugin Management

**verify-structure.py** - Validates marketplace structure and plugin manifests against
Claude Code specifications. Checks marketplace.json schema, plugin.json manifests,
component placement (skills, commands, agents not in .claude-plugin/), YAML frontmatter
in markdown files, hook event types and script paths, MCP server configurations, and
custom component paths. Includes path traversal prevention and manifest conflict
detection between marketplace.json and plugin.json. Run with `--strict` flag to treat
warnings as errors in CI/CD pipelines.

**verify-pr.py** - Verifies pull request claims against actual implementation using
the Claude Agent SDK. Executes git commands and analyzes code changes to ensure PR
descriptions match reality. Supports PR numbers, branch names, and comparison refs
(e.g., `main...feature`). Includes input validation to prevent command injection.
Optionally uses `gh` CLI for PR metadata. Supports `--json` output for automation.
Requires local Claude authentication or `ANTHROPIC_API_KEY`.

## Documentation and Web Scraping

**firecrawl_scrape_url.py** - Generic single-URL scraper using Firecrawl. Fetches any
web page and converts to clean markdown. Supports full-page or main-content-only modes,
custom wait times for dynamic content, configurable output paths, and request timeouts.
Adds source attribution headers automatically. Requires `FIRECRAWL_API_KEY`.

**firecrawl_sdk_research.py** - Advanced web research tool using Firecrawl SDK.
Searches the web with optional category filtering (github, research, pdf), scrapes
content with combined API calls for efficiency, filters results by quality scoring,
and synthesizes into a single markdown document. Includes retry logic with exponential
backoff and quality indicators (⭐ for high-quality sources). Supports `--limit` for
result count and `--output` for custom paths. Requires `FIRECRAWL_API_KEY`.

**extract_docs_example.py** - Example script demonstrating documentation extraction
patterns using Jina Reader and repomix. Shows how to add YAML frontmatter metadata
and organize content by project/section. Not a CLI tool - contains hardcoded examples
for reference. Requires `curl` and optionally `repomix` for repo extraction.

**jina_reader_docs.py** - Downloads Claude Code documentation using direct HTTP calls to
Jina Reader API. Works without MCP setup, provides free tier access (or use API key for
higher limits), and handles retry logic with exponential backoff. Supports `--output-dir`,
`--api-key`, `--retries`, and `--format` (rich/json) options. Best for simple automation
and environments without MCP.

## Markdown Processing

**intelligent-markdown-lint.py** - Coordinates autonomous agents to fix markdown linting
errors using a 5-phase workflow: Discovery, Investigation, Workload Calculation, Fixing,
and Verification. Dispatches investigator and fixer subagents using the Claude Agent SDK.
Triages errors into simple (directly fixable) vs ambiguous (needs investigation) categories.
Supports `--dry-run` for analysis-only mode. Requires rumdl installed via cargo and agent
definitions in `.claude/agents/`. Requires local Claude authentication or `ANTHROPIC_API_KEY`.

**markdown_linter.py** - Full agentic markdown linting orchestrator using rumdl. Provides
custom MCP tools (rumdl_check, rumdl_fix, rumdl_statistics, rumdl_diff) plus investigator
and fixer subagents for intelligent error resolution. Categorizes errors as auto_fixable,
needs_investigation, or skip. Supports path, directory, or single file targeting. Optional
LangSmith tracing via environment variables. Requires rumdl installed via cargo.

**markdown_formatter.py** - Fixes missing language tags and spacing issues in markdown
files. Detects programming languages (json, python, javascript, bash, sql) in unlabeled
code fences and adds appropriate identifiers. Works as a Claude Code hook (stdin JSON)
or standalone CLI tool with multiple file support. Use `--blocking` to exit with code 2
when changes are made (for hook feedback).

**rumdl-parser.py** - Parses rumdl linting output into structured JSON. Identifies YAML
frontmatter, categorizes errors (MD013, MD036, MD025, MD041, MD052), and optionally
distributes work across multiple subagents with `--distribute N`. Use `--summary` for
counts only without detailed error info. Reads from stdin (pipe from rumdl).

**cleanup_bash_research.py** - Specialized cleanup script for the bash-best-practices
research document. Removes GitHub UI clutter, navigation elements, redundant metadata,
permalinks, and HTML artifacts while preserving technical content. Hardcoded to process
`docs/research/bash/bash-best-practices-research.md` - not a general-purpose CLI tool.

## Development Tools

**note_smith.py** - Interactive research assistant demonstrating Claude Agent SDK
features. Provides custom MCP tools (`save_note`, `find_note`) for saving and searching
notes, WebFetch integration for URL summarization, and hook-based command safety.
Supports interactive commands: `/summarize <url>`, `/note <text>`, `/find <pattern>`,
`/help`, `/exit`. CLI options: `--model` (sonnet/opus/haiku), `--notes-dir` for custom
storage location. Optional LangSmith tracing via environment variables. Requires local
Claude authentication or `ANTHROPIC_API_KEY`.

**bash_command_validator_example.py** - PreToolUse hook example that validates bash
commands before execution. Suggests better alternatives like replacing `grep` with `rg`
(ripgrep) and `find -name` with `rg --files` for improved performance. Exit code 2
blocks tool call and shows feedback to Claude. Includes hook configuration JSON example
in docstring.

**test_cache_precision.py** - Tests cache lookup precision with tag-based matching.
Simulates cache lookups by extracting keywords from test queries, matching against
cache entry tags, and calculating precision/recall/F1 metrics. Includes synonym
normalization (k8s→kubernetes, etc.). Supports `--verbose` for per-query details and
`--json` for automation output. Returns Go/No-Go decision based on 70% precision
threshold (exit code 1 on FAIL).

**validate_research_schema.py** - Validates research report JSON files against the
research pipeline schema. Uses jsonschema for Draft-7 validation with format checking
(uri, date-time). Validates allowed sources: github, tavily, deepwiki, exa. Run with
`--test` to validate the schema itself against sample data. Comprehensive error handling
for JSON parsing, permissions, and encoding issues.

## Usage Patterns

Most scripts use inline script dependencies (PEP 723) and run with `uv`:

```bash
./scripts/verify-structure.py
./scripts/verify-pr.py 7
./scripts/intelligent-markdown-lint.py --dry-run
```

Scripts requiring external services check for credentials (API keys or local authentication) and exit with clear error messages when missing.
