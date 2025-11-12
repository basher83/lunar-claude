#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
#     "typer>=0.12.0",
#     "rich>=13.0.0",
# ]
# ///
"""
PR Verification Script using Claude Agent SDK

This script verifies that PR claims match actual implementation by using Claude Agent SDK
to execute git commands and analyze code changes.

Prerequisites:
    - ANTHROPIC_API_KEY environment variable set
    - git installed and configured
    - gh CLI installed (optional, for PR metadata)

Usage:
    ./verify-pr.py <PR-number|branch-name>
    ./verify-pr.py 7
    ./verify-pr.py cursor/implement-plan-from-cu-plan-md-11ba
    ./verify-pr.py main...feature-branch --json

The verification prompt is embedded from .claude/commands/verify-pr.md methodology.
"""

import json
import os
import sys
from enum import Enum
from typing import Any

import anyio
import typer
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)
from rich.console import Console
from rich.table import Table

# Embedded prompt from verify-pr.md (lines 7-316)
# Replaced $ARGUMENTS with {pr_identifier} for runtime substitution
VERIFY_PR_PROMPT = """# Task: Verify Pull Request Claims

**PR to verify:** {pr_identifier}

**Purpose:** Verify that a PR's description, commits, and plan match actual implementation.

**Core 4 Foundation:**
- **Context:** PR metadata + git changes + plan documents
- **Model:** Semantic verification capabilities
- **Prompt:** This systematic verification process
- **Tools:** Git commands, gh CLI, file operations

---

## Instructions

You are verifying a pull request. Check that claims in PR description, commits, and plans match actual code changes.

### Core Principles

1. **Evidence before claims:** Never mark verified without git command output proving it
2. **Verify behavior, not names:** Check what code DOES. Different filenames can provide same functionality.
3. **Counter-evidence first:** Define what would disprove claim BEFORE checking
4. **Cross-reference patterns:** If comparing implementations, check what feature IS first

---

## Step 1: Identify PR and Extract Claims

### Determine PR Type

The argument could be:
- Branch name: `cursor/implement-plan-from-cu-plan-md-11ba`
- PR number: `#7` or `7`
- Comparison: `main...feature-branch`

**Commands to identify:**

```bash
# If branch name given, check if it exists
git show-ref --verify refs/heads/{pr_identifier} 2>/dev/null || git show-ref --verify refs/remotes/origin/{pr_identifier}

# If looks like PR number, try gh
gh pr view {pr_identifier} 2>/dev/null

# Get comparison syntax
git log --oneline main...{pr_identifier} | head -10
```

### Extract Claims

**From PR description (if available):**

```bash
gh pr view {pr_identifier} --json body -q .body
```

**From commit messages:**

```bash
git log --format="%s%n%b" main...{pr_identifier}
```

**From referenced plan documents:**

```bash
# Look for plan references in commits or PR description
git log main...{pr_identifier} | grep -i "plan\|spec\|requirement"
```

**Common claim patterns to extract:**
- "Adds feature X"
- "Fixes bug Y"
- "Implements Z from plan"
- "Includes tests"
- "Updates documentation"
- "Breaking change"
- "Closes #123"

---

## Step 2: Verify Claims Against Implementation

### Feature Implementation Claims

**Claim pattern:** "Adds/Implements feature X"

**Verify:**

```bash
# What files changed?
git diff --name-only main...{pr_identifier}

# Does feature exist in code?
git diff main...{pr_identifier} -- path/to/feature

# Search for feature implementation
git show {pr_identifier}:path/to/file | grep -A 10 "feature_name"
```

**Counter-evidence:** "This would be FALSE if no implementation exists for claimed feature"

### Test Coverage Claims

**Claim pattern:** "Includes tests" or "Adds test coverage"

**Verify:**

```bash
# Test files added?
git diff --name-only main...{pr_identifier} | grep -i test

# Test functions added?
git diff main...{pr_identifier} -- tests/ | grep "^+.*def test_"

# Count tests added
git show {pr_identifier}:path/to/test.py | grep -c "def test_"
```

**Counter-evidence:** "This would be FALSE if no test files or test functions were added"

### Bug Fix Claims

**Claim pattern:** "Fixes bug #123" or "Resolves issue"

**Verify:**

```bash
# Related code changes?
git diff main...{pr_identifier} | grep -A 5 -B 5 "bug_context"

# Issue referenced?
git log main...{pr_identifier} | grep -i "#123\|issue"

# If gh available, check issue status
gh issue view 123 --json state,closedAt
```

### Plan/Requirement Verification

**Claim pattern:** "Implements plan from X" or "Follows requirements in Y"

**Verify:**

```bash
# Read plan document
cat path/to/plan.md

# Check each requirement against implementation
git diff main...{pr_identifier} -- path/matching/requirement
```

**Counter-evidence:** "This would be FALSE if plan requirement X is not implemented"

### Breaking Change Claims

**Claim pattern:** "Breaking change" or "API change"

**Verify:**

```bash
# Check for removed/renamed functions
git diff main...{pr_identifier} | grep "^-.*def \|^-.*class "

# Check for signature changes
git diff main...{pr_identifier} -- path/to/api | grep -A 3 "^-.*def \|^+.*def "
```

### Documentation Claims

**Claim pattern:** "Updates documentation" or "Adds README"

**Verify:**

```bash
# Documentation files changed?
git diff --name-only main...{pr_identifier} | grep -E "\\.md$|docs/"

# Check actual changes
git diff main...{pr_identifier} -- "*.md" docs/
```

---

## Step 3: Verify Line Counts and Stats

If PR claims specific statistics:

```bash
# Total lines changed
git diff --stat main...{pr_identifier}

# Lines per file
git diff --numstat main...{pr_identifier}

# Files changed count
git diff --name-only main...{pr_identifier} | wc -l
```

---

## Step 4: Cross-Reference with Other PRs

If claims involve comparisons (e.g., "Different from PR #8"):

**Process:**
1. Verify what the claimed difference IS in the reference PR
2. Check if difference actually exists
3. Compare functionality, not just filenames

```bash
# Compare file structures
git diff --name-only main...pr-8-branch | sort > /tmp/pr8-files
git diff --name-only main...pr-9-branch | sort > /tmp/pr9-files
diff /tmp/pr8-files /tmp/pr9-files

# Compare implementations
git show pr-8-branch:path/to/file > /tmp/pr8-impl
git show pr-9-branch:path/to/file > /tmp/pr9-impl
diff /tmp/pr8-impl /tmp/pr9-impl
```

---

## Anti-Patterns (What NOT to Do)

❌ Trusting PR description without verifying code
❌ Verifying filename existence without checking implementation
❌ Assuming different filenames = missing functionality
❌ Claiming "tests added" without counting actual test functions
❌ Marking "implements plan" without checking each requirement
❌ Meta-analysis about the PR's philosophical meaning
❌ Comparing commits without comparing actual functionality

---

## Deliverable Format

## PR Overview

- **PR identifier:** {pr_identifier}
- **Base branch:** [detected]
- **Files changed:** [count]
- **Commits:** [count]

## Claims Extracted

1. [Claim from PR description]
2. [Claim from commit message]
3. [Claim from plan reference]

## Verification Results

| Claim | Source | Verified? | Evidence |
|-------|--------|-----------|----------|
| [exact quote] | PR desc/commit/plan | ✅/❌/⚠️ | git command + key output |

## Summary

- Total claims checked: N
- Verified correct: N
- Found incorrect: N
- Critical mismatches: [list]

## Recommendation

[Based on verification: ready to merge / needs fixes / claims don't match implementation]

---

## Example: Verifying PR Implementation

**Given:** `/verify-pr cursor/implement-plan-from-cu-plan-md-11ba`

**Extract claims:**

```bash
# Check commits
git log --oneline main...cursor/implement-plan-from-cu-plan-md-11ba

# Find referenced plan
git log main...cursor/implement-plan-from-cu-plan-md-11ba | grep -i "plan"
# → References cu-plan.md
```

**Verify against cu-plan.md requirements:**

**Claim 1:** "Creates Jina MCP server"
```bash
git diff --name-only main...cursor/... | grep "jina.*mcp"
# → plugins/meta/claude-docs/mcp/jina_docs_mcp.py
```
✅ Verified

**Claim 2:** "Creates Jina direct API script"
```bash
git diff --name-only main...cursor/... | grep -i jina | grep scripts
# → plugins/meta/claude-docs/scripts/claude_docs_jina.py

# Verify it's direct API (not MCP)
git show cursor/...:plugins/meta/claude-docs/scripts/claude_docs_jina.py | grep "dependencies"
# → httpx>=0.27.0 (direct HTTP, not MCP)
```
✅ Verified

---

**Remember:** Your value is verifying that code matches claims. Boring verification is success. Trust the code, not the description.

**Foundation:** Context (PR + plans), Model (verification), Prompt (this process), Tools (git + gh).
"""

console = Console()


class OutputFormat(str, Enum):
    """Output format options."""

    RICH = "rich"
    JSON = "json"


def create_sdk_options() -> ClaudeAgentOptions:
    """
    Create ClaudeAgentOptions for PR verification.

    Uses claude_code system prompt with Bash and Read tools for git operations
    and file reading.

    Returns:
        Configured options for ClaudeSDKClient
    """
    return ClaudeAgentOptions(
        system_prompt="claude_code",  # Provides built-in tool knowledge
        allowed_tools=["Bash", "Read"],  # Git commands and file reading
        permission_mode="acceptEdits",  # Auto-accept for automated workflow
        model="claude-sonnet-4-5",
    )


async def verify_pr(pr_identifier: str) -> dict[str, Any]:
    """
    Verify PR claims against implementation using Claude Agent SDK.

    Args:
        pr_identifier: PR number, branch name, or comparison (e.g., "7", "main...feature")

    Returns:
        Dictionary with verification results and metadata
    """
    # Format prompt with PR identifier
    prompt = VERIFY_PR_PROMPT.format(pr_identifier=pr_identifier)

    # Get SDK configuration
    options = create_sdk_options()

    # Collect response content
    response_text = []
    duration_ms = None
    total_cost_usd = None

    async with ClaudeSDKClient(options=options) as client:
        # Send verification prompt
        await client.query(prompt)

        # Stream and collect responses
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text.append(block.text)

            elif isinstance(message, ResultMessage):
                duration_ms = message.duration_ms
                total_cost_usd = message.total_cost_usd

    # Combine all response text
    full_response = "\n".join(response_text)

    return {
        "pr_identifier": pr_identifier,
        "response": full_response,
        "duration_ms": duration_ms,
        "total_cost_usd": total_cost_usd,
    }


def format_output(results: dict[str, Any], format: OutputFormat) -> None:
    """
    Format and display verification results.

    Args:
        results: Dictionary with verification results
        format: Output format (rich or json)
    """
    if format == OutputFormat.JSON:
        # JSON output for machine-readable format
        output = {
            "pr_identifier": results["pr_identifier"],
            "verification_response": results["response"],
            "duration_ms": results["duration_ms"],
            "total_cost_usd": results["total_cost_usd"],
        }
        print(json.dumps(output, indent=2))
    else:
        # Rich console output
        console.print("\n[cyan]PR Verification Results[/cyan]")
        console.print("=" * 60)

        # Display response
        console.print("\n[bold]Verification Report:[/bold]\n")
        console.print(results["response"])

        # Summary footer
        console.print("\n" + "=" * 60)
        if results["duration_ms"]:
            console.print(f"[dim]Duration: {results['duration_ms']}ms[/dim]")
        if results["total_cost_usd"]:
            console.print(f"[dim]Cost: ${results['total_cost_usd']:.4f}[/dim]")
        console.print("=" * 60)


def validate_api_key() -> None:
    """
    Validate that ANTHROPIC_API_KEY is set.

    Raises:
        ValueError: If API key is missing
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable not set. "
            "Please set it before running this script."
        )


def main(
    pr_identifier: str = typer.Argument(..., help="PR number, branch name, or comparison"),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output results in JSON format"
    ),
) -> None:
    """
    Main entry point for PR verification script.

    Args:
        pr_identifier: PR number (e.g., "7"), branch name, or comparison (e.g., "main...feature")
        json_output: If True, output JSON instead of rich formatted text
    """
    # Validate API key
    try:
        validate_api_key()
    except ValueError as e:
        if json_output:
            print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        else:
            console.print(f"[red]ERROR:[/red] {e}", file=sys.stderr)
        raise typer.Exit(code=1)

    # Run verification
    try:
        if not json_output:
            console.print(f"[cyan]Verifying PR:[/cyan] {pr_identifier}\n")

        results = anyio.run(verify_pr, pr_identifier)

        # Format and display results
        output_format = OutputFormat.JSON if json_output else OutputFormat.RICH
        format_output(results, output_format)

    except Exception as e:
        error_msg = f"Verification failed: {str(e)}"
        if json_output:
            print(json.dumps({"error": error_msg}, indent=2), file=sys.stderr)
        else:
            console.print(f"[red]ERROR:[/red] {error_msg}", file=sys.stderr)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
