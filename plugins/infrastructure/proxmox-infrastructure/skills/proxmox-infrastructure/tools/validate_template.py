#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = ["proxmoxer", "requests"]
# ///
"""
Validate Proxmox VM template health and configuration.

Usage:
    ./validate_template.py --template-id 9000 --node foxtrot
    ./validate_template.py --template-id 9000 --all-nodes

Environment Variables:
    PROXMOX_VE_ENDPOINT - Proxmox API endpoint (e.g., https://192.168.3.5:8006)
    PROXMOX_VE_USERNAME - Username (e.g., root@pam)
    PROXMOX_VE_PASSWORD - Password
    OR
    PROXMOX_VE_API_TOKEN - API token (user@realm!token-id=secret)
"""

import argparse
import os
import sys
from proxmoxer import ProxmoxAPI, ResourceException


class TemplateValidator:
    """Validates Proxmox VM templates."""

    def __init__(self, endpoint: str, auth_type: str, **auth_kwargs):
        """Initialize Proxmox connection."""
        self.endpoint = endpoint.replace("https://", "").replace(":8006", "")

        try:
            if auth_type == "token":
                user, token = auth_kwargs["token"].split("!")
                token_name, token_value = token.split("=")
                self.proxmox = ProxmoxAPI(
                    self.endpoint,
                    user=user,
                    token_name=token_name,
                    token_value=token_value,
                    verify_ssl=False
                )
            else:
                self.proxmox = ProxmoxAPI(
                    self.endpoint,
                    user=auth_kwargs["user"],
                    password=auth_kwargs["password"],
                    verify_ssl=False
                )
        except Exception as e:
            print(f"❌ Failed to connect to Proxmox: {e}", file=sys.stderr)
            sys.exit(1)

    def find_template(self, template_id: int, node: str = None):
        """Find template on cluster."""
        nodes = [node] if node else [n['node'] for n in self.proxmox.nodes.get()]

        for node_name in nodes:
            try:
                vms = self.proxmox.nodes(node_name).qemu.get()
                for vm in vms:
                    if vm['vmid'] == template_id:
                        return node_name, vm
            except ResourceException:
                continue

        return None, None

    def validate_template(self, template_id: int, node: str = None):
        """Validate template configuration."""
        print(f"🔍 Validating template {template_id}...")

        # Find template
        node_name, vm_info = self.find_template(template_id, node)

        if not node_name:
            print(f"❌ Template {template_id} not found", file=sys.stderr)
            return False

        print(f"✓ Found on node: {node_name}")

        # Check if it's actually a template
        if vm_info.get('template', 0) != 1:
            print(f"❌ VM {template_id} is not a template", file=sys.stderr)
            return False

        print(f"✓ Confirmed as template")

        # Get detailed config
        try:
            config = self.proxmox.nodes(node_name).qemu(template_id).config.get()
        except ResourceException as e:
            print(f"❌ Failed to get template config: {e}", file=sys.stderr)
            return False

        # Validation checks
        checks = {
            "Cloud-init drive": self._check_cloudinit(config),
            "QEMU guest agent": self._check_agent(config),
            "SCSI controller": self._check_scsi(config),
            "Boot disk": self._check_boot_disk(config),
            "Serial console": self._check_serial(config),
            "EFI disk": self._check_efi(config),
        }

        # Print results
        print("\n📋 Validation Results:")
        print("-" * 50)

        all_passed = True
        for check_name, (passed, message) in checks.items():
            status = "✓" if passed else "✗"
            print(f"{status} {check_name}: {message}")
            if not passed:
                all_passed = False

        print("-" * 50)

        # Print template info
        print(f"\n📊 Template Info:")
        print(f"  Name: {config.get('name', 'N/A')}")
        print(f"  Memory: {config.get('memory', 'N/A')} MB")
        print(f"  Cores: {config.get('cores', 'N/A')}")
        print(f"  Sockets: {config.get('sockets', 'N/A')}")

        if all_passed:
            print(f"\n✅ Template {template_id} is properly configured")
        else:
            print(f"\n⚠️  Template {template_id} has configuration issues")

        return all_passed

    def _check_cloudinit(self, config):
        """Check for cloud-init drive."""
        for key in config:
            if key.startswith('ide') and 'cloudinit' in str(config[key]):
                return True, f"Found at {key}"
        return False, "Missing cloud-init drive (should be ide2)"

    def _check_agent(self, config):
        """Check for QEMU guest agent."""
        agent = config.get('agent', '0')
        if agent in ['1', 'enabled=1']:
            return True, "Enabled"
        return False, "Not enabled (recommended for IP detection)"

    def _check_scsi(self, config):
        """Check SCSI controller type."""
        scsihw = config.get('scsihw', '')
        if 'virtio' in scsihw:
            return True, f"Using {scsihw}"
        return False, f"Not using virtio-scsi (found: {scsihw or 'none'})"

    def _check_boot_disk(self, config):
        """Check for boot disk."""
        for key in config:
            if key.startswith('scsi') and key != 'scsihw':
                return True, f"Found at {key}"
        return False, "No SCSI disk found"

    def _check_serial(self, config):
        """Check for serial console."""
        if 'serial0' in config:
            return True, "Configured"
        return False, "Not configured (recommended for cloud images)"

    def _check_efi(self, config):
        """Check for EFI disk."""
        if 'efidisk0' in config:
            return True, "Configured"
        return False, "Not configured (needed for UEFI boot)"


def main():
    parser = argparse.ArgumentParser(
        description="Validate Proxmox VM template health and configuration"
    )
    parser.add_argument(
        "--template-id",
        type=int,
        required=True,
        help="Template VM ID (e.g., 9000)"
    )
    parser.add_argument(
        "--node",
        help="Specific Proxmox node to check (default: search all nodes)"
    )
    parser.add_argument(
        "--all-nodes",
        action="store_true",
        help="Search all nodes in cluster"
    )

    args = parser.parse_args()

    # Get authentication from environment
    endpoint = os.getenv("PROXMOX_VE_ENDPOINT")
    api_token = os.getenv("PROXMOX_VE_API_TOKEN")
    username = os.getenv("PROXMOX_VE_USERNAME")
    password = os.getenv("PROXMOX_VE_PASSWORD")

    if not endpoint:
        print("❌ PROXMOX_VE_ENDPOINT environment variable required", file=sys.stderr)
        sys.exit(1)

    # Determine authentication method
    if api_token:
        validator = TemplateValidator(endpoint, "token", token=api_token)
    elif username and password:
        validator = TemplateValidator(endpoint, "password", user=username, password=password)
    else:
        print("❌ Authentication required: set PROXMOX_VE_API_TOKEN or PROXMOX_VE_USERNAME/PASSWORD", file=sys.stderr)
        sys.exit(1)

    # Validate template
    node = None if args.all_nodes else args.node
    success = validator.validate_template(args.template_id, node)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
