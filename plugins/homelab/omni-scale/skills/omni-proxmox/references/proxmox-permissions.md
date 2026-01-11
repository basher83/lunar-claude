# Proxmox Permissions for Infrastructure Provider

For production deployments, create a dedicated Proxmox user with minimal permissions rather than using root.

## Current Deployment

| Setting | Value |
|---------|-------|
| Proxmox API | `https://192.168.3.5:8006` |
| API Token | `terraform@pam!automation` |
| Realm | `pam` (system user) |

## Required Permissions

The infrastructure provider needs these Proxmox permissions:

| Permission | Purpose |
|------------|---------|
| `VM.Allocate` | Create new VMs |
| `VM.Config.Disk` | Attach/configure disks |
| `VM.Config.CPU` | Set CPU cores |
| `VM.Config.Memory` | Set RAM |
| `VM.Config.Network` | Configure network interfaces |
| `VM.Config.Options` | Set VM options (boot order, etc.) |
| `VM.PowerMgmt` | Start/stop/reset VMs |
| `Datastore.AllocateSpace` | Allocate storage for disks |
| `Datastore.Audit` | Read storage pool information |

## Creating Dedicated User

Run these commands on a Proxmox node:

```bash
# Create user in Proxmox VE realm
pveum user add omni@pve

# Set password (for testing with username/password auth)
pveum passwd omni@pve

# Grant permissions at datacenter level
pveum aclmod / -user omni@pve -role PVEVMAdmin

# Verify
pveum user list
```

The `PVEVMAdmin` built-in role includes all necessary permissions.

## Creating API Token (Recommended)

API tokens are more secure than username/password:

```bash
# Create token for the omni user
pveum user token add omni@pve omni-provider

# Output example:
# ┌──────────────┬──────────────────────────────────────┐
# │ key          │ value                                │
# ├──────────────┼──────────────────────────────────────┤
# │ full-tokenid │ omni@pve!omni-provider               │
# │ info         │ {"privsep":"1"}                      │
# │ value        │ xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx │
# └──────────────┴──────────────────────────────────────┘
```

Save the token value immediately. It cannot be retrieved again.

## Config.yaml Format

### Current Deployment (Matrix cluster)

```yaml
proxmox:
  url: "https://192.168.3.5:8006/api2/json"
  insecureSkipVerify: true  # Self-signed Proxmox certs

  tokenID: "terraform@pam!automation"
  tokenSecret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Generic API Token Authentication

```yaml
proxmox:
  url: "https://<proxmox-node>:8006/api2/json"
  insecureSkipVerify: true

  tokenID: "omni@pve!omni-provider"
  tokenSecret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Username/Password Authentication (testing only)

```yaml
proxmox:
  url: "https://<proxmox-node>:8006/api2/json"
  insecureSkipVerify: true

  username: "omni"
  password: "your-password"
  realm: "pve"
```

## Realm Options

| Realm | Description |
|-------|-------------|
| `pve` | Proxmox VE authentication (recommended) |
| `pam` | Linux PAM (system users) |
| `ldap` | LDAP/AD integration |

Use `pve` realm for dedicated Proxmox users. Use `pam` only for system accounts like `root`.

## Token Security

**Best practices:**

- Use API tokens instead of passwords
- Create dedicated user (not root)
- Store token in `.env` file (gitignored)
- Rotate tokens periodically
- Revoke tokens when no longer needed

**Revoking a token:**

```bash
pveum user token remove omni@pve omni-provider
```

## Verifying Access

Test API connectivity:

```bash
# With token (Matrix cluster)
curl -k https://192.168.3.5:8006/api2/json/version \
  -H "Authorization: PVEAPIToken=terraform@pam!automation=<secret>"

# List storage pools
curl -k https://192.168.3.5:8006/api2/json/storage \
  -H "Authorization: PVEAPIToken=terraform@pam!automation=<secret>"
```

Successful response includes Proxmox version information or storage pool list.
