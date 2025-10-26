# When NOT to Use UV Single-File Scripts

> **Status**: 🚧 Placeholder - Content in development

## Overview

Clear guidance on when single-file scripts are inappropriate and a proper Python project is needed.

## Signs You Need a Proper Project

### Complexity Indicators

❌ **Don't use single-file scripts when:**

- **Multiple files required**: Need to split code across modules for maintainability
- **Complex dependencies**: Many interdependent packages or version conflicts
- **Shared code**: Multiple scripts sharing significant common code
- **Long-running services**: Daemons, web servers, or background workers
- **Team collaboration**: Multiple developers working simultaneously
- **Testing complexity**: Extensive test suites with fixtures and complex mocking
- **Build process**: Need compilation, bundling, or complex build steps
- **Distribution**: Publishing to PyPI or packaging for end users
- **Configuration complexity**: Multiple environment configs, secrets management beyond simple lookups

### Size Thresholds

- **> 500 lines**: Script is too large for single-file format
- **> 10 dependencies**: Complex dependency graph suggests project structure
- **> 3 developers**: Collaboration requires proper project tooling

### Use Case Examples

#### ❌ Wrong: Web Application

```python
# DON'T: Single-file Flask/FastAPI app
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fastapi", "uvicorn", "sqlalchemy", "alembic"]
# ///
# 1000+ lines of models, routes, middleware...
```

**Why wrong**: Web apps need multiple files, migrations, configs, tests

**Use instead**: Proper project with `pyproject.toml`, src/ structure

#### ✅ Right: Quick Health Check

```python
# DO: Simple monitoring script
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["httpx>=0.27.0"]
# ///
import httpx

def check_endpoint(url: str) -> bool:
    response = httpx.get(url, timeout=5.0)
    return response.status_code == 200
```

## TODO

This file will be expanded to include:

- Complete decision tree for script vs project
- Migration guide from script to project
- Case studies of migrations
- Tool recommendations for project setup
