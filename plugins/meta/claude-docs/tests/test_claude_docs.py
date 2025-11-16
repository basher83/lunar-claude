"""Tests for claude_docs.py - the active documentation sync script."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def test_find_or_create_ai_docs_dir():
    """Test that default output directory points to official-docs skill."""
    from claude_docs import find_or_create_ai_docs_dir

    docs_dir = find_or_create_ai_docs_dir()

    assert docs_dir.name == "reference"
    assert docs_dir.parent.name == "official-docs"
    assert docs_dir.parent.parent.name == "skills"


def test_default_pages_defined():
    """Test that curated page list is defined and non-empty."""
    from claude_docs import DEFAULT_PAGES

    assert len(DEFAULT_PAGES) > 0
    assert all(isinstance(page, tuple) for page in DEFAULT_PAGES)
    assert all(len(page) == 2 for page in DEFAULT_PAGES)

    # Verify structure: (base_path, page_name)
    base_paths = {page[0] for page in DEFAULT_PAGES}
    assert "claude-code" in base_paths


def test_file_metadata_dataclass():
    """Test FileMetadata dataclass structure."""
    from claude_docs import FileMetadata

    meta = FileMetadata(
        etag="abc123", last_modified="2025-01-01T00:00:00Z", size=1000, downloaded_at=1234567890.0
    )

    assert meta.etag == "abc123"
    assert meta.last_modified == "2025-01-01T00:00:00Z"
    assert meta.size == 1000
    assert meta.downloaded_at == 1234567890.0


def test_file_metadata_serialization():
    """Test that FileMetadata can be serialized to JSON."""
    from claude_docs import FileMetadata

    meta = FileMetadata(
        etag="test-etag", last_modified="2025-11-16", size=5000, downloaded_at=1700000000.0
    )

    # Should be serializable to JSON
    json_str = json.dumps(meta.__dict__)
    assert "test-etag" in json_str
    assert "2025-11-16" in json_str

    # Should be deserializable
    parsed = json.loads(json_str)
    assert parsed["etag"] == "test-etag"
    assert parsed["size"] == 5000


def test_download_result_dataclass():
    """Test DownloadResult dataclass structure."""
    from claude_docs import DownloadResult

    result = DownloadResult(
        status="success",
        downloaded=10,
        skipped=5,
        failed=0,
        duration_seconds=2.5,
        timestamp="2025-11-16T00:00:00Z",
    )

    assert result.status == "success"
    assert result.downloaded == 10
    assert result.skipped == 5
    assert result.failed == 0
    assert result.duration_seconds == 2.5


def test_output_format_enum():
    """Test OutputFormat enum values."""
    from claude_docs import OutputFormat

    assert OutputFormat.RICH == "rich"
    assert OutputFormat.JSON == "json"


def test_base_urls_defined():
    """Test that base URLs are properly defined."""
    from claude_docs import AGENTS_TOOLS_BASE, BASE_URL, CLAUDE_CODE_BASE

    assert BASE_URL == "https://docs.claude.com/en/docs"
    assert f"{BASE_URL}/claude-code" == CLAUDE_CODE_BASE
    assert f"{BASE_URL}/agents-and-tools" == AGENTS_TOOLS_BASE


def test_curated_page_lists():
    """Test that curated page lists contain expected documentation."""
    from claude_docs import AGENT_SKILLS_PAGES, CLAUDE_CODE_PAGES

    # Key Claude Code pages
    assert "plugins" in CLAUDE_CODE_PAGES
    assert "skills" in CLAUDE_CODE_PAGES
    assert "hooks" in CLAUDE_CODE_PAGES

    # Agent Skills pages
    assert any("agent-skills" in page for page in AGENT_SKILLS_PAGES)


@patch("claude_docs.httpx.Client")
def test_download_page_success(mock_client):
    """Test successful page download."""
    from claude_docs import download_page

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "# Test Documentation\n\nContent here."
    mock_response.headers = {
        "etag": "test-etag-123",
        "last-modified": "Mon, 16 Nov 2025 00:00:00 GMT",
    }

    mock_client_instance = MagicMock()
    mock_client_instance.get.return_value = mock_response
    mock_client.return_value.__enter__.return_value = mock_client_instance

    success, duration, size, metadata = download_page(
        "claude-code", "test-page", Path("/tmp/test.md"), max_retries=1
    )

    assert success is True
    assert size > 0
    assert metadata.etag == "test-etag-123"


@patch("claude_docs.httpx.Client")
def test_download_page_with_cache_hit(mock_client):
    """Test page download with cache hit (304 Not Modified)."""
    from claude_docs import FileMetadata, download_page

    # Mock 304 Not Modified response
    mock_response = MagicMock()
    mock_response.status_code = 304

    mock_client_instance = MagicMock()
    mock_client_instance.get.return_value = mock_response
    mock_client.return_value.__enter__.return_value = mock_client_instance

    existing_meta = FileMetadata(etag="cached-etag")

    success, duration, size, metadata = download_page(
        "claude-code",
        "test-page",
        Path("/tmp/test.md"),
        max_retries=1,
        existing_metadata=existing_meta,
    )

    assert success is True
    assert size == 0  # No new content downloaded
