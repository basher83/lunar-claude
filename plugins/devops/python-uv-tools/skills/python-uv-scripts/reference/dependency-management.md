# Dependency Management Reference

> **Status**: 🚧 Placeholder - Content in development

## Overview

Comprehensive guide to managing dependencies in UV single-file scripts using PEP 723 inline metadata.

## Topics to Cover

- [ ] Version pinning strategies
- [ ] Semantic versioning best practices
- [ ] Dependency conflict resolution
- [ ] Optional dependencies
- [ ] Development vs production dependencies
- [ ] Security updates and vulnerability scanning
- [ ] Lock file equivalents for scripts

## Quick Reference

### Version Pinning Strategies

**Exact pinning** (most restrictive):
```python
# /// script
# dependencies = ["requests==2.31.0"]
# ///
```

**Compatible release** (recommended):
```python
# /// script
# dependencies = ["requests~=2.31.0"]  # >=2.31.0, <2.32.0
# ///
```

**Minimum version**:
```python
# /// script
# dependencies = ["requests>=2.31.0"]
# ///
```

### Following Repository Standards

From this repository's `pyproject.toml`, we use:
- `>=` for minimum versions with flexibility
- Specific version ranges for critical dependencies
- Regular dependency audits with Renovate

## TODO

This file will be expanded to include:

- Complete version specifier syntax
- Dependency resolution strategies
- Security scanning integration
- Update strategies and automation
- Conflict resolution techniques
