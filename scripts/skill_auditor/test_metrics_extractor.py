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

if __name__ == "__main__":
    test_extract_description_from_skill_md()
    print("\n✅ All tests passed!")
