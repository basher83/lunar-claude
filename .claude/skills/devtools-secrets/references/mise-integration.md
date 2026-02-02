# mise Integration Reference

## Environment Variables in mise.toml

Direct assignment in the `[env]` section:

```toml
[env]
NODE_ENV = "production"
# Unset a variable
LEGACY_VAR = false
# Redact a sensitive value from mise output
SECRET = { value = "my_secret", redact = true }
# Require a variable to be defined (fails if missing)
DATABASE_URL = { required = true }
```

## env.\_.file — Loading From Files

Supports `.env`, `.json`, `.yaml`, and `.toml` files. sops-encrypted files
are automatically decrypted (age encryption only).

```toml
[env]
# Single dotenv file
_.file = ".env"

# Multiple files with mixed formats
_.file = [
    ".env.json",
    "/User/bob/.env",
    { path = ".secrets.yaml", redact = true }
]

# Load after tool env vars are set
_.file = { path = ".env", tools = true }
```

## env.\_.source — Sourcing Bash Scripts

Executes a bash script via `source` and captures exported variables:

```toml
[env]
_.source = "./script.sh"

# Multiple sources with redaction
_.source = [
    "./scripts/base.sh",
    { path = ".secrets.sh", redact = true }
]

# Source after tools are set up
_.source = { path = "my/env.sh", tools = true }
```

## env.\_.path — PATH Modifications

```toml
[env]
_.path = "./bin"
_.path = ["./bin", "./node_modules/.bin"]
```

## Redaction

Prevent sensitive values from appearing in `mise env` output or logs:

```toml
[env]
SECRET = { value = "my_secret", redact = true }
_.file = { path = ".env.json", redact = true }

# Glob patterns for bulk redaction
redactions = ["SECRET_*", "*_TOKEN", "PASSWORD"]
```

View redacted values explicitly:

```bash
mise env --redacted
mise env --redacted --values
```

In GitHub Actions with `mise-action`, values marked `redact = true` are
automatically masked via `::add-mask::`.

## sops Integration

mise auto-decrypts sops-encrypted files loaded via `env._.file`. Only `age`
encryption is supported. Key resolution order:

1. `MISE_SOPS_AGE_KEY` (inline key)
2. `MISE_SOPS_AGE_KEY_FILE` (path to key file)
3. `SOPS_AGE_KEY_FILE` (standard sops variable)
4. `SOPS_AGE_KEY` (standard sops variable)
5. `~/.config/mise/age.txt` (default fallback)

```toml
[env]
_.file = { path = ".env.json", redact = true }
# If .env.json is sops-encrypted, mise decrypts it automatically
```

## Environment Plugins (Lua)

Custom env plugins use the `env._.<plugin-name>` syntax. A plugin consists of:

- `metadata.lua` — plugin metadata
- `hooks/mise_env.lua` — returns `{key, value}` tables for env vars
- `hooks/mise_path.lua` — returns string array of PATH directories

Both hooks receive `ctx.options` from the TOML config. This is the mechanism
for integrating external secret managers (Vault, fnox, etc.) as env plugins.

## mise Hooks

Lifecycle hooks (distinct from env plugin hooks):

| Hook | Trigger |
|------|---------|
| `enter` | When entering a directory with mise.toml |
| `leave` | When leaving a directory with mise.toml |
| `cd` | On every directory change |
| `preinstall` | Before installing a tool |
| `postinstall` | After installing a tool |
| `watch_files` | When watched files change |

## mise + fnox Integration

### Option 0: fnox env plugin (recommended — used in this repo)

```toml
[env]
_.fnox-env = { tools = true }
```

| Option | Purpose | Default |
|--------|---------|---------|
| `tools` | Access mise-managed fnox binary (required if fnox installed via mise) | `false` |
| `profile` | fnox profile to load | `default` |
| `fnox_bin` | Custom binary path (negates need for `tools = true`) | `fnox` |

This auto-loads all fnox secrets as env vars on `cd` into the project. For
per-environment overrides:

```toml
[env]
_.fnox-env = { tools = true, profile = "dev" }

[env.production]
_.fnox-env = { tools = true, profile = "production" }
```

Activate via `MISE_ENV=production mise env`.

**Caching**: Enable `MISE_ENV_CACHE=1` for encrypted disk caching. Clear with
`mise cache clear` or `mise exec --fresh-env`. Cache auto-invalidates when
`fnox.toml` changes.

### Option 1: mise task wrapping fnox exec

```toml
[tasks.dev]
description = "Start dev server with secrets"
run = "fnox exec -- python manage.py runserver"

[tasks.migrate]
description = "Run migrations with DB credentials"
run = "fnox exec -- python manage.py migrate"
```

### Option 2: Template expressions calling fnox

```toml
[env]
DATABASE_URL = "{{ exec(command='fnox get DATABASE_URL') }}"
```

### Option 3: Hook-based injection on directory entry

```toml
[hooks.enter]
run = "fnox exec -- env > .env.local"
```

## Existing mise Tasks in This Repo

```toml
[tasks.hooks-install]
# Installs pre-commit and infisical scan hooks

[tasks.infisical-scan]
# Runs infisical secret scanning on the repo
```

Use `mise run hooks-install` to set up the pre-commit hook, and
`mise run infisical-scan` to check for leaked secrets.

## Best Practices

- Prefer `fnox exec -- command` in mise tasks over hardcoding secrets
- Use `redact = true` on any secret-bearing file or variable
- Use `redactions` glob patterns as a safety net for bulk coverage
- Use mise env plugins for secrets needed across all tasks
- Keep `mise.toml` free of actual secret values — only references to fnox/infisical
- Use `mise run` as the standard entry point so secrets injection is consistent
