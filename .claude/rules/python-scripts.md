---
paths: scripts/**/*.py, plugins/**/*.py, **/*.py
---

# Python Script Standards

## PEP 723 Inline Metadata (uv Scripts)

All standalone Python scripts should use PEP 723 inline metadata for dependencies:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "rich>=13.0.0",
# ]
# ///
```

## Code Quality

- **Formatter**: ruff format (see `ruff.toml`)
- **Linter**: ruff check with rules defined in `ruff.toml`
- **Type checker**: pyright with strict mode (see `pyrightconfig.json`)

## Conventions

- Use `pathlib.Path` over `os.path`
- Use `rich` for CLI output when appropriate
- Handle errors with specific exception types
- Include docstrings for public functions
- Use type hints consistently

## Running Scripts

```bash
# Run with uv (auto-installs dependencies)
uv run scripts/script_name.py

# Or make executable
chmod +x scripts/script_name.py
./scripts/script_name.py
```
