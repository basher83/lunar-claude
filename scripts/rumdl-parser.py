#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Parse rumdl linting output into structured JSON

Purpose: markdown-linting-automation
Team: infrastructure
Author: devops@spaceships.work

Usage:
    rumdl check . 2>&1 | scripts/rumdl-parser.py [--summary] [--distribute N]

Examples:
    # Summary only (Step 1: Decision making)
    rumdl check . 2>&1 | scripts/rumdl-parser.py --summary

    # Full parsing
    rumdl check . 2>&1 | scripts/rumdl-parser.py

    # Parse and distribute across 6 subagents
    rumdl check . 2>&1 | scripts/rumdl-parser.py --distribute 6

    # Save to file
    rumdl check . 2>&1 | scripts/rumdl-parser.py > analysis.json
"""

import json
import os
import re
import sys
from collections import defaultdict
from typing import Any


def has_yaml_frontmatter(file_path: str) -> bool:
    """
    Check if file starts with YAML frontmatter.

    Args:
        file_path: Path to markdown file

    Returns:
        True if file starts with ---
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, encoding="utf-8") as f:
            first_line = f.readline().strip()
            return first_line == "---"
    except (OSError, UnicodeDecodeError):
        return False


def is_toml_section(line_content: str) -> bool:
    """
    Check if line looks like TOML section header.

    Args:
        line_content: The line content to check

    Returns:
        True if line matches TOML section pattern like [section.name]
    """
    return bool(re.match(r"^\[[\w\.\-]+\]", line_content.strip()))


def categorize_error(error: dict[str, Any], file_path: str) -> str:
    """
    Categorize error as 'fixable' or 'skip' based on context.

    Phase 1 implementation - conservative approach:
    - MD041 (missing H1): Skip if file has YAML frontmatter
    - MD052 (reference not found): Skip if line is TOML section
    - MD013, MD036, MD025: Always fixable
    - Everything else: Skip (conservative)

    Args:
        error: Error dictionary with code, line, column, message
        file_path: Path to the file with the error

    Returns:
        'fixable' or 'skip'
    """
    code = error["code"]

    # MD013 - Line length (always fixable)
    if code == "MD013":
        return "fixable"

    # MD036 - Emphasis instead of heading (always fixable)
    if code == "MD036":
        return "fixable"

    # MD025 - Multiple top-level headings (always fixable)
    if code == "MD025":
        return "fixable"

    # MD041 - Missing H1 (skip if frontmatter)
    if code == "MD041":
        if has_yaml_frontmatter(file_path):
            return "skip"
        return "fixable"

    # MD052 - Reference not found (skip if TOML section)
    if code == "MD052":
        # Extract the reference from message to check if it's TOML
        # Message format: "[MD052] Reference 'changelog' not found"
        match = re.search(r"Reference '([^']+)'", error["message"])
        if match:
            ref_name = match.group(1)
            if is_toml_section(f"[{ref_name}]"):
                return "skip"
        return "fixable"

    # Conservative default: skip everything else
    # (MD033, MD053, and unknown codes)
    return "skip"


def parse_rumdl_line(line: str) -> dict[str, Any] | None:
    """
    Parse a single rumdl output line.

    Format: file.md:line:col: [ERROR_CODE] Error message

    Args:
        line: Single line from rumdl output

    Returns:
        Dictionary with error details or None if not parseable
    """
    if not line or "Issues: Found" in line or "Run `rumdl" in line:
        return None

    parts = line.split(":", 3)
    if len(parts) < 4:
        return None

    try:
        line_num = int(parts[1])
        col_num = int(parts[2])
    except (ValueError, IndexError):
        return None

    error_msg = parts[3].strip()

    # Extract error code from [CODE]
    error_code = "UNKNOWN"
    if "[" in error_msg and "]" in error_msg:
        error_code = error_msg.split("]")[0].replace("[", "").strip()

    return {
        "line": line_num,
        "column": col_num,
        "code": error_code,
        "message": error_msg,
    }


def parse_rumdl_output(rumdl_output: str) -> dict[str, Any]:
    """
    Parse complete rumdl output into structured data.

    Args:
        rumdl_output: Full rumdl check output from stdin

    Returns:
        Dictionary with files and error statistics
    """
    errors_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for line in rumdl_output.strip().split("\n"):
        error_data = parse_rumdl_line(line)
        if error_data:
            file_path = line.split(":")[0].strip()
            # Add categorization to each error
            error_data["category"] = categorize_error(error_data, file_path)
            errors_by_file[file_path].append(error_data)

    # Build structured output with fixable/skip counts
    files = []
    for path, errors in errors_by_file.items():
        fixable_errors = [e for e in errors if e["category"] == "fixable"]
        skip_errors = [e for e in errors if e["category"] == "skip"]

        files.append(
            {
                "path": path,
                "error_count": len(errors),
                "fixable_count": len(fixable_errors),
                "skip_count": len(skip_errors),
                "errors": errors,
            }
        )

    files.sort(key=lambda x: x["fixable_count"], reverse=True)

    return {
        "total_files": len(files),
        "total_errors": sum(f["error_count"] for f in files),
        "total_fixable": sum(f["fixable_count"] for f in files),
        "total_skip": sum(f["skip_count"] for f in files),
        "files": files,
    }


def distribute_files(files: list[dict[str, Any]], num_subagents: int = 6) -> list[dict[str, Any]]:
    """
    Distribute files across subagents to balance FIXABLE error counts.

    Uses greedy algorithm: assign each file to least-loaded subagent
    based on fixable_count (not total error_count).

    Args:
        files: List of file dictionaries with fixable_count
        num_subagents: Number of subagents to create

    Returns:
        List of subagent assignments with files and workload stats
    """
    # Only distribute files that have fixable errors
    fixable_files = [f for f in files if f.get("fixable_count", 0) > 0]

    subagents: list[list[dict[str, Any]]] = [[] for _ in range(num_subagents)]
    workloads = [0] * num_subagents

    # Assign files to least-loaded subagent based on FIXABLE count
    for file_info in fixable_files:
        min_idx = workloads.index(min(workloads))
        subagents[min_idx].append(file_info)
        workloads[min_idx] += file_info.get("fixable_count", 0)

    return [
        {
            "subagent_id": i + 1,
            "file_count": len(files),
            "total_errors": sum(f.get("error_count", 0) for f in files),
            "total_fixable": workload,
            "files": files,
        }
        for i, (files, workload) in enumerate(zip(subagents, workloads, strict=True))
    ]


def main() -> None:
    """Main entry point for rumdl parser."""
    # Parse command-line arguments
    distribute_count = None
    summary_only = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        elif arg == "--summary":
            summary_only = True
            i += 1
        elif arg == "--distribute":
            if i + 1 >= len(sys.argv):
                print("Error: --distribute requires integer argument", file=sys.stderr)
                sys.exit(1)
            try:
                distribute_count = int(sys.argv[i + 1])
            except ValueError:
                print("Error: --distribute requires integer argument", file=sys.stderr)
                sys.exit(1)
            i += 2
        else:
            print(f"Error: Unknown argument: {arg}", file=sys.stderr)
            print(
                "Usage: rumdl check . 2>&1 | scripts/rumdl-parser.py [--summary] [--distribute N]",
                file=sys.stderr,
            )
            sys.exit(1)

    # Read rumdl output from stdin
    try:
        rumdl_output = sys.stdin.read()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)

    if not rumdl_output.strip():
        print("Error: No input received from stdin", file=sys.stderr)
        print("Usage: rumdl check . 2>&1 | scripts/rumdl-parser.py", file=sys.stderr)
        sys.exit(1)

    # Parse the output
    result = parse_rumdl_output(rumdl_output)

    # Add distribution if requested (before stripping, so it has full error details)
    if distribute_count and result["files"]:
        result["distribution"] = distribute_files(result["files"], distribute_count)

    # Summary mode: strip detailed error info from top-level files array only
    # (distribution keeps full details for subagents to use)
    if summary_only:
        result["files"] = [
            {
                "path": f["path"],
                "error_count": f["error_count"],
                "fixable_count": f["fixable_count"],
                "skip_count": f["skip_count"],
            }
            for f in result["files"]
        ]

    # Output JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
