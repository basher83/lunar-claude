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

import asyncio
import json
import subprocess
from typing import Any


def run_rumdl_check() -> str:
    """
    Run rumdl linter and return raw output.

    Returns:
        Raw stdout/stderr from rumdl check
    """
    result = subprocess.run(
        ["rumdl", "check", "."],
        capture_output=True,
        text=True,
    )
    # Combine stdout and stderr (rumdl writes to stderr)
    return result.stdout + result.stderr


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

    Args:
        assignment: Investigation assignment with files and errors

    Returns:
        Investigation report with verdicts and reasoning
    """
    # TODO: Implement Claude Agent SDK subagent spawn
    # For now, return mock data
    print("📊 Spawning Investigator subagent...")
    print(f"Assignment: {json.dumps(assignment, indent=2)}")

    # Mock response
    return {
        "investigations": [
            {
                "file": assignment["assignment"][0]["file"],
                "results": [
                    {
                        "error": assignment["assignment"][0]["errors"][0],
                        "verdict": "fixable",
                        "reasoning": "Mock investigation result",
                    }
                ],
            }
        ]
    }


async def spawn_fixer(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Fixer subagent to execute fixes.

    Args:
        assignment: Fixer assignment with files, errors, and context

    Returns:
        Fix report with results
    """
    # TODO: Implement Claude Agent SDK subagent spawn
    # For now, return mock data
    print("🔧 Spawning Fixer subagent...")
    print(f"Assignment: {json.dumps(assignment, indent=2)}")

    # Mock response
    return {
        "results": [
            {
                "path": assignment["assignment"][0]["path"],
                "fixed": len(assignment["assignment"][0]["errors"]),
                "errors_before": len(assignment["assignment"][0]["errors"]),
                "errors_after": 0,
                "verification": "PASSED (mock)",
            }
        ]
    }


async def main() -> None:
    """Main orchestrator workflow."""
    print("🚀 Intelligent Markdown Linting Orchestrator")
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
    print("\n🔧 Phase 4: Fixing")
    print("-" * 60)

    if total_fixable > 0:
        # TODO: Merge simple + investigated fixable errors
        fixer_assignment = {
            "assignment": [{"path": f["file"], "errors": f["errors"]} for f in triaged["simple"]]
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
            (parsed["total_errors"] - final_parsed["total_errors"]) / parsed["total_errors"] * 100
        )
        print(f"Fix rate: {fix_rate:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
