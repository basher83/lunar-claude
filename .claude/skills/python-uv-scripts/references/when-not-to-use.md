# When NOT to Use Single-File Scripts

This document helps determine when to use a single-file uv script vs. when to use a proper uv project.

## Decision Tree

```text
Is this a Python program?
├─ No → Use appropriate language/tool
└─ Yes
    ├─ Is it a one-time task or simple automation?
    │   ├─ Yes → Consider single-file script
    │   └─ No → Use proper uv project
    └─ Does it meet ANY of these criteria?
        ├─ >500 lines of code → Use proper uv project
        ├─ Multiple Python files needed → Use proper uv project
        ├─ Web application or API → Use proper uv project
        ├─ Long-running service → Use proper uv project
        ├─ Complex configuration → Use proper uv project
        ├─ Shared library code → Use proper uv project
        ├─ Heavy ML/data dependencies → Use proper uv project
        └─ None of the above → Single-file script is appropriate
```

## Use Proper uv Project When

### 1. Code Complexity

**Use project if**:

- Script exceeds 500 lines
- Logic is spread across multiple functions/classes
- Code would benefit from splitting into modules
- Complex data models or class hierarchies

**Example - Too Complex for Script**:

```python
# This needs a proper project structure:
# - 800 lines of code
# - Multiple classes (User, Database, API, Config)
# - Would be clearer as separate modules
# - Needs tests
```

### 2. Multiple Files Needed

**Use project if**:

- Shared utilities across multiple scripts
- Common data models used by different tools
- Reusable library code
- Multiple entry points

**Example**:

```text
# This needs a project:
my-tool/
├── src/
│   ├── __init__.py
│   ├── database.py      # Shared by multiple tools
│   ├── models.py        # Common data structures
│   └── utils.py         # Utility functions
├── scripts/
│   ├── import_data.py   # Uses shared code
│   └── export_data.py   # Uses shared code
└── pyproject.toml
```

### 3. Web Applications

**Use project for**:

- Flask/FastAPI/Django applications
- REST APIs
- Web services
- Applications with routes/controllers

**Example - Needs Project**:

```python
# Don't use single-file script for web apps:
from flask import Flask, request, jsonify

app = Flask(__name__)

# 50+ routes
# Database models
# Authentication
# Background tasks
# Configuration management

# This should be a proper project structure
```

### 4. Long-Running Services

**Use project for**:

- Daemons
- Background workers
- Queue consumers
- Services that run continuously

**Example**:

```python
# Don't use script for services:
# - Runs 24/7
# - Monitors message queue
# - Complex retry logic
# - Logging configuration
# - Health checks
# - Graceful shutdown

# Needs proper project structure with:
# - Proper logging setup
# - Configuration management
# - Process management (systemd/supervisor)
```

### 5. Complex Configuration

**Use project if**:

- Multiple environment configs (dev/staging/prod)
- YAML/JSON configuration files
- Feature flags
- Database connection pools

**Example**:

```text
# This needs a project:
config/
├── dev.yaml
├── staging.yaml
└── production.yaml

# Single-file scripts should use simple env vars instead
```

### 6. Heavy Dependencies

**Use project for**:

- Machine learning frameworks (TensorFlow, PyTorch)
- Large data processing (PySpark)
- Complex scientific computing
- GUI frameworks

**Example - Too Heavy**:

```python
# /// script
# dependencies = [
#   "tensorflow>=2.15.0",     # ❌ ~500MB download
#   "torch>=2.1.0",           # ❌ ~800MB download
#   "transformers>=4.35.0",   # ❌ Complex dependency tree
# ]
# ///

# Use proper project with managed virtual environment
```

### 7. Testing Requirements

**Use project if**:

- Comprehensive test suite needed
- Multiple test files
- Fixtures and mocking
- CI/CD integration

**Example**:

```text
# This needs a project:
tests/
├── unit/
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_api.py
├── integration/
│   └── test_database.py
└── conftest.py

# Can't reasonably organize this with single-file script
```

### 8. Team Collaboration

**Use project if**:

- Multiple developers working on code
- Code review processes
- Versioning and releases
- Documentation requirements

## Single-File Scripts ARE Appropriate For

### ✅ Good Use Cases

**One-time tasks**:

```python
# Convert CSV format
# Migrate data between systems
# Clean up old files
# Generate reports
```

**Simple automation**:

```python
# Check server health
# Send notifications
# Backup files
# Parse logs
```

**CLI utilities**:

```python
# Format files
# Validate data
# Query APIs
# Process input
```

**Prototyping**:

```python
# Test API endpoints
# Experiment with libraries
# Quick data analysis
# Proof of concept
```

### ✅ Characteristics of Good Single-File Scripts

- **<500 lines of code**
- **Self-contained logic**
- **Simple, clear purpose**
- **Minimal dependencies (1-5 packages)**
- **Standalone execution**
- **Quick to understand**

## Examples of Good Single-File Scripts

### Example 1: Health Check

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "psutil>=5.9.0",
#   "rich>=13.0.0",
# ]
# ///
"""Check system health and display metrics."""

import psutil
from rich import print

def main():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    print(f"CPU: {cpu}% | Memory: {mem}% | Disk: {disk}%")

    if cpu > 80 or mem > 80 or disk > 80:
        print("[red]⚠ High resource usage![/red]")
        exit(1)

if __name__ == "__main__":
    main()
```

### Example 2: API Query

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///
"""Query API and display results."""

import httpx
import sys

def main():
    response = httpx.get("https://api.github.com/users/octocat")
    response.raise_for_status()
    data = response.json()
    print(f"Name: {data['name']}")
    print(f"Public repos: {data['public_repos']}")

if __name__ == "__main__":
    main()
```

## Migration Path

**When a script outgrows single-file format**:

1. Create proper uv project:

   ```bash
   uv init my-tool
   cd my-tool
   ```

2. Move script logic to `src/`:

   ```bash
   mv script.py src/my_tool/main.py
   ```

3. Add dependencies to `pyproject.toml`:

   ```toml
   [project]
   dependencies = [
       "httpx>=0.27.0",
       "rich>=13.0.0",
   ]
   ```

4. Create entry point in `pyproject.toml`:

   ```toml
   [project.scripts]
   my-tool = "my_tool.main:main"
   ```

## Summary

**Use single-file scripts for**:

- Simple automation (<500 lines)
- One-off tasks
- CLI utilities
- Prototypes
- Standalone tools

**Use proper uv projects for**:

- Complex applications (>500 lines)
- Multiple files/modules
- Web applications
- Long-running services
- Heavy dependencies
- Team collaboration
- Comprehensive testing

**When in doubt**: Start with a script. If it grows too complex, migrate to a project.
