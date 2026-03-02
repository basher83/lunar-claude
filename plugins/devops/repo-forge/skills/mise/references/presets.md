# mise: Presets

Presets are reusable task scripts that scaffold new projects. They live in `~/.config/mise/tasks/preset/` and run with `mise preset:<name>`.

## Anatomy of a Preset

A preset is an executable bash script with MISE metadata comments:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"

mise use uv ruff
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool
mise tasks add --description "Run linter" lint -- hk check
mise tasks add sync -- uv sync
```

Key elements:

- `#MISE dir="{{cwd}}"` — run in the caller's directory, not the script's location
- `mise use <tool>` — resolves the current version from the registry and pins it in the local mise.toml. Never hardcodes versions.
- `mise config set <path> <value>` — writes configuration to mise.toml programmatically
- `mise tasks add <name> -- <command>` — adds a task definition to mise.toml

## Preset Dependencies

Chain presets using the `depends` directive:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"
#MISE depends=["preset:base"]

mise use python uv ruff
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool
mise tasks add sync -- uv sync
mise tasks add upgrade -- uv lock --upgrade
```

Running `mise preset:uv` automatically runs `preset:base` first. This enables layered scaffolding: base handles universal config (hk, cliff, gitignore), language presets add tool-specific setup.

## `mise config set` Reference

Set arbitrary configuration paths in mise.toml:

```bash
# Tools
mise config set tools.python 3.12

# Environment
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool
mise config set env.DATABASE_URL "postgres://localhost/myapp"

# Settings
mise config set settings.jobs 4
mise config set settings.task_output prefix

# Type flag for non-string values
mise config set settings.disable_tools --type list node,rust
```

## `mise tasks add` Reference

Add tasks programmatically:

```bash
# Simple task
mise tasks add test -- pytest

# Task with description
mise tasks add --description "Run test suite" test -- pytest

# Task with dependencies
mise tasks add --depends lint --depends test check -- echo "All checks passed"

# Task with directory scoping
mise tasks add --dir infrastructure validate -- terraform validate

# Task with alias
mise tasks add --alias t test -- pytest
```

## Integrating `mise generate`

Presets should leverage `mise generate` for standard files:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"

# Bootstrap script for contributors without mise
mise generate bootstrap --localize --write

# GitHub Actions CI workflow
mise generate github-action --write --task=ci

# Task stubs for running without mise installed
mise generate task-stubs
```

## Example: preset:base

Universal scaffolding applied to every new repo:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"

# Tools
mise use hk git-cliff

# hk git hooks
hk init --mise
hk install --mise

# CI and onboarding
mise generate github-action --write --task=ci
mise generate bootstrap --localize --write

# Standard tasks
mise tasks add --description "Run all checks" lint -- hk check
mise tasks add --description "Auto-fix issues" fix -- hk fix
mise tasks add --description "Update changelog" changelog -- git-cliff -o CHANGELOG.md
mise tasks add --description "Full CI gate" --depends lint ci -- echo "CI passed"
```

## Example: preset:uv

Python project scaffolding, depends on base:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"
#MISE depends=["preset:base"]

# Tools (versions resolved live from registry)
mise use python uv ruff

# Python environment
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool

# Tasks
mise tasks add --description "Install dependencies" sync -- uv sync
mise tasks add --description "Upgrade dependencies" upgrade -- uv lock --upgrade
mise tasks add --description "Run tests" test -- uv run pytest
mise tasks add --description "Type check" typecheck -- uv run pyright

# Postinstall hook: auto-setup after mise install
mise config set hooks.postinstall "hk install --mise && uv sync"
```

## Preset Location

Presets live in `~/.config/mise/tasks/preset/`. Each file is a task named by its filename: `~/.config/mise/tasks/preset/uv` becomes `mise preset:uv`.

Mark preset files executable: `chmod +x ~/.config/mise/tasks/preset/*`.

Presets are global by design — they scaffold new repos that don't yet have any project-level configuration.
