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
