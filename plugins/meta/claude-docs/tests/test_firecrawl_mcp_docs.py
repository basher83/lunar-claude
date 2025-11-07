#!/usr/bin/env python3
"""Tests for firecrawl_mcp_docs.py script."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

@pytest.mark.asyncio
async def test_firecrawl_orchestrator_configuration():
    """Test that Firecrawl orchestrator is configured correctly."""
    from firecrawl_mcp_docs import create_orchestrator_options

    options = create_orchestrator_options()

    # Should use claude_code system prompt
    assert options.system_prompt == "claude_code" or \
           (isinstance(options.system_prompt, dict) and
            options.system_prompt.get("preset") == "claude_code")

    # Should have Firecrawl MCP tools
    assert "mcp__firecrawl__firecrawl_scrape" in options.allowed_tools
