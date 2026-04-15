---
name: mise
description: >
  Mise configuration patterns, task definitions, hooks, presets, and language-specific
  setup guidance for dev environment management and project tooling.
when_to_use: >
  Use when setting up mise, creating a mise.toml, configuring a task runner, managing
  tool versions, adding tasks to mise, setting up Python or Rust with mise, onboarding
  a repo, configuring environment variables, creating presets, scaffolding new projects,
  setting up hk git hooks, generating bootstrap, or migrating from pre-commit.
---

# mise

mise is a polyglot tool version manager and task runner. A single `mise.toml` replaces Makefiles, shell scripts, and language-specific version managers (nvm, pyenv, rustup). It manages tool versions, defines project tasks, and sets environment variables from one configuration file.

## Config File Structure

Order sections canonically for consistency:

```toml
min_version = "2024.9.5"

[env]
DATABASE_URL = "postgres://localhost/myapp_dev"

[tools]
python = "3.12"

[tasks]
test.run = "pytest"

[settings]
auto_install = true
not_found_auto_install = true
task_run_auto_install = true
```

Use `min_version` to enforce a minimum mise version. Recognized top-level sections: `[env]`, `[tools]`, `[tasks]`, `[settings]`, `[plugins]`, `[tool_alias]`, `[task_config]`, `[vars]`.

## Tool Version Management

Specify tools in the `[tools]` section. mise installs and activates them automatically.

```toml
[tools]
node = "22"                   # Major version prefix
python = "3.12.2"             # Exact version
go = "latest"                 # Latest stable
erlang = "lts"                # LTS channel
```

Multiple versions install side-by-side (first is default):

```toml
[tools]
python = ["3.11", "3.12"]
```

### Version formats

| Format | Example | Behavior |
|--------|---------|----------|
| Exact | `"3.12.2"` | Specific version |
| Prefix | `"3.12"` | Latest matching 3.12.x |
| Channel | `"latest"`, `"lts"` | Resolved at install time |
| Reference | `"ref:main"` | Git ref, compiled from source |
| Subtraction | `"sub-1:latest"` | One major behind latest |

### Table form with options

```toml
[tools]
node = { version = "22", postinstall = "corepack enable" }
rust = { version = "stable", components = "clippy,rustfmt", profile = "default" }
```

### Backend syntax for non-core tools

```toml
[tools]
"ubi:astral-sh/ruff" = "latest"     # GitHub binary releases
"cargo:cargo-watch" = "latest"       # Cargo crate
"npm:prettier" = "3"                 # npm package
"pipx:ansible-lint" = "latest"       # Python CLI tools via pipx
```

### Custom plugins

Register custom tool plugins in `[plugins]`:

```toml
[plugins]
fnox-env = "https://github.com/jdx/mise-env-fnox"
```

## Task Definitions

Tasks are defined in `[tasks]` or as executable files in `.mise/tasks/`.

### Inline tasks

```toml
tasks.test = "pytest"
tasks.lint = "ruff check ."
tasks.format = "ruff format ."
```

### Table tasks

```toml
[tasks.build]
description = "Build the project"
depends = ["lint"]
run = "cargo build --release"
dir = "{{config_root}}/backend"
env = { RUST_LOG = "info" }
sources = ["src/**/*.rs", "Cargo.toml"]
outputs = ["target/release/myapp"]
```

### Task-level options

Pin tool versions per-task, set aliases for shortcuts, or override the shell:

```toml
[tasks."lint:shellcheck"]
description = "Lint shell scripts"
run = "shellcheck scripts/*.sh"
tools = { "shellcheck" = "0.11.0" }    # Pin tool version for this task
alias = "sc"                            # Short alias for mise run sc
shell = "bash -c"                       # Override default shell
```

### Task directory scoping

Use `dir` to run a task in a specific subdirectory. Essential for monorepos and infrastructure projects where different tasks target different paths:

```toml
[tasks.prod-validate]
description = "Validate production Terraform"
dir = "infrastructure/environments/production"
run = "terraform init -backend=false -input=false >/dev/null && terraform validate"

[tasks.prod-plan]
description = "Plan production changes"
dir = "infrastructure/environments/production"
run = "terraform plan"
```

Relative paths resolve from the config file's directory. Use `{{config_root}}` for explicit anchoring. When multiple tasks share a base directory, the pattern of environment-scoped tasks (same command, different `dir`) keeps configs DRY while remaining explicit about scope.

### Multi-line scripts

```toml
[tasks.setup]
run = [
  "pip install -e '.[dev]'",
  "pre-commit install"
]
```

### File-based tasks

Place executable scripts in `.mise/tasks/`. Subdirectories create namespaces — `.mise/tasks/db/migrate` becomes task `db:migrate`.

```bash
#!/usr/bin/env bash
#MISE description="Run database migrations"
#MISE depends=["db:check"]

alembic upgrade head
```

Mark file tasks executable (`chmod +x`). Any language works via shebang.

### Task arguments

```toml
[tasks.deploy]
usage = '''
arg "<environment>" help="Target environment" default="staging"
flag "-v --verbose" help="Verbose output"
'''
run = "deploy.sh ${usage_environment}"
```

## Namespace Taxonomy

Name tasks as `namespace:verb`. The namespace is a domain noun, the verb is an action. This groups related tasks alphabetically in `mise tasks` output.

```toml
# Per-project namespaces use the project's domain
tasks."vault:triage" = "claude --print /inbox-process"
tasks."cluster:deploy" = "talosctl apply-config"

# Cross-project namespaces for shared concerns
tasks."cc:prime" = "claude --print /vault-prime"
tasks."git:clean" = "git branch --merged | grep -v main | xargs git branch -d"
```

Use the project's primary domain noun as the namespace. Avoid generic names like `run:` or `do:`.

## Environment Variables

```toml
[env]
NODE_ENV = "development"
PROJECT_ROOT = "{{config_root}}"

# Load from dotenv
_.file = ".env"

# Python virtual environment
_.python.venv = { path = ".venv", create = true }
```

Template variables: `{{config_root}}` (directory containing mise.toml), `{{env.VAR}}` (existing env vars).

## Layered Configuration

mise resolves configuration from multiple levels, with closer files taking precedence:

```text
~/.config/mise/config.toml       # Global: cross-cutting tools and tasks
./mise.toml                      # Project: local tools and tasks
./mise.local.toml                # Local overrides (gitignored)
```

Global config handles cross-cutting concerns (shared tools, repo orchestration tasks). Project config handles repo-specific tools and tasks. Global tasks never assume a specific repo structure — use environment variables or auto-detection.

Use `mise.local.toml` (gitignored) for environment-specific overrides. Tasks can generate this file to switch environments:

```toml
[tasks."env:local"]
description = "Switch to local LAN environment"
run = '''
cat > .mise.local.toml << 'EOF'
[env]
NOMAD_ADDR = "http://192.168.11.11:4646"
CONSUL_HTTP_ADDR = "http://192.168.11.11:8500"
EOF
echo "Switched to local. Run 'mise trust' to apply."
'''
```

## Task Dependencies

```toml
[tasks.check]
description = "Full quality gate"
depends = ["format:check", "lint", "test"]

[tasks.deploy]
depends = ["check"]
depends_post = ["notify"]           # Runs after this task completes
wait_for = ["build"]                # Waits without forcing execution
```

Independent dependencies run in parallel by default. Control parallelism with `[settings] jobs = 4`.

## Version Resolution

Never hardcode tool versions from training data — they will be wrong. Always resolve versions at runtime through mise.

Use `mise use <tool>` to install and pin a tool. It queries the registry, resolves the current version, installs it, and writes the pinned version to mise.toml. Default is fuzzy pinning (`mise use python@3.13` writes `python = "3.13"`). Use `--pin` for exact versions (`python = "3.13.2"`) when patch-level precision matters.

For discovery:

- `mise ls-remote <tool>` — list all available versions from the registry
- `mise ls` — list currently installed tools and versions
- `mise outdated` — show tools with newer versions available
- `mise up --bump` — upgrade all tools while maintaining semver ranges

When writing presets, scripts, or giving version advice: always use `mise use` to resolve versions live. Never embed version strings from memory.

## Hooks

Hooks execute scripts during `mise activate` sessions and tool installations. Define them in `mise.toml`:

```toml
[hooks]
enter = "echo 'entering project'"
postinstall = { task = "post-setup" }
```

Events: `enter` (first project entry), `cd` (every directory change), `leave` (exit project), `preinstall`, `postinstall`. The `enter` and `postinstall` events are the most useful — enter for project validation, postinstall for tool-specific setup after `mise install`.

Shell hooks execute in the current shell context for sourcing files:

```toml
[hooks.enter]
shell = "bash"
script = "source .envrc.local"
```

Watch files for auto-formatting on change:

```toml
[[watch_files]]
patterns = ["src/**/*.rs"]
run = "cargo fmt"
```

See [Hooks Reference](references/hooks.md) for all events, environment variables, and patterns.

## Scaffolding with `mise generate`

mise generates common project files. Use these in presets instead of writing files from scratch:

- `mise generate bootstrap --localize --write` — install script for contributors without mise. `--localize` sandboxes mise into `.mise/` within the project.
- `mise generate config` — creates mise.toml, can import from `.tool-versions`
- `mise generate git-pre-commit --task=<task> --write` — git pre-commit hook that runs a mise task
- `mise generate github-action --write --task=ci` — CI workflow using jdx/mise-action
- `mise generate task-docs` — documentation for all defined tasks
- `mise generate task-stubs` — shims in `bin/` so contributors run tasks without mise installed

Pair `bootstrap` with `task-stubs` for zero-mise-required contributor onboarding.

## Presets

Presets are reusable scaffolding scripts stored in `~/.config/mise/tasks/preset/`. Run with `mise preset:<name>`. They compose through dependency chains:

```bash
#!/usr/bin/env bash
#MISE dir="{{cwd}}"
#MISE depends=["preset:base"]

mise use python uv ruff
mise config set env._.python.venv.path .venv
mise config set env._.python.venv.create true -t bool
mise tasks add --description "Install deps" sync -- uv sync
```

The pattern: `mise use` for tool versions (resolved live), `mise config set` for configuration, `mise tasks add` for task definitions, `mise generate` for standard files, and direct file writes for non-mise configs (cliff.toml, .gitignore, hk.pkl).

Presets are global by design — they scaffold new repos that have no project-level configuration yet.

See [Presets Reference](references/presets.md) for the full API and example preset skeletons.

## hk Integration

hk is a Rust-based git hook manager by the same author as mise. It replaces the pre-commit framework with parallel execution, file-level read/write locks, and built-in linter definitions that resolve tools through mise.

```bash
mise use hk                # Install hk
hk init --mise             # Generate hk.pkl + mise integration
hk install --mise          # Set up git hooks
```

hk provides builtins for common tools: `ruff`, `cargo_clippy`, `cargo_fmt`, `shellcheck`, `yamllint`, `prettier`, `eslint`, `mypy`, `hclfmt`, `detect_private_key`, `check_merge_conflict`, `trailing_whitespace`, `check_conventional_commit`, and many more. Builtins need no version pinning — tools resolve through mise.

For existing repos using pre-commit, migrate with `hk migrate pre-commit`. This reads `.pre-commit-config.yaml`, generates `hk.pkl`, and converts hook repos to builtins where possible.

See [hk Reference](references/hk.md) for PKL config details, the full builtins list, step configuration, and profiles.

## Settings

```toml
[settings]
jobs = 4                            # Parallel task execution
task_output = "prefix"              # prefix | interleave | quiet | silent
```

Language-specific settings nest under the tool name: `python.compile`, `rust.cargo_home`. See language reference files for details.

## Claude Code Integration

mise tasks orchestrate shell-side operations around Claude Code sessions. The pattern: mise owns the shell, Claude owns the conversation. When a mise task needs Claude, invoke the CLI with `claude --print`. Reserve interactive `claude` for workflows requiring user interaction. Never reimplement slash command logic in mise — wrap it.

See [Examples](examples/examples.md) for complete Claude Code integration task patterns.

## Reference Guides

- [Python Ecosystem](references/python.md) — Version management, venv handling, and task patterns for Python projects
- [Rust Ecosystem](references/rust.md) — Toolchain management and task patterns for Rust projects
- [Hooks](references/hooks.md) — Hook events, environment variables, and common patterns
- [Presets](references/presets.md) — Preset anatomy, CLI reference, dependency chaining, and example skeletons
- [hk Git Hooks](references/hk.md) — hk.pkl configuration, builtins, step options, profiles, and migration
- [Examples](examples/examples.md) — Complete `mise.toml` files for common project types

## External Resources

- [mise documentation](https://mise.jdx.dev/) — Official docs
- [mise GitHub](https://github.com/jdx/mise) — Source repository
- [mise.toml schema](https://mise.jdx.dev/schema/mise.json) — JSON schema for editor validation
- [hk documentation](https://hk.jdx.dev/) — Git hook manager docs
- [hk GitHub](https://github.com/jdx/hk) — Git hook manager source
