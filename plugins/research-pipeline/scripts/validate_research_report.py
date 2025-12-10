#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema"]
# ///
"""
Validate research reports against JSON schema.

Usage:
    ./validate_research_report.py <report.json>
    uv run validate_research_report.py <report.json>

Examples:
    ./validate_research_report.py .claude/research-cache/my-query/github-report.json
    uv run ${CLAUDE_PLUGIN_ROOT}/scripts/validate_research_report.py report.json
"""

import json
import sys
from pathlib import Path

from jsonschema import ValidationError, validate

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "research-report.schema.json"


def validate_report(report_path: str) -> bool:
    """Validate a research report against the schema."""
    report_file = Path(report_path)

    if not report_file.exists():
        print(f"ERROR: File not found: {report_path}")
        return False

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found: {SCHEMA_PATH}")
        return False

    try:
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Schema file contains invalid JSON: {SCHEMA_PATH}")
        print(f"  Parse error at line {e.lineno}, column {e.colno}: {e.msg}")
        return False

    try:
        with open(report_file, encoding="utf-8") as f:
            report = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Report file contains invalid JSON: {report_path}")
        print(f"  Parse error at line {e.lineno}, column {e.colno}: {e.msg}")
        return False

    try:
        validate(instance=report, schema=schema)
        print(f"✓ Valid: {report['researcher']} report")
        print(f"  Confidence: {report['confidence']}")
        print(f"  Sources: {len(report['sources'])}")
        print(f"  Tags: {report['tags']}")
        return True
    except ValidationError as e:
        print("ERROR: Schema validation failed")
        if e.absolute_path:
            path = ".".join(str(p) for p in e.absolute_path)
            print(f"  Location: {path}")
        print(f"  Error: {e.message}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./validate_research_report.py <report.json>")
        sys.exit(1)

    success = validate_report(sys.argv[1])
    sys.exit(0 if success else 1)
