#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pynetbox>=7.0.0",
#   "infisical-python>=2.3.3",
#   "rich>=13.0.0",
# ]
# [tool.uv.metadata]
# purpose = "api-client-example"
# team = "infrastructure"
# author = "devops@spaceships.work"
# ///

"""
NetBox API Client Example

Demonstrates best practices for API client scripts using uv:
- PEP 723 inline dependencies
- Infisical for secrets management
- Error handling and validation
- Rich output formatting
- Type hints and documentation

This is a production-ready example showing all patterns together.

Usage:
    # List Matrix cluster VMs
    ./netbox_client.py

    # Query specific VM
    ./netbox_client.py --vm docker-01

Example output:
    Matrix Cluster Virtual Machines
    ┌────┬───────────┬──────┬─────────┬──────────────┬──────────────────────────────────┐
    │ ID │ Name      │vCPUs │Memory MB│ Status       │ Primary IP                       │
    ├────┼───────────┼──────┼─────────┼──────────────┼──────────────────────────────────┤
    │ 1  │ docker-01 │ 4    │ 8192    │ active       │ 192.168.3.10/24                  │
    │ 2  │ k8s-01    │ 8    │ 16384   │ active       │ 192.168.3.20/24                  │
    └────┴───────────┴──────┴─────────┴──────────────┴──────────────────────────────────┘
"""

import re
import sys
from typing import Optional
from dataclasses import dataclass

import pynetbox
from infisical import InfisicalClient
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class NetBoxConfig:
    """NetBox connection configuration."""
    url: str = "https://netbox.spaceships.work"
    project_id: str = "7b832220-24c0-45bc-a5f1-ce9794a31259"
    environment: str = "prod"
    path: str = "/matrix"


# ============================================================================
# Authentication
# ============================================================================

def get_netbox_client(config: NetBoxConfig) -> Optional[pynetbox.api]:
    """
    Get authenticated NetBox API client.

    Uses Infisical to securely retrieve API token (Virgo-Core security pattern).

    Args:
        config: NetBox configuration

    Returns:
        Authenticated pynetbox client or None on error

    Raises:
        Exception: If token cannot be retrieved or connection fails
    """
    try:
        # Get token from Infisical (never hardcoded)
        client = InfisicalClient()
        token = client.get_secret(
            secret_name="NETBOX_API_TOKEN",
            project_id=config.project_id,
            environment=config.environment,
            path=config.path
        ).secret_value

        if not token:
            raise ValueError("NETBOX_API_TOKEN is empty")

        # Connect to NetBox
        nb = pynetbox.api(config.url, token=token)

        # Test connection
        _ = nb.status()

        return nb

    except Exception as e:
        console.print(f"[red]Failed to connect to NetBox: {e}[/red]")
        return None


# ============================================================================
# Data Validation
# ============================================================================

def validate_vm_name(name: str) -> bool:
    """
    Validate VM name format.

    Pattern: lowercase letters, numbers, hyphens only
    Example: docker-01, k8s-01-master

    Args:
        name: VM name to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-z0-9-]+$'
    return bool(re.match(pattern, name))


# ============================================================================
# NetBox Queries
# ============================================================================

def get_cluster_vms(nb: pynetbox.api, cluster_name: str = "Matrix") -> list:
    """
    Get all VMs in a cluster.

    Args:
        nb: NetBox API client
        cluster_name: Cluster name to query

    Returns:
        List of VM objects
    """
    try:
        vms = nb.virtualization.virtual_machines.filter(cluster=cluster_name.lower())
        return list(vms)

    except Exception as e:
        console.print(f"[red]Error querying VMs: {e}[/red]")
        return []


def get_vm_details(nb: pynetbox.api, vm_name: str) -> Optional[dict]:
    """
    Get detailed information about a VM.

    Args:
        nb: NetBox API client
        vm_name: VM name

    Returns:
        VM details dict or None if not found
    """
    try:
        # Validate name
        if not validate_vm_name(vm_name):
            console.print(f"[red]Invalid VM name format: {vm_name}[/red]")
            return None

        vm = nb.virtualization.virtual_machines.get(name=vm_name)

        if not vm:
            console.print(f"[yellow]VM '{vm_name}' not found[/yellow]")
            return None

        # Get interfaces
        interfaces = nb.virtualization.interfaces.filter(virtual_machine_id=vm.id)

        # Get IPs
        ips = []
        for iface in interfaces:
            iface_ips = nb.ipam.ip_addresses.filter(vminterface_id=iface.id)
            ips.extend(iface_ips)

        return {
            "vm": vm,
            "interfaces": list(interfaces),
            "ips": ips
        }

    except Exception as e:
        console.print(f"[red]Error getting VM details: {e}[/red]")
        return None


# ============================================================================
# Output Formatting
# ============================================================================

def display_vms_table(vms: list) -> None:
    """
    Display VMs in a formatted table.

    Args:
        vms: List of VM objects
    """
    if not vms:
        console.print("[yellow]No VMs found[/yellow]")
        return

    table = Table(title="Matrix Cluster Virtual Machines")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("vCPUs", justify="right")
    table.add_column("Memory (MB)", justify="right")
    table.add_column("Status")
    table.add_column("Primary IP", style="yellow")

    for vm in vms:
        table.add_row(
            str(vm.id),
            vm.name,
            str(vm.vcpus) if vm.vcpus else "N/A",
            str(vm.memory) if vm.memory else "N/A",
            vm.status.value if hasattr(vm.status, 'value') else str(vm.status),
            str(vm.primary_ip4.address) if vm.primary_ip4 else "N/A"
        )

    console.print(table)
    console.print(f"\n[green]Total VMs: {len(vms)}[/green]")


def display_vm_details(details: dict) -> None:
    """
    Display detailed VM information.

    Args:
        details: VM details dict from get_vm_details()
    """
    vm = details["vm"]
    interfaces = details["interfaces"]
    ips = details["ips"]

    # VM info panel
    info = (
        f"[green]ID:[/green] {vm.id}\n"
        f"[green]Name:[/green] {vm.name}\n"
        f"[green]Cluster:[/green] {vm.cluster.name if vm.cluster else 'N/A'}\n"
        f"[green]Status:[/green] {vm.status}\n"
        f"[green]vCPUs:[/green] {vm.vcpus or 'N/A'}\n"
        f"[green]Memory:[/green] {vm.memory or 'N/A'} MB\n"
        f"[green]Disk:[/green] {vm.disk or 'N/A'} GB\n"
        f"[green]Primary IP:[/green] {vm.primary_ip4.address if vm.primary_ip4 else 'N/A'}"
    )

    console.print(Panel(info, title=f"VM: {vm.name}", border_style="cyan"))

    # Interfaces table
    if interfaces:
        iface_table = Table(title="Network Interfaces")
        iface_table.add_column("Name", style="cyan")
        iface_table.add_column("Type")
        iface_table.add_column("Enabled")
        iface_table.add_column("MTU")

        for iface in interfaces:
            iface_table.add_row(
                iface.name,
                iface.type.value if hasattr(iface.type, 'value') else str(iface.type),
                "✓" if iface.enabled else "✗",
                str(iface.mtu) if iface.mtu else "default"
            )

        console.print("\n", iface_table)

    # IPs table
    if ips:
        ip_table = Table(title="IP Addresses")
        ip_table.add_column("Address", style="yellow")
        ip_table.add_column("DNS Name", style="green")
        ip_table.add_column("Status")

        for ip in ips:
            ip_table.add_row(
                str(ip.address),
                ip.dns_name or "",
                ip.status.value if hasattr(ip.status, 'value') else str(ip.status)
            )

        console.print("\n", ip_table)


# ============================================================================
# Main
# ============================================================================

def main(vm_name: Optional[str] = None) -> int:
    """
    Main entry point.

    Args:
        vm_name: Optional specific VM to query

    Returns:
        Exit code (0 = success, 1 = error)
    """
    config = NetBoxConfig()

    # Get NetBox client
    nb = get_netbox_client(config)
    if not nb:
        return 1

    try:
        if vm_name:
            # Query specific VM
            details = get_vm_details(nb, vm_name)
            if details:
                display_vm_details(details)
                return 0
            return 1
        else:
            # List all VMs in Matrix cluster
            vms = get_cluster_vms(nb, cluster_name="Matrix")
            display_vms_table(vms)
            return 0

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="NetBox API client example",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--vm",
        help="Specific VM to query (default: list all)"
    )

    args = parser.parse_args()

    sys.exit(main(vm_name=args.vm))
