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
    pattern: uv run|uv pip
---

**Use `uv` instead of direct python/pip/pytest commands.**

| Instead of | Use |
|------------|-----|
| `python script.py` | `uv run script.py` |
| `python3.11 script.py` | `uv run script.py` |
| `python -m pytest` | `uv run pytest` |
| `pytest` | `uv run pytest` |
| `pip install package` | `uv add package` |
| `pip install -r requirements.txt` | `uv sync` |
