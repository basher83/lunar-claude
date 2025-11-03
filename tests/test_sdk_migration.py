"""
Tests for Claude Agent SDK migration.

Tests the SDK-based implementation of intelligent markdown linting,
including agent definition loading, SDK option configuration, and
subagent spawning with mocked SDK responses.
"""

# Import functions from the script
import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Import module with dashes in filename
script_path = Path(__file__).parent.parent / "scripts" / "intelligent-markdown-lint.py"
spec = importlib.util.spec_from_file_location("intelligent_markdown_lint", script_path)
intelligent_markdown_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intelligent_markdown_lint)

get_sdk_options = intelligent_markdown_lint.get_sdk_options
load_agent_definition = intelligent_markdown_lint.load_agent_definition
spawn_fixer = intelligent_markdown_lint.spawn_fixer
spawn_investigator = intelligent_markdown_lint.spawn_investigator


class TestLoadAgentDefinition:
    """Test agent definition loading from markdown files."""

    def test_load_valid_agent_definition(self, tmp_path):
        """Test loading a valid agent definition with frontmatter."""
        agent_file = tmp_path / "test-agent.md"
        agent_content = """---
name: test-agent
description: Test agent for unit tests
allowedTools:
  - Read
  - Bash
---

# Test Agent

This is a test agent system prompt.
It has multiple lines.
"""
        agent_file.write_text(agent_content)

        agent_def = load_agent_definition(str(agent_file))

        assert agent_def.description == "Test agent for unit tests"
        assert agent_def.tools == ["Read", "Bash"]
        assert "This is a test agent system prompt" in agent_def.prompt
        assert agent_def.model == "inherit"

    def test_load_agent_without_tools(self, tmp_path):
        """Test loading agent definition without allowedTools field."""
        agent_file = tmp_path / "no-tools.md"
        agent_content = """---
name: no-tools
description: Agent without tools
---

System prompt here.
"""
        agent_file.write_text(agent_content)

        agent_def = load_agent_definition(str(agent_file))

        assert agent_def.description == "Agent without tools"
        assert agent_def.tools == []  # Should default to empty list

    def test_load_missing_file(self):
        """Test loading non-existent agent definition file."""
        with pytest.raises(FileNotFoundError, match="Agent definition not found"):
            load_agent_definition("/nonexistent/path/agent.md")

    def test_load_invalid_frontmatter(self, tmp_path):
        """Test loading file with malformed frontmatter."""
        agent_file = tmp_path / "bad-frontmatter.md"
        agent_content = """---
This is not valid YAML:
  - [ broken
---

Prompt here.
"""
        agent_file.write_text(agent_content)

        with pytest.raises(ValueError, match="Invalid YAML frontmatter"):
            load_agent_definition(str(agent_file))

    def test_load_missing_description(self, tmp_path):
        """Test loading agent without required description field."""
        agent_file = tmp_path / "no-description.md"
        agent_content = """---
name: no-desc
---

Prompt here.
"""
        agent_file.write_text(agent_content)

        with pytest.raises(ValueError, match="missing required 'description' field"):
            load_agent_definition(str(agent_file))

    def test_load_no_frontmatter(self, tmp_path):
        """Test loading file without frontmatter delimiters."""
        agent_file = tmp_path / "no-frontmatter.md"
        agent_content = "Just some content without frontmatter"
        agent_file.write_text(agent_content)

        with pytest.raises(ValueError, match="missing or malformed frontmatter"):
            load_agent_definition(str(agent_file))


class TestGetSDKOptions:
    """Test SDK options factory function."""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "load_agent_definition")
    def test_get_sdk_options_success(self, mock_load):
        """Test successful SDK options creation."""
        # Mock agent definitions
        mock_investigator = MagicMock()
        mock_investigator.description = "Investigator agent"
        mock_fixer = MagicMock()
        mock_fixer.description = "Fixer agent"

        mock_load.side_effect = [mock_investigator, mock_fixer]

        options = get_sdk_options()

        assert options.allowed_tools == ["Bash", "Task", "Read", "Write"]
        assert options.permission_mode == "acceptEdits"
        assert "investigator" in options.agents
        assert "fixer" in options.agents
        assert options.model == "claude-sonnet-4-5-20250929"

    @patch.dict(os.environ, {}, clear=True)
    def test_get_sdk_options_no_api_key(self):
        """Test SDK options creation without API key."""
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable not set"):
            get_sdk_options()

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "load_agent_definition")
    def test_get_sdk_options_missing_agent_file(self, mock_load):
        """Test SDK options creation when agent file is missing."""
        mock_load.side_effect = FileNotFoundError("Agent definition not found")

        with pytest.raises(FileNotFoundError):
            get_sdk_options()


class TestSpawnInvestigator:
    """Test investigator subagent spawning."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "get_sdk_options")
    @patch.object(intelligent_markdown_lint, "ClaudeSDKClient")
    @patch.object(intelligent_markdown_lint, "AssistantMessage")
    @patch.object(intelligent_markdown_lint, "TextBlock")
    async def test_spawn_investigator_success(
        self, mock_text_block_class, mock_assistant_msg_class, mock_client_class, mock_get_options
    ):
        """Test successful investigator spawning with valid JSON response."""
        # Mock SDK options
        mock_options = MagicMock()
        mock_get_options.return_value = mock_options

        # Mock SDK client and response
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client

        # Mock investigator JSON response
        investigation_report = {
            "investigations": [
                {
                    "file": "test.md",
                    "results": [
                        {
                            "error": {"code": "MD033", "line": 10},
                            "verdict": "fixable",
                            "reasoning": "Test",
                        }
                    ],
                }
            ]
        }

        # Create mock message with JSON in code block
        mock_text_block = MagicMock()
        mock_text_block.text = f"""```json
{json.dumps(investigation_report, indent=2)}
```"""

        mock_message = MagicMock(spec=intelligent_markdown_lint.AssistantMessage)
        mock_message.content = [mock_text_block]

        # Mock isinstance checks
        def isinstance_side_effect(obj, cls):
            if obj == mock_message and cls == intelligent_markdown_lint.AssistantMessage:
                return True
            if obj == mock_text_block and cls == intelligent_markdown_lint.TextBlock:
                return True
            return type(obj) == cls

        # Mock async iteration
        async def mock_receive_response():
            yield mock_message

        mock_client.receive_response = mock_receive_response
        mock_client.query = AsyncMock()

        # Execute with mocked isinstance
        with patch("builtins.isinstance", side_effect=isinstance_side_effect):
            assignment = {"assignment": [{"file": "test.md", "errors": []}]}
            result = await spawn_investigator(assignment)

        # Verify
        assert result == investigation_report
        mock_client.query.assert_called_once()

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "get_sdk_options")
    @patch.object(intelligent_markdown_lint, "ClaudeSDKClient")
    async def test_spawn_investigator_no_json(self, mock_client_class, mock_get_options):
        """Test investigator spawning when no valid JSON is returned."""
        mock_options = MagicMock()
        mock_get_options.return_value = mock_options

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client

        # Mock message with no JSON
        mock_text_block = MagicMock()
        mock_text_block.text = "This is just text without JSON"

        mock_message = MagicMock(spec=intelligent_markdown_lint.AssistantMessage)
        mock_message.content = [mock_text_block]

        def isinstance_side_effect(obj, cls):
            if obj == mock_message and cls == intelligent_markdown_lint.AssistantMessage:
                return True
            if obj == mock_text_block and cls == intelligent_markdown_lint.TextBlock:
                return True
            return type(obj) == cls

        async def mock_receive_response():
            yield mock_message

        mock_client.receive_response = mock_receive_response
        mock_client.query = AsyncMock()

        # Execute and expect error
        with patch("builtins.isinstance", side_effect=isinstance_side_effect):
            assignment = {"assignment": []}
            with pytest.raises(RuntimeError, match="did not return valid JSON"):
                await spawn_investigator(assignment)


class TestSpawnFixer:
    """Test fixer subagent spawning."""

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "get_sdk_options")
    @patch.object(intelligent_markdown_lint, "ClaudeSDKClient")
    async def test_spawn_fixer_success(self, mock_client_class, mock_get_options):
        """Test successful fixer spawning with valid JSON response."""
        mock_options = MagicMock()
        mock_get_options.return_value = mock_options

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client

        # Mock fixer JSON response
        fix_report = {
            "results": [{"file": "test.md", "fixed": 5, "errors_before": 10, "errors_after": 5}]
        }

        mock_text_block = MagicMock()
        mock_text_block.text = f"```json\n{json.dumps(fix_report)}\n```"

        mock_message = MagicMock(spec=intelligent_markdown_lint.AssistantMessage)
        mock_message.content = [mock_text_block]

        def isinstance_side_effect(obj, cls):
            if obj == mock_message and cls == intelligent_markdown_lint.AssistantMessage:
                return True
            if obj == mock_text_block and cls == intelligent_markdown_lint.TextBlock:
                return True
            return type(obj) == cls

        async def mock_receive_response():
            yield mock_message

        mock_client.receive_response = mock_receive_response
        mock_client.query = AsyncMock()

        # Execute
        with patch("builtins.isinstance", side_effect=isinstance_side_effect):
            assignment = {"assignment": [{"path": "test.md", "errors": []}]}
            result = await spawn_fixer(assignment)

        # Verify
        assert result == fix_report
        mock_client.query.assert_called_once()

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-key"})
    @patch.object(intelligent_markdown_lint, "get_sdk_options")
    @patch.object(intelligent_markdown_lint, "ClaudeSDKClient")
    async def test_spawn_fixer_no_json(self, mock_client_class, mock_get_options):
        """Test fixer spawning when no valid JSON is returned."""
        mock_options = MagicMock()
        mock_get_options.return_value = mock_options

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client

        mock_text_block = MagicMock()
        mock_text_block.text = "No JSON here"

        mock_message = MagicMock(spec=intelligent_markdown_lint.AssistantMessage)
        mock_message.content = [mock_text_block]

        def isinstance_side_effect(obj, cls):
            if obj == mock_message and cls == intelligent_markdown_lint.AssistantMessage:
                return True
            if obj == mock_text_block and cls == intelligent_markdown_lint.TextBlock:
                return True
            return type(obj) == cls

        async def mock_receive_response():
            yield mock_message

        mock_client.receive_response = mock_receive_response
        mock_client.query = AsyncMock()

        with patch("builtins.isinstance", side_effect=isinstance_side_effect):
            assignment = {"assignment": []}
            with pytest.raises(RuntimeError, match="did not return valid JSON"):
                await spawn_fixer(assignment)
