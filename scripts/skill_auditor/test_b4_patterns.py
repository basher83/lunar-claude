"""Tests for B4 implementation detail detection patterns."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from metrics_extractor import check_b4_implementation_details


def test_b4_function_exists() -> None:
    """B4 check function should be callable"""
    result = check_b4_implementation_details("clean description")
    assert isinstance(result, list)


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
        assert len(result) > 0, f"Should detect violations in: {description}"
        for violation in expected_violations:
            assert violation in result, f"Should detect '{violation}' in: {description}"


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
        assert len(result) > 0, f"Should detect violations in: {description}"
        for violation in expected_violations:
            assert violation in result, f"Should detect '{violation}' in: {description}"


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
