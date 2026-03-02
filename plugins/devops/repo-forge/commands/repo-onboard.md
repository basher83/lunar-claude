---
description: Onboard a repo with standardized tooling
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# Repo Onboard

Detect project type, run the appropriate mise preset chain, and migrate from
pre-commit to hk if applicable.

## Current State

- Working directory: !`pwd`
- Git repo: !`test -d .git && echo "Yes" || echo "No"`
- Existing mise.toml: !`test -f mise.toml && echo "Yes" || echo "No"`
- Existing hk.pkl: !`test -f hk.pkl && echo "Yes" || echo "No"`
- Pre-commit config: !`test -f .pre-commit-config.yaml && echo "Yes (migration candidate)" || echo "No"`

## Phase 1: Detect Project Type

Scan for project type indicators using Glob:

- `pyproject.toml`, `setup.py`, `setup.cfg` → Python
- `Cargo.toml` → Rust
- `*.tf` files in the current or immediate subdirectories → Terraform
- `ansible.cfg`, `playbooks/` directory, `roles/` directory → Ansible

A project may match multiple types (e.g., Python + Terraform monorepo). Track
all matches. If nothing matches, the project is "base only".

## Phase 2: Confirm with User

Use AskUserQuestion to confirm the detected configuration.

Build the question dynamically based on what was detected:

If project type(s) detected, present them. If .pre-commit-config.yaml exists,
include migration in the confirmation. If hk.pkl already exists, note it will
be overwritten.

Question format:

- header: "Onboard"
- question: "Detected: [type(s)]. [Migration note if applicable]. This will run preset:base + preset:[type], creating mise.toml, hk.pkl, .editorconfig, cliff.toml, .gitignore, and renovate.json. Proceed?"
- options:
  - Proceed (Run detected preset chain)
  - Base only (Skip language preset, run preset:base only)
  - Cancel (Abort onboarding)

If multiple types detected, use multiSelect: true to let user choose which
language presets to apply.

## Phase 3: Execute Presets

Based on user confirmation, run the appropriate preset via Bash.

Available presets and their commands:

- **Python**: `mise preset:uv` (depends on preset:base, runs both)
- **Rust**: `mise preset:rust` (depends on preset:base, runs both)
- **Terraform**: `mise preset:terraform` (depends on preset:base, runs both)
- **Ansible**: `mise preset:ansible` (depends on preset:base, runs both)
- **Base only**: `mise preset:base`

If multiple types selected, run them sequentially. Each language preset depends
on preset:base, so base runs automatically on the first preset. Subsequent
language presets will overwrite hk.pkl (expected — later presets should include
all needed steps).

If a preset fails, stop and report the error. Do not continue to the next preset.

## Phase 4: Pre-commit Migration (conditional)

Only if .pre-commit-config.yaml was detected AND user confirmed in Phase 2.

Run migration steps sequentially:

1. `hk migrate pre-commit` — reads .pre-commit-config.yaml, generates hk.pkl
2. Read the generated hk.pkl and show it to the user for review
3. `hk install --mise` — set up git hooks with mise integration
4. Ask user via AskUserQuestion whether to remove .pre-commit-config.yaml:
   - header: "Cleanup"
   - question: "Migration complete. Remove .pre-commit-config.yaml?"
   - options:
     - Remove (Delete the old config)
     - Keep (Keep it alongside hk.pkl for now)
5. If remove: delete .pre-commit-config.yaml
6. Check if pre-commit is in mise.toml tools — if so, run `mise rm pre-commit`

IMPORTANT: If a language preset already wrote hk.pkl in Phase 3, the migration
in this phase will overwrite it. The migrated hk.pkl preserves existing hook
configurations from pre-commit. After migration, the user should review and
merge any language-specific steps (ruff, shellcheck, etc.) back into the
migrated hk.pkl manually.

## Phase 5: Renovate Language Preset (conditional)

If renovate.json exists and a language type was applied, append the matching
renovate preset to the extends array.

Mapping:
- Python → `local>basher83/renovate-config//presets/python.json`
- Rust → `local>basher83/renovate-config//presets/rust.json`
- Terraform → `local>basher83/renovate-config//presets/terraform-tofu.json`
- Ansible → `local>basher83/renovate-config//presets/ansible.json`

Use this pattern to append if not already present:

```bash
jq '.extends += ["local>basher83/renovate-config//presets/<type>.json"] | .extends |= unique' renovate.json > renovate.tmp && mv renovate.tmp renovate.json
```

Skip if jq is not available or if the preset is already in the extends array.

## Phase 6: Summary

Report what was done:

- Files created or modified (list each)
- Tools installed via mise
- Tasks added
- Migration status (if applicable)
- Any presets that were skipped because they don't exist yet
- Suggested next steps (e.g., "run `uv init` to create pyproject.toml",
  "review hk.pkl and add project-specific steps")
