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
    - Adds appropriate language identifiers (python, yaml, json, bash, etc.)
    - Normalizes excessive blank lines (outside code fences only)
    - Preserves code content integrity
"""

import argparse
import json
import os
import re
import sys


def detect_language(code: str) -> str:
    """
    Detect programming language from code content.

    Checks for language-specific patterns in order of specificity.
    Returns the detected language identifier or 'text' if unknown.

    Detected languages: yaml, toml, json, python, typescript, javascript,
    bash, sql, go, rust, diff, html, xml, css.
    """
    s = code.strip()

    # YAML detection (must come before others - very common in this codebase)
    # Look for key: value patterns, leading dashes for lists, or document markers
    if re.search(r"^---\s*$", s, re.M) or re.search(r"^\w[\w\-]*:\s*[^\{]", s, re.M):
        # Exclude if it looks like JSON (has { or [ at start after stripping)
        if not re.match(r"^\s*[\{\[]", s):
            return "yaml"

    # TOML detection (common for config files)
    # Section headers [section] or [section.subsection], key = value patterns
    if re.search(r"^\[[\w\.\-]+\]\s*$", s, re.M) or re.search(r'^\w+\s*=\s*["\'\[\{]', s, re.M):
        return "toml"

    # JSON detection - must start with { or [ and be valid JSON
    if re.match(r"^\s*[\{\[]", s):
        try:
            json.loads(s)
            return "json"
        except json.JSONDecodeError:
            pass

    # Python detection
    if re.search(r"^\s*def\s+\w+\s*\(", s, re.M) or re.search(r"^\s*(import|from)\s+\w+", s, re.M):
        return "python"
    if re.search(r"^\s*class\s+\w+", s, re.M) or re.search(
        r'if\s+__name__\s*==\s*["\']__main__["\']', s
    ):
        return "python"

    # TypeScript detection (before JavaScript - more specific)
    if re.search(r":\s*(string|number|boolean|any|void)\b", s) or re.search(
        r"\binterface\s+\w+", s
    ):
        return "typescript"

    # JavaScript detection
    if re.search(r"\b(function\s+\w+\s*\(|const\s+\w+\s*=|let\s+\w+\s*=)", s):
        return "javascript"
    if re.search(r"=>\s*[\{\(]|console\.(log|error|warn)\(", s):
        return "javascript"

    # Go detection
    if re.search(r"^package\s+\w+", s, re.M) or re.search(r"^func\s+\w+\s*\(", s, re.M):
        return "go"
    if re.search(r":=\s*\w+|fmt\.(Print|Sprintf)", s):
        return "go"

    # Rust detection
    if re.search(r"^(pub\s+)?fn\s+\w+", s, re.M) or re.search(r"\blet\s+mut\s+\w+", s):
        return "rust"
    if re.search(r"^use\s+\w+::", s, re.M) or re.search(r"impl\s+\w+\s+for", s):
        return "rust"

    # Diff detection
    if re.search(r"^(---|\+\+\+)\s+\S+", s, re.M) and re.search(
        r"^@@\s+-\d+,\d+\s+\+\d+,\d+\s+@@", s, re.M
    ):
        return "diff"

    # Bash detection - be more specific to avoid false positives
    # Require shebang OR multiple shell-specific constructs
    if re.search(r"^#!.*\b(bash|sh|zsh)\b", s, re.M):
        return "bash"
    shell_constructs = [
        r"\$\{?\w+\}?",  # Variable expansion
        r"\becho\s+",  # echo command
        r"\|\s*\w+",  # Pipe to command
        r"&&\s*\w+|;\s*\w+",  # Command chaining
    ]
    if sum(1 for p in shell_constructs if re.search(p, s)) >= 2:
        return "bash"

    # SQL detection
    if re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\s+", s, re.I):
        return "sql"

    # HTML detection
    if re.search(r"<(!DOCTYPE|html|head|body|div|span|p|a|script)\b", s, re.I):
        return "html"

    # XML detection (after HTML)
    if re.search(r"<\?xml\s+version=", s) or re.search(r"<\w+[^>]*xmlns[^>]*>", s):
        return "xml"

    # CSS detection
    if re.search(r"^\s*[\.\#]?\w+\s*\{[^}]*\}", s, re.M):
        return "css"

    return "text"


def format_markdown(content: str) -> str:
    """
    Format markdown content with language detection and spacing fixes.

    Adds language identifiers to unlabeled code fences and normalizes
    excessive blank lines (outside code fences only).
    """
    # Split content into code fence and non-code-fence segments
    fence_pattern = r"(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$"

    segments: list[tuple[str, bool]] = []  # (content, is_code_fence)
    last_end = 0

    for match in re.finditer(fence_pattern, content):
        # Add text before this fence
        if match.start() > last_end:
            segments.append((content[last_end : match.start()], False))

        # Process the fence - add language if missing
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            fence_content = f"{indent}```{lang}\n{body}{closing}\n"
        else:
            fence_content = match.group(0)

        segments.append((fence_content, True))
        last_end = match.end()

    # Add remaining content after last fence
    if last_end < len(content):
        segments.append((content[last_end:], False))

    # Rebuild content, fixing blank lines only in non-fence segments
    result_parts = []
    for segment, is_fence in segments:
        if is_fence:
            result_parts.append(segment)
        else:
            # Fix excessive blank lines only outside code fences
            fixed = re.sub(r"\n{3,}", "\n\n", segment)
            result_parts.append(fixed)

    return "".join(result_parts).rstrip() + "\n"


def parse_args() -> tuple[bool, list[str]]:
    """
    Parse command line arguments or read from stdin for hook mode.

    Returns:
        Tuple of (blocking mode flag, list of file paths to process).
    """
    # Check for hook mode first (no args = read from stdin)
    if len(sys.argv) == 1:
        try:
            input_data = json.load(sys.stdin)
            file_path = input_data.get("tool_input", {}).get("file_path", "")
            return False, [file_path] if file_path else []
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input from stdin: {e}", file=sys.stderr)
            return False, []

    # CLI mode: use argparse
    parser = argparse.ArgumentParser(
        description="Fix missing language tags and spacing issues in markdown files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                    Format single file
  %(prog)s docs/*.md                    Format multiple files
  %(prog)s --blocking README.md         Block and report changes (for hooks)

Hook mode:
  echo '{"tool_input":{"file_path":"test.md"}}' | %(prog)s
""",
    )
    parser.add_argument(
        "files",
        nargs="*",
        metavar="FILE",
        help="Markdown files to format (.md, .mdx)",
    )
    parser.add_argument(
        "--blocking",
        action="store_true",
        help="Exit with code 2 when changes are made (for Claude Code hooks)",
    )

    args = parser.parse_args()
    return args.blocking, args.files


def main() -> int:
    """
    Main entry point for markdown formatter.

    Returns exit code: 0 for success/no changes, 2 for blocking mode with changes.
    """
    blocking, file_paths = parse_args()

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

        except OSError as e:
            print(f"Error reading/writing {file_path}: {e}", file=sys.stderr)
        except UnicodeDecodeError as e:
            print(f"Error decoding {file_path}: {e}", file=sys.stderr)

    # In blocking mode, exit with code 2 if changes were made
    if blocking and any_changes:
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
