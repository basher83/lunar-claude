# Security Patterns for uv Scripts

This document covers security best practices for uv scripts, following the lunar-claude repository patterns.

## Never Hardcode Secrets

### ❌ WRONG - Hardcoded Secrets

```python
# NEVER DO THIS
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "super_secret"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Why**: Secrets in code can be:

- Committed to version control
- Exposed in logs
- Shared accidentally
- Difficult to rotate

## Environment Variables (Good)

### ✅ Basic Pattern

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Script using environment variables for secrets."""

import os
import sys

def get_required_env(name: str) -> str:
    """Get required environment variable or exit with error."""
    value = os.getenv(name)
    if not value:
        print(f"Error: {name} environment variable not set", file=sys.stderr)
        sys.exit(1)
    return value

def main():
    api_key = get_required_env("API_KEY")
    database_url = get_required_env("DATABASE_URL")

    # Use secrets
    # ...

if __name__ == "__main__":
    main()
```

**Usage**:

```bash
export API_KEY="your-key-here"
export DATABASE_URL="postgresql://..."
python script.py
```

## Infisical Integration (Best - Following Repo Pattern)

### ✅ Recommended Pattern

Following the lunar-claude repository's approach to secrets management:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "infisical-python>=2.3.3",
# ]
# ///
"""Script using Infisical for secrets management."""

from infisical import InfisicalClient
import sys

def get_secret(client: InfisicalClient, key: str, path: str = "/") -> str:
    """Get secret from Infisical or exit with error."""
    try:
        secret = client.get_secret(key, path=path)
        return secret.secret_value
    except Exception as e:
        print(f"Error fetching secret {key}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Initialize Infisical client
    # Requires INFISICAL_TOKEN environment variable
    client = InfisicalClient()

    # Fetch secrets
    api_key = get_secret(client, "API_KEY", path="/production")
    db_password = get_secret(client, "DATABASE_PASSWORD", path="/production")

    # Use secrets
    # ...

if __name__ == "__main__":
    main()
```

**Setup**:

```bash
export INFISICAL_TOKEN="your-infisical-token"
python script.py
```

**Benefits**:

- Centralized secrets management
- Audit trails
- Secret rotation without code changes
- Team collaboration
- Environment-specific secrets (dev/staging/prod)

## Input Validation

### Validate All External Input

```python
import re
import sys
from pathlib import Path

def validate_ip_address(ip: str) -> bool:
    """Validate IP address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False

    # Check each octet is 0-255
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

def validate_file_path(path_str: str) -> Path:
    """Validate and resolve file path."""
    try:
        path = Path(path_str).resolve()

        # Prevent path traversal
        if '..' in path.parts:
            raise ValueError("Path traversal detected")

        # Check file exists
        if not path.exists():
            raise ValueError(f"File not found: {path}")

        return path

    except Exception as e:
        print(f"Invalid path: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Validate command-line input
    if len(sys.argv) < 2:
        print("Usage: script.py <ip-address>", file=sys.stderr)
        sys.exit(1)

    ip = sys.argv[1]
    if not validate_ip_address(ip):
        print(f"Invalid IP address: {ip}", file=sys.stderr)
        sys.exit(1)

    # Safe to use
    print(f"Valid IP: {ip}")
```

## Secure HTTP Requests

### Verify SSL Certificates

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///
"""Secure HTTP requests with proper SSL verification."""

import httpx
import sys

def fetch_data(url: str, api_key: str):
    """Fetch data with SSL verification and timeouts."""
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        with httpx.Client(
            verify=True,      # ✓ Verify SSL certificates
            timeout=10.0,     # ✓ Set reasonable timeout
        ) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}", file=sys.stderr)
        # Don't expose response body in logs (might contain secrets)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Request failed: {type(e).__name__}", file=sys.stderr)
        sys.exit(1)
```

### When to Disable SSL Verification

**Only for internal/development scenarios**:

```python
import httpx
import os

def fetch_internal_api(url: str):
    """Fetch from internal API (development only)."""
    # Check we're in development environment
    if os.getenv("ENVIRONMENT") != "development":
        raise RuntimeError("SSL verification bypass only allowed in development")

    # Explicitly disable verification for internal self-signed certs
    with httpx.Client(verify=False) as client:
        response = client.get(url)
        return response.json()
```

## Sensitive Data in Logs

### Don't Log Secrets

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_api_request(api_key: str, user_id: str):
    """Process API request without logging secrets."""

    # ❌ WRONG
    logger.info(f"Making request with API key: {api_key}")

    # ✓ CORRECT
    logger.info(f"Making request for user: {user_id}")

    # ✓ CORRECT - Masked secret
    logger.debug(f"API key: {api_key[:8]}...")
```

## File Permissions

### Restrict Permissions on Sensitive Files

```python
import os
from pathlib import Path

def write_credentials(file_path: Path, credentials: str):
    """Write credentials file with restricted permissions."""

    # Write file
    file_path.write_text(credentials)

    # Set permissions to 0600 (owner read/write only)
    os.chmod(file_path, 0o600)

    print(f"Credentials written to {file_path} (permissions: 600)")
```

## Subprocess Security

### Avoid Shell Injection

```python
import subprocess
import sys

def run_command_safe(command: list[str]):
    """Execute command safely without shell injection."""

    # ✓ CORRECT - List format, no shell
    try:
        result = subprocess.run(
            command,              # List, not string
            shell=False,          # No shell interpretation
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        sys.exit(1)

# Usage
run_command_safe(["ls", "-la", "/tmp"])  # ✓ Safe

# ❌ WRONG - Shell injection risk
# subprocess.run(f"ls -la {user_input}", shell=True)
```

## Summary - Security Checklist

Before deploying a uv script, verify:

- [ ] No hardcoded secrets in code
- [ ] Secrets loaded from environment variables or Infisical
- [ ] All external input validated
- [ ] SSL verification enabled for HTTPS requests
- [ ] Secrets not logged or exposed in error messages
- [ ] File permissions restricted for sensitive files (0600)
- [ ] subprocess calls use list format with shell=False
- [ ] Timeout set on all network requests
- [ ] Error messages don't expose sensitive data

## References

- **Infisical Documentation**: <https://infisical.com/docs>
- **OWASP Top 10**: <https://owasp.org/www-project-top-ten/>
- **Python Security Best Practices**: <https://python.readthedocs.io/en/latest/library/security_warnings.html>
