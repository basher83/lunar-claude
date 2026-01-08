#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Cleanup script for bash-best-practices-research.md
Removes GitHub UI clutter, redundant metadata, and formatting issues
while preserving all technical content.
"""

import re
from pathlib import Path


def remove_github_ui_elements(text: str) -> str:
    """Remove GitHub UI navigation elements."""
    # Remove "Skip to content" links
    text = re.sub(r"\[Skip to content\]\([^\)]+\)\n\n?", "", text)

    # Remove "You signed in/out" messages (all on one line)
    text = re.sub(
        r"You signed in with another tab or window\. \[Reload\]\([^\)]+\) to refresh your session\."
        r"You signed out in another tab or window\. \[Reload\]\([^\)]+\) to refresh your session\."
        r"You switched accounts on another tab or window\. \[Reload\]\([^\)]+\) to refresh your session\."
        r"Dismiss alert\n\n?",
        "",
        text,
    )

    # Remove {{ message }} placeholders
    text = re.sub(r"\{\{ message \}\}\n\n?", "", text)

    # Remove repository header lines like "[user]/ **[repo]** Public"
    text = re.sub(r"\[[^\]]+\]\([^\)]+\)/ \*\*\[[^\]]+\]\([^\)]+\)\*\* Public\n\n?", "", text)

    # Remove Notifications links (with or without dashes, standalone or in lists)
    text = re.sub(
        r"^\[Notifications\]\([^\)]+\) You must be signed in to change notification settings\n\n?",
        "",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"- \[Notifications\]\([^\)]+\) You must be signed in to change notification settings\n\n?",
        "",
        text,
    )

    # Remove Fork/Star links with line breaks
    text = re.sub(r"- \[Fork\\\\\n\d+\]\([^\)]+\)\n", "", text)
    text = re.sub(r"- \[Star\\\\\n\d+\]\([^\)]+\)\n", "", text)

    # Remove "Go to file", "Code", "Open more actions menu" text
    text = re.sub(r"Go to file\n\nCode\n\nOpen more actions menu\n\n?", "", text)

    # Remove branch/tag navigation (no newline between links)
    text = re.sub(r"\[Go to Branches page\]\([^\)]+\)\[Go to Tags page\]\([^\)]+\)\n\n?", "", text)

    return text


def remove_redundant_metadata(text: str) -> str:
    """Remove redundant metadata sections."""
    # Remove Stars sections
    text = re.sub(r"### Stars\n\n\[?\*\*?\d+\*\*?\\\\\nstars\]\([^\)]+\)\n\n", "", text)

    # Remove Watchers sections
    text = re.sub(r"### Watchers\n\n\[?\*\*?\d+\*\*?\\\\\nwatching\]\([^\)]+\)\n\n", "", text)

    # Remove Forks sections
    text = re.sub(r"### Forks\n\n\[?\*\*?\d+\*\*?\\\\\nforks\]\([^\)]+\)\n\n?", "", text)

    # Remove Contributors sections with avatars (multiline pattern)
    text = re.sub(
        r"## \[Contributors[^\]]+\]\([^\)]+\)\n\n(?:- \[!\[@[^\]]+\]\([^\)]+\)\]\([^\)]+\)\[[^\]]+\]\([^\)]+\)\n?)+",
        "",
        text,
    )

    # Remove Languages sections
    text = re.sub(r"## Languages\n\n- \[Shell[^\]]+\]\([^\)]+\)\n\n", "", text)

    # Remove "Uh oh!" error messages
    text = re.sub(
        r"### Uh oh!\n\nThere was an error while loading\. \[Please reload this page\]\([^\)]+\)\.\n\n",
        "",
        text,
    )

    # Remove "You can't perform that action at this time." messages
    text = re.sub(r"You can't perform that action at this time\.\n\n", "", text)

    # Remove repository stats lines (stars/forks/branches/tags/activity) with line breaks
    text = re.sub(
        r"\[\d+\\\\\nstars\]\([^\)]+\) \[\d+\\\\\nforks\]\([^\)]+\) \[Branches\]\([^\)]+\) \[Tags\]\([^\)]+\) \[Activity\]\([^\)]+\)\n\n",
        "",
        text,
    )

    # Remove standalone Star/Notifications links
    text = re.sub(r"\[Star\]\([^\)]+\)\n\n", "", text)

    # Remove duplicate "About" sections that are just metadata (more flexible pattern)
    # Match About section followed by Topics/Resources/License
    text = re.sub(
        r"## About\n\n[^\n]+\n\n\n### Topics\n\n[^\n]+\n\n### Resources\n\n\[Readme\]\([^\)]+\)\n\n### License\n\n\[[^\]]+\]\([^\)]+\)\n\n",
        "",
        text,
    )

    # Remove About sections at the end with just description
    text = re.sub(
        r"## About\n\n[^\n]+\n\n\n### Topics\n\n[^\n]+\n\n### Resources\n\n[^\n]+\n\n### License\n\n[^\n]+\n\n### Contributing\n\n[^\n]+\n\n",
        "",
        text,
    )

    return text


def remove_repository_navigation(text: str) -> str:
    """Remove repository navigation elements."""
    # Remove "Folders and files" tables (multiline pattern with DOTALL)
    # Match the entire table including all rows
    text = re.sub(
        r"## Folders and files\n\n\| Name \| Name \| Last commit message \| Last commit date \|\n\| --- \| --- \| --- \| --- \|\n.*?\| View all files \|\n\n",
        "",
        text,
        flags=re.DOTALL,
    )

    # Remove "Repository files navigation" sections
    text = re.sub(r"## Repository files navigation\n\n", "", text)

    # Remove repository title headers like "# user/repo" or "# repo-name"
    # But keep main section headers - be careful here
    # Only remove if it's a standalone repo name header (not part of content)
    text = re.sub(
        r"^# [a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+\n\n(main|master)\n\n", "", text, flags=re.MULTILINE
    )

    # Remove standalone repo name headers (like "# bash-script-template")
    # Only if they appear alone with blank lines around them and are simple repo names
    # Be careful not to remove actual content headers
    text = re.sub(r"\n\n# [a-z0-9-]+\n\n", "\n\n", text)

    # Remove branch/tag counts with links
    text = re.sub(
        r"\[?\*\*\d+\*\* Branches\]\([^\)]+\) \[?\*\*\d+\*\* Tags\]\([^\)]+\)\n\n", "", text
    )

    # Remove standalone "main" or "master" branch indicators (with blank lines)
    text = re.sub(r"^(main|master)\n\n", "", text, flags=re.MULTILINE)

    return text


def clean_permalinks(text: str) -> str:
    """Remove or simplify permalink references."""
    # Remove standalone permalink lines (with blank lines before/after)
    text = re.sub(r"\n\n\[Permalink: [^\]]+\]\([^\)]+\)\n\n", "\n\n", text)

    # Remove permalink lines at start of sections
    text = re.sub(r"^\[Permalink: [^\]]+\]\([^\)]+\)\n\n", "", text, flags=re.MULTILINE)

    # Remove permalink lines that appear right after headings (standalone)
    # Match heading, then permalink on next line(s)
    text = re.sub(
        r"(\n#{1,6} .+?\n\n)\[Permalink: [^\]]+\]\([^\)]+\)\n\n", r"\1", text, flags=re.DOTALL
    )

    # Remove permalink lines that appear right after headings (no blank line between)
    text = re.sub(
        r"(\n#{1,6} .+?\n)\[Permalink: [^\]]+\]\([^\)]+\)\n", r"\1", text, flags=re.DOTALL
    )

    # Remove inline permalinks that are standalone (with trailing backslash)
    # Handle both with and without newline after backslash
    text = re.sub(r"\[Permalink: [^\]]+\]\([^\)]+\)\\\n?", "", text)

    # Also remove permalinks with backslash that appear on their own line
    text = re.sub(r"\n\[Permalink: [^\]]+\]\([^\)]+\)\\\n", "\n", text)

    # Remove permalinks that appear on their own line (not part of a sentence)
    text = re.sub(r"\n\[Permalink: [^\]]+\]\([^\)]+\)\n", "\n", text)

    return text


def clean_html_artifacts(text: str) -> str:
    """Remove HTML artifacts and broken formatting."""
    # Remove HTML-like tags that shouldn't be in markdown
    text = re.sub(r"<br>", "\n", text)
    text = re.sub(r"<br/>", "\n", text)

    # Clean up excessive newlines (more than 2 consecutive)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # Clean up lines with just backslashes (from broken markdown)
    text = re.sub(r"^\\\\\n$", "", text, flags=re.MULTILINE)

    return text


def remove_duplicate_license_sections(text: str) -> str:
    """Remove duplicate license sections that appear multiple times."""
    # This is tricky - we want to keep license info in the main content
    # but remove it from redundant "About" sections
    # We'll handle this more carefully by context

    # Remove license sections that appear right before "About" sections
    text = re.sub(r"### License\n\n\[MIT license\]\([^\)]+\)\n\n## About\n", "## About\n", text)

    return text


def fix_code_blocks(text: str) -> str:
    """Ensure code blocks are properly formatted."""
    # Fix code blocks that might be missing language tags
    # This is a conservative fix - we'll preserve existing formatting

    # Ensure triple backticks are on their own lines
    text = re.sub(r"```([^\n]+)\n", r"```\1\n", text)

    return text


def cleanup_document(file_path: Path) -> None:
    """Main cleanup function."""
    print(f"Reading {file_path}...")
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    original_length = len(content)
    print(f"Original length: {original_length} characters")

    # Apply cleanup functions
    print("Removing GitHub UI elements...")
    content = remove_github_ui_elements(content)

    print("Removing redundant metadata...")
    content = remove_redundant_metadata(content)

    print("Removing repository navigation...")
    content = remove_repository_navigation(content)

    print("Cleaning permalinks...")
    content = clean_permalinks(content)

    print("Cleaning HTML artifacts...")
    content = clean_html_artifacts(content)

    print("Removing duplicate sections...")
    content = remove_duplicate_license_sections(content)

    print("Fixing code blocks...")
    content = fix_code_blocks(content)

    # Final cleanup: remove excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    # Clean up trailing whitespace
    lines = content.split("\n")
    content = "\n".join(line.rstrip() for line in lines)

    final_length = len(content)
    reduction = original_length - final_length
    reduction_pct = (reduction / original_length) * 100

    print(f"\nFinal length: {final_length} characters")
    print(f"Reduction: {reduction} characters ({reduction_pct:.1f}%)")

    # Write cleaned content
    print(f"\nWriting cleaned content to {file_path}...")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Done!")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    doc_path = repo_root / "docs" / "research" / "bash" / "bash-best-practices-research.md"

    cleanup_document(doc_path)
