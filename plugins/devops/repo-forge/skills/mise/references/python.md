# mise: Python Ecosystem

Python version management, virtual environment handling, and common task patterns for Python projects.

## Python Version Management

mise manages Python versions through its core plugin. No separate plugin install required.

```toml
[tools]
python = "3.12"               # Latest 3.12.x (prefix match)
```

Other version formats:

```toml
[tools]
python = "3.12.4"             # Exact version
# or
python = ["3.11", "3.12"]     # Multiple versions (first is default)
```

By default, mise installs precompiled Python binaries for speed. To compile from source (needed for custom build flags or uncommon platforms):

```toml
[settings]
python.compile = true
```

### Idiomatic version files

mise reads `.python-version` files when idiomatic version file support is enabled, providing compatibility with pyenv-based workflows.

## Virtual Environments

Configure automatic venv creation and activation through the `[env]` section:

```toml
[env]
_.python.venv = { path = ".venv", create = true }
```

This creates `.venv` if it doesn't exist and activates it when entering the project directory.

### Extended options

```toml
[env]
_.python.venv = {
  path = ".venv",
  create = true,
  python = "3.11",                          # Pin venv to specific version
  uv_create_args = ["--seed"]               # Pass args to uv venv
}
```

### UV integration

To align UV's Python resolution with the mise-managed version:

```toml
[env]
UV_PYTHON = { value = "{{ tools.python.path }}", tools = true }
```

### Settings

```toml
[settings]
python.uv_venv_auto = false                # false | "source" | "create|source" | true
python.venv_stdlib = false                  # Use stdlib venv instead of uv/virtualenv
```

## uv Integration

Most Python projects use uv as the package manager. Prefix commands with `uv run` to execute through the managed venv:

```toml
[tasks.python-install]
description = "Install Python dependencies"
run = "uv sync"

[tasks.python-upgrade]
description = "Upgrade Python dependencies"
run = "uv lock --upgrade"

[tasks.python-clean]
description = "Clean development environment"
run = ["rm -rf .venv", "rm -rf requirements.lock"]
```

For CI, use `uv sync --frozen` to install from the lockfile without updating it.

## Task Patterns

All task commands below assume uv-managed projects. Prefix with `uv run` when executing tools installed in the project venv.

### Testing

```toml
[tasks.test]
description = "Run test suite"
run = "uv run pytest"

[tasks."test:coverage"]
description = "Run tests with coverage"
run = "uv run pytest --cov=src --cov-report=term-missing"

[tasks."test:watch"]
description = "Run tests on file change"
run = "uv run ptw -- -x"
```

### Linting and Formatting

```toml
[tasks.lint]
description = "Check code style"
run = "uv run ruff check ."

[tasks."lint:fix"]
description = "Auto-fix lint issues"
run = "uv run ruff check --fix ."

[tasks.format]
description = "Format code"
run = "uv run ruff format ."

[tasks."format:check"]
description = "Check formatting without changes"
run = "uv run ruff format --check ."
```

### Type Checking

```toml
[tasks.typecheck]
description = "Run type checker"
run = "uv run mypy src/"
```

### Quality Gate

```toml
[tasks.check]
description = "Full quality gate"
depends = ["format:check", "lint", "typecheck", "test"]
```

### Packaging

```toml
[tasks.build]
description = "Build distribution packages"
depends = ["check"]
run = "uv run python -m build"

[tasks.publish]
description = "Publish to PyPI"
depends = ["build"]
run = "uv run twine upload dist/*"
```

### Development Server

```toml
[tasks.serve]
description = "Run development server"
run = "uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

[tasks."db:migrate"]
description = "Run database migrations"
run = "uv run alembic upgrade head"

[tasks."db:revision"]
description = "Create new migration"
usage = 'arg "<message>" help="Migration description"'
run = "uv run alembic revision --autogenerate -m \"$1\""
```

## Default Packages

Create `~/.default-python-packages` with one package per line to auto-install into every new Python version:

```text
pip
setuptools
wheel
pipx
```

Set `MISE_PYTHON_DEFAULT_PACKAGES_FILE` to use a custom path.
