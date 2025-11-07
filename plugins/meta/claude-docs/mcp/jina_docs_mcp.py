#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.0.0",
#   "httpx>=0.27.0",
#   "pydantic>=2.0.0",
# ]
# ///
"""
Jina Docs MCP Server

MCP server for downloading Claude Code documentation pages using Jina Reader API.
Optimized for parallel batch processing (3-4 URLs optimal).
"""

import os
import threading
import time
from typing import Optional, List
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict


# Initialize MCP server
mcp = FastMCP("jina_docs_mcp")


# Rate limiter for Jina API requests
class RateLimiter:
    """Rate limiter for Jina API requests."""
    
    def __init__(self, requests_per_minute: int = 20):
        """Initialize rate limiter."""
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = 0.0
        self.lock = threading.Lock()
    
    def wait_if_needed(self) -> None:
        """Wait if necessary to respect rate limits."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter(api_key: Optional[str]) -> RateLimiter:
    """Get or create rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        requests_per_minute = 500 if api_key else 20
        _rate_limiter = RateLimiter(requests_per_minute=requests_per_minute)
    return _rate_limiter


def get_api_key() -> Optional[str]:
    """Get Jina API key from environment."""
    return os.getenv("JINA_API_KEY")


BASE_URL = "https://docs.claude.com/en/docs"
CLAUDE_CODE_BASE = f"{BASE_URL}/claude-code"
AGENTS_TOOLS_BASE = f"{BASE_URL}/agents-and-tools"


# Pydantic models for input validation
class DownloadPageInput(BaseModel):
    """Input model for downloading a single page."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    url: str = Field(..., description="Full URL of the documentation page to download (e.g., 'https://docs.claude.com/en/docs/claude-code/plugins.md')")
    output_dir: Optional[str] = Field(default=None, description="Output directory path (default: auto-detect)")
    api_key: Optional[str] = Field(default=None, description="Jina API key (overrides JINA_API_KEY env var)")


class DownloadBatchInput(BaseModel):
    """Input model for downloading multiple pages in parallel."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    urls: List[str] = Field(..., description="List of full URLs to download in parallel (3-4 URLs optimal)", min_length=1, max_length=10)
    output_dir: Optional[str] = Field(default=None, description="Output directory path (default: auto-detect)")
    api_key: Optional[str] = Field(default=None, description="Jina API key (overrides JINA_API_KEY env var)")


class CheckUpdatesInput(BaseModel):
    """Input model for checking which pages need updates."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    urls: List[str] = Field(..., description="List of full URLs to check for updates", min_length=1)
    output_dir: Optional[str] = Field(default=None, description="Output directory path (default: auto-detect)")


class ListAvailableInput(BaseModel):
    """Input model for listing available documentation pages."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    section: Optional[str] = Field(default=None, description="Documentation section filter (e.g., 'claude-code', 'agents-and-tools')")


def find_or_create_output_dir(output_dir: Optional[str]) -> Path:
    """Find or create output directory."""
    if output_dir:
        return Path(output_dir)
    
    # Auto-detect: assume script is in plugins/meta/claude-docs/mcp/
    script_dir = Path(__file__).parent
    return script_dir.parent / "skills" / "claude-docs" / "reference"


async def download_page_jina(
    url: str,
    output_dir: Path,
    api_key: Optional[str],
    rate_limiter: RateLimiter,
) -> dict:
    """
    Download a single page using Jina Reader API.
    
    Args:
        url: Full URL of the page
        output_dir: Output directory
        api_key: Jina API key (optional)
        rate_limiter: Rate limiter instance
        
    Returns:
        Dictionary with success status and metadata
    """
    # Transform URL to use Jina Reader API
    jina_url = f"https://r.jina.ai/{url}"
    
    # Extract filename from URL
    filename = url.split("/")[-1]
    if not filename.endswith(".md"):
        filename += ".md"
    output_file = output_dir / filename
    
    # Prepare headers
    headers = {
        "X-Return-Format": "markdown",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        # Respect rate limits
        rate_limiter.wait_if_needed()
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(jina_url, headers=headers)
            
            if response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "url": url
                }
            
            response.raise_for_status()
            
            content = response.text
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(content)
            
            return {
                "success": True,
                "url": url,
                "filename": str(output_file),
                "size_bytes": len(content.encode('utf-8')),
                "downloaded_at": time.time()
            }
    
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}",
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


@mcp.tool(
    name="jina_docs_download_page",
    annotations={
        "title": "Download Claude Docs Page (Jina)",
        "readOnlyHint": False,  # Downloads files
        "destructiveHint": False,
        "idempotentHint": True,  # Re-downloading is safe
        "openWorldHint": True  # Accesses external URLs
    }
)
async def jina_docs_download_page(params: DownloadPageInput) -> str:
    """Download a single Claude Code documentation page using Jina Reader API.
    
    This tool downloads a documentation page from docs.claude.com using Jina Reader API
    for clean markdown extraction. The page is saved locally for offline reference.
    
    Args:
        params: Input parameters containing:
            - url: Full URL of the documentation page
            - output_dir: Optional output directory (default: auto-detect)
            - api_key: Optional Jina API key (overrides env var)
    
    Returns:
        JSON-formatted string with download result
    """
    import json
    
    api_key = params.api_key or get_api_key()
    rate_limiter = get_rate_limiter(api_key)
    output_dir = find_or_create_output_dir(params.output_dir)
    
    result = await download_page_jina(params.url, output_dir, api_key, rate_limiter)
    
    return json.dumps(result, indent=2)


@mcp.tool(
    name="jina_docs_download_batch",
    annotations={
        "title": "Download Claude Docs (Batch)",
        "readOnlyHint": False,  # Downloads files
        "destructiveHint": False,
        "idempotentHint": True,  # Re-downloading is safe
        "openWorldHint": True  # Accesses external URLs
    }
)
async def jina_docs_download_batch(params: DownloadBatchInput) -> str:
    """Download multiple Claude Code documentation pages in parallel using Jina Reader API.
    
    Optimized for batch operations with 3-4 URLs processed simultaneously. This tool
    leverages Jina Reader API's parallel processing capabilities for faster downloads.
    
    Args:
        params: Input parameters containing:
            - urls: List of full URLs to download (3-4 optimal)
            - output_dir: Optional output directory (default: auto-detect)
            - api_key: Optional Jina API key (overrides env var)
    
    Returns:
        JSON-formatted string with batch download results
    """
    import json
    import asyncio
    
    api_key = params.api_key or get_api_key()
    rate_limiter = get_rate_limiter(api_key)
    output_dir = find_or_create_output_dir(params.output_dir)
    
    # Download pages in parallel
    tasks = [
        download_page_jina(url, output_dir, api_key, rate_limiter)
        for url in params.urls
    ]
    
    results = await asyncio.gather(*tasks)
    
    return json.dumps({
        "success": all(r.get("success", False) for r in results),
        "results": results,
        "total": len(results),
        "succeeded": sum(1 for r in results if r.get("success", False)),
        "failed": sum(1 for r in results if not r.get("success", False))
    }, indent=2)


@mcp.tool(
    name="jina_docs_check_updates",
    annotations={
        "title": "Check Claude Docs Updates",
        "readOnlyHint": True,  # Only checks, doesn't download
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True  # Accesses external URLs
    }
)
async def jina_docs_check_updates(params: CheckUpdatesInput) -> str:
    """Check which Claude Code documentation pages need updating.
    
    Performs HEAD requests to compare ETags and Last-Modified headers with cached
    metadata to determine which pages have been updated.
    
    Args:
        params: Input parameters containing:
            - urls: List of full URLs to check
            - output_dir: Optional output directory (default: auto-detect)
    
    Returns:
        JSON-formatted string with update check results
    """
    import json
    
    output_dir = find_or_create_output_dir(params.output_dir)
    cache_file = output_dir / ".download_cache.json"
    
    # Load cache
    cache = {}
    if cache_file.exists():
        try:
            with cache_file.open() as f:
                cache = json.load(f)
        except Exception:
            pass
    
    results = []
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        for url in params.urls:
            try:
                response = await client.head(url)
                response.raise_for_status()
                
                etag = response.headers.get("etag")
                last_modified = response.headers.get("last-modified")
                
                filename = url.split("/")[-1]
                cached_meta = cache.get(filename, {})
                
                needs_update = True
                if etag and cached_meta.get("etag"):
                    needs_update = etag != cached_meta.get("etag")
                elif last_modified and cached_meta.get("last_modified"):
                    needs_update = last_modified != cached_meta.get("last_modified")
                
                results.append({
                    "url": url,
                    "needs_update": needs_update,
                    "etag": etag,
                    "last_modified": last_modified
                })
            except Exception as e:
                results.append({
                    "url": url,
                    "needs_update": True,
                    "error": str(e)
                })
    
    return json.dumps({
        "results": results,
        "total": len(results),
        "needs_update": sum(1 for r in results if r.get("needs_update", False))
    }, indent=2)


@mcp.tool(
    name="jina_docs_list_available",
    annotations={
        "title": "List Available Claude Docs",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True  # Accesses external URLs
    }
)
async def jina_docs_list_available(params: ListAvailableInput) -> str:
    """List all available Claude Code documentation pages.
    
    Fetches the documentation map and extracts all available page URLs.
    Optionally filters by section (claude-code, agents-and-tools).
    
    Args:
        params: Input parameters containing:
            - section: Optional section filter
    
    Returns:
        JSON-formatted string with list of available pages
    """
    import json
    import re
    
    docs_map_url = f"{CLAUDE_CODE_BASE}/claude_code_docs_map.md"
    jina_url = f"https://r.jina.ai/{docs_map_url}"
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(jina_url)
            response.raise_for_status()
            content = response.text
            
            # Extract paths from markdown links
            pattern = r'###\s+\[[^\]]+\]\(https://docs\.claude\.com/en/docs/claude-code/([^)]+)\.md\)'
            matches = re.findall(pattern, content)
            
            pages = []
            for page_path in matches:
                section = "claude-code"
                if params.section and params.section != section:
                    continue
                
                base_url = CLAUDE_CODE_BASE if section == "claude-code" else AGENTS_TOOLS_BASE
                url = f"{base_url}/{page_path}.md"
                pages.append({
                    "section": section,
                    "path": page_path,
                    "url": url
                })
            
            return json.dumps({
                "success": True,
                "pages": pages,
                "total": len(pages)
            }, indent=2)
    
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


if __name__ == "__main__":
    mcp.run()
