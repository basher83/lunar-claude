---
name: python-uv-scripts
description: >
  Python single-file script development using uv and PEP 723 inline metadata.
  Prevents invalid patterns like [tool.uv.metadata].
  Use when creating standalone Python utilities, converting scripts to uv format,
  managing script dependencies, implementing script testing,
  or establishing team standards for script development.
---

# Python Single-File Scripts with uv

Expert guidance for creating production-ready, self-contained Python scripts using uv's inline dependency management
(PEP 723).

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

### Mode 3: No Dependencies

```python
#!/usr/bin/env -S uv run
# Standard library only
```

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

**Valid `tool.uv` fields** (if needed):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# [tool.uv]
# exclude-newer = "2025-01-01T00:00:00Z"  # For reproducibility
# ///
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
# ///
"""
Purpose: Cluster health monitoring
Team: Infrastructure
"""

import typer
from rich.console import Console
from rich.table import Table
```

### Example 2: CEPH Health Monitor

See [examples/03-production-ready/ceph_health.py](examples/03-production-ready/ceph_health.py)

Pattern: JSON API interaction with structured output

## Best Practices from This Repository

### 1. Security Patterns

See [reference/security-patterns.md](reference/security-patterns.md) for complete security guide including:

- Secrets management (environment variables, keyring, Infisical)
- Input validation
- Dependency security
- File operations security
- Command execution security

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
# ///
"""
Check Proxmox cluster health

Purpose: cluster-monitoring
Team: infrastructure
Author: devops@spaceships.work

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

See pattern guides for complete examples:

- [CLI Applications](patterns/cli-applications.md) - Typer, Click, argparse patterns
- [API Clients](patterns/api-clients.md) - httpx, requests, authentication
- [Data Processing](patterns/data-processing.md) - Polars, pandas, analysis
- [System Automation](patterns/system-automation.md) - psutil, subprocess, system admin

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

> **Note:** See [Common Patterns](#common-patterns) section above for quick access to these guides.

### Working Examples

- [NetBox API Client](examples/04-api-clients/netbox_client.py) - Production-ready API client with Infisical, validation, error handling, and Rich output
- [Cluster Health Checker](examples/03-production-ready/check_cluster_health_enhanced.py) - Production-ready monitoring script with Typer, Rich, and JSON output

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
# ///
"""
One-line description

Purpose: describe-purpose
Team: team-name
Author: email@example.com

Usage:
    python script.py [OPTIONS]

Examples:
    python script.py --help
"""
```

## Best Practices Summary

1. **Always specify Python version** - `requires-python = ">=3.11"`
2. **Pin dependencies appropriately** - Use `>=X.Y.Z` for utilities
3. **Add metadata in docstrings** - Put team info, purpose, and author in module docstring
4. **Include comprehensive docstrings** - Document purpose, usage, and examples
5. **Handle errors gracefully** - Use try/except with clear messages
6. **Validate inputs** - Check arguments before processing
7. **Use quiet mode** - `--quiet` flag for production scripts
8. **Keep it focused** - Single file, single purpose
9. **Test inline** - Add `--test` flag for simple validation
10. **Secure secrets** - Never hardcode, use env vars or keyring
