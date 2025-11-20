#!/usr/bin/env python3
"""Deterministic metrics extraction from SKILL.md files."""

import re
from pathlib import Path
from typing import Any


def extract_skill_metrics(skill_path: Path) -> dict[str, Any]:
    """
    Extract all audit metrics from a skill directory.

    Args:
        skill_path: Path to skill directory containing SKILL.md

    Returns:
        Dictionary of extracted metrics
    """
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    try:
        content = skill_md.read_text()
    except PermissionError as e:
        raise PermissionError(
            f"Permission denied when reading {skill_md}. "
            f"Please check file permissions and try again."
        ) from e
    except UnicodeDecodeError as e:
        raise ValueError(
            f"Unable to read {skill_md} due to encoding issues. "
            f"Please ensure the file is UTF-8 encoded. Error: {e}"
        ) from e
    except OSError as e:
        raise OSError(
            f"I/O error when reading {skill_md}: {e}. "
            f"Please check that the file is accessible and try again."
        ) from e

    # Extract YAML frontmatter fields
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    skill_name = name_match.group(1).strip() if name_match else "unknown"

    # Extract description (handles both multiline '>' and single-line formats)
    # Try multiline format first
    desc_match = re.search(r"description:\s*>\s*(.*?)^---", content, re.MULTILINE | re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        # Try single-line format
        simple_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
        description = simple_match.group(1).strip() if simple_match else ""

    # Extract quoted phrases (deterministic regex)
    quoted_phrases = re.findall(r'"([^"]+)"', description)

    # Extract domain indicators (exact regex from v5 agent)
    domain_pattern = (
        r"\b(SKILL\.md|\.skill|YAML|Claude Code|Anthropic|"
        r"skill|research|validation|compliance|specification|frontmatter)\b"
    )
    domain_matches = re.findall(domain_pattern, description, re.IGNORECASE)
    domain_indicators = list(
        set(match.lower() for match in domain_matches)
    )  # Unique, case-normalized

    # Check for forbidden files (B1)
    forbidden_patterns = ["README*", "INSTALL*", "CHANGELOG*", "QUICK*"]
    forbidden_files = []
    for pattern in forbidden_patterns:
        forbidden_files.extend([f.name for f in skill_path.glob(pattern)])

    # Check for implementation details in description (B4)
    impl_pattern = r"\w+\.(py|sh|js|md|txt|json)|/[a-z-]+:[a-z-]+"
    implementation_details = re.findall(impl_pattern, description)

    # Line count (B3)
    line_count = len(content.split("\n"))

    # Check for YAML frontmatter (B2)
    has_frontmatter = content.startswith("---")
    yaml_delimiters = len(re.findall(r"^---$", content, re.MULTILINE))
    has_name = name_match is not None
    has_description = desc_match is not None or simple_match is not None

    return {
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "description": description,
        "quoted_phrases": quoted_phrases,
        "quoted_count": len(quoted_phrases),
        "domain_indicators": domain_indicators,
        "domain_count": len(domain_indicators),
        "forbidden_files": forbidden_files,
        "implementation_details": implementation_details,
        "line_count": line_count,
        "has_frontmatter": has_frontmatter,
        "yaml_delimiters": yaml_delimiters,
        "has_name": has_name,
        "has_description": has_description,
    }
