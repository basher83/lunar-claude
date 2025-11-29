---
name: require-uv
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: (^|;\s*|&&\s*|\|\|\s*)(python3?(?:\.\d+)?(?:\s+-m\s+\w+)?|pip3?|pytest)\b
  - field: command
    operator: not_contains
    pattern: uv run
---

⛔ **Use `uv run` instead of direct python/pip/pytest commands.**

Examples:

- `uv run python` instead of `python`
- `uv run python -m py_compile` instead of `python3 -m py_compile`
- `uv run pytest` instead of `pytest`
- `uv pip install` instead of `pip install`
