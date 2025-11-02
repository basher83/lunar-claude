#!/usr/bin/env python3
"""Test investigation result aggregation."""


def aggregate_investigation_results(simple_files, investigation_report):
    """
    Aggregate simple errors and investigation results into single Fixer assignment.

    This is a copy of the function from intelligent-markdown-lint.py for testing purposes.
    """
    # Start with simple errors (add context)
    fixer_files = {}

    for file_data in simple_files:
        path = file_data["file"]
        fixer_files[path] = {
            "path": path,
            "errors": [
                {**error, "context": f"Simple error - always fixable (code: {error['code']})"}
                for error in file_data["errors"]
            ],
        }

    # Add investigated errors that are fixable
    investigated_fixable = 0
    false_positives = 0

    for investigation in investigation_report.get("investigations", []):
        file_path = investigation["file"]

        for result in investigation.get("results", []):
            if result["verdict"] == "fixable":
                investigated_fixable += 1

                # Add to fixer assignment with investigation context
                if file_path not in fixer_files:
                    fixer_files[file_path] = {"path": file_path, "errors": []}

                fixer_files[file_path]["errors"].append(
                    {**result["error"], "context": result["reasoning"]}
                )

            elif result["verdict"] == "false_positive":
                false_positives += 1

    assignment = list(fixer_files.values())
    simple_errors = sum(len(f["errors"]) for f in simple_files)

    return {
        "assignment": assignment,
        "stats": {
            "simple_errors": simple_errors,
            "investigated_fixable": investigated_fixable,
            "total_fixable": simple_errors + investigated_fixable,
            "false_positives": false_positives,
        },
    }


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
