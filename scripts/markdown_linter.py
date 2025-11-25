#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
#     "langsmith[claude-agent-sdk]",
# ]
# ///
"""
Intelligent Markdown Linter - Agentic markdown linting with Claude agents.

Purpose: markdown-linting-automation
Team: devops
Author: devops@spaceships.work

A Claude Agent SDK application that orchestrates intelligent markdown linting:
- Custom MCP tools for rumdl operations (check, fix, statistics)
- Investigator subagent for false positive detection
- Fixer subagent for judgment-based fixes
- Orchestrated workflow with before/after reporting

Usage:
    ./scripts/markdown_linter.py [path]     # Lint specific path
    ./scripts/markdown_linter.py            # Lint current directory

Examples:
    # Lint entire repo
    ./scripts/markdown_linter.py .

    # Lint specific directory
    ./scripts/markdown_linter.py docs/

    # Lint single file
    ./scripts/markdown_linter.py README.md

    # With LangSmith tracing
    LANGSMITH_API_KEY=your_key LANGSMITH_TRACING=true ./scripts/markdown_linter.py .

Environment Variables:
    LANGSMITH_API_KEY     - Your LangSmith API key (optional, for tracing)
    LANGSMITH_PROJECT     - LangSmith project name (optional, defaults to "default")
    LANGSMITH_TRACING     - Set to "true" to enable tracing

Note: Authentication uses Claude Code CLI credentials. No ANTHROPIC_API_KEY needed.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from typing import Any

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)

# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING INFRASTRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════


class MarkdownLinterError(Exception):
    """Base exception for markdown linter errors."""

    pass


class RumdlNotFoundError(MarkdownLinterError):
    """Raised when rumdl executable is not found."""

    def __init__(self) -> None:
        super().__init__(
            "rumdl not found. Install with: cargo install rumdl\nVerify: rumdl --version"
        )


class RumdlExecutionError(MarkdownLinterError):
    """Raised when rumdl command fails unexpectedly."""

    def __init__(self, command: str, returncode: int, stderr: str) -> None:
        super().__init__(f"rumdl failed (exit {returncode}): {command}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr


def run_rumdl_command(args: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    """
    Execute rumdl command with error handling and timeout.

    Args:
        args: Command arguments (e.g., ['check', '--output-format', 'json', '.'])
        timeout: Timeout in seconds (default 30)

    Returns:
        CompletedProcess with stdout, stderr, returncode

    Raises:
        RumdlNotFoundError: If rumdl not installed
        subprocess.TimeoutExpired: If command times out
    """
    try:
        result = subprocess.run(
            ["rumdl", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        # Log stderr if present (warnings, etc.)
        if result.stderr:
            print(f"rumdl stderr: {result.stderr[:500]}", file=sys.stderr)
        return result
    except FileNotFoundError:
        raise RumdlNotFoundError() from None


# ═══════════════════════════════════════════════════════════════════════════════
# LANGSMITH TRACING (optional)
# ═══════════════════════════════════════════════════════════════════════════════

if os.getenv("LANGSMITH_TRACING", "").lower() == "true":
    try:
        from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

        configure_claude_agent_sdk()
        print("✓ LangSmith tracing enabled", file=sys.stderr)
    except ImportError:
        print(
            "⚠ LangSmith not installed. Run: uv add langsmith[claude-agent-sdk]",
            file=sys.stderr,
        )
    except ValueError as e:
        print(f"⚠ LangSmith configuration error: {e}", file=sys.stderr)
        print("   Check LANGSMITH_API_KEY environment variable", file=sys.stderr)
    except Exception as e:
        print(
            f"⚠ LangSmith initialization failed: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        print("   Continuing without tracing...", file=sys.stderr)

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Single source of truth for model selection - update here when changing models
MODEL_ID = "claude-sonnet-4-5-20250929"

# ═══════════════════════════════════════════════════════════════════════════════
# RUMDL HELPER FUNCTIONS (from rumdl-parser.py)
# ═══════════════════════════════════════════════════════════════════════════════


def has_yaml_frontmatter(file_path: str) -> bool:
    """Check if file starts with YAML frontmatter."""
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, encoding="utf-8") as f:
            first_line = f.readline().strip()
            return first_line == "---"
    except (OSError, UnicodeDecodeError):
        return False


def is_toml_section(line_content: str) -> bool:
    """Check if line looks like TOML section header."""
    return bool(re.match(r"^\[[\w\.\-]+\]", line_content.strip()))


def categorize_error(error: dict[str, Any], file_path: str) -> str:
    """
    Categorize error as 'auto_fixable', 'needs_investigation', or 'skip'.

    - auto_fixable: rumdl --fix can handle these (marked with [*])
    - needs_investigation: Ambiguous errors requiring AI judgment
    - skip: Known false positives
    """
    code = error.get("code", "")
    is_fixable = error.get("fixable", False)  # From JSON output

    # Auto-fixable by rumdl (MD032, MD031, MD029, etc.)
    if is_fixable:
        return "auto_fixable"

    # MD013 - Line length (needs judgment - is it prose or table/URL?)
    if code == "MD013":
        return "needs_investigation"

    # MD036 - Emphasis instead of heading (needs judgment)
    if code == "MD036":
        return "needs_investigation"

    # MD041 - Missing H1 (skip if frontmatter)
    if code == "MD041":
        if has_yaml_frontmatter(file_path):
            return "skip"
        return "needs_investigation"

    # MD033 - Inline HTML (needs investigation - intentional or accidental?)
    if code == "MD033":
        return "needs_investigation"

    # MD052 - Reference not found (might be TOML section in code block)
    if code == "MD052":
        return "needs_investigation"

    # MD053 - Reference unused (might be cross-file reference)
    if code == "MD053":
        return "needs_investigation"

    # Default: skip unknown codes
    return "skip"


def parse_rumdl_json(json_output: str) -> dict[str, Any]:
    """Parse rumdl JSON output and categorize errors."""
    try:
        data = json.loads(json_output)
    except json.JSONDecodeError as e:
        print(
            f"⚠ JSON parse failed: Line {e.lineno}, Col {e.colno}: {e.msg}",
            file=sys.stderr,
        )
        return {
            "error": f"JSON parse failed: {e.msg}",
            "details": f"Line {e.lineno}, column {e.colno}",
            "files": [],
        }

    # Validate structure
    if not isinstance(data, dict):
        return {"error": f"Expected JSON object, got {type(data).__name__}", "files": []}

    if "files" not in data:
        return {"error": "JSON missing 'files' key", "files": []}

    files_data = []
    total_auto_fixable = 0
    total_needs_investigation = 0
    total_skip = 0

    for file_entry in data.get("files", []):
        file_path = file_entry.get("path", "")
        errors = []

        for issue in file_entry.get("issues", []):
            error = {
                "line": issue.get("line", 0),
                "column": issue.get("column", 0),
                "code": issue.get("rule", ""),
                "message": issue.get("message", ""),
                "fixable": issue.get("fixable", False),
            }
            error["category"] = categorize_error(error, file_path)
            errors.append(error)

            if error["category"] == "auto_fixable":
                total_auto_fixable += 1
            elif error["category"] == "needs_investigation":
                total_needs_investigation += 1
            else:
                total_skip += 1

        if errors:
            files_data.append(
                {
                    "path": file_path,
                    "error_count": len(errors),
                    "auto_fixable_count": sum(1 for e in errors if e["category"] == "auto_fixable"),
                    "investigation_count": sum(
                        1 for e in errors if e["category"] == "needs_investigation"
                    ),
                    "skip_count": sum(1 for e in errors if e["category"] == "skip"),
                    "errors": errors,
                }
            )

    # Sort by investigation count (highest first - those need agent attention)
    files_data.sort(key=lambda x: x["investigation_count"], reverse=True)

    return {
        "total_files": len(files_data),
        "total_errors": total_auto_fixable + total_needs_investigation + total_skip,
        "total_auto_fixable": total_auto_fixable,
        "total_needs_investigation": total_needs_investigation,
        "total_skip": total_skip,
        "files": files_data,
    }


def parse_rumdl_text(text_output: str) -> dict[str, Any]:
    """Parse rumdl text output (fallback if JSON fails)."""
    errors_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for line in text_output.strip().split("\n"):
        if not line or "Issues: Found" in line or "Run `rumdl" in line:
            continue

        parts = line.split(":", 3)
        if len(parts) < 4:
            continue

        try:
            file_path = parts[0].strip()
            line_num = int(parts[1])
            col_num = int(parts[2])
            error_msg = parts[3].strip()

            # Extract error code from [CODE]
            code = "UNKNOWN"
            fixable = "[*]" in error_msg
            if "[" in error_msg and "]" in error_msg:
                code = error_msg.split("]")[0].replace("[", "").strip()

            error = {
                "line": line_num,
                "column": col_num,
                "code": code,
                "message": error_msg,
                "fixable": fixable,
            }
            error["category"] = categorize_error(error, file_path)
            errors_by_file[file_path].append(error)
        except (ValueError, IndexError):
            continue

    files_data = []
    for path, errors in errors_by_file.items():
        files_data.append(
            {
                "path": path,
                "error_count": len(errors),
                "auto_fixable_count": sum(1 for e in errors if e["category"] == "auto_fixable"),
                "investigation_count": sum(
                    1 for e in errors if e["category"] == "needs_investigation"
                ),
                "skip_count": sum(1 for e in errors if e["category"] == "skip"),
                "errors": errors,
            }
        )

    files_data.sort(key=lambda x: x["investigation_count"], reverse=True)

    return {
        "total_files": len(files_data),
        "total_errors": sum(f["error_count"] for f in files_data),
        "total_auto_fixable": sum(f["auto_fixable_count"] for f in files_data),
        "total_needs_investigation": sum(f["investigation_count"] for f in files_data),
        "total_skip": sum(f["skip_count"] for f in files_data),
        "files": files_data,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM MCP TOOLS FOR RUMDL
# ═══════════════════════════════════════════════════════════════════════════════


@tool("rumdl_check", "Lint markdown files and return categorized errors", {"path": str})
async def rumdl_check(args: dict[str, Any]) -> dict[str, Any]:
    """
    Run rumdl check on path and return categorized errors.

    Returns structured data with errors categorized as:
    - auto_fixable: Can be fixed by rumdl --fix
    - needs_investigation: Requires AI judgment
    - skip: Known false positives
    """
    path = args.get("path", ".")

    # Validate path
    if not os.path.exists(path):
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"error": f"Path not found: {path}"}, indent=2),
                }
            ]
        }

    try:
        # Try JSON output first
        result = run_rumdl_command(["check", "--output-format", "json", path])

        if result.returncode == 0 and not result.stdout.strip():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            {
                                "status": "clean",
                                "message": "No linting errors found!",
                                "total_errors": 0,
                            },
                            indent=2,
                        ),
                    }
                ]
            }

        # Parse JSON output
        if result.stdout.strip().startswith("{"):
            parsed = parse_rumdl_json(result.stdout)
        else:
            # Fallback to text parsing
            text_result = run_rumdl_command(["check", path])
            parsed = parse_rumdl_text(text_result.stdout + text_result.stderr)

        return {"content": [{"type": "text", "text": json.dumps(parsed, indent=2)}]}

    except RumdlNotFoundError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"error": str(e), "category": "configuration"}, indent=2),
                }
            ]
        }
    except subprocess.TimeoutExpired:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "error": "Command timed out after 30s",
                            "suggestion": "Try a smaller path",
                        },
                        indent=2,
                    ),
                }
            ]
        }


@tool("rumdl_fix", "Auto-fix markdown errors that rumdl can handle", {"path": str})
async def rumdl_fix(args: dict[str, Any]) -> dict[str, Any]:
    """
    Run rumdl check --fix to auto-fix [*] marked errors.

    This handles: MD032, MD031, MD029, and other auto-fixable rules.
    Returns count of files modified and remaining errors.
    """
    path = args.get("path", ".")

    # Validate path
    if not os.path.exists(path):
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"error": f"Path not found: {path}"}, indent=2),
                }
            ]
        }

    try:
        # Get before count
        before_result = run_rumdl_command(["check", path])
        before_lines = [
            line for line in before_result.stdout.split("\n") if line.strip() and "[" in line
        ]
        before_count = len(before_lines)

        # Run fix
        fix_result = run_rumdl_command(["check", "--fix", path])

        # Get after count
        after_result = run_rumdl_command(["check", path])
        after_lines = [
            line for line in after_result.stdout.split("\n") if line.strip() and "[" in line
        ]
        after_count = len(after_lines)

        fixed_count = before_count - after_count

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "status": "completed",
                            "errors_before": before_count,
                            "errors_after": after_count,
                            "errors_fixed": fixed_count,
                            "fix_output": fix_result.stdout[:1000]
                            if fix_result.stdout
                            else "No output",
                        },
                        indent=2,
                    ),
                }
            ]
        }

    except RumdlNotFoundError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"error": str(e), "category": "configuration"}, indent=2),
                }
            ]
        }
    except subprocess.TimeoutExpired:
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "error": "Command timed out after 30s",
                            "suggestion": "Try a smaller path",
                        },
                        indent=2,
                    ),
                }
            ]
        }


@tool("rumdl_statistics", "Get rule violation statistics for the path", {"path": str})
async def rumdl_statistics(args: dict[str, Any]) -> dict[str, Any]:
    """
    Run rumdl check --statistics to see which rules are failing most.

    Useful for understanding the scope of linting issues and prioritizing fixes.
    """
    path = args.get("path", ".")

    # Validate path
    if not os.path.exists(path):
        return {"content": [{"type": "text", "text": f"❌ Error: Path not found: {path}"}]}

    try:
        result = run_rumdl_command(["check", "--statistics", path])
        output = result.stdout + result.stderr

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Rule violation statistics for {path}:\n\n{output}",
                }
            ]
        }

    except RumdlNotFoundError as e:
        return {"content": [{"type": "text", "text": f"❌ Error: {e}"}]}
    except subprocess.TimeoutExpired:
        return {"content": [{"type": "text", "text": "❌ Error: Command timed out after 30s"}]}


@tool("rumdl_diff", "Preview what changes rumdl --fix would make", {"path": str})
async def rumdl_diff(args: dict[str, Any]) -> dict[str, Any]:
    """
    Run rumdl check --diff to preview fixes without applying them.

    Useful for reviewing what auto-fix would change before committing.
    """
    path = args.get("path", ".")

    # Validate path
    if not os.path.exists(path):
        return {"content": [{"type": "text", "text": f"❌ Error: Path not found: {path}"}]}

    try:
        result = run_rumdl_command(["check", "--diff", path])
        output = result.stdout if result.stdout else "No changes would be made."

        return {
            "content": [{"type": "text", "text": f"Diff preview for {path}:\n\n{output[:5000]}"}]
        }

    except RumdlNotFoundError as e:
        return {"content": [{"type": "text", "text": f"❌ Error: {e}"}]}
    except subprocess.TimeoutExpired:
        return {"content": [{"type": "text", "text": "❌ Error: Command timed out after 30s"}]}


# Create the MCP server with all rumdl tools
RUMDL_SERVER = create_sdk_mcp_server(
    name="rumdl",
    version="1.0.0",
    tools=[rumdl_check, rumdl_fix, rumdl_statistics, rumdl_diff],
)


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT DEFINITIONS (converted from .claude/agents/markdown-*.md)
# ═══════════════════════════════════════════════════════════════════════════════

INVESTIGATOR_PROMPT = """You are the Markdown Linting Investigator. You have **full autonomy** to analyze errors and make determinations.

## Your Mission

Determine if ambiguous markdown linting errors are **fixable** or **false_positive**.

## Analysis Approach

### For MD033 (Inline HTML)

**Question:** Is this HTML intentional or accidental?

**Investigation strategy:**
1. Read the file and examine context around the error line
2. Determine if HTML is:
   - **Intentional:** Documentation component (e.g., `<Tip>`, `<Warning>`), code example → false_positive
   - **Accidental:** Random markup in prose (e.g., `<b>`, `<i>` in regular text) → fixable

### For MD053 (Reference unused)

**Question:** Is this reference actually used elsewhere?

**Investigation strategy:**
1. Extract the reference name from error message
2. Search current file for `[reference]:` definition
3. If not found, search across all .md files with Grep
4. If found elsewhere → false_positive (cross-file reference)

### For MD052 (Reference not found)

**Question:** Is this a TOML section header or actually a broken link reference?

**Investigation strategy:**
1. Read the file and check if error is within a code block
2. Look for TOML patterns: `[section.name]`, `[tools.uv]`, etc.
3. If in code block or matches TOML pattern → false_positive

### For MD041 (Missing H1)

**Question:** Should this file have H1, or is the structure intentional?

**Investigation strategy:**
1. Read first 10 lines of file
2. Check for YAML frontmatter (starts with `---`)
3. If frontmatter present with title field → false_positive

### For MD013 (Line too long)

**Question:** Should this line be wrapped or is it special content?

**Investigation strategy:**
1. Read the line content
2. If it's a URL, table, or code reference → false_positive
3. If it's prose that can be wrapped → fixable

### For MD036 (Emphasis instead of heading)

**Question:** Is this emphasis intentional or a lazy heading?

**Investigation strategy:**
1. Read the context - is this standalone emphasized text on its own line?
2. If it's acting as a section divider → fixable (convert to heading)
3. If it's inline emphasis within prose → false_positive

## Output Format

Return a JSON object with your investigation results:

```json
{
  "investigations": [
    {
      "file": "path/to/file.md",
      "results": [
        {
          "error": {"line": 15, "code": "MD053", "message": "..."},
          "verdict": "false_positive",
          "reasoning": "Reference is defined in setup.md:42. Cross-file reference is valid."
        }
      ]
    }
  ]
}
```

## Critical Rules

- **Use all available tools** - Read files, search patterns, grep across repository
- **Examine full context** - Don't judge errors in isolation
- **Provide clear reasoning** - Explain WHY you made each determination
- **Be thorough** - Cross-file references, code blocks, frontmatter all matter
"""

INVESTIGATOR_AGENT = AgentDefinition(
    description="Autonomous analyzer that determines if markdown errors are fixable or false positives. Use for MD033, MD052, MD053, MD041, MD013, MD036 errors.",
    prompt=INVESTIGATOR_PROMPT,
    tools=["Read", "Grep", "Glob"],
    model=MODEL_ID,
)

FIXER_PROMPT = """You are the Markdown Fixer. Your role is to execute fixes for confirmed errors.

## Your Input

You receive files with errors that have been investigated and confirmed as fixable.

## Fix Strategies

### MD013 (Line too long)

**Strategy:**
1. Identify natural break points (spaces, punctuation)
2. Wrap line while preserving meaning
3. Ensure wrapped lines maintain proper markdown formatting
4. Don't break URLs, tables, or code references

### MD033 (Inline HTML)

**Strategy:**
1. Replace `<b>text</b>` with `**text**`
2. Replace `<i>text</i>` with `*text*`
3. Replace `<code>text</code>` with backticks
4. Preserve surrounding context

### MD036 (Emphasis instead of heading)

**Strategy:**
1. Replace `**Heading Text**` with appropriate heading level
2. Determine heading level from context (usually ## or ###)
3. Ensure blank lines around heading

### MD025 (Multiple H1s)

**Strategy:**
1. Keep first H1 as-is
2. Convert subsequent H1s to H2 (`## Heading`)

## Verification

After fixing each file, the orchestrator will verify with rumdl_check.

## Output Format

Report what you fixed:

```json
{
  "results": [
    {
      "path": "path/to/file.md",
      "fixed": ["MD013 at line 15", "MD036 at line 42"],
      "skipped": ["MD013 at line 88 - URL cannot be wrapped"]
    }
  ]
}
```

## Critical Rules

- **Fix only assigned errors** - Don't modify unrelated content
- **Preserve meaning** - Formatting fixes must not alter semantics
- **Report honestly** - If a fix can't be applied, report it
"""

FIXER_AGENT = AgentDefinition(
    description="Executes markdown fixes based on confirmed errors and investigation context. Use after investigator has determined what's fixable.",
    prompt=FIXER_PROMPT,
    tools=["Read", "Edit"],
    model=MODEL_ID,
)


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ORCHESTRATOR_PROMPT = """You are the Markdown Linting Orchestrator. Coordinate the intelligent linting workflow.

## Available Tools

- `mcp__rumdl__rumdl_check` - Get categorized lint errors
- `mcp__rumdl__rumdl_fix` - Auto-fix [*] marked errors
- `mcp__rumdl__rumdl_statistics` - See rule violation breakdown
- `mcp__rumdl__rumdl_diff` - Preview fixes before applying

## Available Agents

- `investigator` - Analyzes ambiguous errors (MD033, MD052, MD053, MD041, MD013, MD036)
- `fixer` - Applies fixes for confirmed errors

## Workflow

### Phase 1: Auto-Fix Easy Wins
1. Run `rumdl_fix` to auto-fix all [*] marked errors (MD032, MD031, MD029, etc.)
2. This typically handles 60%+ of errors instantly

### Phase 2: Analyze Remaining
3. Run `rumdl_check` to see what's left
4. Review the categorized output:
   - `auto_fixable`: Should be 0 after Phase 1
   - `needs_investigation`: Requires agent analysis
   - `skip`: Known false positives (ignore)

### Phase 3: Investigate Ambiguous Errors
5. If `needs_investigation` > 0:
   - Prepare a list of files and errors for the investigator
   - Use `investigator` agent to analyze each
   - Collect verdicts: fixable vs false_positive

### Phase 4: Apply Judgment Fixes
6. For errors marked fixable by investigator:
   - Use `fixer` agent to apply fixes
   - Verify each fix with `rumdl_check`

### Phase 5: Report Results
7. Run final `rumdl_check` to get after-state
8. Report:
   - Total errors found initially
   - Errors auto-fixed by rumdl
   - Errors fixed by fixer agent
   - False positives preserved
   - Final error count
   - Fix rate percentage

## Important Notes

- Always run rumdl_fix FIRST before investigation
- Don't investigate errors that rumdl can auto-fix
- Trust the investigator's verdicts
- Report clearly with before/after statistics
"""


def get_options(target_path: str) -> ClaudeAgentOptions:
    """Create ClaudeAgentOptions with orchestrator configuration."""
    return ClaudeAgentOptions(
        setting_sources=["user", "project", "local"],
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": ORCHESTRATOR_PROMPT,
        },
        allowed_tools=[
            "Bash",
            "Task",
            "Read",
            "Edit",
            "Grep",
            "Glob",
            "mcp__rumdl__rumdl_check",
            "mcp__rumdl__rumdl_fix",
            "mcp__rumdl__rumdl_statistics",
            "mcp__rumdl__rumdl_diff",
        ],
        agents={
            "investigator": INVESTIGATOR_AGENT,
            "fixer": FIXER_AGENT,
        },
        mcp_servers={"rumdl": RUMDL_SERVER},
        permission_mode="acceptEdits",
        model=MODEL_ID,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════


def display_message(msg: Any) -> None:
    """Display message content in a clean format."""
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(block.text, end="", flush=True)
            elif isinstance(block, ToolUseBlock):
                print(f"\n🛠️  Using: {block.name}")
    elif isinstance(msg, ResultMessage):
        print("\n" + "=" * 60)
        print("✅ Workflow Complete")
        if msg.duration_ms:
            print(f"Duration: {msg.duration_ms / 1000:.1f}s")
        if msg.total_cost_usd:
            print(f"Cost: ${msg.total_cost_usd:.4f}")
        print("=" * 60)


async def run_linting(target_path: str) -> None:
    """Run the intelligent markdown linting workflow."""
    print("=" * 60)
    print("🔍 Intelligent Markdown Linter")
    print(f"   Target: {target_path}")
    print("=" * 60)

    # Validate target path
    if not os.path.exists(target_path):
        print(f"\n❌ Error: Target path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    options = get_options(target_path)

    prompt = f"""Run the intelligent markdown linting workflow on: {target_path}

Execute all phases:
1. Auto-fix with rumdl_fix
2. Check remaining errors with rumdl_check
3. Investigate ambiguous errors with investigator agent
4. Apply fixes with fixer agent
5. Report final statistics

Be thorough and report clear before/after metrics."""

    try:
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                display_message(message)
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        print(f"\n❌ Claude SDK Error: {error_type}", file=sys.stderr)
        print(f"   {error_msg}", file=sys.stderr)

        # Category-based guidance
        error_lower = (error_type + " " + error_msg).lower()
        if "authentication" in error_lower or "api key" in error_lower:
            print("\n   💡 Check Claude Code CLI auth. Run: claude login", file=sys.stderr)
        elif "connection" in error_lower or "network" in error_lower:
            print("\n   💡 Check internet connection and try again.", file=sys.stderr)
        elif "rate" in error_lower or "limit" in error_lower:
            print("\n   💡 Rate limit exceeded. Wait and try again.", file=sys.stderr)
        elif "setting" in error_lower or "config" in error_lower:
            print("\n   💡 Check .claude/settings.json configuration.", file=sys.stderr)
        else:
            print(
                "\n   💡 Try again. If persists, check https://status.anthropic.com",
                file=sys.stderr,
            )

        sys.exit(1)

    print()


async def main() -> None:
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        target_path = sys.argv[1]
    else:
        target_path = "."

    try:
        # Verify rumdl is available
        result = run_rumdl_command(["--version"], timeout=5)
        print(f"✓ rumdl: {result.stdout.strip()}", file=sys.stderr)

        await run_linting(target_path)

    except RumdlNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        if os.getenv("DEBUG"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
