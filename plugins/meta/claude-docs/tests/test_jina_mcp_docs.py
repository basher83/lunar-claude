#!/usr/bin/env python3
"""Tests for jina_mcp_docs.py script."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def test_batch_urls_optimal_size():
    """Test that URLs are batched in optimal sizes (3-4 URLs)."""
    from jina_mcp_docs import batch_urls

    urls = [f"https://example.com/page{i}.md" for i in range(10)]
    batches = list(batch_urls(urls, batch_size=3))

    assert len(batches) == 4  # 3 + 3 + 3 + 1
    assert len(batches[0]) == 3
    assert len(batches[1]) == 3
    assert len(batches[2]) == 3
    assert len(batches[3]) == 1


@pytest.mark.asyncio
async def test_sdk_orchestrator_configuration():
    """Test that SDK orchestrator is configured correctly."""
    from jina_mcp_docs import create_orchestrator_options

    options = create_orchestrator_options()

    # Should use claude_code system prompt for orchestrator
    assert options.system_prompt == "claude_code" or (
        isinstance(options.system_prompt, dict)
        and options.system_prompt.get("preset") == "claude_code"
    )

    # Should have Task tool for delegating to agents
    assert "Task" in options.allowed_tools


@pytest.mark.asyncio
async def test_parallel_download_via_mcp(tmp_path):
    """Test parallel download orchestration via Jina MCP."""
    from claude_agent_sdk import AssistantMessage, TextBlock
    from jina_mcp_docs import download_batch_parallel

    # Mock SDK client responses
    with patch("jina_mcp_docs.ClaudeSDKClient") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance

        # Mock receive_response to return some content
        async def mock_receive():
            yield AssistantMessage(
                model="claude-sonnet-4-5-20250929",
                content=[TextBlock(text="Mock content from parallel_read_url")],
            )

        mock_instance.receive_response = mock_receive

        urls = [
            "https://docs.claude.com/page1.md",
            "https://docs.claude.com/page2.md",
            "https://docs.claude.com/page3.md",
        ]

        results = await download_batch_parallel(urls, tmp_path)

        # Should have attempted parallel download
        assert mock_instance.query.called
        assert len(results) == 3


@pytest.mark.asyncio
async def test_each_url_gets_unique_content(tmp_path):
    """Test that each URL gets its own unique content, not duplicates.

    This test verifies the critical bug fix: the script must parse MCP tool
    responses correctly to write individual page content to each file, not
    the same combined content to all files.
    """
    import json

    from claude_agent_sdk import AssistantMessage, TextBlock, ToolResultBlock, UserMessage
    from jina_mcp_docs import download_batch_parallel

    # Mock SDK client responses with realistic MCP tool result
    with patch("jina_mcp_docs.ClaudeSDKClient") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance

        # Mock receive_response to return MCP tool result with individual content
        async def mock_receive():
            # First yield AssistantMessage (Claude's thinking)
            yield AssistantMessage(
                model="claude-sonnet-4-5-20250929",
                content=[TextBlock(text="I'll fetch those URLs in parallel")],
            )

            # Then yield UserMessage with ToolResultBlock containing actual MCP response
            # This is what parallel_read_url returns: JSON array of {url, content} objects
            tool_result = json.dumps([
                {
                    "url": "https://docs.claude.com/page1.md",
                    "content": "# Page 1 Content\n\nThis is unique content for page 1."
                },
                {
                    "url": "https://docs.claude.com/page2.md",
                    "content": "# Page 2 Content\n\nThis is unique content for page 2."
                },
                {
                    "url": "https://docs.claude.com/page3.md",
                    "content": "# Page 3 Content\n\nThis is unique content for page 3."
                }
            ])

            yield UserMessage(
                content=[ToolResultBlock(
                    tool_use_id="test-123",
                    content=tool_result,
                    is_error=False
                )]
            )

        mock_instance.receive_response = mock_receive

        urls = [
            "https://docs.claude.com/page1.md",
            "https://docs.claude.com/page2.md",
            "https://docs.claude.com/page3.md",
        ]

        results = await download_batch_parallel(urls, tmp_path)

        # Verify each file has unique content (not duplicates)
        page1_content = (tmp_path / "page1.md").read_text()
        page2_content = (tmp_path / "page2.md").read_text()
        page3_content = (tmp_path / "page3.md").read_text()

        # Each file should have its own unique content
        assert "page 1" in page1_content.lower()
        assert "page 2" in page2_content.lower()
        assert "page 3" in page3_content.lower()

        # Files should NOT all have the same content (the bug we're fixing)
        assert page1_content != page2_content
        assert page2_content != page3_content
        assert page1_content != page3_content
