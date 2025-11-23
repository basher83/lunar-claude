#!/usr/bin/env python3
"""Integration test for deterministic metrics extraction."""

import sys
import tempfile
from pathlib import Path

# Add src directory to path for package imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_auditor.metrics_extractor import extract_skill_metrics


def test_metrics_extraction_is_deterministic():
    """
    Test that extracting metrics multiple times produces identical results.

    This is a regression test for the core requirement: Python extraction
    must be deterministic to prevent feedback loops from non-deterministic
    bash command execution.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Create "SKILL.md files" with "YAML frontmatter" for "Claude Code".
  Validate skill structure and compliance using research and analysis.
---

# Test Skill

This is a test skill for determinism verification.
""")

        # Extract metrics 5 times
        results = [extract_skill_metrics(tmp_path) for _ in range(5)]

        # All results should be identical
        first_result = results[0]
        for i, result in enumerate(results[1:], start=1):
            assert result == first_result, (
                f"Run {i + 1} produced different metrics than run 1.\n"
                f"Run 1: {first_result}\n"
                f"Run {i + 1}: {result}"
            )

        # Verify specific metrics are stable and correct
        for i, result in enumerate(results):
            assert result["quoted_count"] == 3, (
                f"Run {i + 1}: Expected 3 quoted phrases, got {result['quoted_count']}"
            )
            assert result["domain_count"] >= 5, (
                f"Run {i + 1}: Expected ≥5 domain indicators, got {result['domain_count']}"
            )
            assert result["line_count"] > 0, f"Run {i + 1}: Line count should be > 0"
            assert result["skill_name"] == "test-skill", (
                f"Run {i + 1}: Skill name should be 'test-skill'"
            )

        print("✅ test_metrics_extraction_is_deterministic passed")


def test_domain_indicators_deduplication_is_deterministic():
    """Test that domain indicator deduplication is consistent across runs."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: >
  Research YAML, research skill, RESEARCH validation, YAML parsing.
---
""")

        # Extract multiple times
        results = [extract_skill_metrics(tmp_path) for _ in range(5)]

        # Domain indicators should be deduplicated identically each time
        for i, result in enumerate(results):
            # Should have "research" and "yaml" (lowercase, deduplicated)
            indicators = set(result["domain_indicators"])
            assert "research" in indicators, f"Run {i + 1}: Missing 'research' indicator"
            assert "yaml" in indicators, f"Run {i + 1}: Missing 'yaml' indicator"

            # Count should be consistent
            assert result["domain_count"] == results[0]["domain_count"], (
                f"Run {i + 1}: Domain count changed from {results[0]['domain_count']} to {result['domain_count']}"
            )

        print("✅ test_domain_indicators_deduplication_is_deterministic passed")


if __name__ == "__main__":
    test_metrics_extraction_is_deterministic()
    test_domain_indicators_deduplication_is_deterministic()
    print("\n✅ All determinism tests passed!")
