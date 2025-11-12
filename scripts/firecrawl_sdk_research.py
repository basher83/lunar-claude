#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "firecrawl-py>=1.0.0",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
# ]
# ///
"""
Firecrawl SDK Research Tool - Search → Scrape → Synthesize

Performs web research using Firecrawl's search and scrape APIs:
1. Search the web for URLs matching your query
2. Scrape content from discovered URLs
3. Combine into a single research markdown document

Usage:
    export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
    ./firecrawl_sdk_research.py "ansible best practices 2025"
    ./firecrawl_sdk_research.py "python async patterns" --limit 5 --output research.md
"""

import asyncio
import os
import sys
from pathlib import Path

import typer
from firecrawl import AsyncFirecrawl
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


async def search_web(query: str, limit: int) -> list[dict]:
    """
    Search the web using Firecrawl's search API.

    Returns list of search results with url, title, description.
    """
    api_key = get_api_key()
    firecrawl = AsyncFirecrawl(api_key=api_key)

    console.print(f"[cyan]Searching:[/cyan] {query}")
    results = await firecrawl.search(query, limit=limit)

    # Results is a SearchData Pydantic object, not a dict
    web_results = results.web if results.web else []
    console.print(f"[green]Found {len(web_results)} results[/green]")

    return [{"url": r.url, "title": r.title, "description": r.description} for r in web_results]


async def scrape_url(firecrawl: AsyncFirecrawl, url: str) -> dict | None:
    """
    Scrape a single URL and return markdown content.

    Returns dict with markdown, title, url or None on failure.
    """
    try:
        result = await firecrawl.scrape(url, formats=["markdown"])

        # Result is a Document object (Pydantic model), not a dict
        markdown = getattr(result, "markdown", "")
        metadata = getattr(result, "metadata", {})
        title = metadata.get("title", url) if isinstance(metadata, dict) else url

        return {"url": url, "title": title, "markdown": markdown}
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to scrape {url}: {e}[/yellow]")
        return None


async def scrape_all(urls: list[str]) -> list[dict]:
    """Scrape all URLs concurrently."""
    api_key = get_api_key()
    firecrawl = AsyncFirecrawl(api_key=api_key)

    console.print(f"[cyan]Scraping {len(urls)} URLs...[/cyan]")

    tasks = [scrape_url(firecrawl, url) for url in urls]
    results = await asyncio.gather(*tasks)

    # Filter out failed scrapes
    successful = [r for r in results if r is not None]
    console.print(f"[green]Successfully scraped {len(successful)}/{len(urls)} URLs[/green]")

    return successful


def combine_results(query: str, search_results: list[dict], scraped_content: list[dict]) -> str:
    """
    Combine search results and scraped content into a research document.
    """
    doc = f"# Research: {query}\n\n"
    doc += f"**Generated:** {Path(__file__).name}\n\n"
    doc += "## Summary\n\n"
    doc += f"Found {len(search_results)} search results, successfully scraped {len(scraped_content)} pages.\n\n"

    # Add table of contents
    doc += "## Sources\n\n"
    for i, result in enumerate(scraped_content, 1):
        doc += f"{i}. [{result['title']}]({result['url']})\n"
    doc += "\n"

    # Add each scraped page
    doc += "## Content\n\n"
    for i, result in enumerate(scraped_content, 1):
        doc += f"### {i}. {result['title']}\n\n"
        doc += f"**Source:** {result['url']}\n\n"
        doc += result["markdown"]
        doc += "\n\n---\n\n"

    return doc


async def research(query: str, limit: int, output_path: Path) -> None:
    """Main research workflow: search → scrape → combine."""

    # Step 1: Search
    search_results = await search_web(query, limit)

    if not search_results:
        console.print("[red]No search results found[/red]")
        sys.exit(1)

    # Step 2: Extract URLs and scrape
    urls = [r["url"] for r in search_results]
    scraped_content = await scrape_all(urls)

    if not scraped_content:
        console.print("[red]Failed to scrape any content[/red]")
        sys.exit(1)

    # Step 3: Combine into research document
    document = combine_results(query, search_results, scraped_content)

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")

    console.print(f"[green]✓ Research saved to:[/green] {output_path}")
    console.print(f"[dim]Total pages: {len(scraped_content)}, Characters: {len(document)}[/dim]")


def main(
    query: str = typer.Argument(..., help="Search query for research"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of search results to scrape"),
    output: str = typer.Option(
        "ai_docs/research.md", "--output", "-o", help="Output markdown file path"
    ),
):
    """
    Research a topic using Firecrawl: search the web, scrape results, and combine into a markdown document.
    """
    output_path = Path(output)

    # Run async research
    asyncio.run(research(query, limit, output_path))


if __name__ == "__main__":
    typer.run(main)
