#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "firecrawl-py>=1.0.0",
# ]
# ///
"""
Fetch Claude Code hooks guide using Firecrawl and save as markdown.

This script scrapes the Claude Code hooks guide documentation page
and saves it as a markdown file in the ai_docs/ directory.

Usage:
    export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
    python fetch-hooks-guide.py

Environment Variables:
    FIRECRAWL_API_KEY - Required Firecrawl API key

Output:
    Creates or overwrites ai_docs/hooks-guide.md with the scraped content
"""

import os
import sys
from pathlib import Path

from firecrawl import Firecrawl


def get_env_var(name: str) -> str:
    """Get required environment variable or exit with error."""
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable not set", file=sys.stderr)
        print(f"Set it with: export {name}='your-api-key'", file=sys.stderr)
        sys.exit(1)
    return value


def fetch_hooks_guide(api_key: str, url: str) -> str:
    """
    Fetch hooks guide using Firecrawl API.

    Args:
        api_key: Firecrawl API key
        url: URL to scrape

    Returns:
        Markdown content of the page

    Raises:
        SystemExit: If scraping fails
    """
    try:
        firecrawl = Firecrawl(api_key=api_key)
        print(f"Scraping: {url}", file=sys.stderr)

        # Scrape the page and request markdown format
        # Use only_main_content to exclude navigation/headers/footers
        result = firecrawl.scrape(
            url,
            formats=["markdown"],
            only_main_content=True
        )

        # Result is a Document object (Pydantic model)
        if not result:
            print("Error: Empty response from Firecrawl", file=sys.stderr)
            sys.exit(1)

        # Access markdown attribute directly from Document object
        markdown = getattr(result, "markdown", None)

        if not markdown:
            print(f"Error: Could not extract markdown from Document", file=sys.stderr)
            print(f"Available attributes: {dir(result)}", file=sys.stderr)
            sys.exit(1)

        return markdown

    except Exception as e:
        print(f"Error: Failed to scrape page: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


def save_markdown(content: str, output_path: Path, source_url: str) -> None:
    """
    Save markdown content to file with source attribution.

    Args:
        content: Markdown content to save
        output_path: Path to output file
        source_url: Original URL for attribution

    Raises:
        SystemExit: If writing fails
    """
    try:
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Add source attribution header
        attribution = f"> SOURCE: <{source_url}>\n\n\n"
        full_content = attribution + content

        # Write content
        output_path.write_text(full_content, encoding="utf-8")
        print(f"✓ Saved to: {output_path}", file=sys.stderr)

    except Exception as e:
        print(f"Error: Failed to write file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    # Configuration
    url = "https://docs.claude.com/en/docs/claude-code/hooks-guide"

    # Get script directory and construct output path
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    output_path = repo_root / "ai_docs" / "hooks-guide.md"

    # Get API key from environment
    api_key = get_env_var("FIRECRAWL_API_KEY")

    # Fetch content
    markdown = fetch_hooks_guide(api_key, url)

    # Save to file with source attribution
    save_markdown(markdown, output_path, url)

    print(f"✓ Successfully fetched hooks guide ({len(markdown)} chars)")


if __name__ == "__main__":
    main()
