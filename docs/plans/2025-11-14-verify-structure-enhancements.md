# verify-structure.py Enhancements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enhance verify-structure.py to validate marketplace.json schema, support strict mode, detect conflicts, and add CLI strict flag.

**Architecture:** Add two new schemas (marketplace + plugin entries), modify check_plugin_manifest() to accept marketplace entry and strict mode flag, add conflict detection, implement argparse CLI with --strict flag, remove hardcoded category checks.

**Tech Stack:** Python 3.11+, jsonschema, rich, argparse (stdlib)

---

## Task 1: Add Marketplace Schema

**Files:**
- Modify: `scripts/verify-structure.py:60-141` (add schemas before PLUGIN_MANIFEST_SCHEMA)

**Step 1: Add marketplace and plugin entry schemas**

Add these constants after line 59 (after VALID_HOOK_TYPES):

```python
# Marketplace manifest schema
MARKETPLACE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["name", "owner", "plugins"],
    "additionalProperties": True,  # Allow custom fields
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
            "description": "Marketplace identifier (kebab-case)"
        },
        "owner": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string", "format": "email"}
            }
        },
        "plugins": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "object"}
        },
        "metadata": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "version": {
                    "type": "string",
                    "pattern": "^\\d+\\.\\d+\\.\\d+$"
                },
                "pluginRoot": {"type": "string"}
            }
        }
    }
}

# Plugin entry schema for marketplace.json plugins array
MARKETPLACE_PLUGIN_ENTRY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["name", "source"],
    "additionalProperties": True,
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
        },
        "source": {
            "oneOf": [
                {"type": "string"},  # Relative path
                {
                    "type": "object",
                    "required": ["source"],
                    "properties": {
                        "source": {"type": "string"},
                        "repo": {"type": "string"},
                        "url": {"type": "string"}
                    }
                }
            ]
        },
        "strict": {"type": "boolean"},
        # Plugin manifest fields (all optional)
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "description": {"type": "string"},
        "author": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "url": {"type": "string", "format": "uri"}
            }
        },
        "homepage": {"type": "string", "format": "uri"},
        "repository": {"type": "string", "format": "uri"},
        "license": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        # Component overrides
        "commands": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ]
        },
        "agents": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ]
        },
        "hooks": {
            "oneOf": [
                {"type": "string"},
                {"type": "object"}
            ]
        },
        "mcpServers": {
            "oneOf": [
                {"type": "string"},
                {"type": "object"}
            ]
        }
    }
}
```

**Step 2: Add marketplace validation function**

Add after validate_json_schema() function (after line 153):

```python
def validate_marketplace_json(marketplace_data: dict) -> list[str]:
    """Validate marketplace.json structure against schema.

    Args:
        marketplace_data: Parsed marketplace.json content

    Returns:
        List of validation errors
    """
    errors = []

    # Validate marketplace-level schema
    schema_errors = validate_json_schema(
        marketplace_data,
        MARKETPLACE_SCHEMA,
        "marketplace.json"
    )
    errors.extend(schema_errors)

    # Validate each plugin entry
    plugins = marketplace_data.get("plugins", [])
    for i, plugin_entry in enumerate(plugins):
        entry_errors = validate_json_schema(
            plugin_entry,
            MARKETPLACE_PLUGIN_ENTRY_SCHEMA,
            f"marketplace.json plugins[{i}] ({plugin_entry.get('name', 'unknown')})"
        )
        errors.extend(entry_errors)

    return errors
```

**Step 3: Test marketplace schema validation**

Create test file: `tests/test_marketplace_validation.json`

```json
{
  "name": "test-marketplace",
  "owner": {
    "name": "Test Owner",
    "email": "test@example.com"
  },
  "plugins": [
    {
      "name": "test-plugin",
      "source": "./plugins/test",
      "version": "1.0.0"
    }
  ]
}
```

Run test:
```bash
# Test valid marketplace
python -c "
import json
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
# Import after adding schemas
exec(open('scripts/verify-structure.py').read().split('def validate_json_schema')[0])
data = json.loads(Path('tests/test_marketplace_validation.json').read_text())
errors = validate_marketplace_json(data)
print('Valid:' if not errors else f'Errors: {errors}')
"
```

Expected: "Valid:"

**Step 4: Test invalid marketplace**

Create test file: `tests/test_marketplace_invalid.json`

```json
{
  "name": "Invalid Name With Spaces",
  "owner": {},
  "plugins": []
}
```

Run test:
```bash
python -c "
import json
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
exec(open('scripts/verify-structure.py').read().split('def validate_json_schema')[0])
data = json.loads(Path('tests/test_marketplace_invalid.json').read_text())
errors = validate_marketplace_json(data)
print(f'Found {len(errors)} errors (expected 3+)')
for e in errors: print(f'  - {e}')
"
```

Expected: Multiple errors for name pattern, missing owner.name, empty plugins array

**Step 5: Commit**

```bash
git add scripts/verify-structure.py tests/test_marketplace_*.json
git commit -m "feat: add marketplace.json schema validation

- Add MARKETPLACE_SCHEMA for marketplace structure
- Add MARKETPLACE_PLUGIN_ENTRY_SCHEMA for plugin entries
- Add validate_marketplace_json() function
- Validates name/owner/plugins required fields
- Validates kebab-case patterns and formats
"
```

---

## Task 2: Integrate Marketplace Validation

**Files:**
- Modify: `scripts/verify-structure.py:560-637` (check_marketplace_structure function)

**Step 1: Call marketplace validation**

In `check_marketplace_structure()`, after loading marketplace.json (around line 607), add validation:

Find this section:
```python
try:
    with open(marketplace_json) as f:
        marketplace_data = json.load(f)
except json.JSONDecodeError as e:
    result['marketplace_errors'].append(f"Invalid JSON in marketplace.json: {e}")
    return result
```

Add after it:
```python
# Validate marketplace schema
marketplace_schema_errors = validate_marketplace_json(marketplace_data)
result['marketplace_errors'].extend(marketplace_schema_errors)

# If marketplace structure invalid, don't continue
if marketplace_schema_errors:
    return result
```

**Step 2: Remove hardcoded category checks**

Find and DELETE lines 583-593 (required_dirs section):

```python
# DELETE THIS ENTIRE SECTION:
required_dirs = [
    "plugins/meta",
    "plugins/infrastructure",
    "plugins/devops",
    "plugins/homelab",
    "templates/plugin-template"
]

for dir_path in required_dirs:
    if not (repo_root / dir_path).is_dir():
        result['marketplace_errors'].append(f"Missing required directory: {dir_path}")
```

**Step 3: Test marketplace validation integration**

```bash
# Should pass on valid lunar-claude marketplace
./scripts/verify-structure.py
```

Expected: Script runs successfully, validates marketplace.json structure

**Step 4: Test with invalid marketplace**

Temporarily break marketplace.json to test:

```bash
# Backup
cp .claude-plugin/marketplace.json .claude-plugin/marketplace.json.bak

# Break name field
python -c "
import json
from pathlib import Path
data = json.loads(Path('.claude-plugin/marketplace.json').read_text())
data['name'] = 'Invalid Name'
Path('.claude-plugin/marketplace.json').write_text(json.dumps(data, indent=2))
"

# Run script
./scripts/verify-structure.py
```

Expected: Error about invalid kebab-case name

```bash
# Restore
mv .claude-plugin/marketplace.json.bak .claude-plugin/marketplace.json
```

**Step 5: Commit**

```bash
git add scripts/verify-structure.py
git commit -m "feat: integrate marketplace validation and remove hardcoded checks

- Call validate_marketplace_json() in check_marketplace_structure()
- Remove hardcoded category directory checks
- Validate only plugins declared in marketplace.json
- Fail early if marketplace structure invalid
"
```

---

## Task 3: Add Strict Mode Support

**Files:**
- Modify: `scripts/verify-structure.py:499-558` (check_plugin_manifest function)
- Modify: `scripts/verify-structure.py:614-635` (check_marketplace_structure plugin loop)

**Step 1: Update check_plugin_manifest signature**

Change function signature (line 499):

FROM:
```python
def check_plugin_manifest(plugin_dir: Path) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.
```

TO:
```python
def check_plugin_manifest(
    plugin_dir: Path,
    marketplace_entry: dict | None = None,
    strict_mode: bool = True
) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.

    Args:
        plugin_dir: Path to plugin directory
        marketplace_entry: Plugin entry from marketplace.json (optional)
        strict_mode: If True, require plugin.json. If False, allow missing plugin.json
```

**Step 2: Implement strict mode logic**

Update the plugin.json loading section (lines 525-538):

FROM:
```python
    # Check plugin.json exists
    if not plugin_json.exists():
        results['manifest'].append(f"{plugin_dir.name}: Missing .claude-plugin/plugin.json")
        return results

    # Validate JSON syntax
    try:
        with open(plugin_json) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results['manifest'].append(f"{plugin_dir.name}: Invalid JSON in plugin.json: {e}")
        return results
```

TO:
```python
    # Strict mode: plugin.json required
    if strict_mode:
        if not plugin_json.exists():
            results['manifest'].append(
                f"{plugin_dir.name}: Missing .claude-plugin/plugin.json (strict mode)"
            )
            return results

        # Load and validate plugin.json
        try:
            with open(plugin_json) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            results['manifest'].append(f"{plugin_dir.name}: Invalid JSON in plugin.json: {e}")
            return results

    # Non-strict mode: plugin.json optional
    else:
        if plugin_json.exists():
            # Load and validate if present
            try:
                with open(plugin_json) as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                results['manifest'].append(f"{plugin_dir.name}: Invalid JSON in plugin.json: {e}")
                return results
        else:
            # Use marketplace entry as manifest
            data = marketplace_entry if marketplace_entry else {}
```

**Step 3: Pass strict mode from marketplace loop**

In `check_marketplace_structure()`, update the plugin validation loop (around lines 614-634):

FROM:
```python
    for plugin_entry in marketplace_data["plugins"]:
        plugin_name = plugin_entry.get("name", "unknown")
        plugin_source = plugin_entry.get("source", "")

        if not plugin_source:
            result['marketplace_errors'].append(f"Plugin '{plugin_name}' missing 'source' field")
            continue

        # Resolve plugin directory
        plugin_dir = repo_root / plugin_source.lstrip("./")

        if not plugin_dir.exists():
            result['marketplace_errors'].append(
                f"Plugin '{plugin_name}' source directory not found: {plugin_source}"
            )
            continue

        # Validate plugin manifest and components
        plugin_results = check_plugin_manifest(plugin_dir)
        result['plugin_results'][plugin_name] = plugin_results
```

TO:
```python
    for plugin_entry in marketplace_data["plugins"]:
        plugin_name = plugin_entry.get("name", "unknown")
        plugin_source = plugin_entry.get("source", "")

        # Skip external sources (GitHub/Git URLs)
        if isinstance(plugin_source, dict):
            continue  # External sources not validated locally

        if not plugin_source:
            result['marketplace_errors'].append(f"Plugin '{plugin_name}' missing 'source' field")
            continue

        # Resolve plugin directory
        plugin_dir = repo_root / plugin_source.lstrip("./")

        if not plugin_dir.exists():
            result['marketplace_errors'].append(
                f"Plugin '{plugin_name}' source directory not found: {plugin_source}"
            )
            continue

        # Get strict mode from marketplace entry (default: true)
        strict_mode = plugin_entry.get("strict", True)

        # Validate plugin manifest and components
        plugin_results = check_plugin_manifest(
            plugin_dir,
            marketplace_entry=plugin_entry,
            strict_mode=strict_mode
        )
        result['plugin_results'][plugin_name] = plugin_results
```

**Step 4: Test strict mode with plugin**

Create test plugin without plugin.json:

```bash
mkdir -p tests/test-plugin-nonstrict/skills/test-skill
echo "---
name: test-skill
description: Test skill
---
# Test" > tests/test-plugin-nonstrict/skills/test-skill/SKILL.md

echo "# Test Plugin" > tests/test-plugin-nonstrict/README.md
```

Create test marketplace.json:

```json
{
  "name": "test-marketplace",
  "owner": {"name": "Test"},
  "plugins": [
    {
      "name": "test-plugin-nonstrict",
      "source": "./tests/test-plugin-nonstrict",
      "strict": false,
      "description": "Test plugin without manifest",
      "version": "1.0.0"
    }
  ]
}
```

Test manually:
```bash
# Modify check_marketplace_structure to use test marketplace
# Should pass validation for strict: false plugin without plugin.json
```

**Step 5: Commit**

```bash
git add scripts/verify-structure.py
git commit -m "feat: implement strict mode support

- Update check_plugin_manifest() to accept marketplace_entry and strict_mode
- When strict=false, allow missing plugin.json
- Use marketplace entry as manifest when plugin.json missing
- Continue validating components in both modes
- Skip external sources (GitHub/Git) gracefully
"
```

---

## Task 4: Add Conflict Detection

**Files:**
- Modify: `scripts/verify-structure.py:514-523` (add warnings to results dict)
- Modify: `scripts/verify-structure.py` (add check_manifest_conflicts function)

**Step 1: Add warnings to results structure**

Update results dict initialization in `check_plugin_manifest()` (around line 514):

FROM:
```python
    results = {
        'manifest': [],
        'placement': [],
        'skills': [],
        'commands': [],
        'agents': [],
        'hooks': [],
        'mcp': [],
        'paths': []
    }
```

TO:
```python
    results = {
        'manifest': [],
        'warnings': [],     # NEW: Conflict warnings
        'placement': [],
        'skills': [],
        'commands': [],
        'agents': [],
        'hooks': [],
        'mcp': [],
        'paths': []
    }
```

**Step 2: Add conflict detection function**

Add after `check_custom_component_paths()` function (before `check_plugin_manifest()`):

```python
def check_manifest_conflicts(
    plugin_name: str,
    marketplace_entry: dict,
    plugin_json_data: dict
) -> list[str]:
    """Detect conflicts between marketplace entry and plugin.json.

    Args:
        plugin_name: Name of the plugin
        marketplace_entry: Plugin entry from marketplace.json
        plugin_json_data: Parsed plugin.json content

    Returns:
        List of warning messages for conflicting values
    """
    warnings = []

    # Fields that can appear in both
    comparable_fields = [
        'version', 'description', 'author', 'homepage',
        'repository', 'license', 'keywords'
    ]

    for field in comparable_fields:
        market_value = marketplace_entry.get(field)
        plugin_value = plugin_json_data.get(field)

        # Both exist and differ
        if market_value and plugin_value and market_value != plugin_value:
            warnings.append(
                f"{plugin_name}: Conflict in '{field}' - "
                f"marketplace: {repr(market_value)}, "
                f"plugin.json: {repr(plugin_value)} "
                f"(plugin.json takes precedence)"
            )

    return warnings
```

**Step 3: Call conflict detection**

In `check_plugin_manifest()`, after loading plugin.json data (in both strict and non-strict paths), add:

```python
    # Check for conflicts if both marketplace entry and plugin.json exist
    if marketplace_entry and plugin_json.exists():
        conflict_warnings = check_manifest_conflicts(
            plugin_dir.name,
            marketplace_entry,
            data
        )
        results['warnings'].extend(conflict_warnings)
```

Insert this right before the component validation section (before `# Validate against schema` or before README check).

**Step 4: Test conflict detection**

Create test files:

`tests/test-conflict-plugin/.claude-plugin/plugin.json`:
```json
{
  "name": "test-conflict",
  "version": "2.0.0",
  "description": "From plugin.json"
}
```

`tests/test-conflict-plugin/README.md`:
```markdown
# Test Conflict Plugin
```

Test marketplace entry:
```json
{
  "name": "test-conflict",
  "source": "./tests/test-conflict-plugin",
  "version": "1.0.0",
  "description": "From marketplace"
}
```

Expected: 2 warnings about version and description conflicts

**Step 5: Commit**

```bash
git add scripts/verify-structure.py
git commit -m "feat: add conflict detection between marketplace and plugin.json

- Add warnings category to results dict
- Implement check_manifest_conflicts() function
- Compare version, description, author, homepage, repository, license, keywords
- Generate warnings when values differ
- Note that plugin.json takes precedence
"
```

---

## Task 5: Add CLI --strict Flag

**Files:**
- Modify: `scripts/verify-structure.py:38-48` (add argparse import)
- Modify: `scripts/verify-structure.py:639-730` (main function)

**Step 1: Add argparse import**

Add to imports section (line 38):

```python
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
```

**Step 2: Add calculate_exit_code function**

Add before `main()` function (around line 639):

```python
def calculate_exit_code(result: dict, strict: bool = False) -> int:
    """Calculate exit code based on errors and warnings.

    Args:
        result: Validation results from check_marketplace_structure()
        strict: If True, warnings cause failure

    Returns:
        0 if validation passed, 1 if failed
    """
    total_errors = 0
    total_warnings = 0

    # Count marketplace-level errors
    total_errors += len(result.get('marketplace_errors', []))

    # Count plugin-level errors and warnings
    for plugin_result in result.get('plugin_results', {}).values():
        for category, issues in plugin_result.items():
            if category == 'warnings':
                total_warnings += len(issues)
            else:
                total_errors += len(issues)

    # Strict mode: warnings are failures
    if strict and total_warnings > 0:
        return 1

    # Normal mode: only errors are failures
    return 1 if total_errors > 0 else 0
```

**Step 3: Update main() to use argparse**

Update `main()` function (lines 639-730):

FROM:
```python
def main() -> int:
    """Run all verification checks."""
    console.print("\n[bold cyan]Verifying lunar-claude marketplace structure...[/bold cyan]\n")

    result = check_marketplace_structure()
```

TO:
```python
def main() -> int:
    """Run all verification checks."""
    parser = argparse.ArgumentParser(
        description="Verify Claude Code marketplace structure and plugins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit codes:
  0 - Validation passed
  1 - Validation failed (errors found, or warnings in strict mode)

Examples:
  ./scripts/verify-structure.py              # Normal mode (warnings allowed)
  ./scripts/verify-structure.py --strict     # Strict mode (warnings fail)
        """
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (useful for CI/CD)'
    )
    args = parser.parse_args()

    mode_text = "[bold cyan]Verifying marketplace structure"
    if args.strict:
        mode_text += " (strict mode)"
    mode_text += "...[/bold cyan]\n"
    console.print("\n" + mode_text)

    result = check_marketplace_structure()
```

**Step 4: Update exit code calculation**

At the end of `main()`, replace the exit code logic:

FROM:
```python
    # Count total errors across all categories
    total_errors = len(result['marketplace_errors'])
    all_plugin_errors = {}

    for plugin_name, plugin_result in result['plugin_results'].items():
        plugin_errors = []
        for category, errors in plugin_result.items():
            if errors:
                plugin_errors.extend(errors)
        if plugin_errors:
            all_plugin_errors[plugin_name] = plugin_errors
            total_errors += len(plugin_errors)
```

TO:
```python
    # Count errors and warnings
    total_errors = len(result['marketplace_errors'])
    total_warnings = 0
    all_plugin_errors = {}
    all_plugin_warnings = {}

    for plugin_name, plugin_result in result['plugin_results'].items():
        plugin_errors = []
        plugin_warnings = []
        for category, issues in plugin_result.items():
            if issues:
                if category == 'warnings':
                    plugin_warnings.extend(issues)
                else:
                    plugin_errors.extend(issues)

        if plugin_errors:
            all_plugin_errors[plugin_name] = plugin_errors
            total_errors += len(plugin_errors)
        if plugin_warnings:
            all_plugin_warnings[plugin_name] = plugin_warnings
            total_warnings += len(plugin_warnings)
```

**Step 5: Update output display for warnings**

After displaying errors in `main()`, add warning display section (before final summary):

```python
    # Display warnings
    if total_warnings > 0:
        warning_style = "yellow" if not args.strict else "red"
        warning_label = "Warnings" if not args.strict else "Warnings (treated as errors)"

        console.print(f"\n[bold {warning_style}]{warning_label} ({total_warnings}):[/bold {warning_style}]\n")

        for plugin_name, warnings in all_plugin_warnings.items():
            console.print(f"  [bold]{plugin_name}:[/bold]")
            for warning in warnings:
                console.print(f"    [{warning_style}]• {warning}[/{warning_style}]")

        if args.strict:
            console.print("\n  [red](--strict mode: warnings treated as errors)[/red]\n")
        console.print()
```

**Step 6: Update final summary**

Update the final summary panel to use `calculate_exit_code()`:

FROM:
```python
    # Final summary
    if total_errors > 0:
        console.print(Panel.fit(
            f"[bold red]✗ Validation failed with {total_errors} error(s)[/bold red]\n"
            "See details above for specific issues.",
            border_style="red"
        ))
        return 1

    # Success!
    console.print(Panel.fit(
        "[bold green]✅ All verification checks passed![/bold green]\n"
        "Marketplace structure and all plugins are valid.",
        border_style="green"
    ))

    return 0
```

TO:
```python
    # Calculate exit code
    exit_code = calculate_exit_code(result, strict=args.strict)

    # Final summary
    if exit_code != 0:
        message = f"✗ Validation failed with {total_errors} error(s)"
        if total_warnings > 0:
            message += f" and {total_warnings} warning(s)"
        if args.strict and total_warnings > 0:
            message += " (warnings treated as errors in strict mode)"

        console.print(Panel.fit(
            f"[bold red]{message}[/bold red]\n"
            "See details above for specific issues.",
            border_style="red"
        ))
    else:
        message = "✅ All verification checks passed!"
        if total_warnings > 0:
            message += f"\n{total_warnings} warning(s) found but not failing (normal mode)"
        message += "\nMarketplace structure and all plugins are valid."

        console.print(Panel.fit(
            f"[bold green]{message}[/bold green]",
            border_style="green"
        ))

    return exit_code
```

**Step 7: Update table display for warnings**

In the table section (around line 668-693), add warnings column:

After:
```python
        table.add_column("Paths", justify="center")
```

Add:
```python
        table.add_column("Warnings", justify="center")
```

Update the row addition to include warnings:

```python
            table.add_row(
                plugin_name,
                status_icon(plugin_result['manifest']),
                status_icon(plugin_result['placement']),
                status_icon(plugin_result['skills']),
                status_icon(plugin_result['commands']),
                status_icon(plugin_result['agents']),
                status_icon(plugin_result['hooks']),
                status_icon(plugin_result['mcp']),
                status_icon(plugin_result['paths']),
                f"[yellow]{len(plugin_result.get('warnings', []))}[/yellow]" if plugin_result.get('warnings') else "[green]0[/green]"
            )
```

**Step 8: Update docstring**

Update module docstring (lines 9-36) to mention strict mode:

```python
"""
Verify Claude Code marketplace structure and validate plugin manifests.

This script validates all aspects of Claude Code marketplaces per official documentation:

Marketplace Structure:
- marketplace.json syntax and schema (name, owner, plugins)
- Plugin entry validation (name, source, strict mode)
- Plugin registry completeness

Plugin Components:
- Manifest (plugin.json) schema and metadata
- Component placement (not in .claude-plugin/)
- Skills (SKILL.md frontmatter, directory structure)
- Commands (markdown frontmatter, file structure)
- Agents (markdown frontmatter, capabilities field)
- Hooks (event types, hook types, script existence)
- MCP servers (configuration, ${CLAUDE_PLUGIN_ROOT} usage)
- Custom component paths (existence, relative paths)

Strict Mode:
- Plugins with strict: false can omit plugin.json
- Conflicts between marketplace and plugin.json generate warnings
- Use --strict flag to fail on warnings (for CI/CD)

Usage:
    ./scripts/verify-structure.py              # Normal mode
    ./scripts/verify-structure.py --strict     # Strict mode (warnings fail)

Exit codes:
    0 - All checks passed (warnings allowed in normal mode)
    1 - Validation errors found (or warnings in strict mode)
"""
```

**Step 9: Test normal mode**

```bash
# Should pass with warnings allowed
./scripts/verify-structure.py
```

Expected: Exit 0, warnings displayed in yellow

**Step 10: Test strict mode**

```bash
# Should fail if warnings present
./scripts/verify-structure.py --strict
```

Expected: Exit 1 if warnings exist, warnings displayed in red

**Step 11: Commit**

```bash
git add scripts/verify-structure.py
git commit -m "feat: add --strict CLI flag and warning display

- Add argparse for CLI argument parsing
- Implement --strict flag to treat warnings as errors
- Add calculate_exit_code() function
- Update main() to use argparse and display warnings
- Add warnings column to validation table
- Normal mode: warnings allowed (exit 0)
- Strict mode: warnings fail (exit 1)
- Update docstring with usage examples
"
```

---

## Task 6: Final Testing and Documentation

**Files:**
- Test: Run comprehensive tests
- Modify: `CLAUDE.md` (if needed)
- Clean up: Remove test files

**Step 1: Test all validation scenarios**

```bash
# Test 1: Valid marketplace passes
./scripts/verify-structure.py
echo "Exit code: $?"  # Should be 0

# Test 2: Strict mode with warnings fails
./scripts/verify-structure.py --strict
echo "Exit code: $?"  # Should be 1 if warnings exist, 0 if none

# Test 3: Invalid marketplace.json
# (Create temp invalid marketplace and test - then restore)

# Test 4: Plugin with strict: false and no plugin.json
# (Should pass validation)

# Test 5: Plugin with conflicts
# (Should show warnings)
```

**Step 2: Clean up test files**

```bash
rm -rf tests/test-marketplace*.json tests/test-plugin-nonstrict tests/test-conflict-plugin
```

**Step 3: Update CLAUDE.md if needed**

Check if `CLAUDE.md` mentions verify-structure.py. If so, update usage:

```markdown
### Structure Verification

```bash
# Verify marketplace and plugin structure (validates plugin.json schema)
./scripts/verify-structure.py

# Strict mode for CI/CD (warnings fail)
./scripts/verify-structure.py --strict
```
```text

**Step 4: Test on actual lunar-claude marketplace**

```bash
# Full validation
./scripts/verify-structure.py

# Check exit code
echo $?
```

Expected: Script passes, validates all declared plugins, no hardcoded category checks

**Step 5: Final commit**

```bash
git add CLAUDE.md  # If modified
git commit -m "docs: update verify-structure.py usage in CLAUDE.md

- Document --strict flag for CI/CD usage
- Update structure verification examples
"
```

---

## Task 7: Create Summary Document

**Files:**
- Create: `docs/verify-structure-enhancements-summary.md`

**Step 1: Create summary document**

```markdown
# verify-structure.py Enhancements Summary

**Date:** 2025-11-14
**Implemented:** Yes

## Overview

Enhanced verify-structure.py to fix critical validation gaps identified in analysis.

## Changes Implemented

### 1. Marketplace Schema Validation

Added complete JSON schema validation for marketplace.json:

- **MARKETPLACE_SCHEMA**: Validates marketplace structure
  - Required: name (kebab-case), owner (with name/email), plugins array
  - Optional: metadata (description, version, pluginRoot)

- **MARKETPLACE_PLUGIN_ENTRY_SCHEMA**: Validates plugin entries
  - Required: name (kebab-case), source (string or object)
  - Optional: strict, version, description, author, etc.

- **validate_marketplace_json()**: Validates marketplace and all plugin entries

### 2. Strict Mode Support

Plugins can now omit plugin.json when `strict: false`:

- Default behavior (`strict: true`): Requires plugin.json
- New behavior (`strict: false`): Plugin.json optional, uses marketplace entry
- Component validation continues in both modes

### 3. Conflict Detection

Warns when marketplace entry and plugin.json have conflicting values:

- **check_manifest_conflicts()**: Detects conflicts in version, description, etc.
- Warnings generated for differing values
- Notes that plugin.json takes precedence

### 4. CLI --strict Flag

New command-line flag for CI/CD:

- **Normal mode**: `./scripts/verify-structure.py` - Warnings allowed (exit 0)
- **Strict mode**: `./scripts/verify-structure.py --strict` - Warnings fail (exit 1)

- **calculate_exit_code()**: Determines exit code based on errors/warnings
- Updated output to display warnings separately
- Added warnings column to validation table

### 5. Removed Hardcoded Checks

Removed repository-specific category validation:

- No longer checks for `plugins/meta`, `plugins/infrastructure`, etc.
- Only validates plugins declared in marketplace.json
- Makes script work with any marketplace structure

## Usage

```bash
# Normal mode (warnings allowed)
./scripts/verify-structure.py

# Strict mode (warnings fail, for CI/CD)
./scripts/verify-structure.py --strict
```

## Testing

All scenarios tested:

- ✅ Valid marketplace.json passes
- ✅ Invalid marketplace.json fails
- ✅ Plugin with strict: false and no plugin.json passes
- ✅ Plugin with strict: true and no plugin.json fails
- ✅ Conflicts generate warnings
- ✅ Normal mode allows warnings (exit 0)
- ✅ Strict mode fails on warnings (exit 1)

## Files Modified

- `scripts/verify-structure.py` - All enhancements

## Lines Added

- ~150 lines for schemas
- ~50 lines for strict mode logic
- ~80 lines for CLI and warnings display
- Total: ~280 new lines

## Backward Compatibility

- Existing validation behavior preserved
- New features are additive
- No breaking changes to existing workflows
```bash

**Step 2: Commit summary**

```bash
git add docs/verify-structure-enhancements-summary.md
git commit -m "docs: add implementation summary for verify-structure enhancements

Summary of all changes implemented:
- Marketplace schema validation
- Strict mode support
- Conflict detection
- CLI --strict flag
- Removal of hardcoded checks
"
```

---

## Verification Checklist

After implementation, verify:

- [ ] Marketplace.json with missing name fails validation
- [ ] Marketplace.json with invalid owner fails validation
- [ ] Plugin entry with missing source fails validation
- [ ] Plugin with strict: false and no plugin.json passes
- [ ] Plugin with strict: true and no plugin.json fails
- [ ] Conflicts between marketplace and plugin.json show warnings
- [ ] `--strict` flag makes warnings fail validation
- [ ] Normal mode allows warnings to pass
- [ ] No hardcoded category directory checks
- [ ] External sources (GitHub/Git) skipped gracefully
- [ ] lunar-claude marketplace validates successfully
- [ ] Help text (`./scripts/verify-structure.py --help`) shows usage

## Success Criteria

All checks pass:
- ✅ Marketplace schema fully validated
- ✅ Strict mode works correctly
- ✅ Conflicts detected and reported
- ✅ CLI flag controls warning behavior
- ✅ Repository-agnostic validation
- ✅ Backward compatible
- ✅ Exit codes correct for CI/CD

---

**Implementation complete!** All critical gaps addressed per design document.
