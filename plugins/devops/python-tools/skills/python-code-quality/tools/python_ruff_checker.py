#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Ruff checker for Claude Code Python files.
Automatically runs ruff check on Python files after edits.

Usage:
    Hook mode (stdin): echo '{"tool_input":{"file_path":"test.py"}}' | python python_ruff_checker.py
    CLI mode: python python_ruff_checker.py test.py

Features:
    - Dual mode: Works with Claude Code hooks (stdin) or command-line arguments
    - Only processes .py files
    - Provides feedback on code quality issues
    - Non-blocking (exits with code 0 even if ruff finds issues)
"""
import json
import os
import subprocess
import sys


def check_python_file(file_path):
    """Run ruff check on a Python file."""
    try:
        result = subprocess.run(
            ["ruff", "check", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"✓ Ruff check passed: {file_path}")
        else:
            print(f"⚠ Ruff found issues in {file_path}:")
            if result.stdout:
                print(result.stdout)

    except subprocess.TimeoutExpired:
        print(f"⚠ Ruff check timed out for {file_path}", file=sys.stderr)
    except FileNotFoundError:
        print("⚠ Ruff not found. Install with: uv tool install ruff", file=sys.stderr)
    except Exception as e:
        print(f"Error running ruff: {e}", file=sys.stderr)


# Main execution
try:
    # Check if file path provided as command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Read from stdin (hook mode)
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')

    if not file_path.endswith('.py'):
        sys.exit(0)  # Not a Python file

    if os.path.exists(file_path):
        check_python_file(file_path)
    else:
        print(f"⚠ File not found: {file_path}", file=sys.stderr)

    # Always exit 0 to be non-blocking
    sys.exit(0)

except Exception as e:
    print(f"Error in ruff checker: {e}", file=sys.stderr)
    sys.exit(0)  # Non-blocking even on errors
