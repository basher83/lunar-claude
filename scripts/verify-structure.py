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

This script validates:
- Plugin manifest schema (plugin.json) against Claude Code reference
- Marketplace registry structure
- Directory structure for all plugins
- Required files and components

Usage:
    ./scripts/verify-structure.py
    python scripts/verify-structure.py

Exit codes:
    0 - All checks passed
    1 - Validation errors found
"""

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

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


def check_plugin_manifest(plugin_dir: Path) -> list[str]:
    """Validate a single plugin's manifest and structure."""
    errors = []
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

    # Check plugin.json exists
    if not plugin_json.exists():
        errors.append(f"{plugin_dir.name}: Missing .claude-plugin/plugin.json")
        return errors

    # Validate JSON syntax
    try:
        with open(plugin_json) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"{plugin_dir.name}: Invalid JSON in plugin.json: {e}")
        return errors

    # Validate against schema
    schema_errors = validate_json_schema(data, PLUGIN_MANIFEST_SCHEMA, plugin_dir.name)
    errors.extend(schema_errors)

    # Check README.md exists
    if not (plugin_dir / "README.md").exists():
        errors.append(f"{plugin_dir.name}: Missing README.md")

    return errors


def check_marketplace_structure() -> tuple[list[str], list[str]]:
    """Check overall marketplace structure. Returns (errors, warnings)."""
    errors = []
    warnings = []
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
            errors.append(f"Missing required directory: {dir_path}")

    # Check marketplace.json
    marketplace_json = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_json.exists():
        errors.append("Missing .claude-plugin/marketplace.json")
        return errors, warnings

    # Validate marketplace.json syntax
    try:
        with open(marketplace_json) as f:
            marketplace_data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in marketplace.json: {e}")
        return errors, warnings

    # Check marketplace structure
    if "plugins" not in marketplace_data:
        errors.append("marketplace.json missing 'plugins' array")
        return errors, warnings

    # Check each plugin in marketplace
    for plugin_entry in marketplace_data["plugins"]:
        plugin_name = plugin_entry.get("name", "unknown")
        plugin_source = plugin_entry.get("source", "")

        if not plugin_source:
            errors.append(f"Plugin '{plugin_name}' missing 'source' field")
            continue

        # Resolve plugin directory
        plugin_dir = repo_root / plugin_source.lstrip("./")

        if not plugin_dir.exists():
            errors.append(f"Plugin '{plugin_name}' source directory not found: {plugin_source}")
            continue

        # Validate plugin manifest
        plugin_errors = check_plugin_manifest(plugin_dir)
        errors.extend(plugin_errors)

    return errors, warnings


def main() -> int:
    """Run all verification checks."""
    console.print("\n[bold cyan]Verifying lunar-claude marketplace structure...[/bold cyan]\n")

    errors, warnings = check_marketplace_structure()

    # Display results
    if errors:
        console.print("[bold red]✗ Validation failed with errors:[/bold red]\n")
        for error in errors:
            console.print(f"  [red]• {error}[/red]")
        console.print()
        return 1

    if warnings:
        console.print("[bold yellow]⚠ Warnings found:[/bold yellow]\n")
        for warning in warnings:
            console.print(f"  [yellow]• {warning}[/yellow]")
        console.print()

    # Success!
    console.print(Panel.fit(
        "[bold green]✅ All verification checks passed![/bold green]\n"
        "Marketplace structure is valid and complete.",
        border_style="green"
    ))

    return 0


if __name__ == "__main__":
    sys.exit(main())
