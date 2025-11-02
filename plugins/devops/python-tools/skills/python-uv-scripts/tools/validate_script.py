#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Validate PEP 723 inline script metadata

Checks Python scripts for:
- Valid PEP 723 metadata block
- Required fields (requires-python, dependencies)
- TOML syntax validity
- Shebang presence and format
- Security issues

Usage:
    validate_script.py <script.py>
    validate_script.py --strict <script.py>
    validate_script.py --force <script>

Examples:
    # Basic validation
    validate_script.py my_script.py

    # Strict mode (all best practices)
    validate_script.py --strict my_script.py

    # Validate executable Python script without .py extension
    validate_script.py my_script

    # Force validation, skip extension check
    validate_script.py --force my_script

    # Validate all scripts in directory
    find . -name '*.py' -exec python validate_script.py {} \\;
"""

import ast
import os
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Validation result"""
    valid: bool
    has_metadata: bool
    has_shebang: bool
    has_docstring: bool
    warnings: list[str]
    errors: list[str]


def extract_metadata_block(content: str) -> str | None:
    """Extract PEP 723 metadata block"""
    # Match metadata block with CRLF tolerance and flexible whitespace
    # Uses lookahead to allow last metadata line without trailing newline
    pattern = r'# /// script\r?\n((?:#.*(?:\r?\n|(?=\r?\n?#\s*///)))+)(?:\r?\n)?#\s*///'
    match = re.search(pattern, content, re.MULTILINE)

    if not match:
        return None

    # Extract TOML content (remove leading # and optional whitespace from each line)
    lines = match.group(1).splitlines()
    toml_lines = []
    for line in lines:
        if line.startswith('#'):
            # Strip '#' followed by optional space or tab
            stripped = re.sub(r'^#[ \t]?', '', line)
            toml_lines.append(stripped)
        else:
            # Preserve non-comment lines (shouldn't occur with our regex but be safe)
            toml_lines.append(line)
    return '\n'.join(toml_lines)


def validate_toml_syntax(toml_content: str) -> list[str]:
    """Validate TOML syntax using structured parsing"""
    errors = []

    # Parse TOML content
    try:
        data = tomllib.loads(toml_content)
    except tomllib.TOMLDecodeError as e:
        errors.append(f"Invalid TOML syntax: {e}")
        return errors

    # Validate required fields
    if 'requires-python' not in data:
        errors.append("Missing 'requires-python' field")
    elif not isinstance(data['requires-python'], str):
        errors.append("'requires-python' must be a string")

    if 'dependencies' not in data:
        errors.append("Missing 'dependencies' field")
    else:
        dependencies = data['dependencies']
        # Dependencies should be a list/array
        if not isinstance(dependencies, list):
            errors.append("'dependencies' must be an array/list")
        else:
            # Validate each dependency item
            for idx, dep in enumerate(dependencies):
                if not isinstance(dep, str):
                    errors.append(
                        f"Dependency at index {idx} must be a string, got {type(dep).__name__}")

    return errors


def check_shebang(content: str) -> tuple[bool, list[str]]:
    """Check shebang line"""
    warnings = []
    lines = content.split('\n')

    if not lines:
        return False, ["Empty file"]

    first_line = lines[0]

    if not first_line.startswith('#!'):
        return False, []

    # Check for recommended shebangs
    recommended = [
        '#!/usr/bin/env -S uv run --script',
        '#!/usr/bin/env -S uv run --script --quiet',
    ]

    if first_line not in recommended:
        warnings.append(f"Shebang not recommended. Use: {recommended[0]}")

    return True, warnings


def check_security_issues(content: str) -> list[str]:
    """Check for common security issues"""
    warnings = []

    # Check for hardcoded secrets
    secret_patterns = [
        (r'password\s*=\s*["\']', "Possible hardcoded password"),
        (r'api[_-]?key\s*=\s*["\']', "Possible hardcoded API key"),
        (r'secret\s*=\s*["\']', "Possible hardcoded secret"),
        (r'token\s*=\s*["\']', "Possible hardcoded token"),
    ]

    for pattern, message in secret_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(f"Security: {message}")

    # Check for shell=True
    if re.search(r'shell\s*=\s*True', content):
        warnings.append(
            "Security: subprocess.run with shell=True (command injection risk)")

    # Check for eval/exec
    if re.search(r'\b(eval|exec)\s*\(', content):
        warnings.append(
            "Security: Use of eval() or exec() (code injection risk)")

    return warnings


def is_valid_python_file(script_path: Path) -> tuple[bool, str]:
    """
    Check if a non-.py file is a valid Python script.

    Returns:
        Tuple of (is_valid, reason) where reason describes why it's valid or invalid
    """
    try:
        content = script_path.read_text(encoding='utf-8')
    except (FileNotFoundError, PermissionError, OSError, UnicodeDecodeError) as e:
        return False, f"Cannot read file: {e}"

    # Check if file is executable with Python shebang
    is_executable = os.access(script_path, os.X_OK)
    lines = content.split('\n')
    has_python_shebang = False

    if lines and lines[0].startswith('#!'):
        shebang = lines[0].lower()
        has_python_shebang = 'python' in shebang

    if is_executable and has_python_shebang:
        return True, "executable with Python shebang"

    # Try to parse as Python to confirm it's valid Python code
    try:
        ast.parse(content)
        return True, "valid Python syntax"
    except SyntaxError as e:
        return False, f"not valid Python: {e}"


def validate_script(script_path: Path, strict: bool = False) -> ValidationResult:
    """Validate Python script"""
    result = ValidationResult(
        valid=True,
        has_metadata=False,
        has_shebang=False,
        has_docstring=False,
        warnings=[],
        errors=[]
    )

    # Read file
    try:
        content = script_path.read_text(encoding='utf-8')
    except (FileNotFoundError, PermissionError, OSError, UnicodeDecodeError) as e:
        result.valid = False
        result.errors.append(f"Failed to read file: {e}")
        return result

    # Check shebang
    has_shebang, shebang_warnings = check_shebang(content)
    result.has_shebang = has_shebang
    result.warnings.extend(shebang_warnings)

    if strict and not has_shebang:
        result.errors.append("Missing shebang (required in strict mode)")
        result.valid = False

    # Check for metadata block
    metadata = extract_metadata_block(content)
    result.has_metadata = metadata is not None

    if not metadata:
        result.errors.append("No PEP 723 metadata block found")
        result.valid = False
        return result

    # Validate TOML syntax
    toml_errors = validate_toml_syntax(metadata)
    result.errors.extend(toml_errors)

    if toml_errors:
        result.valid = False

    # Check for module docstring using AST parsing
    try:
        module_node = ast.parse(content)
        module_docstring = ast.get_docstring(module_node)
        result.has_docstring = module_docstring is not None
    except SyntaxError as e:
        result.has_docstring = False
        result.warnings.append(
            f"Could not parse file for docstring check: {e}")

    if strict and not result.has_docstring:
        result.warnings.append(
            "Missing module docstring (recommended in strict mode)")

    # Security checks (always warnings, never errors - these are heuristic checks)
    security_warnings = check_security_issues(content)
    result.warnings.extend(security_warnings)

    return result


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate PEP 723 script metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('script', help='Python script to validate')
    parser.add_argument('--strict', action='store_true',
                        help='Enable strict validation')
    parser.add_argument('--force', action='store_true',
                        help='Skip Python file extension check')

    args = parser.parse_args()

    script_path = Path(args.script)

    if not script_path.exists():
        print(f"Error: File not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    # Check if file is a Python file
    if script_path.suffix != '.py':
        if args.force:
            print(
                f"Warning: File lacks .py extension, but --force was specified", file=sys.stderr)
        else:
            # Check if it's a valid Python file by other means
            is_valid, reason = is_valid_python_file(script_path)
            if not is_valid:
                print(
                    f"Error: Not a Python file: {script_path}", file=sys.stderr)
                print(f"  Reason: {reason}", file=sys.stderr)
                print(f"  Hint: File must either:", file=sys.stderr)
                print(f"    - Have a .py extension, OR", file=sys.stderr)
                print(f"    - Be executable with a Python shebang, OR",
                      file=sys.stderr)
                print(f"    - Contain valid Python syntax", file=sys.stderr)
                print(f"  Use --force to skip this check", file=sys.stderr)
                sys.exit(1)
            else:
                print(
                    f"Info: File accepted as Python ({reason})", file=sys.stderr)

    # Validate
    result = validate_script(script_path, strict=args.strict)

    # Print results
    print(f"Validating: {script_path}")
    print("=" * 60)

    if result.has_shebang:
        print("✓ Has shebang")
    else:
        print("✗ Missing shebang")

    if result.has_metadata:
        print("✓ Has PEP 723 metadata")
    else:
        print("✗ Missing PEP 723 metadata")

    if result.has_docstring:
        print("✓ Has docstring")
    else:
        print("○ No docstring")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  ⚠ {warning}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  ✗ {error}")

    print("\n" + "=" * 60)

    if result.valid:
        print("Status: ✓ VALID")
        sys.exit(0)
    else:
        print("Status: ✗ INVALID")
        sys.exit(1)


if __name__ == "__main__":
    main()
