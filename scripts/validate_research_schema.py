#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.20.0"]
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

from jsonschema import Draft7Validator

# Research Report Schema (from design doc Task 1.1)
RESEARCH_REPORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["query", "source", "findings", "confidence", "timestamp"],
    "properties": {
        "query": {"type": "string", "minLength": 1},
        "source": {"type": "string", "enum": ["github", "tavily", "deepwiki", "exa"]},
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


def validate_report(json_data: dict) -> tuple[bool, list[str]]:
    """Validate JSON against research report schema."""
    validator = Draft7Validator(RESEARCH_REPORT_SCHEMA)
    errors = list(validator.iter_errors(json_data))

    if errors:
        error_messages = [f"{e.json_path}: {e.message}" for e in errors]
        return False, error_messages
    return True, []


def run_self_test() -> bool:
    """Run self-test with valid and invalid examples."""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/validate_research_schema.py <json_file>")
        print("       uv run scripts/validate_research_schema.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        success = run_self_test()
        sys.exit(0 if success else 1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
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
