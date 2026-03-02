# mise: Hooks

Hooks execute scripts automatically during mise activate sessions and tool installations.

## Hook Events

| Event | Trigger | Requires shell hook |
|-------|---------|-------------------|
| `enter` | First time entering a project directory | Yes |
| `cd` | Every directory change within a project | Yes |
| `leave` | Exiting a project directory | Yes |
| `preinstall` | Before `mise install` runs | No |
| `postinstall` | After `mise install` completes | No |

## Configuration

Define hooks in `mise.toml` under the `[hooks]` section.

### Inline commands

```toml
[hooks]
enter = "echo 'entering project'"
leave = "echo 'leaving project'"
cd = "echo 'changed directory'"
preinstall = "echo 'about to install tools'"
postinstall = "echo 'tools installed'"
```

### Multiple hooks per event

```toml
[hooks]
enter = [
  "echo 'first action'",
  "echo 'second action'"
]
```

### Task triggers

Run a mise task when an event fires:

```toml
[hooks]
enter = { task = "setup" }
postinstall = { task = "post-setup" }
```

### Shell hooks

Execute in the current shell environment. Use for sourcing completions or setting shell variables:

```toml
[hooks.enter]
shell = "bash"
script = "source .envrc.local"
```

## Environment Variables

Available in all hooks:

- `MISE_ORIGINAL_CWD` — user's current directory
- `MISE_PROJECT_ROOT` — project root (directory containing mise.toml)

Available in `cd` hooks:

- `MISE_PREVIOUS_DIR` — directory before the change

Available in `postinstall` hooks:

- `MISE_INSTALLED_TOOLS` — JSON array of installed tools

Available in tool-level `postinstall`:

- `MISE_TOOL_NAME` — tool identifier (e.g., `python`)
- `MISE_TOOL_VERSION` — installed version (e.g., `3.13.2`)
- `MISE_TOOL_INSTALL_PATH` — installation directory

## Watch Files

Monitor file patterns and auto-run commands on change. Requires `mise activate` with shell hook.

```toml
[[watch_files]]
patterns = ["src/**/*.rs"]
run = "cargo fmt"

[[watch_files]]
patterns = ["*.py"]
run = "ruff check --fix ."
```

## Common Patterns

### Project setup on entry

```toml
[hooks]
enter = { task = "setup" }

[tasks.setup]
description = "Ensure project is ready"
run = [
  "hk install --mise",
  "uv sync"
]
```

### Tool-specific postinstall

```toml
[tools]
node = { version = "22", postinstall = "corepack enable" }
rust = { version = "stable", postinstall = "cargo install cargo-audit" }
```

### Validate config on entry

```toml
[hooks]
enter = "mise config ls >/dev/null && echo 'Config OK' || echo 'Config issues detected'"
```
