# mise: Examples

Complete `mise.toml` files for common project types. Copy and adapt as needed.

## Common Base Tasks

Standard boilerplate tasks that appear across most projects. Include the relevant subset when onboarding a repo.

```toml
min_version = "2024.9.5"

[settings]
auto_install = true
not_found_auto_install = true
task_run_auto_install = true

[settings.status]
show_tools = true
show_env = false
truncate = true

[tools]
git-cliff = "2.10.1"
prek = "0.2.20"
"pipx:rumdl" = "latest"

# === Changelog ===
[tasks.changelog]
description = "Update changelog using git-cliff"
run = "git-cliff -o CHANGELOG.md"

# === Hooks ===
[tasks.hooks-install]
description = "Install pre-commit and infisical hooks"
run = "prek install -f && infisical scan install --pre-commit-hook"

[tasks.pre-commit-run]
description = "Run pre-commit hooks"
run = "prek run --all-files"

# === Security ===
[tasks.infisical-scan]
description = "Scan repository for secrets"
run = "infisical scan"

# === Markdown ===
[tasks.markdown-lint]
description = "Lint Markdown files"
run = "rumdl check ."

[tasks.markdown-fix]
description = "Fix Markdown files"
run = "rumdl fmt ."

# === Composite ===
[tasks.setup]
description = "Set up development environment"
depends = ["hooks-install"]
```

## Minimal Starter

Bare-minimum configuration for any project. Add tools and tasks as the project grows.

```toml
[tools]
node = "22"

[tasks]
dev = "npm run dev"
test = "npm test"
```

## Python Web Application

Full configuration for a Python web project with FastAPI, database migrations, and standard quality tooling.

```toml
[env]
DATABASE_URL = "postgres://localhost/myapp_dev"
_.python.venv = { path = ".venv", create = true }

[tools]
python = "3.12"

[tasks]
serve.run = "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
serve.description = "Run development server"

test.run = "pytest"
test.description = "Run test suite"

"test:coverage".run = "pytest --cov=src --cov-report=term-missing"
"test:coverage".description = "Run tests with coverage"

lint.run = "ruff check ."
lint.description = "Check code style"

"lint:fix".run = "ruff check --fix ."
format.run = "ruff format ."
typecheck.run = "mypy src/"

[tasks.check]
description = "Full quality gate"
depends = ["lint", "typecheck", "test"]

[tasks."db:migrate"]
description = "Run database migrations"
run = "alembic upgrade head"

[tasks."db:revision"]
description = "Create new migration"
usage = 'arg "<message>" help="Migration description"'
run = "alembic revision --autogenerate -m \"$1\""
```

## Rust CLI Tool

Configuration for a Rust CLI project with standard Cargo workflows and source tracking.

```toml
[env]
RUST_LOG = "info"

[tools]
rust = { version = "stable", components = "clippy,rustfmt" }
"cargo:cargo-watch" = "latest"

[tasks]
build.run = "cargo build"
build.description = "Build in debug mode"

"build:release".run = "cargo build --release"
"build:release".description = "Build optimized release binary"
"build:release".sources = ["src/**/*.rs", "Cargo.toml", "Cargo.lock"]

test.run = "cargo test"
test.description = "Run test suite"

lint.run = "cargo clippy -- -D warnings"
lint.description = "Run clippy with strict warnings"

format.run = "cargo fmt"
"format:check".run = "cargo fmt -- --check"

watch.run = "cargo watch -x build"
watch.description = "Rebuild on file changes"

run.run = "cargo run"
run.depends = ["build"]

install.run = "cargo install --path ."

[tasks.check]
description = "Full quality gate"
depends = ["format:check", "lint", "test"]
```

## Multi-Language Project

Python backend with Node.js tooling (documentation site, pre-commit hooks, or frontend build).

```toml
[env]
_.python.venv = { path = ".venv", create = true }

[tools]
python = "3.12"
node = "22"

[tasks]
test.run = "pytest"
lint.run = "ruff check . && eslint docs/"
format.run = ["ruff format .", "prettier --write docs/"]

"docs:dev".run = "npm run docs:dev"
"docs:dev".description = "Run docs development server"

"docs:build".run = "npm run docs:build"
"docs:build".description = "Build documentation site"

[tasks.check]
description = "Full quality gate"
depends = ["lint", "test", "docs:build"]
```

## Infrastructure as Code (Terraform)

Configuration for a Terraform project with environment-scoped validation, linting, and operations. Demonstrates `dir` for targeting subdirectories.

```toml
[settings]
auto_install = true
not_found_auto_install = true
jobs = 4

[settings.status]
show_tools = true

[tools]
terraform = "1.14"
terraform-docs = "0.21"
tflint = "0.61"
yamllint = "1.38"
yamlfmt = "0.21"
shellcheck = "0.11"

[tasks.fmt]
description = "Format all Terraform files recursively"
dir = "infrastructure"
run = "terraform fmt -recursive"

[tasks.fmt-check]
description = "Check formatting (CI-friendly)"
dir = "infrastructure"
run = "terraform fmt -recursive -check -diff"

[tasks.yaml-fmt]
description = "Format YAML files"
run = "yamlfmt ."

[tasks.prod-validate]
description = "Validate production Terraform"
dir = "infrastructure/environments/production"
run = "terraform init -backend=false -input=false >/dev/null && terraform validate"

[tasks.prod-plan]
description = "Plan production changes"
dir = "infrastructure/environments/production"
run = "terraform plan"

[tasks.prod-apply]
description = "Apply production changes"
dir = "infrastructure/environments/production"
run = "terraform apply"

[tasks.lint-prod]
description = "Run TFLint in production"
dir = "infrastructure/environments/production"
run = "tflint --init && tflint"

[tasks.shellcheck]
description = "Lint shell scripts"
run = "find scripts -name '*.sh' -exec shellcheck {} +"

[tasks.docs]
description = "Generate Terraform documentation"
run = "./scripts/generate-docs.sh"

[tasks.check]
description = "Format, lint, and validate"
depends = ["fmt", "lint-prod", "prod-validate"]
env = { TF_IN_AUTOMATION = "true", TF_INPUT = "false" }

[tasks.full-check]
description = "Complete validation suite"
depends = ["fmt", "yaml-fmt", "prod-validate", "lint-prod", "shellcheck", "docs"]
env = { TF_IN_AUTOMATION = "true", TF_INPUT = "false" }

[tasks.setup]
description = "Initial project setup"
depends = ["docs"]
```

## Claude Code Integration

Tasks that wrap Claude Code CLI for AI-assisted workflows. Add to a project's `mise.toml` or a global `~/.config/mise/config.toml`.

```toml
[tasks."cc:ask"]
description = "One-shot question to Claude about this project"
run = "claude --print \"$1\""

[tasks."cc:review"]
description = "AI review of staged changes"
run = "git diff --staged | claude --print 'Review these changes for bugs, style issues, and security concerns.'"

[tasks."cc:explain"]
description = "Explain a file using Claude"
usage = 'arg "<file>" help="File to explain"'
run = "cat \"$1\" | claude --print 'Explain this file. Focus on architecture and key decisions.'"
```

For global cross-repo tasks, place in `~/.config/mise/config.toml`:

```toml
[tasks."repo:status"]
description = "Show git state of all managed repos"
run = '''
for repo in ~/dev/projects/*/; do
  if [ -d "$repo/.git" ]; then
    printf "%-30s %s\n" "$(basename $repo)" "$(git -C $repo status --short | head -1)"
  fi
done
'''
```
