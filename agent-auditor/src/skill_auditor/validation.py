"""Validation utilities for skill auditor."""

from typing import Any


def validate_metrics_structure(metrics: dict[str, Any]) -> None:
    """
    Validate that metrics dict contains all required fields.

    Args:
        metrics: Metrics dictionary to validate

    Raises:
        ValueError: If required keys are missing
    """
    required_keys = [
        "skill_name",
        "skill_path",
        "description",
        "quoted_phrases",
        "quoted_count",
        "domain_indicators",
        "domain_count",
        "forbidden_files",
        "implementation_details",
        "line_count",
        "has_frontmatter",
        "yaml_delimiters",
        "has_name",
        "has_description",
    ]

    missing_keys = [key for key in required_keys if key not in metrics]

    if missing_keys:
        raise ValueError(
            f"Metrics extraction incomplete. Missing required keys: "
            f"{', '.join(missing_keys)}. This is likely a bug in metrics_extractor."
        )
