---
name: mise
description: >-
  This skill provides mise configuration patterns, task definitions, and language-specific
  setup guidance. This skill should be used when the user asks to "set up mise", "create a
  mise.toml", "configure task runner", "manage tool versions", "add a task to mise",
  "set up Python with mise", "configure Rust toolchain", "onboard a repo", "add mise to this
  project", "set up dev environment", "configure environment variables in mise", "set up
  global mise config", or mentions mise configuration, dev tooling setup, task definitions,
  layered configuration, or project onboarding.
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
- [Examples](examples/examples.md) — Complete `mise.toml` files for common project types

## External Resources

- [mise documentation](https://mise.jdx.dev/) — Official docs
- [mise GitHub](https://github.com/jdx/mise) — Source repository
- [mise.toml schema](https://mise.jdx.dev/schema/mise.json) — JSON schema for editor validation
