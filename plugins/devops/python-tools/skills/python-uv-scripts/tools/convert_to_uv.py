#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27.0",
# ]
# ///
"""
Convert Python scripts to uv single-file format (PEP 723)

Purpose: script-conversion-automation
Team: devops
Author: devops@spaceships.work

Converts existing Python scripts to use inline dependency management.
Reads dependencies from requirements.txt or detects from imports.

Usage:
    convert_to_uv.py <script.py>
    convert_to_uv.py <script.py> --requirements requirements.txt
    convert_to_uv.py <script.py> --detect-imports
    convert_to_uv.py <script.py> --dry-run

Examples:
    # Convert script with requirements.txt in same directory
    convert_to_uv.py my_script.py

    # Convert script with specific requirements file
    convert_to_uv.py my_script.py --requirements ../requirements.txt

    # Detect dependencies from imports (basic detection)
    convert_to_uv.py my_script.py --detect-imports

    # Preview conversion without creating file
    convert_to_uv.py my_script.py --dry-run

    # Specify output filename
    convert_to_uv.py my_script.py --output my_script_new.py
"""

import ast
import re
import sys
import tomllib
from pathlib import Path

# Common import name -> PyPI package name mappings
IMPORT_TO_PACKAGE = {
    'cv2': 'opencv-python',
    'PIL': 'Pillow',
    'yaml': 'PyYAML',
    'bs4': 'beautifulsoup4',
    'sklearn': 'scikit-learn',
    'dotenv': 'python-dotenv',
    'claude_agent_sdk': 'claude-agent-sdk',
}


def get_pypi_latest_version(package_name: str) -> str | None:
    """
    Query PyPI API for latest version of package.

    Returns version string like "1.2.3" or None if not found.
    """
    try:
        import httpx

        url = f"https://pypi.org/pypi/{package_name}/json"
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['info']['version']
    except Exception:
        # Network error, package not found, etc. - fail silently
        pass
    return None


def find_version_in_project(package_name: str, script_path: Path) -> str | None:
    """
    Look for version constraint in project's pyproject.toml.

    Searches up directory tree from script location.
    """
    current = script_path.parent

    # Search up to 3 levels for pyproject.toml
    for _ in range(3):
        pyproject_path = current / "pyproject.toml"
        if pyproject_path.exists():
            try:
                content = pyproject_path.read_text(encoding='utf-8')
                data = tomllib.loads(content)

                # Check [project.dependencies]
                deps = data.get('project', {}).get('dependencies', [])
                for dep in deps:
                    if isinstance(dep, str) and dep.startswith(package_name):
                        # Extract version constraint
                        # e.g., "package>=1.0.0" -> ">=1.0.0"
                        version_part = dep[len(package_name):].strip()
                        if version_part:
                            return version_part

                # Check [tool.uv.sources] or other sections if needed
                # (could expand this to check dev-dependencies, etc.)

            except Exception:
                pass

        # Move up one directory
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent

    return None


def normalize_package_name(import_name: str, use_pypi: bool = True) -> str:
    """
    Normalize import name to PyPI package name.

    Strategy:
    1. Check known mappings first (fast)
    2. Try hyphen normalization (common pattern: my_package → my-package)
    3. Validate with PyPI if enabled
    4. Fall back to original

    Returns: Normalized package name
    """
    # Known mapping takes precedence
    if import_name in IMPORT_TO_PACKAGE:
        return IMPORT_TO_PACKAGE[import_name]

    # Try hyphen normalization (most common pattern)
    if '_' in import_name:
        hyphenated = import_name.replace('_', '-')

        # Validate with PyPI if enabled
        if use_pypi and get_pypi_latest_version(hyphenated):
            return hyphenated

        # Without PyPI, trust the normalization (common convention)
        if not use_pypi:
            return hyphenated

    # Fall back to original
    return import_name


def resolve_package_version(
    import_name: str,
    script_path: Path,
    use_pypi: bool = True
) -> str:
    """
    Resolve package name and version constraint.

    Returns: "package>=X.Y.Z" format

    Strategy:
    1. Normalize import name to package name (handles underscore → hyphen)
    2. Check project's pyproject.toml for version
    3. Query PyPI for latest version
    4. Fall back to unversioned package name
    """
    # Normalize import name to package name
    package_name = normalize_package_name(import_name, use_pypi)

    # Try to find version in project
    version = find_version_in_project(package_name, script_path)
    if version:
        return f"{package_name}{version}"

    # Try PyPI if enabled
    if use_pypi:
        latest = get_pypi_latest_version(package_name)
        if latest:
            # Use minimum version constraint with latest
            return f"{package_name}>={latest}"

    # Fall back to unversioned (let uv resolve)
    return package_name


def has_pep723_metadata(content: str) -> bool:
    """Check if script already has PEP 723 metadata"""
    pattern = r'# /// script\r?\n((?:#.*(?:\r?\n|(?=\r?\n?#\s*///)))+)(?:\r?\n)?#\s*///'
    return bool(re.search(pattern, content, re.MULTILINE))


def read_requirements_file(req_path: Path) -> list[str]:
    """Read dependencies from requirements.txt"""
    if not req_path.exists():
        return []

    try:
        content = req_path.read_text(encoding='utf-8')
        deps = []
        for line in content.splitlines():
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Skip -e and --editable
            if line.startswith('-e') or line.startswith('--editable'):
                continue
            # Skip -r and --requirement
            if line.startswith('-r') or line.startswith('--requirement'):
                continue
            deps.append(line)
        return deps
    except (UnicodeDecodeError, OSError) as e:
        print(f"Warning: Could not read {req_path}: {e}", file=sys.stderr)
        return []


def detect_imports(content: str) -> list[str]:
    """
    Detect third-party imports from script (basic detection).

    Returns import names, not package names (caller should map these).
    """
    imports = set()

    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Get base module name
                    base = alias.name.split('.')[0]
                    imports.add(base)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    base = node.module.split('.')[0]
                    imports.add(base)
    except SyntaxError as e:
        print(f"Warning: Could not parse script for imports: {e}", file=sys.stderr)
        return []

    # Filter out standard library modules (basic filter)
    stdlib_modules = {
        'abc', 'argparse', 'ast', 'asyncio', 'base64', 'collections', 'contextlib',
        'copy', 'csv', 'dataclasses', 'datetime', 'decimal', 'email', 'enum', 'functools',
        'glob', 'hashlib', 'http', 'inspect', 'io', 'itertools', 'json', 'logging',
        'math', 'multiprocessing', 'operator', 'os', 'pathlib', 'pickle', 'platform',
        'pprint', 'queue', 're', 'secrets', 'shutil', 'socket', 'sqlite3', 'ssl',
        'string', 'subprocess', 'sys', 'tempfile', 'threading', 'time', 'tomllib',
        'traceback', 'typing', 'unittest', 'urllib', 'uuid', 'warnings', 'weakref',
        'xml', 'zipfile', 'zoneinfo'
    }

    third_party = [imp for imp in imports if imp not in stdlib_modules]
    return sorted(third_party)


def generate_header(
    dependencies: list[str],
    python_version: str = ">=3.11",
    quiet: bool = False
) -> str:
    """Generate PEP 723 header with shebang"""
    shebang = "#!/usr/bin/env -S uv run --script"
    if quiet:
        shebang += " --quiet"

    # Format dependencies for TOML array
    if dependencies:
        deps_str = ",\n#     ".join(f'"{dep}"' for dep in dependencies)
        deps_section = f"# dependencies = [\n#     {deps_str},\n# ]"
    else:
        deps_section = "# dependencies = []"

    header = f"""{shebang}
# /// script
# requires-python = "{python_version}"
{deps_section}
# ///
"""
    return header


def convert_script(
    script_path: Path,
    output_path: Path | None = None,
    requirements_path: Path | None = None,
    detect_imports_flag: bool = False,
    dry_run: bool = False,
    python_version: str = ">=3.11",
    quiet_mode: bool = False,
    use_pypi: bool = True
) -> bool:
    """
    Convert script to uv format.

    Returns True if successful, False otherwise.
    """
    # Read original script
    try:
        content = script_path.read_text(encoding='utf-8')
    except (FileNotFoundError, PermissionError, OSError, UnicodeDecodeError) as e:
        print(f"Error: Cannot read {script_path}: {e}", file=sys.stderr)
        return False

    # Check if already has metadata
    if has_pep723_metadata(content):
        print(f"Error: {script_path} already has PEP 723 metadata", file=sys.stderr)
        print("  Use validate_script.py to check the existing metadata", file=sys.stderr)
        return False

    # Determine dependencies
    dependencies = []

    if requirements_path:
        # Use specified requirements file
        dependencies = read_requirements_file(requirements_path)
        if dependencies:
            print(f"Found {len(dependencies)} dependencies in {requirements_path}")
    else:
        # Look for requirements.txt in same directory
        default_req = script_path.parent / "requirements.txt"
        if default_req.exists():
            dependencies = read_requirements_file(default_req)
            if dependencies:
                print(f"Found {len(dependencies)} dependencies in {default_req}")

    # Optionally detect imports
    if detect_imports_flag:
        detected = detect_imports(content)
        if detected:
            print(f"Detected imports: {', '.join(detected)}")
            print("Resolving versions...")

            # If no dependencies from requirements, use detected
            if not dependencies:
                # Use smart version resolution
                resolved = []
                for imp in detected:
                    # Normalize package name first
                    normalized_pkg = normalize_package_name(imp, use_pypi)

                    # Then resolve version
                    dep = resolve_package_version(imp, script_path, use_pypi=use_pypi)
                    resolved.append(dep)

                    # Show what was resolved
                    if imp in IMPORT_TO_PACKAGE:
                        print(f"  - Mapped '{imp}' → '{IMPORT_TO_PACKAGE[imp]}' (known mapping)")
                    elif imp != normalized_pkg:
                        print(f"  - Normalized '{imp}' → '{normalized_pkg}' (auto-detected)")

                    if '>=' in dep:
                        version = dep.split('>=')[1]
                        source = "from project" if find_version_in_project(dep.split('>=')[0], script_path) else "from PyPI"
                        print(f"  - Resolved version: {version} {source}")
                    else:
                        print(f"  - Using package: {dep} (uv will resolve version)")

                dependencies = resolved

    # Generate header
    header = generate_header(dependencies, python_version, quiet_mode)

    # Remove old shebang if present
    lines = content.split('\n')
    if lines and lines[0].startswith('#!'):
        # Skip old shebang
        content_without_shebang = '\n'.join(lines[1:])
    else:
        content_without_shebang = content

    # Combine header and content
    new_content = header + content_without_shebang

    # Determine output path
    if output_path is None:
        # Default: add _uv before extension
        stem = script_path.stem
        suffix = script_path.suffix
        output_path = script_path.parent / f"{stem}_uv{suffix}"

    # Dry run - just print
    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - Preview of converted script:")
        print("=" * 60)
        print(new_content[:500])  # Show first 500 chars
        if len(new_content) > 500:
            print(f"\n... ({len(new_content) - 500} more characters)")
        print("=" * 60)
        print(f"Would create: {output_path}")
        return True

    # Write output
    try:
        output_path.write_text(new_content, encoding='utf-8')
        print(f"✓ Created: {output_path}")

        # Make executable
        import stat
        current_permissions = output_path.stat().st_mode
        output_path.chmod(current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print("✓ Made executable")

        # Print next steps
        print("\nNext steps:")
        print(f"  1. Review dependencies in {output_path}")
        print("  2. Add version constraints if needed")
        print(f"  3. Test: {output_path}")
        print(f"  4. Validate: validate_script.py {output_path}")

        return True
    except (PermissionError, OSError) as e:
        print(f"Error: Cannot write {output_path}: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Python scripts to uv single-file format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('script', help='Python script to convert')
    parser.add_argument(
        '--requirements', '-r',
        help='Path to requirements.txt (default: look in same directory)'
    )
    parser.add_argument(
        '--detect-imports', '-d',
        action='store_true',
        help='Detect dependencies from imports (basic detection)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output filename (default: <script>_uv.py)'
    )
    parser.add_argument(
        '--python-version', '-p',
        default='>=3.11',
        help='Python version constraint (default: >=3.11)'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Add --quiet flag to shebang'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview conversion without creating file'
    )
    parser.add_argument(
        '--no-pypi',
        action='store_true',
        help='Skip PyPI queries for version resolution (faster, offline)'
    )

    args = parser.parse_args()

    script_path = Path(args.script)

    if not script_path.exists():
        print(f"Error: File not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    # Parse requirements path if provided
    req_path = Path(args.requirements) if args.requirements else None

    # Parse output path if provided
    out_path = Path(args.output) if args.output else None

    # Convert
    success = convert_script(
        script_path=script_path,
        output_path=out_path,
        requirements_path=req_path,
        detect_imports_flag=args.detect_imports,
        dry_run=args.dry_run,
        python_version=args.python_version,
        quiet_mode=args.quiet,
        use_pypi=not args.no_pypi
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
