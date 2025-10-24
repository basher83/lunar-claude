# =============================================================================
# Basic VM Deployment Example
# =============================================================================
# This is a minimal example for learning the VM module. It shows only the
# required parameters with sensible defaults for everything else.
#
# Use this as a starting point for understanding the module, then refer to
# Triangulum-Prime examples for production-ready configurations.

terraform {
  required_version = ">= 1.0"

  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.69"
    }
  }
}

# Provider configuration (credentials from environment)
provider "proxmox" {
  endpoint = var.proxmox_endpoint
  # Uses PROXMOX_VE_API_TOKEN or PROXMOX_VE_USERNAME/PASSWORD from environment
}

# =============================================================================
# Basic VM Module Usage
# =============================================================================

module "basic_vm" {
  source = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=vm/1.0.1"

  # === REQUIRED: Basic Configuration ===
  vm_type  = "clone"           # Clone from existing template
  pve_node = var.proxmox_node  # Which Proxmox node to deploy on
  vm_name  = var.vm_name       # Name of the VM

  # === REQUIRED: Clone Source ===
  # Specify which template to clone from
  src_clone = {
    datastore_id = "local-lvm"
    tpl_id       = 9000  # Your template VMID
  }

  # === REQUIRED: Disk Configuration ===
  # Define the VM's disk
  vm_disk = {
    scsi0 = {
      datastore_id = "local-lvm"
      size         = 20  # GB
      main_disk    = true
      # Note: file_format, iothread, ssd, discard use optimal defaults
    }
  }

  # === REQUIRED: Network Configuration ===
  # At minimum, configure one network interface
  vm_net_ifaces = {
    net0 = {
      bridge    = "vmbr0"
      ipv4_addr = "${var.ip_address}/24"
      ipv4_gw   = var.gateway
      # Note: model defaults to "virtio", vlan_id defaults to null
    }
  }

  # === REQUIRED: Cloud-init Configuration ===
  vm_init = {
    datastore_id = "local-lvm"

    user = {
      name = var.username
      keys = [var.ssh_public_key]
    }

    dns = {
      domain  = "spaceships.work"
      servers = ["192.168.3.1"]
    }
  }

  # === REQUIRED: EFI Disk (for UEFI boot) ===
  vm_efi_disk = {
    datastore_id = "local-lvm"
    # file_format defaults to "raw"
    # type defaults to "4m"
  }

  # === OPTIONAL OVERRIDES ===
  # These are only shown here for educational purposes.
  # The module already provides these defaults - you DON'T need to specify them!

  # CPU (defaults to 2 cores, "host" type)
  # vm_cpu = {
  #   cores = 2
  #   type  = "host"
  # }

  # Memory (defaults to 2048 MB / 2GB)
  # vm_mem = {
  #   dedicated = 2048
  # }

  # Guest agent (defaults to enabled)
  # vm_agent = {
  #   enabled = true
  # }

  # VM start behavior (defaults: start on deploy, start on boot)
  # vm_start = {
  #   on_deploy = true
  #   on_boot   = true
  # }

  # === Learn More ===
  # See module DEFAULTS.md for complete list of defaults:
  # https://github.com/basher83/Triangulum-Prime/blob/main/terraform-bgp-vm/DEFAULTS.md
}

# =============================================================================
# Outputs
# =============================================================================

output "vm_id" {
  description = "The ID of the created VM"
  value       = module.basic_vm.vm_id
}

output "vm_name" {
  description = "The name of the created VM"
  value       = module.basic_vm.vm_name
}

output "vm_ipv4_addresses" {
  description = "IPv4 addresses assigned to the VM"
  value       = module.basic_vm.ipv4_addresses
}
