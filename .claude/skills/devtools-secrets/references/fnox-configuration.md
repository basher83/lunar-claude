# fnox Configuration Reference

## fnox.toml Structure

```toml
default_provider = "age"
if_missing = "error"  # error | warn | ignore

import = ["shared/fnox.toml"]  # merge in other config files

[providers.age]
type = "age"
recipients = [
  "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p",
  "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGQs..."
]

[providers.infisical]
type = "infisical"
project_id = "abc123"
environment = "dev"
path = "/"

[secrets]
# Encrypted in git via age
INFISICAL_TOKEN = { provider = "age", value = "encrypted-token..." }
# Retrieved from infisical at runtime
DATABASE_URL = { provider = "infisical", value = "DATABASE_URL" }
# With metadata
API_KEY = { provider = "infisical", description = "Third-party API key", if_missing = "warn" }
# Plain default (non-sensitive)
LOG_LEVEL = { provider = "plain", default = "info" }
```

## Providers

### Encryption (secrets stored encrypted in fnox.toml, safe to commit)

| Provider | Type | Notes |
|----------|------|-------|
| **age** | `age` | Modern encryption, works with SSH keys. Key via `FNOX_AGE_KEY` or `FNOX_AGE_KEY_FILE` |
| **AWS KMS** | `aws-kms` | Cloud KMS encryption |
| **Azure KMS** | `azure-kms` | Cloud KMS encryption |
| **GCP KMS** | `gcp-kms` | Cloud KMS encryption |

### Cloud Secret Storage (fnox.toml has references only)

| Provider | Type | Notes |
|----------|------|-------|
| **AWS Parameter Store** | `aws-ps` | SSM parameters |
| **AWS Secrets Manager** | `aws-sm` | Full secret management |
| **Azure Key Vault** | `azure-sm` | Azure secrets |
| **GCP Secret Manager** | `gcp-sm` | GCP secrets |
| **HashiCorp Vault** | `vault` | Self-hosted or HCP |

### Password Managers & Secret Services

| Provider | Type | Notes |
|----------|------|-------|
| **1Password** | `1password` | Via `op` CLI. Auth: `OP_SERVICE_ACCOUNT_TOKEN` |
| **Bitwarden** | `bitwarden` | Via `bw` or `rbw` CLI. Auth: `BW_SESSION` |
| **Infisical** | `infisical` | Via `infisical` CLI. Auth: Universal Auth (client ID + secret) or `INFISICAL_TOKEN` |
| **Passwordstate** | `passwordstate` | HTTP API. Requires `base_url`, `api_key`, `password_list_id` |

### Local Storage

| Provider | Type | Notes |
|----------|------|-------|
| **OS Keychain** | `keychain` | macOS Keychain, Windows Credential Manager, Linux Secret Service. Config: `service` (namespace), optional `prefix`. Does not work in headless CI. |
| **KeePass** | `keepass` | Local `.kdbx` database files |
| **password-store** | `password-store` | GPG-encrypted `~/.password-store/` via `pass` CLI |
| **plain** | `plain` | Non-sensitive default values |

## Provider Configuration Examples

### age

```toml
[providers.age]
type = "age"
recipients = ["age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"]
```

```bash
# Generate a dedicated age key
age-keygen -o ~/.config/fnox/age.txt

# Set decryption key
export FNOX_AGE_KEY=$(grep "AGE-SECRET-KEY" ~/.config/fnox/age.txt)

# Encrypt a secret
fnox set DATABASE_URL "postgresql://prod.example.com/db" --provider age
```

Age has first-class SSH key support — use existing keys instead of generating
new ones:

```toml
[providers.age]
type = "age"
recipients = [
  "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGQs...",  # existing SSH pubkey
  "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p",  # age native key
]
```

```bash
# Decrypt using SSH key (age auto-detects ~/.ssh/id_ed25519)
export FNOX_AGE_KEY_FILE=~/.ssh/id_ed25519

# Multiple recipients = any matching key can decrypt
fnox set SECRET "value" --provider age
```

### OS Keychain

```toml
[providers.keychain]
type = "keychain"
service = "fnox"  # namespace to isolate fnox secrets
```

```bash
# Store a secret in OS keychain
fnox set DATABASE_URL "postgresql://localhost/mydb" --provider keychain

# Linux requires libsecret
sudo apt-get install libsecret-1-0 libsecret-1-dev
```

OS-managed encryption with zero external dependencies. Good for local dev
bootstrap (e.g., storing provider tokens), but not usable in headless CI.

### Infisical

```toml
[providers.infisical]
type = "infisical"
project_id = "project-uuid"
environment = "dev"        # must match infisical environment slug exactly
path = "/"                 # secret path within the project
```

Auth is handled by `infisical` CLI login or `INFISICAL_TOKEN` env var.

### Plain (defaults)

```toml
[secrets]
# Non-sensitive defaults (no provider needed)
NODE_ENV = { default = "development" }
LOG_LEVEL = { default = "info" }
PORT = { default = "3000" }

# Encrypted secret with a dev fallback
DATABASE_URL = { provider = "age", value = "encrypted...", default = "postgresql://localhost/dev_db" }
```

The `default` field provides a fallback when the provider is unavailable (e.g.,
local dev without credentials). Never use plain/default for passwords, API keys,
or tokens.

## Profiles

Profiles allow per-environment configuration. They inherit top-level secrets
and can override providers and individual secrets.

```toml
[profiles.dev]
[profiles.dev.providers.infisical]
environment = "dev"

[profiles.staging]
[profiles.staging.providers.infisical]
environment = "staging"

[profiles.prod]
[profiles.prod.providers.infisical]
environment = "prod"

# Per-profile secret overrides (inherits all top-level secrets)
[profiles.prod.secrets]
DATABASE_URL = { provider = "aws-sm", value = "prod/database-url" }
```

List available profiles: `fnox profiles`

Select a profile:

```bash
fnox exec --profile staging -- command
# or
export FNOX_PROFILE=staging
fnox exec -- command
```

## Hierarchical Config Loading

Config is merged in order (later overrides earlier):

1. `~/.config/fnox/config.toml` — global defaults
2. `fnox.toml` in parent directories — monorepo root config
3. `fnox.toml` in current directory — project config
4. `fnox.$FNOX_PROFILE.toml` — profile-specific overrides
5. `fnox.local.toml` — local overrides (gitignored)
6. `--config <path>` flag — explicit override

This enables monorepo setups where child configs override parent configs, and
local configs override everything at the same directory level.

## Core Commands

| Command | Purpose |
|---------|---------|
| `fnox init` | Create fnox.toml in current directory |
| `fnox exec -- cmd` | Run command with secrets injected as env vars |
| `fnox exec --profile prod -- cmd` | Run with specific profile |
| `fnox get SECRET_NAME` | Retrieve a single secret value to stdout |
| `fnox set SECRET_NAME value` | Store a secret (encrypts or stores remotely) |
| `fnox set SECRET_NAME --provider age` | Store with a specific provider |
| `fnox list` | List all configured secret names |
| `fnox import -i .env` | Import secrets from .env file |
| `fnox import -i f.json json` | Import from JSON/YAML/TOML |
| `fnox export` | Export secrets as .env format |
| `fnox export --format json` | Export as JSON |

`fnox set` behavior depends on provider capability:

- **Encryption** providers: encrypts value and stores it inline in fnox.toml
- **Remote** providers: stores value externally and saves a reference

## CI/CD — GitHub Actions

### With age encryption

```yaml
- uses: jdx/mise-action@v3
- name: Run tests with secrets
  env:
    FNOX_AGE_KEY: ${{ secrets.FNOX_AGE_KEY }}
  run: fnox exec -- npm test
```

Generate a dedicated CI key: `age-keygen`, add public key to fnox.toml
recipients, store secret key as GitHub Secret `FNOX_AGE_KEY`.

### With infisical

```yaml
- uses: jdx/mise-action@v3
- name: Run tests with secrets
  env:
    INFISICAL_TOKEN: ${{ secrets.INFISICAL_TOKEN }}
  run: fnox exec -- npm test
```

Use `if_missing = "warn"` for secrets that may not be available in CI.

## Shell Integration

Alternative to mise env plugin — fnox can inject secrets directly via shell
hooks:

```bash
# Add to ~/.bashrc, ~/.zshrc, or fish config
eval "$(fnox activate bash)"   # bash
eval "$(fnox activate zsh)"    # zsh
fnox activate fish | source    # fish
```

On `cd` into a directory with `fnox.toml`, secrets auto-load (`+3 DATABASE_URL,
API_KEY, JWT_SECRET`). On `cd` out, they unload (`-3`).

| Env Var | Purpose |
|---------|---------|
| `FNOX_SHELL_OUTPUT` | `none` / `normal` (default) / `debug` |
| `FNOX_PROFILE` | Profile to load (dev/staging/prod) |

Force reload without changing dirs: `cd .`

> **Note**: If using mise env plugin (`_.fnox-env`), shell integration is
> redundant — use one or the other.

## Import / Export

Migrate from plaintext `.env` files to encrypted storage:

```bash
# Import .env and encrypt with age
fnox import -i .env --provider age

# Import only matching secrets with a prefix
fnox import -i .env --filter "^DATABASE_" --prefix "PROD_"

# Export for Docker Compose / K8s
fnox export --format json --profile production > secrets.json
```

Supported formats: `.env`, JSON, YAML, TOML. Pipe from stdin supported.

## Best Practices

- Keep `fnox.toml` in version control — encrypted values and references are safe
- Use `fnox.local.toml` for personal overrides (add to `.gitignore`)
- Match fnox profile names to infisical environment slugs exactly
- Use age provider for secrets that must work offline or without a server
- Use `if_missing = "warn"` in CI where not all secrets are needed
- Prefer `fnox exec --` over `fnox get` for injecting multiple secrets at once
- Bootstrap pattern: encrypt `INFISICAL_TOKEN` with age, then use infisical for everything else
