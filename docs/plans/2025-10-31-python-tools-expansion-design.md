# Python Tools Plugin Expansion Design

**Date:** October 31, 2025
**Author:** basher83
**Status:** Approved

## Purpose

Transform the `python-uv-tools` plugin into a comprehensive Python development toolkit covering scripting, code quality, and common patterns. The plugin will provide portable, reusable guidance for Python developers across all projects.

## Design Overview

### Plugin Rename

Rename `plugins/devops/python-uv-tools/` to `plugins/devops/python-tools/` to reflect the expanded scope.

**Updated metadata:**
- Name: `python-tools`
- Description: "Comprehensive Python development toolkit covering scripting (uv), code quality (ruff/pyright), and common patterns (JSON parsing)"
- Keywords: python, uv, scripting, ruff, pyright, code-quality, json, patterns, best-practices

### Multi-Skill Architecture

Organize the plugin into three focused skills:

1. **python-uv-scripts** (existing) - uv-based script development
2. **python-code-quality** (new) - ruff and pyright tooling
3. **python-json-parsing** (new) - JSON parsing best practices

Each skill uses layered documentation with progressive disclosure.

## Skill 1: python-uv-scripts

**Status:** Keep as-is

No changes to existing skill. Continues to provide uv scripting guidance with PEP 723 inline metadata.

## Skill 2: python-code-quality

**Purpose:** Guide developers through Python code quality tools (ruff, pyright).

**Triggers:** ruff, pyright, linting, formatting, type checking, code quality, pre-commit

### Directory Structure

```text
skills/python-code-quality/
├── SKILL.md
├── reference/
│   ├── ruff-configuration.md (from ai_docs/)
│   ├── ruff-linting-settings.md (from ai_docs/)
│   ├── ruff-formatting-settings.md (from ai_docs/)
│   └── pyright-configuration.md (from ai_docs/)
├── patterns/
│   ├── pre-commit-integration.md
│   └── ci-cd-quality-gates.md
├── examples/
│   ├── pyrightconfig-starter.json
│   ├── pyrightconfig-strict.json
│   ├── ruff-minimal.toml
│   └── ruff-comprehensive.toml
├── tools/
│   ├── python_formatter.py (from scripts/)
│   └── python_ruff_checker.py (from scripts/)
└── workflows/
    └── quality-workflow.md
```

### Content to Create

1. **SKILL.md** - Entry point covering:
   - Quick start: running ruff and pyright
   - When to use ruff vs alternatives (black, flake8)
   - Editor integration (VS Code, PyCharm)
   - Pre-commit hooks
   - CI/CD integration

2. **patterns/pre-commit-integration.md** - Pre-commit setup with ruff/pyright

3. **patterns/ci-cd-quality-gates.md** - GitHub Actions and GitLab CI examples

4. **examples/*.json, *.toml** - Generic configuration templates (NOT lunar-claude specific)

5. **workflows/quality-workflow.md** - Development workflow with quality checks

## Skill 3: python-json-parsing

**Purpose:** Provide best practices for JSON parsing with performance and security focus.

**Triggers:** json, parse json, json parsing, orjson, msgspec, ujson, large json, json performance, json security, jsonpath, jmespath, json injection

### Directory Structure

```text
skills/python-json-parsing/
├── SKILL.md
├── reference/
│   └── json-parsing-best-practices-2025.md (from docs/research/)
├── patterns/
│   ├── streaming-large-json.md
│   ├── custom-object-serialization.md
│   └── jsonpath-querying.md
├── anti-patterns/
│   ├── security-json-injection.md
│   └── eval-usage.md
├── examples/
│   ├── high-performance-parsing.py
│   ├── large-file-streaming.py
│   └── secure-validation.py
└── tools/
    └── json-performance-benchmark.py
```

### Content to Create

1. **SKILL.md** - Entry point covering:
   - Quick start: json.loads() basics
   - Performance comparison table (json vs orjson vs msgspec)
   - When to use streaming vs in-memory parsing
   - Security checklist (injection prevention, no eval())
   - Reference to detailed best practices document

2. **patterns/streaming-large-json.md** - ijson and JSONL patterns for large files

3. **patterns/custom-object-serialization.md** - Custom encoder/decoder patterns

4. **patterns/jsonpath-querying.md** - JSONPath and JMESPath usage

5. **anti-patterns/security-json-injection.md** - Injection attack prevention

6. **anti-patterns/eval-usage.md** - Why never to use eval() for JSON

7. **examples/high-performance-parsing.py** - orjson and msgspec examples

8. **examples/large-file-streaming.py** - Streaming JSON with ijson

9. **examples/secure-validation.py** - jsonschema validation examples

10. **tools/json-performance-benchmark.py** - Benchmark script comparing libraries

## Plugin README Update

Create comprehensive README introducing all skills:

**Structure:**
- Installation instructions
- Three skill sections (uv-scripts, code-quality, json-parsing)
- "When to use" guidance for each skill
- How layered documentation works
- Link to each skill's directory

## File Migrations

**Move from ai_docs/ to python-code-quality/reference/:**
- ruff-configuration.md
- ruff-linting-settings.md
- ruff-formatting-settings.md
- pyright-configuration.md

**Move from scripts/ to python-code-quality/tools/:**
- python_formatter.py
- python_ruff_checker.py

**Move from docs/research/ to python-json-parsing/reference/:**
- python-json-parsing-best-practices-2025.md

## Configuration Isolation

Root-level configs (`pyrightconfig.json`, `ruff.toml`) remain at project root. Skills provide **generic templates** in examples/ directories, not references to lunar-claude's project-specific configs.

This prevents Claude from applying lunar-claude's specific settings to other projects.

## Skill Auto-Discovery

Claude discovers skills through trigger keywords in SKILL.md descriptions:

**python-code-quality triggers:**
- ruff, pyright, linting, formatting, type checking
- code quality, pre-commit, flake8, black, mypy

**python-json-parsing triggers:**
- json, parse json, json parsing
- orjson, msgspec, ujson
- large json, json performance, json security
- jsonpath, jmespath, json injection

**python-uv-scripts triggers (existing):**
- uv, uv script, pep 723
- inline dependencies, single-file script

No trigger overlap between skills.

## Implementation Estimate

**Files to move:** 6
**Files to create:** 15-20
**Files to update:** 3 (plugin.json, marketplace.json, README.md)

## Success Criteria

1. Plugin renamed without breaking existing users
2. Three skills independently discoverable by Claude
3. Generic examples (no lunar-claude-specific configs)
4. All migrations complete
5. README guides users to correct skill
6. Documentation follows layered approach (SKILL.md + subdirectories)

## Next Steps

1. Write design to docs/plans/
2. Set up git worktree for implementation
3. Create implementation plan with task breakdown
