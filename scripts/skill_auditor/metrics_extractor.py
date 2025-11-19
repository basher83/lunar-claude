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

    # Extract description (handles both multiline '>' and single-line formats)
    # Try multiline format first
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        # Try single-line format
        simple_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
        description = simple_match.group(1).strip() if simple_match else ""

    # Extract quoted phrases (deterministic regex)
    quoted_phrases = re.findall(r'"([^"]+)"', description)

    return {
        "description": description,
        "quoted_phrases": quoted_phrases,
        "quoted_count": len(quoted_phrases),
    }
