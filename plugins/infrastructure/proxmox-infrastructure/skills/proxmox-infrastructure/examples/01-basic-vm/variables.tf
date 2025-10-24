variable "proxmox_endpoint" {
  description = "Proxmox API endpoint (e.g., https://192.168.3.5:8006)"
  type        = string
  default     = "https://192.168.3.5:8006"
}

variable "proxmox_node" {
  description = "Proxmox node to deploy on"
  type        = string
  default     = "foxtrot"
}

variable "vm_name" {
  description = "Name of the VM"
  type        = string
  default     = "test-vm-01"
}

variable "ip_address" {
  description = "Static IP address for the VM (without CIDR)"
  type        = string
  default     = "192.168.3.100"
}

variable "gateway" {
  description = "Network gateway"
  type        = string
  default     = "192.168.3.1"
}

variable "username" {
  description = "VM username for cloud-init"
  type        = string
  default     = "ansible"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
  # Set via environment variable or tfvars file
}
