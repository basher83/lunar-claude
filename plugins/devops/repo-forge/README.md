# repo-forge

Project setup and validation toolkit. Ensures repos are properly configured
with standard tooling across Python, Rust, Terraform, and Ansible projects.

Uses mise presets as the delivery mechanism for scaffolding, with hk (jdx/hk)
replacing pre-commit for git hook management.

## Skills

| Skill | Status | Purpose |
|-------|--------|---------|
| `mise` | Available | Config, tasks, hooks, presets, hk integration, version resolution |

## Planned Components

| Component | Type | Purpose |
|-----------|------|---------|
| `preset:base` | Preset | Universal scaffolding (hk, cliff, gitignore, editorconfig, renovate) |
| `preset:uv` | Preset | Python project setup (uv, ruff, venv, quality tooling) |
| `preset:rust` | Preset | Rust project setup (cargo, clippy, audit) |
| `preset:terraform` | Preset | Terraform/OpenTofu setup (tflint, terraform-docs, yamllint) |
| `preset:ansible` | Preset | Ansible setup (ansible-lint, yamllint, molecule) |
| `repo-onboard` | Command | Project type detection, preset orchestration, migration |
