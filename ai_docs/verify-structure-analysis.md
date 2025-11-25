# Objective Analysis: verify-structure.py

Comparison of `/scripts/verify-structure.py` against requirements in
`ai_docs/monorepo-marketplace.md`.

## Summary

The script validates plugin manifests and components correctly but has gaps in
marketplace-level validation and strict mode handling.

**Status by Area:**

- ✅ Plugin manifest schema validation
- ✅ Component placement validation
- ✅ Component content validation
- ⚠️ Marketplace schema validation (partial)
- ❌ Strict mode handling (missing)
- ❌ External source validation (missing)
- ⚠️ Marketplace entry validation (minimal)

## Detailed Analysis

### 1. Marketplace Registry Validation

**Documentation Requirements:**

Required fields:

- `name` - Marketplace identifier (kebab-case)
- `owner` - Maintainer information (object with name, email)
- `plugins` - Array of plugin entries

Optional fields:

- `metadata.description`
- `metadata.version`
- `metadata.pluginRoot`

**Script Implementation:**

Lines 596-612:

```python
marketplace_json = repo_root / ".claude-plugin" / "marketplace.json"
if not marketplace_json.exists():
    result['marketplace_errors'].append("Missing .claude-plugin/marketplace.json")

# ... JSON parse ...

if "plugins" not in marketplace_data:
    result['marketplace_errors'].append("marketplace.json missing 'plugins' array")
```

**Gaps:**

- ❌ Does not validate `name` field exists
- ❌ Does not validate `owner` field exists or structure
- ❌ Does not validate `name` follows kebab-case pattern
- ❌ Does not validate optional `metadata.*` fields
- ❌ No schema validation for marketplace.json

**Impact:** Marketplace file could be missing required fields and script would not detect it.

### 2. Plugin Entry Validation

**Documentation Requirements:**

Required fields in marketplace plugin entries:

- `name` - Plugin identifier (kebab-case)
- `source` - Location (string or object)

Optional fields:

- `description`, `version`, `author`, `homepage`, `repository`, `license`
- `keywords`, `category`, `tags`
- `strict` - Controls plugin.json requirement (default: true)
- Component overrides: `commands`, `agents`, `hooks`, `mcpServers`

**Script Implementation:**

Lines 615-621:

```python
for plugin_entry in marketplace_data["plugins"]:
    plugin_name = plugin_entry.get("name", "unknown")
    plugin_source = plugin_entry.get("source", "")

    if not plugin_source:
        result['marketplace_errors'].append(f"Plugin '{plugin_name}' missing 'source' field")
```

**Gaps:**

- ❌ Does not validate `name` follows kebab-case pattern
- ❌ Does not validate optional fields (description, version, etc.)
- ❌ Does not validate `source` format/type
- ❌ Does not read or use `strict` field
- ⚠️ Checks existence of name/source but not formats

**Impact:** Plugin entries could have invalid formats and script would not detect them.

### 3. Plugin Source Types

**Documentation Requirements:**

Three source types supported:

1. Relative path: `"./plugins/category/plugin"`
2. GitHub object: `{"source": "github", "repo": "owner/repo"}`
3. Git URL object: `{"source": "url", "url": "https://..."}`

**Script Implementation:**

Lines 624-625:

```python
plugin_dir = repo_root / plugin_source.lstrip("./")
```

**Gaps:**

- ❌ Only handles string sources (relative paths)
- ❌ Does not handle GitHub object sources
- ❌ Does not handle Git URL object sources
- ❌ Would fail or skip validation for external sources

**Impact:** External plugin sources cannot be validated. Script assumes all sources are local relative paths.

### 4. Strict Mode Handling

**Documentation Requirements:**

`strict` field in plugin entry controls plugin.json requirement:

- **Default (`strict: true`)**: Plugin must have `.claude-plugin/plugin.json`
- **Relaxed (`strict: false`)**: Plugin.json is optional; marketplace entry is complete manifest

**Script Implementation:**

Lines 528-530:

```python
if not plugin_json.exists():
    results['manifest'].append(f"{plugin_dir.name}: Missing .claude-plugin/plugin.json")
    return results
```

**Gaps:**

- ❌ Always requires plugin.json exists
- ❌ Does not check `strict` field from marketplace entry
- ❌ Does not allow plugins without plugin.json when `strict: false`

**Impact:** Plugins with `strict: false` in marketplace would fail validation even
though they are valid per documentation.

### 5. Plugin Manifest Validation

**Documentation Requirements:**

Required field:

- `name` - Plugin identifier (kebab-case)

Optional fields:

- `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`
- Component paths: `commands`, `agents`, `hooks`, `mcpServers`

**Script Implementation:**

Lines 61-141: PLUGIN_MANIFEST_SCHEMA

- Requires `name` field
- Validates kebab-case pattern for name
- Validates semantic version format
- Validates email format for author
- Validates URI formats for homepage/repository
- Validates component path types

Lines 541-542:

```python
schema_errors = validate_json_schema(data, PLUGIN_MANIFEST_SCHEMA, plugin_dir.name)
results['manifest'].extend(schema_errors)
```

**Status:** ✅ Correct and thorough

### 6. Component Placement Validation

**Documentation Requirements:**

Components must be at plugin root, not in `.claude-plugin/`:

- `skills/`
- `commands/`
- `agents/`
- `hooks/`

**Script Implementation:**

Lines 192-208:

```python
invalid_locations = ["commands", "agents", "skills", "hooks"]

for component in invalid_locations:
    if (claude_plugin_dir / component).exists():
        errors.append(
            f"{plugin_name}: {component}/ directory found in .claude-plugin/ "
            "but must be at plugin root (common mistake - see official docs)"
        )
```

**Status:** ✅ Correct

### 7. Component Content Validation

**Skills Validation:**

Lines 211-249:

- Checks skills/ directory structure
- Validates SKILL.md files exist
- Validates frontmatter (name, description)

**Status:** ✅ Correct

**Commands Validation:**

Lines 252-281:

- Checks commands/ directory
- Validates .md files
- Validates frontmatter (description)

**Status:** ✅ Correct

**Agents Validation:**

Lines 284-313:

- Checks agents/ directory
- Validates .md files
- Validates frontmatter (description, capabilities)

**Status:** ✅ Correct

**Hooks Validation:**

Lines 316-399:

- Validates hooks.json or inline hooks
- Checks valid event types (PreToolUse, PostToolUse, etc.)
- Checks valid hook types (command, validation, notification)
- Validates ${CLAUDE_PLUGIN_ROOT} usage
- Checks script files exist

**Status:** ✅ Correct

**MCP Validation:**

Lines 402-460:

- Validates .mcp.json or inline config
- Checks mcpServers structure
- Validates ${CLAUDE_PLUGIN_ROOT} usage
- Checks command field exists

**Status:** ✅ Correct

**Custom Paths Validation:**

Lines 463-496:

- Validates custom component paths start with "./"
- Checks paths exist

**Status:** ✅ Correct

### 8. README Validation

**Documentation Requirements:**

Each plugin should have README.md (per directory structure example).

**Script Implementation:**

Lines 545-546:

```python
if not (plugin_dir / "README.md").exists():
    results['manifest'].append(f"{plugin_dir.name}: Missing README.md")
```

**Status:** ✅ Correct

### 9. Repository-Specific Validation

**Script Implementation:**

Lines 583-593:

```python
required_dirs = [
    "plugins/meta",
    "plugins/infrastructure",
    "plugins/devops",
    "plugins/homelab",
    "templates/plugin-template"
]
```

**Analysis:**

- Hardcoded for lunar-claude repository structure
- Not applicable to general marketplace validation
- Would fail for marketplaces with different category names

**Status:** ⚠️ Repository-specific, not general

### 10. metadata.pluginRoot Handling

**Documentation Requirements:**

Optional field `metadata.pluginRoot` sets base path for relative plugin sources.

**Script Implementation:**

None - field is not read or used.

**Gap:**

- ❌ Does not read metadata.pluginRoot
- ❌ Does not apply base path to relative sources

**Impact:** Minor - most marketplaces use explicit paths from root.

## Critical Issues

### Issue 1: Strict Mode Not Implemented

**Severity:** High

**Description:** Script always requires plugin.json, ignoring `strict: false` setting.

**Example:**

```json
{
  "name": "simple-plugin",
  "source": "./plugins/simple",
  "description": "Complete definition here",
  "version": "1.0.0",
  "strict": false
}
```

**Expected:** Plugin valid without plugin.json
**Actual:** Script fails with "Missing .claude-plugin/plugin.json"

**Location:** Lines 528-530, 615-634

**Fix Required:**

1. Read `strict` field from marketplace plugin entry
2. Skip plugin.json validation when `strict: false`
3. Validate marketplace entry as complete manifest when strict mode off

### Issue 2: External Sources Not Handled

**Severity:** Medium

**Description:** Script only processes relative path sources, skips GitHub/Git URL sources.

**Example:**

```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repository"
  }
}
```

**Expected:** Skip validation (external) or fetch and validate
**Actual:** Script treats object as invalid path, reports error or skips

**Location:** Lines 624-625

**Fix Options:**

1. Skip validation for external sources (document limitation)
2. Fetch and validate external sources (complex)

### Issue 3: No Marketplace Schema Validation

**Severity:** Medium

**Description:** marketplace.json structure not validated against schema.

**Missing Validations:**

- `name` field required and kebab-case
- `owner` field required with name/email structure
- `plugins` array validates entry schemas
- Optional metadata fields validated

**Location:** Lines 596-612

**Fix Required:** Create marketplace schema and validate like plugin manifest.

### Issue 4: Repository-Specific Paths

**Severity:** Low

**Description:** Hardcoded category directories specific to lunar-claude.

**Location:** Lines 583-593

**Fix Options:**

1. Make configurable
2. Remove from general validation
3. Document as repository-specific check

## Validation Coverage Matrix

| Requirement | Documented | Validated | Notes |
|-------------|-----------|-----------|-------|
| marketplace.json exists | Yes | ✅ | Line 596 |
| marketplace.name required | Yes | ❌ | Not checked |
| marketplace.owner required | Yes | ❌ | Not checked |
| marketplace.plugins array | Yes | ✅ | Line 610 |
| Plugin entry name required | Yes | ⚠️ | Checked but not format |
| Plugin entry source required | Yes | ⚠️ | Checked but not format |
| Plugin entry name kebab-case | Yes | ❌ | Not validated |
| Plugin entry strict field | Yes | ❌ | Not read or used |
| Source: relative path | Yes | ✅ | Line 624 |
| Source: GitHub object | Yes | ❌ | Not handled |
| Source: Git URL object | Yes | ❌ | Not handled |
| plugin.json required (strict: true) | Yes | ✅ | Line 528 |
| plugin.json optional (strict: false) | Yes | ❌ | Not implemented |
| plugin.json schema | Yes | ✅ | Lines 61-141 |
| Plugin name kebab-case | Yes | ✅ | Line 70 |
| Plugin README.md | Yes | ✅ | Line 545 |
| Components not in .claude-plugin | Yes | ✅ | Lines 192-208 |
| Skills structure | Yes | ✅ | Lines 211-249 |
| Commands structure | Yes | ✅ | Lines 252-281 |
| Agents structure | Yes | ✅ | Lines 284-313 |
| Hooks configuration | Yes | ✅ | Lines 316-399 |
| MCP configuration | Yes | ✅ | Lines 402-460 |
| Custom paths | Yes | ✅ | Lines 463-496 |
| ${CLAUDE_PLUGIN_ROOT} usage | Yes | ✅ | Lines 384-397, 454-458 |

## Recommendations

### Priority 1: Critical

1. **Implement strict mode handling**
   - Read `strict` field from marketplace entries
   - Make plugin.json optional when `strict: false`
   - Validate marketplace entry as complete manifest in strict-false mode

2. **Add marketplace schema validation**
   - Create MARKETPLACE_SCHEMA with required fields
   - Validate name, owner, plugins structure
   - Validate kebab-case patterns

### Priority 2: Important

1. **Handle external sources gracefully**
   - Detect GitHub/Git URL source objects
   - Skip validation with informational message
   - Document limitation in script output

2. **Add plugin entry schema validation**
   - Validate each entry in marketplace plugins array
   - Check required fields and formats
   - Validate source type structures

### Priority 3: Enhancement

1. **Make category directories configurable**
   - Move hardcoded paths to configuration
   - Or remove repository-specific checks
   - Document as optional repository validation

2. **Support metadata.pluginRoot**
   - Read and apply base path to relative sources
   - Document if unsupported

## Conclusion

The script provides strong validation for plugin manifests and component structure
but has significant gaps in marketplace-level validation and strict mode handling.

**Works correctly:**

- Plugin manifest schema validation
- Component placement and content validation
- ${CLAUDE_PLUGIN_ROOT} usage verification
- README existence checks

**Needs implementation:**

- Strict mode support (critical gap)
- Marketplace schema validation
- External source handling
- Plugin entry format validation

The script is suitable for validating plugins within lunar-claude but would need
updates to validate arbitrary marketplace repositories per the official
documentation.
