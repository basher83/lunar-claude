#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema>=4.20.0",
#   "pyyaml>=6.0.0",
#   "rich>=13.0.0",
# ]
# ///
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

Plugin Manifest Requirements:
- By default, all plugins must have .claude-plugin/plugin.json
- Plugins with "strict: false" in marketplace.json can omit plugin.json
- When plugin.json is missing, marketplace entry data is used for validation

CLI Options:
- Normal mode: Warnings are displayed but don't cause failure (exit 0)
- Use --strict flag to treat warnings as errors (exit 1, for CI/CD)

Usage:
    ./scripts/verify-structure.py              # Normal mode
    ./scripts/verify-structure.py --strict     # Strict mode (warnings fail)

Exit codes:
    0 - All checks passed (warnings allowed in normal mode)
    1 - Validation errors found (or warnings in strict mode)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def validate_plugin_path(
    base_dir: Path, relative_path: str, context: str
) -> tuple[Path | None, str | None]:
    """Validate a plugin-relative path stays within base directory.

    Args:
        base_dir: Base directory (plugin or repo root)
        relative_path: Relative path string from config
        context: Context for error messages

    Returns:
        Tuple of (resolved_path, error_message). If error, path is None.
    """
    try:
        import os.path

        # Resolve base directory
        base_resolved = base_dir.resolve()

        # Use os.path.join and normpath to properly handle .. in paths
        # Path's / operator normalizes too early and doesn't catch traversal
        full_path_str = os.path.join(str(base_resolved), relative_path)
        normalized_str = os.path.normpath(full_path_str)
        path_resolved = Path(normalized_str)

        # Check if normalized path is under base directory
        try:
            path_resolved.relative_to(base_resolved)
        except ValueError:
            return None, f"{context}: Path escapes base directory: {relative_path}"
        else:
            # Path is safe, return the path object for existence checks
            # Use the original Path construction for the return value
            full_path = base_dir / relative_path.lstrip("./")
            return full_path, None
    except OSError as e:
        return None, f"{context}: Invalid path: {e}"


# Valid hook event types from official docs
VALID_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Notification",
    "Stop",
    "SubagentStop",
    "SessionStart",
    "SessionEnd",
    "PreCompact",
}

# Valid hook types
VALID_HOOK_TYPES = {"command", "validation", "notification"}

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
            "description": "Marketplace identifier (kebab-case)",
        },
        "owner": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string", "format": "email"},
            },
        },
        "plugins": {"type": "array", "minItems": 1, "items": {"type": "object"}},
        "metadata": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
                "pluginRoot": {"type": "string"},
            },
        },
    },
}

# Plugin entry schema for marketplace.json plugins array
MARKETPLACE_PLUGIN_ENTRY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["name", "source"],
    "additionalProperties": True,
    "properties": {
        "name": {"type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"},
        "source": {
            "oneOf": [
                {"type": "string"},  # Relative path
                {
                    "type": "object",
                    "required": ["source"],
                    "properties": {
                        "source": {"type": "string"},
                        "repo": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
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
                "url": {"type": "string", "format": "uri"},
            },
        },
        "homepage": {"type": "string", "format": "uri"},
        "repository": {"type": "string", "format": "uri"},
        "license": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        # Component overrides
        "commands": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
        "agents": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
        "hooks": {"oneOf": [{"type": "string"}, {"type": "object"}]},
        "mcpServers": {"oneOf": [{"type": "string"}, {"type": "object"}]},
    },
}

# Plugin manifest schema based on Claude Code plugin reference documentation
# See: https://docs.anthropic.com/claude/docs/plugin-reference
PLUGIN_MANIFEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["name"],
    "additionalProperties": False,
    "properties": {
        # Required
        "name": {
            "type": "string",
            "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
            "description": "Unique identifier (kebab-case, no spaces)",
        },
        # Optional metadata
        "version": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$",
            "description": "Semantic version",
        },
        "description": {"type": "string", "description": "Brief explanation of plugin purpose"},
        "author": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "url": {"type": "string", "format": "uri"},
            },
            "required": ["name"],
        },
        "homepage": {"type": "string", "format": "uri", "description": "Documentation URL"},
        "repository": {"type": "string", "format": "uri", "description": "Source code URL"},
        "license": {"type": "string", "description": "License identifier"},
        "keywords": {"type": "array", "items": {"type": "string"}, "description": "Discovery tags"},
        # Component paths
        "commands": {
            "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}],
            "description": "Additional command files/directories",
        },
        "agents": {
            "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}],
            "description": "Additional agent files",
        },
        "hooks": {
            "oneOf": [{"type": "string"}, {"type": "object"}],
            "description": "Hook config path or inline config",
        },
        "mcpServers": {
            "oneOf": [{"type": "string"}, {"type": "object"}],
            "description": "MCP config path or inline config",
        },
    },
}


def validate_json_schema(data: dict[str, Any], schema: dict[str, Any], context: str) -> list[str]:
    """Validate JSON data against JSON Schema Draft 7 specification.

    Args:
        data: Dictionary to validate
        schema: JSON Schema dict (Draft 7 format)
        context: Human-readable context for error messages

    Returns:
        List of formatted error messages with context and field paths
    """
    from jsonschema.exceptions import SchemaError, UnknownType
    from referencing.exceptions import Unresolvable

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
    except Unresolvable as e:
        errors.append(f"{context}: Schema reference resolution failed: {e}")
    except UnknownType as e:
        errors.append(f"{context}: Unknown type in schema: {e}")
    except (ValueError, TypeError) as e:
        errors.append(f"{context}: Invalid data structure: {e}")

    return errors


def validate_marketplace_json(marketplace_data: dict) -> list[str]:
    """Validate marketplace.json structure against schema.

    Args:
        marketplace_data: Parsed marketplace.json content

    Returns:
        List of validation errors
    """
    errors = []

    # Validate marketplace-level schema
    schema_errors = validate_json_schema(marketplace_data, MARKETPLACE_SCHEMA, "marketplace.json")
    errors.extend(schema_errors)

    # Validate each plugin entry
    plugins = marketplace_data.get("plugins", [])
    for i, plugin_entry in enumerate(plugins):
        entry_errors = validate_json_schema(
            plugin_entry,
            MARKETPLACE_PLUGIN_ENTRY_SCHEMA,
            f"marketplace.json plugins[{i}] ({plugin_entry.get('name', 'unknown')})",
        )
        errors.extend(entry_errors)

    return errors


def validate_markdown_frontmatter(
    file_path: Path, required_fields: list[str], plugin_name: str
) -> list[str]:
    """Validate YAML frontmatter in markdown file."""
    errors = []
    rel_path = file_path.relative_to(file_path.parent.parent)

    try:
        content = file_path.read_text(encoding="utf-8")
    except PermissionError:
        # Best-effort attempt to get file mode for diagnostics
        try:
            mode = f"{file_path.stat().st_mode:o}"
        except OSError:
            mode = "unknown"
        errors.append(
            f"{plugin_name}/{rel_path}: Permission denied reading file\n"
            f"  Check file permissions (current: {mode})"
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

    # Check frontmatter exists
    if not content.startswith("---"):
        errors.append(f"{plugin_name}/{rel_path}: Missing YAML frontmatter (must start with ---)")
        return errors

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{plugin_name}/{rel_path}: Malformed frontmatter (missing closing ---)")
        return errors

    frontmatter_text = parts[1].strip()

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"{plugin_name}/{rel_path}: Invalid YAML in frontmatter\n  {e}")
        return errors

    # Ensure frontmatter is a dictionary
    if not isinstance(frontmatter, dict):
        errors.append(
            f"{plugin_name}/{rel_path}: Frontmatter must be a YAML mapping (key-value pairs), "
            f"got {type(frontmatter).__name__}"
        )
        return errors

    # Check for required fields with non-empty values
    for field in required_fields:
        if field not in frontmatter:
            errors.append(
                f"{plugin_name}/{rel_path}: Missing required field '{field}' in frontmatter"
            )
        elif not frontmatter[field]:
            errors.append(f"{plugin_name}/{rel_path}: Required field '{field}' is empty or null")

    return errors


def check_component_placement(plugin_dir: Path) -> list[str]:
    """Check that components are at root, not in .claude-plugin/."""
    errors = []
    plugin_name = plugin_dir.name
    claude_plugin_dir = plugin_dir / ".claude-plugin"

    # These should NOT be in .claude-plugin/
    invalid_locations = ["commands", "agents", "skills", "hooks"]

    for component in invalid_locations:
        if (claude_plugin_dir / component).exists():
            errors.append(
                f"{plugin_name}: {component}/ directory found in .claude-plugin/ "
                "but must be at plugin root (common mistake - see official docs)"
            )

    return errors


def check_skills_directory(plugin_dir: Path) -> list[str]:
    """Validate skills/ directory and SKILL.md files."""
    errors = []
    plugin_name = plugin_dir.name
    skills_dir = plugin_dir / "skills"

    if not skills_dir.exists():
        return []  # Optional component

    if not skills_dir.is_dir():
        errors.append(f"{plugin_name}: skills/ exists but is not a directory")
        return errors

    # Check each skill subdirectory
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

    if not skill_dirs:
        errors.append(
            f"{plugin_name}/skills/: Directory exists but contains no skill subdirectories"
        )
        return errors

    for skill_path in skill_dirs:
        skill_md = skill_path / "SKILL.md"

        if not skill_md.exists():
            errors.append(f"{plugin_name}/skills/{skill_path.name}: Missing required SKILL.md file")
            continue

        # Validate SKILL.md frontmatter
        frontmatter_errors = validate_markdown_frontmatter(
            skill_md, ["name", "description"], plugin_name
        )
        errors.extend(frontmatter_errors)

    return errors


def check_commands_directory(plugin_dir: Path) -> list[str]:
    """Validate commands/ directory and command files."""
    errors = []
    plugin_name = plugin_dir.name
    commands_dir = plugin_dir / "commands"

    if not commands_dir.exists():
        return []  # Optional component

    if not commands_dir.is_dir():
        errors.append(f"{plugin_name}: commands/ exists but is not a directory")
        return errors

    # Check each .md file
    command_files = list(commands_dir.glob("*.md"))

    if not command_files:
        errors.append(f"{plugin_name}/commands/: Directory exists but contains no .md files")
        return errors

    for cmd_file in command_files:
        # Validate frontmatter
        frontmatter_errors = validate_markdown_frontmatter(cmd_file, ["description"], plugin_name)
        errors.extend(frontmatter_errors)

    return errors


def check_agents_directory(plugin_dir: Path) -> list[str]:
    """Validate agents/ directory and agent files."""
    errors = []
    plugin_name = plugin_dir.name
    agents_dir = plugin_dir / "agents"

    if not agents_dir.exists():
        return []  # Optional component

    if not agents_dir.is_dir():
        errors.append(f"{plugin_name}: agents/ exists but is not a directory")
        return errors

    # Check each .md file
    agent_files = list(agents_dir.glob("*.md"))

    if not agent_files:
        errors.append(f"{plugin_name}/agents/: Directory exists but contains no .md files")
        return errors

    for agent_file in agent_files:
        # Validate frontmatter - agents require description and capabilities
        frontmatter_errors = validate_markdown_frontmatter(
            agent_file, ["description", "capabilities"], plugin_name
        )
        errors.extend(frontmatter_errors)

    return errors


def check_hooks_configuration(plugin_dir: Path, plugin_data: dict) -> list[str]:
    """Validate hooks configuration (file or inline)."""
    errors = []
    plugin_name = plugin_dir.name

    # Check for hooks/hooks.json file
    hooks_file = plugin_dir / "hooks" / "hooks.json"
    inline_hooks = plugin_data.get("hooks")

    if not hooks_file.exists() and not inline_hooks:
        return []  # Optional component

    # Load hooks configuration
    hooks_config = None

    if isinstance(inline_hooks, dict):
        hooks_config = inline_hooks
    elif isinstance(inline_hooks, str):
        # Path to hooks file - validate to prevent path traversal
        custom_hooks_path, error = validate_plugin_path(
            plugin_dir, inline_hooks, f"{plugin_name}/hooks"
        )
        if error:
            errors.append(error)
            return errors
        if not custom_hooks_path.exists():
            errors.append(
                f"{plugin_name}: Hooks file specified in plugin.json not found: {inline_hooks}"
            )
            return errors
        try:
            with open(custom_hooks_path, encoding="utf-8") as f:
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
        except UnicodeDecodeError:
            errors.append(
                f"{plugin_name}: Hooks file is not valid UTF-8: {inline_hooks}\n"
                f"  Ensure file is text, not binary"
            )
            return errors
        except OSError as e:
            errors.append(f"{plugin_name}: Cannot read hooks file: {e}")
            return errors
    elif hooks_file.exists():
        try:
            with open(hooks_file, encoding="utf-8") as f:
                hooks_config = json.load(f)
        except FileNotFoundError:
            errors.append(f"{plugin_name}/hooks/hooks.json: File not found")
            return errors
        except PermissionError:
            errors.append(f"{plugin_name}/hooks/hooks.json: Permission denied reading file")
            return errors
        except json.JSONDecodeError as e:
            errors.append(
                f"{plugin_name}/hooks/hooks.json: Invalid JSON\n"
                f"  Line {e.lineno}, column {e.colno}: {e.msg}"
            )
            return errors
        except UnicodeDecodeError:
            errors.append(
                f"{plugin_name}/hooks/hooks.json: File is not valid UTF-8\n"
                f"  Ensure file is text, not binary"
            )
            return errors
        except OSError as e:
            errors.append(f"{plugin_name}/hooks/hooks.json: Cannot read file: {e}")
            return errors

    if not hooks_config:
        return errors

    # Validate hooks structure
    if "hooks" not in hooks_config:
        errors.append(f"{plugin_name}: Hooks configuration missing 'hooks' key")
        return errors

    # Validate event types
    for event_type, hook_list in hooks_config["hooks"].items():
        if event_type not in VALID_HOOK_EVENTS:
            errors.append(
                f"{plugin_name}: Invalid hook event '{event_type}' "
                f"(valid: {', '.join(sorted(VALID_HOOK_EVENTS))})"
            )

        # Validate each hook in the event
        if isinstance(hook_list, list):
            for _i, hook_entry in enumerate(hook_list):
                if "hooks" in hook_entry and isinstance(hook_entry["hooks"], list):
                    for _j, hook in enumerate(hook_entry["hooks"]):
                        if "type" in hook and hook["type"] not in VALID_HOOK_TYPES:
                            errors.append(
                                f"{plugin_name}: Invalid hook type '{hook['type']}' "
                                f"(valid: {', '.join(sorted(VALID_HOOK_TYPES))})"
                            )

                        # Check if command script exists
                        if hook.get("type") == "command" and "command" in hook:
                            cmd = hook["command"]
                            # Check for ${CLAUDE_PLUGIN_ROOT} usage
                            if "${CLAUDE_PLUGIN_ROOT}" in cmd:
                                # Extract path after variable
                                script_path = cmd.replace("${CLAUDE_PLUGIN_ROOT}/", "")
                                script_path = script_path.split()[
                                    0
                                ]  # Get just the script, not args
                                full_path = plugin_dir / script_path
                                if not full_path.exists():
                                    errors.append(
                                        f"{plugin_name}: Hook command script not found: {script_path}"
                                    )
                            elif cmd.startswith("/"):
                                errors.append(
                                    f"{plugin_name}: Hook command uses absolute path instead of "
                                    "${{CLAUDE_PLUGIN_ROOT}}: {cmd}"
                                )

    return errors


def check_mcp_servers(plugin_dir: Path, plugin_data: dict) -> list[str]:
    """Validate MCP server configuration."""
    errors = []
    plugin_name = plugin_dir.name

    # Check for .mcp.json file
    mcp_file = plugin_dir / ".mcp.json"
    inline_mcp = plugin_data.get("mcpServers")

    if not mcp_file.exists() and not inline_mcp:
        return []  # Optional component

    # Load MCP configuration
    mcp_config = None

    if isinstance(inline_mcp, dict):
        mcp_config = inline_mcp
    elif isinstance(inline_mcp, str):
        # Path to MCP file - validate to prevent path traversal
        custom_mcp_path, error = validate_plugin_path(
            plugin_dir, inline_mcp, f"{plugin_name}/mcpServers"
        )
        if error:
            errors.append(error)
            return errors
        if not custom_mcp_path.exists():
            errors.append(
                f"{plugin_name}: MCP file specified in plugin.json not found: {inline_mcp}"
            )
            return errors
        try:
            with open(custom_mcp_path, encoding="utf-8") as f:
                mcp_config = json.load(f)
        except FileNotFoundError:
            errors.append(f"{plugin_name}: MCP file not found: {inline_mcp}")
            return errors
        except PermissionError:
            errors.append(f"{plugin_name}: Permission denied reading MCP file: {inline_mcp}")
            return errors
        except json.JSONDecodeError as e:
            errors.append(
                f"{plugin_name}: Invalid JSON in MCP file {inline_mcp}\n"
                f"  Line {e.lineno}, column {e.colno}: {e.msg}"
            )
            return errors
        except UnicodeDecodeError:
            errors.append(
                f"{plugin_name}: MCP file is not valid UTF-8: {inline_mcp}\n"
                f"  Ensure file is text, not binary"
            )
            return errors
        except OSError as e:
            errors.append(f"{plugin_name}: Cannot read MCP file: {e}")
            return errors
    elif mcp_file.exists():
        try:
            with open(mcp_file, encoding="utf-8") as f:
                mcp_config = json.load(f)
        except PermissionError:
            errors.append(f"{plugin_name}: Permission denied reading .mcp.json")
            return errors
        except json.JSONDecodeError as e:
            errors.append(
                f"{plugin_name}/.mcp.json: Invalid JSON\n"
                f"  Line {e.lineno}, column {e.colno}: {e.msg}"
            )
            return errors
        except UnicodeDecodeError:
            errors.append(
                f"{plugin_name}/.mcp.json: File is not valid UTF-8\n"
                f"  Ensure file is text, not binary"
            )
            return errors
        except OSError as e:
            errors.append(f"{plugin_name}: Cannot read .mcp.json: {e}")
            return errors

    if not mcp_config:
        return errors

    # Validate MCP server structure
    if "mcpServers" not in mcp_config:
        errors.append(f"{plugin_name}: MCP configuration missing 'mcpServers' key")
        return errors

    # Validate each server
    for server_name, server_config in mcp_config["mcpServers"].items():
        if "command" not in server_config:
            errors.append(f"{plugin_name}: MCP server '{server_name}' missing 'command' field")

        # Check for ${CLAUDE_PLUGIN_ROOT} usage in paths
        command = server_config.get("command", "")
        if "/" in command and "${CLAUDE_PLUGIN_ROOT}" not in command and command.startswith("/"):
            errors.append(
                f"{plugin_name}: MCP server '{server_name}' uses absolute path instead of "
                "${{CLAUDE_PLUGIN_ROOT}}"
            )

    return errors


def check_custom_component_paths(plugin_dir: Path, plugin_data: dict) -> list[str]:
    """Validate custom component paths specified in plugin.json."""
    errors = []
    plugin_name = plugin_dir.name

    # Check custom command paths
    custom_commands = plugin_data.get("commands")
    if custom_commands:
        paths = [custom_commands] if isinstance(custom_commands, str) else custom_commands
        for path in paths:
            if not path.startswith("./"):
                errors.append(f"{plugin_name}: Custom command path must start with './': {path}")
            else:
                # Validate to prevent path traversal
                full_path, error = validate_plugin_path(plugin_dir, path, f"{plugin_name}/commands")
                if error:
                    errors.append(error)
                elif not full_path.exists():
                    errors.append(f"{plugin_name}: Custom command path not found: {path}")

    # Check custom agent paths
    custom_agents = plugin_data.get("agents")
    if custom_agents:
        paths = [custom_agents] if isinstance(custom_agents, str) else custom_agents
        for path in paths:
            if not path.startswith("./"):
                errors.append(f"{plugin_name}: Custom agent path must start with './': {path}")
            else:
                # Validate to prevent path traversal
                full_path, error = validate_plugin_path(plugin_dir, path, f"{plugin_name}/agents")
                if error:
                    errors.append(error)
                elif not full_path.exists():
                    errors.append(f"{plugin_name}: Custom agent path not found: {path}")

    return errors


def check_manifest_conflicts(
    plugin_name: str, marketplace_entry: dict, plugin_json_data: dict
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
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
    ]

    for field in comparable_fields:
        market_value = marketplace_entry.get(field)
        plugin_value = plugin_json_data.get(field)

        # Both exist and differ
        if market_value is not None and plugin_value is not None:
            # Special handling for keywords (order-insensitive)
            if (
                field == "keywords"
                and isinstance(market_value, list)
                and isinstance(plugin_value, list)
            ):
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

    return warnings


def check_plugin_manifest(
    plugin_dir: Path, marketplace_entry: dict | None = None, require_manifest: bool = True
) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.

    Args:
        plugin_dir: Path to plugin directory
        marketplace_entry: Plugin entry from marketplace.json (optional)
        require_manifest: If True, plugin.json is required. If False, plugin.json
                         is optional and marketplace entry data is used as fallback.
                         This value comes from the 'strict' field in marketplace.json.

    Returns dict with categorized errors and warnings:
    {
        'manifest': [...],
        'warnings': [...],
        'placement': [...],
        'skills': [...],
        'commands': [...],
        'agents': [...],
        'hooks': [...],
        'mcp': [...],
        'paths': [...]
    }
    """
    results = {
        "manifest": [],
        "warnings": [],  # NEW: Conflict warnings
        "placement": [],
        "skills": [],
        "commands": [],
        "agents": [],
        "hooks": [],
        "mcp": [],
        "paths": [],
    }

    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

    # Require manifest: plugin.json required
    if require_manifest:
        if not plugin_json.exists():
            results["manifest"].append(
                f"{plugin_dir.name}: Missing .claude-plugin/plugin.json (required by marketplace.json)"
            )
            return results

        # Load and validate plugin.json
        try:
            with open(plugin_json, encoding="utf-8") as f:
                data = json.load(f)
        except PermissionError:
            results["manifest"].append(f"{plugin_dir.name}: Permission denied reading plugin.json")
            return results
        except json.JSONDecodeError as e:
            results["manifest"].append(
                f"{plugin_dir.name}: Invalid JSON in plugin.json\n"
                f"  Line {e.lineno}, column {e.colno}: {e.msg}"
            )
            return results
        except UnicodeDecodeError:
            results["manifest"].append(
                f"{plugin_dir.name}: plugin.json is not valid UTF-8\n"
                f"  Ensure file is text, not binary"
            )
            return results
        except OSError as e:
            results["manifest"].append(f"{plugin_dir.name}: Cannot read plugin.json: {e}")
            return results

        # Validate against schema
        schema_errors = validate_json_schema(data, PLUGIN_MANIFEST_SCHEMA, plugin_dir.name)
        results["manifest"].extend(schema_errors)

    # Optional manifest: plugin.json optional
    else:
        if plugin_json.exists():
            # Load and validate if present
            try:
                with open(plugin_json, encoding="utf-8") as f:
                    data = json.load(f)
            except PermissionError:
                results["manifest"].append(
                    f"{plugin_dir.name}: Permission denied reading plugin.json"
                )
                return results
            except json.JSONDecodeError as e:
                results["manifest"].append(
                    f"{plugin_dir.name}: Invalid JSON in plugin.json\n"
                    f"  Line {e.lineno}, column {e.colno}: {e.msg}"
                )
                return results
            except UnicodeDecodeError:
                results["manifest"].append(
                    f"{plugin_dir.name}: plugin.json is not valid UTF-8\n"
                    f"  Ensure file is text, not binary"
                )
                return results
            except OSError as e:
                results["manifest"].append(f"{plugin_dir.name}: Cannot read plugin.json: {e}")
                return results

            # Validate against schema only when plugin.json exists
            schema_errors = validate_json_schema(data, PLUGIN_MANIFEST_SCHEMA, plugin_dir.name)
            results["manifest"].extend(schema_errors)
        else:
            # Use marketplace entry as manifest (don't validate against plugin.json schema)
            data = marketplace_entry if marketplace_entry else {}

    # Check for conflicts if both marketplace entry and plugin.json exist
    if marketplace_entry and plugin_json.exists():
        conflict_warnings = check_manifest_conflicts(plugin_dir.name, marketplace_entry, data)
        results["warnings"].extend(conflict_warnings)

    # Check README.md exists
    if not (plugin_dir / "README.md").exists():
        results["manifest"].append(f"{plugin_dir.name}: Missing README.md")

    # Run all component validations
    results["placement"] = check_component_placement(plugin_dir)
    results["skills"] = check_skills_directory(plugin_dir)
    results["commands"] = check_commands_directory(plugin_dir)
    results["agents"] = check_agents_directory(plugin_dir)
    results["hooks"] = check_hooks_configuration(plugin_dir, data)
    results["mcp"] = check_mcp_servers(plugin_dir, data)
    results["paths"] = check_custom_component_paths(plugin_dir, data)

    return results


def check_marketplace_structure() -> dict[str, Any]:
    """Check overall marketplace structure.

    Returns dict with:
    {
        'marketplace_errors': [...],
        'plugin_results': {
            'plugin-name': {
                'manifest': [...],
                'skills': [...],
                ...
            }
        }
    }
    """
    result = {"marketplace_errors": [], "plugin_results": {}}

    repo_root = Path(__file__).parent.parent

    # Check marketplace.json
    marketplace_json = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_json.exists():
        result["marketplace_errors"].append("Missing .claude-plugin/marketplace.json")
        return result

    # Validate marketplace.json syntax
    try:
        with open(marketplace_json, encoding="utf-8") as f:
            marketplace_data = json.load(f)
    except PermissionError:
        result["marketplace_errors"].append(
            "Permission denied reading .claude-plugin/marketplace.json"
        )
        return result
    except json.JSONDecodeError as e:
        result["marketplace_errors"].append(
            f"Invalid JSON in marketplace.json\n  Line {e.lineno}, column {e.colno}: {e.msg}"
        )
        return result
    except UnicodeDecodeError:
        result["marketplace_errors"].append(
            "marketplace.json is not valid UTF-8\n  Ensure file is text, not binary"
        )
        return result
    except OSError as e:
        result["marketplace_errors"].append(f"Cannot read marketplace.json: {e}")
        return result

    # Validate marketplace schema
    marketplace_schema_errors = validate_marketplace_json(marketplace_data)
    result["marketplace_errors"].extend(marketplace_schema_errors)

    # If marketplace structure invalid, don't continue
    if marketplace_schema_errors:
        return result

    # Check each plugin in marketplace
    for plugin_entry in marketplace_data["plugins"]:
        plugin_name = plugin_entry.get("name", "unknown")
        plugin_source = plugin_entry.get("source", "")

        # Skip external sources (GitHub/Git URLs)
        if isinstance(plugin_source, dict):
            continue  # External sources not validated locally

        if not plugin_source:
            result["marketplace_errors"].append(f"Plugin '{plugin_name}' missing 'source' field")
            continue

        # Resolve plugin directory - validate to prevent path traversal
        plugin_dir, error = validate_plugin_path(
            repo_root, plugin_source, f"Plugin '{plugin_name}'"
        )
        if error:
            result["marketplace_errors"].append(error)
            continue

        if not plugin_dir.exists():
            result["marketplace_errors"].append(
                f"Plugin '{plugin_name}' source directory not found: {plugin_source}"
            )
            continue

        # Get strict mode from marketplace entry (default: true)
        require_manifest = plugin_entry.get("strict", True)

        # Validate plugin manifest and components
        plugin_results = check_plugin_manifest(
            plugin_dir, marketplace_entry=plugin_entry, require_manifest=require_manifest
        )
        result["plugin_results"][plugin_name] = plugin_results

    return result


def calculate_exit_code(result: dict[str, Any], strict: bool = False) -> int:
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
    total_errors += len(result.get("marketplace_errors", []))

    # Count plugin-level errors and warnings
    for plugin_result in result.get("plugin_results", {}).values():
        for category, issues in plugin_result.items():
            if category == "warnings":
                total_warnings += len(issues)
            else:
                total_errors += len(issues)

    # Strict mode: warnings are failures
    if strict and total_warnings > 0:
        return 1

    # Normal mode: only errors are failures
    return 1 if total_errors > 0 else 0


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
        """,
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors (useful for CI/CD)"
    )
    args = parser.parse_args()

    mode_text = "[bold cyan]Verifying marketplace structure"
    if args.strict:
        mode_text += " (strict mode)"
    mode_text += "...[/bold cyan]\n"
    console.print("\n" + mode_text)

    result = check_marketplace_structure()

    # Count errors and warnings
    total_errors = len(result["marketplace_errors"])
    total_warnings = 0
    all_plugin_errors = {}
    all_plugin_warnings = {}

    for plugin_name, plugin_result in result["plugin_results"].items():
        plugin_errors = []
        plugin_warnings = []
        for category, issues in plugin_result.items():
            if issues:
                if category == "warnings":
                    plugin_warnings.extend(issues)
                else:
                    plugin_errors.extend(issues)

        if plugin_errors:
            all_plugin_errors[plugin_name] = plugin_errors
            total_errors += len(plugin_errors)
        if plugin_warnings:
            all_plugin_warnings[plugin_name] = plugin_warnings
            total_warnings += len(plugin_warnings)

    # Display marketplace errors
    if result["marketplace_errors"]:
        console.print("[bold red]Marketplace Structure Errors:[/bold red]\n")
        for error in result["marketplace_errors"]:
            console.print(f"  [red]• {error}[/red]")
        console.print()

    # Display plugin validation results
    if result["plugin_results"]:
        # Create summary table
        table = Table(title="Plugin Validation Summary", show_header=True, header_style="bold cyan")
        table.add_column("Plugin", style="cyan")
        table.add_column("Manifest", justify="center")
        table.add_column("Placement", justify="center")
        table.add_column("Skills", justify="center")
        table.add_column("Commands", justify="center")
        table.add_column("Agents", justify="center")
        table.add_column("Hooks", justify="center")
        table.add_column("MCP", justify="center")
        table.add_column("Paths", justify="center")
        table.add_column("Warnings", justify="center")

        for plugin_name, plugin_result in result["plugin_results"].items():

            def status_icon(errors):
                return "[red]✗[/red]" if errors else "[green]✓[/green]"

            table.add_row(
                plugin_name,
                status_icon(plugin_result["manifest"]),
                status_icon(plugin_result["placement"]),
                status_icon(plugin_result["skills"]),
                status_icon(plugin_result["commands"]),
                status_icon(plugin_result["agents"]),
                status_icon(plugin_result["hooks"]),
                status_icon(plugin_result["mcp"]),
                status_icon(plugin_result["paths"]),
                f"[yellow]{len(plugin_result.get('warnings', []))}[/yellow]"
                if plugin_result.get("warnings")
                else "[green]0[/green]",
            )

        console.print(table)
        console.print()

        # Display detailed errors by category
        for plugin_name, plugin_result in result["plugin_results"].items():
            has_errors = any(
                errors
                for category, errors in plugin_result.items()
                if category != "warnings" and errors
            )
            if has_errors:
                console.print(f"\n[bold yellow]{plugin_name} - Detailed Errors:[/bold yellow]")

                for category, errors in plugin_result.items():
                    if category != "warnings" and errors:
                        category_label = category.capitalize()
                        console.print(f"\n  [cyan]{category_label}:[/cyan]")
                        for error in errors:
                            console.print(f"    [red]• {error}[/red]")

                console.print()

    # Display warnings
    if total_warnings > 0:
        warning_style = "yellow" if not args.strict else "red"
        warning_label = "Warnings" if not args.strict else "Warnings (treated as errors)"

        console.print(
            f"\n[bold {warning_style}]{warning_label} ({total_warnings}):[/bold {warning_style}]\n"
        )

        for plugin_name, warnings in all_plugin_warnings.items():
            console.print(f"  [bold]{plugin_name}:[/bold]")
            for warning in warnings:
                console.print(f"    [{warning_style}]• {warning}[/{warning_style}]")

        if args.strict:
            console.print("\n  [red](--strict mode: warnings treated as errors)[/red]\n")
        console.print()

    # Calculate exit code
    exit_code = calculate_exit_code(result, strict=args.strict)

    # Final summary
    if exit_code != 0:
        message = f"✗ Validation failed with {total_errors} error(s)"
        if total_warnings > 0:
            message += f" and {total_warnings} warning(s)"
        if args.strict and total_warnings > 0:
            message += " (warnings treated as errors in strict mode)"

        console.print(
            Panel.fit(
                f"[bold red]{message}[/bold red]\nSee details above for specific issues.",
                border_style="red",
            )
        )
    else:
        message = "✅ All verification checks passed!"
        if total_warnings > 0:
            message += f"\n{total_warnings} warning(s) found but not failing (normal mode)"
        message += "\nMarketplace structure and all plugins are valid."

        console.print(Panel.fit(f"[bold green]{message}[/bold green]", border_style="green"))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
