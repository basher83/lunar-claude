#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
#     "pyyaml>=6.0",
# ]
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

import yaml
from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)


def load_agent_definition(path: str) -> AgentDefinition:
    """
    Load agent definition from markdown file with YAML frontmatter.

    Args:
        path: Path to .md file with frontmatter

    Returns:
        AgentDefinition instance

    Raises:
        FileNotFoundError: If agent definition file not found
        ValueError: If agent definition is invalid or missing required fields
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Agent definition not found: {path}")

    with open(path) as f:
        content = f.read()

    # Parse frontmatter (expected format: ---\nYAML\n---\nContent)
    parts = content.split("---")
    if len(parts) < 3:
        raise ValueError(
            f"Invalid agent definition in {path}: "
            "missing or malformed frontmatter (expected: ---\\nYAML\\n---\\nContent)"
        )

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter in {path}: {e}") from e

    # Extract system prompt (everything after second ---)
    system_prompt = parts[2].strip()

    # Validate required fields
    if not frontmatter or "description" not in frontmatter:
        raise ValueError(f"Agent definition in {path} missing required 'description' field")

    # Parse tools - can be comma-separated string or array
    tools_value = frontmatter.get("tools", frontmatter.get("allowedTools", []))
    if isinstance(tools_value, str):
        # Convert comma-separated string to list
        tools = [t.strip() for t in tools_value.split(",")]
    else:
        tools = tools_value

    return AgentDefinition(
        description=frontmatter["description"],
        prompt=system_prompt,
        tools=tools,
        model="inherit",  # Use orchestrator's model
    )


def get_sdk_options() -> ClaudeAgentOptions:
    """
    Create ClaudeAgentOptions with programmatically defined subagents.

    Per SDK best practices, subagents are defined programmatically using
    the agents parameter (not filesystem auto-discovery).

    Returns:
        Configured options for ClaudeSDKClient

    Raises:
        ValueError: If ANTHROPIC_API_KEY not set
        FileNotFoundError: If agent definition files not found
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Load agent definitions from filesystem (for content)
    # but register them programmatically (SDK best practice)
    investigator_def = load_agent_definition(".claude/agents/markdown-investigator.md")
    fixer_def = load_agent_definition(".claude/agents/markdown-fixer.md")

    return ClaudeAgentOptions(
        system_prompt="claude_code",  # Use Claude Code preset with Task tool knowledge
        allowed_tools=["Bash", "Task", "Read", "Write"],  # Orchestrator tools
        permission_mode="acceptEdits",  # Auto-accept file edits
        agents={
            "markdown-investigator": investigator_def,
            "markdown-fixer": fixer_def,
        },
        cwd=os.getcwd(),
        model="claude-sonnet-4-5-20250929",
    )


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
    Spawn Investigator subagent using Claude Agent SDK.

    The SDK handles:
    - Loading agent definition
    - Tool availability (Read, Grep, Glob, Bash)
    - Response parsing and aggregation

    Args:
        assignment: Investigation assignment with files and errors

    Returns:
        Investigation report with verdicts and reasoning
    """
    print("📊 Spawning Investigator subagent...")

    options = get_sdk_options()

    # Build prompt for orchestrator to delegate to investigator
    prompt = f"""Use the 'markdown-investigator' subagent to analyze these markdown linting errors.

The investigator has full autonomy to:
- Read files to examine context
- Search across the repository (Grep, Glob)
- Execute bash commands for complex analysis

Assignment:
{json.dumps(assignment, indent=2)}

The investigator should return a JSON report with:
- Per-file investigations
- Per-error verdicts (fixable or false_positive)
- Reasoning for each determination

Wait for the investigator to complete and return its full report.
"""

    investigation_report = None
    all_response_text = []

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_response():
            # SDK returns structured messages
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text = block.text
                        all_response_text.append(text)

                        # Try multiple JSON extraction strategies
                        json_text = None

                        # Strategy 1: Extract from markdown code block
                        if "```json" in text:
                            json_start = text.find("```json") + 7
                            json_end = text.find("```", json_start)
                            json_text = text[json_start:json_end].strip()
                        # Strategy 2: Extract from plain code block
                        elif "```\n{" in text:
                            json_start = text.find("```\n") + 4
                            json_end = text.find("```", json_start)
                            json_text = text[json_start:json_end].strip()
                        # Strategy 3: Find JSON object in text
                        elif "{" in text and "}" in text:
                            # Find the first { and last }
                            first_brace = text.find("{")
                            last_brace = text.rfind("}")
                            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                                json_text = text[first_brace : last_brace + 1]

                        if json_text:
                            try:
                                investigation_report = json.loads(json_text)
                                break  # Successfully parsed JSON
                            except json.JSONDecodeError as e:
                                print(f"JSON parse error: {e}")
                                print(f"Attempted JSON: {json_text[:200]}...")
                                continue

    if not investigation_report:
        raise RuntimeError("Investigator did not return valid JSON report")

    print(f"✅ Investigation complete: analyzed {len(assignment['assignment'])} files")
    return investigation_report


async def spawn_fixer(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Fixer subagent using Claude Agent SDK.

    The SDK handles:
    - Loading agent definition
    - Tool availability (Read, Edit, Bash)
    - Response parsing and aggregation

    Args:
        assignment: Fixer assignment with files, errors, and context

    Returns:
        Fix report with results
    """
    print("🔧 Spawning Fixer subagent...")

    options = get_sdk_options()

    # Build prompt for orchestrator to delegate to fixer
    prompt = f"""Use the 'markdown-fixer' subagent to fix these markdown errors.

The fixer has access to:
- Read tool (examine current file state)
- Edit tool (apply fixes)
- Bash tool (verify with rumdl check)

Assignment (includes investigation context):
{json.dumps(assignment, indent=2)}

For each file:
1. Read current content
2. Apply fixes based on error codes and investigation context
3. Verify with: rumdl check [filepath]
4. Report results

The fixer should return a JSON report with:
- Per-file fix results
- Errors before/after counts
- Verification status

Wait for the fixer to complete and return its full report.
"""

    fix_report = None
    all_response_text = []

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text = block.text
                        all_response_text.append(text)

                        # Try multiple JSON extraction strategies
                        json_text = None

                        # Strategy 1: Extract from markdown code block
                        if "```json" in text:
                            json_start = text.find("```json") + 7
                            json_end = text.find("```", json_start)
                            json_text = text[json_start:json_end].strip()
                        # Strategy 2: Extract from plain code block
                        elif "```\n{" in text:
                            json_start = text.find("```\n") + 4
                            json_end = text.find("```", json_start)
                            json_text = text[json_start:json_end].strip()
                        # Strategy 3: Find JSON object in text
                        elif "{" in text and "}" in text:
                            first_brace = text.find("{")
                            last_brace = text.rfind("}")
                            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                                json_text = text[first_brace : last_brace + 1]

                        if json_text:
                            try:
                                fix_report = json.loads(json_text)
                                break  # Successfully parsed JSON
                            except json.JSONDecodeError as e:
                                print(f"JSON parse error: {e}")
                                print(f"Attempted JSON: {json_text[:200]}...")
                                continue

    if not fix_report:
        raise RuntimeError("Fixer did not return valid JSON report")

    print(f"✅ Fixes complete: processed {len(assignment['assignment'])} files")
    return fix_report


def aggregate_investigation_results(
    simple_files: list[dict[str, Any]],
    investigation_report: dict[str, Any],
) -> dict[str, Any]:
    """
    Aggregate simple errors and investigation results into single Fixer assignment.

    Args:
        simple_files: Files with simple (directly fixable) errors
        investigation_report: Investigator's verdict report

    Returns:
        {
            "assignment": [
                {
                    "path": str,
                    "errors": [
                        {
                            "line": int,
                            "code": str,
                            "message": str,
                            "context": str  # Investigation reasoning or "Always fixable"
                        }
                    ]
                }
            ],
            "stats": {
                "simple_errors": int,
                "investigated_fixable": int,
                "total_fixable": int,
                "false_positives": int
            }
        }
    """
    # Start with simple errors (add context)
    fixer_files = {}

    for file_data in simple_files:
        path = file_data["file"]
        fixer_files[path] = {
            "path": path,
            "errors": [
                {**error, "context": f"Simple error - always fixable (code: {error['code']})"}
                for error in file_data["errors"]
            ],
        }

    # Add investigated errors that are fixable
    investigated_fixable = 0
    false_positives = 0

    for investigation in investigation_report.get("investigations", []):
        file_path = investigation["file"]

        for result in investigation.get("results", []):
            if result["verdict"] == "fixable":
                investigated_fixable += 1

                # Add to fixer assignment with investigation context
                if file_path not in fixer_files:
                    fixer_files[file_path] = {"path": file_path, "errors": []}

                fixer_files[file_path]["errors"].append(
                    {**result["error"], "context": result["reasoning"]}
                )

            elif result["verdict"] == "false_positive":
                false_positives += 1

    assignment = list(fixer_files.values())
    simple_errors = sum(len(f["errors"]) for f in simple_files)

    return {
        "assignment": assignment,
        "stats": {
            "simple_errors": simple_errors,
            "investigated_fixable": investigated_fixable,
            "total_fixable": simple_errors + investigated_fixable,
            "false_positives": false_positives,
        },
    }


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

    aggregated = aggregate_investigation_results(triaged["simple"], investigation_report)

    stats = aggregated["stats"]
    print(f"Simple errors: {stats['simple_errors']}")
    print(f"Investigated fixable: {stats['investigated_fixable']}")
    print(f"False positives preserved: {stats['false_positives']}")
    print(f"Total fixable: {stats['total_fixable']}")

    # Phase 4: Fixing
    if args.dry_run:
        print("\n⏭️  Phase 4: Fixing (SKIPPED - dry-run mode)")
        print("-" * 60)
        print("Dry-run mode: Skipping fixes.")
        print(f"Total fixable errors identified: {stats['total_fixable']}")
    else:
        print("\n🔧 Phase 4: Fixing")
        print("-" * 60)

        if stats["total_fixable"] > 0:
            fix_report = await spawn_fixer(aggregated)

            total_fixed = sum(r["fixed"] for r in fix_report["results"])
            print(f"✅ Fixed {total_fixed} errors across {len(fix_report['results'])} files")
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
