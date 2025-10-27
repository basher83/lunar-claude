# Real-World uv Script Examples

This document references production-ready examples of uv scripts from the community.

For comprehensive examples and references, see: `ai_docs/Python-uv-Script-Examples-and-References.md`

## Quick Reference Examples

### Minimal Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

def main():
    print("Hello from uv!")

if __name__ == "__main__":
    main()
```

### CLI Tool with Typer

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///

import typer
from rich import print

app = typer.Typer()

@app.command()
def greet(name: str):
    print(f"[green]Hello, {name}![/green]")

if __name__ == "__main__":
    app()
```

### HTTP Client

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx

response = httpx.get("https://api.github.com")
print(f"Status: {response.status_code}")
```

### Data Processing

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "polars>=0.20.0",
# ]
# ///

import polars as pl

df = pl.read_csv("data.csv")
print(df.describe())
```

## Community Examples

For detailed real-world examples, see research document at:
`ai_docs/Python-uv-Script-Examples-and-References.md`

**Key resources from that document**:

1. **PyBites Tutorial** - Project-less utilities with Google Books API, YouTube transcripts
2. **Trey Hunner** - Video normalization, screen recording captions
3. **GitHub Repositories**:
   - gdamjan/uv-getting-started - Complete project template
   - fedragon/uv-workspace-example - Workspace functionality
   - fpgmaas/cookiecutter-uv-example - Template repository

4. **Production Patterns**:
   - CLI applications with command-line parsing
   - API integrations (OpenAI, GitHub, Google Books)
   - Data processing and transformation
   - File processing automation

## Templates in This Skill

See `assets/templates/` for ready-to-use templates:

- `basic-script.py` - Minimal working example
- `cli-app.py` - Typer CLI pattern
- `api-client.py` - HTTP client with error handling
- `data-processor.py` - Polars data processing

## Common Patterns

### Error Handling

```python
import sys

try:
    # Operation that might fail
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Environment Variables

```python
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Error: API_KEY not set", file=sys.stderr)
    sys.exit(1)
```

### File Operations

```python
from pathlib import Path

config_file = Path("config.yaml")
if config_file.exists():
    content = config_file.read_text()
```

### Subprocess Calls

```python
import subprocess

result = subprocess.run(
    ["command", "arg1", "arg2"],
    capture_output=True,
    text=True,
    check=True
)
print(result.stdout)
```

## Where to Find More Examples

1. **Official uv docs**: <https://docs.astral.sh/uv/guides/scripts/>
2. **PEP 723 spec**: <https://peps.python.org/pep-0723/>
3. **This repository's research**: `ai_docs/Python-uv-Script-Examples-and-References.md`
4. **This skill's templates**: `assets/templates/`

## Testing Your Scripts

Run scripts with:

```bash
# Make executable
chmod +x script.py

# Run directly
./script.py

# Or with uv explicitly
uv run --script script.py
```

Verify metadata with:

```bash
# uv will show errors for invalid metadata
uv run --script script.py
```
