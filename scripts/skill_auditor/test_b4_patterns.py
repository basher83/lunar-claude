"""Tests for B4 implementation detail detection patterns."""
import pytest
from skill_auditor.metrics_extractor import check_b4_implementation_details


def test_b4_function_exists():
    """B4 check function should be callable"""
    result = check_b4_implementation_details("clean description")
    assert isinstance(result, list)
