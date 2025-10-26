# Cloud-Init Patterns for Proxmox VE

*Source: <https://pve.proxmox.com/wiki/Cloud-Init_Support*>

## Overview

Cloud-Init is the de facto multi-distribution package that handles early initialization of virtual machines. When a VM starts for the first time, Cloud-Init applies network and SSH key settings configured on the hypervisor.

## Template Creation Workflow

### Download and Import Cloud Image

```bash
# Download Ubuntu cloud image
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img

# Create VM with VirtIO SCSI controller
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci

# Import disk to storage
qm set 9000 --scsi0 local-lvm:0,import-from=/path/to/bionic-server-cloudimg-amd64.img
```

**Important**: Ubuntu Cloud-Init images require `virtio-scsi-pci` controller type for SCSI drives.

### Configure Cloud-Init Components

```bash
# Add Cloud-Init CD-ROM drive
qm set 9000 --ide2 local-lvm:cloudinit

# Set boot order (speeds up boot)
qm set 9000 --boot order=scsi0

# Configure serial console (required for many cloud images)
qm set 9000 --serial0 socket --vga serial0

# Convert to template
qm template 9000
```

## Deploying from Templates

### Clone Template

```bash
# Clone template to new VM
qm clone 9000 123 --name ubuntu2
```

### Configure VM

```bash
# Set SSH public key
qm set 123 --sshkey ~/.ssh/id_rsa.pub

# Configure network
qm set 123 --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
```

## Custom Cloud-Init Configuration

### Using Custom Config Files

Proxmox allows custom cloud-init configurations via the `cicustom` option:

```bash
qm set 9000 --cicustom "user=<volume>,network=<volume>,meta=<volume>"
```

Example using local snippets storage:

```bash
qm set 9000 --cicustom "user=local:snippets/userconfig.yaml"
```

### Dump Generated Config

Use as a base for custom configurations:

```bash
qm cloudinit dump 9000 user
qm cloudinit dump 9000 network
qm cloudinit dump 9000 meta
```

## Cloud-Init Options Reference

### cicustom

Specify custom files to replace automatically generated ones:

- `meta=<volume>` - Meta data (provider specific)
- `network=<volume>` - Network data
- `user=<volume>` - User data
- `vendor=<volume>` - Vendor data

### cipassword

Password for the user. **Not recommended** - use SSH keys instead.

### citype

Configuration format: `configdrive2 | nocloud | opennebula`

- Default: `nocloud` for Linux, `configdrive2` for Windows

### ciupgrade

Automatic package upgrade after first boot (default: `true`)

### ciuser

Username to configure (instead of image's default user)

### ipconfig[n]

IP addresses and gateways for network interfaces.

Format: `[gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>]`

Special values:

- `ip=dhcp` - Use DHCP for IPv4
- `ip6=auto` - Use stateless autoconfiguration (requires cloud-init 19.4+)

### sshkeys

Public SSH keys (one per line, OpenSSH format)

### nameserver

DNS server IP address

### searchdomain

DNS search domains

## Best Practices

1. **Use SSH keys** instead of passwords for authentication
2. **Configure serial console** for cloud images (many require it)
3. **Set boot order** to speed up boot process
4. **Convert to template** for fast linked clone deployment
5. **Store custom configs in snippets** storage (must be on all nodes for migration)
6. **Test with a clone** before modifying template

## Troubleshooting

### Template Won't Boot

- Check if serial console is configured: `qm set <vmid> --serial0 socket --vga serial0`
- Verify boot order: `qm set <vmid> --boot order=scsi0`

### Network Not Configured

- Ensure cloud-init CD-ROM is attached: `qm set <vmid> --ide2 local-lvm:cloudinit`
- Check IP configuration: `qm config <vmid> | grep ipconfig`

### SSH Keys Not Working

- Verify sshkeys format (OpenSSH format, one per line)
- Check cloud-init logs in VM: `cat /var/log/cloud-init.log`
