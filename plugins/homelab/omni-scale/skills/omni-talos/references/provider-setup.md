# Provider Setup

The Proxmox provider runs as Docker containers inside the `omni-provider` LXC (CT 200) on Foxtrot.

## File Locations

| File | Purpose |
|------|---------|
| `proxmox-provider/compose.yml` | Docker Compose for provider + Tailscale sidecar |
| `proxmox-provider/config.yaml` | Proxmox API credentials (gitignored) |
| `proxmox-provider/.env` | Environment variables (gitignored) |

## Initial Setup

```bash
# Copy example files
cp proxmox-provider/config.yaml.example proxmox-provider/config.yaml
cp proxmox-provider/.env.example proxmox-provider/.env

# Edit with actual credentials
vim proxmox-provider/config.yaml  # Proxmox API token
vim proxmox-provider/.env         # Tailscale key, Omni service account

# Deploy
cd proxmox-provider
docker compose up -d
```

## Provider Config (config.yaml)

```yaml
proxmox:
  url: "https://192.168.3.5:8006/api2/json"
  tokenID: "terraform@pam!automation"
  tokenSecret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  insecureSkipVerify: true  # Self-signed Proxmox certs
```

For Proxmox API token setup, see `proxmox-permissions.md`.

## Environment Variables (.env)

```bash
TS_AUTHKEY=tskey-auth-xxx          # Tailscale auth key (reusable, ephemeral)
OMNI_SERVICE_ACCOUNT_KEY=xxx       # Omni service account key
```

## Provider Image

**Important:** Use `:local-fix` tag, not `:latest`. Upstream has hostname conflict bug.

```yaml
# In compose.yml
image: ghcr.io/siderolabs/omni-infra-provider-proxmox:local-fix
```

## Verification

After deployment:

```bash
# Check provider registered with Omni
omnictl get infraproviders

# Check provider status
omnictl get infraproviderstatuses

# View provider logs
scripts/provider-ctl.py --logs 50
```
