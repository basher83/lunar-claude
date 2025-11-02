#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema>=4.20.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Verify lunar-claude marketplace structure and validate plugin manifests.

This script validates all aspects of Claude Code plugins per official documentation:

Marketplace Structure:
- marketplace.json syntax and schema
- Plugin registry completeness
- Required category directories

Plugin Components:
- Manifest (plugin.json) schema and metadata
- Component placement (not in .claude-plugin/)
- Skills (SKILL.md frontmatter, directory structure)
- Commands (markdown frontmatter, file structure)
- Agents (markdown frontmatter, capabilities field)
- Hooks (event types, hook types, script existence)
- MCP servers (configuration, ${CLAUDE_PLUGIN_ROOT} usage)
- Custom component paths (existence, relative paths)

Usage:
    ./scripts/verify-structure.py
    python scripts/verify-structure.py

Exit codes:
    0 - All checks passed
    1 - Validation errors found
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Valid hook event types from official docs
VALID_HOOK_EVENTS = {
    "PreToolUse", "PostToolUse", "UserPromptSubmit", "Notification",
    "Stop", "SubagentStop", "SessionStart", "SessionEnd", "PreCompact"
}

# Valid hook types
VALID_HOOK_TYPES = {"command", "validation", "notification"}

# Plugin manifest schema based on ai_docs/plugins-referance.md
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
            "description": "Unique identifier (kebab-case, no spaces)"
        },
        # Optional metadata
        "version": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$",
            "description": "Semantic version"
        },
        "description": {
            "type": "string",
            "description": "Brief explanation of plugin purpose"
        },
        "author": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "url": {"type": "string", "format": "uri"}
            },
            "required": ["name"]
        },
        "homepage": {
            "type": "string",
            "format": "uri",
            "description": "Documentation URL"
        },
        "repository": {
            "type": "string",
            "format": "uri",
            "description": "Source code URL"
        },
        "license": {
            "type": "string",
            "description": "License identifier"
        },
        "keywords": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Discovery tags"
        },
        # Component paths
        "commands": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ],
            "description": "Additional command files/directories"
        },
        "agents": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ],
            "description": "Additional agent files"
        },
        "hooks": {
            "oneOf": [
                {"type": "string"},
                {"type": "object"}
            ],
            "description": "Hook config path or inline config"
        },
        "mcpServers": {
            "oneOf": [
                {"type": "string"},
                {"type": "object"}
            ],
            "description": "MCP config path or inline config"
        }
    }
}


def validate_json_schema(data: dict[str, Any], schema: dict[str, Any], context: str) -> list[str]:
    """Validate JSON data against schema, return list of errors."""
    validator = Draft7Validator(schema)
    errors = []

    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"{context}: {path}: {error.message}")

    return errors


def validate_markdown_frontmatter(
    file_path: Path,
    required_fields: list[str],
    plugin_name: str
) -> list[str]:
    """Validate YAML frontmatter in markdown file."""
    errors = []
    rel_path = file_path.relative_to(file_path.parent.parent)

    try:
        content = file_path.read_text()
    except Exception as e:
        errors.append(f"{plugin_name}/{rel_path}: Error reading file: {e}")
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

    frontmatter = parts[1].strip()

    # Basic check for required fields
    for field in required_fields:
        if not re.search(rf"^{field}:\s*.+", frontmatter, re.MULTILINE):
            errors.append(f"{plugin_name}/{rel_path}: Missing required field '{field}' in frontmatter")

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
        errors.append(f"{plugin_name}/skills/: Directory exists but contains no skill subdirectories")
        return errors

    for skill_path in skill_dirs:
        skill_md = skill_path / "SKILL.md"

        if not skill_md.exists():
            errors.append(
                f"{plugin_name}/skills/{skill_path.name}: "
                "Missing required SKILL.md file"
            )
            continue

        # Validate SKILL.md frontmatter
        frontmatter_errors = validate_markdown_frontmatter(
            skill_md,
            ["name", "description"],
            plugin_name
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
        frontmatter_errors = validate_markdown_frontmatter(
            cmd_file,
            ["description"],
            plugin_name
        )
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
            agent_file,
            ["description", "capabilities"],
            plugin_name
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
        # Path to hooks file
        custom_hooks_path = plugin_dir / inline_hooks.lstrip("./")
        if not custom_hooks_path.exists():
            errors.append(f"{plugin_name}: Hooks file specified in plugin.json not found: {inline_hooks}")
            return errors
        try:
            with open(custom_hooks_path) as f:
                hooks_config = json.load(f)
        except Exception as e:
            errors.append(f"{plugin_name}: Error loading hooks file: {e}")
            return errors
    elif hooks_file.exists():
        try:
            with open(hooks_file) as f:
                hooks_config = json.load(f)
        except Exception as e:
            errors.append(f"{plugin_name}/hooks/hooks.json: Invalid JSON: {e}")
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
            for i, hook_entry in enumerate(hook_list):
                if "hooks" in hook_entry and isinstance(hook_entry["hooks"], list):
                    for j, hook in enumerate(hook_entry["hooks"]):
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
                                script_path = script_path.split()[0]  # Get just the script, not args
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
        # Path to MCP file
        custom_mcp_path = plugin_dir / inline_mcp.lstrip("./")
        if not custom_mcp_path.exists():
            errors.append(f"{plugin_name}: MCP file specified in plugin.json not found: {inline_mcp}")
            return errors
        try:
            with open(custom_mcp_path) as f:
                mcp_config = json.load(f)
        except Exception as e:
            errors.append(f"{plugin_name}: Error loading MCP file: {e}")
            return errors
    elif mcp_file.exists():
        try:
            with open(mcp_file) as f:
                mcp_config = json.load(f)
        except Exception as e:
            errors.append(f"{plugin_name}/.mcp.json: Invalid JSON: {e}")
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
                errors.append(
                    f"{plugin_name}: Custom command path must start with './': {path}"
                )
            else:
                full_path = plugin_dir / path.lstrip("./")
                if not full_path.exists():
                    errors.append(f"{plugin_name}: Custom command path not found: {path}")

    # Check custom agent paths
    custom_agents = plugin_data.get("agents")
    if custom_agents:
        paths = [custom_agents] if isinstance(custom_agents, str) else custom_agents
        for path in paths:
            if not path.startswith("./"):
                errors.append(
                    f"{plugin_name}: Custom agent path must start with './': {path}"
                )
            else:
                full_path = plugin_dir / path.lstrip("./")
                if not full_path.exists():
                    errors.append(f"{plugin_name}: Custom agent path not found: {path}")

    return errors


def check_plugin_manifest(plugin_dir: Path) -> dict[str, list[str]]:
    """Validate a single plugin's manifest and structure.

    Returns dict with categorized errors:
    {
        'manifest': [...],
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
        'manifest': [],
        'placement': [],
        'skills': [],
        'commands': [],
        'agents': [],
        'hooks': [],
        'mcp': [],
        'paths': []
    }

    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

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

    # Validate against schema
    schema_errors = validate_json_schema(data, PLUGIN_MANIFEST_SCHEMA, plugin_dir.name)
    results['manifest'].extend(schema_errors)

    # Check README.md exists
    if not (plugin_dir / "README.md").exists():
        results['manifest'].append(f"{plugin_dir.name}: Missing README.md")

    # Run all component validations
    results['placement'] = check_component_placement(plugin_dir)
    results['skills'] = check_skills_directory(plugin_dir)
    results['commands'] = check_commands_directory(plugin_dir)
    results['agents'] = check_agents_directory(plugin_dir)
    results['hooks'] = check_hooks_configuration(plugin_dir, data)
    results['mcp'] = check_mcp_servers(plugin_dir, data)
    results['paths'] = check_custom_component_paths(plugin_dir, data)

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
    result = {
        'marketplace_errors': [],
        'plugin_results': {}
    }

    repo_root = Path(__file__).parent.parent

    # Check core directories
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

    # Check marketplace.json
    marketplace_json = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_json.exists():
        result['marketplace_errors'].append("Missing .claude-plugin/marketplace.json")
        return result

    # Validate marketplace.json syntax
    try:
        with open(marketplace_json) as f:
            marketplace_data = json.load(f)
    except json.JSONDecodeError as e:
        result['marketplace_errors'].append(f"Invalid JSON in marketplace.json: {e}")
        return result

    # Check marketplace structure
    if "plugins" not in marketplace_data:
        result['marketplace_errors'].append("marketplace.json missing 'plugins' array")
        return result

    # Check each plugin in marketplace
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

    return result


def main() -> int:
    """Run all verification checks."""
    console.print("\n[bold cyan]Verifying lunar-claude marketplace structure...[/bold cyan]\n")

    result = check_marketplace_structure()

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

    # Display marketplace errors
    if result['marketplace_errors']:
        console.print("[bold red]Marketplace Structure Errors:[/bold red]\n")
        for error in result['marketplace_errors']:
            console.print(f"  [red]• {error}[/red]")
        console.print()

    # Display plugin validation results
    if result['plugin_results']:
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

        for plugin_name, plugin_result in result['plugin_results'].items():
            def status_icon(errors):
                return "[red]✗[/red]" if errors else "[green]✓[/green]"

            table.add_row(
                plugin_name,
                status_icon(plugin_result['manifest']),
                status_icon(plugin_result['placement']),
                status_icon(plugin_result['skills']),
                status_icon(plugin_result['commands']),
                status_icon(plugin_result['agents']),
                status_icon(plugin_result['hooks']),
                status_icon(plugin_result['mcp']),
                status_icon(plugin_result['paths'])
            )

        console.print(table)
        console.print()

        # Display detailed errors by category
        for plugin_name, plugin_result in result['plugin_results'].items():
            has_errors = any(errors for errors in plugin_result.values())
            if has_errors:
                console.print(f"\n[bold yellow]{plugin_name} - Detailed Errors:[/bold yellow]")

                for category, errors in plugin_result.items():
                    if errors:
                        category_label = category.capitalize()
                        console.print(f"\n  [cyan]{category_label}:[/cyan]")
                        for error in errors:
                            console.print(f"    [red]• {error}[/red]")

                console.print()

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


if __name__ == "__main__":
    sys.exit(main())
