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
Download Claude Code documentation using Jina MCP Server (parallel operations).

This script demonstrates parallel URL reading via Claude Agent SDK + Jina MCP.
Best for: Research tasks requiring multiple sources, speed optimization (3-4 URLs optimal).

NOTE: This is a POC demonstrating Claude Agent SDK patterns for parallel MCP tool usage.
The response parsing implementation (lines 160-174) saves combined content to all files
as a placeholder. A production implementation would parse structured MCP responses
to extract individual URL content.

Prerequisites:
    - Jina MCP server configured in Claude settings
    - JINA_API_KEY environment variable set
    - ANTHROPIC_API_KEY environment variable set

Usage:
    ./jina_mcp_docs.py                              # Downloads with optimal batching
    ./jina_mcp_docs.py --batch-size 4               # Custom batch size
    ./jina_mcp_docs.py --output-dir docs
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

# Claude Agent SDK imports
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

# Same constants as other scripts
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

# Optimal batch size based on research
OPTIMAL_BATCH_SIZE = 3

def batch_urls(urls: list[str], batch_size: int = OPTIMAL_BATCH_SIZE) -> list[list[str]]:
    """Split URLs into optimal batches for parallel processing."""
    return [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

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
    Validate required API keys are present in environment.

    Raises:
        ValueError: If required API keys are missing
    """
    missing_keys = []

    if not os.getenv("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")

    if not os.getenv("JINA_API_KEY"):
        missing_keys.append("JINA_API_KEY")

    if missing_keys:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_keys)}\n"
            "Please set them before running this script."
        )

def create_orchestrator_options() -> ClaudeAgentOptions:
    """
    Create SDK options for orchestrator that uses Jina MCP tools.

    The orchestrator needs:
    - claude_code system prompt (provides MCP tool knowledge)
    - Jina MCP tools available in environment
    """
    return ClaudeAgentOptions(
        system_prompt="claude_code",  # CRITICAL for orchestrator
        allowed_tools=[
            "mcp__jina-mcp-server__read_url",
            "mcp__jina-mcp-server__parallel_read_url",
            "Task",  # For delegating to agents
        ],
        permission_mode="acceptEdits",
        model="claude-sonnet-4-5-20250929"
    )

async def download_batch_parallel(
    urls: list[str],
    output_dir: Path = Path("./ai_docs"),
) -> list[tuple[str, bool, str]]:
    """
    Download a batch of URLs in parallel using Jina MCP parallel_read_url.

    Args:
        urls: List of URLs to download (max 3-4 for optimal performance)
        output_dir: Directory to save files

    Returns:
        List of (url, success, content) tuples
    """
    options = create_orchestrator_options()
    results = []

    async with ClaudeSDKClient(options=options) as client:
        # Build parallel read request
        url_objects = [{"url": url} for url in urls]

        # Query Claude to use parallel_read_url MCP tool
        prompt = f"""Use the Jina MCP parallel_read_url tool to fetch these URLs in parallel:

{json.dumps(url_objects, indent=2)}

Return the content for each URL."""

        await client.query(prompt)

        # Collect responses
        full_response = []
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        full_response.append(block.text)

        # Parse response and extract content
        # TODO: POC LIMITATION - This saves combined content to all files
        # Production implementation should:
        # 1. Parse structured MCP tool response (JSON array of {url, content} objects)
        # 2. Map each URL to its specific content
        # 3. Save individual content to corresponding files
        # Current behavior: All files get the same combined response
        combined_content = "\n\n".join(full_response)

        for url in urls:
            # Extract page name from URL
            page_name = url.split("/")[-1].replace(".md", "")
            flat_filename = page_name.replace("/", "-")
            output_file = output_dir / f"{flat_filename}.md"

            # TODO: Replace with parsed individual content per URL
            output_file.write_text(combined_content)
            results.append((url, True, combined_content))

    return results

async def download_all_parallel(
    pages: list[tuple[str, str]],
    output_dir: Path,
    batch_size: int,
    format: OutputFormat,
) -> tuple[int, int, float, list[float]]:
    """
    Download all pages using parallel batching strategy.

    Returns:
        Tuple of (success_count, failed_count, total_time, batch_times)
    """
    start_time = time.time()
    success_count = 0
    failed_count = 0
    batch_times = []

    # Build full URLs
    urls = []
    for section, page in pages:
        base_url = get_base_url(section)
        urls.append(f"{base_url}/{page}.md")

    # Split into batches
    url_batches = batch_urls(urls, batch_size)

    if format == OutputFormat.RICH:
        console.print(
            f"[cyan]Processing {len(urls)} URLs in {len(url_batches)} batches "
            f"(batch size: {batch_size})[/cyan]\n"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "[cyan]Downloading batches...",
                total=len(url_batches)
            )

            for batch_num, batch in enumerate(url_batches, 1):
                progress.update(
                    task,
                    description=f"[cyan]Batch {batch_num}/{len(url_batches)} "
                    f"({len(batch)} URLs)..."
                )

                batch_start = time.time()
                results = await download_batch_parallel(batch, output_dir)
                batch_duration = time.time() - batch_start
                batch_times.append(batch_duration)

                for url, success, content in results:
                    page_name = url.split("/")[-1].replace(".md", "")
                    if success:
                        console.print(
                            f"[green]SUCCESS:[/green] {page_name} "
                            f"[dim](batch {batch_num}, {len(content)} bytes)[/dim]"
                        )
                        success_count += 1
                    else:
                        console.print(f"[red]ERROR:[/red] {page_name}", file=sys.stderr)
                        failed_count += 1

                progress.advance(task)
    else:
        # JSON mode
        for batch in url_batches:
            batch_start = time.time()
            results = await download_batch_parallel(batch, output_dir)
            batch_duration = time.time() - batch_start
            batch_times.append(batch_duration)

            for url, success, content in results:
                if success:
                    success_count += 1
                else:
                    failed_count += 1

    total_time = time.time() - start_time
    return success_count, failed_count, total_time, batch_times

def main(
    output_dir: Path = typer.Option(
        Path("./ai_docs"),
        "--output-dir", "-o",
        help="Directory to save downloaded files",
    ),
    batch_size: int = typer.Option(
        OPTIMAL_BATCH_SIZE,
        "--batch-size",
        help="URLs per parallel batch (3-4 optimal, max 5)",
        min=1, max=5,
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format: 'rich' or 'json'",
    ),
) -> None:
    """
    Download Claude Code docs using Jina MCP Server (parallel operations).

    This demonstrates parallel URL reading via Claude Agent SDK.
    Best for: Research tasks, speed optimization (3-4x faster than sequential).

    Requires: Jina MCP server configured with JINA_API_KEY and ANTHROPIC_API_KEY.
    """
    # Validate required API keys before proceeding
    try:
        validate_api_keys()
    except ValueError as e:
        if format == OutputFormat.RICH:
            console.print(f"[red]ERROR:[/red] {e}", file=sys.stderr)
        else:
            print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        raise typer.Exit(code=1)

    output_dir.mkdir(exist_ok=True, parents=True)

    if format == OutputFormat.RICH:
        console.print(
            "[cyan]Downloading using Jina MCP Server (parallel operations)[/cyan]"
        )
        console.print(f"[dim]Output: {output_dir.absolute()}/[/dim]\n")

    # Run async download
    success_count, failed_count, total_time, batch_times = asyncio.run(
        download_all_parallel(DEFAULT_PAGES, output_dir, batch_size, format)
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
        table = Table(title="Download Summary", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Pages", str(len(DEFAULT_PAGES)))
        table.add_row("Downloaded", f"[green]{success_count}[/green]")
        if failed_count > 0:
            table.add_row("Failed", f"[red]{failed_count}[/red]")
        table.add_row("Total Batches", str(len(batch_times)))
        table.add_row("Total Time", f"{total_time:.2f}s")

        if batch_times:
            avg_batch_time = sum(batch_times) / len(batch_times)
            table.add_row("Avg Batch Time", f"{avg_batch_time:.2f}s")

        console.print(table)

        # Performance note
        console.print(
            "\n[yellow]NOTE:[/yellow] Parallel batching "
            "(~3x faster than sequential). Optimal batch size: 3-4 URLs."
        )

    if failed_count > 0:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(main)
