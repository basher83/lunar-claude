#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.

Usage:
    Hook mode (stdin): echo '{"tool_input":{"file_path":"test.md"}}' | python markdown_formatter.py
    CLI mode: python markdown_formatter.py test.md
    CLI mode (multiple files): python markdown_formatter.py file1.md file2.md
    Blocking mode: python markdown_formatter.py --blocking test.md

Options:
    --blocking    Exit with code 2 when changes are made (sends feedback to Claude)
                  Default: Exit with code 0 (output only in transcript mode)

Features:
    - Dual mode: Works with Claude Code hooks (stdin) or command-line arguments
    - Blocking mode option for immediate Claude feedback
    - Detects programming languages in unlabeled code fences
    - Adds appropriate language identifiers (python, json, bash, etc.)
    - Normalizes excessive blank lines
    - Preserves code content integrity
"""

import json
import os
import re
import sys


def detect_language(code: str) -> str:
    """Best-effort language detection from code content."""
    s = code.strip()

    # JSON detection
    if re.search(r"^\s*[{\[]", s):
        try:
            json.loads(s)
            return "json"
        except json.JSONDecodeError:
            pass

    # Python detection
    if re.search(r"^\s*def\s+\w+\s*\(", s, re.M) or re.search(r"^\s*(import|from)\s+\w+", s, re.M):
        return "python"

    # JavaScript detection
    if re.search(r"\b(function\s+\w+\s*\(|const\s+\w+\s*=)", s) or re.search(
        r"=>|console\.(log|error)", s
    ):
        return "javascript"

    # Bash detection
    if re.search(r"^#!.*\b(bash|sh)\b", s, re.M) or re.search(
        r"\b(if|then|fi|for|in|do|done)\b", s
    ):
        return "bash"

    # SQL detection
    if re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+", s, re.I):
        return "sql"

    return "text"


def format_markdown(content: str) -> str:
    """Format markdown content with language detection."""

    # Fix unlabeled code fences
    def add_lang_to_fence(match: re.Match[str]) -> str:
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)

    fence_pattern = r"(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$"
    content = re.sub(fence_pattern, add_lang_to_fence, content)

    # Fix excessive blank lines (only outside code fences)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.rstrip() + "\n"


# Main execution
try:
    # Parse arguments
    blocking = False
    file_paths = []

    if len(sys.argv) > 1:
        # CLI mode: parse arguments
        args = sys.argv[1:]
        if "--blocking" in args:
            blocking = True
            args.remove("--blocking")
        file_paths = args
    else:
        # Hook mode: Read from stdin
        try:
            input_data = json.load(sys.stdin)
            file_path = input_data.get("tool_input", {}).get("file_path", "")
            if file_path:
                file_paths = [file_path]
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input from stdin: {e}", file=sys.stderr)
            sys.exit(0)  # Non-blocking even on errors

    # Track if any changes were made
    any_changes = False

    # Process each file
    for file_path in file_paths:
        # Skip non-markdown files
        if not file_path.endswith((".md", ".mdx")):
            continue

        if not os.path.exists(file_path):
            print(f"⚠ File not found: {file_path}", file=sys.stderr)
            continue

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            formatted = format_markdown(content)

            if formatted != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(formatted)

                message = f"✓ Fixed markdown formatting in {file_path}"
                if blocking:
                    print(message, file=sys.stderr)
                else:
                    print(message)

                any_changes = True

        except Exception as e:
            print(f"Error formatting {file_path}: {e}", file=sys.stderr)

    # In blocking mode, exit with code 2 if changes were made
    if blocking and any_changes:
        sys.exit(2)

    # Always exit 0 to be non-blocking (unless blocking mode with changes)
    sys.exit(0)

except Exception as e:
    print(f"Error in markdown formatter: {e}", file=sys.stderr)
    sys.exit(0)  # Non-blocking even on errors
