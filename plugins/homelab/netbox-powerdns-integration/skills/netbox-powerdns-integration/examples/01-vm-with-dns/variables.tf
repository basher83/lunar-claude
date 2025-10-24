variable "proxmox_endpoint" {
  description = "Proxmox API endpoint"
  type        = string
  default     = "https://192.168.3.5:8006"
}

variable "proxmox_node" {
  description = "Proxmox node for deployment"
  type        = string
  default     = "foxtrot"
}

variable "netbox_url" {
  description = "NetBox server URL"
  type        = string
  default     = "https://netbox.spaceships.work"
}

variable "netbox_api_token" {
  description = "NetBox API token"
  type        = string
  sensitive   = true
  # Set via: export TF_VAR_netbox_api_token="your-token"
  # Or use: NETBOX_API_TOKEN environment variable
}

variable "template_id" {
  description = "Proxmox template VMID to clone from"
  type        = number
  default     = 9000
}

variable "vm_name" {
  description = "VM name (short, used in Proxmox)"
  type        = string
  default     = "docker-01-nexus"
}

variable "fqdn" {
  description = "Fully qualified domain name (must follow naming convention: <service>-<NN>-<purpose>.<domain>)"
  type        = string
  default     = "docker-01-nexus.spaceships.work"

  validation {
    condition     = can(regex("^[a-z0-9-]+-\\d{2}-[a-z0-9-]+\\.[a-z0-9.-]+$", var.fqdn))
    error_message = "FQDN must follow naming convention: <service>-<NN>-<purpose>.<domain> (e.g., docker-01-nexus.spaceships.work)"
  }
}

variable "vm_description" {
  description = "VM description (shown in both Proxmox and NetBox)"
  type        = string
  default     = "Docker host for Nexus container registry"
}

variable "ip_address" {
  description = "Static IP address (without CIDR)"
  type        = string
  default     = "192.168.1.100"
}

variable "gateway" {
  description = "Network gateway"
  type        = string
  default     = "192.168.1.1"
}

variable "network_bridge" {
  description = "Proxmox network bridge"
  type        = string
  default     = "vmbr0"
}

variable "vlan_id" {
  description = "VLAN ID (null for no VLAN)"
  type        = number
  default     = 30
}

variable "dns_domain" {
  description = "DNS domain for cloud-init"
  type        = string
  default     = "spaceships.work"
}

variable "dns_server" {
  description = "DNS server IP"
  type        = string
  default     = "192.168.3.1"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
  # Set via: export TF_VAR_ssh_public_key="$(cat ~/.ssh/id_rsa.pub)"
}
