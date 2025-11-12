#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31.0",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
# ]
# ///
"""
Download Claude Code documentation using Jina Reader API (direct HTTP calls).

This script demonstrates the direct HTTP approach using the Jina Reader API.
Best for: Simple scripts, automation without MCP setup, direct control over HTTP.

Usage:
    ./jina_reader_docs.py                              # Use free tier
    ./jina_reader_docs.py --api-key YOUR_KEY           # Use API key
    ./jina_reader_docs.py --output-dir docs --retries 5
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import requests
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table


class OutputFormat(str, Enum):
    """Output format options."""
    RICH = "rich"
    JSON = "json"

console = Console()

@dataclass
class FileMetadata:
    """Metadata for tracking file versions."""
    etag: str | None = None
    last_modified: str | None = None
    size: int = 0
    downloaded_at: float = 0.0

@dataclass
class DownloadResult:
    """Result of documentation download operation."""
    status: str
    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    duration_seconds: float = 0.0
    timestamp: str = ""

# Same constants as claude_docs.py
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

def build_jina_reader_url(url: str) -> str:
    """Construct Jina Reader API URL by prefixing with r.jina.ai."""
    return f"https://r.jina.ai/{url}"

def get_api_key(cli_key: str | None) -> str | None:
    """Get API key from CLI arg or environment, with CLI taking precedence."""
    if cli_key:
        return cli_key
    return os.environ.get("JINA_API_KEY")

def get_base_url(section: str) -> str:
    """Get the base URL for a documentation section."""
    if section == "claude-code":
        return CLAUDE_CODE_BASE
    elif section == "agents-and-tools":
        return AGENTS_TOOLS_BASE
    else:
        return f"{BASE_URL}/{section}"

def download_page_jina(
    url: str,
    api_key: str | None = None,
    retries: int = 3,
    timeout: int = 30,
) -> tuple[bool, str, dict]:
    """
    Download a page using Jina Reader API with retry logic.

    Args:
        url: Full URL to the documentation page
        api_key: Jina API key (optional, uses free tier if None)
        retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success: bool, content: str, metadata: dict)
    """
    reader_url = build_jina_reader_url(url)
    headers = {"X-Return-Format": "markdown"}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(reader_url, headers=headers, timeout=timeout)
            response.raise_for_status()

            metadata = {
                "etag": response.headers.get("etag"),
                "last_modified": response.headers.get("last-modified"),
                "size": len(response.text.encode('utf-8')),
                "downloaded_at": time.time(),
            }

            return True, response.text, metadata

        except requests.exceptions.HTTPError as e:
            if attempt < retries and e.response.status_code >= 500:
                wait_time = 2 ** (attempt - 1)
                console.print(
                    f"[yellow]WARNING:[/yellow] HTTP {e.response.status_code}, "
                    f"retrying in {wait_time}s (attempt {attempt}/{retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                console.print(
                    f"[red]ERROR:[/red] HTTP {e.response.status_code}",
                    file=sys.stderr
                )
                return False, "", {}

        except requests.exceptions.RequestException as e:
            if attempt < retries:
                wait_time = 2 ** (attempt - 1)
                console.print(
                    f"[yellow]WARNING:[/yellow] Network error, "
                    f"retrying in {wait_time}s (attempt {attempt}/{retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                console.print(f"[red]ERROR:[/red] {e}", file=sys.stderr)
                return False, "", {}

    return False, "", {}

def main(
    output_dir: Path = typer.Option(
        Path(__file__).parent.parent / "ai_docs",
        "--output-dir", "-o",
        help="Directory to save downloaded files",
    ),
    api_key: str | None = typer.Option(
        None,
        "--api-key",
        help="Jina API key (defaults to JINA_API_KEY env var)",
    ),
    retries: int = typer.Option(
        3,
        "--retries", "-r",
        help="Maximum retry attempts per page",
        min=1, max=10,
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format: 'rich' or 'json'",
    ),
) -> None:
    """
    Download Claude Code docs using Jina Reader API (direct HTTP calls).

    This demonstrates the simplest approach: direct HTTP requests to Jina Reader.
    Best for scripts and automation without MCP setup.
    """
    output_dir.mkdir(exist_ok=True, parents=True)

    # Get API key (CLI overrides environment)
    api_key = get_api_key(api_key)

    if format == OutputFormat.RICH:
        key_status = "with API key" if api_key else "free tier (20 RPM)"
        console.print(
            f"[cyan]Downloading using Jina Reader API ({key_status})[/cyan]"
        )
        console.print(f"[dim]Output: {output_dir.absolute()}/[/dim]\n")

    start_time = time.time()
    success_count = 0
    failed_count = 0
    total_bytes = 0
    download_times = []

    pages = DEFAULT_PAGES

    if format == OutputFormat.RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Downloading...", total=len(pages))

            for section, page in pages:
                progress.update(task, description=f"[cyan]Downloading {page}...")

                base_url = get_base_url(section)
                url = f"{base_url}/{page}.md"

                page_start = time.time()
                success, content, metadata = download_page_jina(
                    url, api_key=api_key, retries=retries
                )
                duration = time.time() - page_start

                if success:
                    # Save to file
                    flat_filename = page.replace("/", "-")
                    output_file = output_dir / f"{flat_filename}.md"
                    output_file.write_text(content)

                    size_kb = metadata["size"] / 1024
                    speed_kbps = (metadata["size"] / 1024) / duration if duration > 0 else 0
                    console.print(
                        f"[green]SUCCESS:[/green] {flat_filename}.md "
                        f"[dim]({size_kb:.1f}KB in {duration:.2f}s @ {speed_kbps:.1f}KB/s)[/dim]"
                    )
                    success_count += 1
                    total_bytes += metadata["size"]
                    download_times.append(duration)
                else:
                    failed_count += 1

                progress.advance(task)
    else:
        # JSON mode
        for section, page in pages:
            base_url = get_base_url(section)
            url = f"{base_url}/{page}.md"

            page_start = time.time()
            success, content, metadata = download_page_jina(
                url, api_key=api_key, retries=retries
            )
            duration = time.time() - page_start

            if success:
                flat_filename = page.replace("/", "-")
                output_file = output_dir / f"{flat_filename}.md"
                output_file.write_text(content)

                success_count += 1
                total_bytes += metadata["size"]
                download_times.append(duration)
            else:
                failed_count += 1

    total_time = time.time() - start_time

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

        table.add_row("Total Pages", str(len(pages)))
        table.add_row("Downloaded", f"[green]{success_count}[/green]")
        if failed_count > 0:
            table.add_row("Failed", f"[red]{failed_count}[/red]")
        table.add_row("Total Size", f"{total_bytes / 1024:.1f} KB")
        table.add_row("Total Time", f"{total_time:.2f}s")

        if download_times:
            avg_time = sum(download_times) / len(download_times)
            table.add_row("Avg Time/Page", f"{avg_time:.2f}s")

        console.print(table)

        # Note about parallel potential
        if len(download_times) > 1:
            console.print(
                "\n[yellow]NOTE:[/yellow] Sequential processing. "
                "See jina_mcp_docs.py for parallel downloads (~3x faster)."
            )

    if failed_count > 0:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(main)
