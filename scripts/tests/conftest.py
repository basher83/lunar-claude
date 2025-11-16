"""Pytest configuration for scripts tests."""

import sys
from pathlib import Path

# Add scripts directory to Python path for all tests
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
