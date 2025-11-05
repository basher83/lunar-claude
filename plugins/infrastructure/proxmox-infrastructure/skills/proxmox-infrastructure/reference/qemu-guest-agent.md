# QEMU Guest Agent Integration

## Overview

The QEMU Guest Agent (`qemu-guest-agent`) is a service running inside VMs that enables communication between Proxmox and the guest OS. It provides IP address detection, graceful shutdowns, filesystem freezing for snapshots, and more.

## Why Use QEMU Guest Agent?

**Without Guest Agent:**

- VM IP address unknown to Proxmox
- Shutdown = hard power off
- Snapshots don't freeze filesystem (risk of corruption)
- No guest-level monitoring

**With Guest Agent:**

- Automatic IP address detection
- Graceful shutdown/reboot
- Consistent snapshots with filesystem freeze
- Execute commands inside VM
- Query guest information (hostname, users, OS details)

## Installation in Guest VM

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install qemu-guest-agent
sudo systemctl enable qemu-guest-agent
sudo systemctl start qemu-guest-agent
```

### RHEL/Rocky/AlmaLinux

```bash
sudo dnf install qemu-guest-agent
sudo systemctl enable qemu-guest-agent
sudo systemctl start qemu-guest-agent
```

### Verify Installation

```bash
systemctl status qemu-guest-agent
```

**Expected output:**

```text
● qemu-guest-agent.service - QEMU Guest Agent
     Loaded: loaded (/lib/systemd/system/qemu-guest-agent.service; enabled)
     Active: active (running)
```

## Enable in VM Configuration

### Via Proxmox Web UI

**VM → Hardware → Add → QEMU Guest Agent**

OR edit VM options:

**VM → Options → QEMU Guest Agent → Edit → Check "Use QEMU Guest Agent"**

### Via CLI

```bash
qm set <vmid> --agent 1
```

**With custom options:**

```bash
# Enable with filesystem freeze support
qm set <vmid> --agent enabled=1,fstrim_cloned_disks=1
```

### Via Terraform

```hcl
resource "proxmox_vm_qemu" "vm" {
  name = "my-vm"
  # ... other config ...

  agent = 1  # Enable guest agent
}
```

### Via Ansible

```yaml
- name: Enable QEMU guest agent
  community.proxmox.proxmox_kvm:
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_token_id: "{{ proxmox_token_id }}"
    api_token_secret: "{{ proxmox_token_secret }}"
    node: foxtrot
    vmid: 101
    agent: 1
    update: true
```

## Using Guest Agent

### Check Agent Status

**Via CLI:**

```bash
# Test if agent is responding
qm agent 101 ping

# Get guest info
qm agent 101 info

# Get network interfaces
qm agent 101 network-get-interfaces

# Get IP addresses
qm agent 101 get-osinfo
```

**Example output:**

```json
{
  "result": {
    "id": "ubuntu",
    "kernel-release": "5.15.0-91-generic",
    "kernel-version": "#101-Ubuntu SMP",
    "machine": "x86_64",
    "name": "Ubuntu",
    "pretty-name": "Ubuntu 22.04.3 LTS",
    "version": "22.04",
    "version-id": "22.04"
  }
}
```

### Execute Commands

**Via CLI:**

```bash
# Execute command in guest
qm guest exec 101 -- whoami

# With arguments
qm guest exec 101 -- ls -la /tmp
```

**Via Python API:**

```python
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI('192.168.3.5', user='root@pam', password='pass')

# Execute command
result = proxmox.nodes('foxtrot').qemu(101).agent.exec.post(
    command=['whoami']
)

# Get execution result
pid = result['pid']
exec_status = proxmox.nodes('foxtrot').qemu(101).agent('exec-status').get(pid=pid)
print(exec_status)
```

### Graceful Shutdown/Reboot

**Shutdown (graceful with agent):**

```bash
# Sends ACPI shutdown to guest, waits for agent to shutdown OS
qm shutdown 101

# Force shutdown if doesn't complete in 60s
qm shutdown 101 --timeout 60 --forceStop 1
```

**Reboot:**

```bash
qm reboot 101
```

## Snapshot Integration

### Filesystem Freeze for Consistent Snapshots

When guest agent is enabled, Proxmox can freeze the filesystem before taking a snapshot, ensuring consistency.

**Create snapshot with FS freeze:**

```bash
# Guest agent automatically freezes filesystem
qm snapshot 101 before-upgrade --vmstate 0 --description "Before upgrade"
```

**Rollback to snapshot:**

```bash
qm rollback 101 before-upgrade
```

**Delete snapshot:**

```bash
qm delsnapshot 101 before-upgrade
```

## IP Address Detection

### Automatic IP Assignment

With guest agent, Proxmox automatically detects VM IP addresses.

**View in Web UI:**

VM → Summary → IPs section shows detected IPs

**Via CLI:**

```bash
qm agent 101 network-get-interfaces | jq '.result[] | select(.name=="eth0") | ."ip-addresses"'
```

**Via Python:**

```python
interfaces = proxmox.nodes('foxtrot').qemu(101).agent('network-get-interfaces').get()

for iface in interfaces['result']:
    if iface['name'] == 'eth0':
        for ip in iface.get('ip-addresses', []):
            if ip['ip-address-type'] == 'ipv4':
                print(f"IPv4: {ip['ip-address']}")
```

## Advanced Configuration

### Guest Agent Options

**Full options syntax:**

```bash
qm set <vmid> --agent [enabled=]<1|0>[,fstrim_cloned_disks=<1|0>][,type=<virtio|isa>]
```

**Parameters:**

- `enabled` - Enable/disable guest agent (default: 1)
- `fstrim_cloned_disks` - Run fstrim after cloning disk (default: 0)
- `type` - Agent communication type: virtio or isa (default: virtio)

**Example:**

```bash
# Enable with fstrim on cloned disks
qm set 101 --agent enabled=1,fstrim_cloned_disks=1
```

### Filesystem Trim (fstrim)

For VMs on thin-provisioned storage (LVM-thin, CEPH), fstrim helps reclaim unused space.

**Manual fstrim:**

```bash
# Inside VM
sudo fstrim -av
```

**Automatic on clone:**

```bash
qm set <vmid> --agent enabled=1,fstrim_cloned_disks=1
```

**Scheduled fstrim (inside VM):**

```bash
# Enable weekly fstrim timer
sudo systemctl enable fstrim.timer
sudo systemctl start fstrim.timer
```

## Cloud-Init Integration

### Include in Cloud-Init Template

**During template creation:**

```bash
# Install agent package
virt-customize -a ubuntu-22.04.img \
  --install qemu-guest-agent \
  --run-command "systemctl enable qemu-guest-agent"

# Create VM from image
qm create 9000 --name ubuntu-template --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0
qm importdisk 9000 ubuntu-22.04.img local-lvm
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0
qm set 9000 --agent 1  # Enable guest agent
qm set 9000 --ide2 local-lvm:cloudinit
qm template 9000
```

### Cloud-Init User Data

**Include in cloud-init config:**

```yaml
#cloud-config
packages:
  - qemu-guest-agent

runcmd:
  - systemctl enable qemu-guest-agent
  - systemctl start qemu-guest-agent
```

## Troubleshooting

### Guest Agent Not Responding

**1. Check if service is running in guest:**

```bash
# Inside VM
systemctl status qemu-guest-agent
journalctl -u qemu-guest-agent
```

**2. Check if agent is enabled in VM config:**

```bash
# On Proxmox host
qm config 101 | grep agent
```

**3. Check virtio serial device:**

```bash
# Inside VM
ls -l /dev/virtio-ports/
# Should show: org.qemu.guest_agent.0
```

**4. Restart agent:**

```bash
# Inside VM
sudo systemctl restart qemu-guest-agent
```

**5. Check Proxmox can communicate:**

```bash
# On Proxmox host
qm agent 101 ping
```

### IP Address Not Detected

**Possible causes:**

1. Guest agent not running
2. Network interface not configured
3. DHCP not assigning IP
4. Firewall blocking communication

**Debug:**

```bash
# Check all interfaces
qm agent 101 network-get-interfaces | jq

# Verify cloud-init completed
# Inside VM
cloud-init status
```

### Filesystem Freeze Timeout

**Symptoms:**

Snapshot creation hangs or times out.

**Solution:**

```bash
# Disable FS freeze for snapshots
qm set 101 --agent enabled=1

# Take snapshot without FS freeze
qm snapshot 101 test --vmstate 0
```

### Agent Installed but Not Enabled

**Check VM config:**

```bash
qm config 101 | grep agent
```

**If missing, enable:**

```bash
qm set 101 --agent 1
```

**Restart VM for changes to take effect:**

```bash
qm reboot 101
```

## Best Practices

1. **Always install in templates** - Include qemu-guest-agent in VM templates
2. **Enable during provisioning** - Set `--agent 1` when creating VMs
3. **Use for production VMs** - Critical for graceful shutdowns and monitoring
4. **Enable fstrim for thin storage** - Helps reclaim space on LVM-thin and CEPH
5. **Test before snapshots** - Verify agent works: `qm agent <vmid> ping`
6. **Cloud-init integration** - Automate installation via cloud-init packages
7. **Monitor agent status** - Check agent is running in monitoring tools

## Ansible Automation Example

```yaml
---
- name: Ensure QEMU guest agent is configured
  hosts: proxmox_vms
  become: true
  tasks:
    - name: Install qemu-guest-agent
      ansible.builtin.apt:
        name: qemu-guest-agent
        state: present
      when: ansible_os_family == "Debian"

    - name: Enable and start qemu-guest-agent
      ansible.builtin.systemd:
        name: qemu-guest-agent
        enabled: true
        state: started

    - name: Verify agent is running
      ansible.builtin.systemd:
        name: qemu-guest-agent
      register: agent_status

    - name: Report agent status
      ansible.builtin.debug:
        msg: "Guest agent is {{ agent_status.status.ActiveState }}"
```

## Further Reading

- [Proxmox QEMU Guest Agent Documentation](https://pve.proxmox.com/wiki/Qemu-guest-agent)
- [QEMU Guest Agent Protocol](https://www.qemu.org/docs/master/interop/qemu-ga.html)
