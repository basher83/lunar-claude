# Design: verify-structure.py Enhancements

**Date:** 2025-11-14
**Status:** Design Complete
**Priority:** Critical Gaps (Priority 1 from analysis)

## Overview

Enhance `scripts/verify-structure.py` to fix critical validation gaps identified in `ai_docs/verify-structure-analysis.md`. The script currently validates plugin structure well but lacks marketplace-level validation and strict mode support.

## Goals

1. Validate marketplace.json schema and structure
2. Support `strict: false` mode for plugins without plugin.json
3. Detect conflicts between marketplace entries and plugin.json
4. Add `--strict` flag for CI/CD usage
5. Remove hardcoded lunar-claude category checks

## Non-Goals

- External source fetching (GitHub/Git URLs remain skipped)
- metadata.pluginRoot support (low priority)
- General refactoring beyond necessary changes

## Architecture

### Current Flow

```bash
load marketplace.json
  → validate plugins array exists
  → for each plugin entry:
      → resolve source path
      → require plugin.json exists
      → validate plugin.json schema
      → validate components
```

### Enhanced Flow

```bash
load marketplace.json
  → validate marketplace schema (NEW)
  → validate each plugin entry schema (NEW)
  → for each plugin entry:
      → resolve source path
      → check strict mode (NEW)
      → if strict=true: require plugin.json
      → if strict=false: allow missing plugin.json
      → if both exist: detect conflicts (NEW)
      → validate components (always)
```

### Result Types

**Three-tier validation:**

1. **Errors** - Critical issues, always fail validation
2. **Warnings** - Conflicts or style issues, fail only with `--strict` flag
3. **Info** - Informational messages, never fail

**Exit Codes:**

- Normal mode: Exit 0 if no errors (warnings allowed)
- Strict mode (`--strict`): Exit 1 if any errors OR warnings

## Component Design

### 1. Marketplace Schema Validation

**New Schema: MARKETPLACE_SCHEMA**

Validates marketplace.json structure:

```python
MARKETPLACE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["name", "owner", "plugins"],
    "additionalProperties": True,
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
```

**Validates:**
- Required fields: name, owner, plugins
- Kebab-case marketplace name
- Owner has name field, email is valid format
- Plugins array has at least one entry
- Metadata fields use correct formats

**New Schema: MARKETPLACE_PLUGIN_ENTRY_SCHEMA**

Validates each plugin entry in the plugins array:

```python
MARKETPLACE_PLUGIN_ENTRY_SCHEMA = {
    "type": "object",
    "required": ["name", "source"],
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
        "author": {"type": "object"},
        "homepage": {"type": "string", "format": "uri"},
        "repository": {"type": "string", "format": "uri"},
        "license": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"},
        "tags": {"type": "array"},
        # Component overrides
        "commands": {"oneOf": [{"type": "string"}, {"type": "array"}]},
        "agents": {"oneOf": [{"type": "string"}, {"type": "array"}]},
        "hooks": {"oneOf": [{"type": "string"}, {"type": "object"}]},
        "mcpServers": {"oneOf": [{"type": "string"}, {"type": "object"}]}
    }
}
```

**Implementation:**

Add function `validate_marketplace_json()`:

```python
def validate_marketplace_json(marketplace_data: dict) -> list[str]:
    """Validate marketplace.json against schema.

    Returns list of validation errors.
    """
    errors = []

    # Validate marketplace schema
    schema_errors = validate_json_schema(
        marketplace_data,
        MARKETPLACE_SCHEMA,
        "marketplace.json"
    )
    errors.extend(schema_errors)

    # Validate each plugin entry
    for i, plugin_entry in enumerate(marketplace_data.get("plugins", [])):
        entry_errors = validate_json_schema(
            plugin_entry,
            MARKETPLACE_PLUGIN_ENTRY_SCHEMA,
            f"marketplace.json plugins[{i}]"
        )
        errors.extend(entry_errors)

    return errors
```

Call from `check_marketplace_structure()` after loading marketplace.json.

### 2. Strict Mode Support

**Detection:**

Read `strict` field from marketplace plugin entry (defaults to `true`):

```python
for plugin_entry in marketplace_data["plugins"]:
    plugin_name = plugin_entry.get("name")
    strict_mode = plugin_entry.get("strict", True)  # Default: true

    plugin_results = check_plugin_manifest(
        plugin_dir,
        marketplace_entry=plugin_entry,
        strict_mode=strict_mode
    )
```

**Modified Signature:**

```python
def check_plugin_manifest(
    plugin_dir: Path,
    marketplace_entry: dict,
    strict_mode: bool = True
) -> dict[str, list[str]]:
```

**Validation Logic:**

```python
plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

# Strict mode: plugin.json required
if strict_mode:
    if not plugin_json.exists():
        results['manifest'].append(
            f"{plugin_dir.name}: Missing .claude-plugin/plugin.json (strict mode)"
        )
        return results
    data = load_and_validate_plugin_json(plugin_json)

# Non-strict mode: plugin.json optional
else:
    if plugin_json.exists():
        data = load_and_validate_plugin_json(plugin_json)
    else:
        # Use marketplace entry as manifest
        data = marketplace_entry
        # Optional: Add info message about using marketplace entry

# Continue with component validation using data
results['skills'] = check_skills_directory(plugin_dir)
results['commands'] = check_commands_directory(plugin_dir)
results['agents'] = check_agents_directory(plugin_dir)
results['hooks'] = check_hooks_configuration(plugin_dir, data)
results['mcp'] = check_mcp_servers(plugin_dir, data)
results['paths'] = check_custom_component_paths(plugin_dir, data)
```

**Behavior:**

- `strict: true` (default): Requires plugin.json, fails if missing
- `strict: false`: Uses marketplace entry if no plugin.json, continues validation
- Component validation happens in both modes

### 3. Conflict Detection

**Purpose:**

Warn when marketplace entry and plugin.json have different values for the same field.

**Implementation:**

```python
def check_manifest_conflicts(
    plugin_name: str,
    marketplace_entry: dict,
    plugin_json_data: dict
) -> list[str]:
    """Detect conflicts between marketplace entry and plugin.json.

    Returns list of warnings for conflicting values.
    """
    warnings = []

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

**Integration:**

Call from `check_plugin_manifest()` when both sources exist:

```python
if plugin_json.exists() and marketplace_entry:
    conflict_warnings = check_manifest_conflicts(
        plugin_dir.name,
        marketplace_entry,
        data
    )
    results['warnings'] = conflict_warnings
```

**Result Structure Update:**

```python
results = {
    'manifest': [],    # Errors
    'warnings': [],    # Warnings (NEW)
    'placement': [],   # Errors
    'skills': [],      # Errors
    'commands': [],    # Errors
    'agents': [],      # Errors
    'hooks': [],       # Errors
    'mcp': [],         # Errors
    'paths': []        # Errors
}
```

### 4. Strict Mode Flag

**Command-Line Argument:**

```python
import argparse

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Claude Code marketplace structure and plugins"
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (useful for CI/CD)'
    )
    args = parser.parse_args()

    result = check_marketplace_structure()
    exit_code = calculate_exit_code(result, strict=args.strict)
    return exit_code
```

**Exit Code Calculation:**

```python
def calculate_exit_code(result: dict, strict: bool = False) -> int:
    """Calculate exit code based on errors and warnings.

    Args:
        result: Validation results
        strict: If True, warnings cause failure

    Returns:
        0 if passed, 1 if failed
    """
    total_errors = 0
    total_warnings = 0

    # Count marketplace errors
    total_errors += len(result['marketplace_errors'])

    # Count plugin errors and warnings
    for plugin_result in result['plugin_results'].values():
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

**Output Display:**

```python
# After displaying errors, show warnings
if total_warnings > 0:
    style = "yellow" if not strict else "red"
    label = "Warnings" if not strict else "Warnings (treated as errors)"
    console.print(f"\n[bold {style}]{label} ({total_warnings}):[/bold {style}]\n")

    for plugin_name, plugin_result in result['plugin_results'].items():
        if plugin_result.get('warnings'):
            for warning in plugin_result['warnings']:
                console.print(f"  [{style}]• {warning}[/{style}]")

    if strict:
        console.print("\n  [red](--strict mode active)[/red]\n")

# Final summary
if total_errors > 0 or (strict and total_warnings > 0):
    message = f"✗ Validation failed with {total_errors} error(s)"
    if total_warnings > 0:
        message += f" and {total_warnings} warning(s)"
    console.print(Panel.fit(f"[bold red]{message}[/bold red]", border_style="red"))
    return 1
```

### 5. Remove Hardcoded Category Checks

**Code to Remove:**

Lines 583-593:

```python
# DELETE THIS:
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

**Rationale:**

- Script should validate what's published in marketplace.json, not repo organization
- Makes script work with any marketplace structure
- Source path validation already happens in plugin loop

**Existing Validation:**

Plugin source validation remains (lines 624-630):

```python
plugin_dir = repo_root / plugin_source.lstrip("./")

if not plugin_dir.exists():
    result['marketplace_errors'].append(
        f"Plugin '{plugin_name}' source directory not found: {plugin_source}"
    )
    continue
```

This validates each declared plugin source exists, which is sufficient.

## Implementation Checklist

### Phase 1: Schema Validation

- [ ] Add MARKETPLACE_SCHEMA constant
- [ ] Add MARKETPLACE_PLUGIN_ENTRY_SCHEMA constant
- [ ] Implement validate_marketplace_json() function
- [ ] Call validate_marketplace_json() in check_marketplace_structure()
- [ ] Test with valid and invalid marketplace.json files

### Phase 2: Strict Mode

- [ ] Update check_plugin_manifest() signature to accept marketplace_entry and strict_mode
- [ ] Implement strict mode logic in check_plugin_manifest()
- [ ] Update check_marketplace_structure() to pass strict mode
- [ ] Test with strict: true and strict: false plugins
- [ ] Test component validation works in both modes

### Phase 3: Conflict Detection

- [ ] Add 'warnings' to results dict structure
- [ ] Implement check_manifest_conflicts() function
- [ ] Call check_manifest_conflicts() from check_plugin_manifest()
- [ ] Test with matching and conflicting values

### Phase 4: CLI Flag

- [ ] Add argparse import
- [ ] Add --strict argument to main()
- [ ] Implement calculate_exit_code() function
- [ ] Update display logic to show warnings
- [ ] Test normal mode (warnings pass)
- [ ] Test strict mode (warnings fail)

### Phase 5: Cleanup

- [ ] Remove hardcoded category directory checks (lines 583-593)
- [ ] Update docstring to reflect new behavior
- [ ] Test with different marketplace structures

### Phase 6: Verification

- [ ] Run script on lunar-claude marketplace (should pass)
- [ ] Test all error conditions
- [ ] Test all warning conditions
- [ ] Verify exit codes in both modes
- [ ] Update CLAUDE.md if needed

## Testing Scenarios

### Marketplace Schema

1. Missing `name` field → Error
2. Invalid kebab-case name → Error
3. Missing `owner.name` → Error
4. Invalid `owner.email` format → Error
5. Missing `plugins` array → Error
6. Empty `plugins` array → Error
7. Invalid `metadata.version` format → Error

### Plugin Entry Schema

1. Missing `name` field → Error
2. Missing `source` field → Error
3. Invalid kebab-case plugin name → Error
4. Invalid version format → Error
5. Invalid URL formats → Error

### Strict Mode

1. Plugin with strict: true and no plugin.json → Error
2. Plugin with strict: false and no plugin.json → Pass
3. Plugin with strict: false, no plugin.json, has skills/ → Pass
4. Plugin with strict: false and plugin.json present → Validate both

### Conflict Detection

1. Matching values → No warning
2. Different versions → Warning
3. Different descriptions → Warning
4. Field in marketplace only → No warning
5. Field in plugin.json only → No warning

### CLI Flag

1. Normal mode with warnings → Exit 0
2. Normal mode with errors → Exit 1
3. Strict mode with warnings → Exit 1
4. Strict mode with errors → Exit 1

## Success Criteria

1. ✅ Marketplace.json structure fully validated
2. ✅ Plugins work with strict: false mode
3. ✅ Conflicts detected and reported as warnings
4. ✅ --strict flag controls warning behavior
5. ✅ No hardcoded repository-specific checks
6. ✅ All existing validations continue working
7. ✅ Script validates lunar-claude successfully
8. ✅ Exit codes work correctly for CI/CD

## Migration Notes

**Breaking Changes:**
- None (new features are additive)

**New Requirements:**
- argparse (standard library, already available)

**Backward Compatibility:**
- Existing behavior preserved for strict: true (default)
- New warnings don't break existing workflows (unless --strict used)
- Category directory removal doesn't affect plugin validation

## Future Enhancements (Out of Scope)

- External source fetching and validation
- metadata.pluginRoot support
- Additional output formats (JSON, JUnit XML)
- Plugin dependency validation
- Performance optimization for large marketplaces
