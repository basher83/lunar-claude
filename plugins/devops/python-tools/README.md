# Python Tools

Comprehensive Python development toolkit for scripting, code quality, and common patterns.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install python-tools:

```bash
/plugin install python-tools@lunar-claude
```

## Skills

### python-uv-scripts

Python single-file script development using uv and PEP 723 inline metadata.

**Use when:**

- Creating standalone Python utilities
- Converting scripts to uv format
- Managing script dependencies with inline metadata
- Building self-executable Python scripts

**Triggers:** uv, uv script, pep 723, inline dependencies, single-file script

**Learn more:** [skills/python-uv-scripts/](skills/python-uv-scripts/)

---

### python-json-parsing

Best practices for JSON parsing in Python with performance optimization and security focus.

**Use when:**

- Working with JSON data from APIs
- Optimizing JSON performance in high-throughput applications
- Handling large JSON files (> 100MB)
- Securing applications against JSON injection
- Extracting data from complex nested JSON structures

**Triggers:** json, parse json, json parsing, orjson, msgspec, large json, json performance,
json security, jsonpath

**Learn more:** [skills/python-json-parsing/](skills/python-json-parsing/)

---

## How It Works

### Autonomous Mode

Simply ask Claude for help with Python development:

```text
"Parse this large JSON file efficiently"
"Create a Python script using uv that fetches API data"
```

Claude automatically activates the relevant skill based on your request.

### Layered Documentation

Each skill uses progressive disclosure for comprehensive guidance:

- **SKILL.md** - Main entry point with quick start and overview
- **patterns/** - Production-ready implementation patterns
- **anti-patterns/** - Common mistakes to avoid
- **examples/** - Real-world code examples and config templates
- **reference/** - Deep technical documentation
- **tools/** - Helper scripts and utilities
- **workflows/** - Process documentation

This structure provides quick answers while making deep knowledge accessible when needed.

## Supporting Documentation

### python-uv-scripts

- `/patterns/` - Common script patterns (CLI tools, API clients, data processing)
- `/anti-patterns/` - When NOT to use single-file scripts
- `/examples/` - Real-world script examples
- `/workflows/` - CI/CD integration for uv scripts
- `/reference/` - uv command reference and troubleshooting
- `/tools/` - Script conversion and validation utilities

### python-json-parsing

- `/reference/` - Comprehensive 2025 best practices research
- `/patterns/` - Streaming large files, custom serialization, JSONPath querying
- `/anti-patterns/` - Security (injection prevention), eval() dangers
- `/examples/` - High-performance parsing, streaming, validation
- `/tools/` - Performance benchmark script

## Version History

- 1.1.0 - Remove python-code-quality skill (superseded by repo-forge presets)
- 1.0.0 - Initial release
  - python-uv-scripts: uv-based script development
  - python-json-parsing: JSON best practices with performance and security focus
