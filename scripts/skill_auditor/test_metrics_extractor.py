#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Unit tests for metrics extraction module.

For integration/determinism tests, see test_determinism.py
"""

import tempfile
from pathlib import Path

from metrics_extractor import extract_skill_metrics


def test_extract_description_from_skill_md():
    """Test extraction of description field from YAML frontmatter."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  This is a test skill with "quoted phrases" for testing.
  It has multiple lines.
---

# Test Skill

Content here.
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "description" in metrics
        assert "test skill" in metrics["description"].lower()
        assert "quoted phrases" in metrics["description"]
        print("✅ test_extract_description_from_skill_md passed")


def test_extract_quoted_phrases():
    """Test extraction of quoted phrases from description."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Use when "creating skills", "validating SKILL.md",
  or "auditing against specs".
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "quoted_phrases" in metrics
        assert len(metrics["quoted_phrases"]) == 3
        assert "creating skills" in metrics["quoted_phrases"]
        assert "validating SKILL.md" in metrics["quoted_phrases"]
        assert "auditing against specs" in metrics["quoted_phrases"]
        print("✅ test_extract_quoted_phrases passed")


def test_quoted_phrase_count():
    """Test quoted phrase count metric."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Test with "phrase one" and "phrase two"
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert metrics["quoted_count"] == 2
        print("✅ test_quoted_phrase_count passed")


def test_extract_domain_indicators():
    """Test extraction of domain-specific indicators."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Create SKILL.md files with YAML frontmatter for Claude Code.
  Validate skill structure and compliance.
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "domain_indicators" in metrics
        # Should find: skill.md, yaml, frontmatter, claude code, skill, compliance
        # All normalized to lowercase
        assert len(metrics["domain_indicators"]) >= 5
        assert "skill.md" in metrics["domain_indicators"]
        assert "domain_count" in metrics
        assert metrics["domain_count"] >= 5
        print("✅ test_extract_domain_indicators passed")


def test_domain_indicators_case_insensitive():
    """Test domain indicators extraction is case-insensitive."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Work with skill files and YAML and Frontmatter for validation
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "domain_indicators" in metrics
        # Verify case-insensitive matching (skill, YAML, Frontmatter, validation)
        assert len(metrics["domain_indicators"]) >= 3
        print("✅ test_domain_indicators_case_insensitive passed")


def test_domain_indicators_unique():
    """Test domain indicators are unique (no duplicates)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Create skill files for skill validation. The skill must have YAML.
---
""")

        metrics = extract_skill_metrics(tmp_path)

        # 'skill' appears 3 times but should only be counted once
        # Should find: skill, YAML, validation
        skill_count = sum(
            1 for indicator in metrics["domain_indicators"] if indicator.lower() == "skill"
        )
        assert skill_count == 1, "Domain indicators should be unique"
        print("✅ test_domain_indicators_unique passed")


def test_domain_indicators_mixed_case_deduplication():
    """Test domain indicators with mixed case are properly deduplicated."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Research the specification for compliance validation.
  The research shows that Validation requires Research.
---
""")

        metrics = extract_skill_metrics(tmp_path)

        # 'research', 'Research' should be deduplicated to one
        # 'validation', 'Validation' should be deduplicated to one
        research_count = sum(
            1 for indicator in metrics["domain_indicators"] if indicator.lower() == "research"
        )
        validation_count = sum(
            1 for indicator in metrics["domain_indicators"] if indicator.lower() == "validation"
        )

        assert research_count == 1, "Mixed-case 'research'/'Research' should be deduplicated"
        assert validation_count == 1, "Mixed-case 'validation'/'Validation' should be deduplicated"

        # Verify all indicators are lowercase
        for indicator in metrics["domain_indicators"]:
            assert indicator == indicator.lower(), (
                f"Domain indicator '{indicator}' should be lowercase"
            )

        print("✅ test_domain_indicators_mixed_case_deduplication passed")


def test_forbidden_files_detection():
    """Test detection of forbidden files."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: test\n---")

        # Create forbidden file
        (tmp_path / "README.md").write_text("Forbidden")

        metrics = extract_skill_metrics(tmp_path)

        assert "forbidden_files" in metrics
        assert len(metrics["forbidden_files"]) == 1
        assert "README.md" in metrics["forbidden_files"]
        print("✅ test_forbidden_files_detection passed")


def test_forbidden_files_multiple():
    """Test detection of multiple forbidden files."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: test\n---")

        # Create multiple forbidden files
        (tmp_path / "README.md").write_text("Forbidden")
        (tmp_path / "INSTALL.txt").write_text("Forbidden")
        (tmp_path / "CHANGELOG.md").write_text("Forbidden")
        (tmp_path / "QUICKSTART.md").write_text("Forbidden")

        metrics = extract_skill_metrics(tmp_path)

        assert "forbidden_files" in metrics
        assert len(metrics["forbidden_files"]) == 4
        assert "README.md" in metrics["forbidden_files"]
        assert "INSTALL.txt" in metrics["forbidden_files"]
        assert "CHANGELOG.md" in metrics["forbidden_files"]
        assert "QUICKSTART.md" in metrics["forbidden_files"]
        print("✅ test_forbidden_files_multiple passed")


def test_no_forbidden_files():
    """Test that no forbidden files returns empty list."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: test\n---")

        # Only allowed file
        (tmp_path / "helper_script.py").write_text("# Helper")

        metrics = extract_skill_metrics(tmp_path)

        assert "forbidden_files" in metrics
        assert len(metrics["forbidden_files"]) == 0
        print("✅ test_no_forbidden_files passed")


def test_line_count():
    """Test SKILL.md line count."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        content = "---\nname: test\n---\n" + "\n".join([f"Line {i}" for i in range(100)])
        skill_md.write_text(content)

        metrics = extract_skill_metrics(tmp_path)

        assert "line_count" in metrics
        assert metrics["line_count"] > 100
        print("✅ test_line_count passed")


def test_implementation_details_detection():
    """Test detection of implementation details in description."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Uses script.py and helper.sh with /slash:command
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "implementation_details" in metrics
        assert len(metrics["implementation_details"]) >= 2  # .py, .sh, /slash:command
        print("✅ test_implementation_details_detection passed")


def test_implementation_details_various_patterns():
    """Test detection of various implementation detail patterns."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Uses tools like script.py, helper.sh, config.json,
  and commands like /commit:push or /review:code
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "implementation_details" in metrics
        # Should find: script.py, helper.sh, config.json, /commit:push, /review:code
        assert len(metrics["implementation_details"]) >= 5
        print("✅ test_implementation_details_various_patterns passed")


def test_no_implementation_details():
    """Test that clean description has no implementation details."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Use when creating skills or validating content.
  Focus on quality and compliance.
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "implementation_details" in metrics
        assert len(metrics["implementation_details"]) == 0
        print("✅ test_no_implementation_details passed")


def test_yaml_frontmatter_valid():
    """Test detection of valid YAML frontmatter."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: Valid skill
---

Content here.
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "has_frontmatter" in metrics
        assert metrics["has_frontmatter"] is True
        assert "yaml_delimiters" in metrics
        assert metrics["yaml_delimiters"] == 2
        assert "has_name" in metrics
        assert metrics["has_name"] is True
        assert "has_description" in metrics
        assert metrics["has_description"] is True
        print("✅ test_yaml_frontmatter_valid passed")


def test_yaml_frontmatter_missing():
    """Test detection of missing YAML frontmatter."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""# Skill without frontmatter

This is bad.
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "has_frontmatter" in metrics
        assert metrics["has_frontmatter"] is False
        assert "yaml_delimiters" in metrics
        assert metrics["yaml_delimiters"] == 0
        print("✅ test_yaml_frontmatter_missing passed")


def test_yaml_frontmatter_incomplete():
    """Test detection of incomplete YAML frontmatter."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
---

Missing description field.
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "has_frontmatter" in metrics
        assert metrics["has_frontmatter"] is True
        assert "has_name" in metrics
        assert metrics["has_name"] is True
        assert "has_description" in metrics
        assert metrics["has_description"] is False
        print("✅ test_yaml_frontmatter_incomplete passed")


def test_extract_metrics_permission_error():
    """Test that PermissionError on SKILL.md read is handled gracefully."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: test\n---\n")

        # Make file unreadable
        skill_md.chmod(0o000)

        try:
            try:
                extract_skill_metrics(tmp_path)
                # If we get here, the test fails - no exception was raised
                raise AssertionError("Expected PermissionError to be raised but it was not")
            except PermissionError as e:
                # Verify error message is helpful
                error_msg = str(e)
                assert "Permission denied" in error_msg, (
                    f"Expected 'Permission denied' in error message, got: {error_msg}"
                )
                assert str(skill_md) in error_msg, (
                    f"Expected file path in error message, got: {error_msg}"
                )
        finally:
            # Restore permissions for cleanup
            skill_md.chmod(0o644)

        print("✅ test_extract_metrics_permission_error passed")


def test_extract_metrics_unicode_decode_error():
    """Test that UnicodeDecodeError on SKILL.md is handled gracefully."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"

        # Write invalid UTF-8 bytes
        skill_md.write_bytes(b"\xff\xfe Invalid UTF-8 \x80\x81")

        try:
            extract_skill_metrics(tmp_path)
            # If we get here, the test fails - no exception was raised
            raise AssertionError("Expected ValueError to be raised but it was not")
        except ValueError as e:
            error_msg = str(e)
            assert "encoding issues" in error_msg.lower(), (
                f"Expected 'encoding issues' in error message, got: {error_msg}"
            )
            assert "UTF-8" in error_msg, f"Expected 'UTF-8' in error message, got: {error_msg}"

        print("✅ test_extract_metrics_unicode_decode_error passed")


def test_yaml_frontmatter_empty_description():
    """Test detection of empty description field."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: ""
---
# Content
""")

        metrics = extract_skill_metrics(tmp_path)

        # Empty quoted string should result in empty description
        assert metrics["description"] == '""', (
            f"Expected empty quoted description, got: {metrics['description']}"
        )
        assert metrics["quoted_count"] == 0, (
            f"Expected 0 quoted phrases in empty description, got: {metrics['quoted_count']}"
        )
        # Empty description may still match "description" as domain indicator
        assert metrics["domain_count"] == 0, (
            f"Expected 0 domain indicators in empty description, got: {metrics['domain_count']}"
        )

        print("✅ test_yaml_frontmatter_empty_description passed")


def test_description_with_special_regex_characters():
    """Test extraction handles regex special characters in description."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Use for $pecial (characters) like [brackets] and *.wildcards
  with "nested 'quotes' inside" patterns.
---
""")

        metrics = extract_skill_metrics(tmp_path)

        assert "$pecial" in metrics["description"], "Should preserve $ characters"
        assert "(characters)" in metrics["description"], "Should preserve parentheses"
        assert "[brackets]" in metrics["description"], "Should preserve brackets"
        assert "*.wildcards" in metrics["description"], "Should preserve asterisks"
        assert "nested 'quotes' inside" in metrics["quoted_phrases"], (
            f"Should extract nested quotes, got: {metrics['quoted_phrases']}"
        )

        print("✅ test_description_with_special_regex_characters passed")


if __name__ == "__main__":
    test_extract_description_from_skill_md()
    test_extract_quoted_phrases()
    test_quoted_phrase_count()
    test_extract_domain_indicators()
    test_domain_indicators_case_insensitive()
    test_domain_indicators_unique()
    test_domain_indicators_mixed_case_deduplication()
    test_forbidden_files_detection()
    test_forbidden_files_multiple()
    test_no_forbidden_files()
    test_line_count()
    test_implementation_details_detection()
    test_implementation_details_various_patterns()
    test_no_implementation_details()
    test_yaml_frontmatter_valid()
    test_yaml_frontmatter_missing()
    test_yaml_frontmatter_incomplete()
    test_extract_metrics_permission_error()
    test_extract_metrics_unicode_decode_error()
    test_yaml_frontmatter_empty_description()
    test_description_with_special_regex_characters()
    print("\n✅ All tests passed!")
