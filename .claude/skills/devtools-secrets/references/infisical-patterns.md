# Infisical Patterns Reference

## Initial Setup

```bash
# Install (if not via mise)
curl -1sLf 'https://dl.infisical.com/get-cli.sh' | bash

# Initialize project (creates .infisical.json)
infisical init

# Login (interactive browser-based)
infisical login

# Login interactively in terminal
infisical login --interactive

# Login non-interactively (CI/scripting)
infisical login --method=universal-auth \
  --client-id=<client-id> \
  --client-secret=<client-secret>
```

## .infisical.json

Created by `infisical init`. **Safe to commit** — contains no secrets.

```json
{
  "workspaceId": "project-uuid",
  "defaultEnvironment": "dev",
  "gitBranchToEnvironmentMapping": null
}
```

## Core CLI Commands

| Command | Purpose |
|---------|---------|
| `infisical init` | Create .infisical.json for current project |
| `infisical login` | Authenticate (token stored in system keyring) |
| `infisical run -- cmd` | Run command with secrets as env vars |
| `infisical run --env=prod -- cmd` | Run with specific environment |
| `infisical run --path=/apps/api -- cmd` | Run with specific secret path |
| `infisical run --recursive -- cmd` | Include secrets from subfolders |
| `infisical run --watch -- cmd` | Watch for changes, restart on update |
| `infisical secrets` | List secrets for current environment |
| `infisical secrets set KEY=VALUE` | Set a secret |
| `infisical secrets get KEY` | Get a specific secret |
| `infisical secrets delete KEY` | Delete a secret |
| `infisical export` | Export secrets to stdout (dotenv format) |
| `infisical export --format=json` | Export as JSON |
| `infisical export --format=yaml` | Export as YAML |
| `infisical export --format=dotenv-export` | Export with `export` prefix |
| `infisical export --output-file=.env` | Export to file |
| `infisical export --template=tmpl.tpl` | Export using custom template |
| `infisical scan` | Scan repo for leaked secrets (140+ types) |
| `infisical scan --verbose` | Scan full git history |
| `infisical scan install --pre-commit-hook` | Install git pre-commit hook |

## Environment Scoping

Secrets are scoped by **environment** and **path**:

```bash
# Environment slugs: dev, staging, test, prod
infisical run --env=staging -- command

# Secret paths for organizing within an environment
infisical run --env=prod --path=/apps/api -- command

# Recursive: fetch secrets from all subpaths
infisical run --env=prod --path=/apps --recursive -- command
```

Default environment is `dev` if `--env` is not specified.

## Authentication Methods

### Interactive (local development)

```bash
# Browser-based (default)
infisical login

# Terminal-based
infisical login --interactive
```

Token is stored in the system keyring. Has a TTL — re-login when expired.

### Machine Identity (CI/CD, automation)

| Method | Use case | Auth mechanism |
|--------|----------|----------------|
| **Universal Auth** | Platform-agnostic CI/CD | Client ID + Client Secret |
| **Token Auth** | Simple token-based | Static token |
| **AWS Auth** | EC2, Lambda, ECS | AWS IAM role |
| **Azure Auth** | Azure VMs, Functions, AKS | Managed identity |
| **GCP Auth** | Compute Engine, Cloud Run, GKE | Service account |
| **Kubernetes Auth** | Pods in K8s | Service account token |
| **OIDC Auth** | GitHub Actions, GitLab CI | JWT from OIDC provider |

### Universal Auth (most common for CI)

```bash
# Get access token
infisical login --method=universal-auth \
  --client-id=<client-id> \
  --client-secret=<client-secret> \
  --plain --silent

# Or use the token directly
export INFISICAL_TOKEN="<access-token>"
infisical run -- command
```

### INFISICAL_TOKEN

Any command accepts `--token` flag or `INFISICAL_TOKEN` env var:

```bash
export INFISICAL_TOKEN="st.xxx.yyy"
infisical run -- deploy.sh
# or
infisical run --token="st.xxx.yyy" -- deploy.sh
```

## Secret Scanning

Built-in scanner (based on gitleaks) detects 140+ secret types:

```bash
# Scan working directory
infisical scan

# Scan full git history
infisical scan --verbose

# Scan specific path
infisical scan --path ./src

# Install as pre-commit hook (runs on every commit)
infisical scan install --pre-commit-hook
```

This repo installs the pre-commit hook via `mise run hooks-install`.

## CI/CD Patterns

### GitHub Actions — Secrets Action (recommended)

```yaml
- uses: Infisical/secrets-action@v1.0.7
  with:
    method: "universal-auth"
    client-id: ${{ secrets.INFISICAL_CLIENT_ID }}
    client-secret: ${{ secrets.INFISICAL_CLIENT_SECRET }}
    env-slug: "prod"
    project-slug: "my-project"
```

### GitHub Actions — OIDC Auth (no stored secrets)

```yaml
permissions:
  id-token: write

steps:
  - uses: Infisical/secrets-action@v1.0.7
    with:
      method: "oidc"
      env-slug: "dev"
      project-slug: "my-project"
      identity-id: "6b579c00-..."
```

### GitHub Actions — CLI with fnox

```yaml
- uses: jdx/mise-action@v3
- name: Run with secrets
  env:
    INFISICAL_TOKEN: ${{ secrets.INFISICAL_TOKEN }}
  run: fnox exec -- npm test
```

### Generic CI — Universal Auth

```bash
# Authenticate and capture token
export INFISICAL_TOKEN=$(infisical login \
  --method=universal-auth \
  --client-id="$INFISICAL_CLIENT_ID" \
  --client-secret="$INFISICAL_CLIENT_SECRET" \
  --plain --silent)

# Use in subsequent commands
infisical run --env=prod -- ./deploy.sh
```

## Infisical as fnox Provider vs Standalone

| Approach | When to use |
|----------|-------------|
| **fnox + infisical** | Multiple secret backends, local dev, unified interface |
| **infisical standalone** | Simple setup, single backend, CI/CD pipelines |

When using fnox, infisical is configured as a provider in `fnox.toml`. The
`infisical` CLI must still be installed and authenticated — fnox calls it
under the hood.

## Best Practices

- Always run `infisical scan` before pushing (or install the pre-commit hook)
- Use machine identity auth in CI/CD, never user credentials
- Use OIDC auth in GitHub Actions when possible (no stored secrets needed)
- Keep `.infisical.json` in version control for team consistency
- Use environment-specific secrets (dev/staging/prod), not a single set
- Use `--path` to organize secrets by service/component within an environment
- Use `--watch` during local development for live secret reloading
- Rotate machine identity credentials periodically
- Prefer `infisical run --` over manual `export` for secret injection
