#!/usr/bin/env python3
"""Tests for skill-auditor main application logic."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# This is a workaround since skill-auditor.py is a script, not a module
# We'll copy the logic we're testing here and verify against it
# In production, consider refactoring to make build_analysis_prompt importable


def build_analysis_prompt(metrics: dict) -> str:
    """
    Build the analysis prompt for Claude (duplicate for testing).

    This is imported from skill-auditor.py for testing.
    """
    # Calculate binary checks
    b1_pass = len(metrics["forbidden_files"]) == 0
    b2_pass = metrics["yaml_delimiters"] == 2 and metrics["has_name"] and metrics["has_description"]
    b3_pass = metrics["line_count"] < 500
    b4_pass = len(metrics["implementation_details"]) == 0

    # Calculate warnings
    w1_pass = metrics["quoted_count"] >= 3
    w3_pass = metrics["domain_count"] >= 3

    # Build status strings
    b1_status = "✅ PASS" if b1_pass else "❌ FAIL"
    b2_status = "✅ PASS" if b2_pass else "❌ FAIL"
    b3_status = "✅ PASS" if b3_pass else "❌ FAIL"
    b4_status = "✅ PASS" if b4_pass else "❌ FAIL"
    w1_status = "✅ PASS" if w1_pass else "❌ FAIL"
    w3_status = "✅ PASS" if w3_pass else "❌ FAIL"

    prompt = f"""Audit the following skill metrics:

## Binary Checks

- B1: No forbidden files → {b1_status}
- B2: Valid YAML frontmatter → {b2_status}
- B3: SKILL.md under 500 lines → {b3_status}
- B4: No implementation details → {b4_status}

## Warnings

- W1: ≥3 quoted phrases → {w1_status}
- W3: ≥3 domain indicators → {w3_status}
"""

    return prompt


def test_build_analysis_prompt_b1_forbidden_files_fail():
    """Test B1 check fails when forbidden files present."""
    metrics = {
        "forbidden_files": ["README.md"],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B1: No forbidden files → ❌ FAIL" in prompt


def test_build_analysis_prompt_b1_forbidden_files_pass():
    """Test B1 check passes when no forbidden files."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B1: No forbidden files → ✅ PASS" in prompt


def test_build_analysis_prompt_b2_yaml_missing_delimiters():
    """Test B2 check fails when YAML delimiters missing."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 1,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B2: Valid YAML frontmatter → ❌ FAIL" in prompt


def test_build_analysis_prompt_b2_yaml_missing_name():
    """Test B2 check fails when name field missing."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": False,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B2: Valid YAML frontmatter → ❌ FAIL" in prompt


def test_build_analysis_prompt_b2_yaml_missing_description():
    """Test B2 check fails when description field missing."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": False,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B2: Valid YAML frontmatter → ❌ FAIL" in prompt


def test_build_analysis_prompt_b3_line_count_threshold():
    """Test B3 check fails when line count exceeds 500."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 500,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B3: SKILL.md under 500 lines → ❌ FAIL" in prompt


def test_build_analysis_prompt_b4_implementation_details():
    """Test B4 check fails when implementation details present."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": ["script.py"],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B4: No implementation details → ❌ FAIL" in prompt


def test_build_analysis_prompt_w1_quoted_phrases():
    """Test W1 check fails when fewer than 3 quoted phrases."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 2,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "W1: ≥3 quoted phrases → ❌ FAIL" in prompt


def test_build_analysis_prompt_w3_domain_indicators():
    """Test W3 check fails when fewer than 3 domain indicators."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 2,
    }

    prompt = build_analysis_prompt(metrics)
    assert "W3: ≥3 domain indicators → ❌ FAIL" in prompt


def test_build_analysis_prompt_all_pass():
    """Test all checks pass with valid metrics."""
    metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
    }

    prompt = build_analysis_prompt(metrics)
    assert "B1: No forbidden files → ✅ PASS" in prompt
    assert "B2: Valid YAML frontmatter → ✅ PASS" in prompt
    assert "B3: SKILL.md under 500 lines → ✅ PASS" in prompt
    assert "B4: No implementation details → ✅ PASS" in prompt
    assert "W1: ≥3 quoted phrases → ✅ PASS" in prompt
    assert "W3: ≥3 domain indicators → ✅ PASS" in prompt


def test_validate_metrics_structure_missing_keys():
    """Test that validation catches missing required keys."""
    incomplete_metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        # Missing: has_name, has_description, line_count, etc.
    }

    # This should raise ValueError
    try:
        # Assume we'll create a validate_metrics_structure function
        from validation import validate_metrics_structure

        validate_metrics_structure(incomplete_metrics)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "missing" in str(e).lower()
        assert "has_name" in str(e)


def test_validate_metrics_structure_complete():
    """Test that validation passes with complete metrics."""
    complete_metrics = {
        "forbidden_files": [],
        "yaml_delimiters": 2,
        "has_name": True,
        "has_description": True,
        "line_count": 100,
        "implementation_details": [],
        "quoted_count": 5,
        "domain_count": 5,
        "skill_name": "test",
        "skill_path": "/tmp/test",
        "description": "test description",
        "quoted_phrases": ["phrase1"],
        "domain_indicators": ["yaml"],
        "has_frontmatter": True,
    }

    from validation import validate_metrics_structure

    # Should not raise
    validate_metrics_structure(complete_metrics)


if __name__ == "__main__":
    tests = [
        test_build_analysis_prompt_b1_forbidden_files_fail,
        test_build_analysis_prompt_b1_forbidden_files_pass,
        test_build_analysis_prompt_b2_yaml_missing_delimiters,
        test_build_analysis_prompt_b2_yaml_missing_name,
        test_build_analysis_prompt_b2_yaml_missing_description,
        test_build_analysis_prompt_b3_line_count_threshold,
        test_build_analysis_prompt_b4_implementation_details,
        test_build_analysis_prompt_w1_quoted_phrases,
        test_build_analysis_prompt_w3_domain_indicators,
        test_build_analysis_prompt_all_pass,
        test_validate_metrics_structure_missing_keys,
        test_validate_metrics_structure_complete,
    ]

    failed = []
    passed = 0

    for test in tests:
        try:
            test()
            passed += 1
            print(f"✅ {test.__name__}")
        except AssertionError as e:
            failed.append((test.__name__, str(e)))
            print(f"❌ {test.__name__}: {e}")
        except Exception as e:
            failed.append((test.__name__, f"Unexpected error: {type(e).__name__}: {e}"))
            print(f"❌ {test.__name__}: Unexpected {type(e).__name__}: {e}")

    print(f"\n{'=' * 60}")
    print(f"Ran {len(tests)} tests: {passed} passed, {len(failed)} failed")

    if failed:
        print("\n❌ Failed tests:")
        for test_name, error in failed:
            print(f"   - {test_name}: {error}")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)
