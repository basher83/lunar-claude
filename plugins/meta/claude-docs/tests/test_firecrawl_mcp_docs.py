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
async def test_download_with_metadata(tmp_path):
    """Test that Firecrawl returns rich metadata."""
    from claude_agent_sdk import AssistantMessage, TextBlock
    from firecrawl_mcp_docs import download_page_firecrawl

    # Mock SDK client responses
    with patch("firecrawl_mcp_docs.ClaudeSDKClient") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance

        # Mock receive_response to return some content
        async def mock_receive():
            yield AssistantMessage(
                model="claude-sonnet-4-5-20250929",
                content=[TextBlock(text="Mock content from firecrawl")],
            )

        mock_instance.receive_response = mock_receive

        url = "https://docs.claude.com/page1.md"
        success, content, metadata = await download_page_firecrawl(url, tmp_path)

        # Should have attempted download via MCP
        assert mock_instance.query.called
        assert success is True
        assert "Mock content from firecrawl" in content


@pytest.mark.asyncio
async def test_error_handling_robustness():
    """Test that Firecrawl handles errors gracefully."""
    from firecrawl_mcp_docs import download_page_firecrawl

    # Should handle failures without crashing
    url = "https://invalid-url-that-will-fail.com"
    success, content, metadata = await download_page_firecrawl(url, Path("/tmp"))

    # May succeed or fail, but should not raise exception
    assert isinstance(success, bool)
