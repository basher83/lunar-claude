# PEP 723: Inline Script Metadata

## Official Specification

This document summarizes PEP 723, the official Python specification for inline script metadata.

**Source**: <https://peps.python.org/pep-0723/>

## Valid Metadata Format

The ONLY valid metadata format for uv scripts is:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "package-name>=1.0.0",
#   "another-package~=2.0.0",
# ]
# ///
```

## Required Elements

### 1. Shebang (recommended)

```python
#!/usr/bin/env -S uv run --script
```

- Makes script directly executable
- `--script` flag tells uv to use inline metadata
- Optional `--quiet` flag suppresses uv output

### 2. Metadata Block (required for dependencies)

```python
# /// script
# [TOML content here]
# ///
```

- MUST start with `# /// script`
- MUST end with `# ///`
- Content between markers is TOML format
- Each line MUST be commented with `#`

### 3. TOML Fields

**requires-python** (optional):

```toml
requires-python = ">=3.11"
```

- Specifies minimum Python version
- Uses PEP 440 version specifiers

**dependencies** (optional):

```toml
dependencies = [
  "httpx>=0.27.0",
  "rich>=13.0.0",
]
```

- Array of package specifications
- Uses PEP 508 dependency format
- Each dependency on its own line (recommended for readability)

## Version Specifiers

**Recommended formats**:

- `>=X.Y.Z` - Minimum version (most flexible)
- `~=X.Y.Z` - Compatible release (patch updates only)
- `==X.Y.Z` - Exact version (most strict)

**Examples**:

```toml
dependencies = [
  "httpx>=0.27.0",     # Any version >= 0.27.0
  "typer~=0.9.0",      # 0.9.x versions only
  "requests==2.31.0",  # Exact version
]
```

## INVALID Metadata

**❌ THESE DO NOT WORK AND WILL CAUSE ERRORS:**

### Invalid: [tool.uv.metadata]

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# [tool.uv.metadata]        # ❌ INVALID
# purpose = "testing"
# team = "devops"
# ///
```

**Why**: `[tool.uv.metadata]` is NOT part of PEP 723 and is not supported by uv.

### Invalid: [tool.uv]

```python
# /// script
# [tool.uv]                # ❌ INVALID
# exclude-newer = "2024-01-01"
# ///
```

**Why**: Only `requires-python` and `dependencies` are valid in PEP 723 metadata blocks.

### Invalid: Custom fields

```python
# /// script
# requires-python = ">=3.11"
# author = "me"            # ❌ INVALID
# version = "1.0.0"        # ❌ INVALID
# ///
```

**Why**: PEP 723 only supports `requires-python` and `dependencies`.

## Complete Working Example

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
#   "typer>=0.9.0",
# ]
# ///
"""
Example script showing correct PEP 723 format.

Usage:
    python script.py
"""

import httpx
from rich import print
import typer

app = typer.Typer()

@app.command()
def main():
    """Main function."""
    print("[green]Hello from uv![/green]")

if __name__ == "__main__":
    app()
```

## References

- **PEP 723 Official Spec**: <https://peps.python.org/pep-0723/>
- **uv Script Guide**: <https://docs.astral.sh/uv/guides/scripts/>
- **PEP 508 (Dependency Specifiers)**: <https://peps.python.org/pep-0508/>
- **PEP 440 (Version Specifiers)**: <https://peps.python.org/pep-0440/>
