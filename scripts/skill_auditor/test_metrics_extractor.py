#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for metrics_extractor module."""

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
        skill_count = sum(1 for indicator in metrics["domain_indicators"] if indicator.lower() == "skill")
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
        research_count = sum(1 for indicator in metrics["domain_indicators"] if indicator.lower() == "research")
        validation_count = sum(1 for indicator in metrics["domain_indicators"] if indicator.lower() == "validation")

        assert research_count == 1, "Mixed-case 'research'/'Research' should be deduplicated"
        assert validation_count == 1, "Mixed-case 'validation'/'Validation' should be deduplicated"

        # Verify all indicators are lowercase
        for indicator in metrics["domain_indicators"]:
            assert indicator == indicator.lower(), f"Domain indicator '{indicator}' should be lowercase"

        print("✅ test_domain_indicators_mixed_case_deduplication passed")

if __name__ == "__main__":
    test_extract_description_from_skill_md()
    test_extract_quoted_phrases()
    test_quoted_phrase_count()
    test_extract_domain_indicators()
    test_domain_indicators_case_insensitive()
    test_domain_indicators_unique()
    test_domain_indicators_mixed_case_deduplication()
    print("\n✅ All tests passed!")
