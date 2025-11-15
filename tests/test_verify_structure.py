"""Tests for verify-structure.py error handling."""

import importlib.util
import sys
from pathlib import Path

# Load the verify-structure.py module
spec = importlib.util.spec_from_file_location(
    "verify_structure",
    str(Path(__file__).parent.parent / "scripts" / "verify-structure.py"),
)
verify_structure = importlib.util.module_from_spec(spec)
sys.modules["verify_structure"] = verify_structure
spec.loader.exec_module(verify_structure)


class TestErrorHandling:
    """Test error handling specificity."""

    def test_file_read_handles_permission_error(self, tmp_path):
        """Should catch and report permission errors specifically."""
        from verify_structure import validate_markdown_frontmatter

        # Create file with no read permissions
        test_file = tmp_path / "test.md"
        test_file.write_text("---\nname: test\n---")
        test_file.chmod(0o000)  # No permissions

        try:
            errors = validate_markdown_frontmatter(test_file, ["name"], "test-plugin")

            # Should get a clear permission error message
            assert len(errors) > 0
            # Check for specific permission error handling (not generic "Error reading file")
            assert "permission denied" in errors[0].lower()
            # Should show file permissions in octal
            assert "current:" in errors[0].lower() or "check file permissions" in errors[0].lower()
        finally:
            test_file.chmod(0o644)  # Restore permissions for cleanup

    def test_file_read_handles_unicode_error(self, tmp_path):
        """Should catch and report encoding errors specifically."""
        from verify_structure import validate_markdown_frontmatter

        # Create file with invalid UTF-8
        test_file = tmp_path / "test.md"
        test_file.write_bytes(b"\xff\xfe\x00\x00")  # Invalid UTF-8

        errors = validate_markdown_frontmatter(test_file, ["name"], "test-plugin")

        assert len(errors) > 0
        # Check for specific UTF-8 error handling (not generic "Error reading file")
        assert "not valid utf-8" in errors[0].lower()
        # Should mention binary file or encoding issue
        assert "binary" in errors[0].lower() or "byte" in errors[0].lower()


class TestJSONErrorHandling:
    """Test JSON loading error specificity."""

    def test_hooks_json_invalid_syntax(self, tmp_path):
        """Should report JSON syntax errors clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir()

        # Create invalid JSON
        hooks_file = hooks_dir / "hooks.json"
        hooks_file.write_text('{"invalid json')

        from verify_structure import check_hooks_configuration

        errors = check_hooks_configuration(plugin_dir, {"hooks": "hooks/hooks.json"})

        assert len(errors) > 0
        # Should mention JSON syntax error with line/column info
        assert "json" in errors[0].lower() or "invalid" in errors[0].lower()
        assert "line" in errors[0].lower() and "column" in errors[0].lower()

    def test_hooks_file_not_found(self, tmp_path):
        """Should report missing file clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()

        from verify_structure import check_hooks_configuration

        errors = check_hooks_configuration(plugin_dir, {"hooks": "nonexistent.json"})

        assert len(errors) > 0
        assert "not found" in errors[0].lower() or "does not exist" in errors[0].lower()

    def test_hooks_json_permission_denied(self, tmp_path):
        """Should report permission errors clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir()

        # Create file with no read permissions
        hooks_file = hooks_dir / "hooks.json"
        hooks_file.write_text('{"hooks": []}')
        hooks_file.chmod(0o000)

        from verify_structure import check_hooks_configuration

        try:
            errors = check_hooks_configuration(plugin_dir, {"hooks": "hooks/hooks.json"})
            assert len(errors) > 0
            assert "permission" in errors[0].lower()
        finally:
            hooks_file.chmod(0o644)

    def test_hooks_json_unicode_error(self, tmp_path):
        """Should report encoding errors clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir()

        # Create file with invalid UTF-8
        hooks_file = hooks_dir / "hooks.json"
        hooks_file.write_bytes(b"\xff\xfe\x00\x00")

        from verify_structure import check_hooks_configuration

        errors = check_hooks_configuration(plugin_dir, {"hooks": "hooks/hooks.json"})

        assert len(errors) > 0
        # Should mention UTF-8/encoding issue and suggest it's not text
        assert "utf-8" in errors[0].lower() or "encoding" in errors[0].lower()
        assert (
            "binary" in errors[0].lower()
            or "text" in errors[0].lower()
            or "ensure" in errors[0].lower()
        )


class TestMCPAndManifestErrors:
    """Test MCP config and manifest error handling."""

    def test_mcp_json_file_not_found(self, tmp_path):
        """Should handle MCP file not found errors specifically."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()

        from verify_structure import check_mcp_servers

        # Reference a non-existent MCP file
        errors = check_mcp_servers(plugin_dir, {"mcpServers": "config/mcp.json"})

        assert len(errors) > 0
        assert "not found" in errors[0].lower()

    def test_mcp_json_invalid_syntax(self, tmp_path):
        """Should report MCP JSON syntax errors clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        mcp_file = plugin_dir / ".mcp.json"
        mcp_file.write_text('{"invalid json')

        from verify_structure import check_mcp_servers

        errors = check_mcp_servers(plugin_dir, {})

        assert len(errors) > 0
        assert "json" in errors[0].lower() or "invalid" in errors[0].lower()
        assert "line" in errors[0].lower() and "column" in errors[0].lower()

    def test_mcp_custom_path_permission_denied(self, tmp_path):
        """Should report permission errors clearly for custom MCP files."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        config_dir = plugin_dir / "config"
        config_dir.mkdir()
        mcp_file = config_dir / "mcp.json"
        mcp_file.write_text('{"mcpServers": {}}')
        mcp_file.chmod(0o000)

        from verify_structure import check_mcp_servers

        try:
            errors = check_mcp_servers(plugin_dir, {"mcpServers": "config/mcp.json"})
            assert len(errors) > 0
            assert "permission" in errors[0].lower()
        finally:
            mcp_file.chmod(0o644)

    def test_mcp_custom_path_unicode_error(self, tmp_path):
        """Should report encoding errors clearly for custom MCP files."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        config_dir = plugin_dir / "config"
        config_dir.mkdir()
        mcp_file = config_dir / "mcp.json"
        mcp_file.write_bytes(b"\xff\xfe\x00\x00")

        from verify_structure import check_mcp_servers

        errors = check_mcp_servers(plugin_dir, {"mcpServers": "config/mcp.json"})

        assert len(errors) > 0
        assert "utf-8" in errors[0].lower() or "encoding" in errors[0].lower()

    def test_plugin_manifest_permission_denied_strict_mode(self, tmp_path):
        """Should catch permission errors in strict mode plugin.json loading."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_text('{"name": "test"}')
        plugin_json.chmod(0o000)

        from verify_structure import check_plugin_manifest

        try:
            result = check_plugin_manifest(plugin_dir, require_manifest=True)
            assert len(result["manifest"]) > 0
            assert "permission" in result["manifest"][0].lower()
        finally:
            plugin_json.chmod(0o644)

    def test_plugin_manifest_unicode_error_strict_mode(self, tmp_path):
        """Should catch encoding errors in strict mode plugin.json loading."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_bytes(b"\xff\xfe\x00\x00")

        from verify_structure import check_plugin_manifest

        result = check_plugin_manifest(plugin_dir, require_manifest=True)
        assert len(result["manifest"]) > 0
        assert (
            "utf-8" in result["manifest"][0].lower() or "encoding" in result["manifest"][0].lower()
        )

    def test_plugin_manifest_permission_denied_non_strict_mode(self, tmp_path):
        """Should catch permission errors in non-strict mode plugin.json loading."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_text('{"name": "test"}')
        plugin_json.chmod(0o000)

        from verify_structure import check_plugin_manifest

        try:
            result = check_plugin_manifest(plugin_dir, require_manifest=False)
            assert len(result["manifest"]) > 0
            assert "permission" in result["manifest"][0].lower()
        finally:
            plugin_json.chmod(0o644)

    def test_plugin_manifest_unicode_error_non_strict_mode(self, tmp_path):
        """Should catch encoding errors in non-strict mode plugin.json loading."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()
        plugin_json = claude_plugin_dir / "plugin.json"
        plugin_json.write_bytes(b"\xff\xfe\x00\x00")

        from verify_structure import check_plugin_manifest

        result = check_plugin_manifest(plugin_dir, require_manifest=False)
        assert len(result["manifest"]) > 0
        assert (
            "utf-8" in result["manifest"][0].lower() or "encoding" in result["manifest"][0].lower()
        )

    def test_marketplace_json_unicode_error(self, tmp_path, monkeypatch):
        """Should catch encoding errors in marketplace.json loading."""
        from unittest.mock import MagicMock

        from verify_structure import check_marketplace_structure

        # Create a mock that simulates reading invalid UTF-8
        mock_file = MagicMock()
        mock_file.__enter__ = MagicMock(
            side_effect=UnicodeDecodeError("utf-8", b"\xff\xfe\x00\x00", 0, 1, "invalid start byte")
        )
        mock_file.__exit__ = MagicMock(return_value=False)

        # Mock the open function to raise UnicodeDecodeError
        def mock_open_func(file, *args, **kwargs):
            if "marketplace.json" in str(file):
                return mock_file
            # Fall back to real open for other files
            return open(file, *args, **kwargs)

        # Mock Path.exists to return True for marketplace.json
        original_path = __import__("pathlib").Path

        class MockPath(original_path):
            def exists(self):
                if "marketplace.json" in str(self):
                    return True
                return super().exists()

        monkeypatch.setattr("pathlib.Path", MockPath)
        monkeypatch.setattr("builtins.open", mock_open_func)

        result = check_marketplace_structure()

        assert len(result["marketplace_errors"]) > 0
        # Should mention UTF-8/encoding issue
        assert "utf-8" in result["marketplace_errors"][0].lower()
        # Should mention binary file or ensure text
        assert (
            "binary" in result["marketplace_errors"][0].lower()
            or "ensure" in result["marketplace_errors"][0].lower()
        )


class TestSchemaValidation:
    """Test JSON schema validation error handling."""

    def test_invalid_schema_definition(self):
        """Should catch schema errors gracefully."""
        from verify_structure import validate_json_schema

        # Create invalid schema
        invalid_schema = {
            "type": "object",
            "properties": {"name": {"type": "invalid_type"}},  # Invalid type
        }

        data = {"name": "test"}

        errors = validate_json_schema(data, invalid_schema, "test-context")

        # Should get internal error message, not crash
        assert len(errors) > 0
        assert "internal error" in errors[0].lower() or "schema" in errors[0].lower()


class TestMarketplaceValidation:
    """Test marketplace.json schema validation."""

    def test_valid_marketplace_passes(self, tmp_path):
        """Valid marketplace.json should pass validation."""

        from verify_structure import validate_marketplace_json

        marketplace = {
            "name": "test-marketplace",
            "owner": {"name": "Test Owner", "email": "test@example.com"},
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "plugins/test-plugin",
                    "version": "1.0.0",
                }
            ],
        }

        errors = validate_marketplace_json(marketplace)
        assert len(errors) == 0

    def test_invalid_marketplace_name_pattern(self, tmp_path):
        """Invalid name pattern should fail."""

        from verify_structure import validate_marketplace_json

        marketplace = {
            "name": "Invalid_Name",  # Underscores not allowed
            "owner": {"name": "Test"},
            "plugins": [{"name": "test", "source": "./test", "version": "1.0.0"}],
        }

        errors = validate_marketplace_json(marketplace)
        assert len(errors) > 0
        assert any("pattern" in str(e).lower() or "name" in str(e).lower() for e in errors)


class TestStrictMode:
    """Test strict mode functionality."""

    def test_strict_true_requires_plugin_json(self, tmp_path):
        """Strict mode should require plugin.json."""
        from verify_structure import check_plugin_manifest

        marketplace_entry = {
            "name": "test-plugin",
            "source": "plugins/test-plugin",
        }

        # Create plugin dir WITHOUT plugin.json
        plugin_dir = tmp_path / "plugins" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "README.md").write_text("# Test")

        result = check_plugin_manifest(plugin_dir, marketplace_entry, require_manifest=True)

        assert len(result["manifest"]) > 0
        assert any("plugin.json" in str(e).lower() for e in result["manifest"])

    def test_strict_false_allows_missing_plugin_json(self, tmp_path):
        """Non-strict mode should allow missing plugin.json."""
        from verify_structure import check_plugin_manifest

        marketplace_entry = {
            "name": "test-plugin",
            "source": "plugins/test-plugin",
            "version": "1.0.0",
            "description": "Test plugin",
        }

        plugin_dir = tmp_path / "plugins" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "README.md").write_text("# Test")

        result = check_plugin_manifest(plugin_dir, marketplace_entry, require_manifest=False)

        # Should have no manifest errors
        assert len(result["manifest"]) == 0 or not any(
            "plugin.json" in str(e).lower() for e in result["manifest"]
        )


class TestExitCodes:
    """Test exit code calculation."""

    def test_exit_0_no_errors_no_warnings(self):
        """No errors or warnings should exit 0."""
        from verify_structure import calculate_exit_code

        result = {"marketplace_errors": [], "plugin_results": {}}
        exit_code = calculate_exit_code(result, strict=False)
        assert exit_code == 0

    def test_exit_0_warnings_normal_mode(self):
        """Warnings in normal mode should exit 0."""
        from verify_structure import calculate_exit_code

        result = {
            "marketplace_errors": [],
            "plugin_results": {"test-plugin": {"warnings": ["warning1"]}},
        }
        exit_code = calculate_exit_code(result, strict=False)
        assert exit_code == 0

    def test_exit_1_warnings_strict_mode(self):
        """Warnings in strict mode should exit 1."""
        from verify_structure import calculate_exit_code

        result = {
            "marketplace_errors": [],
            "plugin_results": {"test-plugin": {"warnings": ["warning1"]}},
        }
        exit_code = calculate_exit_code(result, strict=True)
        assert exit_code == 1

    def test_exit_1_with_errors(self):
        """Errors should always exit 1."""
        from verify_structure import calculate_exit_code

        result = {
            "marketplace_errors": [],
            "plugin_results": {"test-plugin": {"manifest": ["error1"]}},
        }

        assert calculate_exit_code(result, strict=False) == 1
        assert calculate_exit_code(result, strict=True) == 1


class TestConflictDetection:
    """Test conflict detection between marketplace and plugin.json."""

    def test_version_conflict_generates_warning(self):
        """Differing versions should generate warning."""
        from verify_structure import check_manifest_conflicts

        marketplace_entry = {"name": "test", "version": "1.0.0"}
        plugin_json = {"name": "test", "version": "2.0.0"}

        warnings = check_manifest_conflicts("test-plugin", marketplace_entry, plugin_json)

        assert len(warnings) > 0
        assert any("version" in w.lower() for w in warnings)
        assert any("1.0.0" in w for w in warnings)
        assert any("2.0.0" in w for w in warnings)

    def test_no_warning_when_values_match(self):
        """Matching values should not generate warnings."""
        from verify_structure import check_manifest_conflicts

        entry = {"name": "test", "version": "1.0.0"}

        warnings = check_manifest_conflicts("test-plugin", entry, entry)

        assert len(warnings) == 0


class TestConflictDetectionEdgeCases:
    """Test conflict detection edge cases."""

    def test_keywords_order_insensitive(self):
        """Keywords with different order should not conflict."""
        from verify_structure import check_manifest_conflicts

        marketplace = {"keywords": ["terraform", "ansible", "infrastructure"]}
        plugin_json = {"keywords": ["ansible", "infrastructure", "terraform"]}

        warnings = check_manifest_conflicts("test", marketplace, plugin_json)

        # Should have NO keyword warnings
        assert not any("keyword" in w.lower() for w in warnings)


class TestSecurityValidation:
    """Test security validations."""

    def test_rejects_path_traversal_in_hooks(self, tmp_path):
        """Should reject path traversal attempts in hooks path."""
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()

        from verify_structure import check_hooks_configuration

        # Attempt path traversal
        plugin_data = {"hooks": "../../etc/passwd"}

        errors = check_hooks_configuration(plugin_dir, plugin_data)

        assert len(errors) > 0
        assert any("escape" in e.lower() or "outside" in e.lower() for e in errors)

    def test_rejects_path_traversal_in_mcp(self, tmp_path):
        """Should reject path traversal attempts in MCP path."""
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()

        from verify_structure import check_mcp_servers

        # Attempt path traversal
        plugin_data = {"mcpServers": "../../../etc/passwd"}

        errors = check_mcp_servers(plugin_dir, plugin_data)

        assert len(errors) > 0
        assert any("escape" in e.lower() or "outside" in e.lower() for e in errors)

    def test_rejects_path_traversal_in_custom_commands(self, tmp_path):
        """Should reject path traversal attempts in custom command paths."""
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()

        from verify_structure import check_custom_component_paths

        # Attempt path traversal (paths must start with ./ to get past initial check)
        plugin_data = {"commands": "./../../etc/passwd"}

        errors = check_custom_component_paths(plugin_dir, plugin_data)

        assert len(errors) > 0
        assert any("escape" in e.lower() or "outside" in e.lower() for e in errors)

    def test_rejects_path_traversal_in_custom_agents(self, tmp_path):
        """Should reject path traversal attempts in custom agent paths."""
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()

        from verify_structure import check_custom_component_paths

        # Attempt path traversal (paths must start with ./ to get past initial check)
        plugin_data = {"agents": "./../../../etc/passwd"}

        errors = check_custom_component_paths(plugin_dir, plugin_data)

        assert len(errors) > 0
        assert any("escape" in e.lower() or "outside" in e.lower() for e in errors)
