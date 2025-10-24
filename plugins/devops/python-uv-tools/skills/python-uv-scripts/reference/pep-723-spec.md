# PEP 723: Inline Script Metadata Specification

Complete reference for PEP 723 inline script metadata format used by uv.

## Overview

PEP 723 defines a standardized way to embed dependency and configuration metadata directly within Python script files. This eliminates the need for separate `requirements.txt` files and enables self-contained, reproducible scripts.

## Basic Format

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "package-name>=1.0.0",
# ]
# ///
```

**Key Requirements:**
- Must appear as comments (`#`)
- Must use `# /// script` as opening marker
- Must use `# ///` as closing marker
- Must be valid TOML syntax
- Recommended placement: After shebang, before module docstring

## Complete Specification

### Required Fields

#### requires-python

Specifies minimum Python version:

```python
# /// script
# requires-python = ">=3.11"
# ///
```

**Formats:**
```python
requires-python = ">=3.11"      # Minimum version
requires-python = ">=3.11,<3.13" # Version range
requires-python = "==3.12"       # Exact version
```

#### dependencies

Lists required packages:

```python
# /// script
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
#   "typer~=0.9.0",
# ]
# ///
```

**Version Specifiers:**
```python
"package"           # Any version
"package>=1.0"      # Minimum version
"package>=1.0,<2.0" # Version range
"package~=1.2.3"    # Compatible release (1.2.x)
"package==1.2.3"    # Exact version
```

### Optional Fields

#### [tool.uv] Section

uv-specific configuration:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
#
# [tool.uv]
# exclude-newer = "2024-10-01T00:00:00Z"
# index-url = "https://pypi.org/simple"
# ///
```

**Available options:**
- `exclude-newer`: Only use packages published before this date
- `index-url`: Alternative PyPI index
- `extra-index-url`: Additional package indexes
- `find-links`: Additional package sources
- `no-index`: Ignore PyPI entirely

#### [tool.uv.sources]

Custom package sources:

```python
# /// script
# dependencies = ["my-package"]
#
# [tool.uv.sources]
# my-package = { git = "https://github.com/user/repo", tag = "v1.0" }
# ///
```

#### [tool.uv.metadata]

Custom metadata (not part of PEP 723, but useful for teams):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
#
# [tool.uv.metadata]
# purpose = "cluster-monitoring"
# team = "infrastructure"
# author = "devops@example.com"
# created = "2024-10-20"
# ///
```

## Complete Examples

### Minimal Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Simple script with no dependencies"""

print("Hello, world!")
```

### Production Script

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
#   "typer>=0.9.0",
# ]
#
# [tool.uv]
# exclude-newer = "2024-10-01T00:00:00Z"
#
# [tool.uv.metadata]
# purpose = "api-client"
# team = "infrastructure"
# author = "devops@spaceships.work"
# ///
"""
API client for Proxmox cluster monitoring

Usage:
    check_cluster.py [--node NODE] [--json]
"""

import typer
import httpx
from rich import print
```

### With Git Dependencies

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "my-internal-lib",
# ]
#
# [tool.uv.sources]
# my-internal-lib = { git = "https://github.com/org/lib.git", tag = "v1.2.3" }
# ///
```

### With Local Dependencies

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "my-local-package",
# ]
#
# [tool.uv.sources]
# my-local-package = { path = "../my-package", editable = true }
# ///
```

## Placement Guidelines

### Correct Placement

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Module docstring comes after metadata"""

import sys

def main():
    pass

if __name__ == "__main__":
    main()
```

### Multiple Metadata Blocks (Invalid)

```python
# ❌ INVALID - Only one metadata block allowed
# /// script
# requires-python = ">=3.11"
# ///

# /// script
# dependencies = ["httpx"]
# ///
```

## Validation

### Valid Metadata

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",      # Comments allowed in arrays
#   "rich",
# ]
# ///
```

### Invalid Metadata

```python
# ❌ Missing closing marker
# /// script
# requires-python = ">=3.11"

# ❌ Invalid TOML syntax
# /// script
# dependencies = httpx  # Missing quotes
# ///

# ❌ Not in comments
/// script
requires-python = ">=3.11"
///
```

## Creating Metadata

### Manual Creation

Add metadata block manually:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx
```

### Using uv init

Generate script with metadata:

```bash
uv init --script my_script.py --python 3.11
```

### Using uv add

Add dependencies to existing script:

```bash
uv add --script my_script.py httpx rich typer
```

## Validation Tools

### Check Metadata Validity

```bash
# Parse metadata
uv run --script my_script.py --dry-run

# Validate with custom tool
python tools/validate_script.py my_script.py
```

### Extract Metadata

```python
import re
import tomllib

def extract_metadata(script_path: str) -> dict:
    """Extract PEP 723 metadata from script"""
    with open(script_path) as f:
        content = f.read()

    # Find metadata block
    pattern = r'# /// script\n((?:# .*\n)+)# ///'
    match = re.search(pattern, content)

    if not match:
        return {}

    # Parse TOML (remove leading # from each line)
    toml_lines = match.group(1).split('\n')
    toml_content = '\n'.join(line[2:] for line in toml_lines if line.startswith('# '))

    return tomllib.loads(toml_content)
```

## Compatibility

### PEP 723 Support

- ✅ uv (native support)
- ✅ pip (via `pip-run`)
- ✅ pipx (v1.4.0+)
- ⚠️  Other tools (check documentation)

### Fallback for Non-Supporting Tools

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""
Fallback installation for non-PEP-723 tools:
    pip install httpx
    python script.py
"""
```

## Best Practices

1. **Always include requires-python** - Prevents compatibility issues
2. **Pin major versions** - `>=X.Y.Z` for stability
3. **Add metadata section** - Document purpose and ownership
4. **Keep dependencies minimal** - Only what's necessary
5. **Document fallbacks** - Help non-uv users
6. **Validate syntax** - Use validation tools
7. **Version consistently** - Match project conventions

## References

- [PEP 723 Specification](https://peps.python.org/pep-0723/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [TOML Specification](https://toml.io/)
- [Python Version Specifiers](https://peps.python.org/pep-0440/)
