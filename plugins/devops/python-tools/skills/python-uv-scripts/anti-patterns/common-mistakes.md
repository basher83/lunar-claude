# Anti-Patterns: Common Mistakes with uv Scripts

This document lists common mistakes when creating uv scripts and how to avoid them.

## Critical Mistakes

### ❌ Using [tool.uv.metadata]

**WRONG**:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# [tool.uv.metadata]        # ❌ THIS DOES NOT WORK
# purpose = "testing"
# team = "devops"
# ///
```

**Error**:

```text
error: TOML parse error at line 4, column 7
  |
4 | [tool.uv.metadata]
  |       ^^
unknown field `metadata`
```

**Why**: `[tool.uv.metadata]` is not part of PEP 723 and is not supported by uv.

**CORRECT**: Use docstrings for metadata:

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

**NOTE**: `[tool.uv]` (without `.metadata`) IS valid for fields like `exclude-newer`. See reference/pep-723-spec.md.

### ❌ Adding Custom TOML Fields

**WRONG**:

```python
# /// script
# requires-python = ">=3.11"
# author = "me"             # ❌ INVALID
# version = "1.0.0"         # ❌ INVALID
# description = "test"      # ❌ INVALID
# dependencies = []
# ///
```

**CORRECT**: Only use `requires-python` and `dependencies` at the top level:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Author: me
Version: 1.0.0
Description: test
"""
```

### ❌ Hardcoded Secrets

**WRONG**:

```python
API_KEY = "sk-1234567890abcdef"          # ❌ NEVER DO THIS
PASSWORD = "super_secret_password"        # ❌ NEVER DO THIS
```

**CORRECT**: Use environment variables:

```python
import os
import sys

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Error: API_KEY environment variable not set", file=sys.stderr)
    sys.exit(1)
```

**BETTER**: Use Infisical (following repo pattern):

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

### ❌ Missing Error Handling

**WRONG**:

```python
import httpx

response = httpx.get("https://api.example.com")  # ❌ No error handling
data = response.json()
```

**CORRECT**:

```python
import httpx
import sys

try:
    response = httpx.get("https://api.example.com", timeout=10.0)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}", file=sys.stderr)
    sys.exit(1)
except httpx.RequestError as e:
    print(f"Request failed: {e}", file=sys.stderr)
    sys.exit(1)
```

## When NOT to Use Single-File Scripts

### ❌ Complex Applications

Don't use single-file scripts when:

- **Script exceeds 500 lines** → Use a proper uv project
- **Multiple modules needed** → Use a proper uv project
- **Shared code across scripts** → Use a proper uv project with shared library
- **Web applications** → Use a proper uv project (Flask/FastAPI/Django)
- **Long-running services** → Use a proper uv project
- **Complex configuration** → Use a proper uv project with config files

**Example - Too Complex**:

```python
# This should be a uv project, not a script:
# - 15+ dependencies
# - Database models
# - API routes
# - Background workers
# - Multiple configuration files
# - 1000+ lines of code
```

### ❌ Heavy Dependencies

**WRONG**: Using heavy ML/data libraries in scripts:

```python
# /// script
# dependencies = [
#   "tensorflow>=2.15.0",     # ❌ Too heavy for script
#   "torch>=2.1.0",           # ❌ Too heavy for script
#   "transformers>=4.35.0",   # ❌ Too heavy for script
# ]
# ///
```

**Why**: These create very large environments. Use a proper project instead.

**OK**: Lightweight data processing:

```python
# /// script
# dependencies = [
#   "polars>=0.20.0",         # ✓ Reasonable for scripts
#   "httpx>=0.27.0",          # ✓ Reasonable for scripts
# ]
# ///
```

## Common Syntax Mistakes

### ❌ Missing # on TOML Lines

**WRONG**:

```python
# /// script
requires-python = ">=3.11"    # ❌ Missing # at start
dependencies = []              # ❌ Missing # at start
# ///
```

**CORRECT**:

```python
# /// script
# requires-python = ">=3.11"   # ✓ Each line starts with #
# dependencies = []             # ✓ Each line starts with #
# ///
```

### ❌ Wrong Marker Format

**WRONG**:

```python
# /// scripts                   # ❌ Wrong: "scripts" not "script"
# requires-python = ">=3.11"
# ///

# // script                     # ❌ Wrong: "//" not "///"
# requires-python = ">=3.11"
# //

# /// script                    # ❌ Wrong: No closing marker
# requires-python = ">=3.11"
```

**CORRECT**:

```python
# /// script                    # ✓ Exactly "/// script"
# requires-python = ">=3.11"
# ///                           # ✓ Exactly "///"
```

## Dependency Management Mistakes

### ❌ No Version Constraints

**WRONG**:

```python
# /// script
# dependencies = [
#   "httpx",                    # ❌ No version specified
#   "requests",                 # ❌ Could break unexpectedly
# ]
# ///
```

**CORRECT**:

```python
# /// script
# dependencies = [
#   "httpx>=0.27.0",           # ✓ Minimum version specified
#   "requests>=2.31.0",        # ✓ Prevents breaking changes
# ]
# ///
```

### ❌ Overly Strict Pinning

**WRONG** (for utility scripts):

```python
# /// script
# dependencies = [
#   "httpx==0.27.0",           # ❌ Too strict, prevents updates
#   "rich==13.7.0",            # ❌ Blocks security fixes
# ]
# ///
```

**CORRECT**:

```python
# /// script
# dependencies = [
#   "httpx>=0.27.0",           # ✓ Allows updates
#   "rich>=13.0.0",            # ✓ Allows security fixes
# ]
# ///
```

**NOTE**: Exact pinning (`==`) is appropriate for deployment scripts where reproducibility is critical.

## Additional Pitfalls

### ❌ Missing Shebang

**WRONG**:

```python
# No shebang - script won't be directly executable
# /// script
# dependencies = ["requests"]
# ///
```

**CORRECT**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
```

### ❌ Broad Exception Handling

**WRONG**:

```python
try:
    do_something()
except Exception:  # Too broad!
    pass
```

**CORRECT**:

```python
try:
    do_something()
except (FileNotFoundError, PermissionError) as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### ❌ Platform-Specific Code Without Guards

**WRONG**:

```python
import pwd  # Unix-only, crashes on Windows
user = pwd.getpwuid(os.getuid())
```

**CORRECT**:

```python
import sys
if sys.platform != "win32":
    import pwd
    user = pwd.getpwuid(os.getuid())
else:
    user = os.environ.get("USERNAME")
```

## Summary

**Never use**:

- `[tool.uv.metadata]` (invalid field)
- Custom fields in PEP 723 metadata (only `requires-python` and `dependencies`)
- Hardcoded secrets
- Scripts for complex applications (>500 lines, web apps, services)

**Always use**:

- Valid PEP 723 format only
- `[tool.uv]` (without `.metadata`) for valid fields like `exclude-newer`
- Environment variables or Infisical for secrets
- Error handling for external calls
- Version constraints on dependencies
- Proper projects when scripts become too complex
