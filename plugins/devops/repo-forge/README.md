# repo-forge

Project setup and validation toolkit. Ensures repos are properly configured
with standard tooling across Python, Rust, Terraform, and Ansible projects.

Uses mise presets as the delivery mechanism for scaffolding, with hk (jdx/hk)
replacing pre-commit for git hook management.

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| `mise` | Skill | Config, tasks, hooks, presets, hk integration, version resolution |
| `repo-onboard` | Command | Project type detection, preset orchestration, migration |
| `preset:base` | Preset | Universal scaffolding (hk, cliff, gitignore, editorconfig, renovate) |
| `preset:uv` | Preset | Python project setup (uv, ruff, venv, quality tooling) |
| `preset:rust` | Preset | Rust project setup (cargo, clippy, taplo) |
| `preset:terraform` | Preset | Terraform/OpenTofu setup (tflint, terraform-docs, yamllint) |
| `preset:ansible` | Preset | Ansible setup (ansible-lint, yamllint) |

## File Locations

Presets live outside this plugin at the global mise tasks path:

```text
~/.config/mise/tasks/preset/
├── base        # Universal — hk, cliff, gitignore, editorconfig, renovate, bootstrap
├── uv          # Python — depends on base
├── rust        # Rust — depends on base
├── terraform   # Terraform — depends on base
└── ansible     # Ansible — depends on base
```

The skill and command live in this plugin:

```text
plugins/devops/repo-forge/
├── skills/mise/          # Knowledge layer (SKILL.md + references)
└── commands/repo-onboard.md  # Orchestration command
```
