# VM with Automatic DNS Registration

**Learning objective:** Experience the full infrastructure automation workflow from VM creation to DNS resolution.

## What This Example Demonstrates

This is the "holy grail" of infrastructure automation - deploy infrastructure and have DNS automatically configured:

```text
Terraform Deploy → Proxmox VM Created → NetBox IP Registered
→ PowerDNS Records Auto-Created → Ready for Ansible
```

**Benefits:**

- ✅ No manual DNS configuration
- ✅ Single source of truth (NetBox)
- ✅ Audit trail for all infrastructure changes
- ✅ Automatic forward + reverse DNS
- ✅ Ready for dynamic inventory

## Architecture

```text
┌──────────────┐
│  Terraform   │
└──────┬───────┘
       │
       ├─ Creates VM in Proxmox ─────────────► VM: docker-01-nexus
       │                                       IP: 192.168.1.100
       │
       └─ Registers IP in NetBox ────────────► NetBox IPAM
                  │                            Tags: ["production-dns"]
                  │
                  │ netbox-powerdns-sync plugin (automatic)
                  │
                  ▼
           ┌────────────┐
           │  PowerDNS  │
           └─────┬──────┘
                 │
                 ├─► A record:   docker-01-nexus.spaceships.work → 192.168.1.100
                 └─► PTR record: 100.1.168.192.in-addr.arpa → docker-01-nexus.spaceships.work
```

## Prerequisites

### 1. Proxmox Template

Template must exist (default: VMID 9000):

```bash
# Create using Virgo-Core template deployment
cd ../../../terraform/netbox-template
tofu apply
```

### 2. NetBox Configuration

**NetBox PowerDNS Sync Plugin** must be configured with:

- Zone: `spaceships.work`
- Tag rule matching: `production-dns`
- PowerDNS server connection configured

See: [../../reference/sync-plugin-reference.md](../../reference/sync-plugin-reference.md)

### 3. Environment Variables

```bash
# Proxmox
export PROXMOX_VE_ENDPOINT="https://192.168.3.5:8006"
export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"

# NetBox
export NETBOX_API_TOKEN="your-netbox-token"
export TF_VAR_netbox_api_token="$NETBOX_API_TOKEN"

# SSH Key
export TF_VAR_ssh_public_key="$(cat ~/.ssh/id_rsa.pub)"
```

### 4. DNS Naming Convention

FQDN must follow: `<service>-<NN>-<purpose>.<domain>`

**Validate name first:**

```bash
../../tools/validate_dns_naming.py docker-01-nexus.spaceships.work
```

## Quick Start

### 1. Initialize

```bash
tofu init
```

### 2. Plan

```bash
tofu plan
```

**Expected resources:**

- 1 Proxmox VM (docker-01-nexus)
- 1 NetBox IP address (192.168.1.100)
- DNS records created automatically (not shown in plan)

### 3. Deploy

```bash
tofu apply
```

**Wait 30 seconds** for DNS propagation (netbox-powerdns-sync runs async).

### 4. Verify Complete Workflow

#### Step 1: Check VM exists

```bash
# On Proxmox node
qm status $(terraform output -raw vm_id)
```

#### Step 2: Check NetBox registration

```bash
curl -H "Authorization: Token $NETBOX_API_TOKEN" \
  "https://netbox.spaceships.work/api/ipam/ip-addresses/?address=192.168.1.100" | jq
```

#### Step 3: Verify DNS forward resolution

```bash
dig @192.168.3.1 docker-01-nexus.spaceships.work +short
# Expected: 192.168.1.100
```

#### Step 4: Verify DNS reverse resolution

```bash
dig @192.168.3.1 -x 192.168.1.100 +short
# Expected: docker-01-nexus.spaceships.work.
```

#### Step 5: SSH into VM

```bash
ssh ansible@docker-01-nexus.spaceships.work
# or
ssh ansible@192.168.1.100
```

### 5. Cleanup

```bash
tofu destroy
```

**Note:** DNS records are automatically removed when NetBox IP is deleted.

## How It Works

### The Magic Tag: `production-dns`

```hcl
resource "netbox_ip_address" "docker_host" {
  tags = [
    "terraform",
    "production-dns",  # ← This triggers DNS automation
    "docker-host"
  ]
}
```

The `production-dns` tag matches a zone rule in NetBox PowerDNS Sync plugin configuration.

### NetBox PowerDNS Sync Plugin

**Configuration (in NetBox):**

```python
# Plugins → NetBox PowerDNS Sync → Zones → spaceships.work
zone_config = {
    "name": "spaceships.work",
    "powerdns_server": "PowerDNS Server 1",
    "tag_match": ["production-dns"],  # ← Matches our tag
    "naming_method": "device",  # Use device/IP name
    "auto_sync": True,
    "sync_schedule": "*/5 * * * *"  # Every 5 minutes
}
```

**What happens:**

1. IP address created in NetBox with `production-dns` tag
2. Plugin detects new IP matches zone rule
3. Plugin calls PowerDNS API to create records:
   - A record from `dns_name` field
   - PTR record from IP address
4. Records appear in DNS within 30 seconds

## Customization

### Different Service Type

```hcl
# In terraform.tfvars or as -var
vm_name = "k8s-01-master"
fqdn    = "k8s-01-master.spaceships.work"
```

### Development Environment

Use different domain and tags:

```hcl
variable "dns_domain" {
  default = "dev.spaceships.work"
}

resource "netbox_ip_address" "docker_host" {
  tags = ["terraform", "dev-dns", "docker-host"]  # Different tag for dev zone
}
```

### Multiple Environments

```bash
# Production
tofu apply -var-file=prod.tfvars

# Development
tofu apply -var-file=dev.tfvars
```

## Troubleshooting

### DNS Records Not Created

**1. Check NetBox IP registration:**

```bash
curl -H "Authorization: Token $NETBOX_API_TOKEN" \
  "https://netbox.spaceships.work/api/ipam/ip-addresses/?dns_name=docker-01-nexus.spaceships.work" | jq
```

Verify:

- IP exists in NetBox
- Has `production-dns` tag
- `dns_name` field is set

**2. Check zone configuration:**

- NetBox → Plugins → NetBox PowerDNS Sync → Zones
- Verify `spaceships.work` zone exists
- Check tag rules match `production-dns`

**3. Check sync results:**

- NetBox → Plugins → NetBox PowerDNS Sync → Zones → spaceships.work
- Click "Sync Now" to manually trigger
- Review sync results for errors

**4. Check PowerDNS:**

```bash
# Query PowerDNS API directly
curl -H "X-API-Key: $POWERDNS_API_KEY" \
  http://192.168.3.1:8081/api/v1/servers/localhost/zones/spaceships.work | jq
```

### SSH Connection Fails

**Try IP first:**

```bash
ssh ansible@192.168.1.100
```

If IP works but FQDN doesn't:

- DNS not propagated yet (wait 30s)
- Check DNS resolution: `dig @192.168.3.1 docker-01-nexus.spaceships.work`

### NetBox Provider Authentication

**Error:** `authentication failed`

**Solution:**

```bash
# Test API token
curl -H "Authorization: Token $NETBOX_API_TOKEN" \
  https://netbox.spaceships.work/api/status/ | jq

# Regenerate token if needed
# NetBox → Admin → API Tokens → Create
```

## Integration with Ansible

After deployment, use for Ansible configuration:

```yaml
---
# Ansible playbook using NetBox dynamic inventory
- name: Configure Docker hosts
  hosts: tag_docker_host  # From NetBox tags
  become: true

  tasks:
    - name: Install Docker
      ansible.builtin.apt:
        name: docker.io
        state: present
```

**Run with dynamic inventory:**

```bash
cd ../../../ansible
ansible-playbook -i inventory/netbox.yml playbooks/configure-docker.yml
```

See: [../../workflows/ansible-dynamic-inventory.md](../../workflows/ansible-dynamic-inventory.md)

## Next Steps

### Learn More Workflows

- **Bulk Deployment:** `../02-bulk-deployment/` (coming soon)
- **DNS Automation Guide:** [../../workflows/dns-automation.md](../../workflows/dns-automation.md)
- **Naming Conventions:** [../../workflows/naming-conventions.md](../../workflows/naming-conventions.md)

### Production Checklist

Before using in production:

- [ ] NetBox PowerDNS Sync plugin tested and working
- [ ] DNS naming convention documented
- [ ] Zone rules configured for all environments
- [ ] API tokens secured (not in version control)
- [ ] Backup/restore procedures for NetBox
- [ ] Monitoring for DNS sync failures
- [ ] Documentation for team

## Benefits of This Approach

**Single Source of Truth:**

- All infrastructure documented in NetBox
- DNS automatically matches reality
- Easy to audit what exists

**Automation:**

- No manual DNS configuration
- Reduced human error
- Faster deployments

**Consistency:**

- Naming convention enforced
- Tag-based organization
- Audit trail via Terraform

**Integration:**

- Ansible dynamic inventory
- Monitoring integrations
- IPAM + DNS + DCIM in one place

## Related Documentation

- [NetBox Provider Guide](../../reference/terraform-provider-guide.md)
- [PowerDNS Sync Plugin](../../reference/sync-plugin-reference.md)
- [DNS Naming Conventions](../../workflows/naming-conventions.md)
- [DNS Automation Workflows](../../workflows/dns-automation.md)
