"""Tests for init_skill.py script."""

import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "skill-creator" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from init_skill import create_skill_structure, validate_skill_name


class TestSkillNameValidation:
    """Test skill name validation."""

    def test_valid_skill_names(self):
        """Valid skill names should pass validation."""
        valid_names = [
            "my-skill",
            "test-skill-123",
            "a-b-c",
            "skill-with-numbers-42",
        ]
        for name in valid_names:
            assert validate_skill_name(name) is True, f"'{name}' should be valid"

    def test_invalid_skill_names(self):
        """Invalid skill names should fail validation."""
        invalid_names = [
            "MySkill",  # uppercase
            "my_skill",  # underscore
            "my skill",  # space
            "my-skill-",  # trailing hyphen
            "-my-skill",  # leading hyphen
            "123-skill",  # starts with number
            "",  # empty
            "a",  # too short
        ]
        for name in invalid_names:
            assert validate_skill_name(name) is False, f"'{name}' should be invalid"


class TestSkillCreation:
    """Test skill structure creation."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    def test_create_basic_skill_structure(self, temp_dir):
        """Should create basic skill structure."""
        skill_name = "test-skill"
        skill_path = temp_dir / skill_name

        create_skill_structure(skill_name, temp_dir)

        assert skill_path.exists(), "Skill directory should be created"
        assert skill_path.is_dir(), "Skill path should be a directory"
        assert (skill_path / "SKILL.md").exists(), "SKILL.md should be created"

    def test_skill_md_has_frontmatter(self, temp_dir):
        """Created SKILL.md should have valid frontmatter."""
        skill_name = "test-skill"
        skill_path = temp_dir / skill_name

        create_skill_structure(skill_name, temp_dir)

        skill_md = skill_path / "SKILL.md"
        content = skill_md.read_text()

        assert content.startswith("---"), "Should start with frontmatter delimiter"
        assert "name: test-skill" in content, "Should contain skill name"
        assert "description:" in content, "Should contain description field"

    def test_creates_resource_directories(self, temp_dir):
        """Should create scripts and references directories."""
        skill_name = "test-skill"
        skill_path = temp_dir / skill_name

        create_skill_structure(skill_name, temp_dir)

        assert (skill_path / "scripts").exists(), "scripts/ directory should be created"
        assert (skill_path / "references").exists(), "references/ directory should be created"

    def test_creates_placeholder_files(self, temp_dir):
        """Should create .gitkeep files in resource directories."""
        skill_name = "test-skill"
        skill_path = temp_dir / skill_name

        create_skill_structure(skill_name, temp_dir)

        assert (skill_path / "scripts" / ".gitkeep").exists()
        assert (skill_path / "references" / ".gitkeep").exists()

    def test_error_if_directory_exists(self, temp_dir):
        """Should raise error if skill directory already exists."""
        skill_name = "test-skill"
        skill_path = temp_dir / skill_name
        skill_path.mkdir()

        with pytest.raises(FileExistsError):
            create_skill_structure(skill_name, temp_dir)
