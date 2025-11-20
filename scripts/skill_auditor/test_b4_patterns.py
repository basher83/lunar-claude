"""Tests for B4 implementation detail detection patterns.

This module validates the check_b4_implementation_details() function's ability to:
- Detect file extensions (e.g., .yaml, .py, .js)
- Detect command paths (e.g., /commands:sync)
- Detect architecture patterns (e.g., multi-tier, 8-phase)
- Detect tool/library names (e.g., firecrawl, docker, pandas)
- Avoid false positives on conceptual terms

Run as a module:
    python -m scripts.skill_auditor.test_b4_patterns

Run with pytest:
    pytest scripts/skill_auditor/test_b4_patterns.py
"""

from .metrics_extractor import check_b4_implementation_details


def test_b4_function_exists() -> None:
    """B4 check function should be callable and handle edge cases."""
    result = check_b4_implementation_details("clean description")
    assert isinstance(result, list)
    assert len(result) == 0, "Clean description should have no violations"

    # Edge cases
    assert check_b4_implementation_details("") == [], "Empty string should return empty list"
    result_special = check_b4_implementation_details("!@#$%^&*()")
    assert isinstance(result_special, list), "Special characters should not raise exceptions"


def test_b4_catches_file_extensions() -> None:
    """B4 should detect file extensions in descriptions"""
    # Note: Integration tests in test_metrics_extractor.py also cover file extensions
    cases = [
        ("loads config from settings.yaml", ["settings.yaml"]),
        ("runs script.py and helper.sh", ["script.py", "helper.sh"]),
        ("processes data.json and output.csv", ["data.json", "output.csv"]),
        ("executes main.ts with config.yml", ["main.ts", "config.yml"]),
    ]

    for description, expected_violations in cases:
        result = check_b4_implementation_details(description)
        assert set(result) == set(expected_violations), \
            f"Expected {expected_violations}, got {result} for: {description}"


def test_b4_catches_command_paths() -> None:
    """B4 should detect command path patterns like /commands:name"""
    # Note: Integration tests in test_metrics_extractor.py also cover command paths
    cases = [
        ("invokes /commands:sync and /tools:analyze", ["/commands:sync", "/tools:analyze"]),
        ("uses /commit:push for changes", ["/commit:push"]),
        ("runs /review:code before merge", ["/review:code"]),
    ]

    for description, expected_violations in cases:
        result = check_b4_implementation_details(description)
        assert set(result) == set(expected_violations), \
            f"Expected {expected_violations}, got {result} for: {description}"


def test_b4_catches_architecture_patterns() -> None:
    """B4 should detect architecture terminology"""
    cases = [
        ("uses multi-tier approach", ["multi-tier"]),
        ("implements 8-phase processing", ["8-phase"]),
        ("three-stage pipeline", ["three-stage"]),
        ("5-step workflow", ["5-step"]),
    ]

    for description, expected_violations in cases:
        result = check_b4_implementation_details(description)
        assert set(result) == set(expected_violations), \
            f"Expected {expected_violations}, got {result} for: {description}"


def test_b4_catches_tool_names() -> None:
    """B4 should detect specific tool and library names"""
    cases = [
        ("uses firecrawl for scraping", ["firecrawl"]),
        ("built with docker and kubernetes", ["docker", "kubernetes"]),
        ("leverages pandas and numpy", ["pandas", "numpy"]),
        ("implements with react and express", ["react", "express"]),
    ]

    for description, expected_violations in cases:
        result = check_b4_implementation_details(description)
        assert set(result) == set(expected_violations), \
            f"Expected {expected_violations}, got {result} for: {description}"


def test_b4_allows_conceptual_terms() -> None:
    """B4 should NOT flag conceptual/abstract terminology"""
    cases = [
        "processes data in multiple tiers",  # "tiers" not "multi-tier"
        "works in phases",  # "phases" not "8-phase"
        "handles web content",  # conceptual, not "firecrawl"
        "provides an API for users",  # conceptual use, not implementation
        "manages database connections",  # conceptual, not "postgresql"
        "framework-agnostic approach",  # mentions framework conceptually
    ]

    for description in cases:
        result = check_b4_implementation_details(description)
        assert len(result) == 0, f"Should NOT flag: '{description}' but found: {result}"


def main() -> None:
    """Run all tests when executed as a module."""
    test_b4_function_exists()
    print("✅ test_b4_function_exists")

    test_b4_catches_file_extensions()
    print("✅ test_b4_catches_file_extensions")

    test_b4_catches_command_paths()
    print("✅ test_b4_catches_command_paths")

    test_b4_catches_architecture_patterns()
    print("✅ test_b4_catches_architecture_patterns")

    test_b4_catches_tool_names()
    print("✅ test_b4_catches_tool_names")

    test_b4_allows_conceptual_terms()
    print("✅ test_b4_allows_conceptual_terms")

    print("\nAll tests passed!")


if __name__ == "__main__":
    main()
