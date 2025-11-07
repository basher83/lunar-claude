"""Tests for jina_reader_docs.py script."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts directory to path for imports
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def test_jina_reader_url_construction():
    """Test that Jina Reader URLs are constructed correctly."""
    from jina_reader_docs import build_jina_reader_url

    url = "https://docs.claude.com/en/docs/claude-code/skills.md"
    reader_url = build_jina_reader_url(url)

    assert reader_url == "https://r.jina.ai/https://docs.claude.com/en/docs/claude-code/skills.md"


def test_api_key_auto_detection():
    """Test that API key is auto-detected from environment."""
    from jina_reader_docs import get_api_key

    with patch.dict("os.environ", {"JINA_API_KEY": "test-key-123"}):
        api_key = get_api_key(cli_key=None)
        assert api_key == "test-key-123"


def test_api_key_cli_override():
    """Test that CLI API key overrides environment."""
    from jina_reader_docs import get_api_key

    with patch.dict("os.environ", {"JINA_API_KEY": "env-key"}):
        api_key = get_api_key(cli_key="cli-key")
        assert api_key == "cli-key"


@patch("requests.get")
def test_download_with_jina_reader(mock_get):
    """Test downloading a page via Jina Reader API."""
    from jina_reader_docs import download_page_jina

    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "# Test Content\n\nThis is test markdown."
    mock_response.headers = {"etag": "test-etag"}
    mock_get.return_value = mock_response

    url = "https://docs.claude.com/en/docs/claude-code/skills.md"
    success, content, metadata = download_page_jina(url, api_key="test-key")

    assert success is True
    assert "Test Content" in content
    assert metadata["etag"] == "test-etag"


@patch("requests.get")
def test_retry_logic_on_server_error(mock_get):
    """Test retry logic triggers on 5xx errors."""
    import requests
    from jina_reader_docs import download_page_jina

    # Mock server error followed by success
    error_response = Mock()
    error_response.status_code = 503

    # Create proper HTTPError
    http_error = requests.exceptions.HTTPError("Server error")
    http_error.response = error_response
    error_response.raise_for_status.side_effect = http_error

    success_response = Mock()
    success_response.status_code = 200
    success_response.text = "# Success"
    success_response.headers = {"etag": "success-etag"}

    mock_get.side_effect = [error_response, success_response]

    url = "https://docs.claude.com/en/docs/claude-code/skills.md"
    success, content, metadata = download_page_jina(url, api_key="test-key", retries=2)

    assert success is True
    assert "Success" in content
