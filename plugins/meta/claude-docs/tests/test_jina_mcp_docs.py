#!/usr/bin/env python3
"""Tests for jina_mcp_docs.py script."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys

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
    assert options.system_prompt == "claude_code" or \
           (isinstance(options.system_prompt, dict) and
            options.system_prompt.get("preset") == "claude_code")

    # Should have Task tool for delegating to agents
    assert "Task" in options.allowed_tools or \
           "mcp__jina-mcp-server__read_url" in options.allowed_tools or \
           "mcp__jina-mcp-server__parallel_read_url" in options.allowed_tools
