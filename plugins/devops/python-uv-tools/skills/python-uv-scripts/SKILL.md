---
name: python-uv-scripts
description: Python single-file script development using uv and PEP 723 inline metadata. Covers script creation, dependency management, self-executable scripts, testing patterns, security best practices, CI/CD integration, and when to use (or not use) single-file scripts vs projects. Use when creating standalone Python utilities, converting scripts to uv format, managing script dependencies, implementing script testing, or establishing team standards for script development.
---

# Python Single-File Scripts with uv

Expert guidance for creating production-ready, self-contained Python scripts using uv's inline dependency management (PEP 723).

## Quick Start

### Create Your First uv Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
# ]
# ///

import httpx
from rich import print

response = httpx.get("https://api.github.com")
print(f"[green]Status: {response.status_code}[/green]")
```

Make it executable:
```bash
chmod +x script.py
./script.py  # uv automatically installs dependencies
```

### Convert Existing Script

```bash
# Add inline metadata to existing script
./tools/convert_to_uv.py existing_script.py

# Validate PEP 723 metadata
./tools/validate_script.py script.py
```

## When to Use This Skill

Activate this skill when:
- Creating standalone Python utilities or automation scripts
- Converting scripts from `requirements.txt` to uv format
- Adding dependencies to existing single-file scripts
- Implementing testing for utility scripts
- Establishing team standards for script development
- Reviewing scripts for security or best practices
- Setting up CI/CD for script execution
- Creating infrastructure automation tools (like cluster health checkers)

## Core Concepts

### What is PEP 723?

**PEP 723** defines inline script metadata for Python files:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "package>=1.0.0",
# ]
# ///
```

**Benefits:**
- ✅ Dependencies live with the code
- ✅ No separate `requirements.txt`
- ✅ Reproducible execution
- ✅ Version constraints included
- ✅ Self-documenting

### uv Script Execution Modes

**Mode 1: Inline Dependencies** (Recommended for utilities)
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["httpx"]
# ///
```

**Mode 2: Project Mode** (For larger scripts)
```bash
uv run script.py  # Uses pyproject.toml
```

**Mode 3: No Dependencies**
```python
#!/usr/bin/env -S uv run
# Standard library only
```

## Real-World Examples from This Repository

### Example 1: Cluster Health Checker

See [examples/03-production-ready/check_cluster_health_enhanced.py](examples/03-production-ready/check_cluster_health_enhanced.py)

**Current version** (basic):
```python
#!/usr/bin/env python3
import subprocess
# Manual dependency installation required
```

**Enhanced with uv** (production-ready):
```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "rich>=13.0.0",
#   "typer>=0.9.0",
# ]
# [tool.uv.metadata]
# purpose = "cluster-monitoring"
# team = "infrastructure"
# ///

import typer
from rich.console import Console
from rich.table import Table
```

### Example 2: CEPH Health Monitor

See [examples/03-production-ready/ceph_health.py](examples/03-production-ready/ceph_health.py)

Pattern: JSON API interaction with structured output

## Best Practices from This Repository

### 1. Security Patterns

**Don't hardcode secrets:**
```python
# ❌ BAD
password = "super_secret"

# ✅ GOOD - Use environment variables
import os
password = os.getenv("PROXMOX_PASSWORD")
if not password:
    raise ValueError("PROXMOX_PASSWORD not set")
```

**Better - Use keyring:**
```python
# /// script
# dependencies = ["keyring>=24.0.0"]
# ///
import keyring
password = keyring.get_password("proxmox", "api_user")
```

**Best - Use Infisical (following repository pattern):**
```python
# /// script
# dependencies = ["infisical-python>=2.3.3"]
# ///
from infisical import InfisicalClient

client = InfisicalClient()
password = client.get_secret("PROXMOX_PASSWORD", path="/matrix")
```

See [patterns/security-patterns.md](patterns/security-patterns.md) for complete guide.

### 2. Version Pinning Strategy

Following this repository's approach (from `pyproject.toml`):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",      # Minimum version for compatibility
#   "rich>=13.0.0",       # Known good version
#   "ansible>=11.1.0",    # Match project requirements
# ]
# ///
```

**Pinning levels:**
- `>=X.Y.Z` - Minimum version (most flexible)
- `~=X.Y.Z` - Compatible release (patch updates only)
- `==X.Y.Z` - Exact version (most strict)

See [reference/dependency-management.md](reference/dependency-management.md).

### 3. Team Standards

**File naming:**
```bash
check_cluster_health.py    # ✅ Descriptive, snake_case
validate_template.py       # ✅ Action-oriented
cluster.py                 # ❌ Too generic
```

**Shebang pattern:**
```python
#!/usr/bin/env -S uv run --script --quiet
# --quiet suppresses uv's own output
```

**Documentation template:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# [tool.uv.metadata]
# purpose = "cluster-monitoring"
# team = "infrastructure"
# author = "devops@spaceships.work"
# ///
"""
Script Purpose: Check Proxmox cluster health

Usage:
    python check_cluster_health.py [--node NODE] [--json]

Examples:
    python check_cluster_health.py --node foxtrot
    python check_cluster_health.py --json
"""
```

### 4. Error Handling Patterns

Following Ansible best practices from this repository:

```python
import sys
import subprocess

def run_command(cmd: str) -> str:
    """Execute command with proper error handling"""
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed: {cmd}", file=sys.stderr)
        print(f"  {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found: {cmd.split()[0]}", file=sys.stderr)
        sys.exit(1)
```

See [patterns/error-handling.md](patterns/error-handling.md).

### 5. Testing Patterns

**Inline testing** (for simple scripts):
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

def validate_ip(ip: str) -> bool:
    """Validate IP address format"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(pattern, ip))

# Inline tests
if __name__ == "__main__":
    import sys

    # Run tests if --test flag provided
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        assert validate_ip("192.168.1.1") == True
        assert validate_ip("256.1.1.1") == False
        print("All tests passed!")
        sys.exit(0)

    # Normal execution
    print(validate_ip("192.168.3.5"))
```

See [workflows/testing-strategies.md](workflows/testing-strategies.md).

## When NOT to Use Single-File Scripts

See [anti-patterns/when-not-to-use.md](anti-patterns/when-not-to-use.md) for details.

**Use a proper project instead when:**
- ❌ Script exceeds 500 lines
- ❌ Multiple modules/files needed
- ❌ Complex configuration management
- ❌ Requires packaging/distribution
- ❌ Shared library code across multiple scripts
- ❌ Web applications or long-running services

**Example - Too Complex for Single File:**
```python
# This should be a uv project, not a script:
# - 15+ dependencies
# - Database models
# - API routes
# - Background workers
# - Configuration management
# - Multiple environments
```

## Common Patterns

### Pattern: CLI Application

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
def hello(name: str):
    """Greet someone"""
    print(f"[green]Hello {name}![/green]")

if __name__ == "__main__":
    app()
```

See [patterns/cli-applications.md](patterns/cli-applications.md).

### Pattern: API Client

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx
import os

def get_proxmox_nodes(api_url: str, token: str):
    """Fetch Proxmox cluster nodes"""
    headers = {"Authorization": f"PVEAPIToken={token}"}

    with httpx.Client(verify=False) as client:
        response = client.get(f"{api_url}/nodes", headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    api_url = os.getenv("PROXMOX_API_URL")
    token = os.getenv("PROXMOX_TOKEN")

    nodes = get_proxmox_nodes(api_url, token)
    for node in nodes['data']:
        print(f"{node['node']}: {node['status']}")
```

See [patterns/api-clients.md](patterns/api-clients.md).

### Pattern: Data Processing

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "polars>=0.20.0",
# ]
# ///

import polars as pl
import sys

def analyze_logs(log_file: str):
    """Analyze log file for errors"""
    df = pl.read_csv(log_file)

    errors = df.filter(pl.col("level") == "ERROR")
    print(f"Total errors: {len(errors)}")

    by_component = errors.group_by("component").count()
    print("\nErrors by component:")
    print(by_component)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_logs.py <log_file>")
        sys.exit(1)

    analyze_logs(sys.argv[1])
```

See [patterns/data-processing.md](patterns/data-processing.md).

### Pattern: System Automation

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "psutil>=5.9.0",
# ]
# ///

import psutil
import sys

def check_disk_space(threshold: int = 80):
    """Check if disk usage exceeds threshold"""
    usage = psutil.disk_usage('/')
    percent = usage.percent

    if percent >= threshold:
        print(f"WARNING: Disk usage at {percent}%", file=sys.stderr)
        sys.exit(1)

    print(f"OK: Disk usage at {percent}%")

if __name__ == "__main__":
    threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    check_disk_space(threshold)
```

See [patterns/system-automation.md](patterns/system-automation.md).

## CI/CD Integration

### GitHub Actions

```yaml
name: Run Health Checks

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Check cluster health
        run: |
          uv run --script tools/check_cluster_health.py --json
        env:
          PROXMOX_TOKEN: ${{ secrets.PROXMOX_TOKEN }}
```

### GitLab CI

```yaml
cluster-health:
  image: ghcr.io/astral-sh/uv:python3.11-bookworm-slim
  script:
    - uv run --script tools/check_cluster_health.py
  only:
    - schedules
```

See [workflows/ci-cd-integration.md](workflows/ci-cd-integration.md).

## Tools Available

### Script Validation

```bash
# Validate PEP 723 metadata
./tools/validate_script.py script.py

# Output:
# ✓ Valid PEP 723 metadata
# ✓ Python version specified
# ✓ Dependencies properly formatted
```

### Script Conversion

```bash
# Convert requirements.txt-based script to uv
./tools/convert_to_uv.py old_script.py

# Creates:
# - old_script_uv.py with inline dependencies
# - Preserves original script
```

### Dependency Linting

```bash
# Check for security issues in dependencies
./tools/lint_dependencies.py script.py

# Output:
# ⚠ httpx: CVE-2024-1234 (update to >=0.27.2)
# ✓ rich: No known vulnerabilities
```

## Progressive Disclosure

For deeper knowledge:

### Reference Documentation
- [PEP 723 Specification](reference/pep-723-spec.md) - Complete inline metadata spec
- [Dependency Management](reference/dependency-management.md) - Version pinning strategies
- [Security Patterns](reference/security-patterns.md) - Secrets, validation, input sanitization

### Pattern Guides
- [CLI Applications](patterns/cli-applications.md) - Typer, Click, argparse patterns
- [API Clients](patterns/api-clients.md) - httpx, requests, authentication
- [Data Processing](patterns/data-processing.md) - Polars, pandas, analysis
- [System Automation](patterns/system-automation.md) - psutil, subprocess, system admin
- [Error Handling](patterns/error-handling.md) - Exception handling, logging

### Working Examples
- [NetBox API Client](examples/04-api-clients/netbox_client.py) - Production-ready API client with Infisical, validation, error handling, and Rich output
- [Examples README](examples/README.md) - Complete examples directory with progressive complexity

### Anti-Patterns
- [When NOT to Use](anti-patterns/when-not-to-use.md) - Signs you need a proper project
- [Common Mistakes](anti-patterns/common-mistakes.md) - Pitfalls and how to avoid them

### Workflows
- [Team Adoption](workflows/team-adoption.md) - Rolling out uv scripts across teams
- [CI/CD Integration](workflows/ci-cd-integration.md) - GitHub Actions, GitLab CI
- [Testing Strategies](workflows/testing-strategies.md) - Inline tests, pytest integration

## Related Skills

- **Ansible Best Practices** - Many Ansible modules could be standalone uv scripts
- **Proxmox Infrastructure** - Validation tools use this pattern
- **NetBox + PowerDNS Integration** - API interaction scripts

## Quick Reference

### Shebang Options

```python
# Standard script execution
#!/usr/bin/env -S uv run --script

# Quiet mode (suppress uv output)
#!/usr/bin/env -S uv run --script --quiet

# With Python version
#!/usr/bin/env -S uv run --script --python 3.11
```

### Common Dependencies

```python
# CLI applications
"typer>=0.9.0"        # Modern CLI framework
"click>=8.0.0"        # Alternative CLI framework
"rich>=13.0.0"        # Rich text and formatting

# API clients
"httpx>=0.27.0"       # Modern async HTTP client
"requests>=2.31.0"    # Traditional HTTP client

# Data processing
"polars>=0.20.0"      # Fast dataframe library
"pandas>=2.0.0"       # Traditional dataframe library

# Infrastructure
"ansible>=11.1.0"     # Automation (from this repo)
"infisical-python>=2.3.3"  # Secrets (from this repo)

# System automation
"psutil>=5.9.0"       # System monitoring
```

### Metadata Template

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   # Add dependencies here
# ]
# [tool.uv.metadata]
# purpose = "describe-purpose"
# team = "team-name"
# author = "email@example.com"
# ///
"""
One-line description

Usage:
    python script.py [OPTIONS]

Examples:
    python script.py --help
"""
```

## Best Practices Summary

1. **Always specify Python version** - `requires-python = ">=3.11"`
2. **Pin dependencies appropriately** - Use `>=X.Y.Z` for utilities
3. **Add metadata** - Use `[tool.uv.metadata]` for team info
4. **Include docstrings** - Document purpose and usage
5. **Handle errors gracefully** - Use try/except with clear messages
6. **Validate inputs** - Check arguments before processing
7. **Use quiet mode** - `--quiet` flag for production scripts
8. **Keep it focused** - Single file, single purpose
9. **Test inline** - Add `--test` flag for simple validation
10. **Secure secrets** - Never hardcode, use env vars or keyring
