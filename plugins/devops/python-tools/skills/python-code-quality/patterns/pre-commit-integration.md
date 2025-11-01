# Pre-commit Integration for Ruff and Pyright

Run quality checks automatically before each commit to prevent bad code from
entering the repository.

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
