# mise: hk — Git Hook Manager

hk is a Rust-based git hook manager by the same author as mise (jdx). It replaces the pre-commit framework with parallel execution, file locking for safe concurrent fixes, and built-in linter definitions that resolve tools through mise.

## Setup

```bash
mise use hk               # Install hk via mise
hk init --mise             # Generate hk.pkl + mise.toml integration
hk install --mise          # Set up git hooks using mise for tool resolution
```

Set `HK_MISE=1` in your environment to enable mise integration by default.

## hk.pkl Structure

hk uses Apple's PKL language for configuration. A minimal hk.pkl (update the version in `amends`/`import` to match your installed hk version):

```pkl
amends "package://github.com/jdx/hk/releases/download/v1.27.0/hk@1.27.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v1.27.0/hk@1.27.0#/Builtins.pkl"

local linters = new Mapping<String, Step> {
    ["ruff"] = Builtins.ruff
    ["shellcheck"] = Builtins.shellcheck
}

hooks {
    ["pre-commit"] {
        fix = true
        stash = "git"
        steps = linters
    }
}
```

PKL essentials for hk configs:

- `amends` imports the base schema (pin to an hk release version)
- `import` loads the builtins library
- `local` defines reusable variables (not exported to config)
- `Mapping<String, Step>` is a typed dictionary of step definitions
- Builtins are referenced as `Builtins.<name>` and can be extended with `(Builtins.ruff) { glob = List("src/**/*.py") }`
- `List()` creates typed lists: `List("*.py", "*.pyi")`

## Builtins

Built-in linter/formatter definitions — no version pinning needed, tools resolve through mise.

### Python

`black`, `ruff`, `ruff_format`, `mypy`, `pylint`, `ty` (Astral's type checker)

### Rust

`cargo_fmt`, `cargo_clippy`, `rustfmt`

### JavaScript/TypeScript

`prettier`, `eslint`, `tsc`, `biome`, `deno`

### Go

`go_fmt`, `go_imports`, `golangci_lint`, `go_sec`

### Shell

`shellcheck`, `shfmt`

### Configuration Formats

`yamllint`, `yamlfmt`, `taplo` (TOML check), `taplo_format` (TOML format), `jq` (JSON), `pkl`, `pkl_format`, `hclfmt` (HCL/Terraform), `tombi`

### Markup

`markdown_lint`, `lychee` (link checking)

### Security and Git

`detect_private_key`, `check_merge_conflict`, `check_case_conflict`, `no_commit_to_branch`

### File Hygiene

`trailing_whitespace`, `newlines`, `mixed_line_ending`, `fix_smart_quotes`

### Commit Validation

`check_conventional_commit`, `mise` (config validation)

## Step Configuration

Each step defines how a linter runs:

```pkl
["custom-linter"] {
    glob = List("*.py")          // Files to match from staged set
    stage = List("*.py")         // Files to re-stage after fix
    check = "ruff check {{files}}"   // Read-only check command
    fix = "ruff check --fix {{files}}" // File-modifying fix command
    check_first = true           // Run check with read lock first (default)
    batch = true                 // Split files into batches for parallelism
    exclusive = true             // Block other steps while running
    depends = List("prettier")   // Run after specified steps
    profiles = List("slow")      // Only run in specified profiles
    condition = "test -f ruff.toml"  // Skip if condition fails
    env {
        ["PYTHONPATH"] = "src"
    }
}
```

Key concepts:

- `check` gets a read lock — multiple checks run concurrently
- `fix` gets a write lock — only one fix per file at a time
- `check_first` (default true) optimizes: run check first, only fix if it fails
- `{{files}}` expands to the matched file list
- `batch = true` splits files across parallel workers (good for single-threaded tools)
- `exclusive = true` runs this step alone (use for tasks that need the full repo state)

## Profiles

Separate fast checks from slow ones:

```pkl
["cargo-clippy"] = (Builtins.cargo_clippy) {
    profiles = List("slow")
}
```

Run with profile: `hk check --slow` or `HK_PROFILE=slow hk check`.

Default pre-commit hooks run fast steps only. CI runs `hk check --slow` for the full suite.

## Hook Types

| Hook | Purpose |
|------|---------|
| `pre-commit` | Run before commit creation. Supports fix and stash. |
| `pre-push` | Run before push. Typically check-only. |
| `commit-msg` | Validate commit message format. |
| `prepare-commit-msg` | Template or modify commit messages. |
| `check` | Standalone `hk check` command (not tied to git). |
| `fix` | Standalone `hk fix` command (not tied to git). |

## Migration from pre-commit

```bash
hk migrate pre-commit       # Reads .pre-commit-config.yaml, generates hk.pkl
hk install --mise            # Set up git hooks
rm .pre-commit-config.yaml   # Remove old config
mise rm pre-commit           # Remove pre-commit tool from mise
```

The migration command converts hook repos to builtins where possible and preserves glob patterns and exclusions.

## Global Configuration

Define shared steps in `~/.config/hk/hk.pkl` (hkrc). These apply across all projects unless overridden by a project-level hk.pkl.

## External Resources

- [hk documentation](https://hk.jdx.dev/) — Official docs
- [hk GitHub](https://github.com/jdx/hk) — Source repository
- [PKL language](https://pkl-lang.org/) — Configuration language reference
