# Common Mistakes and Anti-Patterns

Lessons learned from real-world Proxmox deployments. Avoid these pitfalls to save time and frustration.

## VM Provisioning with OpenTofu

**Note**: Use `tofu` CLI (not `terraform`). All examples use OpenTofu.

### ❌ Cloud-Init File Not on Target Node

**Problem**: `tofu plan` succeeds but VM fails to start or configure properly.

```hcl
# BAD - Cloud-init file only exists locally
resource "proxmox_virtual_environment_vm" "example" {
  initialization {
    user_data_file_id = "local:snippets/user-data.yaml"  # File doesn't exist on node!
  }
}
```

**Solution**: Cloud-init YAML file MUST exist on the target Proxmox node's datastore.

```bash
# Upload to Proxmox node first
scp user-data.yaml root@foxtrot:/var/lib/vz/snippets/

# Or use Ansible to deploy it
ansible proxmox_nodes -m copy -a "src=user-data.yaml dest=/var/lib/vz/snippets/"
```

**Reference**: See `terraform/netbox-template/user-data.yaml.example` for the required format.

---

### ❌ Template Missing on Target Node

**Problem**: `tofu apply` fails with "template not found" error.

```hcl
# BAD - Template referenced but doesn't exist
resource "proxmox_virtual_environment_vm" "example" {
  node_name = "foxtrot"
  clone {
    vm_id = 9000  # Template doesn't exist on foxtrot!
  }
}
```

**Solution**: Ensure template exists on the specific node you're deploying to.

```bash
# Check template exists
ssh root@foxtrot "qm list | grep 9000"

# Clone template to another node if needed
ssh root@foxtrot "qm clone 9000 9000 --pool templates"
```

**Better**: Use Ansible playbook to create templates consistently across nodes:
```bash
cd ansible && uv run ansible-playbook playbooks/proxmox-build-template.yml
```

---

### ❌ Remote Backend Configuration Errors

**Problem**: OpenTofu fails to authenticate with Proxmox when using Scalr remote backend.

```hcl
# BAD - Incorrect provider config for remote backend
provider "proxmox" {
  endpoint = var.proxmox_api_url
  ssh {
    agent = true  # ❌ Doesn't work with remote backend!
  }
}
```

**Solution (Remote Backend - Scalr)**:

```hcl
provider "proxmox" {
  endpoint = var.proxmox_api_url
  username = var.proxmox_username  # Must use variables
  password = var.proxmox_password  # Must use variables

  ssh {
    agent = false  # Critical: false for remote backend
    username = var.ssh_username
  }
}
```

Required environment variables:
```bash
export SCALR_HOSTNAME="your-scalr-host"
export SCALR_TOKEN="your-scalr-token"
export TF_VAR_proxmox_username="root@pam"
export TF_VAR_proxmox_password="your-password"
```

**Solution (Local Testing)**:

```hcl
provider "proxmox" {
  endpoint = var.proxmox_api_url

  ssh {
    agent = true   # Use SSH agent for local testing
    username = "root"
  }
}
```

**Reference Architecture**:
- Local examples: `terraform/examples/`
- Versioned root modules: `basher83/Triangulum-Prime/terraform-bgp-vm`

---

## Template Creation

### ❌ Cloud Image Not Downloaded to Target Node

**Problem**: Ansible playbook fails when creating template from cloud image.

```yaml
# BAD - Assuming image exists
- name: Create VM from cloud image
  ansible.builtin.command: >
    qm importdisk {{ template_id }} ubuntu-22.04.img local-lvm
  # Fails: ubuntu-22.04.img doesn't exist!
```

**Solution**: Download cloud image to target node first.

```yaml
# GOOD - Download first
- name: Download Ubuntu cloud image
  ansible.builtin.get_url:
    url: https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
    dest: /tmp/ubuntu-22.04.img
    checksum: sha256:...

- name: Import disk to VM
  ansible.builtin.command: >
    qm importdisk {{ template_id }} /tmp/ubuntu-22.04.img local-lvm
```

**Reference**: See `ansible/playbooks/proxmox-build-template.yml` for complete workflow.

---

### ❌ Cloud-Init Snippet Format Violations

**Problem**: VM boots but cloud-init doesn't configure properly.

```yaml
# BAD - Wrong format
#cloud-config
users:
  - name: admin
    sudo: ALL=(ALL) NOPASSWD:ALL
# Missing critical fields!
```

**Solution**: Use the standardized snippet format pre-configured for Ansible.

```yaml
# GOOD - Complete format
#cloud-config
users:
  - name: ansible
    groups: sudo
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAA...

package_update: true
package_upgrade: false

packages:
  - qemu-guest-agent
  - python3
  - python3-pip

runcmd:
  - systemctl enable qemu-guest-agent
  - systemctl start qemu-guest-agent
```

**Critical Requirements**:
- ✅ MUST include `qemu-guest-agent` package
- ✅ MUST include `python3` for Ansible compatibility
- ✅ MUST configure SSH key for Ansible user
- ✅ MUST enable qemu-guest-agent service

**Reference Format**: `terraform/netbox-template/user-data.yaml.example`

---

### ❌ Mixing Terraform and Ansible Provisioning

**Problem**: Confusion about which tool is responsible for what.

**Anti-Pattern**:
```hcl
# BAD - Complex provisioning in Terraform
resource "proxmox_virtual_environment_vm" "example" {
  initialization {
    user_data_file_id = "local:snippets/complex-setup.yaml"
    # Hundreds of lines of cloud-init doing app setup
  }
}
```

**Best Practice**: Clear separation of concerns.

**OpenTofu Responsibility**:
- VM resource allocation (CPU, memory, disk)
- Network configuration
- Basic cloud-init (user, SSH keys, qemu-guest-agent)
- Infrastructure provisioning

**Ansible Responsibility**:
- Application installation
- Configuration management
- Service orchestration
- Ongoing management

**Pattern**:
1. OpenTofu: Provision VM with minimal cloud-init
2. Cloud-init: Create ansible user, install qemu-guest-agent, python3
3. Ansible: Configure everything else

**Reference Architecture**:
- Template creation: `basher83/Triangulum-Prime/deployments/homelab/templates`
- OpenTofu examples: `terraform/examples/`

---

## Best Practices Summary

### Template Creation
1. ✅ Download cloud images to target node before import
2. ✅ Use standardized cloud-init snippet format
3. ✅ Always include qemu-guest-agent
4. ✅ Keep cloud-init minimal - let Ansible handle configuration
5. ✅ Reference: `basher83/Triangulum-Prime/deployments/homelab/templates`

### OpenTofu Provisioning
1. ✅ Verify template exists on target node
2. ✅ Upload cloud-init snippets before referencing
3. ✅ Use `ssh.agent = false` for remote backends (Scalr)
4. ✅ Use `ssh.agent = true` for local testing
5. ✅ Set credentials via OpenTofu variables, not hardcoded
6. ✅ Reference: `terraform/examples/` and `basher83/Triangulum-Prime`

### Workflow
1. ✅ Create template once per node (or sync across nodes)
2. ✅ Upload cloud-init snippets to `/var/lib/vz/snippets/`
3. ✅ Provision VM via OpenTofu (infrastructure)
4. ✅ Configure VM via Ansible (applications/services)

---

## Quick Troubleshooting

### VM Won't Start After tofu apply

**Check**:
1. Does template exist? `qm list | grep <template-id>`
2. Does cloud-init file exist? `ls -la /var/lib/vz/snippets/`
3. Is qemu-guest-agent installed? `qm agent <vmid> ping`

### tofu Can't Connect to Proxmox

**Remote Backend**:
1. `ssh.agent = false`? ✅
2. `SCALR_HOSTNAME` and `SCALR_TOKEN` set? ✅
3. Using OpenTofu variables for credentials? ✅

**Local Testing**:
1. `ssh.agent = true`? ✅
2. SSH key in agent? `ssh-add -l` ✅
3. Can you SSH to node? `ssh root@foxtrot` ✅

### Cloud-Init Didn't Configure VM

**Check**:
1. File format matches `user-data.yaml.example`? ✅
2. Includes qemu-guest-agent? ✅
3. Includes python3? ✅
4. VM console logs: `qm terminal <vmid>` then check `/var/log/cloud-init.log`
