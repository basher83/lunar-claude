#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Skill Initializer - Creates a new skill from template or research.

Usage:
    init_skill.py <skill-name> --path <path> [--research-dir <research-path>]

Examples:
    # Basic initialization with example files
    ./init_skill.py my-new-skill --path plugins/meta/meta-claude/skills/

    # With research - copies research to references, generates SKILL.md with links
    ./init_skill.py coderabbit --path plugins/meta/meta-claude/skills/ --research-dir docs/research/coderabbit/
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Template for SKILL.md when NO research is provided (includes TODO placeholders)
SKILL_TEMPLATE_BASIC = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Quick Start

[TODO: Add quick start examples here]

## Resources

This skill includes resource directories for bundled content:

- **references/** - Documentation loaded into context as needed
- **scripts/** - Executable code for automation
- **assets/** - Files used in output (templates, images, etc.)

Delete any unneeded directories.
"""

# Template for SKILL.md when research IS provided (includes reference links)
SKILL_TEMPLATE_WITH_RESEARCH = """---
name: {skill_name}
description: >
  [TODO: Complete description of what this skill does. Include trigger phrases
  like "when user asks to...", "use when...", specific file types, or tasks.]
---

# {skill_title}

[TODO: 1-2 sentences explaining what this skill enables]

## Quick Start

[TODO: Add quick start examples - CLI commands, code snippets, or workflows]

## References

This skill includes detailed documentation in the references/ directory:

{reference_links}

[TODO: Add sections summarizing key content from references. Keep SKILL.md
concise and link to references for details.]
"""


def title_case_skill_name(skill_name: str) -> str:
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def find_markdown_files(research_dir: Path) -> list[Path]:
    """Find all markdown files in research directory recursively."""
    return sorted(research_dir.rglob("*.md"))


def copy_research_to_references(research_dir: Path, references_dir: Path) -> list[tuple[str, str]]:
    """
    Copy markdown files from research to references directory.

    Returns list of (filename, original_path) tuples for reference link generation.
    """
    references_dir.mkdir(parents=True, exist_ok=True)
    copied_files = []

    md_files = find_markdown_files(research_dir)

    for src_file in md_files:
        # Flatten nested paths: cli/commands.md -> cli-commands.md
        relative = src_file.relative_to(research_dir)
        if len(relative.parts) > 1:
            # Nested file - flatten with hyphens
            flat_name = "-".join(relative.parts[:-1]) + "-" + relative.name
        else:
            flat_name = relative.name

        dest_file = references_dir / flat_name

        # Skip README files (usually just indices)
        if src_file.name.lower() == "readme.md":
            continue

        shutil.copy2(src_file, dest_file)
        copied_files.append((flat_name, str(relative)))
        print(f"  ✓ Copied {relative} → references/{flat_name}")

    return copied_files


def generate_reference_links(copied_files: list[tuple[str, str]]) -> str:
    """Generate markdown links for all copied reference files."""
    if not copied_files:
        return "- No reference files found"

    lines = []
    for filename, _original in copied_files:
        # Convert filename to readable title: yaml-configuration-guide.md -> Yaml Configuration Guide
        title = filename.replace(".md", "").replace("-", " ").title()
        lines.append(f"- **{title}:** See [references/{filename}](references/{filename})")

    return "\n".join(lines)


def init_skill_basic(skill_name: str, skill_dir: Path) -> bool:
    """Initialize skill with basic template and example files."""
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE_BASIC.format(skill_name=skill_name, skill_title=skill_title)

    # Create SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_content)
    print("✅ Created SKILL.md (basic template)")

    # Create empty resource directories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)
    print("✅ Created scripts/, references/, assets/ directories")

    return True


def init_skill_with_research(skill_name: str, skill_dir: Path, research_dir: Path) -> bool:
    """Initialize skill from research materials."""
    skill_title = title_case_skill_name(skill_name)
    references_dir = skill_dir / "references"

    # Copy research files to references
    print(f"\n📁 Copying research from {research_dir}:")
    copied_files = copy_research_to_references(research_dir, references_dir)

    if not copied_files:
        print("⚠️  No markdown files found in research directory")
        print("   Falling back to basic template")
        return init_skill_basic(skill_name, skill_dir)

    # Generate reference links for SKILL.md
    reference_links = generate_reference_links(copied_files)

    # Create SKILL.md with research-aware template
    skill_content = SKILL_TEMPLATE_WITH_RESEARCH.format(
        skill_name=skill_name,
        skill_title=skill_title,
        reference_links=reference_links,
    )

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_content)
    print(f"\n✅ Created SKILL.md with {len(copied_files)} reference links")

    return True


def init_skill(skill_name: str, path: str, research_dir: str | None = None) -> Path | None:
    """
    Initialize a new skill directory.

    Args:
        skill_name: Name of the skill (hyphen-case)
        path: Directory where skill folder will be created
        research_dir: Optional path to research materials

    Returns:
        Path to created skill directory, or None if error
    """
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Validate research directory if provided
    if research_dir:
        research_path = Path(research_dir).resolve()
        if not research_path.exists():
            print(f"❌ Error: Research directory not found: {research_path}")
            return None
        if not research_path.is_dir():
            print(f"❌ Error: Research path is not a directory: {research_path}")
            return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Initialize based on whether research was provided
    try:
        if research_dir:
            success = init_skill_with_research(skill_name, skill_dir, Path(research_dir).resolve())
        else:
            success = init_skill_basic(skill_name, skill_dir)

        if not success:
            return None

    except Exception as e:
        print(f"❌ Error initializing skill: {e}")
        return None

    # Print summary
    print(f"\n✅ Skill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md - complete TODOs and refine description")
    if research_dir:
        print("2. Review references/ - remove any unnecessary files")
        print("3. Add Quick Start examples and key content summaries")
    else:
        print("2. Add content to SKILL.md based on skill purpose")
        print("3. Add scripts/, references/, or assets/ as needed")
    print("4. Run validator to check skill structure")

    return skill_dir


def parse_args(args: list[str]) -> tuple[str, str, str | None]:
    """Parse command line arguments."""
    skill_name = None
    path = None
    research_dir = None

    i = 0
    while i < len(args):
        if args[i] == "--path" and i + 1 < len(args):
            path = args[i + 1]
            i += 2
        elif args[i] == "--research-dir" and i + 1 < len(args):
            research_dir = args[i + 1]
            i += 2
        elif not args[i].startswith("--") and skill_name is None:
            skill_name = args[i]
            i += 1
        else:
            i += 1

    return skill_name, path, research_dir


def print_usage():
    """Print usage information."""
    print("Usage: init_skill.py <skill-name> --path <path> [--research-dir <dir>]")
    print("\nArguments:")
    print("  <skill-name>       Skill name in hyphen-case (e.g., 'code-reviewer')")
    print("  --path <path>      Directory where skill folder will be created")
    print("  --research-dir     Optional: Path to research materials to copy")
    print("\nExamples:")
    print("  # Basic skill with template")
    print("  init_skill.py my-skill --path plugins/meta/meta-claude/skills/")
    print()
    print("  # Skill from research (copies research to references/)")
    print("  init_skill.py coderabbit --path plugins/meta/meta-claude/skills/ \\")
    print("      --research-dir docs/research/coderabbit/")


def main():
    """Main entry point."""
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    skill_name, path, research_dir = parse_args(sys.argv[1:])

    if not skill_name or not path:
        print("❌ Error: Missing required arguments")
        print()
        print_usage()
        sys.exit(1)

    print(f"🚀 Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    if research_dir:
        print(f"   Research: {research_dir}")
    print()

    result = init_skill(skill_name, path, research_dir)

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
