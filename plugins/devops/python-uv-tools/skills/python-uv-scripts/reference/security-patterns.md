# Security Patterns for uv Scripts

Security best practices for Python single-file scripts following Virgo-Core patterns.

## Never Hardcode Secrets

### ❌ Anti-Pattern: Hardcoded Secrets

```python
# NEVER DO THIS
API_KEY = "sk_live_1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"
PROXMOX_PASSWORD = "admin123"
```

**Risks:**
- Secrets exposed in version control
- No audit trail
- Difficult to rotate
- Same credentials across environments

### ✅ Pattern 1: Environment Variables

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import os
import sys

def get_secret(name: str, required: bool = True) -> str:
    """Get secret from environment"""
    value = os.getenv(name)

    if required and not value:
        print(f"Error: {name} environment variable not set", file=sys.stderr)
        sys.exit(1)

    return value

# Usage
PROXMOX_PASSWORD = get_secret("PROXMOX_PASSWORD")
API_URL = get_secret("PROXMOX_API_URL")
```

**Usage:**
```bash
export PROXMOX_PASSWORD="$(cat ~/.secrets/proxmox_pass)"
./script.py
```

### ✅ Pattern 2: Keyring Integration

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "keyring>=24.0.0",
# ]
# ///

import keyring
import sys

def get_password(service: str, username: str) -> str:
    """Get password from system keyring"""
    password = keyring.get_password(service, username)

    if not password:
        print(f"Error: No password found for {username}@{service}", file=sys.stderr)
        print(f"Set with: keyring set {service} {username}", file=sys.stderr)
        sys.exit(1)

    return password

# Usage
proxmox_password = get_password("proxmox", "terraform@pam")
```

**Setup:**
```bash
# Store password in system keyring
keyring set proxmox terraform@pam
# Prompts for password, stores securely

# Run script (no password in environment)
./script.py
```

### ✅ Pattern 3: Infisical Integration (Repository Standard)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "infisical-python>=2.3.3",
# ]
# ///

from infisical import InfisicalClient
import os
import sys

def get_infisical_secret(
    secret_name: str,
    project_id: str,
    environment: str = "prod",
    path: str = "/"
) -> str:
    """Get secret from Infisical vault"""
    try:
        client = InfisicalClient()
        secret = client.get_secret(
            secret_name=secret_name,
            project_id=project_id,
            environment=environment,
            path=path
        )
        return secret.secret_value
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}", file=sys.stderr)
        sys.exit(1)

# Usage (following Virgo-Core pattern)
PROXMOX_PASSWORD = get_infisical_secret(
    secret_name="PROXMOX_PASSWORD",
    project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
    environment="prod",
    path="/matrix"
)
```

**Setup:**
```bash
# Authenticate with Infisical
infisical login

# Run script (secrets fetched automatically)
./script.py
```

## Input Validation

### ❌ Anti-Pattern: No Validation

```python
import subprocess

# DANGEROUS - Command injection risk
def ping_host(hostname: str):
    subprocess.run(f"ping -c 3 {hostname}", shell=True)

# User provides: "localhost; rm -rf /"
ping_host(sys.argv[1])  # 💥 System destroyed
```

### ✅ Pattern: Validate All Inputs

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import re
import sys
import subprocess

def validate_hostname(hostname: str) -> bool:
    """Validate hostname format"""
    # Only allow alphanumeric, dots, hyphens
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]$'
    if not re.match(pattern, hostname):
        return False

    # Max length check
    if len(hostname) > 253:
        return False

    return True

def ping_host(hostname: str):
    """Safely ping a host"""
    if not validate_hostname(hostname):
        print(f"Error: Invalid hostname: {hostname}", file=sys.stderr)
        sys.exit(1)

    # Use list form (no shell injection)
    result = subprocess.run(
        ["ping", "-c", "3", hostname],
        capture_output=True,
        text=True
    )

    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ping_host.py <hostname>", file=sys.stderr)
        sys.exit(1)

    ping_host(sys.argv[1])
```

### Input Validation Patterns

```python
import re
from ipaddress import IPv4Address, AddressValueError

def validate_ip(ip: str) -> bool:
    """Validate IPv4 address"""
    try:
        IPv4Address(ip)
        return True
    except AddressValueError:
        return False

def validate_port(port: int) -> bool:
    """Validate TCP/UDP port number"""
    return 1 <= port <= 65535

def validate_vmid(vmid: int) -> bool:
    """Validate Proxmox VMID (100-999999999)"""
    return 100 <= vmid <= 999999999

def validate_path(path: str) -> bool:
    """Validate file path (no directory traversal)"""
    # Reject paths with ../
    if ".." in path:
        return False

    # Reject absolute paths
    if path.startswith("/"):
        return False

    return True
```

## Dependency Security

### Pin Dependencies

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",      # ✅ Minimum version pinned
#   "rich>=13.0.0",       # ✅ Known good version
# ]
# ///
```

**Why pin?**
- Prevents automatic upgrades with vulnerabilities
- Ensures reproducible execution
- Allows controlled dependency updates

### Exclude Recent Packages

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27.0"]
#
# [tool.uv]
# exclude-newer = "2024-10-01T00:00:00Z"  # Only packages before this date
# ///
```

**Use cases:**
- Prevent supply chain attacks from compromised packages
- Freeze dependencies at known-good state
- Reproducible builds in CI/CD

### Check for Vulnerabilities

```bash
# Use safety or pip-audit
uv pip install safety
safety check --json

# Or use built-in tools
uv pip list --format json | jq '.[] | select(.name == "httpx")'
```

## File Operations Security

### ❌ Anti-Pattern: Unsafe File Access

```python
# DANGEROUS - Path traversal vulnerability
def read_log(filename: str):
    with open(f"/var/log/{filename}") as f:
        return f.read()

# User provides: "../../../etc/passwd"
read_log(sys.argv[1])  # 💥 Reads /etc/passwd
```

### ✅ Pattern: Safe File Operations

```python
import os
import sys
from pathlib import Path

def safe_read_log(filename: str, log_dir: str = "/var/log") -> str:
    """Safely read log file"""
    # Resolve to absolute paths
    log_dir_path = Path(log_dir).resolve()
    file_path = (log_dir_path / filename).resolve()

    # Ensure file is within log directory
    try:
        file_path.relative_to(log_dir_path)
    except ValueError:
        print(f"Error: Path traversal detected: {filename}", file=sys.stderr)
        sys.exit(1)

    # Check file exists and is readable
    if not file_path.exists():
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)

    if not file_path.is_file():
        print(f"Error: Not a file: {filename}", file=sys.stderr)
        sys.exit(1)

    # Read with size limit
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    if file_path.stat().st_size > MAX_SIZE:
        print(f"Error: File too large: {filename}", file=sys.stderr)
        sys.exit(1)

    with open(file_path) as f:
        return f.read()
```

## Command Execution Security

### ❌ Anti-Pattern: Shell Injection

```python
# DANGEROUS
import subprocess

def list_directory(path: str):
    subprocess.run(f"ls -la {path}", shell=True)

# User provides: "; rm -rf /"
list_directory(sys.argv[1])  # 💥 Disaster
```

### ✅ Pattern: Safe Command Execution

```python
import subprocess
import sys

def list_directory(path: str):
    """Safely list directory contents"""
    # Validate path first
    if not validate_path(path):
        print(f"Error: Invalid path: {path}", file=sys.stderr)
        sys.exit(1)

    # Use list form (no shell)
    try:
        result = subprocess.run(
            ["ls", "-la", path],
            capture_output=True,
            text=True,
            check=True,
            timeout=5  # Prevent hanging
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Command timed out", file=sys.stderr)
        sys.exit(1)
```

## Logging and Audit

### Secure Logging

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "structlog>=24.0.0",
# ]
# ///

import structlog
import sys

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
)

log = structlog.get_logger()

def process_data(user_id: int, action: str):
    """Process user action with audit logging"""
    log.info(
        "user_action",
        user_id=user_id,
        action=action,
        # Don't log sensitive data!
    )

    # ... processing logic ...

    log.info(
        "action_completed",
        user_id=user_id,
        action=action,
        status="success"
    )
```

### Never Log Secrets

```python
# ❌ BAD - Logs password
log.info(f"Connecting with password: {password}")

# ✅ GOOD - No sensitive data
log.info("Connecting to API", endpoint=api_url)

# ✅ GOOD - Masked credentials
log.info("Authentication successful", user=username)
```

## Network Security

### HTTPS Only

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["httpx>=0.27.0"]
# ///

import httpx
import sys

def fetch_api(url: str) -> dict:
    """Fetch data from API (HTTPS only)"""
    # Validate HTTPS
    if not url.startswith("https://"):
        print("Error: Only HTTPS URLs allowed", file=sys.stderr)
        sys.exit(1)

    with httpx.Client(verify=True) as client:  # Verify SSL certs
        response = client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

### Certificate Verification

```python
import httpx
import certifi

# Use trusted CA bundle
client = httpx.Client(verify=certifi.where())

# For internal CAs, specify cert path
client = httpx.Client(verify="/path/to/internal-ca.pem")

# ONLY disable for development (never in production)
if os.getenv("DEVELOPMENT") == "true":
    client = httpx.Client(verify=False)
```

## Security Checklist

Before deploying a script:

- [ ] No hardcoded secrets
- [ ] Secrets from environment/keyring/Infisical
- [ ] All inputs validated
- [ ] No shell=True in subprocess
- [ ] File paths checked for traversal
- [ ] Dependencies pinned
- [ ] No sensitive data in logs
- [ ] HTTPS for network requests
- [ ] Certificate verification enabled
- [ ] Timeouts on external calls
- [ ] Error messages don't leak information
- [ ] Principle of least privilege applied

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Infisical Python SDK](https://infisical.com/docs/sdks/languages/python)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- Virgo-Core Infisical integration: [../../ansible/tasks/infisical-secret-lookup.yml](../../ansible/tasks/infisical-secret-lookup.yml)
