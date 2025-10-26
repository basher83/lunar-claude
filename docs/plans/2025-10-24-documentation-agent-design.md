# Documentation Maintenance Agent Design

**Date:** 2025-10-24
**Status:** Design
**Author:** Brainstorming session with Claude Code

## Problem Statement

Managing documentation across 10+ repositories (lunar-claude marketplace, homelab infrastructure, DevOps tools) presents four challenges:

1. **Volume**: Manual maintenance across multiple repos consumes excessive time
2. **Quality**: Inconsistent formatting, broken links, and grammar issues degrade documentation
3. **Gaps**: Missing sections remain unidentified without systematic analysis
4. **Staleness**: Documentation drifts from codebase as APIs change, versions update, and examples become outdated

Current tools (markdownlint-cli2, pre-commit hooks) catch syntax errors but cannot detect semantic problems like code-docs mismatches or missing documentation.

## Solution: Layered Analysis Pipeline

The system uses three independent analysis layers that can run separately or in sequence:

**Layer 1: Fast Checks** - Executes existing tools (markdownlint-cli2, basic link validation) without AI inference. Runs in seconds. Calls existing mise tasks to avoid duplication.

**Layer 2: AI-Powered Analysis** - Claude Sonnet analyzes grammar, writing quality, and identifies documentation gaps. Uses Claude Agent SDK with specialized prompts. Runs in 1-3 minutes per repo.

**Layer 3: Deep Staleness Detection** - Parses code (Python, Terraform, Ansible), extracts API signatures, compares with documentation. Validates code examples by execution. Tracks version references against git tags. Runs in 5-10 minutes for complex repos.

A **Multi-Repo Coordinator** sits above these layers, reading a configuration file listing repositories. It processes repos in parallel and aggregates results into unified reports.

The system operates in two modes: CLI for local ad-hoc runs (`doc-agent scan --quick` or `doc-agent scan --deep`), and Python service for scheduled automation (cron or GitHub Actions).

## Architecture

### Components

**CLI Entry Point** (`doc-agent` command)

Python executable using Click or Typer for argument parsing. Commands: `scan`, `report`, `config`, `cache-clear`. Flags: `--layer [1|2|3|all]`, `--repo <path>`, `--incremental`, `--output [terminal|json|markdown]`. Reads configuration from `~/.config/doc-agent/config.yaml` or repo-local `.doc-agent.yaml`.

**Configuration Manager**

YAML-based configuration lists repos, per-repo settings, and analysis preferences. Supports inheritance: global defaults → plugin-category defaults → repo-specific overrides. Terraform repos might skip grammar checks but emphasize code-docs matching. Stores cache metadata (last run timestamp, file checksums for incremental processing).

**Layer 1 Runner**

Subprocess executor calls existing tools: `mise run markdown-lint`, `mise run markdown-fix`. Parses tool outputs (markdownlint JSON format) into unified result structure. Falls back gracefully if mise task doesn't exist in a repo.

**Layer 2 Agent** (Claude SDK)

Single Claude agent with context about repo type (homelab, infrastructure, devops). Four analysis passes: grammar/clarity, structure consistency, completeness gaps, audience appropriateness. Generates structured JSON output with severity levels (critical, warning, info).

**Layer 3 Analyzers** (Specialized parsers)

- **Python**: AST parser extracts function signatures, compares with doc references
- **Terraform**: HCL parser for resource/variable definitions vs. documentation
- **Ansible**: YAML parser for role/playbook structures
- **Code example validator**: Extracts fenced code blocks, attempts execution in isolated environment
- **Version tracker**: Regex patterns match version references, compare against git tags/releases

**Multi-Repo Coordinator**

Reads repo list from config. Spawns parallel workers (using Python multiprocessing or asyncio). Aggregates results into dashboard format.

**Report Generator**

Multiple output formats: terminal (rich/colorized), JSON (for automation), Markdown (for commit/PR). Per-repo reports plus cross-repo summary. Action items prioritized by severity.

### Data Flow

**Local Ad-Hoc Execution:**

1. Developer runs `doc-agent scan --layer 1 --repo /path/to/repo`
2. Configuration Manager loads repo-specific settings
3. Layer 1 Runner checks cache: any files unchanged since last run?
4. For changed files: executes mise tasks, collects results
5. Results formatted to terminal with color coding
6. Cache updated with checksums and timestamps

**Deep Analysis:**

1. Developer runs `doc-agent scan --deep --repo /path/to/repo` (layers 1-3)
2. Layer 1 runs first, identifies files with issues
3. Layer 2 receives Layer 1 results as context: "These files already have linting errors, focus on content quality"
4. Layer 3 receives both prior layers: "These docs mention `deploy_vm()` function - verify it exists in codebase"
5. Each layer enriches analysis with its findings
6. Final report shows issues grouped by file, with layer attribution

**Multi-Repo Scheduled:**

1. Cron/GitHub Action triggers `doc-agent scan --all-repos --output markdown`
2. Coordinator reads `~/.config/doc-agent/config.yaml` with 10+ repo paths
3. Spawns parallel workers (4-6 concurrent repos)
4. Each worker runs layers 1-2 (fast) on its repo
5. Layer 3 (slow) runs only if Layer 2 detects staleness warnings
6. Aggregated report written to markdown, optionally creates GitHub issues for critical findings

**Incremental Mode:**

Git-aware diffing identifies changed `.md` files since last commit or last scan. Only analyzes those files. Cross-file references (links) still validated across entire repo.

## Layer 3: Deep Staleness Detection

### Code-Docs Mismatch Detection

**Python**: AST parser walks `**/*.py` files, extracts function/class signatures. Builds index: `{"deploy_vm": {"params": ["name", "cpu", "memory"], "file": "vm.py:42"}}`. Searches docs for function references (backtick code spans, code blocks). Reports: functions documented but not in code, functions in code but undocumented, parameter mismatches.

**Terraform**: HCL parser extracts `resource`, `variable`, `output` blocks. Cross-references with documentation mentioning resource types. Validates variable descriptions match actual variable definitions. Checks if outputs are documented.

**Ansible**: YAML parser extracts role names, playbook tasks, variables. Validates role documentation against actual role structure. Checks playbook documentation mentions correct task names.

### Version Reference Tracking

Regex patterns scan docs for version strings: `v1.2.3`, `version 2.0`, `Python 3.11`. Git tag analyzer fetches latest tags from each repo. Dependency file parser reads `requirements.txt`, `mise.toml`, `package.json`. Reports version mismatches: "Docs say Python 3.11, mise.toml specifies 3.13".

### Code Example Validation

Extracts fenced code blocks tagged with language (` ```python `, ` ```bash `). Python examples: attempts AST parse (syntax validation). Bash examples: runs through shellcheck. For examples with file paths: validates the paths exist in repo. Optionally: executes examples in sandboxed environment (uv run for Python).

### Dead Internal Reference Detection

Extracts all markdown links: `[text](path)`, `[text](url)`. Internal links (relative paths): validates file exists at path. Anchor links (`#section`): validates heading exists in target file. Cross-doc references: tracks if referenced file moved/deleted since last scan. Reports: broken links, suggestions for updated paths based on git history.

## Configuration

### Global Configuration

`~/.config/doc-agent/config.yaml`:

```yaml
repos:
  - path: /workspaces/lunar-claude
    category: marketplace
    layers: [1, 2, 3]
  - path: ~/homelab/terraform-proxmox
    category: infrastructure
    layers: [1, 3]  # Skip grammar, focus on code-docs matching
  - path: ~/homelab/ansible-k8s
    category: infrastructure

defaults:
  output_format: terminal
  incremental: true
  parallel_workers: 4

layer_1:
  use_mise_tasks: true
  fallback_commands:
    markdown_lint: "markdownlint-cli2 **/*.md"

layer_2:
  model: "claude-sonnet-4.5"
  focus_areas: [grammar, completeness, structure]

layer_3:
  code_languages: [python, terraform, ansible, bash]
  validate_examples: true
  version_tracking: true
```

### Per-Repo Configuration

`.doc-agent.yaml` in repo root:

```yaml
# lunar-claude specific settings
layer_2:
  focus_areas: [completeness, structure]  # Skip grammar for plugin docs

layer_3:
  skip_code_matching: true  # No code to match, pure documentation repo
  version_tracking: true    # But track version refs

custom_patterns:
  plugin_version: "plugins/.*/\\.claude-plugin/plugin\\.json"
```

### Integration with Existing Tools

Layer 1 calls existing mise tasks. First tries: `mise run markdown-lint` in repo directory. Parses output: markdownlint-cli2 JSON format. If mise task doesn't exist: falls back to direct markdownlint-cli2 command. Also calls: `mise run infisical-scan` for secret detection.

The agent avoids duplicating work. If Layer 1 already caught markdown syntax error, Layer 2 doesn't re-report it. Results are deduplicated: same issue from multiple layers shows only once. Attribution shows which layer detected each issue.

Pre-commit hooks continue to block bad commits. Agent runs post-commit or on-demand for deeper analysis. Agent can suggest additions to `.pre-commit-config.yaml` based on findings.

## Output Formats

### Terminal Output

Uses `rich` library for colorized, structured output. Real-time progress: "Layer 1 complete (2.3s), starting Layer 2...". Issue summary table: grouped by file, severity color-coded (red=critical, yellow=warning, blue=info). Actionable items: "Run `doc-agent fix --auto` to apply 12 auto-fixable issues". Layer attribution: `[L1]` markdown syntax, `[L2]` grammar, `[L3]` code mismatch.

Example:

```text
📄 lunar-claude/README.md
  [L1] Line 42: MD013 Line length exceeds 120 characters
  [L2] Paragraph 3: Consider breaking long sentence for clarity
  [L3] References function 'verify_plugin()' not found in codebase

📄 lunar-claude/docs/plans/2025-01-15-docs-agent.md
  [L2] Missing "Testing Strategy" section recommended for design docs
  [L3] Code example line 87: Python syntax error in example

Summary: 15 issues (3 critical, 8 warnings, 4 info) across 8 files
Auto-fixable: 12 issues | Run: doc-agent fix --auto
```

### JSON Output

Structured for parsing by other tools or GitHub Actions:

```json
{
  "scan_timestamp": "2025-10-24T10:30:00Z",
  "repo": "/workspaces/lunar-claude",
  "layers_executed": [1, 2, 3],
  "duration_seconds": 47.3,
  "summary": {
    "files_scanned": 23,
    "issues_found": 15,
    "critical": 3,
    "warnings": 8,
    "info": 4,
    "auto_fixable": 12
  },
  "issues": [
    {
      "file": "README.md",
      "line": 42,
      "layer": 1,
      "severity": "warning",
      "code": "MD013",
      "message": "Line length exceeds 120 characters",
      "auto_fixable": true
    }
  ]
}
```

### Markdown Report

Generated for automated runs, posted as PR comment:

```markdown
## Documentation Analysis Report

**Scan Date**: 2025-10-24
**Repository**: lunar-claude
**Layers**: 1, 2, 3

### Summary
- 📄 Files scanned: 23
- ⚠️ Issues found: 15 (3 critical, 8 warnings, 4 info)
- ✅ Auto-fixable: 12

### Critical Issues
- `README.md:42` - References undefined function `verify_plugin()`
- `docs/architecture.md:156` - Broken link to moved file

### Auto-Fix Available
Run the following to fix 12 issues automatically:
```bash
doc-agent fix --auto --repo /workspaces/lunar-claude
```

<details>
<summary>View all issues</summary>
[Detailed issue list...]
</details>

```text

### Cross-Repo Dashboard

Aggregated view across all 10+ repos. Health score per repo (percentage of clean docs). Trending: issues increasing/decreasing over time. Hotspots: files with most frequent issues. Repo comparison: which repos have best/worst doc quality.

## Fix Command

`doc-agent fix --auto` applies fixes for Layer 1 issues: markdown formatting (via markdownlint --fix), broken internal links with suggested replacements. Creates git commit with detailed message.

`doc-agent fix --interactive` for Layer 2/3 issues: shows each issue, suggests fix, asks for approval. "This function is undocumented. Generate documentation? [y/N]". Applies approved fixes incrementally.

## Implementation Technology

- **Language**: Python 3.13 (matching lunar-claude development environment)
- **Agent SDK**: Claude Agent SDK for Python
- **CLI Framework**: Click or Typer
- **Terminal UI**: rich library for colorized output
- **Code Parsers**:
  - Python: ast module (standard library)
  - Terraform: python-hcl2
  - Ansible: PyYAML
  - Bash: subprocess with shellcheck
- **Git Operations**: GitPython
- **Concurrency**: asyncio for multi-repo processing
- **Configuration**: PyYAML for config files
- **Caching**: JSON files in `~/.cache/doc-agent/`

## Deployment Modes

### Local Ad-Hoc Usage

Primary workflow for daily development. Developer notices docs need attention. Runs `doc-agent scan --repo .` in current directory. Reviews terminal output with color-coded issues. Optionally runs `doc-agent fix --auto` for quick fixes. Commits results.

### Scheduled Automation

Cron job or systemd timer on homelab dev machine. Runs nightly: `doc-agent scan --all-repos --output markdown`. Generates markdown report in `~/doc-agent-reports/`. Optionally sends email notification if critical issues found.

### GitHub Actions

`.github/workflows/doc-maintenance.yml` triggers on PR or weekly schedule. Runs Layer 1 and Layer 2 (fast layers). Posts markdown report as PR comment. Auto-fixes Layer 1 issues and pushes commit if requested.

### Self-Hosted Runner

GitHub Actions running on homelab hardware. Full control over environment. Can run all three layers without cost concerns. Access to private repos and internal documentation.

## Next Steps

1. **Validation**: Review design with implementation team
2. **Worktree Setup**: Create isolated workspace for development
3. **Implementation Plan**: Break down into bite-sized tasks
4. **Prototype**: Start with Layer 1 integration and CLI foundation
5. **Iterate**: Add Layer 2 (Claude SDK), then Layer 3 (parsers)
6. **Test**: Validate across lunar-claude, Terraform, and Ansible repos
7. **Deploy**: Set up scheduled automation and GitHub Actions
