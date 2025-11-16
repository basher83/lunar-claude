#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "firecrawl-py>=1.0.0",
#   "typer>=0.12.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Scrape a single URL using Firecrawl and save as markdown.

Generic URL scraper that fetches web content and converts it to clean markdown.
Useful for downloading documentation, articles, or any web page content.

Usage:
    export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"

    # Scrape a URL to default location (ai_docs/scraped-content.md)
    scripts/firecrawl_scrape_url.py "https://docs.example.com/guide"

    # Specify custom output path
    scripts/firecrawl_scrape_url.py "https://example.com" --output docs/example.md

    # Include full page (headers, footers, navigation)
    scripts/firecrawl_scrape_url.py "https://example.com" --full-page

    # Scrape with custom options
    scripts/firecrawl_scrape_url.py "https://example.com" --wait-for 2000 --timeout 60000
"""

import os
import sys
from pathlib import Path

import typer
from firecrawl import Firecrawl
from rich.console import Console

console = Console()


def get_api_key() -> str:
    """Get Firecrawl API key from environment or exit."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        console.print("[red]Error: FIRECRAWL_API_KEY environment variable not set[/red]")
        console.print("Set it with: export FIRECRAWL_API_KEY='fc-your-api-key'")
        sys.exit(1)
    return api_key


def scrape_url(
    api_key: str,
    url: str,
    only_main_content: bool = True,
    wait_for: int | None = None,
    timeout: int | None = None,
) -> str:
    """
    Scrape a URL using Firecrawl API.

    Args:
        api_key: Firecrawl API key
        url: URL to scrape
        only_main_content: If True, exclude navigation/headers/footers
        wait_for: Milliseconds to wait for page to load
        timeout: Request timeout in milliseconds

    Returns:
        Markdown content of the page

    Raises:
        SystemExit: If scraping fails
    """
    try:
        firecrawl = Firecrawl(api_key=api_key)
        console.print(f"[cyan]Scraping:[/cyan] {url}")

        # Build scrape options
        scrape_options = {
            "formats": ["markdown"],
            "only_main_content": only_main_content,
        }
        if wait_for is not None:
            scrape_options["wait_for"] = wait_for
        if timeout is not None:
            scrape_options["timeout"] = timeout

        # Scrape the page
        result = firecrawl.scrape(url, **scrape_options)

        if not result:
            console.print("[red]Error: Empty response from Firecrawl[/red]")
            sys.exit(1)

        # Access markdown attribute from Document object
        markdown = getattr(result, "markdown", None)

        if not markdown:
            console.print("[red]Error: Could not extract markdown from response[/red]")
            console.print(f"[dim]Available attributes: {dir(result)}[/dim]")
            sys.exit(1)

        return markdown

    except Exception as e:
        console.print(f"[red]Error: Failed to scrape page: {e}[/red]")
        import traceback

        traceback.print_exc()
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
        console.print(f"[green]✓ Saved to:[/green] {output_path}")
        console.print(f"[dim]Characters: {len(content):,}[/dim]")

    except Exception as e:
        console.print(f"[red]Error: Failed to write file: {e}[/red]")
        sys.exit(1)


def main(
    url: str = typer.Argument(..., help="URL to scrape"),
    output: str = typer.Option(
        "ai_docs/scraped-content.md",
        "--output",
        "-o",
        help="Output markdown file path",
    ),
    full_page: bool = typer.Option(
        False,
        "--full-page",
        "-f",
        help="Include full page content (headers, footers, navigation)",
    ),
    wait_for: int | None = typer.Option(
        None,
        "--wait-for",
        "-w",
        help="Milliseconds to wait for page to load before scraping",
    ),
    timeout: int | None = typer.Option(
        None,
        "--timeout",
        "-t",
        help="Request timeout in milliseconds",
    ),
):
    """
    Scrape a single URL using Firecrawl and save as markdown.

    Examples:
        # Scrape documentation page
        scripts/firecrawl_scrape_url.py "https://docs.example.com/guide"

        # Scrape to custom location
        scripts/firecrawl_scrape_url.py "https://example.com" -o docs/page.md

        # Include full page content
        scripts/firecrawl_scrape_url.py "https://example.com" --full-page

        # Wait for dynamic content to load
        scripts/firecrawl_scrape_url.py "https://spa.example.com" --wait-for 3000
    """
    output_path = Path(output)

    # Get API key
    api_key = get_api_key()

    # Scrape URL
    only_main_content = not full_page
    markdown = scrape_url(
        api_key,
        url,
        only_main_content=only_main_content,
        wait_for=wait_for,
        timeout=timeout,
    )

    # Save to file
    save_markdown(markdown, output_path, url)

    console.print(f"[green]✓ Successfully scraped {len(markdown):,} characters[/green]")


if __name__ == "__main__":
    typer.run(main)
