# Python UV Tools

Expert guidance for creating production-ready, self-contained Python scripts using uv's inline dependency management (PEP 723).

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install python-uv-tools:

```bash
/plugin install python-uv-tools@lunar-claude
```

## Components

### Skills

- **python-uv-scripts** - Comprehensive skill for Python single-file script development with uv
  - Script creation with inline dependencies
  - Dependency management best practices
  - Self-executable script patterns
  - Testing strategies
  - Security best practices
  - CI/CD integration patterns
  - When to use (and not use) single-file scripts

## Usage

### Autonomous Mode

Simply ask Claude to help with Python/uv scripts:

```
"Create a Python script using uv that fetches GitHub API data"
"Convert this Python script to use uv inline dependencies"
"Help me add testing to my uv script"
```

Claude will automatically use the python-uv-scripts skill.

## How It Works

The python-uv-scripts skill provides comprehensive guidance on:

- **Quick Start**: Template for creating your first uv script
- **Core Patterns**: Common patterns for different use cases (API clients, CLI tools, data processing, etc.)
- **Anti-Patterns**: What to avoid and when not to use single-file scripts
- **Testing**: Patterns for testing scripts with inline dependencies
- **Security**: Best practices for secure script development
- **CI/CD**: Integration with continuous integration pipelines
- **Reference**: Complete uv command reference and troubleshooting

## Supporting Documentation

The skill includes extensive reference material:
- `/patterns/` - Common implementation patterns
- `/anti-patterns/` - Mistakes to avoid
- `/examples/` - Real-world examples
- `/workflows/` - CI/CD and development workflows
- `/reference/` - Command reference and troubleshooting
- `/tools/` - Supporting tools and utilities

## Version History

- 1.0.0 - Initial release with comprehensive uv scripting guidance
