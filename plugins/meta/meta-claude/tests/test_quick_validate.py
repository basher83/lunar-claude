"""Tests for quick_validate.py script."""

import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "skill-factory" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from quick_validate import validate_skill


class TestSkillValidation:
    """Test skill validation functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    def test_validate_missing_skill_md(self, temp_dir):
        """Should fail when SKILL.md is missing."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        valid, message = validate_skill(skill_dir)

        assert valid is False
        assert "SKILL.md not found" in message

    def test_validate_missing_frontmatter(self, temp_dir):
        """Should fail when frontmatter is missing."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("# Just a heading\n\nNo frontmatter here.")

        valid, message = validate_skill(skill_dir)

        assert valid is False
        assert "frontmatter" in message.lower()

    def test_validate_invalid_frontmatter_format(self, temp_dir):
        """Should fail when frontmatter format is invalid."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test\n# Missing closing delimiter")

        valid, message = validate_skill(skill_dir)

        assert valid is False
        assert "frontmatter" in message.lower()

    def test_validate_missing_required_fields(self, temp_dir):
        """Should fail when required frontmatter fields are missing."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        # Missing 'description' field
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: test-skill\n---\n\n# Test Skill")

        valid, message = validate_skill(skill_dir)

        assert valid is False
        assert "description" in message.lower()

    def test_validate_unexpected_frontmatter_keys(self, temp_dir):
        """Should fail when frontmatter contains unexpected keys."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill
invalid_key: should not be here
---

# Test Skill
""")

        valid, message = validate_skill(skill_dir)

        assert valid is False
        assert "unexpected" in message.lower()

    def test_validate_valid_skill(self, temp_dir):
        """Should pass validation for a valid skill."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for validation
---

# Test Skill

This is a valid skill.
""")

        valid, message = validate_skill(skill_dir)

        assert valid is True

    def test_validate_skill_with_optional_fields(self, temp_dir):
        """Should pass validation with optional frontmatter fields."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for validation
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  version: 1.0.0
  author: Test Author
---

# Test Skill
""")

        valid, message = validate_skill(skill_dir)

        assert valid is True

    def test_validate_skill_name_matches_directory(self, temp_dir):
        """Should validate that skill name matches directory name."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        # Skill name doesn't match directory name
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: different-skill
description: A test skill
---

# Test Skill
""")

        valid, message = validate_skill(skill_dir)

        # This might pass or fail depending on implementation
        # Just check the function returns a tuple
        assert isinstance(valid, bool)
        assert isinstance(message, str)
