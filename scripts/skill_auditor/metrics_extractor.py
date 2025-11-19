#!/usr/bin/env python3
"""Deterministic metrics extraction from SKILL.md files."""

import re
from pathlib import Path
from typing import Dict, Any

def extract_skill_metrics(skill_path: Path) -> Dict[str, Any]:
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

    content = skill_md.read_text()

    # Extract description (between 'description: >' and '---')
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    return {
        "description": description,
    }
