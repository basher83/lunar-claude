# Basic VM Deployment Example

**Learning objective:** Deploy your first VM using the unified VM module with minimal configuration.

## What This Example Shows

- ✅ Minimal required configuration for VM deployment
- ✅ Cloning from an existing template
- ✅ Static IP address configuration with cloud-init
- ✅ SSH key injection
- ✅ Module defaults (what you DON'T need to specify)

## Prerequisites

1. **Proxmox template** exists (VMID 9000)
   - Create one using: `terraform/netbox-template/` or Ansible playbook
   - Or use Triangulum-Prime template examples

2. **Proxmox API credentials** configured:
   ```bash
   export PROXMOX_VE_ENDPOINT="https://192.168.3.5:8006"
   export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"
   # OR
   export PROXMOX_VE_USERNAME="root@pam"
   export PROXMOX_VE_PASSWORD="your-password"
   ```

3. **SSH public key** available:
   ```bash
   export TF_VAR_ssh_public_key="$(cat ~/.ssh/id_rsa.pub)"
   ```

## Quick Start

### 1. Initialize Terraform

```bash
tofu init
```

### 2. Review the Plan

```bash
tofu plan
```

**Expected resources:**
- 1 VM (cloned from template 9000)
- Cloud-init configuration
- Network interface with static IP

### 3. Deploy

```bash
tofu apply
```

### 4. Verify

```bash
# SSH into the VM
ssh ansible@192.168.3.100

# Check VM in Proxmox
qm status 100  # Or whatever VMID was assigned
```

### 5. Cleanup

```bash
tofu destroy
```

## Understanding the Configuration

### What You MUST Specify

```hcl
# These 6 parameters are required:
vm_type       = "clone"               # Clone from template
pve_node      = "foxtrot"             # Which node
vm_name       = "test-vm-01"          # VM name
src_clone     = { ... }               # Template to clone
vm_disk       = { ... }               # Disk config
vm_net_ifaces = { ... }               # Network config
vm_init       = { ... }               # Cloud-init config
vm_efi_disk   = { ... }               # EFI boot disk
```

### What Uses Defaults

The module provides sensible defaults for:

| Setting | Default | Why It's Good |
|---------|---------|---------------|
| CPU cores | 2 | Minimal baseline |
| Memory | 2048 MB (2GB) | Enough for most services |
| CPU type | `host` | Best performance |
| Guest agent | Enabled | Needed for IP detection |
| BIOS | `ovmf` (UEFI) | Modern, secure |
| Machine | `q35` | Modern chipset |
| Display | Standard VGA | Works everywhere |
| Serial console | Enabled | Troubleshooting |
| RNG device | Enabled | Entropy for crypto |

**See:** [Module DEFAULTS.md](https://github.com/basher83/Triangulum-Prime/blob/main/terraform-bgp-vm/DEFAULTS.md)

## Customization

### Change VM Resources

Override defaults in `main.tf`:

```hcl
module "basic_vm" {
  # ... required params ...

  # Override CPU
  vm_cpu = {
    cores = 4  # Increase to 4 cores
  }

  # Override memory
  vm_mem = {
    dedicated = 8192  # 8GB
  }
}
```

### Use Different Template

Change the template ID:

```hcl
src_clone = {
  datastore_id = "local-lvm"
  tpl_id       = 9001  # Different template
}
```

### Add VLAN Tagging

```hcl
vm_net_ifaces = {
  net0 = {
    bridge    = "vmbr0"
    vlan_id   = 30         # Add VLAN tag
    ipv4_addr = "192.168.3.100/24"
    ipv4_gw   = "192.168.3.1"
  }
}
```

## Common Issues

### Issue: "Template 9000 not found"

**Solution:** Create a template first:
```bash
cd ../../.. # Back to repo root
cd terraform/netbox-template
tofu apply
```

### Issue: "IP address already in use"

**Solution:** Change `ip_address` variable:
```bash
tofu apply -var="ip_address=192.168.3.101"
```

### Issue: "Cannot connect to Proxmox API"

**Solution:** Check credentials:
```bash
echo $PROXMOX_VE_ENDPOINT
echo $PROXMOX_VE_API_TOKEN
```

### Issue: "EFI disk creation failed"

**Solution:** Ensure datastore has space:
```bash
# On Proxmox node
pvesm status
```

## Next Steps

### Learn More

1. **Production Configuration:** See `../02-production-vm/`
   - Shows common overrides for production
   - Resource sizing best practices
   - Tagging and organization

2. **Template Creation:** See `../03-template-creation/`
   - How to create templates from cloud images
   - Template best practices

3. **Complete Examples:** Triangulum-Prime repository
   - [Single VM](https://github.com/basher83/Triangulum-Prime/tree/main/examples/single-vm)
   - [MicroK8s Cluster](https://github.com/basher83/Triangulum-Prime/tree/main/examples/microk8s-cluster)
   - [Custom Cloud-init](https://github.com/basher83/Triangulum-Prime/tree/main/examples/template-with-custom-cloudinit)

### Integration Examples

- **NetBox + DNS:** See `.claude/skills/netbox-powerdns-integration/examples/01-vm-with-dns/`
- **Ansible Configuration:** See `.claude/skills/ansible-best-practices/examples/`

## Module Documentation

- **README:** [terraform-bgp-vm](https://github.com/basher83/Triangulum-Prime/tree/main/terraform-bgp-vm)
- **DEFAULTS:** [DEFAULTS.md](https://github.com/basher83/Triangulum-Prime/blob/main/terraform-bgp-vm/DEFAULTS.md)
- **Full API:** Module variables.tf

## Philosophy: DRY (Don't Repeat Yourself)

This example follows the module's DRY principle:

✅ **Good:** Only specify what differs from defaults
```hcl
vm_cpu = {
  cores = 4  # Only override cores, use default type
}
```

❌ **Bad:** Repeating module defaults
```hcl
vm_cpu = {
  cores = 4
  type  = "host"  # This is already the default!
}
```

**Why?** Reduces maintenance burden and makes changes obvious.
