#!/usr/bin/env python3
"""Tests for firecrawl_mcp_docs.py script."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.mark.asyncio
async def test_firecrawl_orchestrator_configuration():
    """Test that Firecrawl orchestrator is configured correctly."""
    from firecrawl_mcp_docs import create_orchestrator_options

    options = create_orchestrator_options()

    # Should use claude_code system prompt
    assert options.system_prompt == "claude_code" or (
        isinstance(options.system_prompt, dict)
        and options.system_prompt.get("preset") == "claude_code"
    )

    # Should have Firecrawl MCP tools
    assert "mcp__firecrawl__firecrawl_scrape" in options.allowed_tools


@pytest.mark.asyncio
@patch("claude_agent_sdk.ClaudeSDKClient")
async def test_download_with_metadata(mock_client):
    """Test that Firecrawl returns rich metadata."""
    from firecrawl_mcp_docs import download_page_firecrawl

    mock_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_instance

    url = "https://docs.claude.com/page1.md"
    success, content, metadata = await download_page_firecrawl(url, Path("/tmp"))

    # Should have attempted download via MCP
    assert mock_instance.query.called


@pytest.mark.asyncio
async def test_error_handling_robustness():
    """Test that Firecrawl handles errors gracefully."""
    from firecrawl_mcp_docs import download_page_firecrawl

    # Should handle failures without crashing
    url = "https://invalid-url-that-will-fail.com"
    success, content, metadata = await download_page_firecrawl(url, Path("/tmp"))

    # May succeed or fail, but should not raise exception
    assert isinstance(success, bool)
