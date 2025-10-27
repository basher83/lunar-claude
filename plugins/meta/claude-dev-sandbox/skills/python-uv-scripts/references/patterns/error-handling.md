# Error Handling Patterns

Best practices for error handling in uv scripts.

## Exit Codes

Always use appropriate exit codes:

- `0` - Success
- `1` - General error
- `2` - Invalid usage

```python
import sys

if len(sys.argv) < 2:
    print("Usage: script.py <input>", file=sys.stderr)
    sys.exit(2)  # Invalid usage

try:
    result = process()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)  # General error

# Success
sys.exit(0)
```

## Try-Except Pattern

```python
import sys

def main():
    try:
        # Operations that might fail
        data = fetch_data()
        result = process(data)
        save(result)

    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Invalid data: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## HTTP Error Handling

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx
import sys

try:
    response = httpx.get("https://api.example.com", timeout=10.0)
    response.raise_for_status()
    data = response.json()

except httpx.HTTPStatusError as e:
    print(f"HTTP {e.response.status_code} error", file=sys.stderr)
    sys.exit(1)

except httpx.RequestError as e:
    print(f"Request failed: {type(e).__name__}", file=sys.stderr)
    sys.exit(1)

except httpx.TimeoutException:
    print("Request timed out", file=sys.stderr)
    sys.exit(1)
```

## File Operation Errors

```python
from pathlib import Path
import sys

def read_config(path: Path):
    """Read configuration file with error handling."""
    try:
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")

        if not path.is_file():
            raise ValueError(f"Not a file: {path}")

        return path.read_text()

    except PermissionError:
        print(f"Permission denied: {path}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Error reading config: {e}", file=sys.stderr)
        sys.exit(1)
```

## Subprocess Errors

```python
import subprocess
import sys

try:
    result = subprocess.run(
        ["command", "arg"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)

except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
    print(f"Error output: {e.stderr}", file=sys.stderr)
    sys.exit(1)

except FileNotFoundError:
    print("Command not found", file=sys.stderr)
    sys.exit(1)
```

## Validation Errors

```python
import sys

def validate_input(value: str) -> int:
    """Validate and convert input."""
    if not value:
        print("Error: Empty value", file=sys.stderr)
        sys.exit(2)

    try:
        number = int(value)
    except ValueError:
        print(f"Error: Not a number: {value}", file=sys.stderr)
        sys.exit(2)

    if number < 0:
        print("Error: Must be non-negative", file=sys.stderr)
        sys.exit(2)

    return number
```

## Graceful Cleanup

```python
import sys
from pathlib import Path

def main():
    temp_file = Path("/tmp/data.tmp")

    try:
        # Create temporary file
        temp_file.write_text("data")

        # Process
        result = process(temp_file)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        # Always cleanup
        if temp_file.exists():
            temp_file.unlink()
```

## Summary

- Always write errors to `stderr`
- Use specific exception types
- Provide helpful error messages
- Use appropriate exit codes
- Clean up resources in `finally` blocks
- Don't expose secrets in error messages
