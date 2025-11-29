#!/usr/bin/env python3
"""
Format skill research by removing UI artifacts and cleaning markdown.

Similar to cleanup_bash_research.py but generic for any skill research.
"""
# /// script
# dependencies = []
# ///

import re
import sys
from pathlib import Path


def clean_github_ui(content: str) -> str:
    """Remove GitHub UI elements from markdown content."""
    # Remove navigation elements
    content = re.sub(r"Skip to content.*?\n", "", content, flags=re.DOTALL)
    content = re.sub(r"\[.*?\]\(#.*?\)\s*\n", "", content)

    # Remove footer/header patterns
    content = re.sub(r"---\s*©.*?\n", "", content)
    content = re.sub(r"GitHub, Inc\.\s*\n", "", content)

    # Remove redundant blank lines (more than 2 consecutive)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content


def format_markdown(content: str) -> str:
    """Apply basic markdown formatting."""
    # Ensure code fences have blank lines
    content = re.sub(r"([^\n])\n```", r"\1\n\n```", content)
    content = re.sub(r"```\n([^\n])", r"```\n\n\1", content)

    # Ensure lists have blank lines (but not between consecutive list items)
    # Use multiline mode to check if previous line was a list item
    # Match: line that doesn't start with list marker, then list marker
    # Don't match: list item followed by list item
    content = re.sub(r"(?m)^(?![*-] )(.+)\n([*-] )", r"\1\n\n\2", content)

    return content


def process_file(file_path: Path) -> None:
    """Process a single markdown file."""
    print(f"Processing: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    # Clean UI artifacts
    content = clean_github_ui(content)

    # Apply formatting
    content = format_markdown(content)

    # Write back
    file_path.write_text(content, encoding="utf-8")
    print(f"✓ Cleaned: {file_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: format_skill_research.py <research-directory>")
        sys.exit(1)

    research_dir = Path(sys.argv[1])

    if not research_dir.exists():
        print(f"Error: Directory not found: {research_dir}")
        sys.exit(1)

    # Process all markdown files
    md_files = list(research_dir.glob("**/*.md"))

    if not md_files:
        print(f"No markdown files found in {research_dir}")
        sys.exit(0)

    print(f"Found {len(md_files)} markdown files to clean")

    for md_file in md_files:
        try:
            process_file(md_file)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            sys.exit(1)

    print(f"\n✓ Formatted {len(md_files)} files in {research_dir}")


if __name__ == "__main__":
    main()
