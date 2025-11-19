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

if __name__ == "__main__":
    test_extract_description_from_skill_md()
    test_extract_quoted_phrases()
    test_quoted_phrase_count()
    print("\n✅ All tests passed!")
