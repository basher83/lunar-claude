# Python Tools Plugin Expansion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand python-uv-tools into comprehensive python-tools plugin with code quality and JSON parsing skills.

**Architecture:** Multi-skill plugin with three focused skills (python-uv-scripts, python-code-quality, python-json-parsing), each using layered documentation pattern. Generic config templates prevent cross-project pollution.

**Tech Stack:** Markdown documentation, Python example scripts, YAML/JSON/TOML configs

---

## Task 1: Rename Plugin Directory and Update Metadata

**Files:**
- Rename: `plugins/devops/python-uv-tools/` → `plugins/devops/python-tools/`
- Modify: `plugins/devops/python-tools/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Rename plugin directory**

```bash
cd plugins/devops
mv python-uv-tools python-tools
```

**Step 2: Update plugin.json**

File: `plugins/devops/python-tools/.claude-plugin/plugin.json`

```json
{
  "name": "python-tools",
  "version": "1.0.0",
  "description": "Comprehensive Python development toolkit covering scripting (uv), code quality (ruff/pyright), and common patterns (JSON parsing)",
  "author": {
    "name": "basher83",
    "email": "basher83@mail.spaceships.work"
  },
  "keywords": ["python", "uv", "scripting", "ruff", "pyright", "code-quality", "json", "patterns", "best-practices"]
}
```

**Step 3: Update marketplace.json**

File: `.claude-plugin/marketplace.json`

Find the python-uv-tools entry (around line 68) and update:

```json
{
  "name": "python-tools",
  "source": "./plugins/devops/python-tools",
  "description": "Comprehensive Python development toolkit covering scripting (uv), code quality (ruff/pyright), and common patterns (JSON parsing)",
  "version": "1.0.0",
  "category": "devops",
  "keywords": ["python", "uv", "scripting", "ruff", "pyright", "code-quality", "json", "patterns", "best-practices"],
  "author": {
    "name": "basher83"
  }
}
```

**Step 4: Verify structure**

Run: `./scripts/verify-structure.py`
Expected: python-tools plugin validates successfully

**Step 5: Commit rename**

```bash
git add -A
git commit -m "refactor(plugins): rename python-uv-tools to python-tools

Expand scope from uv-specific to comprehensive Python development toolkit.
Prepares for addition of code quality and JSON parsing skills."
```

---

## Task 2: Create python-code-quality Skill Structure

**Files:**
- Create: `plugins/devops/python-tools/skills/python-code-quality/`
- Create: `plugins/devops/python-tools/skills/python-code-quality/SKILL.md`
- Create: `plugins/devops/python-tools/skills/python-code-quality/reference/`
- Create: `plugins/devops/python-tools/skills/python-code-quality/patterns/`
- Create: `plugins/devops/python-tools/skills/python-code-quality/examples/`
- Create: `plugins/devops/python-tools/skills/python-code-quality/tools/`
- Create: `plugins/devops/python-tools/skills/python-code-quality/workflows/`

**Step 1: Create skill directory structure**

```bash
cd plugins/devops/python-tools/skills
mkdir -p python-code-quality/{reference,patterns,examples,tools,workflows}
```

**Step 2: Create SKILL.md**

File: `plugins/devops/python-tools/skills/python-code-quality/SKILL.md`

```markdown
---
name: python-code-quality
description: >
  Python code quality tooling with ruff and pyright.
  Use when setting up linting, formatting, type checking,
  configuring ruff or pyright, or establishing code quality standards.
---

# Python Code Quality with Ruff and Pyright

Modern Python code quality tooling using ruff (linting + formatting) and pyright (type checking).

## Quick Start

### Install Tools

```bash
# Using uv (recommended)
uv add --dev ruff pyright

# Using pip
pip install ruff pyright
```

### Run Quality Checks

```bash
# Format and lint with ruff
ruff check --fix .
ruff format .

# Type check with pyright
pyright
```

## When to Use This Skill

Use this skill when:
- Setting up linting and formatting for a Python project
- Configuring type checking
- Establishing code quality standards for a team
- Integrating quality checks into pre-commit or CI/CD
- Migrating from black/flake8/mypy to ruff/pyright

## Ruff: All-in-One Linter and Formatter

Ruff combines the functionality of flake8, black, isort, and more:

**Benefits:**
- 10-100x faster than alternatives
- Drop-in replacement for black, flake8, isort
- Single tool configuration
- Auto-fix for many violations

**Configuration:** See `reference/ruff-configuration.md`

## Pyright: Fast Type Checker

Pyright provides static type checking for Python:

**Benefits:**
- Faster than mypy
- Better editor integration (VS Code, etc.)
- Incremental type checking
- Configurable strictness

**Configuration:** See `reference/pyright-configuration.md`

## Recommended Workflow

1. **Pre-commit Hooks** - Run quality checks before each commit
   - See: `patterns/pre-commit-integration.md`

2. **CI/CD Quality Gates** - Block merges on quality failures
   - See: `patterns/ci-cd-quality-gates.md`

3. **Editor Integration** - Real-time feedback while coding
   - See: `workflows/quality-workflow.md`

## Configuration Templates

Generic starter configs in `examples/`:
- `pyrightconfig-starter.json` - Minimal type checking
- `pyrightconfig-strict.json` - Strict type checking
- `ruff-minimal.toml` - Basic linting + formatting
- `ruff-comprehensive.toml` - Full-featured config

## Helper Tools

- `tools/python_formatter.py` - Batch format Python files
- `tools/python_ruff_checker.py` - Check code quality

## Ruff vs Alternatives

| Feature | Ruff | Black + Flake8 + isort |
|---------|------|------------------------|
| Speed | ⚡⚡⚡ | ⚡ |
| Configuration | Single file | Multiple files |
| Auto-fix | ✅ | Partial |
| Formatting | ✅ | Black only |
| Import sorting | ✅ | isort only |

## Pyright vs mypy

| Feature | Pyright | mypy |
|---------|---------|------|
| Speed | ⚡⚡⚡ | ⚡⚡ |
| VS Code integration | Native | Extension |
| Configuration | JSON | INI/TOML |
| Incremental checking | ✅ | ✅ |

## Common Patterns

### Ignore Specific Lines

```python
# Ruff
x = 1  # noqa: F841  # Unused variable

# Pyright
x = 1  # type: ignore
```

### Configure Per-Directory

```toml
# ruff.toml
[tool.ruff]
exclude = ["migrations/", "scripts/"]

[tool.ruff.lint]
select = ["E", "F", "W"]
```

## Next Steps

1. Choose config template from `examples/`
2. Set up pre-commit hooks: `patterns/pre-commit-integration.md`
3. Add CI/CD quality gates: `patterns/ci-cd-quality-gates.md`
4. Configure editor integration: `workflows/quality-workflow.md`

## Reference Documentation

- `reference/ruff-configuration.md` - Complete ruff configuration guide
- `reference/ruff-linting-settings.md` - Linting rule categories
- `reference/ruff-formatting-settings.md` - Formatting options
- `reference/pyright-configuration.md` - Pyright setup and configuration
```text

**Step 3: Verify skill structure**

```bash
ls -la plugins/devops/python-tools/skills/python-code-quality/
```

Expected: SKILL.md and 5 subdirectories

**Step 4: Commit skill structure**

```bash
git add plugins/devops/python-tools/skills/python-code-quality/
git commit -m "feat(python-tools): add python-code-quality skill structure

Create layered documentation structure for ruff and pyright guidance."
```

---

## Task 3: Migrate Reference Documentation to python-code-quality

**Files:**
- Move: `ai_docs/ruff-configuration.md` → `plugins/devops/python-tools/skills/python-code-quality/reference/`
- Move: `ai_docs/ruff-linting-settings.md` → `plugins/devops/python-tools/skills/python-code-quality/reference/`
- Move: `ai_docs/ruff-formatting-settings.md` → `plugins/devops/python-tools/skills/python-code-quality/reference/`
- Move: `ai_docs/pyright-configuration.md` → `plugins/devops/python-tools/skills/python-code-quality/reference/`

**Step 1: Move ruff documentation**

```bash
mv ai_docs/ruff-configuration.md plugins/devops/python-tools/skills/python-code-quality/reference/
mv ai_docs/ruff-linting-settings.md plugins/devops/python-tools/skills/python-code-quality/reference/
mv ai_docs/ruff-formatting-settings.md plugins/devops/python-tools/skills/python-code-quality/reference/
```

**Step 2: Move pyright documentation**

```bash
mv ai_docs/pyright-configuration.md plugins/devops/python-tools/skills/python-code-quality/reference/
```

**Step 3: Verify migration**

```bash
ls plugins/devops/python-tools/skills/python-code-quality/reference/
```

Expected: 4 .md files

**Step 4: Commit migration**

```bash
git add -A
git commit -m "refactor(python-tools): migrate ruff/pyright docs to python-code-quality skill

Move reference documentation from ai_docs/ to skill reference directory."
```

---

## Task 4: Migrate Tools to python-code-quality

**Files:**
- Move: `scripts/python_formatter.py` → `plugins/devops/python-tools/skills/python-code-quality/tools/`
- Move: `scripts/python_ruff_checker.py` → `plugins/devops/python-tools/skills/python-code-quality/tools/`

**Step 1: Move formatter and checker**

```bash
mv scripts/python_formatter.py plugins/devops/python-tools/skills/python-code-quality/tools/
mv scripts/python_ruff_checker.py plugins/devops/python-tools/skills/python-code-quality/tools/
```

**Step 2: Verify tools**

```bash
ls plugins/devops/python-tools/skills/python-code-quality/tools/
```

Expected: python_formatter.py, python_ruff_checker.py

**Step 3: Test tools still work**

```bash
cd plugins/devops/python-tools/skills/python-code-quality/tools/
python python_formatter.py --help
python python_ruff_checker.py --help
```

Expected: Help text displays for both

**Step 4: Commit migration**

```bash
git add -A
git commit -m "refactor(python-tools): migrate formatting tools to python-code-quality skill

Move helper scripts from scripts/ to skill tools directory."
```

---

## Task 5: Create python-json-parsing Skill Structure

**Files:**
- Create: `plugins/devops/python-tools/skills/python-json-parsing/`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/SKILL.md`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/reference/`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/patterns/`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/anti-patterns/`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/examples/`
- Create: `plugins/devops/python-tools/skills/python-json-parsing/tools/`

**Step 1: Create skill directory structure**

```bash
cd plugins/devops/python-tools/skills
mkdir -p python-json-parsing/{reference,patterns,anti-patterns,examples,tools}
```

**Step 2: Create SKILL.md**

File: `plugins/devops/python-tools/skills/python-json-parsing/SKILL.md`

```markdown
---
name: python-json-parsing
description: >
  Python JSON parsing best practices covering performance optimization (orjson/msgspec),
  handling large files (streaming/JSONL), security (injection prevention),
  and advanced querying (JSONPath/JMESPath).
  Use when working with JSON data, parsing APIs, handling large JSON files,
  or optimizing JSON performance.
---

# Python JSON Parsing Best Practices

Comprehensive guide to JSON parsing in Python with focus on performance, security, and scalability.

## Quick Start

### Basic JSON Parsing

```python
import json

# Parse JSON string
data = json.loads('{"name": "Alice", "age": 30}')

# Parse JSON file
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Write JSON file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

**Key Rule:** Always specify `encoding="utf-8"` when reading/writing files.

## When to Use This Skill

Use this skill when:
- Working with JSON APIs or data interchange
- Optimizing JSON performance in high-throughput applications
- Handling large JSON files (> 100MB)
- Securing applications against JSON injection
- Extracting data from complex nested JSON structures

## Performance: Choose the Right Library

### Library Comparison (10,000 records benchmark)

| Library | Serialize (s) | Deserialize (s) | Best For |
|---------|---------------|-----------------|----------|
| **orjson** | 0.42 | 1.27 | FastAPI, web APIs (3.9x faster) |
| **msgspec** | 0.49 | 0.93 | Maximum performance (1.7x faster deserialization) |
| **json** (stdlib) | 1.62 | 1.62 | Universal compatibility |
| **ujson** | 1.41 | 1.85 | Drop-in replacement (2x faster) |

**Recommendation:**
- Use **orjson** for FastAPI/web APIs (native support, fastest serialization)
- Use **msgspec** for data pipelines (fastest overall, typed validation)
- Use **json** when compatibility is critical

### Installation

```bash
# High-performance libraries
pip install orjson msgspec ujson

# Advanced querying
pip install jsonpath-ng jmespath

# Streaming large files
pip install ijson

# Schema validation
pip install jsonschema
```

## Large Files: Streaming Strategies

For files > 100MB, avoid loading into memory.

**Strategy 1: JSONL (JSON Lines)**

Convert large JSON arrays to line-delimited format:

```python
# Stream process JSONL
with open("large.jsonl", "r") as infile, open("output.jsonl", "w") as outfile:
    for line in infile:
        obj = json.loads(line)
        obj["processed"] = True
        outfile.write(json.dumps(obj) + "\n")
```

**Strategy 2: Streaming with ijson**

```python
import ijson

# Process large JSON without loading into memory
with open("huge.json", "rb") as f:
    for item in ijson.items(f, "products.item"):
        process(item)  # Handle one item at a time
```

See: `patterns/streaming-large-json.md`

## Security: Prevent JSON Injection

**Critical Rules:**
1. ✅ Always use `json.loads()`, never `eval()`
2. ✅ Validate input with `jsonschema`
3. ✅ Sanitize user input before serialization
4. ✅ Escape special characters (`"` and `\`)

**Vulnerable Code:**

```python
# NEVER DO THIS
username = request.GET['username']  # User input: admin", "role": "admin
json_string = f'{{"user":"{username}","role":"user"}}'
# Result: privilege escalation
```

**Secure Code:**

```python
# Use json.dumps for serialization
data = {"user": username, "role": "user"}
json_string = json.dumps(data)  # Properly escaped
```

See: `anti-patterns/security-json-injection.md`, `anti-patterns/eval-usage.md`

## Advanced: JSONPath for Complex Queries

Extract data from nested JSON without complex loops:

```python
import jsonpath_ng as jp

data = {
    "products": [
        {"name": "Apple", "price": 12.88},
        {"name": "Peach", "price": 27.25}
    ]
}

# Filter by price
query = jp.parse("products[?price>20].name")
results = [match.value for match in query.find(data)]
# Output: ["Peach"]
```

**Key Operators:**
- `$` - Root selector
- `..` - Recursive descendant
- `*` - Wildcard
- `[?<predicate>]` - Filter (e.g., `[?price > 20]`)
- `[start:end:step]` - Array slicing

See: `patterns/jsonpath-querying.md`

## Custom Objects: Serialization

Handle datetime, UUID, Decimal, and custom classes:

```python
from datetime import datetime
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

# Usage
data = {"timestamp": datetime.now(), "tags": {"python", "json"}}
json_str = json.dumps(data, cls=CustomEncoder)
```

See: `patterns/custom-object-serialization.md`

## Performance Checklist

- [ ] Use orjson/msgspec for high-throughput applications
- [ ] Specify UTF-8 encoding when reading/writing files
- [ ] Use streaming (ijson/JSONL) for files > 100MB
- [ ] Minify JSON for production (`separators=(',', ':')`)
- [ ] Pretty-print for development (`indent=2`)

## Security Checklist

- [ ] Never use `eval()` for JSON parsing
- [ ] Validate input with `jsonschema`
- [ ] Sanitize user input before serialization
- [ ] Use `json.dumps()` to prevent injection
- [ ] Escape special characters in user data

## Reference Documentation

**Performance:**
- `reference/json-parsing-best-practices-2025.md` - Comprehensive research with benchmarks

**Patterns:**
- `patterns/streaming-large-json.md` - ijson and JSONL strategies
- `patterns/custom-object-serialization.md` - Handle datetime, UUID, custom classes
- `patterns/jsonpath-querying.md` - Advanced nested data extraction

**Security:**
- `anti-patterns/security-json-injection.md` - Prevent injection attacks
- `anti-patterns/eval-usage.md` - Why never to use eval()

**Examples:**
- `examples/high-performance-parsing.py` - orjson and msgspec code
- `examples/large-file-streaming.py` - Streaming with ijson
- `examples/secure-validation.py` - jsonschema validation

**Tools:**
- `tools/json-performance-benchmark.py` - Benchmark different libraries
```text

**Step 3: Verify skill structure**

```bash
ls -la plugins/devops/python-tools/skills/python-json-parsing/
```

Expected: SKILL.md and 5 subdirectories

**Step 4: Commit skill structure**

```bash
git add plugins/devops/python-tools/skills/python-json-parsing/
git commit -m "feat(python-tools): add python-json-parsing skill structure

Create layered documentation structure for JSON parsing best practices."
```

---

## Task 6: Migrate JSON Research to python-json-parsing

**Files:**
- Move: `docs/research/python-json-parsing-best-practices-2025.md` → `plugins/devops/python-tools/skills/python-json-parsing/reference/`

**Step 1: Move research document**

```bash
mv docs/research/python-json-parsing-best-practices-2025.md plugins/devops/python-tools/skills/python-json-parsing/reference/
```

**Step 2: Verify migration**

```bash
ls plugins/devops/python-tools/skills/python-json-parsing/reference/
```

Expected: python-json-parsing-best-practices-2025.md

**Step 3: Commit migration**

```bash
git add -A
git commit -m "refactor(python-tools): migrate JSON research to python-json-parsing skill

Move comprehensive research document to skill reference directory."
```

---

## Task 7: Create python-code-quality Example Configs

**Files:**
- Create: `plugins/devops/python-tools/skills/python-code-quality/examples/pyrightconfig-starter.json`
- Create: `plugins/devops/python-tools/skills/python-code-quality/examples/pyrightconfig-strict.json`
- Create: `plugins/devops/python-tools/skills/python-code-quality/examples/ruff-minimal.toml`
- Create: `plugins/devops/python-tools/skills/python-code-quality/examples/ruff-comprehensive.toml`

**Step 1: Create pyrightconfig-starter.json**

File: `plugins/devops/python-tools/skills/python-code-quality/examples/pyrightconfig-starter.json`

```json
{
  "include": ["src", "tests"],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    ".venv",
    "build",
    "dist"
  ],
  "venvPath": ".",
  "venv": ".venv",
  "typeCheckingMode": "basic",
  "reportMissingTypeStubs": false,
  "reportUnknownMemberType": false,
  "reportUnknownArgumentType": false,
  "reportUnknownVariableType": false
}
```

**Step 2: Create pyrightconfig-strict.json**

File: `plugins/devops/python-tools/skills/python-code-quality/examples/pyrightconfig-strict.json`

```json
{
  "include": ["src"],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    ".venv",
    "build",
    "dist"
  ],
  "venvPath": ".",
  "venv": ".venv",
  "typeCheckingMode": "strict",
  "reportMissingTypeStubs": true,
  "reportUnknownMemberType": true,
  "reportUnknownArgumentType": true,
  "reportUnknownVariableType": true,
  "reportPrivateUsage": true,
  "reportUnusedImport": true,
  "reportUnusedVariable": true
}
```

**Step 3: Create ruff-minimal.toml**

File: `plugins/devops/python-tools/skills/python-code-quality/examples/ruff-minimal.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Step 4: Create ruff-comprehensive.toml**

File: `plugins/devops/python-tools/skills/python-code-quality/examples/ruff-comprehensive.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",  # allow assert in tests
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

**Step 5: Verify examples**

```bash
ls plugins/devops/python-tools/skills/python-code-quality/examples/
```

Expected: 4 config files (2 .json, 2 .toml)

**Step 6: Commit examples**

```bash
git add plugins/devops/python-tools/skills/python-code-quality/examples/
git commit -m "feat(python-tools): add generic config templates for ruff and pyright

Provide starter and strict configurations as portable templates."
```

---

## Task 8: Create python-code-quality Patterns

**Files:**
- Create: `plugins/devops/python-tools/skills/python-code-quality/patterns/pre-commit-integration.md`
- Create: `plugins/devops/python-tools/skills/python-code-quality/patterns/ci-cd-quality-gates.md`

**Step 1: Create pre-commit integration pattern**

File: `plugins/devops/python-tools/skills/python-code-quality/patterns/pre-commit-integration.md`

```markdown
# Pre-commit Integration for Ruff and Pyright

Run quality checks automatically before each commit to prevent bad code from entering the repository.

## Setup

### 1. Install pre-commit

```bash
pip install pre-commit
```

### 2. Create .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.380
    hooks:
      - id: pyright
```

### 3. Install hooks

```bash
pre-commit install
```

## Usage

Pre-commit hooks now run automatically:

```bash
git add .
git commit -m "feat: add feature"
# Hooks run automatically before commit
```

### Skip hooks (when needed)

```bash
git commit --no-verify -m "wip: work in progress"
```

## Manual Runs

Run hooks on all files:

```bash
pre-commit run --all-files
```

Run specific hook:

```bash
pre-commit run ruff --all-files
pre-commit run pyright --all-files
```

## Configuration

### Ruff with auto-fix

```yaml
- id: ruff
  args: [--fix, --exit-non-zero-on-fix]
```

### Pyright with specific directories

```yaml
- id: pyright
  files: ^(src|tests)/
```

## Troubleshooting

**Hook fails with "command not found":**
- Ensure ruff/pyright installed in environment
- Try: `pre-commit clean` then `pre-commit install`

**Hooks too slow:**
- Run only on changed files (default behavior)
- Skip pyright in pre-commit, run in CI instead

**Want to update hook versions:**

```bash
pre-commit autoupdate
```

## Best Practices

1. **Keep hooks fast** - Pre-commit should be < 10 seconds
2. **Auto-fix when possible** - Use `--fix` for ruff
3. **Document skip policy** - When is `--no-verify` acceptable?
4. **Update regularly** - Run `pre-commit autoupdate` monthly
```bash

**Step 2: Create CI/CD pattern**

File: `plugins/devops/python-tools/skills/python-code-quality/patterns/ci-cd-quality-gates.md`

```markdown
# CI/CD Quality Gates for Ruff and Pyright

Block merges when code quality fails. Run comprehensive checks in CI that catch issues missed locally.

## GitHub Actions

### Basic Quality Check

Create `.github/workflows/quality.yml`:

```yaml
name: Code Quality

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ruff pyright
          pip install -r requirements.txt

      - name: Run ruff
        run: |
          ruff check .
          ruff format --check .

      - name: Run pyright
        run: pyright
```

### Comprehensive Check with Caching

```yaml
name: Code Quality

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install ruff pyright
          pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check . --output-format=github

      - name: Check formatting
        run: ruff format --check . --diff

      - name: Type check with pyright
        run: pyright --outputjson > pyright-report.json

      - name: Upload pyright report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: pyright-report
          path: pyright-report.json
```

## GitLab CI

Create `.gitlab-ci.yml`:

```yaml
code-quality:
  stage: test
  image: python:3.11
  before_script:
    - pip install ruff pyright
    - pip install -r requirements.txt
  script:
    - ruff check .
    - ruff format --check .
    - pyright
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Quality Metrics

### Track Quality Over Time

```yaml
- name: Generate quality report
  run: |
    ruff check . --output-format=json > ruff-report.json
    pyright --outputjson > pyright-report.json

- name: Comment PR with quality metrics
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const ruffReport = JSON.parse(fs.readFileSync('ruff-report.json'));
      const pyrightReport = JSON.parse(fs.readFileSync('pyright-report.json'));

      const comment = `## Code Quality Report

      **Ruff:** ${ruffReport.length} issues
      **Pyright:** ${pyrightReport.generalDiagnostics.length} issues
      `;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

## Branch Protection Rules

### GitHub

Settings → Branches → Branch protection rules:

1. Require status checks to pass before merging
2. Select "Code Quality" workflow
3. Require branches to be up to date before merging

### GitLab

Settings → Repository → Protected branches:

1. Allowed to merge: Developers + Maintainers
2. Require approval from code owners
3. Pipelines must succeed

## Best Practices

1. **Fail fast** - Run quality checks before tests
2. **Cache dependencies** - Speed up CI with pip caching
3. **Parallel jobs** - Run ruff and pyright in parallel
4. **Quality trends** - Track violations over time
5. **Auto-fix in CI** - Create PR with ruff fixes automatically

## Auto-fix Bot Example

```yaml
- name: Auto-fix with ruff
  run: ruff check --fix .

- name: Commit fixes
  run: |
    git config user.name "ruff-bot"
    git config user.email "bot@example.com"
    git add .
    git diff --staged --quiet || git commit -m "style: auto-fix ruff violations"
    git push
```

## Troubleshooting

**CI passes but pre-commit fails:**
- Ensure same ruff/pyright versions in CI and pre-commit
- Check `.pre-commit-config.yaml` rev matches installed version

**CI too slow:**
- Use pip caching
- Run quality checks in parallel with tests
- Consider skipping pyright on non-Python file changes
```text

**Step 3: Verify patterns**

```bash
ls plugins/devops/python-tools/skills/python-code-quality/patterns/
```

Expected: 2 .md files

**Step 4: Commit patterns**

```bash
git add plugins/devops/python-tools/skills/python-code-quality/patterns/
git commit -m "feat(python-tools): add pre-commit and CI/CD integration patterns

Provide guidance for automated quality checks."
```

---

## Task 9: Update Plugin README

**Files:**
- Modify: `plugins/devops/python-tools/README.md`

**Step 1: Update README**

File: `plugins/devops/python-tools/README.md`

```markdown
# Python Tools

Comprehensive Python development toolkit for scripting, code quality, and common patterns.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install python-tools:

```bash
/plugin install python-tools@lunar-claude
```

## Skills

### python-uv-scripts

Python single-file script development using uv and PEP 723 inline metadata.

**Use when:**
- Creating standalone Python utilities
- Converting scripts to uv format
- Managing script dependencies with inline metadata
- Building self-executable Python scripts

**Triggers:** uv, uv script, pep 723, inline dependencies, single-file script

**Learn more:** [skills/python-uv-scripts/](skills/python-uv-scripts/)

---

### python-code-quality

Python code quality tooling with ruff (linting + formatting) and pyright (type checking).

**Use when:**
- Setting up linting and formatting for a project
- Configuring type checking with pyright
- Establishing code quality standards for a team
- Integrating quality checks into pre-commit or CI/CD
- Migrating from black/flake8/mypy

**Triggers:** ruff, pyright, linting, formatting, type checking, code quality, pre-commit

**Learn more:** [skills/python-code-quality/](skills/python-code-quality/)

---

### python-json-parsing

Best practices for JSON parsing in Python with performance optimization and security focus.

**Use when:**
- Working with JSON data from APIs
- Optimizing JSON performance in high-throughput applications
- Handling large JSON files (> 100MB)
- Securing applications against JSON injection
- Extracting data from complex nested JSON structures

**Triggers:** json, parse json, json parsing, orjson, msgspec, large json, json performance, json security, jsonpath

**Learn more:** [skills/python-json-parsing/](skills/python-json-parsing/)

---

## How It Works

### Autonomous Mode

Simply ask Claude for help with Python development:

```text
"Set up ruff and pyright for my project"
"Parse this large JSON file efficiently"
"Create a Python script using uv that fetches API data"
```

Claude automatically activates the relevant skill based on your request.

### Layered Documentation

Each skill uses progressive disclosure for comprehensive guidance:

- **SKILL.md** - Main entry point with quick start and overview
- **patterns/** - Production-ready implementation patterns
- **anti-patterns/** - Common mistakes to avoid
- **examples/** - Real-world code examples and config templates
- **reference/** - Deep technical documentation
- **tools/** - Helper scripts and utilities
- **workflows/** - Process documentation

This structure provides quick answers while making deep knowledge accessible when needed.

## Supporting Documentation

### python-uv-scripts

- `/patterns/` - Common script patterns (CLI tools, API clients, data processing)
- `/anti-patterns/` - When NOT to use single-file scripts
- `/examples/` - Real-world script examples
- `/workflows/` - CI/CD integration for uv scripts
- `/reference/` - uv command reference and troubleshooting
- `/tools/` - Script conversion and validation utilities

### python-code-quality

- `/reference/` - Complete ruff and pyright configuration guides
- `/patterns/` - Pre-commit hooks, CI/CD quality gates
- `/examples/` - Starter and strict config templates
- `/tools/` - Batch formatter and checker scripts
- `/workflows/` - Development workflow with quality checks

### python-json-parsing

- `/reference/` - Comprehensive 2025 best practices research
- `/patterns/` - Streaming large files, custom serialization, JSONPath querying
- `/anti-patterns/` - Security (injection prevention), eval() dangers
- `/examples/` - High-performance parsing, streaming, validation
- `/tools/` - Performance benchmark script

## Version History

- 1.0.0 - Initial release as comprehensive Python development toolkit
  - python-uv-scripts: uv-based script development
  - python-code-quality: ruff and pyright tooling
  - python-json-parsing: JSON best practices with performance and security focus
```text

**Step 2: Verify README**

```bash
cat plugins/devops/python-tools/README.md | grep -E "^## |^### "
```

Expected: Clear section headings for all three skills

**Step 3: Commit README**

```bash
git add plugins/devops/python-tools/README.md
git commit -m "docs(python-tools): update README for expanded toolkit

Document all three skills with triggers and use cases."
```

---

## Task 10: Verify Complete Structure

**Step 1: Run structure verification**

```bash
./scripts/verify-structure.py
```

Expected: All plugins validate successfully, including python-tools

**Step 2: Check skill discoverability**

```bash
ls -R plugins/devops/python-tools/skills/
```

Expected output:
```text
plugins/devops/python-tools/skills/:
python-code-quality
python-json-parsing
python-uv-scripts

plugins/devops/python-tools/skills/python-code-quality:
SKILL.md  examples  patterns  reference  tools  workflows

plugins/devops/python-tools/skills/python-json-parsing:
SKILL.md  anti-patterns  examples  patterns  reference  tools

plugins/devops/python-tools/skills/python-uv-scripts:
[existing structure]
```

**Step 3: Final commit**

```bash
git add -A
git status
```

Expected: Clean working directory, all changes committed

---

## Success Criteria

- [ ] Plugin renamed from python-uv-tools to python-tools
- [ ] python-code-quality skill created with complete structure
- [ ] python-json-parsing skill created with complete structure
- [ ] All documentation migrated from ai_docs/ and docs/research/
- [ ] All tools migrated from scripts/
- [ ] Generic config examples created (no lunar-claude pollution)
- [ ] README updated with all three skills
- [ ] Structure validation passes
- [ ] All changes committed with clear messages

## Next Steps

After implementation:
1. Test skill activation in new Claude Code session
2. Verify generic configs work in fresh project
3. Update marketplace version if publishing
