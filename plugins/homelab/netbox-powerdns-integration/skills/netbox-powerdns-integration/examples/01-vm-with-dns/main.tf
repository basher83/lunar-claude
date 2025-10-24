# =============================================================================
# VM with Automatic DNS Registration
# =============================================================================
# This example demonstrates the complete infrastructure automation workflow:
#   1. Create VM in Proxmox (using unified module)
#   2. Register IP address in NetBox with DNS name
#   3. DNS records automatically created in PowerDNS (via netbox-powerdns-sync plugin)
#   4. Ready for Ansible configuration management
#
# Result: Fully automated infrastructure from VM → DNS → Configuration

terraform {
  required_version = ">= 1.0"

  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.69"
    }
    netbox = {
      source  = "e-breuninger/netbox"
      version = "~> 5.0.0"
    }
  }
}

# === Proxmox Provider ===
provider "proxmox" {
  endpoint = var.proxmox_endpoint
  # Credentials from environment:
  # PROXMOX_VE_API_TOKEN or PROXMOX_VE_USERNAME/PASSWORD
}

# === NetBox Provider ===
provider "netbox" {
  server_url = var.netbox_url
  api_token  = var.netbox_api_token
  # Or use environment: NETBOX_API_TOKEN
}

# =============================================================================
# Step 1: Create VM in Proxmox
# =============================================================================

module "docker_host" {
  source = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=vm/1.0.1"

  # VM Configuration
  vm_type  = "clone"
  pve_node = var.proxmox_node
  vm_name  = var.vm_name

  # Clone from template
  src_clone = {
    datastore_id = "local-lvm"
    tpl_id       = var.template_id
  }

  # Production-ready resources
  vm_cpu = {
    cores = 4  # Docker workload
  }

  vm_mem = {
    dedicated = 8192  # 8GB for containers
  }

  # Disk configuration
  vm_disk = {
    scsi0 = {
      datastore_id = "local-lvm"
      size         = 100  # Larger for Docker images
      main_disk    = true
    }
  }

  # Network with VLAN
  vm_net_ifaces = {
    net0 = {
      bridge    = var.network_bridge
      vlan_id   = var.vlan_id
      ipv4_addr = "${var.ip_address}/24"
      ipv4_gw   = var.gateway
    }
  }

  # Cloud-init
  vm_init = {
    datastore_id = "local-lvm"

    user = {
      name = "ansible"
      keys = [var.ssh_public_key]
    }

    dns = {
      domain  = var.dns_domain
      servers = [var.dns_server]
    }
  }

  # EFI disk
  vm_efi_disk = {
    datastore_id = "local-lvm"
  }

  # Tags for organization
  vm_tags = ["terraform", "docker-host", "production"]
}

# =============================================================================
# Step 2: Register IP in NetBox with DNS Name
# =============================================================================

resource "netbox_ip_address" "docker_host" {
  ip_address  = "${var.ip_address}/24"
  dns_name    = var.fqdn  # e.g., docker-01-nexus.spaceships.work
  status      = "active"
  description = var.vm_description

  # CRITICAL: This tag triggers automatic DNS sync via netbox-powerdns-sync plugin
  tags = [
    "terraform",
    "production-dns",  # ← Matches zone rule in NetBox PowerDNS Sync plugin
    "docker-host"
  ]

  # Ensure VM is created first
  depends_on = [module.docker_host]

  lifecycle {
    # Prevent accidental deletion of IP registration
    prevent_destroy = false  # Set to true for production
  }
}

# =============================================================================
# Step 3: DNS Records Created Automatically
# =============================================================================
#
# The netbox-powerdns-sync plugin automatically creates:
#   - A record:   docker-01-nexus.spaceships.work → 192.168.1.100
#   - PTR record: 100.1.168.192.in-addr.arpa → docker-01-nexus.spaceships.work
#
# No manual DNS configuration needed!
#
# Verify with:
#   dig @192.168.3.1 docker-01-nexus.spaceships.work +short
#   dig @192.168.3.1 -x 192.168.1.100 +short

# =============================================================================
# Outputs
# =============================================================================

output "vm_id" {
  description = "Proxmox VM ID"
  value       = module.docker_host.vm_id
}

output "vm_name" {
  description = "VM name"
  value       = module.docker_host.vm_name
}

output "vm_ip" {
  description = "VM IP address"
  value       = var.ip_address
}

output "fqdn" {
  description = "Fully qualified domain name (with automatic DNS)"
  value       = var.fqdn
}

output "netbox_ip_id" {
  description = "NetBox IP address ID"
  value       = netbox_ip_address.docker_host.id
}

output "ssh_command" {
  description = "SSH command to access the VM"
  value       = "ssh ansible@${var.fqdn}"
}

output "verification_commands" {
  description = "Commands to verify DNS resolution"
  value = {
    forward = "dig @${var.dns_server} ${var.fqdn} +short"
    reverse = "dig @${var.dns_server} -x ${var.ip_address} +short"
  }
}
