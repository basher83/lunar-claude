"""Tests for package_skill.py script."""

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "skill-creator" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from package_skill import package_skill


class TestPackageSkill:
    """Test skill packaging functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    @pytest.fixture
    def valid_skill(self, temp_dir):
        """Create a valid skill for testing."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        # Create SKILL.md with valid frontmatter
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for packaging
---

# Test Skill

This is a test skill.
""")

        # Create some additional files
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "test.py").write_text("print('Hello')")

        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        (refs_dir / "readme.md").write_text("# Reference")

        return skill_dir

    def test_package_nonexistent_skill(self, temp_dir):
        """Should return None for nonexistent skill."""
        result = package_skill(temp_dir / "nonexistent")
        assert result is None

    def test_package_file_instead_of_directory(self, temp_dir):
        """Should return None when path is a file, not directory."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Not a directory")

        result = package_skill(test_file)
        assert result is None

    def test_package_directory_without_skill_md(self, temp_dir):
        """Should return None when SKILL.md is missing."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        result = package_skill(skill_dir)
        assert result is None

    def test_package_invalid_skill(self, temp_dir):
        """Should return None when skill fails validation."""
        skill_dir = temp_dir / "test-skill"
        skill_dir.mkdir()

        # Create SKILL.md without proper frontmatter
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("# Invalid Skill\n\nNo frontmatter")

        result = package_skill(skill_dir)
        assert result is None

    def test_package_valid_skill(self, valid_skill, temp_dir):
        """Should create .skill file for valid skill."""
        result = package_skill(valid_skill, temp_dir)

        assert result is not None
        assert result.exists()
        assert result.suffix == ".skill"
        assert result.name == "test-skill.skill"

    def test_package_creates_valid_zip(self, valid_skill, temp_dir):
        """Should create valid zip archive."""
        result = package_skill(valid_skill, temp_dir)

        assert zipfile.is_zipfile(result)

    def test_package_includes_all_files(self, valid_skill, temp_dir):
        """Should include all skill files in package."""
        result = package_skill(valid_skill, temp_dir)

        with zipfile.ZipFile(result, 'r') as zf:
            names = zf.namelist()

            # Should contain SKILL.md and created files
            assert any("SKILL.md" in name for name in names)
            assert any("scripts/test.py" in name for name in names)
            assert any("references/readme.md" in name for name in names)

    def test_package_default_output_location(self, valid_skill):
        """Should create package in current directory when no output specified."""
        result = package_skill(valid_skill)

        assert result is not None
        assert result.parent == Path.cwd()

        # Cleanup
        if result and result.exists():
            result.unlink()

    def test_package_custom_output_location(self, valid_skill, temp_dir):
        """Should create package in specified output directory."""
        output_dir = temp_dir / "output"
        result = package_skill(valid_skill, output_dir)

        assert result is not None
        assert result.parent == output_dir
        assert output_dir.exists()

    def test_package_creates_output_directory(self, valid_skill, temp_dir):
        """Should create output directory if it doesn't exist."""
        output_dir = temp_dir / "nested" / "output"
        assert not output_dir.exists()

        result = package_skill(valid_skill, output_dir)

        assert result is not None
        assert output_dir.exists()
