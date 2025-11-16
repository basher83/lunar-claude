#!/usr/bin/env python3
"""Tests for firecrawl_sdk_research.py script."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

# Mock the firecrawl module before importing
sys.modules["firecrawl"] = MagicMock()
sys.modules["typer"] = MagicMock()
sys.modules["rich"] = MagicMock()
sys.modules["rich.console"] = MagicMock()

# Now import the module
from firecrawl_sdk_research import (
    combine_results,
    filter_quality,
    get_api_key,
    retry_with_backoff,
)


class TestGetApiKey:
    """Test API key retrieval."""

    def test_api_key_found(self):
        """Should return API key when environment variable is set."""
        with patch.dict("os.environ", {"FIRECRAWL_API_KEY": "test-key"}):
            assert get_api_key() == "test-key"

    def test_api_key_missing(self):
        """Should exit when API key is not set."""
        with (
            patch.dict("os.environ", {}, clear=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            get_api_key()
        assert exc_info.value.code == 1


class TestRetryWithBackoff:
    """Test retry logic with exponential backoff."""

    @pytest.mark.asyncio
    async def test_success_on_first_try(self):
        """Should return result on first successful attempt."""
        async_func = AsyncMock(return_value="success")
        result = await retry_with_backoff(async_func)
        assert result == "success"
        assert async_func.call_count == 1

    @pytest.mark.asyncio
    async def test_success_on_retry(self):
        """Should retry and eventually succeed."""
        async_func = AsyncMock(side_effect=[Exception("fail"), "success"])
        result = await retry_with_backoff(async_func, max_retries=3)
        assert result == "success"
        assert async_func.call_count == 2

    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self):
        """Should raise exception after max retries."""
        async_func = AsyncMock(side_effect=Exception("persistent failure"))
        with pytest.raises(Exception, match="persistent failure"):
            await retry_with_backoff(async_func, max_retries=3)
        assert async_func.call_count == 3


class TestFilterQuality:
    """Test quality filtering logic."""

    def test_filters_short_content(self):
        """Should filter out results with very short content."""
        results = [
            {"url": "https://example.com", "title": "Test", "markdown": "Short"},
            {
                "url": "https://example.com",
                "title": "Test",
                "markdown": "A" * 1000,
            },
        ]
        filtered = filter_quality(results, min_content_length=500)
        assert len(filtered) == 1
        assert filtered[0]["markdown"] == "A" * 1000

    def test_filters_error_pages(self):
        """Should filter out error pages."""
        results = [
            {
                "url": "https://example.com",
                "title": "404 Not Found",
                "markdown": "A" * 1000,
            },
            {"url": "https://example.com", "title": "Valid", "markdown": "A" * 1000},
        ]
        filtered = filter_quality(results, min_content_length=500)
        assert len(filtered) == 1
        assert filtered[0]["title"] == "Valid"

    def test_quality_scoring_for_github(self):
        """Should give higher scores to GitHub repos."""
        results = [
            {
                "url": "https://github.com/user/repo",
                "title": "GitHub Repo",
                "markdown": "A" * 1000,
            },
            {
                "url": "https://example.com",
                "title": "Regular",
                "markdown": "A" * 1000,
            },
        ]
        filtered = filter_quality(results, min_content_length=500)
        assert len(filtered) == 2
        # GitHub should have higher score and be sorted first
        assert "github.com" in filtered[0]["url"]
        assert filtered[0]["quality_score"] > filtered[1]["quality_score"]

    def test_quality_scoring_for_code_blocks(self):
        """Should boost score for content with code blocks."""
        results = [
            {
                "url": "https://example.com/code",
                "title": "With Code",
                "markdown": "```python\nprint('hello')\n```" + "A" * 1000,
            },
            {
                "url": "https://example.com/text",
                "title": "No Code",
                "markdown": "A" * 1000,
            },
        ]
        filtered = filter_quality(results, min_content_length=500)
        assert len(filtered) == 2
        assert filtered[0]["title"] == "With Code"
        assert filtered[0]["quality_score"] > filtered[1]["quality_score"]

    def test_quality_scoring_for_premium_domains(self):
        """Should boost score for premium quality domains."""
        results = [
            {
                "url": "https://docs.ansible.com/guide",
                "title": "Ansible Docs",
                "markdown": "A" * 1000,
            },
            {
                "url": "https://example.com",
                "title": "Random",
                "markdown": "A" * 1000,
            },
        ]
        filtered = filter_quality(results, min_content_length=500)
        assert len(filtered) == 2
        assert "ansible.com" in filtered[0]["url"]
        assert filtered[0]["quality_score"] >= 10  # Premium domain boost

    def test_sorting_by_quality_score(self):
        """Should sort results by quality score in descending order."""
        results = [
            {"url": "https://example.com/low", "title": "Low", "markdown": "A" * 600},
            {
                "url": "https://github.com/high/repo",
                "title": "High",
                "markdown": "```code```" + "A" * 3000,
            },
            {
                "url": "https://example.com/mid",
                "title": "Mid",
                "markdown": "A" * 1500,
            },
        ]
        filtered = filter_quality(results, min_content_length=500)
        # Should be sorted highest to lowest
        assert filtered[0]["title"] == "High"
        assert filtered[1]["title"] == "Mid"
        assert filtered[2]["title"] == "Low"


class TestCombineResults:
    """Test research document generation."""

    def test_combines_metadata(self):
        """Should include metadata section with query and counts."""
        search_results = [{"url": "https://example.com", "title": "Test"}]
        scraped = [
            {
                "url": "https://example.com",
                "title": "Test",
                "markdown": "Content",
                "quality_score": 5,
                "domain": "example.com",
            }
        ]
        doc = combine_results("test query", search_results, scraped)

        assert "# Research: test query" in doc
        assert "- **Query:** test query" in doc
        assert "- **Search Results:** 1" in doc
        assert "- **Scraped Pages:** 1" in doc

    def test_combines_with_categories(self):
        """Should include categories in metadata when provided."""
        doc = combine_results(
            "test query", [], [], categories=["github", "research"]
        )
        assert "- **Categories:** github, research" in doc

    def test_includes_sources_section(self):
        """Should include table of contents with sources."""
        scraped = [
            {
                "url": "https://example.com",
                "title": "Test Article",
                "markdown": "Content",
                "quality_score": 5,
                "domain": "example.com",
            }
        ]
        doc = combine_results("test", [], scraped)

        assert "## Sources" in doc
        assert "[Test Article](https://example.com)" in doc
        assert "Domain: `example.com`" in doc
        assert "Quality Score: 5" in doc

    def test_quality_badges(self):
        """Should add quality badges for high-quality sources."""
        scraped = [
            {
                "url": "https://example.com/high",
                "title": "High Quality",
                "markdown": "A" * 1000,
                "quality_score": 12,
                "domain": "example.com",
            },
            {
                "url": "https://example.com/mid",
                "title": "Mid Quality",
                "markdown": "A" * 1000,
                "quality_score": 6,
                "domain": "example.com",
            },
            {
                "url": "https://example.com/low",
                "title": "Low Quality",
                "markdown": "A" * 1000,
                "quality_score": 2,
                "domain": "example.com",
            },
        ]
        doc = combine_results("test", [], scraped)

        assert "High Quality](https://example.com/high) ⭐" in doc
        assert "Mid Quality](https://example.com/mid) ✓" in doc
        # Low quality should have no badge
        lines = doc.split("\n")
        low_quality_line = [line for line in lines if "Low Quality" in line][0]
        assert " ⭐" not in low_quality_line and " ✓" not in low_quality_line

    def test_includes_content_section(self):
        """Should include full content for each scraped page."""
        scraped = [
            {
                "url": "https://example.com",
                "title": "Test",
                "description": "Test description",
                "markdown": "# Test Content\n\nSome text here.",
                "quality_score": 5,
                "domain": "example.com",
            }
        ]
        doc = combine_results("test", [], scraped)

        assert "## Content" in doc
        assert "### 1. Test" in doc
        assert "**Source:** [https://example.com](https://example.com)" in doc
        assert "*Test description*" in doc
        assert "# Test Content" in doc
        assert "Some text here." in doc
