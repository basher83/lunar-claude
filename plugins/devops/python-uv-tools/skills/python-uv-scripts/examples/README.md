# uv Script Examples

Progressive examples demonstrating uv single-file script patterns.

## Example Structure

### 01-basic-script/

Simple scripts with minimal dependencies showing fundamental concepts.

### 02-with-dependencies/

Scripts demonstrating dependency management with PEP 723 metadata.

### 03-production-ready/

Production-quality scripts with:

- Comprehensive error handling
- Security best practices
- Rich CLI interfaces
- Structured output (JSON + Rich)
- Input validation
- Proper logging

## Featured Example

**check_cluster_health_enhanced.py** - Production-ready cluster monitoring script

This demonstrates all best practices from the skill:

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
```

**Features:**

- ✅ PEP 723 inline metadata
- ✅ Typer CLI with help text
- ✅ Rich formatted output
- ✅ JSON mode for automation
- ✅ Input validation (hostname)
- ✅ Proper error handling
- ✅ Security patterns (no hardcoded credentials)
- ✅ Exit codes for CI/CD
- ✅ Comprehensive documentation

**Usage:**

```bash
# Interactive mode
./check_cluster_health_enhanced.py --node foxtrot

# JSON for automation
./check_cluster_health_enhanced.py --json | jq '.is_healthy'

# Help text
./check_cluster_health_enhanced.py --help
```

## Comparison with Basic Version

**Basic** (.claude/skills/proxmox-infrastructure/tools/check_cluster_health.py):

- Manual dependency installation required
- Basic argparse
- Plain text output
- Minimal error handling

**Enhanced** (this example):

- Inline dependencies (self-installing)
- Typer with rich help
- Beautiful table output + JSON mode
- Comprehensive error handling
- Input validation
- Production-ready

## Try It Yourself

```bash
# Validate the production example
../tools/validate_script.py 03-production-ready/check_cluster_health_enhanced.py

# Run it (uv installs dependencies automatically)
./03-production-ready/check_cluster_health_enhanced.py --help
```

## See Also

- [Main Skill Documentation](../SKILL.md)
- [PEP 723 Reference](../reference/pep-723-spec.md)
- [Security Patterns](../reference/security-patterns.md)
