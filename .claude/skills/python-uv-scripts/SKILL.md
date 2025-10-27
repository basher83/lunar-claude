---
name: python-uv-scripts
description: Create production-ready Python scripts with uv and PEP 723. Prevents invalid patterns like [tool.uv.metadata]. Use when creating scripts, converting bash, or debugging PEP 723 errors.
---

# Python uv Scripts

Expert guidance for creating production-ready, self-contained Python scripts using uv's inline dependency management (PEP 723).

## Overview

Create Python scripts that:

- Automatically install their own dependencies
- Use only valid PEP 723 metadata (avoiding common mistakes)
- Follow security best practices
- Know when to use single-file scripts vs. proper projects

## When to Use This Skill

Activate this skill when:

- **Creating new uv scripts** - "Create a script to check cluster health"
- **Converting bash to Python** - "Convert this bash script to a uv script"
- **Adding dependencies** - "Add httpx dependency to my script"
- **Debugging PEP 723 errors** - "Why is my uv script failing?"
- **Choosing script vs. project** - "Should this be a script or a uv project?"
- **Security patterns** - "How do I handle secrets in a uv script?"

## Quick Start: Valid PEP 723 Format

The ONLY valid metadata format is:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Script description here.

Usage:
    python script.py
"""

import httpx
from rich import print

def main():
    print("[green]Hello from uv![/green]")

if __name__ == "__main__":
    main()
```

**Critical**: Only `requires-python` and `dependencies` are valid in PEP 723 metadata blocks.

## Creating Scripts: Choose the Right Template

Based on the use case, start with an appropriate template from `assets/templates/`:

### Basic Script (No Dependencies)

Use `assets/templates/basic-script.py` for:

- Simple automation with standard library only
- File operations
- Quick utilities

### CLI Application

Use `assets/templates/cli-app.py` for:

- Command-line tools with arguments
- Subcommands
- Formatted output with tables/progress bars
- File input/output handling

### API Client

Use `assets/templates/api-client.py` for:

- HTTP requests to APIs
- Authentication with tokens
- Error handling for network calls
- JSON processing

### Data Processor

Use `assets/templates/data-processor.py` for:

- CSV/data file processing
- Data transformation
- Analysis and reporting
- Batch operations

## Critical Anti-Patterns: What NOT to Do

### ❌ NEVER Use [tool.uv.metadata]

**WRONG** - This will cause errors:

```python
# /// script
# requires-python = ">=3.11"
# [tool.uv.metadata]        # ❌ THIS DOES NOT WORK
# purpose = "testing"
# ///
```

**Error**:

```text
error: TOML parse error at line 3, column 7
unknown field `metadata`
```

**Why**: `[tool.uv.metadata]` is not part of PEP 723 and is not supported by uv.

**CORRECT** - Use Python docstrings for metadata:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Purpose: Testing automation
Team: DevOps
Author: team@example.com
"""
```

### ❌ NEVER Hardcode Secrets

**WRONG**:

```python
API_KEY = "sk-1234567890"  # ❌ NEVER DO THIS
```

**CORRECT** - Use environment variables:

```python
import os
import sys

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Error: API_KEY not set", file=sys.stderr)
    sys.exit(1)
```

**BETTER** - Use Infisical (following repo pattern):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "infisical-python>=2.3.3",
# ]
# ///

from infisical import InfisicalClient

client = InfisicalClient()
api_key = client.get_secret("API_KEY", path="/production")
```

For complete anti-patterns guide, see: `references/anti-patterns.md`

## Converting Bash Scripts to Python

### Decision Framework

**Convert when**:

- Complex logic or data processing needed
- API interactions involved
- Cross-platform compatibility required
- Better error handling needed

**Keep as bash when**:

- Simple file operations (cp, mv, mkdir)
- Heavily uses shell features
- System administration tasks
- Script works fine and won't grow

### Common Conversions

**Bash HTTP request**:

```bash
curl -X GET https://api.github.com/users/octocat
```

**Python equivalent**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx

response = httpx.get("https://api.github.com/users/octocat")
response.raise_for_status()
data = response.json()
print(f"Name: {data['name']}")
```

For complete bash-to-Python conversion guide, see: `references/bash-to-python.md`

## When NOT to Use Single-File Scripts

Use a proper uv project instead when:

- **Script exceeds 500 lines**
- **Multiple Python files needed**
- **Web application or API** (Flask/FastAPI/Django)
- **Long-running service**
- **Complex configuration** (multiple env files)
- **Shared library code** across multiple scripts
- **Heavy dependencies** (TensorFlow, PyTorch, PySpark)

### Example - Too Complex for Script

```python
# This should be a uv project:
# - 800 lines of code
# - Database models
# - API routes
# - Background workers
# - Complex configuration
# - Multiple environments
```

For complete decision criteria, see: `references/when-not-to-use.md`

## Common Patterns

### Error Handling

Always write errors to stderr and use appropriate exit codes:

```python
import sys

try:
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

For complete error handling patterns, see: `references/patterns/error-handling.md`

### CLI Applications

Use Typer for command-line tools:

```python
# /// script
# dependencies = ["typer>=0.9.0", "rich>=13.0.0"]
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

For complete CLI patterns, see: `references/patterns/cli-applications.md`

### API Clients

Use httpx for HTTP requests with proper error handling:

```python
# /// script
# dependencies = ["httpx>=0.27.0"]
# ///

import httpx
import sys

try:
    response = httpx.get("https://api.example.com", timeout=10.0)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    print(f"HTTP error {e.response.status_code}", file=sys.stderr)
    sys.exit(1)
```

For complete API client patterns, see: `references/patterns/api-clients.md`

## Security Checklist

Before deploying a uv script:

- [ ] No hardcoded secrets in code
- [ ] Secrets loaded from environment variables or Infisical
- [ ] All external input validated
- [ ] SSL verification enabled for HTTPS requests
- [ ] Secrets not logged or exposed in error messages
- [ ] subprocess calls use list format with `shell=False`
- [ ] Timeout set on all network requests
- [ ] Error messages don't expose sensitive data

For complete security patterns, see: `references/security-patterns.md`

## Valid PEP 723 Reference

Only these fields are supported:

```python
# /// script
# requires-python = ">=3.11"    # Python version constraint
# dependencies = [               # Package dependencies
#   "package-name>=1.0.0",
# ]
# ///
```

**Version specifiers**:

- `>=X.Y.Z` - Minimum version (recommended for utilities)
- `~=X.Y.Z` - Compatible release (patch updates only)
- `==X.Y.Z` - Exact version (for reproducibility)

For complete PEP 723 spec, see: `references/pep-723-spec.md`

## Working with This Skill

### Templates Available

In `assets/templates/`:

- `basic-script.py` - Minimal working example
- `cli-app.py` - Typer CLI with subcommands
- `api-client.py` - HTTP client with error handling
- `data-processor.py` - Polars data processing

### Reference Documentation

In `references/`:

- `pep-723-spec.md` - Official PEP 723 specification
- `anti-patterns.md` - Common mistakes to avoid
- `when-not-to-use.md` - Decision criteria for scripts vs. projects
- `security-patterns.md` - Security best practices
- `bash-to-python.md` - Converting bash scripts
- `examples.md` - Real-world examples
- `patterns/` - CLI, error handling, API client patterns

### Typical Workflow

1. **Choose template** from `assets/templates/` based on use case
2. **Copy template** and customize for specific needs
3. **Add dependencies** to `dependencies` array if needed
4. **Implement logic** following patterns from `references/patterns/`
5. **Handle errors** per `references/patterns/error-handling.md`
6. **Secure secrets** per `references/security-patterns.md`
7. **Test** by running: `chmod +x script.py && ./script.py`

## Common Debugging

### "unknown field" Error

```text
error: TOML parse error at line X
unknown field `metadata`
```

**Cause**: Using invalid PEP 723 fields like `[tool.uv.metadata]`
**Fix**: Remove invalid fields, use only `requires-python` and `dependencies`
**Reference**: `references/anti-patterns.md`

### Import Errors

```text
ModuleNotFoundError: No module named 'httpx'
```

**Cause**: Dependency not listed in metadata
**Fix**: Add to `dependencies` array:

```python
# /// script
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///
```

### Permission Denied

```text
Permission denied
```

**Cause**: Script not executable
**Fix**: `chmod +x script.py`

## Progressive Resources

For deeper knowledge:

- **Official PEP 723**: `references/pep-723-spec.md`
- **Anti-patterns**: `references/anti-patterns.md`
- **Security**: `references/security-patterns.md`
- **Examples**: `references/examples.md` and `ai_docs/Python-uv-Script-Examples-and-References.md`
- **Patterns**: `references/patterns/` for CLI, error handling, API clients

## Summary

**Create scripts with**:

- Valid PEP 723 format only (`requires-python`, `dependencies`)
- Environment variables or Infisical for secrets
- Proper error handling (stderr, exit codes)
- Appropriate templates from `assets/templates/`

**Avoid**:

- `[tool.uv.metadata]` or other invalid fields
- Hardcoded secrets
- Scripts for complex applications (>500 lines, web apps, services)
- Missing error handling

**When in doubt**:

- Check `references/anti-patterns.md` for what NOT to do
- Check `references/when-not-to-use.md` for script vs. project decision
- Use templates from `assets/templates/` as starting points
