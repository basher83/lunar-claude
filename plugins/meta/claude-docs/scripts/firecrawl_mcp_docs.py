#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "claude-agent-sdk>=0.1.6",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
# ]
# ///
"""
Download Claude Code documentation using Firecrawl MCP Server (robust scraping).

This script demonstrates production-grade scraping via Claude Agent SDK + Firecrawl MCP.
Best for: Production scraping, complex pages, need for rich metadata and reliability.

NOTE: This is a POC demonstrating Claude Agent SDK patterns for Firecrawl MCP tool usage.
The metadata implementation (lines 160-165) uses placeholder values. A production
implementation would parse structured MCP responses to extract actual Firecrawl metadata
(cache status, credits used, etc.).

Prerequisites:
    - Firecrawl MCP server configured in Claude settings
    - FIRECRAWL_API_KEY environment variable set

Usage:
    ./firecrawl_mcp_docs.py                         # Downloads with full metadata
    ./firecrawl_mcp_docs.py --output-dir docs
    ./firecrawl_mcp_docs.py --main-content-only     # Strip navigation/footers
"""

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import typer
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table


class OutputFormat(str, Enum):
    """Output format options."""
    RICH = "rich"
    JSON = "json"


console = Console()


@dataclass
class DownloadResult:
    """Result of documentation download operation."""
    status: str
    downloaded: int = 0
    failed: int = 0
    duration_seconds: float = 0.0
    timestamp: str = ""


# Same constants
BASE_URL = "https://docs.claude.com/en/docs"
CLAUDE_CODE_BASE = f"{BASE_URL}/claude-code"
AGENTS_TOOLS_BASE = f"{BASE_URL}/agents-and-tools"

CLAUDE_CODE_PAGES = [
    "sub-agents", "plugins", "skills", "output-styles", "hooks-guide",
    "plugin-marketplaces", "settings", "statusline", "slash-commands",
    "hooks", "plugins-reference", "memory", "mcp"
]

AGENT_SKILLS_PAGES = [
    "agent-skills/overview",
    "agent-skills/quickstart",
    "agent-skills/best-practices",
]

DEFAULT_PAGES = [
    ("claude-code", page) for page in CLAUDE_CODE_PAGES
] + [
    ("agents-and-tools", page) for page in AGENT_SKILLS_PAGES
]


def get_base_url(section: str) -> str:
    """Get the base URL for a documentation section."""
    if section == "claude-code":
        return CLAUDE_CODE_BASE
    elif section == "agents-and-tools":
        return AGENTS_TOOLS_BASE
    else:
        return f"{BASE_URL}/{section}"


def validate_api_keys() -> None:
    """
    Validate required environment variables are set.

    Raises:
        ValueError: If any required API keys are missing.
    """
    missing_keys = []

    # ANTHROPIC_API_KEY not needed - SDK uses current Claude Code session

    if not os.getenv("FIRECRAWL_API_KEY"):
        missing_keys.append("FIRECRAWL_API_KEY")

    if missing_keys:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_keys)}\n"
            "Please set them before running this script."
        )


def create_orchestrator_options() -> ClaudeAgentOptions:
    """
    Create SDK options for orchestrator that uses Firecrawl MCP tools.

    Firecrawl provides:
    - Robust scraping with better error handling
    - Rich metadata (cache status, credits used, etc.)
    - Support for complex/large pages
    """
    return ClaudeAgentOptions(
        system_prompt="claude_code",
        allowed_tools=[
            "mcp__firecrawl__firecrawl_scrape",
            "mcp__firecrawl__firecrawl_search",
        ],
        permission_mode="acceptEdits",
        model="claude-sonnet-4-5-20250929"
    )


async def download_page_firecrawl(
    url: str,
    output_dir: Path,
    main_content_only: bool = True,
) -> tuple[bool, str, dict]:
    """
    Download a page using Firecrawl MCP scrape tool.

    Args:
        url: Full URL to download
        output_dir: Directory to save file
        main_content_only: Strip navigation/footers (default: True)

    Returns:
        Tuple of (success, content, metadata)
    """
    options = create_orchestrator_options()

    try:
        async with ClaudeSDKClient(options=options) as client:
            # Build scrape request
            prompt = f"""Use the Firecrawl firecrawl_scrape tool to fetch this URL:

URL: {url}
Options:
- formats: ["markdown"]
- onlyMainContent: {str(main_content_only).lower()}

Return the scraped markdown content and metadata."""

            await client.query(prompt)

            # Collect response
            full_response = []
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            full_response.append(block.text)

            combined_content = "\n\n".join(full_response)

            # Validate content
            if not combined_content or len(combined_content.strip()) < 100:
                return False, "", {
                    "url": url,
                    "error": "Empty or minimal content received",
                }

            # Extract page name and save
            page_name = url.split("/")[-1].replace(".md", "")
            flat_filename = page_name.replace("/", "-")
            output_file = output_dir / f"{flat_filename}.md"
            output_file.write_text(combined_content)

            # Metadata (in production, would parse from MCP tool response)
            metadata = {
                "url": url,
                "size": len(combined_content),
                "main_content_only": main_content_only,
            }

            return True, combined_content, metadata

    except Exception as e:
        return False, "", {
            "url": url,
            "error": str(e),
        }


async def download_all_sequential(
    pages: list[tuple[str, str]],
    output_dir: Path,
    main_content_only: bool,
    format: OutputFormat,
) -> tuple[int, int, float]:
    """
    Download all pages sequentially using Firecrawl.

    Note: Firecrawl doesn't support parallel operations,
    but provides better reliability for individual pages.

    Returns:
        Tuple of (success_count, failed_count, total_time)
    """
    start_time = time.time()
    success_count = 0
    failed_count = 0

    if format == OutputFormat.RICH:
        console.print(
            f"[cyan]Processing {len(pages)} URLs sequentially "
            f"(Firecrawl optimized for reliability)[/cyan]\n"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "[cyan]Downloading...",
                total=len(pages)
            )

            for section, page in pages:
                base_url = get_base_url(section)
                url = f"{base_url}/{page}.md"

                progress.update(
                    task, description=f"[cyan]Downloading {page}...")

                page_start = time.time()
                try:
                    success, content, metadata = await download_page_firecrawl(
                        url, output_dir, main_content_only
                    )
                    duration = time.time() - page_start

                    if success:
                        size_kb = metadata["size"] / 1024
                        console.print(
                            f"[green]SUCCESS:[/green] {page} "
                            f"[dim]({size_kb:.1f}KB in {duration:.2f}s)[/dim]"
                        )
                        success_count += 1
                    else:
                        console.print(
                            f"[red]ERROR:[/red] {page}", file=sys.stderr)
                        failed_count += 1
                except Exception as e:
                    console.print(
                        f"[red]ERROR:[/red] {page}: {e}",
                        file=sys.stderr
                    )
                    failed_count += 1

                progress.advance(task)
    else:
        # JSON mode
        for section, page in pages:
            base_url = get_base_url(section)
            url = f"{base_url}/{page}.md"

            try:
                success, content, metadata = await download_page_firecrawl(
                    url, output_dir, main_content_only
                )
                if success:
                    success_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1

    total_time = time.time() - start_time
    return success_count, failed_count, total_time


def main(
    output_dir: Path = typer.Option(
        Path(__file__).parent.parent / "ai_docs",
        "--output-dir", "-o",
        help="Directory to save downloaded files",
    ),
    main_content_only: bool = typer.Option(
        True,
        "--main-content-only",
        help="Extract only main content (strip navigation/footers)",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format: 'rich' or 'json'",
    ),
) -> None:
    """
    Download Claude Code docs using Firecrawl MCP Server (robust scraping).

    This demonstrates production-grade scraping with rich metadata.
    Best for: Complex pages, need for reliability, production scraping.

    Requires: Firecrawl MCP server configured with FIRECRAWL_API_KEY.
    """
    # Validate API keys first
    try:
        validate_api_keys()
    except ValueError as e:
        if format == OutputFormat.RICH:
            console.print(f"[red]ERROR:[/red] {e}", file=sys.stderr)
        else:
            error_result = {
                "status": "error",
                "message": str(e)
            }
            print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(exist_ok=True, parents=True)

    if format == OutputFormat.RICH:
        console.print(
            "[cyan]Downloading using Firecrawl MCP Server (robust scraping)[/cyan]"
        )
        console.print(f"[dim]Output: {output_dir.absolute()}/[/dim]\n")

    # Run async download
    success_count, failed_count, total_time = asyncio.run(
        download_all_sequential(DEFAULT_PAGES, output_dir,
                                main_content_only, format)
    )

    # Output results
    if format == OutputFormat.JSON:
        result = {
            "status": "success" if failed_count == 0 else "error",
            "downloaded": success_count,
            "failed": failed_count,
            "duration_seconds": round(total_time, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        print(json.dumps(result))
    else:
        console.print()
        table = Table(title="Download Summary",
                      show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Pages", str(len(DEFAULT_PAGES)))
        table.add_row("Downloaded", f"[green]{success_count}[/green]")
        if failed_count > 0:
            table.add_row("Failed", f"[red]{failed_count}[/red]")
        table.add_row("Total Time", f"{total_time:.2f}s")

        console.print(table)

        # Feature note
        console.print(
            "\n[yellow]NOTE:[/yellow] Features: Rich metadata, robust error handling, "
            "complex page support. Trade speed for reliability."
        )

    if failed_count > 0:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
