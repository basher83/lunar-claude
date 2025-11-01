---
name: python-code-quality
description: >
  Python code quality tooling with ruff and pyright.
  Use when setting up linting, formatting, type checking,
  configuring ruff or pyright, or establishing code quality standards.
---

# Python Code Quality with Ruff and Pyright

Modern Python code quality tooling using ruff (linting + formatting) and pyright (type checking).

## Quick Start

### Install Tools

```bash
# Using uv (recommended)
uv add --dev ruff pyright

# Using pip
pip install ruff pyright
```

### Run Quality Checks

```bash
# Format and lint with ruff
ruff check --fix .
ruff format .

# Type check with pyright
pyright
```

## When to Use This Skill

Use this skill when:

- Setting up linting and formatting for a Python project
- Configuring type checking
- Establishing code quality standards for a team
- Integrating quality checks into pre-commit or CI/CD
- Migrating from black/flake8/mypy to ruff/pyright

## Ruff: All-in-One Linter and Formatter

Ruff combines the functionality of flake8, black, isort, and more:

**Benefits:**

- 10-100x faster than alternatives
- Drop-in replacement for black, flake8, isort
- Single tool configuration
- Auto-fix for many violations

**Configuration:** See `reference/ruff-configuration.md`

## Pyright: Fast Type Checker

Pyright provides static type checking for Python:

**Benefits:**

- Faster than mypy
- Better editor integration (VS Code, etc.)
- Incremental type checking
- Configurable strictness

**Configuration:** See `reference/pyright-configuration.md`

## Recommended Workflow

1. **Pre-commit Hooks** - Run quality checks before each commit
   - See: `patterns/pre-commit-integration.md`

2. **CI/CD Quality Gates** - Block merges on quality failures
   - See: `patterns/ci-cd-quality-gates.md`

3. **Editor Integration** - Real-time feedback while coding
   - See: `workflows/quality-workflow.md`

## Configuration Templates

Generic starter configs in `examples/`:

- `pyrightconfig-starter.json` - Minimal type checking
- `pyrightconfig-strict.json` - Strict type checking
- `ruff-minimal.toml` - Basic linting + formatting
- `ruff-comprehensive.toml` - Full-featured config

## Helper Tools

- `tools/python_formatter.py` - Batch format Python files
- `tools/python_ruff_checker.py` - Check code quality

## Ruff vs Alternatives

| Feature | Ruff | Black + Flake8 + isort |
|---------|------|------------------------|
| Speed | ⚡⚡⚡ | ⚡ |
| Configuration | Single file | Multiple files |
| Auto-fix | ✅ | Partial |
| Formatting | ✅ | Black only |
| Import sorting | ✅ | isort only |

## Pyright vs mypy

| Feature | Pyright | mypy |
|---------|---------|------|
| Speed | ⚡⚡⚡ | ⚡⚡ |
| VS Code integration | Native | Extension |
| Configuration | JSON | INI/TOML |
| Incremental checking | ✅ | ✅ |

## Common Patterns

### Ignore Specific Lines

```python
# Ruff
x = 1  # noqa: F841  # Unused variable

# Pyright
x = 1  # type: ignore
```

### Configure Per-Directory

```toml
# ruff.toml
[tool.ruff]
exclude = ["migrations/", "scripts/"]

[tool.ruff.lint]
select = ["E", "F", "W"]
```

## Next Steps

1. Choose config template from `examples/`
2. Set up pre-commit hooks: `patterns/pre-commit-integration.md`
3. Add CI/CD quality gates: `patterns/ci-cd-quality-gates.md`
4. Configure editor integration: `workflows/quality-workflow.md`

## Reference Documentation

- `reference/ruff-configuration.md` - Complete ruff configuration guide
- `reference/ruff-linting-settings.md` - Linting rule categories
- `reference/ruff-formatting-settings.md` - Formatting options
- `reference/pyright-configuration.md` - Pyright setup and configuration
