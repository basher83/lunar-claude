#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
#     "pyyaml>=6.0",
# ]
# ///
"""End-to-end test for intelligent markdown linting."""

import asyncio
import os
import shutil
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, "scripts")

# Import module with dashes in filename
import importlib.util

spec = importlib.util.spec_from_file_location(
    "intelligent_markdown_lint", "scripts/intelligent-markdown-lint.py"
)
intelligent_markdown_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intelligent_markdown_lint)

run_rumdl_check = intelligent_markdown_lint.run_rumdl_check
parse_rumdl_output = intelligent_markdown_lint.parse_rumdl_output
triage_errors = intelligent_markdown_lint.triage_errors


async def test_e2e_intelligent_linting():
    """Test complete intelligent linting workflow."""

    # Setup: Copy test fixtures to temp directory
    test_repo = Path("tests/fixtures/test-repo")
    temp_repo = Path("tests/fixtures/test-repo-temp")

    if temp_repo.exists():
        shutil.rmtree(temp_repo)
    shutil.copytree(test_repo, temp_repo)

    original_cwd = os.getcwd()

    try:
        # Change to test repo
        os.chdir(temp_repo)

        # Phase 1: Discovery
        print("📋 Phase 1: Discovery")
        output = run_rumdl_check()
        parsed = parse_rumdl_output(output)

        print(f"Found {parsed['total_errors']} errors")
        assert parsed["total_errors"] > 0, "Should find errors in test fixtures"

        # Phase 2: Triage
        print("\n📊 Phase 2: Triage")
        triaged = triage_errors(parsed)

        print(f"Simple: {triaged['simple_count']}")
        print(f"Ambiguous: {triaged['ambiguous_count']}")

        # Verify expected categorization
        assert triaged["simple_count"] >= 3, "Should find MD013, MD036, MD025"
        assert triaged["ambiguous_count"] >= 2, "Should find MD033, MD041"

        # Expected errors:
        # Simple: MD013 (long line), MD036 (emphasis), MD025 (duplicate H1)
        # Ambiguous: MD033 (<b> and <Tip>), MD041 (after frontmatter)

        print("\n✅ Test passed: Discovery and triage working correctly")

    finally:
        # Cleanup
        os.chdir(original_cwd)
        if temp_repo.exists():
            shutil.rmtree(temp_repo)


if __name__ == "__main__":
    asyncio.run(test_e2e_intelligent_linting())
