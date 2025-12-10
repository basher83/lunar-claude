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
1. Search the web for URLs matching your query (with optional category filtering)
2. Scrape content from discovered URLs (combined with search for efficiency)
3. Filter and rank results by quality
4. Combine into a single research markdown document

Usage:
    export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
    scripts/firecrawl_sdk_research.py "ansible proxmox ceph"
    scripts/firecrawl_sdk_research.py "python async patterns" --limit 5 --category github
    scripts/firecrawl_sdk_research.py "machine learning" --category research --output research.md
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

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


async def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """
    Retry a function with exponential backoff.

    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2**attempt)
            console.print(
                f"[yellow]Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}[/yellow]"
            )
            await asyncio.sleep(delay)


async def search_and_scrape(
    query: str,
    limit: int,
    categories: list[str] | None = None,
    scrape_options: dict | None = None,
) -> list[dict]:
    """
    Search the web using Firecrawl's search API with optional scraping.

    Uses search API with scrape_options to combine operations for efficiency.
    Returns list of results with url, title, description, and optionally markdown content.

    Args:
        query: Search query string
        limit: Maximum number of results to return
        categories: Optional list of categories (github, research, pdf)
        scrape_options: Optional dict of scrape options (formats, etc.)
    """
    api_key = get_api_key()
    firecrawl = AsyncFirecrawl(api_key=api_key)

    # Build search parameters
    search_params = {"query": query, "limit": limit}
    if categories:
        search_params["categories"] = categories
    if scrape_options:
        search_params["scrape_options"] = scrape_options

    async def _search():
        return await firecrawl.search(**search_params)

    console.print(f"[cyan]Searching:[/cyan] {query}")
    if categories:
        console.print(f"[dim]Categories: {', '.join(categories)}[/dim]")
    if scrape_options:
        console.print("[dim]Scraping enabled[/dim]")

    results = await retry_with_backoff(_search)

    # When scrape_options are used, results.web contains Document objects
    # Otherwise, results.web contains SearchResult objects
    result_list = []

    web_results = results.web if results.web else []
    console.print(f"[green]Found {len(web_results)} results[/green]")

    for r in web_results:
        # Check if this is a Document object (has markdown attribute) or SearchResult
        has_markdown = hasattr(r, "markdown") and getattr(r, "markdown", None)

        if has_markdown:
            # Document object (from search with scrape_options)
            # URL is in metadata.url or metadata.source_url
            metadata = getattr(r, "metadata", None)
            url = ""
            title = ""
            description = ""

            if metadata:
                # Handle both dict and object metadata types
                # Firecrawl API returns metadata as dict with "url" and "sourceURL" keys
                if isinstance(metadata, dict):
                    url = metadata.get("url", "") or metadata.get("sourceURL", "")
                    title = metadata.get("title", "")
                    description = metadata.get("description", "")
                else:
                    # Fallback for object-like metadata (if SDK changes)
                    url = getattr(metadata, "url", "") or getattr(metadata, "sourceURL", "")
                    title = getattr(metadata, "title", "")
                    description = getattr(metadata, "description", "")

            result_dict = {
                "url": url,
                "title": title,
                "description": description,
                "markdown": getattr(r, "markdown", ""),
            }
            if metadata:
                # Convert metadata to dict if possible
                try:
                    if isinstance(metadata, dict):
                        result_dict["metadata"] = metadata
                    elif hasattr(metadata, "model_dump"):
                        result_dict["metadata"] = metadata.model_dump()
                    else:
                        result_dict["metadata"] = {}
                except (AttributeError, TypeError, ValueError):
                    result_dict["metadata"] = {}
        else:
            # SearchResult object (regular search without scraping)
            result_dict = {
                "url": r.url,
                "title": r.title,
                "description": getattr(r, "description", ""),
            }

        result_list.append(result_dict)

    return result_list


async def scrape_url(firecrawl: AsyncFirecrawl, url: str) -> dict | None:
    """
    Scrape a single URL and return markdown content.

    Returns dict with markdown, title, url, metadata or None on failure.
    """

    async def _scrape():
        return await firecrawl.scrape(url, formats=["markdown"])

    try:
        result = await retry_with_backoff(_scrape)

        # Result is a Document object (Pydantic model), not a dict
        markdown = getattr(result, "markdown", "")
        metadata = getattr(result, "metadata", {})
        title = metadata.get("title", url) if isinstance(metadata, dict) else url

        return {
            "url": url,
            "title": title,
            "markdown": markdown,
            "metadata": metadata if isinstance(metadata, dict) else {},
        }
    except Exception as e:  # noqa: BLE001
        console.print(f"[yellow]Warning: Failed to scrape {url}: {e}[/yellow]")
        return None


def filter_quality(results: list[dict], min_content_length: int = 500) -> list[dict]:
    """
    Filter results by quality indicators.

    Filters out:
    - Results with very short content
    - Error pages
    - Low-quality domains (can be extended)

    Args:
        results: List of result dicts with markdown content
        min_content_length: Minimum content length in characters

    Returns:
        Filtered list of results with quality scores
    """
    filtered = []

    # High-quality domains (prioritize these)
    quality_domains = {
        "github.com",
        "docs.github.com",
        "docs.ansible.com",
        "pve.proxmox.com",
        "docs.ceph.com",
        "ansible.com",
        "proxmox.com",
    }

    for result in results:
        url = result.get("url", "")
        markdown = result.get("markdown", "")
        title = result.get("title", "")

        # Skip if content is too short
        if len(markdown) < min_content_length:
            continue

        # Skip error pages
        if any(
            indicator in title.lower() or indicator in markdown.lower()[:500]
            for indicator in ["404", "not found", "error", "access denied", "forbidden"]
        ):
            continue

        # Calculate quality score
        quality_score = 0
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Boost score for quality domains
        if any(qd in domain for qd in quality_domains):
            quality_score += 10

        # Boost score for GitHub repos
        if "github.com" in domain and "/" in parsed_url.path:
            quality_score += 5

        # Boost score for longer, more detailed content
        if len(markdown) > 2000:
            quality_score += 3
        elif len(markdown) > 1000:
            quality_score += 1

        # Boost score for code blocks (indicates technical content)
        if "```" in markdown:
            quality_score += 2

        result["quality_score"] = quality_score
        result["domain"] = domain
        filtered.append(result)

    # Sort by quality score (highest first)
    filtered.sort(key=lambda x: x.get("quality_score", 0), reverse=True)

    return filtered


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


def combine_results(
    query: str,
    search_results: list[dict],
    scraped_content: list[dict],
    categories: list[str] | None = None,
) -> str:
    """
    Combine search results and scraped content into a research document.

    Args:
        query: Original search query
        search_results: List of search result dicts
        scraped_content: List of scraped content dicts (with markdown)
        categories: Optional list of categories used in search
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    doc = f"# Research: {query}\n\n"

    # Metadata section
    doc += "## Metadata\n\n"
    doc += f"- **Query:** {query}\n"
    doc += f"- **Generated:** {timestamp}\n"
    doc += f"- **Script:** {Path(__file__).name}\n"
    if categories:
        doc += f"- **Categories:** {', '.join(categories)}\n"
    doc += f"- **Search Results:** {len(search_results)}\n"
    doc += f"- **Scraped Pages:** {len(scraped_content)}\n"
    doc += "\n"

    # Summary
    doc += "## Summary\n\n"
    doc += f"Found {len(search_results)} search results, successfully scraped {len(scraped_content)} pages.\n\n"

    # Quality distribution
    if scraped_content and any("quality_score" in r for r in scraped_content):
        high_quality = sum(1 for r in scraped_content if r.get("quality_score", 0) >= 10)
        doc += f"- **High Quality Sources:** {high_quality}/{len(scraped_content)}\n"
    doc += "\n"

    # Add table of contents with quality indicators
    doc += "## Sources\n\n"
    for i, result in enumerate(scraped_content, 1):
        quality_score = result.get("quality_score", 0)
        domain = result.get("domain", "")
        quality_badge = ""
        if quality_score >= 10:
            quality_badge = " ⭐"
        elif quality_score >= 5:
            quality_badge = " ✓"

        doc += f"{i}. [{result['title']}]({result['url']}){quality_badge}\n"
        if domain:
            doc += f"   - Domain: `{domain}`\n"
        if quality_score > 0:
            doc += f"   - Quality Score: {quality_score}\n"
    doc += "\n"

    # Add each scraped page
    doc += "## Content\n\n"
    for i, result in enumerate(scraped_content, 1):
        quality_score = result.get("quality_score", 0)
        domain = result.get("domain", "")

        doc += f"### {i}. {result['title']}\n\n"
        doc += f"**Source:** [{result['url']}]({result['url']})\n"
        if domain:
            doc += f"**Domain:** `{domain}`\n"
        if quality_score > 0:
            doc += f"**Quality Score:** {quality_score}\n"
        doc += "\n"

        # Add description if available
        description = result.get("description", "")
        if description:
            doc += f"*{description}*\n\n"

        doc += result.get("markdown", "")
        doc += "\n\n---\n\n"

    return doc


async def research(
    query: str,
    limit: int,
    output_path: Path,
    categories: list[str] | None = None,
) -> None:
    """
    Main research workflow: search → scrape → filter → combine.

    Uses combined search+scrape API for efficiency when possible.
    """
    # Use combined search+scrape API for efficiency
    scrape_options = {"formats": ["markdown"]}

    # Step 1: Search and scrape in one call
    search_results = await search_and_scrape(
        query=query,
        limit=limit,
        categories=categories,
        scrape_options=scrape_options,
    )

    if not search_results:
        console.print("[red]No search results found[/red]")
        sys.exit(1)

    # Step 2: Check if we already have markdown content from search+scrape
    has_content = any(r.get("markdown") for r in search_results)

    if has_content:
        # Content already scraped, just filter
        console.print("[cyan]Content already scraped, filtering by quality...[/cyan]")
        scraped_content = [r for r in search_results if r.get("markdown")]
    else:
        # Need to scrape separately (fallback)
        console.print("[cyan]Scraping URLs separately...[/cyan]")
        urls = [r["url"] for r in search_results]
        scraped_content = await scrape_all(urls)

    if not scraped_content:
        console.print("[red]Failed to scrape any content[/red]")
        sys.exit(1)

    # Step 3: Filter by quality
    console.print("[cyan]Filtering results by quality...[/cyan]")
    filtered_content = filter_quality(scraped_content)
    console.print(
        f"[green]Kept {len(filtered_content)}/{len(scraped_content)} high-quality results[/green]"
    )

    if not filtered_content:
        console.print(
            "[yellow]Warning: All results filtered out. Saving unfiltered results.[/yellow]"
        )
        filtered_content = scraped_content

    # Step 4: Combine into research document
    document = combine_results(query, search_results, filtered_content, categories)

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")

    console.print(f"[green]✓ Research saved to:[/green] {output_path}")
    console.print(f"[dim]Total pages: {len(filtered_content)}, Characters: {len(document)}[/dim]")


def main(
    query: str = typer.Argument(..., help="Search query for research"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of search results to scrape"),
    output: str = typer.Option(
        "ai_docs/research.md", "--output", "-o", help="Output markdown file path"
    ),
    category: str | None = typer.Option(
        None,
        "--category",
        "-c",
        help="Search category: github, research, or pdf",
    ),
    categories: str | None = typer.Option(
        None,
        "--categories",
        help="Comma-separated list of categories: github,research,pdf",
    ),
):
    """
    Research a topic using Firecrawl: search the web, scrape results, filter by quality, and combine into a markdown document.

    Examples:
        # Search GitHub for ansible proxmox ceph examples
        scripts/firecrawl_sdk_research.py "ansible proxmox ceph" --category github

        # Search research papers
        scripts/firecrawl_sdk_research.py "machine learning" --category research

        # Multiple categories
        scripts/firecrawl_sdk_research.py "neural networks" --categories github,research
    """
    output_path = Path(output)

    # Parse categories
    category_list = None
    if categories and category:
        raise typer.BadParameter("Use either --category or --categories, not both.")
    if categories:
        category_list = [c.strip() for c in categories.split(",")]
    elif category:
        category_list = [category]

    # Run async research
    asyncio.run(research(query, limit, output_path, categories=category_list))


if __name__ == "__main__":
    typer.run(main)
