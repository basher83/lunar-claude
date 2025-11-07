#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
# ]
# ///
"""
Download Claude Code documentation pages using Firecrawl API.

This script uses Firecrawl API for enhanced reliability and better error handling
when scraping documentation pages. Optimized for reliability over speed.

Usage:
    ./claude_docs_firecrawl.py                    # Downloads to ./ai_docs
    ./claude_docs_firecrawl.py --output-dir docs  # Downloads to ./docs
    ./claude_docs_firecrawl.py --retries 5        # Try up to 5 times per page
    ./claude_docs_firecrawl.py --api-key KEY     # Override FIRECRAWL_API_KEY env var
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

import httpx
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table


class OutputFormat(str, Enum):
    """Output format options for the script."""
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
    firecrawl_status: str | None = None
    firecrawl_credits_used: int | None = None


@dataclass
class DownloadResult:
    """Result of documentation download operation."""
    status: str  # "success" or "error"
    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    duration_seconds: float = 0.0
    timestamp: str = ""


BASE_URL = "https://docs.claude.com/en/docs"
CLAUDE_CODE_BASE = f"{BASE_URL}/claude-code"
AGENTS_TOOLS_BASE = f"{BASE_URL}/agents-and-tools"
DOCS_MAP_URL = f"{CLAUDE_CODE_BASE}/claude_code_docs_map.md"
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0/scrape"

# Curated list of most useful pages for Claude Code development
CLAUDE_CODE_PAGES = [
    "sub-agents",
    "plugins",
    "skills",
    "output-styles",
    "hooks-guide",
    "plugin-marketplaces",
    "settings",
    "statusline",
    "slash-commands",
    "hooks",
    "plugins-reference",
    "memory",
    "mcp"
]

# Agent Skills API documentation
AGENT_SKILLS_PAGES = [
    "agent-skills/overview",
    "agent-skills/quickstart",
    "agent-skills/best-practices",
]

# Combined default pages with their base URLs
DEFAULT_PAGES = [
    ("claude-code", page) for page in CLAUDE_CODE_PAGES
] + [
    ("agents-and-tools", page) for page in AGENT_SKILLS_PAGES
]


def load_cache(cache_file: Path) -> dict[str, FileMetadata]:
    """
    Load metadata cache from JSON file.

    Args:
        cache_file: Path to cache file

    Returns:
        Dictionary mapping page names to their metadata
    """
    if not cache_file.exists():
        return {}

    try:
        with cache_file.open() as f:
            data = json.load(f)
            return {
                page: FileMetadata(**meta)
                for page, meta in data.items()
            }
    except (json.JSONDecodeError, TypeError) as e:
        console.print(
            f"[yellow]Warning: Could not load cache: {e}[/yellow]", file=sys.stderr)
        return {}


def save_cache(cache_file: Path, cache: dict[str, FileMetadata]) -> None:
    """
    Save metadata cache to JSON file.

    Args:
        cache_file: Path to cache file
        cache: Dictionary of page metadata
    """
    try:
        data = {
            page: {
                "etag": meta.etag,
                "last_modified": meta.last_modified,
                "size": meta.size,
                "downloaded_at": meta.downloaded_at,
                "firecrawl_status": meta.firecrawl_status,
                "firecrawl_credits_used": meta.firecrawl_credits_used,
            }
            for page, meta in cache.items()
        }
        with cache_file.open("w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        console.print(
            f"[yellow]Warning: Could not save cache: {e}[/yellow]", file=sys.stderr)


def discover_all_pages(client: httpx.Client, api_key: Optional[str]) -> list[tuple[str, str]]:
    """
    Fetch the docs map and extract all available page paths.

    Args:
        client: httpx Client instance
        api_key: Firecrawl API key (optional)

    Returns:
        List of (section, page_path) tuples found in the docs map
    """
    try:
        # Use Firecrawl to scrape the docs map
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        payload = {
            "url": DOCS_MAP_URL,
            "formats": ["markdown"],
            "onlyMainContent": True,
        }
        
        response = client.post(
            FIRECRAWL_API_URL,
            json=payload,
            headers=headers,
            timeout=30.0
        )
        response.raise_for_status()
        
        result = response.json()
        content = result.get("markdown", result.get("data", {}).get("markdown", ""))
        
        if not content:
            # Fallback to direct HTTP request
            response = client.get(DOCS_MAP_URL, timeout=30.0)
            response.raise_for_status()
            content = response.text

        # Extract paths from markdown links: ### [name](https://docs.claude.com/en/docs/claude-code/path.md)
        import re
        pattern = r'###\s+\[[^\]]+\]\(https://docs\.claude\.com/en/docs/claude-code/([^)]+)\.md\)'
        matches = re.findall(pattern, content)

        if not matches:
            stderr_console = Console(stderr=True)
            stderr_console.print(
                "[yellow]Warning: Could not find pages in docs map, using defaults[/yellow]"
            )
            return DEFAULT_PAGES

        # Return as tuples with 'claude-code' section
        return [("claude-code", page) for page in matches]

    except Exception as e:
        stderr_console = Console(stderr=True)
        stderr_console.print(
            f"[yellow]Warning: Could not fetch docs map: {e}[/yellow]"
        )
        return DEFAULT_PAGES


def get_base_url(section: str) -> str:
    """Get the base URL for a documentation section."""
    if section == "claude-code":
        return CLAUDE_CODE_BASE
    elif section == "agents-and-tools":
        return AGENTS_TOOLS_BASE
    else:
        return f"{BASE_URL}/{section}"


def needs_update(
    client: httpx.Client,
    section: str,
    page: str,
    cached_meta: FileMetadata | None,
) -> tuple[bool, str | None, str | None]:
    """
    Check if a page needs to be downloaded by comparing HTTP headers.

    Args:
        client: httpx Client instance
        section: Documentation section (e.g., 'claude-code', 'agents-and-tools')
        page: Page name
        cached_meta: Cached metadata for this page (if available)

    Returns:
        Tuple of (needs_update: bool, etag: str, last_modified: str)
    """
    base_url = get_base_url(section)
    url = f"{base_url}/{page}.md"

    try:
        # Make HEAD request to check headers without downloading content
        response = client.head(url, timeout=10.0)
        response.raise_for_status()

        etag = response.headers.get("etag")
        last_modified = response.headers.get("last-modified")

        # If we don't have cached metadata, we need to download
        if not cached_meta:
            return True, etag, last_modified

        # Compare ETag (most reliable)
        if etag and cached_meta.etag:
            if etag == cached_meta.etag:
                return False, etag, last_modified

        # Compare Last-Modified as fallback
        if last_modified and cached_meta.last_modified:
            if last_modified == cached_meta.last_modified:
                return False, etag, last_modified

        # If headers don't match or aren't available, assume update needed
        return True, etag, last_modified

    except Exception:
        # If HEAD request fails, assume we need to try downloading
        stderr_console = Console(stderr=True)
        stderr_console.print(
            f"[dim]Could not check {page} headers, will attempt download[/dim]"
        )
        return True, None, None


def download_page_firecrawl(
    client: httpx.Client,
    section: str,
    page: str,
    output_dir: Path,
    api_key: Optional[str],
    max_retries: int = 3,
    etag: str | None = None,
    last_modified: str | None = None,
) -> tuple[bool, float, int, FileMetadata]:
    """
    Download a single documentation page using Firecrawl API with retry logic.

    Args:
        client: httpx Client instance
        section: Documentation section (e.g., 'claude-code', 'agents-and-tools')
        page: Page name (without .md extension)
        output_dir: Directory to save the file
        api_key: Firecrawl API key (required)
        max_retries: Maximum number of retry attempts (default: 3)
        etag: ETag from HEAD request (if available)
        last_modified: Last-Modified from HEAD request (if available)

    Returns:
        Tuple of (success: bool, duration: float, size_bytes: int, metadata: FileMetadata)
    """
    base_url = get_base_url(section)
    url = f"{base_url}/{page}.md"

    # Flatten path: replace slashes with dashes for output filename
    flat_filename = page.replace("/", "-")
    output_file = output_dir / f"{flat_filename}.md"

    start_time = time.time()

    # Prepare headers
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        console.print(
            f"[red]✗[/red] {page}: Firecrawl API key required (set FIRECRAWL_API_KEY env var)",
            file=sys.stderr
        )
        empty_meta = FileMetadata()
        return False, time.time() - start_time, 0, empty_meta

    # Prepare request payload
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,  # Reduce size for documentation pages
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = client.post(
                FIRECRAWL_API_URL,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            # Handle rate limit errors with exponential backoff
            if response.status_code == 429:
                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    console.print(
                        f"[yellow]⚠[/yellow] {page}: Rate limited, "
                        f"retrying in {wait_time}s (attempt {attempt}/{max_retries})"
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    console.print(
                        f"[red]✗[/red] {page}: Rate limit exceeded",
                        file=sys.stderr
                    )
                    empty_meta = FileMetadata()
                    return False, time.time() - start_time, 0, empty_meta
            
            response.raise_for_status()
            
            result = response.json()
            
            # Extract markdown content from Firecrawl response
            # Response format: {"success": true, "data": {"markdown": "...", ...}, ...}
            if result.get("success"):
                data = result.get("data", {})
                content = data.get("markdown", "")
                
                if not content:
                    # Fallback: try to get content from other fields
                    content = data.get("content", "")
                
                if not content:
                    raise ValueError("No markdown content in Firecrawl response")
                
                output_file.write_text(content)

                duration = time.time() - start_time
                size_bytes = len(content.encode('utf-8'))

                # Extract metadata from Firecrawl response
                metadata = FileMetadata(
                    etag=etag,
                    last_modified=last_modified,
                    size=size_bytes,
                    downloaded_at=time.time(),
                    firecrawl_status=result.get("status", "unknown"),
                    firecrawl_credits_used=result.get("creditsUsed"),
                )

                return True, duration, size_bytes, metadata
            else:
                error_msg = result.get("error", "Unknown error")
                raise ValueError(f"Firecrawl API error: {error_msg}")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                console.print(
                    f"[red]✗[/red] {page}: Invalid API key",
                    file=sys.stderr
                )
                empty_meta = FileMetadata()
                return False, time.time() - start_time, 0, empty_meta
            
            if attempt < max_retries and e.response.status_code >= 500:
                # Retry on server errors with exponential backoff
                wait_time = 2 ** (attempt - 1)
                console.print(
                    f"[yellow]⚠[/yellow] {page}: HTTP {e.response.status_code}, "
                    f"retrying in {wait_time}s (attempt {attempt}/{max_retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                console.print(
                    f"[red]✗[/red] {page}: HTTP {e.response.status_code}",
                    file=sys.stderr
                )
                empty_meta = FileMetadata()
                return False, time.time() - start_time, 0, empty_meta

        except httpx.RequestError as e:
            if attempt < max_retries:
                # Retry on network errors with exponential backoff
                wait_time = 2 ** (attempt - 1)
                console.print(
                    f"[yellow]⚠[/yellow] {page}: Network error, "
                    f"retrying in {wait_time}s (attempt {attempt}/{max_retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                console.print(f"[red]✗[/red] {page}: {e}", file=sys.stderr)
                empty_meta = FileMetadata()
                return False, time.time() - start_time, 0, empty_meta

        except (ValueError, KeyError) as e:
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)
                console.print(
                    f"[yellow]⚠[/yellow] {page}: Parse error ({e}), "
                    f"retrying in {wait_time}s (attempt {attempt}/{max_retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                console.print(
                    f"[red]✗[/red] {page}: Parse error: {e}",
                    file=sys.stderr
                )
                empty_meta = FileMetadata()
                return False, time.time() - start_time, 0, empty_meta

        except Exception as e:
            console.print(
                f"[red]✗[/red] {page}: Unexpected error: {e}",
                file=sys.stderr
            )
            empty_meta = FileMetadata()
            return False, time.time() - start_time, 0, empty_meta

    # Should never reach here
    empty_meta = FileMetadata()
    return False, time.time() - start_time, 0, empty_meta


def find_or_create_ai_docs_dir() -> Path:
    """
    Get reference docs directory for the claude-docs skill.

    Returns ../skills/claude-docs/reference/ relative to the script.
    """
    script_dir = Path(__file__).parent
    return script_dir.parent / "skills" / "claude-docs" / "reference"


def main(
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir", "-o",
        help="Directory to save downloaded documentation files (default: auto-detect or create ai_docs/)",
        dir_okay=True,
        file_okay=False,
    ),
    retries: int = typer.Option(
        3,
        "--retries", "-r",
        help="Maximum number of retry attempts per page",
        min=1,
        max=10,
    ),
    all_pages: bool = typer.Option(
        False,
        "--all",
        help="Download all 70+ pages from the docs map",
    ),
    check_only: bool = typer.Option(
        False,
        "--check",
        help="Only check for updates, don't download (dry-run)",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive", "-i",
        help="Interactively select which pages to download",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format: 'rich' for human-readable or 'json' for machine-readable",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="Firecrawl API key (overrides FIRECRAWL_API_KEY environment variable)",
    ),
) -> None:
    """
    Download Claude Code documentation pages using Firecrawl API.

    This script uses Firecrawl API for enhanced reliability and better error handling.
    Optimized for reliability over speed (sequential processing).
    """
    # Configure console based on output format
    global console
    console = Console()

    # Auto-detect API key from environment if not provided
    if api_key is None:
        api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        console.print(
            "[red]Error: Firecrawl API key required[/red]\n"
            "[yellow]Set FIRECRAWL_API_KEY environment variable or use --api-key[/yellow]",
            file=sys.stderr
        )
        raise typer.Exit(code=1)

    # Determine output directory (auto-detect or use provided)
    if output_dir is None:
        output_dir = find_or_create_ai_docs_dir()

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True, parents=True)

    # Load cache
    cache_file = output_dir / ".download_cache.json"
    cache = load_cache(cache_file)

    # Determine which pages to download
    with httpx.Client(follow_redirects=True) as client:
        if all_pages:
            if format == OutputFormat.RICH:
                console.print(
                    "[cyan]Discovering all pages from docs map...[/cyan]")
            pages = discover_all_pages(client, api_key)
            if format == OutputFormat.RICH:
                console.print(f"[dim]Found {len(pages)} pages[/dim]\n")
        elif interactive:
            if format == OutputFormat.JSON:
                # Interactive mode not supported in JSON format, use defaults
                pages = DEFAULT_PAGES
            else:
                # Fetch all available pages first
                all_available = discover_all_pages(client, api_key)
                console.print(
                    f"[cyan]Available pages ({len(all_available)}):[/cyan]")
                for idx, (section, page) in enumerate(all_available, 1):
                    console.print(f"  {idx}. [{section}] {page}")
                console.print(
                    "\n[yellow]Enter page numbers to download (comma-separated)[/yellow]")
                console.print("[dim]Or press Enter to use defaults[/dim]")

                selection = input("> ").strip()

                if not selection:
                    pages = DEFAULT_PAGES
                    console.print(
                        f"[dim]Using default {len(pages)} pages[/dim]\n")
                else:
                    try:
                        indices = [int(x.strip()) -
                                   1 for x in selection.split(",")]
                        pages = [all_available[i]
                                 for i in indices if 0 <= i < len(all_available)]
                        console.print(
                            f"[green]Selected {len(pages)} pages[/green]\n")
                    except (ValueError, IndexError) as e:
                        console.print(f"[red]Invalid selection: {e}[/red]")
                        console.print(
                            "[yellow]Using defaults instead[/yellow]\n")
                        pages = DEFAULT_PAGES
        else:
            pages = DEFAULT_PAGES

    if format == OutputFormat.RICH:
        console.print(
            f"[cyan]{'Checking' if check_only else 'Downloading'} Claude Code documentation to {output_dir.absolute()}/[/cyan]")
        console.print(
            f"[dim]Pages: {len(pages)} | Max retries: {retries} | Firecrawl API{' | DRY RUN' if check_only else ''}[/dim]\n")

    start_time = time.time()
    success_count = 0
    failed_count = 0
    skipped_count = 0
    total_bytes = 0
    download_times = []

    with httpx.Client(follow_redirects=True) as client:
        if format == OutputFormat.RICH:
            # Rich mode: Use progress bar and status messages
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "[cyan]Checking pages...", total=len(pages))

                for section, page in pages:
                    progress.update(
                        task, description=f"[cyan]Checking {page}...")

                    # Flatten filename for display and saving
                    flat_filename = page.replace("/", "-")

                    # Check if file needs updating
                    cached_meta = cache.get(page)
                    should_update, etag, last_modified = needs_update(
                        client, section, page, cached_meta)

                    if not should_update:
                        # File hasn't changed, skip download
                        console.print(
                            f"[dim]⊙[/dim] {flat_filename}.md [dim](unchanged, skipped)[/dim]")
                        skipped_count += 1
                        progress.advance(task)
                        continue

                    # In check-only mode, just report that update is needed
                    if check_only:
                        console.print(
                            f"[yellow]↻[/yellow] {flat_filename}.md [yellow](update available)[/yellow]"
                        )
                        success_count += 1  # Count as "needs update"
                        progress.advance(task)
                        continue

                    # Download the file (sequential processing for reliability)
                    progress.update(
                        task, description=f"[cyan]Downloading {page}...")
                    success, duration, size_bytes, metadata = download_page_firecrawl(
                        client, section, page, output_dir, api_key, max_retries=retries,
                        etag=etag, last_modified=last_modified
                    )

                    if success:
                        size_kb = size_bytes / 1024
                        speed_kbps = (size_bytes / 1024) / \
                            duration if duration > 0 else 0
                        console.print(
                            f"[green]✓[/green] {flat_filename}.md "
                            f"[dim]({size_kb:.1f}KB in {duration:.2f}s @ {speed_kbps:.1f}KB/s)[/dim]"
                        )
                        success_count += 1
                        total_bytes += size_bytes
                        download_times.append(duration)
                        # Update cache with new metadata
                        cache[page] = metadata
                    else:
                        failed_count += 1

                    progress.advance(task)
        else:
            # JSON mode: Silent operation, no progress bar or status messages
            for section, page in pages:
                # Check if file needs updating
                cached_meta = cache.get(page)
                should_update, etag, last_modified = needs_update(
                    client, section, page, cached_meta)

                if not should_update:
                    # File hasn't changed, skip download
                    skipped_count += 1
                    continue

                # In check-only mode, just count that update is needed
                if check_only:
                    success_count += 1  # Count as "needs update"
                    continue

                # Download the file
                success, duration, size_bytes, metadata = download_page_firecrawl(
                    client, section, page, output_dir, api_key, max_retries=retries,
                    etag=etag, last_modified=last_modified
                )

                if success:
                    success_count += 1
                    total_bytes += size_bytes
                    download_times.append(duration)
                    # Update cache with new metadata
                    cache[page] = metadata
                else:
                    failed_count += 1

    # Save updated cache
    save_cache(cache_file, cache)

    total_time = time.time() - start_time

    # Prepare result data
    result = DownloadResult(
        status="success" if failed_count == 0 else "error",
        downloaded=success_count,
        skipped=skipped_count,
        failed=failed_count,
        duration_seconds=round(total_time, 2),
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )

    # Output based on format
    if format == OutputFormat.JSON:
        # Machine-readable JSON output (single line)
        output = {
            "status": result.status,
            "downloaded": result.downloaded,
            "skipped": result.skipped,
            "failed": result.failed,
            "duration_seconds": result.duration_seconds,
            "timestamp": result.timestamp
        }
        print(json.dumps(output))
    else:
        # Rich format (existing table output)
        console.print()
        summary_title = "Update Check Summary" if check_only else "Download Summary"
        table = Table(title=summary_title,
                      show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Pages", str(len(pages)))

        if check_only:
            table.add_row("↻ Updates Available",
                          f"[yellow]{success_count}[/yellow]")
        else:
            table.add_row("✓ Downloaded", f"[green]{success_count}[/green]")

        if skipped_count > 0:
            table.add_row("⊙ Up-to-date", f"[dim]{skipped_count}[/dim]")
        if failed_count > 0:
            table.add_row("✗ Failed", f"[red]{failed_count}[/red]")

        table.add_row("Total Size", f"{total_bytes / 1024:.1f} KB")
        table.add_row("Total Time", f"{total_time:.2f}s")

        if download_times:
            avg_time = sum(download_times) / len(download_times)
            table.add_row("Avg Time/Page", f"{avg_time:.2f}s")
            table.add_row("Overall Speed",
                          f"{(total_bytes / 1024) / total_time:.1f} KB/s")

        console.print(table)

    # Exit with error if any downloads failed
    if failed_count > 0:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
