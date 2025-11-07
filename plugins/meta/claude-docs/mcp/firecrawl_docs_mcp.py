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
Firecrawl Docs MCP Server

MCP server for downloading Claude Code documentation pages using Firecrawl API.
Optimized for reliability and enhanced error handling.
"""

import os
import time
from typing import Optional, List
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict


# Initialize MCP server
mcp = FastMCP("firecrawl_docs_mcp")


FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0/scrape"

BASE_URL = "https://docs.claude.com/en/docs"
CLAUDE_CODE_BASE = f"{BASE_URL}/claude-code"
AGENTS_TOOLS_BASE = f"{BASE_URL}/agents-and-tools"


def get_api_key() -> Optional[str]:
    """Get Firecrawl API key from environment."""
    return os.getenv("FIRECRAWL_API_KEY")


# Pydantic models for input validation
class ScrapePageInput(BaseModel):
    """Input model for scraping a single page."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    url: str = Field(..., description="Full URL of the documentation page to scrape (e.g., 'https://docs.claude.com/en/docs/claude-code/plugins.md')")
    output_dir: Optional[str] = Field(default=None, description="Output directory path (default: auto-detect)")
    api_key: Optional[str] = Field(default=None, description="Firecrawl API key (overrides FIRECRAWL_API_KEY env var)")
    only_main_content: bool = Field(default=True, description="Extract only main content (reduces size)")


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


class ExtractMetadataInput(BaseModel):
    """Input model for extracting metadata from a page."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    url: str = Field(..., description="Full URL of the page to extract metadata from")
    api_key: Optional[str] = Field(default=None, description="Firecrawl API key (overrides FIRECRAWL_API_KEY env var)")


def find_or_create_output_dir(output_dir: Optional[str]) -> Path:
    """Find or create output directory."""
    if output_dir:
        return Path(output_dir)
    
    # Auto-detect: assume script is in plugins/meta/claude-docs/mcp/
    script_dir = Path(__file__).parent
    return script_dir.parent / "skills" / "claude-docs" / "reference"


async def scrape_page_firecrawl(
    url: str,
    output_dir: Path,
    api_key: Optional[str],
    only_main_content: bool = True,
) -> dict:
    """
    Scrape a single page using Firecrawl API.
    
    Args:
        url: Full URL of the page
        output_dir: Output directory
        api_key: Firecrawl API key (required)
        only_main_content: Extract only main content
        
    Returns:
        Dictionary with success status and metadata
    """
    if not api_key:
        return {
            "success": False,
            "error": "Firecrawl API key required (set FIRECRAWL_API_KEY env var)",
            "url": url
        }
    
    # Extract filename from URL
    filename = url.split("/")[-1]
    if not filename.endswith(".md"):
        filename += ".md"
    output_file = output_dir / filename
    
    # Prepare headers and payload
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": only_main_content,
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.post(
                FIRECRAWL_API_URL,
                json=payload,
                headers=headers
            )
            
            if response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "url": url
                }
            
            if response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid API key",
                    "url": url
                }
            
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get("success"):
                error_msg = result.get("error", "Unknown error")
                return {
                    "success": False,
                    "error": f"Firecrawl API error: {error_msg}",
                    "url": url
                }
            
            # Extract markdown content
            data = result.get("data", {})
            content = data.get("markdown", "")
            
            if not content:
                content = data.get("content", "")
            
            if not content:
                return {
                    "success": False,
                    "error": "No markdown content in Firecrawl response",
                    "url": url
                }
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(content)
            
            return {
                "success": True,
                "url": url,
                "filename": str(output_file),
                "size_bytes": len(content.encode('utf-8')),
                "downloaded_at": time.time(),
                "firecrawl_status": result.get("status", "unknown"),
                "credits_used": result.get("creditsUsed")
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
    name="firecrawl_docs_scrape_page",
    annotations={
        "title": "Scrape Claude Docs Page (Firecrawl)",
        "readOnlyHint": False,  # Downloads files
        "destructiveHint": False,
        "idempotentHint": True,  # Re-downloading is safe
        "openWorldHint": True  # Accesses external URLs
    }
)
async def firecrawl_docs_scrape_page(params: ScrapePageInput) -> str:
    """Scrape a single Claude Code documentation page using Firecrawl API.
    
    This tool scrapes a documentation page from docs.claude.com using Firecrawl API
    for enhanced reliability and better handling of large/complex pages. The page
    is saved locally for offline reference.
    
    Args:
        params: Input parameters containing:
            - url: Full URL of the documentation page
            - output_dir: Optional output directory (default: auto-detect)
            - api_key: Optional Firecrawl API key (overrides env var)
            - only_main_content: Extract only main content (default: True)
    
    Returns:
        JSON-formatted string with scrape result
    """
    import json
    
    api_key = params.api_key or get_api_key()
    output_dir = find_or_create_output_dir(params.output_dir)
    
    result = await scrape_page_firecrawl(
        params.url,
        output_dir,
        api_key,
        params.only_main_content
    )
    
    return json.dumps(result, indent=2)


@mcp.tool(
    name="firecrawl_docs_check_updates",
    annotations={
        "title": "Check Claude Docs Updates",
        "readOnlyHint": True,  # Only checks, doesn't download
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True  # Accesses external URLs
    }
)
async def firecrawl_docs_check_updates(params: CheckUpdatesInput) -> str:
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
    name="firecrawl_docs_list_available",
    annotations={
        "title": "List Available Claude Docs",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True  # Accesses external URLs
    }
)
async def firecrawl_docs_list_available(params: ListAvailableInput) -> str:
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
    api_key = get_api_key()
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            # Try Firecrawl first, fallback to direct HTTP
            if api_key:
                headers = {"Authorization": f"Bearer {api_key}"}
                payload = {
                    "url": docs_map_url,
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                }
                
                try:
                    response = await client.post(
                        FIRECRAWL_API_URL,
                        json=payload,
                        headers=headers,
                        timeout=30.0
                    )
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            data = result.get("data", {})
                            content = data.get("markdown", "") or data.get("content", "")
                        else:
                            raise ValueError("Firecrawl API error")
                    else:
                        raise ValueError(f"HTTP {response.status_code}")
                except Exception:
                    # Fallback to direct HTTP
                    response = await client.get(docs_map_url)
                    response.raise_for_status()
                    content = response.text
            else:
                # Direct HTTP if no API key
                response = await client.get(docs_map_url)
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


@mcp.tool(
    name="firecrawl_docs_extract_metadata",
    annotations={
        "title": "Extract Metadata from Claude Docs Page",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True  # Accesses external URLs
    }
)
async def firecrawl_docs_extract_metadata(params: ExtractMetadataInput) -> str:
    """Extract structured metadata from a Claude Code documentation page using Firecrawl.
    
    Uses Firecrawl API to extract rich metadata including status, cache info, and
    credits used. This is useful for monitoring and understanding page characteristics.
    
    Args:
        params: Input parameters containing:
            - url: Full URL of the page
            - api_key: Optional Firecrawl API key (overrides env var)
    
    Returns:
        JSON-formatted string with extracted metadata
    """
    import json
    
    api_key = params.api_key or get_api_key()
    
    if not api_key:
        return json.dumps({
            "success": False,
            "error": "Firecrawl API key required (set FIRECRAWL_API_KEY env var)"
        }, indent=2)
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "url": params.url,
        "formats": ["markdown"],
        "onlyMainContent": True,
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.post(
                FIRECRAWL_API_URL,
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", {})
                return json.dumps({
                    "success": True,
                    "url": params.url,
                    "status": result.get("status", "unknown"),
                    "credits_used": result.get("creditsUsed"),
                    "metadata": {
                        "title": data.get("title"),
                        "description": data.get("description"),
                        "language": data.get("language"),
                        "author": data.get("author"),
                        "published_time": data.get("publishedTime"),
                    },
                    "content_length": len(data.get("markdown", "") or data.get("content", ""))
                }, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "url": params.url
                }, indent=2)
    
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "url": params.url
        }, indent=2)


if __name__ == "__main__":
    mcp.run()
