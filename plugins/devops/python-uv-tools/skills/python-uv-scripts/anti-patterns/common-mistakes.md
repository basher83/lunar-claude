# Common Mistakes and Pitfalls

> **Status**: ✅ Ready (ongoing enhancement planned - see TODO section)

## Overview

Common mistakes when writing UV single-file scripts and how to avoid them.

## Common Pitfalls

### 1. Missing Shebang or Incorrect Format

❌ **Wrong**:

```python
# No shebang - script won't be directly executable
# /// script
# dependencies = ["requests"]
# ///
```

✅ **Correct**:

```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["requests"]
# ///
```

### 2. Hardcoded Credentials

❌ **Wrong**:

```python
API_KEY = "sk-PLACEHOLDER-NEVER-HARDCODE"  # NEVER do this!
```

✅ **Correct**:

```python
from infisical import InfisicalClient
client = InfisicalClient()
api_key = client.get_secret("API_KEY", path="/prod")
```

### 3. No Error Handling

❌ **Wrong**:

```python
data = requests.get(url).json()  # Will crash on network error
```

✅ **Correct**:

```python
try:
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 4. Broad Exception Handling

❌ **Wrong**:

```python
try:
    do_something()
except Exception:  # Too broad!
    pass
```

✅ **Correct**:

```python
try:
    do_something()
except (FileNotFoundError, PermissionError) as e:
    console.print(f"[red]Error: {e}[/red]")
    sys.exit(1)
```

### 5. No Version Pinning

❌ **Wrong**:

```python
# /// script
# dependencies = ["requests"]  # Any version - breaks unpredictably
# ///
```

✅ **Correct**:

```python
# /// script
# dependencies = ["requests>=2.31.0"]
# ///
```

### 6. Platform-Specific Code Without Guards

❌ **Wrong**:

```python
import pwd  # Unix-only, crashes on Windows
user = pwd.getpwuid(os.getuid())
```

✅ **Correct**:

```python
import sys
if sys.platform != "win32":
    import pwd
    user = pwd.getpwuid(os.getuid())
else:
    user = os.environ.get("USERNAME")
```

## TODO

This file will be expanded to include:

- Complete checklist of common mistakes
- Detailed explanations and fixes
- Code review guidelines
- Linting rules to catch issues
