#!/usr/bin/env python3
"""Test investigation result aggregation."""

import importlib.util
import sys
from unittest.mock import MagicMock

# Mock the anthropic module to avoid dependency issues during testing
sys.modules["anthropic"] = MagicMock()

# Load the module from the script with hyphens in the name
spec = importlib.util.spec_from_file_location(
    "intelligent_markdown_lint",
    "scripts/intelligent-markdown-lint.py",
)
module = importlib.util.module_from_spec(spec)
sys.modules["intelligent_markdown_lint"] = module
spec.loader.exec_module(module)

aggregate_investigation_results = module.aggregate_investigation_results


def test_aggregate_simple_and_investigated():
    """Test aggregating simple errors with investigation results."""
    simple_files = [
        {"file": "config.md", "errors": [{"line": 45, "code": "MD013", "message": "Line too long"}]}
    ]

    investigation_report = {
        "investigations": [
            {
                "file": "setup.md",
                "results": [
                    {
                        "error": {"line": 23, "code": "MD033", "message": "HTML"},
                        "verdict": "fixable",
                        "reasoning": "Accidental HTML",
                    },
                    {
                        "error": {"line": 15, "code": "MD053", "message": "Ref not found"},
                        "verdict": "false_positive",
                        "reasoning": "Cross-file reference",
                    },
                ],
            }
        ]
    }

    result = aggregate_investigation_results(simple_files, investigation_report)

    assert result["stats"]["simple_errors"] == 1
    assert result["stats"]["investigated_fixable"] == 1
    assert result["stats"]["false_positives"] == 1
    assert result["stats"]["total_fixable"] == 2

    # Check assignment structure
    assert len(result["assignment"]) == 2  # config.md and setup.md

    # Verify context is included
    config_file = next(f for f in result["assignment"] if f["path"] == "config.md")
    assert "context" in config_file["errors"][0]
    assert "Simple error" in config_file["errors"][0]["context"]

    setup_file = next(f for f in result["assignment"] if f["path"] == "setup.md")
    assert "context" in setup_file["errors"][0]
    assert setup_file["errors"][0]["context"] == "Accidental HTML"

    print("✅ Test passed")


if __name__ == "__main__":
    test_aggregate_simple_and_investigated()
