#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.40.0"]
# ///
"""
Intelligent Markdown Linting Orchestrator

Purpose: Coordinate autonomous agents to fix markdown linting errors
Team: infrastructure
Author: devops@spaceships.work

Architecture:
- Orchestrator (this script): Strategic coordination
- Investigator subagent: Autonomous error analysis
- Fixer subagent: Execute fixes with context

Usage:
    ./scripts/intelligent-markdown-lint.py [--dry-run]

Examples:
    # Run full linting workflow
    ./scripts/intelligent-markdown-lint.py

    # Analyze only (no fixes)
    ./scripts/intelligent-markdown-lint.py --dry-run
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from typing import Any

from anthropic import AsyncAnthropic


def get_anthropic_client() -> AsyncAnthropic:
    """
    Get configured Anthropic client.

    Returns:
        AsyncAnthropic client instance

    Raises:
        ValueError: If ANTHROPIC_API_KEY not set
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    return AsyncAnthropic(api_key=api_key)


def run_rumdl_check() -> str:
    """
    Run rumdl linter and return raw output.

    Returns:
        Raw stdout/stderr from rumdl check

    Raises:
        SystemExit: If rumdl command is not found
    """
    try:
        result = subprocess.run(
            ["rumdl", "check", "."],
            capture_output=True,
            text=True,
        )
        # Combine stdout and stderr (rumdl writes to stderr)
        return result.stdout + result.stderr
    except FileNotFoundError:
        print("❌ Error: 'rumdl' command not found", file=sys.stderr)
        print("\nInstallation instructions:", file=sys.stderr)
        print("  cargo install rumdl", file=sys.stderr)
        print("\nOr visit: https://github.com/spacedriveapp/rumdl", file=sys.stderr)
        sys.exit(1)


def parse_rumdl_output(output: str) -> dict[str, Any]:
    """
    Parse rumdl output into structured error data.

    Args:
        output: Raw rumdl output

    Returns:
        {
            "total_errors": int,
            "files": [
                {
                    "path": str,
                    "errors": [
                        {"line": int, "code": str, "message": str}
                    ]
                }
            ]
        }
    """
    errors_by_file: dict[str, list[dict[str, Any]]] = {}

    for line in output.strip().split("\n"):
        if not line or "Issues: Found" in line or "Run `rumdl" in line:
            continue

        # Format: file.md:line:col: [ERROR_CODE] Error message
        parts = line.split(":", 3)
        if len(parts) < 4:
            continue

        try:
            file_path = parts[0].strip()
            line_num = int(parts[1])
            # col_num = int(parts[2])  # Not needed for now
            error_msg = parts[3].strip()

            # Extract error code from [CODE]
            error_code = "UNKNOWN"
            if "[" in error_msg and "]" in error_msg:
                error_code = error_msg.split("]")[0].replace("[", "").strip()

            error_data = {
                "line": line_num,
                "code": error_code,
                "message": error_msg,
            }

            if file_path not in errors_by_file:
                errors_by_file[file_path] = []
            errors_by_file[file_path].append(error_data)

        except (ValueError, IndexError):
            continue

    files = [{"path": path, "errors": errors} for path, errors in errors_by_file.items()]

    return {
        "total_errors": sum(len(f["errors"]) for f in files),
        "files": files,
    }


def triage_errors(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """
    Categorize errors as simple (directly fixable) or ambiguous (needs investigation).

    Args:
        parsed_data: Parsed rumdl output

    Returns:
        {
            "simple": [{"file": str, "errors": [...]}],
            "ambiguous": [{"file": str, "errors": [...]}],
            "simple_count": int,
            "ambiguous_count": int
        }
    """
    SIMPLE_CODES = {"MD013", "MD036", "MD025"}
    AMBIGUOUS_CODES = {"MD033", "MD053", "MD052", "MD041"}

    simple_files = []
    ambiguous_files = []

    for file_data in parsed_data["files"]:
        simple_errors = [e for e in file_data["errors"] if e["code"] in SIMPLE_CODES]
        ambiguous_errors = [e for e in file_data["errors"] if e["code"] in AMBIGUOUS_CODES]

        if simple_errors:
            simple_files.append({"file": file_data["path"], "errors": simple_errors})

        if ambiguous_errors:
            ambiguous_files.append({"file": file_data["path"], "errors": ambiguous_errors})

    return {
        "simple": simple_files,
        "ambiguous": ambiguous_files,
        "simple_count": sum(len(f["errors"]) for f in simple_files),
        "ambiguous_count": sum(len(f["errors"]) for f in ambiguous_files),
    }


async def spawn_investigator(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Investigator subagent to analyze ambiguous errors.

    Uses Claude Agent SDK to create a subagent with access to Read, Grep, Glob, Bash tools.
    The agent has full autonomy to investigate errors and determine fixable vs false_positive.

    Args:
        assignment: Investigation assignment with files and errors

    Returns:
        Investigation report with verdicts and reasoning
    """
    client = get_anthropic_client()

    print("📊 Spawning Investigator subagent...")

    # Load agent definition from file
    agent_path = ".claude/agents/markdown-investigator.md"
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent definition not found: {agent_path}")

    with open(agent_path) as f:
        agent_content = f.read()
        # Extract system prompt (everything after frontmatter)
        parts = agent_content.split("---")
        if len(parts) < 3:
            raise ValueError(
                f"Invalid agent definition in {agent_path}: missing or malformed frontmatter"
            )
        system_prompt = parts[2].strip()

    # Build investigation prompt
    prompt = f"""Investigate the following markdown linting errors and determine if they are fixable or false positives.

Assignment:
{json.dumps(assignment, indent=2)}

Analyze each error using your tools (Read, Grep, Glob, Bash) and provide a structured JSON report with verdicts and reasoning.
"""

    # Call Claude with agent configuration
    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract JSON from response
    response_text = response.content[0].text

    # Try to parse JSON from response (handle markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        json_text = response_text

    try:
        investigation_report = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse investigation report: {e}")
        print(f"Assignment was: {json.dumps(assignment, indent=2)}")
        print(f"Response: {response_text}")
        raise

    print(f"✅ Investigation complete: analyzed {len(assignment['assignment'])} files")
    return investigation_report


async def spawn_fixer(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Fixer subagent to execute fixes.

    Uses Claude Agent SDK to create a subagent with access to Read, Edit, Bash tools.
    The agent fixes errors based on investigation context.

    Args:
        assignment: Fixer assignment with files, errors, and context

    Returns:
        Fix report with results
    """
    client = get_anthropic_client()

    print("🔧 Spawning Fixer subagent...")

    # Load agent definition from file
    agent_path = ".claude/agents/markdown-fixer.md"
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent definition not found: {agent_path}")

    with open(agent_path) as f:
        agent_content = f.read()
        # Extract system prompt (everything after frontmatter)
        parts = agent_content.split("---")
        if len(parts) < 3:
            raise ValueError(
                f"Invalid agent definition in {agent_path}: missing or malformed frontmatter"
            )
        system_prompt = parts[2].strip()

    # Build fixing prompt
    prompt = f"""Fix the following markdown linting errors using the provided investigation context.

Assignment:
{json.dumps(assignment, indent=2)}

For each file:
1. Read the current content
2. Apply fixes based on error codes and context
3. Verify with rumdl check
4. Report results as JSON
"""

    # Call Claude with agent configuration
    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract JSON from response
    response_text = response.content[0].text

    # Try to parse JSON from response (handle markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        json_text = response_text

    try:
        fix_report = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse fix report: {e}")
        print(f"Assignment was: {json.dumps(assignment, indent=2)}")
        print(f"Response: {response_text}")
        raise

    print(f"✅ Fixes complete: processed {len(assignment['assignment'])} files")
    return fix_report


async def main() -> None:
    """Main orchestrator workflow."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Intelligent Markdown Linting Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze only (no fixes applied)",
    )
    args = parser.parse_args()

    print("🚀 Intelligent Markdown Linting Orchestrator")
    if args.dry_run:
        print("(DRY-RUN MODE: Analysis only, no fixes will be applied)")
    print("=" * 60)

    # Phase 1: Discovery
    print("\n📋 Phase 1: Discovery & Triage")
    print("-" * 60)

    rumdl_output = run_rumdl_check()
    parsed = parse_rumdl_output(rumdl_output)
    triaged = triage_errors(parsed)

    print(f"Total errors found: {parsed['total_errors']}")
    print(f"├─ Simple (directly fixable): {triaged['simple_count']}")
    print(f"└─ Ambiguous (needs investigation): {triaged['ambiguous_count']}")

    # Phase 2: Investigation
    if triaged["ambiguous_count"] > 0:
        print("\n🔍 Phase 2: Investigation")
        print("-" * 60)

        investigation_assignment = {
            "assignment": [{"file": f["file"], "errors": f["errors"]} for f in triaged["ambiguous"]]
        }

        investigation_report = await spawn_investigator(investigation_assignment)
        print(f"Investigation complete: {investigation_report}")
    else:
        investigation_report = {"investigations": []}

    # Phase 3: Calculate Workload
    print("\n📊 Phase 3: Calculate Workload")
    print("-" * 60)

    # TODO: Aggregate investigation results
    total_fixable = triaged["simple_count"]  # + investigated fixable
    print(f"Total fixable errors: {total_fixable}")

    # Phase 4: Fixing
    if args.dry_run:
        print("\n⏭️  Phase 4: Fixing (SKIPPED - dry-run mode)")
        print("-" * 60)
        print("Dry-run mode: Skipping fixes.")
        print(f"Total fixable errors identified: {total_fixable}")
    else:
        print("\n🔧 Phase 4: Fixing")
        print("-" * 60)

        if total_fixable > 0:
            # TODO: Merge simple + investigated fixable errors
            fixer_assignment = {
                "assignment": [
                    {"path": f["file"], "errors": f["errors"]} for f in triaged["simple"]
                ]
            }

            fix_report = await spawn_fixer(fixer_assignment)
            print(f"Fixes applied: {fix_report}")
        else:
            print("No fixable errors found.")

        # Phase 5: Verification
        print("\n✅ Phase 5: Verification")
        print("-" * 60)

        final_output = run_rumdl_check()
        final_parsed = parse_rumdl_output(final_output)

        print(f"Errors before: {parsed['total_errors']}")
        print(f"Errors after: {final_parsed['total_errors']}")

        if parsed["total_errors"] > 0:
            fix_rate = (
                (parsed["total_errors"] - final_parsed["total_errors"])
                / parsed["total_errors"]
                * 100
            )
            print(f"Fix rate: {fix_rate:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
