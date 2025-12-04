#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema[format]>=4.20.0"]
# ///
"""
Validate research report JSON against schema.

Usage:
    uv run scripts/validate_research_schema.py <json_file>
    uv run scripts/validate_research_schema.py --test
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

# Allowed research sources - centralized for easy extension with new agents
ALLOWED_SOURCES = ["github", "tavily", "deepwiki", "exa"]

# Research Report Schema (from design doc Task 1.1)
# Note: Empty findings arrays are allowed for error/edge cases where an agent
# returns no results. Successful queries should typically produce at least one finding.
RESEARCH_REPORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["query", "source", "findings", "confidence", "timestamp"],
    "properties": {
        "query": {"type": "string", "minLength": 1},
        "source": {"type": "string", "enum": ALLOWED_SOURCES},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "url", "summary", "relevance"],
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string", "format": "uri"},
                    "summary": {"type": "string"},
                    "relevance": {"type": "number", "minimum": 0, "maximum": 1},
                    "code_snippets": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "timestamp": {"type": "string", "format": "date-time"},
    },
}

# Module-level validator with format checking enabled for uri and date-time
VALIDATOR = Draft7Validator(RESEARCH_REPORT_SCHEMA, format_checker=FormatChecker())


def validate_report(json_data: dict) -> tuple[bool, list[str]]:
    """Validate a research report object against the JSON schema.

    Args:
        json_data: Parsed JSON payload representing a single research report.

    Returns:
        A tuple of:
        - bool: True if the report is valid.
        - list[str]: Human-readable error messages if invalid (empty when valid).
    """
    errors = list(VALIDATOR.iter_errors(json_data))

    if errors:
        error_messages = [f"{e.json_path}: {e.message}" for e in errors]
        return False, error_messages
    return True, []


def run_self_test() -> bool:
    """Run built-in valid/invalid self-tests for the research schema.

    Returns:
        True if all self-tests behave as expected (valid report passes,
        invalid variants fail); False otherwise.
    """
    print("Running self-test...\n")
    all_passed = True

    # Valid example
    valid_report = {
        "query": "kubernetes deployment patterns",
        "source": "github",
        "findings": [
            {
                "title": "K8s Best Practices",
                "url": "https://github.com/example/k8s-patterns",
                "summary": "Production-ready Kubernetes patterns",
                "relevance": 0.95,
                "code_snippets": ["apiVersion: apps/v1"],
            }
        ],
        "confidence": 0.85,
        "timestamp": "2025-12-01T10:00:00Z",
    }

    is_valid, errors = validate_report(valid_report)
    test_passed = is_valid
    print(f"Valid report test: {'PASS' if test_passed else 'FAIL'}")
    if not test_passed:
        all_passed = False
        print(f"  Errors: {errors}")

    # Invalid example (missing required field)
    invalid_report = {
        "query": "test",
        "source": "github",
        # missing: findings, confidence, timestamp
    }

    is_valid, errors = validate_report(invalid_report)
    test_passed = not is_valid  # Should be invalid
    print(f"Invalid report test: {'PASS' if test_passed else 'FAIL'}")
    if not test_passed:
        all_passed = False
    else:
        print(f"  Caught errors: {len(errors)} validation errors (expected)")

    # Invalid enum
    invalid_source = {
        "query": "test",
        "source": "invalid_source",  # Not in enum
        "findings": [],
        "confidence": 0.5,
        "timestamp": "2025-12-01T10:00:00Z",
    }

    is_valid, errors = validate_report(invalid_source)
    test_passed = not is_valid  # Should be invalid
    print(f"Invalid source test: {'PASS' if test_passed else 'FAIL'}")
    if not test_passed:
        all_passed = False

    print(f"\nSelf-test complete: {'ALL PASSED' if all_passed else 'FAILURES DETECTED'}")
    return all_passed


def main() -> None:
    """CLI entrypoint for validating research report JSON files.

    Exits with status code 0 on success and non-zero on validation or I/O errors.
    """
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/validate_research_schema.py <json_file>")
        print("       uv run scripts/validate_research_schema.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        success = run_self_test()
        sys.exit(0 if success else 1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: Not a file or does not exist: {json_path}")
        sys.exit(1)

    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_path}")
        print(f"  Line {e.lineno}, Column {e.colno}: {e.msg}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading {json_path}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: File encoding issue in {json_path}")
        print(f"  {e.reason} at position {e.start}")
        print("  Hint: Ensure the file is UTF-8 encoded")
        sys.exit(1)
    except OSError as e:
        print(f"Error: Cannot read {json_path}: {e.strerror}")
        sys.exit(1)

    is_valid, errors = validate_report(data)

    if is_valid:
        print(f"✓ Valid: {json_path}")
        sys.exit(0)
    else:
        print(f"✗ Invalid: {json_path}")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
