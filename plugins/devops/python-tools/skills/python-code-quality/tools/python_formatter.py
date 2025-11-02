#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Python formatter for Claude Code.
Automatically formats and fixes Python files using ruff.

Usage:
    Hook mode (stdin): echo '{"tool_input":{"file_path":"test.py"}}' | python python_formatter.py
    CLI mode: python python_formatter.py test.py
    Blocking mode: python python_formatter.py --blocking test.py

Options:
    --blocking    Exit with code 2 when changes are made (sends feedback to Claude)
                  Default: Exit with code 0 (output only in transcript mode)

Features:
    - Dual mode: Works with Claude Code hooks (stdin) or command-line arguments
    - Auto-formats code with ruff format
    - Auto-fixes linting issues with ruff check --fix
    - Only processes .py files
    - Reports what was changed
    - Blocking mode option for immediate Claude feedback
"""

import json
import os
import subprocess
import sys


def format_python_file(file_path: str, blocking: bool = False) -> bool:
    """Format and fix a Python file using ruff.

    Args:
        file_path: Path to the Python file to format
        blocking: If True, output to stderr for blocking behavior

    Returns:
        bool: True if changes were made, False otherwise
    """
    changes_made = []

    try:
        # Run ruff format
        format_result = subprocess.run(
            ["ruff", "format", file_path], capture_output=True, text=True, timeout=30
        )

        # Check if formatting made changes
        # ruff format returns 0 whether changes were made or not
        # but outputs "1 file reformatted" vs "1 file left unchanged"
        output = (format_result.stdout + format_result.stderr).lower()
        if "reformatted" in output:
            changes_made.append("formatted code style")

        # Run ruff check --fix to auto-fix linting issues
        fix_result = subprocess.run(
            ["ruff", "check", "--fix", file_path], capture_output=True, text=True, timeout=30
        )

        # Check if fixes were applied
        if fix_result.stdout and "fixed" in fix_result.stdout.lower():
            changes_made.append("fixed linting issues")

        # Report results
        if changes_made:
            message = f"✓ Python formatter: {', '.join(changes_made)} in {file_path}"
            if blocking:
                print(message, file=sys.stderr)
            else:
                print(message)
            return True

        return False

    except subprocess.TimeoutExpired:
        print(f"⚠ Ruff timed out for {file_path}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("⚠ Ruff not found. Install with: uv tool install ruff", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error running ruff: {e}", file=sys.stderr)
        return False


# Main execution
try:
    # Parse arguments
    blocking = False
    file_path = ""

    # Check for --blocking flag and file path
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if "--blocking" in args:
            blocking = True
            args.remove("--blocking")
        if args:
            file_path = args[0]
    else:
        # Read from stdin (hook mode)
        input_data = json.load(sys.stdin)
        file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith(".py"):
        sys.exit(0)  # Not a Python file

    if os.path.exists(file_path):
        changes_made = format_python_file(file_path, blocking=blocking)

        # In blocking mode, exit with code 2 if changes were made
        if blocking and changes_made:
            sys.exit(2)
    else:
        print(f"⚠ File not found: {file_path}", file=sys.stderr)

    # Always exit 0 to be non-blocking (unless blocking mode with changes)
    sys.exit(0)

except Exception as e:
    print(f"Error in Python formatter: {e}", file=sys.stderr)
    sys.exit(0)  # Non-blocking even on errors
