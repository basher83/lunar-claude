#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
#   "typer>=0.12.0",
#   "beautifulsoup4>=4.12.0",
# ]
# ///
"""
Hybrid Claude Code Documentation Sync.

Combines auto-discovery with clean output:
- Recursive crawling + llms.txt discovery
- ETag/Last-Modified + MD5 change detection
- Direct .md fetching only (no HTML fallback)
- Tiered storage: core/extended/full-site
- Clean filenames matching claude_docs.py style

Usage:
    ./sync_docs.py                  # Sync core docs
    ./sync_docs.py --extended       # Include extended docs
    ./sync_docs.py --all            # Full site mirror
    ./sync_docs.py --check          # Check for updates (dry-run)
    ./sync_docs.py --verbose        # Show all debug output
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urljoin, urlparse

import httpx
import typer
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

if TYPE_CHECKING:
    pass

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

BASE_URL = "https://docs.claude.com"
LLMS_TXT_URL = "https://docs.claude.com/llms.txt"

# Seed URLs for recursive discovery
SEED_URLS = [
    "https://docs.claude.com/en/docs/intro",
    "https://docs.claude.com/en/docs/claude-code/overview",
    "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview",
]

# URL patterns that define each tier
# Core: Essential for Claude Code plugin/skill development
CORE_PATTERNS = [
    r"/agent-sdk/",           # Agent SDK docs (plugins, skills, etc.)
    r"/agent-skills/",        # Agent Skills API
]

# Extended: Useful but not always needed
EXTENDED_PATTERNS = [
    r"/agents-and-tools/",    # Tool use, MCP, etc.
    r"/build-with-claude/prompt-engineering/",  # Prompt engineering guides
]

# Pages to always include in core (by page name suffix after flattening)
# These override the pattern-based classification
CORE_PAGES = {
    "plugins",
    "plugins-reference",
    "plugin-marketplaces",
    "skills",
    "hooks",
    "hooks-guide",
    "slash-commands",
    "sub-agents",
    "settings",
    "mcp",
    "memory",
    "output-styles",
    "statusline",
    "overview",  # Agent SDK overview
    "permissions",
    "sessions",
    "custom-tools",
    "modifying-system-prompts",
}

console = Console()

# Global verbose flag - set by main()
VERBOSE = False


class OutputFormat(str, Enum):
    """Output format for the script."""

    RICH = "rich"
    JSON = "json"


class Tier(str, Enum):
    """Documentation tier classification."""

    CORE = "core"
    EXTENDED = "extended"
    FULL = "full"


class DownloadStatus(str, Enum):
    """Result status of a download attempt."""

    SUCCESS = "success"
    UNCHANGED = "unchanged"  # Content hash matched
    FETCH_FAILED = "fetch_failed"


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------


@dataclass
class PageMeta:
    """Metadata for a documentation page."""

    url: str
    tier: str = "full"
    etag: str | None = None
    last_modified: str | None = None
    content_hash: str | None = None
    downloaded_at: float = 0.0
    size_bytes: int = 0


@dataclass
class SyncCache:
    """Cache for sync state."""

    pages: dict[str, PageMeta] = field(default_factory=dict)
    discovered_at: float = 0.0
    discovery_method: str = ""


@dataclass
class SyncResult:
    """Result of a sync operation."""

    status: str
    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    total_bytes: int = 0
    duration_seconds: float = 0.0


# -----------------------------------------------------------------------------
# Cache Management
# -----------------------------------------------------------------------------


def load_cache(cache_file: Path) -> SyncCache:
    """Load sync cache from JSON file."""
    if not cache_file.exists():
        return SyncCache()

    try:
        data = json.loads(cache_file.read_text())
        pages = {}
        for name, meta in data.get("pages", {}).items():
            pages[name] = PageMeta(
                url=meta.get("url", ""),
                tier=meta.get("tier", "full"),
                etag=meta.get("etag"),
                last_modified=meta.get("last_modified"),
                content_hash=meta.get("content_hash"),
                downloaded_at=meta.get("downloaded_at", 0.0),
                size_bytes=meta.get("size_bytes", 0),
            )
        return SyncCache(
            pages=pages,
            discovered_at=data.get("discovered_at", 0.0),
            discovery_method=data.get("discovery_method", ""),
        )
    except json.JSONDecodeError as e:
        console.print(f"[yellow]Warning: Cache file corrupted (invalid JSON): {e}[/yellow]")
        console.print("[yellow]Starting fresh - all files will be re-checked[/yellow]")
        return SyncCache()
    except (TypeError, KeyError, ValueError) as e:
        console.print(f"[yellow]Warning: Cache file has invalid structure: {e}[/yellow]")
        console.print("[yellow]Starting fresh - all files will be re-checked[/yellow]")
        return SyncCache()
    except OSError as e:
        console.print(f"[red]Error reading cache file: {e}[/red]")
        console.print("[yellow]Starting fresh - all files will be re-checked[/yellow]")
        return SyncCache()


def save_cache(cache_file: Path, cache: SyncCache) -> None:
    """Save sync cache to JSON file."""
    data = {
        "discovered_at": cache.discovered_at,
        "discovery_method": cache.discovery_method,
        "pages": {
            name: {
                "url": meta.url,
                "tier": meta.tier,
                "etag": meta.etag,
                "last_modified": meta.last_modified,
                "content_hash": meta.content_hash,
                "downloaded_at": meta.downloaded_at,
                "size_bytes": meta.size_bytes,
            }
            for name, meta in cache.pages.items()
        },
    }
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write: write to temp file, then rename
        temp_file = cache_file.with_suffix(".tmp")
        temp_file.write_text(json.dumps(data, indent=2))
        temp_file.replace(cache_file)  # Atomic on POSIX systems
    except PermissionError:
        console.print(f"[red]Error: Cannot write cache file (permission denied): {cache_file}[/red]")
        console.print("[yellow]Sync state will not be preserved for next run[/yellow]")
    except OSError as e:
        console.print(f"[red]Error saving cache: {e}[/red]")
        console.print("[yellow]Sync state will not be preserved for next run[/yellow]")


# -----------------------------------------------------------------------------
# URL Classification
# -----------------------------------------------------------------------------


def classify_tier(url: str) -> str:
    """Classify a URL into a tier based on patterns."""
    path = urlparse(url).path

    # Extract page name for core page matching
    page_name = path.rstrip("/").split("/")[-1]
    if page_name in CORE_PAGES:
        return Tier.CORE.value

    # Check core patterns
    for pattern in CORE_PATTERNS:
        if re.search(pattern, path):
            return Tier.CORE.value

    # Check extended patterns
    for pattern in EXTENDED_PATTERNS:
        if re.search(pattern, path):
            return Tier.EXTENDED.value

    return Tier.FULL.value


def normalize_url(url: str) -> str:
    """Normalize URL by removing fragments and trailing slashes."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    # Skip malformed URLs that have /docs/en/ instead of /en/docs/
    # These cause redirect loops
    if "/docs/en/" in path:
        if VERBOSE:
            console.print(f"  [dim]Skipping malformed URL (redirect loop pattern): {url}[/dim]")
        return ""

    return f"{parsed.scheme}://{parsed.netloc}{path}"


def url_to_page_name(url: str) -> str:
    """Convert URL to a clean, meaningful page name.

    Extracts just the meaningful part of the path, not the full hierarchy.
    e.g., /en/docs/agents-and-tools/agent-skills/best-practices -> agent-skills-best-practices
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")

    # Security: Reject paths with traversal attempts
    if ".." in path:
        console.print(f"[red]Security: Rejecting path with traversal attempt: {url}[/red]")
        return ""

    # Remove /en/docs/ or /en/release-notes/ prefix
    if path.startswith("en/docs/"):
        path = path[8:]  # len("en/docs/")
    elif path.startswith("en/release-notes/"):
        path = path[17:]  # len("en/release-notes/")
    elif path.startswith("en/"):
        path = path[3:]

    # Remove .md suffix if present
    if path.endswith(".md"):
        path = path[:-3]

    # Strip common section prefixes to get meaningful name
    # e.g., "agents-and-tools/agent-skills/best-practices" -> "agent-skills/best-practices"
    section_prefixes = [
        "claude-code/",
        "agents-and-tools/",
        "build-with-claude/",
        "about-claude/",
        "test-and-evaluate/",
    ]
    for prefix in section_prefixes:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break

    # Replace slashes with dashes for flat storage
    return path.replace("/", "-")


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def discover_via_crawl(
    client: httpx.Client,
    seed_urls: list[str],
    max_depth: int = 5,
    delay: float = 0.3,
) -> dict[str, PageMeta]:
    """
    Discover documentation pages by recursively crawling from seed URLs.

    This finds pages that may not be in llms.txt or other indexes.
    """
    discovered: dict[str, PageMeta] = {}
    to_visit: list[tuple[str, int]] = [(url, 0) for url in seed_urls]
    visited: set[str] = set()
    discovery_failures = 0

    console.print("[cyan]Discovering pages via crawl...[/cyan]")

    while to_visit:
        url, depth = to_visit.pop(0)
        url = normalize_url(url)

        # Skip empty URLs (from malformed paths) or already visited
        if not url or url in visited or depth > max_depth:
            continue

        visited.add(url)

        # Only process docs.claude.com URLs
        if not url.startswith(BASE_URL):
            continue

        try:
            response = client.get(url, timeout=15.0)

            if response.status_code == 404:
                continue

            response.raise_for_status()

            # Check if it's a documentation page
            parsed = urlparse(url)
            if "/docs/" in parsed.path or "/release-notes/" in parsed.path:
                page_name = url_to_page_name(url)
                tier = classify_tier(url)
                discovered[page_name] = PageMeta(url=url, tier=tier)
                console.print(f"  [dim]Found:[/dim] {page_name} [dim]({tier})[/dim]")

            # Parse HTML to find more links
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                absolute_url = urljoin(url, href)

                # Validate immediately - reject external URLs before normalization
                if not absolute_url.startswith(BASE_URL):
                    continue

                absolute_url = normalize_url(absolute_url)

                # Skip empty URLs (from malformed paths)
                if not absolute_url:
                    continue

                # Follow docs and release-notes links
                if absolute_url not in visited:
                    parsed_link = urlparse(absolute_url)
                    if "/docs/" in parsed_link.path or "/release-notes/" in parsed_link.path:
                        to_visit.append((absolute_url, depth + 1))

            time.sleep(delay)

        except httpx.HTTPStatusError as e:
            if e.response.status_code != 404:
                console.print(f"  [yellow]HTTP {e.response.status_code}: {url}[/yellow]")
                discovery_failures += 1
            time.sleep(delay)
            continue
        except httpx.TimeoutException:
            console.print(f"  [yellow]Timeout: {url} - skipping[/yellow]")
            discovery_failures += 1
            time.sleep(delay)
            continue
        except httpx.RequestError as e:
            console.print(f"  [yellow]Network error for {url}: {type(e).__name__}[/yellow]")
            discovery_failures += 1
            time.sleep(delay)
            continue

    if discovery_failures > 0:
        console.print(f"[yellow]Warning: {discovery_failures} URLs failed during crawl[/yellow]")
        if len(discovered) > 0 and discovery_failures > len(discovered) * 0.2:
            console.print("[yellow]High failure rate - consider re-running with --rediscover[/yellow]")

    console.print(f"[green]Crawl complete: {len(discovered)} pages found[/green]")
    return discovered


def discover_via_llms_txt(client: httpx.Client) -> dict[str, PageMeta]:
    """
    Discover documentation pages from llms.txt.

    This is a fast supplementary method that catches pages listed in the sitemap.
    """
    console.print("[cyan]Discovering pages from llms.txt...[/cyan]")

    try:
        response = client.get(LLMS_TXT_URL, timeout=30.0)
        response.raise_for_status()

        discovered: dict[str, PageMeta] = {}
        # Match all docs and release-notes pages
        pattern = re.compile(
            r"https://docs\.claude\.com/en/(?:docs|release-notes)/[^\s)]+\.md"
        )

        for match in pattern.finditer(response.text):
            url = match.group(0)
            # Remove .md suffix for the page URL
            page_url = url[:-3] if url.endswith(".md") else url
            page_name = url_to_page_name(page_url)
            tier = classify_tier(page_url)
            discovered[page_name] = PageMeta(url=page_url, tier=tier)

        console.print(f"[green]llms.txt: {len(discovered)} pages found[/green]")
        return discovered

    except httpx.TimeoutException:
        console.print("[yellow]Warning: llms.txt fetch timed out - using crawl results only[/yellow]")
        return {}
    except httpx.HTTPStatusError as e:
        console.print(f"[yellow]Warning: llms.txt returned HTTP {e.response.status_code}[/yellow]")
        return {}
    except httpx.RequestError as e:
        console.print(f"[yellow]Network error fetching llms.txt ({type(e).__name__}): {e}[/yellow]")
        return {}


def discover_all(
    client: httpx.Client,
    use_crawl: bool = True,
    use_llms_txt: bool = True,
) -> dict[str, PageMeta]:
    """
    Discover all documentation pages using multiple methods.

    Combines crawling and llms.txt for comprehensive coverage.
    """
    all_pages: dict[str, PageMeta] = {}

    if use_crawl:
        crawled = discover_via_crawl(client, SEED_URLS)
        all_pages.update(crawled)

    if use_llms_txt:
        from_llms = discover_via_llms_txt(client)
        # Merge, preferring crawled data (has more accurate tier info)
        for name, meta in from_llms.items():
            if name not in all_pages:
                all_pages[name] = meta

    # Summary by tier
    tiers = {"core": 0, "extended": 0, "full": 0}
    for meta in all_pages.values():
        tiers[meta.tier] = tiers.get(meta.tier, 0) + 1

    console.print(
        f"\n[bold]Discovery complete:[/bold] {len(all_pages)} total pages\n"
        f"  Core: {tiers['core']} | Extended: {tiers['extended']} | Full: {tiers['full']}"
    )

    return all_pages


# -----------------------------------------------------------------------------
# Change Detection
# -----------------------------------------------------------------------------


def calculate_md5(content: str) -> str:
    """Calculate MD5 hash of content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def check_for_changes(
    client: httpx.Client,
    url: str,
    cached_meta: PageMeta | None,
) -> tuple[bool, str | None, str | None]:
    """
    Check if a page needs to be downloaded.

    Uses HEAD request to check ETag/Last-Modified headers.
    Returns (needs_update, etag, last_modified).
    """
    try:
        # Try .md URL first
        md_url = f"{url}.md" if not url.endswith(".md") else url
        response = client.head(md_url, timeout=10.0)

        if response.status_code == 404:
            # Fallback to HTML URL
            response = client.head(url, timeout=10.0)

        if response.status_code >= 400:
            return True, None, None

        etag = response.headers.get("etag")
        last_modified = response.headers.get("last-modified")

        if not cached_meta:
            return True, etag, last_modified

        # Compare ETag
        if etag and cached_meta.etag and etag == cached_meta.etag:
            return False, etag, last_modified

        # Compare Last-Modified
        if (
            last_modified
            and cached_meta.last_modified
            and last_modified == cached_meta.last_modified
        ):
            return False, etag, last_modified

        return True, etag, last_modified

    except httpx.TimeoutException:
        console.print(f"  [dim]HEAD timeout for {url} - will attempt full download[/dim]")
        return True, None, None
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 429:
            console.print(f"  [yellow]Rate limited checking {url} - backing off[/yellow]")
            time.sleep(2.0)  # Back off on rate limit
        elif status in (401, 403):
            console.print(f"  [red]Access denied ({status}) for {url}[/red]")
        elif status >= 500:
            console.print(f"  [yellow]Server error {status} checking {url}[/yellow]")
        return True, None, None
    except httpx.RequestError as e:
        console.print(f"  [yellow]Network error checking {url}: {type(e).__name__}[/yellow]")
        return True, None, None


# -----------------------------------------------------------------------------
# Content Fetching
# -----------------------------------------------------------------------------


def fetch_markdown(client: httpx.Client, url: str, verbose: bool = False) -> str | None:
    """
    Fetch markdown content directly from .md endpoint.

    No HTML fallback - if .md fails, returns None.
    This ensures consistent, clean markdown output.
    """
    md_url = f"{url}.md" if not url.endswith(".md") else url

    try:
        response = client.get(md_url, timeout=30.0)

        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            if verbose:
                console.print(f"  [dim]No .md endpoint: {url}[/dim]")
            return None
        else:
            console.print(f"  [yellow].md returned {response.status_code}: {url}[/yellow]")
            return None

    except httpx.TimeoutException:
        console.print(f"  [yellow]Timeout fetching: {md_url}[/yellow]")
        return None
    except httpx.RequestError as e:
        console.print(f"  [yellow]Error fetching {md_url}: {type(e).__name__}[/yellow]")
        return None


def download_page(
    client: httpx.Client,
    page_name: str,
    meta: PageMeta,
    output_dir: Path,
    etag: str | None,
    last_modified: str | None,
) -> tuple[DownloadStatus, PageMeta]:
    """
    Download a single documentation page.

    Returns (status, updated_meta).
    """
    content = fetch_markdown(client, meta.url)

    if not content:
        return DownloadStatus.FETCH_FAILED, meta

    # Calculate content hash for change detection
    content_hash = calculate_md5(content)

    # Skip if content hasn't actually changed (MD5 check)
    if meta.content_hash and meta.content_hash == content_hash:
        return DownloadStatus.UNCHANGED, meta

    # Determine output path based on tier
    tier_dir = output_dir / meta.tier
    output_file = tier_dir / f"{page_name}.md"

    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content)
    except PermissionError:
        console.print(f"[red]Permission denied writing {output_file}[/red]")
        return DownloadStatus.FETCH_FAILED, meta
    except OSError as e:
        console.print(f"[red]Failed to write {output_file}: {e}[/red]")
        return DownloadStatus.FETCH_FAILED, meta

    # Update metadata
    updated_meta = PageMeta(
        url=meta.url,
        tier=meta.tier,
        etag=etag,
        last_modified=last_modified,
        content_hash=content_hash,
        downloaded_at=time.time(),
        size_bytes=len(content.encode("utf-8")),
    )

    return DownloadStatus.SUCCESS, updated_meta


# -----------------------------------------------------------------------------
# Main Sync Logic
# -----------------------------------------------------------------------------


def get_default_output_dir() -> Path:
    """Get the default output directory relative to this script."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "skills" / "official_docs" / "references"


def main(
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Directory to save documentation (default: auto-detect)",
    ),
    extended: bool = typer.Option(
        False,
        "--extended",
        "-e",
        help="Include extended docs (agents, prompt engineering)",
    ),
    all_docs: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Download all documentation (full site mirror)",
    ),
    check_only: bool = typer.Option(
        False,
        "--check",
        "-c",
        help="Check for updates without downloading (dry-run)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force re-download all files (ignore cache)",
    ),
    rediscover: bool = typer.Option(
        False,
        "--rediscover",
        "-r",
        help="Re-crawl site to discover new pages",
    ),
    format_output: OutputFormat = typer.Option(
        OutputFormat.RICH,
        "--format",
        help="Output format: 'rich' or 'json'",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed debug output",
    ),
) -> None:
    """
    Sync Claude Code documentation from docs.claude.com.

    By default, syncs only core Claude Code docs (~25 files).
    Use --extended for additional docs, --all for full site mirror.
    """
    global VERBOSE
    VERBOSE = verbose

    # Determine output directory
    if output_dir is None:
        output_dir = get_default_output_dir()

    output_dir.mkdir(parents=True, exist_ok=True)

    # Early validation: ensure we can write to the output directory
    test_file = output_dir / ".write_test"
    try:
        test_file.write_text("test")
        test_file.unlink()
    except (PermissionError, OSError) as e:
        console.print(f"[red]Cannot write to output directory: {output_dir}[/red]")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)

    # Load cache
    cache_file = output_dir / ".sync_cache.json"
    cache = load_cache(cache_file)

    # Determine which tiers to sync
    tiers_to_sync = {Tier.CORE.value}
    if extended:
        tiers_to_sync.add(Tier.EXTENDED.value)
    if all_docs:
        tiers_to_sync = {Tier.CORE.value, Tier.EXTENDED.value, Tier.FULL.value}

    if format_output == OutputFormat.RICH:
        tier_str = ", ".join(sorted(tiers_to_sync))
        console.print("\n[bold]Claude Code Documentation Sync[/bold]")
        console.print(f"Output: {output_dir.absolute()}")
        console.print(f"Tiers: {tier_str}")
        if check_only:
            console.print("[yellow]DRY RUN - no files will be downloaded[/yellow]")
        console.print()

    start_time = time.time()

    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        # Discovery phase
        discovery_age = time.time() - cache.discovered_at
        needs_discovery = (
            rediscover or not cache.pages or discovery_age > 86400  # 24 hours
        )

        if needs_discovery:
            discovered = discover_all(client, use_crawl=True, use_llms_txt=True)

            # Validate discovery results
            if not discovered and not cache.pages:
                console.print("[red]Error: Discovery found no pages and cache is empty[/red]")
                console.print("[red]Check network connectivity and try again[/red]")
                raise typer.Exit(code=1)

            if discovered and len(discovered) < 10:
                console.print(
                    f"[yellow]Warning: Only {len(discovered)} pages discovered "
                    f"(expected 50+)[/yellow]"
                )

            # Merge with existing cache to preserve metadata
            for name, meta in discovered.items():
                if name in cache.pages:
                    # Preserve existing metadata
                    meta.etag = cache.pages[name].etag
                    meta.last_modified = cache.pages[name].last_modified
                    meta.content_hash = cache.pages[name].content_hash
                    meta.downloaded_at = cache.pages[name].downloaded_at
                    meta.size_bytes = cache.pages[name].size_bytes
                cache.pages[name] = meta

            cache.discovered_at = time.time()
            cache.discovery_method = "crawl+llms_txt"

            if format_output == OutputFormat.RICH:
                console.print()

        # Filter pages by tier
        pages_to_sync = {
            name: meta
            for name, meta in cache.pages.items()
            if meta.tier in tiers_to_sync
        }

        if format_output == OutputFormat.RICH:
            console.print(
                f"[cyan]{'Checking' if check_only else 'Syncing'} "
                f"{len(pages_to_sync)} pages...[/cyan]\n"
            )

        # Sync phase
        downloaded = 0
        skipped = 0
        failed = 0
        total_bytes = 0

        if format_output == OutputFormat.RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Syncing...", total=len(pages_to_sync))

                for name, meta in pages_to_sync.items():
                    progress.update(task, description=f"[cyan]Checking {name}...")

                    # Check for changes via headers
                    if not force:
                        needs_update, etag, last_mod = check_for_changes(
                            client, meta.url, meta
                        )
                        if not needs_update:
                            console.print(f"[dim]⊙ {name} (unchanged)[/dim]")
                            skipped += 1
                            progress.advance(task)
                            continue
                    else:
                        etag, last_mod = None, None

                    if check_only:
                        console.print(f"[yellow]↻ {name} (update available)[/yellow]")
                        downloaded += 1
                        progress.advance(task)
                        continue

                    # Download
                    progress.update(task, description=f"[cyan]Downloading {name}...")
                    status, updated_meta = download_page(
                        client, name, meta, output_dir, etag, last_mod
                    )

                    if status == DownloadStatus.SUCCESS:
                        console.print(
                            f"[green]✓[/green] {name} "
                            f"[dim]({updated_meta.size_bytes / 1024:.1f}KB)[/dim]"
                        )
                        cache.pages[name] = updated_meta
                        downloaded += 1
                        total_bytes += updated_meta.size_bytes
                    elif status == DownloadStatus.UNCHANGED:
                        console.print(f"[dim]⊙ {name} (content unchanged)[/dim]")
                        skipped += 1
                    else:  # FETCH_FAILED
                        console.print(f"[red]✗ {name} (failed)[/red]")
                        failed += 1

                    progress.advance(task)
                    time.sleep(0.2)  # Be polite to the server
        else:
            # JSON mode - silent operation
            for name, meta in pages_to_sync.items():
                if not force:
                    needs_update, etag, last_mod = check_for_changes(
                        client, meta.url, meta
                    )
                    if not needs_update:
                        skipped += 1
                        continue
                else:
                    etag, last_mod = None, None

                if check_only:
                    downloaded += 1
                    continue

                status, updated_meta = download_page(
                    client, name, meta, output_dir, etag, last_mod
                )

                if status == DownloadStatus.SUCCESS:
                    cache.pages[name] = updated_meta
                    downloaded += 1
                    total_bytes += updated_meta.size_bytes
                elif status == DownloadStatus.UNCHANGED:
                    skipped += 1
                else:  # FETCH_FAILED
                    failed += 1

                time.sleep(0.2)

    # Save cache
    save_cache(cache_file, cache)

    duration = time.time() - start_time

    # Output results
    result = SyncResult(
        status="success" if failed == 0 else "error",
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
        total_bytes=total_bytes,
        duration_seconds=round(duration, 2),
    )

    if format_output == OutputFormat.JSON:
        output = {
            "status": result.status,
            "downloaded": result.downloaded,
            "skipped": result.skipped,
            "failed": result.failed,
            "total_bytes": result.total_bytes,
            "duration_seconds": result.duration_seconds,
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(output))
    else:
        console.print()
        table = Table(
            title="Sync Summary" if not check_only else "Update Check Summary",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Pages", str(len(pages_to_sync)))

        if check_only:
            table.add_row("↻ Updates Available", f"[yellow]{downloaded}[/yellow]")
        else:
            table.add_row("✓ Downloaded", f"[green]{downloaded}[/green]")

        if skipped > 0:
            table.add_row("⊙ Unchanged", f"[dim]{skipped}[/dim]")
        if failed > 0:
            table.add_row("✗ Failed", f"[red]{failed}[/red]")

        table.add_row("Total Size", f"{total_bytes / 1024:.1f} KB")
        table.add_row("Duration", f"{duration:.2f}s")

        console.print(table)

        # Tier breakdown
        console.print("\n[bold]Pages by Tier:[/bold]")
        for tier in sorted(tiers_to_sync):
            count = sum(1 for m in cache.pages.values() if m.tier == tier)
            console.print(f"  {tier}: {count} pages")

    if failed > 0:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
