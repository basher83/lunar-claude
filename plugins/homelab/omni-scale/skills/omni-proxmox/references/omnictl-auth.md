# omnictl Authentication

The omnictl CLI requires authentication to communicate with Omni. Two methods are available.

## Option 1: Service Account Key (Recommended for Automation)

Service account keys provide non-interactive authentication for scripts and CI/CD.

### Creating a Service Account

1. Open Omni UI
2. Navigate to Settings → Service Accounts
3. Click "Create Service Account"
4. Set appropriate permissions (Admin, Operator, or Reader)
5. Copy the generated key

### Using the Key

**Environment variable:**

```bash
export OMNICTL_SERVICE_ACCOUNT_KEY="your-key-here"
export OMNICTL_ENDPOINT="https://omni.spaceships.work"

omnictl get clusters
```

**Command line:**

```bash
omnictl --omni-url https://omni.spaceships.work \
        --service-account-key "your-key-here" \
        get clusters
```

**In scripts:**

```bash
# Check for existing key or prompt
if [ -z "$OMNICTL_SERVICE_ACCOUNT_KEY" ]; then
  echo "Set OMNICTL_SERVICE_ACCOUNT_KEY environment variable"
  exit 1
fi
```

### Key Permissions

| Role | Capabilities |
|------|--------------|
| Admin | Full access (create/delete clusters, manage users) |
| Operator | Manage clusters (create/scale/delete) |
| Reader | View-only access |

## Option 2: OIDC Browser Flow (Interactive)

For interactive use, omnictl authenticates via browser on first command.

### Triggering Authentication

Any omnictl command triggers OAuth if not already authenticated:

```bash
omnictl get clusters
```

This opens a browser window for Auth0 OIDC authentication. After login, credentials are cached locally.

### Cached Credentials

Credentials are stored in `~/.talos/omni/config` and persist across sessions until they expire.

## Configuration Management

Use `omnictl config` to manage the configuration file:

```bash
# View current config
omnictl config info

# Generate new config (triggers OIDC flow)
omnictl config new --url https://omni.spaceships.work > ~/.talos/omni/config

# Merge additional context
omnictl config merge ./another-config
```

### Configuration File Location

| Variable | Default |
|----------|---------|
| `OMNICONFIG` env | If set, uses this path |
| Default | `~/.talos/omni/config` |
| Deprecated | `$XDG_CONFIG_HOME/omni/config` (read-only fallback) |

### Config File Format

```yaml
contexts:
  default:
    url: https://omni.spaceships.work
    # Auth is cached separately after OIDC flow

current-context: default
```

## Verifying Authentication

Test that authentication works:

```bash
# Should return cluster list (empty is OK)
# Triggers browser auth if not authenticated
omnictl get clusters

# Check infrastructure providers
omnictl get infraproviders

# Check current user context
omnictl user list
```

## Troubleshooting

**"unauthorized" error:**

- Service account key is invalid or expired
- Key doesn't have required permissions
- OIDC session expired (run any command to re-authenticate)

**"connection refused" error:**

- Omni URL is incorrect
- Omni is not running
- Network connectivity issue (check Tailscale)

**"certificate error":**

- Add `--insecure-skip-tls-verify` flag
- Or configure proper TLS certificates in Omni

**Browser doesn't open for OIDC:**

- Check if `xdg-open` (Linux) or `open` (macOS) works
- Manually visit the URL printed in terminal

## Best Practices

1. Use service account keys for automation
2. Use OIDC flow for interactive sessions
3. Store keys in environment variables, not command history
4. Use minimal permissions for service accounts
5. Rotate service account keys periodically
