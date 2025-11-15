# Fix PR #15 Critical Issues Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix critical error handling and add test coverage for verify-structure.py PR #15

**Architecture:** TDD approach to add comprehensive test suite, fix all bare exception catches with specific exception types, correct documentation issues, and improve edge case handling.

**Tech Stack:** Python 3.11+, pytest, jsonschema, rich

**Reference:** docs/reviews/pr/ (comprehensive review from 5 specialized agents)

---

## Task 1: Fix Bare Exception Catches in File Reading

**Files:**
- Modify: `scripts/verify-structure.py:315-317`
- Test: `tests/test_verify_structure.py` (create)

**Priority:** CRITICAL - Hides KeyboardInterrupt and programming errors

### Step 1: Write failing test for specific exceptions

Create: `tests/test_verify_structure.py`

```python
"""Tests for verify-structure.py error handling."""

import json
import tempfile
from pathlib import Path
import pytest

class TestErrorHandling:
    """Test error handling specificity."""

    def test_file_read_handles_permission_error(self, tmp_path):
        """Should catch and report permission errors specifically."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import validate_markdown_frontmatter

        # Create file with no read permissions
        test_file = tmp_path / "test.md"
        test_file.write_text("---\nname: test\n---")
        test_file.chmod(0o000)  # No permissions

        try:
            errors = validate_markdown_frontmatter(test_file, ["name"], "test-plugin")

            # Should get a clear permission error message
            assert len(errors) > 0
            assert "permission" in errors[0].lower() or "cannot read" in errors[0].lower()
        finally:
            test_file.chmod(0o644)  # Restore permissions for cleanup

    def test_file_read_handles_unicode_error(self, tmp_path):
        """Should catch and report encoding errors specifically."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import validate_markdown_frontmatter

        # Create file with invalid UTF-8
        test_file = tmp_path / "test.md"
        test_file.write_bytes(b"\xff\xfe\x00\x00")  # Invalid UTF-8

        errors = validate_markdown_frontmatter(test_file, ["name"], "test-plugin")

        assert len(errors) > 0
        assert "encoding" in errors[0].lower() or "utf-8" in errors[0].lower()
```

### Step 2: Run test to verify it fails

Run: `pytest tests/test_verify_structure.py::TestErrorHandling::test_file_read_handles_permission_error -v`

Expected: FAIL (currently catches all exceptions generically)

### Step 3: Fix exception handling in verify-structure.py

Modify: `scripts/verify-structure.py:315-317`

Change from:
```python
try:
    content = file_path.read_text()
except Exception as e:
    errors.append(f"{plugin_name}/{rel_path}: Error reading file: {e}")
    return errors
```

To:
```python
try:
    content = file_path.read_text(encoding='utf-8')
except PermissionError as e:
    errors.append(
        f"{plugin_name}/{rel_path}: Permission denied reading file\n"
        f"  Check file permissions (current: {file_path.stat().st_mode:o})"
    )
    return errors
except UnicodeDecodeError as e:
    errors.append(
        f"{plugin_name}/{rel_path}: File is not valid UTF-8\n"
        f"  Ensure file is text, not binary. Error at byte {e.start}: {e.reason}"
    )
    return errors
except OSError as e:
    errors.append(f"{plugin_name}/{rel_path}: Cannot read file: {e}")
    return errors
```

### Step 4: Run test to verify it passes

Run: `pytest tests/test_verify_structure.py::TestErrorHandling -v`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: use specific exception types for file reading

Replaced bare 'except Exception' with specific exception types:
- PermissionError: Shows clear permission denied message
- UnicodeDecodeError: Indicates encoding issue with file
- OSError: Catches other file I/O errors

Allows KeyboardInterrupt to propagate for clean Ctrl+C.

Resolves PR #15 critical issue #1 (line 315)"
```

---

## Task 2: Fix JSON Loading Exception Handling (Hooks)

**Files:**
- Modify: `scripts/verify-structure.py:487-492, 494-499`
- Modify: `tests/test_verify_structure.py`

**Priority:** CRITICAL - Misleading error messages

### Step 1: Write test for JSON error specificity

```python
class TestJSONErrorHandling:
    """Test JSON loading error specificity."""

    def test_hooks_json_invalid_syntax(self, tmp_path):
        """Should report JSON syntax errors clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir()

        # Create invalid JSON
        hooks_file = hooks_dir / "hooks.json"
        hooks_file.write_text('{"invalid json')

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_hooks_configuration

        errors = check_hooks_configuration(plugin_dir, {"hooks": "hooks/hooks.json"})

        assert len(errors) > 0
        assert "json" in errors[0].lower()
        assert "line" in errors[0].lower() or "column" in errors[0].lower()

    def test_hooks_file_not_found(self, tmp_path):
        """Should report missing file clearly."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_hooks_configuration

        errors = check_hooks_configuration(plugin_dir, {"hooks": "nonexistent.json"})

        assert len(errors) > 0
        assert "not found" in errors[0].lower() or "does not exist" in errors[0].lower()
```

### Step 2: Run test to verify it fails

Run: `pytest tests/test_verify_structure.py::TestJSONErrorHandling -v`

Expected: FAIL

### Step 3: Fix JSON exception handling

Modify: `scripts/verify-structure.py:487-492`

```python
try:
    with open(custom_hooks_path, encoding='utf-8') as f:
        hooks_config = json.load(f)
except FileNotFoundError:
    errors.append(f"{plugin_name}: Hooks file not found: {inline_hooks}")
    return errors
except PermissionError:
    errors.append(f"{plugin_name}: Permission denied reading hooks file: {inline_hooks}")
    return errors
except json.JSONDecodeError as e:
    errors.append(
        f"{plugin_name}: Invalid JSON in hooks file {inline_hooks}\n"
        f"  Line {e.lineno}, column {e.colno}: {e.msg}"
    )
    return errors
except UnicodeDecodeError as e:
    errors.append(
        f"{plugin_name}: Hooks file is not valid UTF-8: {inline_hooks}\n"
        f"  Ensure file is text, not binary"
    )
    return errors
except OSError as e:
    errors.append(f"{plugin_name}: Cannot read hooks file: {e}")
    return errors
```

Apply same pattern to line 494-499.

### Step 4: Run test to verify it passes

Run: `pytest tests/test_verify_structure.py::TestJSONErrorHandling -v`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: improve JSON error handling specificity

Replaced generic exception handling with specific types for hooks:
- FileNotFoundError: Clear 'file not found' message
- JSONDecodeError: Shows line/column of syntax error
- PermissionError: Indicates permission issue
- UnicodeDecodeError: Shows encoding problem

Resolves PR #15 critical issues #2, #3 (lines 487, 494)"
```

---

## Task 3: Fix Remaining JSON Exception Handlers

**Files:**
- Modify: `scripts/verify-structure.py:573-585, 817-822, 734-739, 749-754`
- Modify: `tests/test_verify_structure.py`

### Step 1: Write tests for MCP and manifest loading

```python
class TestMCPAndManifestErrors:
    """Test MCP config and manifest error handling."""

    def test_mcp_json_errors(self, tmp_path):
        """Should handle MCP JSON errors specifically."""
        # Similar to hooks tests
        pass

    def test_plugin_manifest_permission_denied(self, tmp_path):
        """Should catch permission errors in strict mode."""
        # Create plugin.json with no read permission
        # Verify clear error message
        pass

    def test_marketplace_json_unicode_error(self, tmp_path):
        """Should catch encoding errors in marketplace.json."""
        # Create binary file as marketplace.json
        # Verify encoding error message
        pass
```

### Step 2: Run tests to verify failure

Run: `pytest tests/test_verify_structure.py::TestMCPAndManifestErrors -v`

Expected: FAIL

### Step 3: Apply same exception handling pattern

Apply the specific exception handling pattern from Task 2 to:
- Lines 573-585 (MCP config loading)
- Lines 817-822 (marketplace.json loading)
- Lines 734-739 (plugin.json strict mode)
- Lines 749-754 (plugin.json non-strict mode)

### Step 4: Run tests to verify passes

Run: `pytest tests/test_verify_structure.py::TestMCPAndManifestErrors -v`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: apply specific exception handling to all JSON loading

Applied specific exception handling pattern to:
- MCP config loading (lines 573-585)
- Marketplace.json loading (lines 817-822)
- Plugin.json loading strict mode (lines 734-739)
- Plugin.json loading non-strict mode (lines 749-754)

All now catch FileNotFoundError, PermissionError, JSONDecodeError,
UnicodeDecodeError separately for clear error messages.

Resolves PR #15 critical issues #4, #5, #6, #7, #8"
```

---

## Task 4: Add Schema Validation Error Handling

**Files:**
- Modify: `scripts/verify-structure.py:260-269`
- Modify: `tests/test_verify_structure.py`

### Step 1: Write test for schema validation errors

```python
class TestSchemaValidation:
    """Test JSON schema validation error handling."""

    def test_invalid_schema_definition(self):
        """Should catch schema errors gracefully."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import validate_json_schema

        # Create invalid schema
        invalid_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "invalid_type"}  # Invalid type
            }
        }

        data = {"name": "test"}

        errors = validate_json_schema(data, invalid_schema, "test-context")

        # Should get internal error message, not crash
        assert len(errors) > 0
        assert "internal error" in errors[0].lower() or "schema" in errors[0].lower()
```

### Step 2: Run test to verify failure

Run: `pytest tests/test_verify_structure.py::TestSchemaValidation -v`

Expected: FAIL (crashes with unhandled SchemaError)

### Step 3: Add error handling to validate_json_schema

Modify: `scripts/verify-structure.py:260-269`

```python
def validate_json_schema(data: dict[str, Any], schema: dict[str, Any], context: str) -> list[str]:
    """Validate JSON data against JSON Schema Draft 7 specification.

    Args:
        data: Dictionary to validate
        schema: JSON Schema dict (Draft 7 format)
        context: Human-readable context for error messages

    Returns:
        List of formatted error messages with context and field paths
    """
    from jsonschema.exceptions import SchemaError

    errors = []

    try:
        validator = Draft7Validator(schema)
    except SchemaError as e:
        errors.append(
            f"{context}: INTERNAL ERROR - Invalid schema definition: {e}\n"
            f"  This is a bug in the verification script, please report it"
        )
        return errors

    try:
        for error in validator.iter_errors(data):
            path = " -> ".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"{context}: {path}: {error.message}")
    except RecursionError:
        errors.append(f"{context}: Data structure too deeply nested (recursion limit)")
    except Exception as e:
        errors.append(
            f"{context}: Unexpected error during validation: {e.__class__.__name__}: {e}\n"
            f"  Please report this as a bug"
        )

    return errors
```

### Step 4: Run test to verify it passes

Run: `pytest tests/test_verify_structure.py::TestSchemaValidation -v`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: add error handling to schema validation

Catches SchemaError for malformed schemas, RecursionError for deep
nesting, and other unexpected errors to prevent crashes.

Resolves PR #15 critical issue #9"
```

---

## Task 5: Add Minimum Test Suite for Core Functionality

**Files:**
- Modify: `tests/test_verify_structure.py`

### Step 1: Add marketplace schema tests

```python
class TestMarketplaceValidation:
    """Test marketplace.json schema validation."""

    def test_valid_marketplace_passes(self, tmp_path):
        """Valid marketplace.json should pass validation."""
        marketplace = {
            "name": "test-marketplace",
            "owner": {"name": "Test Owner", "email": "test@example.com"},
            "plugins": [{
                "name": "test-plugin",
                "source": "plugins/test-plugin",
                "version": "1.0.0"
            }]
        }

        marketplace_file = tmp_path / ".claude-plugin" / "marketplace.json"
        marketplace_file.parent.mkdir(parents=True)
        marketplace_file.write_text(json.dumps(marketplace))

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import validate_marketplace_json

        result = validate_marketplace_json(tmp_path)
        assert result['valid'] is True
        assert len(result['errors']) == 0

    def test_invalid_marketplace_name_pattern(self, tmp_path):
        """Invalid name pattern should fail."""
        marketplace = {
            "name": "Invalid_Name",  # Underscores not allowed
            "owner": {"name": "Test"},
            "plugins": [{"name": "test", "source": "./test"}]
        }

        marketplace_file = tmp_path / ".claude-plugin" / "marketplace.json"
        marketplace_file.parent.mkdir(parents=True)
        marketplace_file.write_text(json.dumps(marketplace))

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import validate_marketplace_json

        result = validate_marketplace_json(tmp_path)
        assert result['valid'] is False
        assert any("pattern" in str(e).lower() for e in result['errors'])
```

### Step 2: Add strict mode tests

```python
class TestStrictMode:
    """Test strict mode functionality."""

    def test_strict_true_requires_plugin_json(self, tmp_path):
        """Strict mode should require plugin.json."""
        marketplace = {
            "name": "test-marketplace",
            "owner": {"name": "Test"},
            "plugins": [{
                "name": "test-plugin",
                "source": "plugins/test-plugin",
                "strict": True  # Explicit strict
            }]
        }

        # Create plugin dir WITHOUT plugin.json
        plugin_dir = tmp_path / "plugins" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "README.md").write_text("# Test")

        # Setup and run check
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_plugin_manifest

        result = check_plugin_manifest(plugin_dir, marketplace["plugins"][0], strict_mode=True)

        assert len(result['errors']) > 0
        assert any("plugin.json" in str(e).lower() for e in result['errors'])

    def test_strict_false_allows_missing_plugin_json(self, tmp_path):
        """Non-strict mode should allow missing plugin.json."""
        marketplace_entry = {
            "name": "test-plugin",
            "source": "plugins/test-plugin",
            "strict": False,
            "version": "1.0.0",
            "description": "Test plugin"
        }

        plugin_dir = tmp_path / "plugins" / "test-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "README.md").write_text("# Test")

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_plugin_manifest

        result = check_plugin_manifest(plugin_dir, marketplace_entry, strict_mode=False)

        # Should have no manifest errors
        assert len(result['errors']) == 0 or not any("plugin.json" in str(e).lower() for e in result['errors'])
```

### Step 3: Add exit code tests

```python
class TestExitCodes:
    """Test exit code calculation."""

    def test_exit_0_no_errors_no_warnings(self):
        """No errors or warnings should exit 0."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import calculate_exit_code

        result = {'errors': [], 'warnings': []}
        exit_code = calculate_exit_code(result, strict=False)
        assert exit_code == 0

    def test_exit_0_warnings_normal_mode(self):
        """Warnings in normal mode should exit 0."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import calculate_exit_code

        result = {'errors': [], 'warnings': ['warning1']}
        exit_code = calculate_exit_code(result, strict=False)
        assert exit_code == 0

    def test_exit_1_warnings_strict_mode(self):
        """Warnings in strict mode should exit 1."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import calculate_exit_code

        result = {'errors': [], 'warnings': ['warning1']}
        exit_code = calculate_exit_code(result, strict=True)
        assert exit_code == 1

    def test_exit_1_with_errors(self):
        """Errors should always exit 1."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import calculate_exit_code

        result = {'errors': ['error1'], 'warnings': []}

        assert calculate_exit_code(result, strict=False) == 1
        assert calculate_exit_code(result, strict=True) == 1
```

### Step 4: Add conflict detection tests

```python
class TestConflictDetection:
    """Test conflict detection between marketplace and plugin.json."""

    def test_version_conflict_generates_warning(self):
        """Differing versions should generate warning."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_manifest_conflicts

        marketplace_entry = {"name": "test", "version": "1.0.0"}
        plugin_json = {"name": "test", "version": "2.0.0"}

        warnings = check_manifest_conflicts("test-plugin", marketplace_entry, plugin_json)

        assert len(warnings) > 0
        assert any("version" in w.lower() for w in warnings)
        assert any("1.0.0" in w for w in warnings)
        assert any("2.0.0" in w for w in warnings)

    def test_no_warning_when_values_match(self):
        """Matching values should not generate warnings."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_manifest_conflicts

        entry = {"name": "test", "version": "1.0.0"}

        warnings = check_manifest_conflicts("test-plugin", entry, entry)

        assert len(warnings) == 0
```

### Step 5: Run all tests

Run: `pytest tests/test_verify_structure.py -v`

Expected: ALL PASS

### Step 6: Commit

```bash
git add tests/test_verify_structure.py
git commit -m "test: add comprehensive test suite for core functionality

Added 11 critical tests covering:
- Marketplace schema validation (2 tests)
- Strict mode behavior (2 tests)
- Exit code calculation (4 tests)
- Conflict detection (2 tests)
- Integration test (1 test)

Resolves PR #15 critical issue: Zero test coverage

Test coverage now covers all critical paths."
```

---

## Task 6: Fix Keywords Array Comparison

**Files:**
- Modify: `scripts/verify-structure.py:675`
- Modify: `tests/test_verify_structure.py`

### Step 1: Write failing test

```python
class TestConflictDetectionEdgeCases:
    """Test conflict detection edge cases."""

    def test_keywords_order_insensitive(self):
        """Keywords with different order should not conflict."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_manifest_conflicts

        marketplace = {"keywords": ["terraform", "ansible", "infrastructure"]}
        plugin_json = {"keywords": ["ansible", "infrastructure", "terraform"]}

        warnings = check_manifest_conflicts("test", marketplace, plugin_json)

        # Should have NO keyword warnings
        assert not any("keyword" in w.lower() for w in warnings)
```

### Step 2: Run test to verify it fails

Run: `pytest tests/test_verify_structure.py::TestConflictDetectionEdgeCases::test_keywords_order_insensitive -v`

Expected: FAIL (currently order-sensitive)

### Step 3: Fix keywords comparison

Modify: `scripts/verify-structure.py:675`

```python
# Both exist and differ
if market_value is not None and plugin_value is not None:
    # Special handling for keywords (order-insensitive)
    if field == 'keywords' and isinstance(market_value, list) and isinstance(plugin_value, list):
        if set(market_value) != set(plugin_value):
            warnings.append(
                f"{plugin_name}: Conflict in '{field}' - "
                f"marketplace: {repr(sorted(market_value))}, "
                f"plugin.json: {repr(sorted(plugin_value))} "
                f"(plugin.json takes precedence)"
            )
    elif market_value != plugin_value:
        warnings.append(
            f"{plugin_name}: Conflict in '{field}' - "
            f"marketplace: {repr(market_value)}, "
            f"plugin.json: {repr(plugin_value)} "
            f"(plugin.json takes precedence)"
        )
```

### Step 4: Run test to verify it passes

Run: `pytest tests/test_verify_structure.py::TestConflictDetectionEdgeCases::test_keywords_order_insensitive -v`

Expected: PASS

### Step 5: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: make keywords comparison order-insensitive

Uses set comparison for keywords arrays to avoid false positives
when keywords are same but in different order.

Also changed to 'is not None' check for better empty value handling.

Resolves PR #15 important issues #4, #5"
```

---

## Task 7: Add Path Traversal Validation

**Files:**
- Modify: `scripts/verify-structure.py:483, 569, 626, 640, 846-847`
- Modify: `tests/test_verify_structure.py`

### Step 1: Write security test

```python
class TestSecurityValidation:
    """Test security validations."""

    def test_rejects_path_traversal_in_hooks(self, tmp_path):
        """Should reject path traversal attempts in hooks path."""
        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()

        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from verify_structure import check_hooks_configuration

        # Attempt path traversal
        plugin_data = {"hooks": "../../etc/passwd"}

        errors = check_hooks_configuration(plugin_dir, plugin_data)

        assert len(errors) > 0
        assert any("escape" in e.lower() or "outside" in e.lower() for e in errors)

    def test_rejects_path_traversal_in_marketplace_source(self, tmp_path):
        """Should reject plugin source paths that escape repo."""
        # Test marketplace validation rejects ../../../ paths
        pass
```

### Step 2: Run test to verify failure

Run: `pytest tests/test_verify_structure.py::TestSecurityValidation -v`

Expected: FAIL (currently allows path traversal)

### Step 3: Add path validation helper

Add to `scripts/verify-structure.py` after imports:

```python
def validate_plugin_path(base_dir: Path, relative_path: str, context: str) -> tuple[Path | None, str | None]:
    """Validate a plugin-relative path stays within base directory.

    Args:
        base_dir: Base directory (plugin or repo root)
        relative_path: Relative path string from config
        context: Context for error messages

    Returns:
        Tuple of (resolved_path, error_message). If error, path is None.
    """
    try:
        full_path = base_dir / relative_path.lstrip("./")
        resolved = full_path.resolve()
        base_resolved = base_dir.resolve()

        # Check if resolved path is under base directory
        resolved.relative_to(base_resolved)
        return full_path, None
    except ValueError:
        return None, f"{context}: Path escapes base directory: {relative_path}"
    except Exception as e:
        return None, f"{context}: Invalid path: {e}"
```

### Step 4: Apply validation to all path resolutions

Update lines 483, 569, 626, 640, 846 to use `validate_plugin_path()`:

```python
# Line 483 example:
custom_hooks_path, error = validate_plugin_path(plugin_dir, inline_hooks, f"{plugin_name}/hooks")
if error:
    errors.append(error)
    return errors
```

### Step 5: Run test to verify it passes

Run: `pytest tests/test_verify_structure.py::TestSecurityValidation -v`

Expected: PASS

### Step 6: Commit

```bash
git add tests/test_verify_structure.py scripts/verify-structure.py
git commit -m "fix: validate paths to prevent directory traversal

Added validate_plugin_path() helper that ensures all custom paths
stay within their base directory. Applied to:
- Hook paths (line 483)
- MCP paths (line 569)
- Custom component paths (lines 626, 640)
- Plugin source paths (line 846)

Resolves PR #15 important issue #6 (security)"
```

---

## Task 8: Fix Documentation Issues

**Files:**
- Modify: `scripts/verify-structure.py:176, 689-697, 29-32`

### Step 1: Fix file reference typo

Modify: `scripts/verify-structure.py:176`

```python
# Plugin manifest schema based on Claude Code plugin reference documentation
# See: https://docs.anthropic.com/claude/docs/plugin-reference
```

### Step 2: Rename confusing parameter

Modify: `scripts/verify-structure.py:689, 696-697`

Change from:
```python
def check_plugin_manifest(
    plugin_dir: Path,
    marketplace_entry: dict | None = None,
    strict_mode: bool = True
) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.

    Args:
        strict_mode: If False, allow missing plugin.json
```

To:
```python
def check_plugin_manifest(
    plugin_dir: Path,
    marketplace_entry: dict | None = None,
    require_manifest: bool = True
) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.

    Args:
        plugin_dir: Path to plugin directory
        marketplace_entry: Plugin entry from marketplace.json (optional)
        require_manifest: If True, plugin.json is required. If False, plugin.json
                         is optional and marketplace entry data is used as fallback.
                         This value comes from the 'strict' field in marketplace.json.
```

Update all uses of `strict_mode` parameter to `require_manifest` throughout function.

### Step 3: Clarify module docstring

Modify: `scripts/verify-structure.py:29-32`

```python
Plugin Manifest Requirements:
- By default, all plugins must have .claude-plugin/plugin.json
- Plugins with "strict: false" in marketplace.json can omit plugin.json
- When plugin.json is missing, marketplace entry data is used for validation

CLI Options:
- Normal mode: Warnings are displayed but don't cause failure (exit 0)
- Use --strict flag to treat warnings as errors (exit 1, for CI/CD)
```

### Step 4: Commit

```bash
git add scripts/verify-structure.py
git commit -m "docs: fix file reference and clarify strict mode terminology

Fixed:
- Corrected typo: 'referance' -> 'reference'
- Updated file path to correct documentation URL
- Renamed 'strict_mode' parameter to 'require_manifest' for clarity
- Clarified distinction between:
  - marketplace.json 'strict' field (controls manifest requirement)
  - CLI --strict flag (controls warning treatment)

Resolves PR #15 critical issue #3 (documentation)"
```

---

## Task 9: Fix Minor Issues

**Files:**
- Modify: `scripts/verify-structure.py:519, 521`

### Step 1: Fix unused loop variables

Modify: `scripts/verify-structure.py:519, 521`

```python
# Line 519
for _i, hook_entry in enumerate(hook_list):

# Line 521
for _j, hook in enumerate(hook_entry["hooks"]):
```

### Step 2: Run formatter

Run: `ruff format scripts/verify-structure.py`

### Step 3: Commit

```bash
git add scripts/verify-structure.py
git commit -m "style: fix linting and formatting issues

- Renamed unused loop variables to _i, _j
- Applied ruff formatter for consistent style

Resolves PR #15 minor issues #7, #8"
```

---

## Task 10: Final Verification

**Files:**
- N/A (verification only)

### Step 1: Run full test suite

Run: `pytest tests/test_verify_structure.py -v --cov=scripts`

Expected: All tests PASS, >80% coverage on new code

### Step 2: Run linting

Run: `ruff check scripts/verify-structure.py`

Expected: No errors

### Step 3: Test actual script

Run: `./scripts/verify-structure.py`

Expected: Validates successfully

### Step 4: Test strict mode

Run: `./scripts/verify-structure.py --strict`

Expected: Appropriate exit code based on warnings

### Step 5: Final commit

```bash
git add -A
git commit -m "test: verify all fixes work end-to-end

All critical issues resolved:
- 9 bare exception catches fixed with specific types
- 11 comprehensive tests added
- Documentation issues corrected
- Edge cases fixed (keywords, empty strings)
- Security: Path traversal validation added
- Style: Linting clean, formatted

PR #15 ready for merge."
```

---

## Summary

**Total Tasks:** 10
**Estimated Time:** 3-4 hours
**Test Coverage:** 11+ tests minimum
**TDD Approach:** Write test first, verify failure, fix, verify pass, commit

**Priority Order:**
1. ✅ Critical: Fix all bare exception catches (Tasks 1-4)
2. ✅ Critical: Add minimum test suite (Task 5)
3. ✅ Important: Fix edge cases (Task 6)
4. ✅ Important: Security validation (Task 7)
5. ✅ Critical: Fix documentation (Task 8)
6. ✅ Minor: Style issues (Task 9)
7. ✅ Quality: Final verification (Task 10)

**Deferred Issues:**
- Schema documentation examples (nice to have)
- Error message standardization (low priority)
- Type annotations improvements (already good)

**Testing Strategy:**
- Unit tests for each exception type
- Integration tests for end-to-end validation
- Security tests for path traversal
- Edge case tests for conflict detection
- CLI behavior tests

**Commit Strategy:**
- Commit after each task completion
- Test + fix together in same commit
- Clear messages referencing review issues
- Final verification commit

**After This Plan:**
PR #15 will have:
- ✅ Zero bare exception catches
- ✅ Comprehensive test coverage
- ✅ Clear, accurate documentation
- ✅ Security validations
- ✅ Clean linting
- ✅ Production-ready code
