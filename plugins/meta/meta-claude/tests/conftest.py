"""Pytest configuration for meta-claude tests."""

import sys
from pathlib import Path

# Add scripts directory to Python path for all tests
SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "skill-creator" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
