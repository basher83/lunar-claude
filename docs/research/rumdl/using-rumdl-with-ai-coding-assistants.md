# Using rumdl to Lint and Fix Markdown with AI Coding Assistants

## Executive Summary

**rumdl** is a high-performance Markdown linter and formatter written in Rust, designed to bring the speed and developer experience improvements of tools like `ruff` to the Markdown ecosystem. With 54 lint rules, automatic formatting capabilities, and seamless integration with modern editors and AI coding assistants, rumdl represents a significant advancement in Markdown quality assurance workflows.

This document synthesizes research on using rumdl with AI coding assistants like Claude Code, Cursor, VS Code, and other MCP-compatible tools to automate markdown linting and fixing workflows.

## Table of Contents

1. [Introduction to rumdl](#introduction-to-rumdl)
2. [Key Features and Benefits](#key-features-and-benefits)
3. [Installation and Setup](#installation-and-setup)
4. [Integration with AI Coding Assistants](#integration-with-ai-coding-assistants)
5. [Usage Patterns and Workflows](#usage-patterns-and-workflows)
6. [MCP Integration Possibilities](#mcp-integration-possibilities)
7. [Best Practices](#best-practices)
8. [Comparison with Alternatives](#comparison-with-alternatives)
9. [Real-World Examples](#real-world-examples)
10. [Future Directions](#future-directions)

---

## Introduction to rumdl

### What is rumdl?

**rumdl** is a blazing-fast Markdown linter and formatter built in Rust, inspired by `ruff`'s approach to Python linting. It brings similar speed and developer experience improvements to the Markdown ecosystem.

### Core Philosophy

- **Performance First**: Built for speed with Rust, significantly faster than alternatives
- **Zero Dependencies**: Single binary with no runtime requirements
- **Developer Experience**: Modern CLI with detailed error reporting and auto-fix capabilities
- **Compatibility**: 97.2% markdownlint compatibility for easy migration
- **Flexibility**: Highly configurable with TOML-based config files

### Performance Benchmarks

Benchmarked on the Rust Book repository (478 markdown files, October 2025):

- **rumdl**: ~0.8 seconds for 1000 files
- **markdownlint**: ~4.2 seconds for 1000 files
- **Performance improvement**: **5x faster** than markdownlint

With intelligent caching, subsequent runs are even faster—rumdl only re-lints files that have changed, making it ideal for watch mode and editor integration.

---

## Key Features and Benefits

### Linting Capabilities

- **54 lint rules** covering common Markdown issues
- **40+ auto-fixable rules** for automatic issue resolution
- **Rule categories**:
  - Headings (MD001, MD002, MD003, etc.)
  - Lists (MD004, MD005, MD007, etc.)
  - Whitespace (MD009, MD010, MD012, etc.)
  - Code blocks (MD040, MD046, MD048, etc.)
  - Links (MD034, MD039, MD042, etc.)
  - Images (MD045, MD052, etc.)
  - Style consistency (MD031, MD032, MD035, etc.)

### Formatting Features

- **Automatic formatting** with `--fix` flag (applies to 40+ auto-fixable rules out of 54 total rules)
- **Stdin/stdout support** for editor integrations
- **Watch mode** for continuous linting
- **Diff preview** to see changes before applying

**Note**: Not all rules are auto-fixable. The `--fix` flag automatically fixes violations for 40+ rules, but some rules require manual fixes or context-aware decisions.

### Non-Auto-Fixable Rules

The following rules are **NOT** auto-fixable and require manual intervention:

- **MD013** (Line length) - Requires content-aware line breaking decisions. Automatic wrapping could break semantic meaning or readability.
- **MD033** (Inline HTML) - HTML may be intentional (e.g., for styling, embedded content, or special formatting). Cannot be automatically removed without context.
- **MD041** (First line should be H1) - May be intentional if H1 is in YAML frontmatter or document structure doesn't require a top-level heading.
- **MD044** (Proper names) - Requires domain knowledge to determine correct capitalization of proper nouns and brand names.
- **MD052** (Reference links/images) - Broken references may be intentional placeholders or require external knowledge to fix.
- **MD053** (Link/image reference definitions) - Reference definition issues may require understanding of document structure and external dependencies.

**Note**: To get the most up-to-date list of auto-fixable vs. non-auto-fixable rules, run `rumdl rule` to see which rules are marked with auto-fix indicators. The exact count may vary by rumdl version, but typically 10-14 rules out of 54 total are not auto-fixable.

### Developer Experience

- **Modern CLI** with colorized output
- **JSON output** for tool integration
- **GitHub Actions annotations** support
- **Pre-commit hooks** integration
- **Language Server Protocol (LSP)** support

### Configuration

- **Multiple config formats**: `.rumdl.toml`, `pyproject.toml`, markdownlint compatibility
- **Automatic discovery**: Searches up directory tree for config files
- **Global configuration**: User-level defaults
- **Inline configuration**: HTML comments for rule exceptions
- **JSON Schema**: Autocomplete and validation in editors

---

## Installation and Setup

### Installation Methods

#### Using Cargo (Rust)

```bash
cargo install rumdl
```

#### Using pip (Python)

```bash
pip install rumdl
```

#### Using uv (Recommended for Python Projects)

```bash
# Install directly
uv tool install rumdl

# Or run without installing
uv tool run rumdl check .
```

#### Using Homebrew (macOS/Linux)

```bash
brew install rumdl
```

#### Using Nix (macOS/Linux)

```bash
nix-channel --update
nix-env --install --attr nixpkgs.rumdl
```

#### Download Binary

```bash
# Linux/macOS
curl -LsSf https://github.com/rvben/rumdl/releases/latest/download/rumdl-linux-x86_64.tar.gz | tar xzf - -C /usr/local/bin

# Windows PowerShell
Invoke-WebRequest -Uri "https://github.com/rvben/rumdl/releases/latest/download/rumdl-windows-x86_64.zip" -OutFile "rumdl.zip"
Expand-Archive -Path "rumdl.zip" -DestinationPath "$env:USERPROFILE\.rumdl"
```

### VS Code Extension Installation

For the best development experience, install the rumdl VS Code extension:

```bash
# Install the VS Code extension
rumdl vscode

# Check if the extension is installed
rumdl vscode --status

# Force reinstall the extension
rumdl vscode --force
```

The extension provides:

- 🔍 Real-time linting as you type
- 💡 Quick fixes for common issues
- 🎨 Code formatting on save
- 📋 Hover tooltips with rule documentation
- ⚡ Lightning-fast performance with zero lag

The CLI automatically detects VS Code, Cursor, or Windsurf and installs the appropriate extension.

### Initial Configuration

Create a default configuration file:

```bash
# Create .rumdl.toml
rumdl init

# Or for Python projects, add to pyproject.toml
rumdl init --pyproject
```

---

## Integration with AI Coding Assistants

### Claude Code Integration

Claude Code can leverage rumdl through several integration patterns:

#### 1. Command-Line Integration

Claude Code can execute rumdl commands directly:

```bash
# Lint markdown files
rumdl check .

# Auto-fix issues
rumdl check --fix .

# Format files
rumdl fmt .

# Check specific file
rumdl check README.md
```

#### 2. VS Code Extension Integration

When using Claude Code with VS Code or Cursor, the rumdl extension provides:

- **Real-time diagnostics**: Issues appear as you type
- **Quick fixes**: One-click auto-fixes for common issues
- **Format on save**: Automatic formatting when saving files
- **Status bar integration**: Shows linting status

**Configuration for Format on Save:**

```json
{
  "[markdown]": {
    "editor.formatOnSave": true
  }
}
```

#### 3. Script-Based Integration

Create scripts that Claude Code can invoke:

```python
#!/usr/bin/env python3
"""Lint markdown files using rumdl."""
import subprocess
import sys

def lint_markdown(file_path: str) -> dict:
    """Run rumdl check on a file and return results."""
    result = subprocess.run(
        ["rumdl", "check", "--output", "json", file_path],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

### Cursor Integration

Cursor (a VS Code fork) supports rumdl through:

1. **VS Code Extension Compatibility**: The rumdl extension works in Cursor
2. **Command Palette**: Access rumdl commands via `Cmd/Ctrl + Shift + P`
3. **AI Assistant Context**: Cursor's AI can see rumdl diagnostics and suggest fixes

### VS Code Integration

The rumdl VS Code extension provides:

- **Automatic activation** for `.md`, `.markdown`, `.mdown`, `.mkd`, `.mdx` files
- **LSP support** via `rumdl server --stdio`
- **Bundled binary**: No separate installation required
- **Cross-platform**: Optimized binaries for Windows, macOS, Linux

**Available Commands:**

- `rumdl: Fix All` - Apply all available auto-fixes
- `rumdl: Restart Server` - Restart the language server
- `rumdl: Show Client Logs` - View extension logs
- `rumdl: Show Server Logs` - View server logs
- `rumdl: Check Extension Status` - Display status and configuration

### Editor Integration Patterns

#### Stdin/Stdout Formatting

rumdl supports formatting via stdin/stdout, ideal for editor integrations:

```bash
# Format content from stdin
cat README.md | rumdl fmt - > README_formatted.md

# Use in a pipeline
echo "# Title " | rumdl fmt -
# Output: # Title

# Format clipboard content (macOS)
pbpaste | rumdl fmt - | pbcopy

# Provide filename context for better error messages
cat README.md | rumdl check - --stdin-filename README.md
```

#### Editor Integration with Quiet Mode

For editor integration, use stdin/stdout mode with `--quiet` flag:

```bash
# Format selection in editor (vim example)
:'<,'>!rumdl fmt - --quiet

# Format entire buffer
:%!rumdl fmt - --quiet
```

---

## Usage Patterns and Workflows

### Basic Workflow

1. **Discovery**: Run `rumdl check .` to find all errors
2. **Analysis**: Review errors and identify fixable vs. manual fixes
3. **Auto-fix**: Run `rumdl check --fix .` to automatically fix issues (applies to 40+ auto-fixable rules; remaining violations require manual fixes)
4. **Verification**: Run `rumdl check .` again to confirm fixes and identify any remaining manual fixes needed

### AI-Assisted Workflow

#### Pattern 1: Discovery and Fix

```bash
# Step 1: Discover all issues
rumdl check . > linting-report.txt

# Step 2: Parse and categorize (using rumdl-parser.py)
rumdl check . 2>&1 | scripts/rumdl-parser.py --summary

# Step 3: Auto-fix what can be fixed
rumdl check --fix .

# Step 4: AI assistant handles remaining issues
# (manual fixes requiring context understanding)
```

#### Pattern 2: Continuous Integration

```yaml
# GitHub Actions example
- name: Lint Markdown
  run: rumdl check --output-format github .
```

This produces annotations that GitHub automatically displays in PRs.

#### Pattern 3: Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/rvben/rumdl-pre-commit
    rev: v0.0.99
    hooks:
      - id: rumdl
        args: [--fix]  # Auto-fix issues
```

**Important**: The rumdl-pre-commit hook runs `rumdl` directly, which means it automatically discovers and respects configuration files (`.rumdl.toml`, `rumdl.toml`, or `pyproject.toml`) from the project root. Any `exclude` patterns defined in your rumdl config file will be applied when the pre-commit hook runs, so you don't need to configure excludes separately in `.pre-commit-config.yaml`.

### Advanced Workflows

#### Selective Rule Application

```bash
# Disable specific rules
rumdl check --disable MD013,MD033 README.md

# Enable only specific rules
rumdl check --enable MD001,MD003 README.md
```

#### File Filtering

```bash
# Exclude specific files/directories
rumdl check --exclude "node_modules,dist" .

# Include only specific files
rumdl check --include "docs/*.md,README.md" .

# Combine include and exclude
rumdl check --include "docs/**/*.md" --exclude "docs/temp,docs/drafts" .
```

#### Watch Mode

```bash
# Continuous linting as files change
rumdl check --watch docs/
```

#### Key Flags for AI Assistants

rumdl provides several flags that are particularly valuable for AI coding assistants:

##### `--diff`: Preview Changes Without Modifying Files

The `--diff` flag shows what would be fixed without actually modifying files, which is essential for AI assistants to:

- **Review changes before applying**: AI can see exactly what will change
- **Explain fixes to users**: Show users what will be fixed before committing
- **Validate fixes**: Ensure the proposed changes are correct
- **Build confidence**: Users can review diffs before accepting fixes

```bash
# Preview what would be fixed
rumdl check --diff .

# Combine with specific rules
rumdl check --diff --enable MD022,MD031 .
```

**Example Output:**

```diff
--- README.md
+++ README.md
@@ -10,6 +10,7 @@

 ## Introduction

+
 This is the content.
```

##### `--list-rules`: Discover Available Rules

The `--list-rules` flag helps AI assistants understand what rules are available:

```bash
# List all available rules
rumdl check --list-rules

# AI can use this to:
# - Understand rule capabilities
# - Suggest appropriate rules to users
# - Validate rule names before using --enable/--disable
```

**Use Cases for AI:**

- **Rule Discovery**: AI can discover available rules programmatically
- **Rule Validation**: Verify rule names before using them
- **User Guidance**: Suggest relevant rules based on user needs
- **Documentation**: Generate rule documentation automatically

##### `--verbose`: Detailed Output for Debugging

The `--verbose` flag provides detailed output including:

- Files checked (even if no issues found)
- Summary statistics
- More context about each violation

```bash
# Get verbose output for better context
rumdl check --verbose .

# Useful for AI when:
# - Debugging why certain files aren't being checked
# - Understanding the full scope of issues
# - Providing detailed reports to users
```

**Example Verbose Output:**

```text
✓ No issues found in CONTRIBUTING.md
README.md:12:1: [MD022] Headings should be surrounded by blank lines [*]
README.md:24:5: [MD037] Spaces inside emphasis markers [*]

Found 2 issues in 1 file (2 files checked)
Run `rumdl fmt` to automatically fix issues
```

##### `--profile`: Performance Analysis

The `--profile` flag shows profiling information, useful for:

- **Performance optimization**: Identify slow operations
- **Large repository analysis**: Understand where time is spent
- **CI/CD optimization**: Optimize linting workflows

```bash
# Get profiling information
rumdl check --profile .

# AI can use this to:
# - Optimize linting workflows
# - Identify performance bottlenecks
# - Recommend configuration changes for speed
```

##### `--no-config` and `--isolated`: Configuration Control

These flags help AI assistants work with configuration:

```bash
# Ignore all configuration files (use defaults)
rumdl check --no-config .

# Isolated mode (ignore config discovery)
rumdl check --isolated .
```

**Use Cases:**

- **Testing**: Test with default rules without config interference
- **Debugging**: Isolate configuration issues
- **CI/CD**: Ensure consistent behavior regardless of local config
- **Documentation**: Show default behavior to users

##### `--color`: Output Formatting Control

Control colored output for different environments:

```bash
# Disable colors (useful for CI/logs)
rumdl check --color never .

# Force colors (useful for terminals)
rumdl check --color always .

# Auto-detect (default)
rumdl check --color auto .
```

**AI Use Cases:**

- **CI/CD Integration**: Use `--color never` for clean logs
- **Terminal Output**: Use `--color always` for better readability
- **Log Parsing**: Disable colors when parsing output programmatically

#### Statistics and Rule Violation Analysis

The `--statistics` flag provides a high-level summary of rule violations, which is particularly valuable for AI assistants:

```bash
# Show rule violation statistics summary
rumdl check --statistics .
```

**Example Output:**

```text
Rule Violation Statistics:
  MD013 (Line length): 45 violations
  MD022 (Headings surrounded by blank lines): 23 violations
  MD031 (Fenced code blocks surrounded by blank lines): 12 violations
  MD033 (Inline HTML): 8 violations
  MD041 (First line should be H1): 5 violations
  ...
```

**Why Statistics Are Useful for AI Assistants:**

1. **Prioritization**: AI can identify which rules are violated most frequently and prioritize fixes accordingly
2. **Pattern Recognition**: Statistics reveal common patterns across the codebase that may indicate systematic issues
3. **Configuration Decisions**: Helps AI assistants recommend which rules to disable or configure based on actual usage patterns
4. **Efficient Workflows**: AI can focus on high-impact fixes first (rules with many violations)
5. **Progress Tracking**: Statistics provide measurable metrics for tracking improvement over time
6. **Resource Allocation**: When distributing work across multiple agents, statistics help balance workloads based on violation counts

**AI Assistant Workflow with Statistics:**

```bash
# Step 1: Get overview of violations
rumdl check --statistics . > stats.json

# Step 2: AI analyzes statistics to prioritize
# - Focus on rules with most violations first
# - Identify rules that might need configuration changes
# - Determine which rules are rarely violated (candidates for disabling)

# Step 3: Targeted fixing based on statistics
rumdl check --fix --enable MD013,MD022 .  # Fix most common issues first

# Step 4: Re-check statistics to measure progress
rumdl check --statistics .
```

**Combining Statistics with JSON Output:**

```bash
# Get both detailed errors and statistics
rumdl check --output json --statistics . | jq '.statistics'
```

This combination allows AI assistants to:

- Understand the big picture (statistics)
- Access detailed information (JSON output)
- Make informed decisions about fix prioritization
- Track progress over time

### Integration with AI Coding Assistants

#### Workflow: AI-Generated Markdown Validation

1. **AI generates markdown content**
2. **Automatically lint with rumdl**:

   ```bash
   echo "$CONTENT" | rumdl check --stdin --stdin-filename generated.md
   ```

3. **Auto-fix issues**:

   ```bash
   echo "$CONTENT" | rumdl fmt - > fixed.md
   ```

4. **Review and commit**

#### Workflow: Documentation Quality Assurance

1. **Pre-commit hook runs rumdl**
2. **Auto-fixes applied automatically**
3. **Remaining issues flagged for AI review**
4. **AI assistant provides context-aware fixes**

#### Workflow: Preview Before Fixing

The `--diff` flag enables AI assistants to show users what will change:

```python
#!/usr/bin/env python3
"""Preview fixes before applying them."""
import subprocess

def preview_fixes(file_path: str) -> str:
    """Show diff of what would be fixed."""
    result = subprocess.run(
        ["rumdl", "check", "--diff", file_path],
        capture_output=True,
        text=True
    )
    return result.stdout

# AI workflow:
# 1. Show user what will change
diff_output = preview_fixes("README.md")
print("Preview of fixes:")
print(diff_output)

# 2. Ask user for confirmation
# 3. Apply fixes if confirmed
```

#### Workflow: Statistics-Driven AI Decision Making

The `--statistics` flag enables AI assistants to make data-driven decisions:

```python
#!/usr/bin/env python3
"""AI assistant workflow using rumdl statistics."""
import subprocess
import json

def analyze_markdown_quality() -> dict:
    """Use statistics to inform AI decision-making."""
    # Get statistics
    result = subprocess.run(
        ["rumdl", "check", "--statistics", "--output", "json", "."],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    # AI analyzes statistics
    stats = data.get("statistics", {})

    # Prioritize rules by violation count
    prioritized_rules = sorted(
        stats.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )

    # AI decision logic
    recommendations = {
        "high_priority_fixes": [
            rule for rule, info in prioritized_rules[:5]
            if info.get("fixable", False)
        ],
        "config_suggestions": [
            rule for rule, info in prioritized_rules
            if info["count"] > 50  # Many violations might indicate config issue
        ],
        "low_priority": [
            rule for rule, info in prioritized_rules
            if info["count"] < 3  # Rare violations might be acceptable
        ]
    }

    return {
        "statistics": stats,
        "recommendations": recommendations,
        "total_violations": sum(info["count"] for info in stats.values())
    }
```

**Benefits for AI Assistants:**

- **Efficient Resource Allocation**: Focus on rules with most violations
- **Intelligent Configuration**: Suggest rule changes based on violation patterns
- **Progress Measurement**: Track improvement metrics over time
- **Pattern Detection**: Identify systematic issues across the codebase

---

## MCP Integration Possibilities

### Current State

While rumdl itself doesn't have an official MCP server, there are related projects:

#### markdownlint-mcp

The `markdownlint-mcp` project provides an MCP server for markdown linting:

- **Repository**: `github.com/ernestgwilsonii/markdownlint-mcp`
- **Features**:
  - `lint_markdown` tool - Analyze markdown files
  - `fix_markdown` tool - Auto-fix issues
  - `get_configuration` tool - Display rules and config
- **Status**: Production ready with 82% test coverage (522 passing tests)

**Usage with Claude Desktop:**

```json
{
  "mcpServers": {
    "markdownlint": {
      "command": "npx",
      "args": ["markdownlint-mcp"]
    }
  }
}
```

### Potential rumdl MCP Server

A rumdl-specific MCP server could provide:

1. **Direct rumdl Integration**: Use rumdl binary instead of markdownlint
2. **Performance Benefits**: Leverage rumdl's 5x speed advantage
3. **Enhanced Features**: Access to rumdl's 54 rules and auto-fix capabilities
4. **Better Compatibility**: Native rumdl configuration support

**Proposed MCP Tools:**

- `rumdl_lint` - Lint markdown files using rumdl
- `rumdl_fix` - Auto-fix markdown issues
- `rumdl_format` - Format markdown files
- `rumdl_config` - Get/set rumdl configuration
- `rumdl_rules` - List available rules and their descriptions
- `rumdl_statistics` - Get rule violation statistics for AI decision-making
- `rumdl_diff` - Preview changes without modifying files
- `rumdl_profile` - Get performance profiling information

**Example Implementation:**

```python
# rumdl-mcp-server (hypothetical)
from mcp.server import Server
from mcp.types import Tool

server = Server("rumdl-mcp")

@server.tool()
async def rumdl_lint(file_path: str) -> dict:
    """Lint a markdown file using rumdl."""
    import subprocess
    result = subprocess.run(
        ["rumdl", "check", "--output", "json", file_path],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

@server.tool()
async def rumdl_fix(file_path: str) -> dict:
    """Auto-fix markdown issues in a file."""
    import subprocess
    result = subprocess.run(
        ["rumdl", "check", "--fix", file_path],
        capture_output=True,
        text=True
    )
    return {"fixed": result.returncode == 0}
```

### Integration Benefits

MCP integration would enable:

1. **Seamless AI Workflows**: AI assistants can lint/fix markdown automatically
2. **Context Awareness**: AI can see linting issues and provide intelligent fixes
3. **Automated Quality**: Ensure markdown quality in AI-generated content
4. **Workflow Integration**: Combine linting with other MCP tools

---

## Best Practices

### Configuration Management

#### Project-Level Configuration

Create `.rumdl.toml` in project root:

```toml
# Global settings
[global]
line-length = 100
exclude = ["node_modules", "build", "dist"]
respect-gitignore = true

# Disable specific rules
disabled-rules = ["MD013", "MD033"]

# Per-file rule exceptions
[per-file-ignores]
"README.md" = ["MD033"]  # Allow HTML in README
"docs/api/**/*.md" = ["MD013", "MD041"]  # Relax rules for generated docs

# Rule-specific configuration
[MD007]
indent = 2

[MD013]
line-length = 100
code-blocks = false
tables = false
reflow = true  # Enable automatic line wrapping
```

**Exclude Pattern Format**: rumdl uses gitignore-style pattern matching for exclude patterns. You can use:

- **Simple paths**: Exact directory or file names (e.g., `"node_modules"`, `"CHANGELOG.md"`)
- **Glob patterns**: Pattern matching with `**` and `*` (e.g., `"**/reference/*.md"`, `"docs/**/*.md"`)

Both formats work, so use simple paths for exact matches and glob patterns when you need pattern matching. These excludes apply to all rumdl invocations, including when run via the pre-commit hook.

#### Python Project Configuration

For Python projects, use `pyproject.toml`:

```toml
[tool.rumdl]
line-length = 100
disable = ["MD033"]
include = ["docs/*.md", "README.md"]
exclude = [".git", "node_modules"]

[tool.rumdl.MD013]
code_blocks = false
tables = false
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Lint Markdown

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install rumdl
        run: cargo install rumdl
      - name: Lint Markdown
        run: rumdl check --output-format github .
```

#### Pre-commit Hooks

```yaml
repos:
  - repo: https://github.com/rvben/rumdl-pre-commit
    rev: v0.0.99
    hooks:
      - id: rumdl
        args: [--fix]  # Auto-fix issues
```

**Configuration Integration**: The rumdl-pre-commit hook executes `rumdl` directly, which means it automatically discovers and reads configuration files (`.rumdl.toml`, `rumdl.toml`, or `pyproject.toml`) from the project root. Excludes defined in your rumdl config file are respected by the pre-commit hook, so you can manage exclusions in one place rather than duplicating them in `.pre-commit-config.yaml`.

### AI Assistant Integration Patterns

#### Pattern 1: Validation Before Commit

```bash
# In AI assistant workflow
rumdl check . && git commit -m "Update documentation"
```

#### Pattern 2: Auto-Fix in AI Workflow

```bash
# AI generates markdown, then auto-fixes
rumdl check --fix . && rumdl check .  # Verify fixes
```

#### Pattern 3: Selective Fixing

```bash
# Fix only specific rule categories
rumdl check --fix --enable MD022,MD031,MD032 .
```

### Performance Optimization

1. **Use caching**: rumdl automatically caches results
2. **Exclude patterns**: Use `.rumdl.toml` to exclude generated files (applies to pre-commit hooks automatically)
3. **Watch mode**: Use `--watch` for development instead of repeated runs
4. **Selective rules**: Enable only needed rules for faster runs

**Note**: Excludes configured in `.rumdl.toml` are automatically respected by the rumdl-pre-commit hook since the hook runs `rumdl` directly, which discovers and reads config files from the project root.

### Error Handling

#### Exit Codes

- `0`: Success (no violations or all fixed)
- `1`: Violations found (or remain after `--fix`)
- `2`: Tool error

**Note**: `rumdl fmt` exits 0 on successful formatting (even if unfixable violations remain), making it compatible with editor integrations.

#### JSON Output for Automation

```bash
# Get structured output for tool integration
rumdl check --output json README.md | jq '.files[].issues[]'

# Get statistics summary for AI decision-making
rumdl check --statistics . | jq '.statistics'
```

#### Statistics for AI Workflows

The `--statistics` flag is particularly powerful for AI assistants:

```bash
# Get statistics to inform AI decision-making
rumdl check --statistics .

# Combine with JSON output for programmatic access
rumdl check --statistics --output json . > analysis.json
```

**Use Cases:**

1. **Prioritization**: AI can focus on rules with most violations
2. **Configuration**: Statistics reveal which rules might need adjustment
3. **Progress Tracking**: Measure improvement over time
4. **Resource Allocation**: Distribute work based on violation counts
5. **Pattern Detection**: Identify systematic issues across codebase

#### Complete Flag Reference for AI Assistants

Here's a comprehensive reference of flags useful for AI assistants:

| Flag | Purpose | AI Use Case |
|------|---------|-------------|
| `--diff` | Preview changes without modifying | Show users what will change before applying |
| `--fix` | Auto-fix issues | Apply fixes automatically |
| `--list-rules` | List all available rules | Discover capabilities, validate rule names |
| `--statistics` | Show violation statistics | Prioritize fixes, track progress |
| `--verbose` | Detailed output | Debug issues, provide comprehensive reports |
| `--profile` | Performance profiling | Optimize workflows, identify bottlenecks |
| `--output json` | JSON output format | Programmatic processing, tool integration |
| `--quiet` | Suppress diagnostic output | Clean output for parsing, editor integration |
| `--enable <rules>` | Enable specific rules | Targeted linting, focused fixes |
| `--disable <rules>` | Disable specific rules | Skip problematic rules, custom workflows |
| `--include <patterns>` | Include only matching files | Focus on specific areas |
| `--exclude <patterns>` | Exclude matching files | Skip generated/vendor files |
| `--force-exclude` | Enforce excludes even for explicit paths | Pre-commit hook compatibility |
| `--respect-gitignore` | Respect .gitignore files | Follow project conventions |
| `--stdin` | Read from stdin | Editor integration, pipeline processing |
| `--stdin-filename` | Provide filename context | Better error messages for stdin |
| `--no-config` | Ignore all config files | Test defaults, consistent CI behavior |
| `--isolated` | Ignore config discovery | Isolated testing, debugging |
| `--color <mode>` | Control colored output | CI/log formatting, terminal optimization |
| `--watch` | Watch mode for continuous linting | Development workflows |
| `--config <file>` | Specify config file | Override defaults, test configurations |

```text

---

## Comparison with Alternatives

### rumdl vs. markdownlint

| Feature | rumdl | markdownlint |
|---------|-------|--------------|
| **Performance** | ⭐⭐⭐⭐⭐ (5x faster) | ⭐⭐ |
| **Language** | Rust | JavaScript |
| **Rules** | 54 rules | 52 rules |
| **Compatibility** | 97.2% markdownlint compatible | 100% |
| **Auto-fix** | 40+ rules | Limited |
| **Dependencies** | Zero (single binary) | Node.js ecosystem |
| **LSP Support** | ✅ Native | Via extensions |
| **Configuration** | TOML, pyproject.toml, markdownlint | JSON/YAML |

### rumdl vs. mdformat

| Feature | rumdl | mdformat |
|---------|-------|----------|
| **Focus** | Linting + Formatting | Formatting only |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rule Coverage** | 54 rules | Limited |
| **Auto-fix** | Comprehensive | Formatting only |

### rumdl vs. Prettier

| Feature | rumdl | Prettier |
|---------|-------|----------|
| **Markdown Focus** | ✅ Primary | ⚠️ Secondary |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rule-Based** | ✅ 54 specific rules | ⚠️ General formatting |
| **Markdownlint Compatible** | ✅ Yes | ❌ No |

### When to Use rumdl

**Choose rumdl when:**

- ✅ You need maximum performance (large markdown repositories)
- ✅ You want markdownlint compatibility with better speed
- ✅ You need comprehensive auto-fix capabilities
- ✅ You prefer zero-dependency tools
- ✅ You want LSP support for editor integration
- ✅ You work with Python projects (pyproject.toml support)

**Consider alternatives when:**

- ⚠️ You need 100% markdownlint rule coverage (use markdownlint)
- ⚠️ You only need basic formatting (use mdformat)
- ⚠️ You're already heavily invested in Prettier ecosystem

---

## Real-World Examples

### Example 1: Documentation Repository

**Scenario**: Large documentation repository with 500+ markdown files

**Setup**:

```

```toml

## .rumdl.toml

[global]
line-length = 100
exclude = ["node_modules", "dist", "build"]
respect-gitignore = true

[per-file-ignores]
"CHANGELOG.md" = ["MD013", "MD041"]  # Long lines and no H1
"docs/api/**/*.md" = ["MD013"]  # Generated API docs
```

**Workflow**:

```text

```

```bash

## Pre-commit: Auto-fix issues

rumdl check --fix .

## CI: Report issues

rumdl check --output-format github .
```

### Example 2: AI-Generated Documentation

**Scenario**: AI assistant generates markdown documentation that needs validation

**Workflow**:

```text

```

```python
import subprocess
import json

def validate_ai_generated_markdown(content: str, filename: str) -> dict:
    """Validate AI-generated markdown using rumdl."""

## Write content to temp file

    with open(f"/tmp/{filename}", "w") as f:
        f.write(content)

    # Check for issues
    result = subprocess.run(
        ["rumdl", "check", "--output", "json", f"/tmp/{filename}"],
        capture_output=True,
        text=True
    )

    issues = json.loads(result.stdout)

    # Auto-fix if possible
    if issues.get("total_fixable", 0) > 0:
        subprocess.run(["rumdl", "check", "--fix", f"/tmp/{filename}"])
        # Re-read fixed content
        with open(f"/tmp/{filename}", "r") as f:
            content = f.read()

    return {
        "content": content,
        "issues": issues,
        "fixed": issues.get("total_fixable", 0) > 0
    }
```

### Example 3: Claude Code Integration

**Scenario**: Using rumdl with Claude Code for markdown quality assurance

**CLAUDE.md Configuration**:

```text

```

```text

```

```text

```

```markdown

## Markdown Quality Standards

All markdown files must pass rumdl linting:

1. Run `rumdl check .` before committing
2. Auto-fix issues with `rumdl check --fix .`
3. Manual fixes required for non-auto-fixable rules (see [Non-Auto-Fixable Rules](#non-auto-fixable-rules) section for complete list):
   - MD013 (line length) - requires content-aware line breaking
   - MD033 (inline HTML) - may be intentional
   - MD041 (first line H1) - may be in frontmatter
   - MD044 (proper names) - requires domain knowledge
   - MD052 (reference links/images) - may be intentional placeholders
   - MD053 (link/image reference definitions) - requires understanding of document structure

```

**Claude Code Workflow**:

1. Claude generates markdown content
2. Automatically runs `rumdl check --fix .`
3. Reviews remaining issues with context
4. Provides intelligent fixes for non-auto-fixable rules

### Example 4: Multi-Agent Workflow

**Scenario**: Distributing markdown linting fixes across multiple AI agents

**Using rumdl-parser.py**:

```text

```

```text

```

```text

```

```text

```

```text

```

```text

```

```text

```bash

## Step 1: Discover and categorize issues

rumdl check . 2>&1 | scripts/rumdl-parser.py --summary

## Step 2: Distribute fixable issues across 6 subagents

rumdl check . 2>&1 | scripts/rumdl-parser.py --distribute 6

## Step 3: Each subagent fixes assigned files

## Subagent 1: Fixes files with most fixable errors

## Subagent 2-6: Handle remaining files
```

---

## Future Directions

### Potential Enhancements

1. **Official MCP Server**: Native rumdl MCP server for AI assistant integration
2. **Enhanced AI Integration**: Better context-aware fixes using AI
3. **Rule Customization**: User-defined rules via configuration
4. **Performance Improvements**: Even faster linting for very large repositories
5. **Extended Rule Coverage**: Additional rules beyond markdownlint compatibility

### Community Trends

Based on research findings:

- **Performance Focus**: Rust-based tools are becoming the standard for performance-critical linting
- **AI Integration**: Growing demand for tools that work seamlessly with AI coding assistants
- **MCP Adoption**: MCP protocol is becoming the standard for AI tool integration
- **Unified Workflows**: Tools that combine linting, formatting, and fixing in one workflow

### Recommendations

1. **Adopt rumdl** for new projects requiring markdown linting
2. **Migrate from markdownlint** if performance is a concern
3. **Integrate with AI workflows** using command-line or MCP patterns
4. **Use pre-commit hooks** to ensure quality before commits
5. **Leverage auto-fix** capabilities to reduce manual work

---

## Conclusion

rumdl represents a significant advancement in Markdown linting and formatting, offering:

- **5x performance improvement** over markdownlint
- **97.2% compatibility** with existing markdownlint configurations
- **Comprehensive auto-fix** capabilities for 40+ rules
- **Seamless integration** with modern editors and AI coding assistants
- **Zero dependencies** with a single binary distribution

For AI coding assistants like Claude Code, Cursor, and VS Code, rumdl provides:

- **Real-time linting** via VS Code extension
- **Command-line integration** for automated workflows
- **JSON output** for programmatic processing
- **MCP integration potential** for native AI assistant support

The combination of rumdl's performance, compatibility, and integration capabilities makes it an ideal choice for teams using AI coding assistants to maintain high-quality markdown documentation.

---

## References

### Official Resources

- **GitHub Repository**: <<https://github.com/rvben/rumdl>>
- **Documentation**: <<https://github.com/rvben/rumdl#readme>>
- **VS Code Extension**: <<https://marketplace.visualstudio.com/items?itemName=rvben.rumdl>>
- **Crates.io**: <<https://crates.io/crates/rumdl>>
- **Pre-commit Hook**: <<https://github.com/rvben/rumdl-pre-commit>>

### Related Projects

- **markdownlint-mcp**: <https://github.com/ernestgwilsonii/markdownlint-mcp>
- **markdownlint**: <https://github.com/DavidAnson/markdownlint>
- **ruff**: <https://github.com/astral-sh/ruff> (inspiration for rumdl)

### Community Discussions

- **Lobsters Discussion**: <<https://lobste.rs/s/sxdel7/rumdl_markdown_linter_written_rust>>
- **Reddit Discussions**: Various threads on r/ClaudeAI, r/ClaudeCode

### Research Sources

- GitHub repository README and documentation
- VS Code extension documentation
- Community discussions and reviews
- MCP server implementations
- Performance benchmarks and comparisons

---

**Document Version**: 1.0
**Last Updated**: 2025-01-XX
**Research Method**: Multi-source web search and GitHub content analysis
**Tools Used**: Jina MCP (web search, URL reading), GitHub MCP (repository access)
