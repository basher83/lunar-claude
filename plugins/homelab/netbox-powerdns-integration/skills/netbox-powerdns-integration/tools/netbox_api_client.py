#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pynetbox>=7.0.0",
#   "infisicalsdk>=1.0.3",
#   "rich>=13.0.0",
#   "typer>=0.9.0",
# ]
# ///

"""
NetBox API Client

Complete working example of NetBox REST API usage with pynetbox.
Demonstrates authentication, queries, filtering, error handling, and best practices.

Usage:
    # List all sites
    ./netbox_api_client.py sites list

    # Get specific device
    ./netbox_api_client.py devices get --name foxtrot

    # List VMs in cluster
    ./netbox_api_client.py vms list --cluster matrix

    # Query IPs by DNS name
    ./netbox_api_client.py ips query --dns-name docker-01

    # Get available IPs in prefix
    ./netbox_api_client.py prefixes available --prefix 192.168.3.0/24

    # Create VM with IP
    ./netbox_api_client.py vms create --name test-vm --cluster matrix --ip 192.168.3.100

Example:
    ./netbox_api_client.py devices get --name foxtrot --output json
"""

import os
import sys
from typing import Optional
from dataclasses import dataclass

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pynetbox
from infisical_sdk import InfisicalSDKClient

app = typer.Typer(help="NetBox API Client for Matrix cluster infrastructure")
console = Console()


# ============================================================================
# Configuration and Authentication
# ============================================================================

@dataclass
class NetBoxConfig:
    """NetBox connection configuration."""
    url: str
    token: str
    ssl_verify: bool = True


def get_netbox_client() -> pynetbox.api:
    """
    Get authenticated NetBox API client.

    Uses Infisical SDK with Universal Auth to securely retrieve API token.
    Requires INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET environment variables.

    Returns:
        pynetbox.api: Authenticated NetBox client

    Raises:
        ValueError: If token cannot be retrieved or is empty
        typer.Exit: On connection or authentication errors (CLI exits)
    """
    try:
        # Initialize Infisical SDK client
        client = InfisicalSDKClient(host="https://app.infisical.com")

        # Authenticate using Universal Auth (machine identity)
        client_id = os.getenv("INFISICAL_CLIENT_ID")
        client_secret = os.getenv("INFISICAL_CLIENT_SECRET")

        if not client_id or not client_secret:
            console.print(
                "[red]INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET environment variables required[/red]")
            raise typer.Exit(1)

        client.auth.universal_auth.login(
            client_id=client_id,
            client_secret=client_secret
        )

        # Get NetBox API token from Infisical
        secret = client.secrets.get_secret_by_name(
            secret_name="NETBOX_API_TOKEN",
            project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
            environment_slug="prod",
            secret_path="/matrix"
        )

        token = secret.secretValue

        if not token:
            console.print("[red]NETBOX_API_TOKEN is empty in Infisical[/red]")
            raise ValueError("NETBOX_API_TOKEN is empty")

        config = NetBoxConfig(
            url="https://netbox.spaceships.work",
            token=token,
            ssl_verify=True
        )

        return pynetbox.api(config.url, token=config.token)

    except ValueError:
        # ValueError already logged above, re-raise to propagate
        raise
    except Exception as e:
        console.print(f"[red]Failed to connect to NetBox: {e}[/red]")
        raise typer.Exit(1)


# ============================================================================
# Sites Commands
# ============================================================================

sites_app = typer.Typer(help="Manage NetBox sites")


@sites_app.command("list")
def sites_list(
    output: str = typer.Option("table", help="Output format: table or json")
):
    """List all sites in NetBox."""
    nb = get_netbox_client()

    try:
        sites = nb.dcim.sites.all()

        if output == "json":
            import json
            sites_data = [
                {
                    "id": s.id,
                    "name": s.name,
                    "slug": s.slug,
                    "status": s.status.value if hasattr(s.status, 'value') else str(s.status),
                    "description": s.description or ""
                }
                for s in sites
            ]
            print(json.dumps(sites_data, indent=2))
        else:
            table = Table(title="NetBox Sites")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Slug", style="yellow")
            table.add_column("Status")
            table.add_column("Description")

            for site in sites:
                table.add_row(
                    str(site.id),
                    site.name,
                    site.slug,
                    site.status.value if hasattr(
                        site.status, 'value') else str(site.status),
                    site.description or ""
                )

            console.print(table)
            console.print(f"\n[green]Total sites: {len(sites)}[/green]")

    except Exception as e:
        console.print(f"[red]Error listing sites: {e}[/red]")
        sys.exit(1)


@sites_app.command("get")
def sites_get(
    slug: str = typer.Option(..., help="Site slug"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Get specific site by slug."""
    nb = get_netbox_client()

    try:
        site = nb.dcim.sites.get(slug=slug)

        if not site:
            console.print(f"[red]Site '{slug}' not found[/red]")
            sys.exit(1)

        if output == "json":
            import json
            site_data = {
                "id": site.id,
                "name": site.name,
                "slug": site.slug,
                "status": site.status.value if hasattr(site.status, 'value') else str(site.status),
                "description": site.description or "",
                "tags": [tag.name for tag in site.tags] if site.tags else []
            }
            print(json.dumps(site_data, indent=2))
        else:
            console.print(Panel(
                f"[green]Name:[/green] {site.name}\n"
                f"[green]Slug:[/green] {site.slug}\n"
                f"[green]Status:[/green] {site.status}\n"
                f"[green]Description:[/green] {site.description or 'N/A'}\n"
                f"[green]Tags:[/green] {', '.join([tag.name for tag in site.tags]) if site.tags else 'None'}",
                title=f"Site: {site.name}",
                border_style="green"
            ))

    except Exception as e:
        console.print(f"[red]Error getting site: {e}[/red]")
        sys.exit(1)


# ============================================================================
# Devices Commands
# ============================================================================

devices_app = typer.Typer(help="Manage NetBox devices")


@devices_app.command("list")
def devices_list(
    site: Optional[str] = typer.Option(None, help="Filter by site slug"),
    role: Optional[str] = typer.Option(None, help="Filter by device role"),
    tag: Optional[str] = typer.Option(None, help="Filter by tag"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """List devices with optional filtering."""
    nb = get_netbox_client()

    try:
        # Build filter
        filters = {}
        if site:
            filters['site'] = site
        if role:
            filters['role'] = role
        if tag:
            filters['tag'] = tag

        devices = nb.dcim.devices.filter(
            **filters) if filters else nb.dcim.devices.all()

        if output == "json":
            import json
            devices_data = [
                {
                    "id": d.id,
                    "name": d.name,
                    "site": d.site.name if d.site else None,
                    "role": d.device_role.name if d.device_role else None,
                    "status": d.status.value if hasattr(d.status, 'value') else str(d.status),
                    "primary_ip": str(d.primary_ip4.address) if d.primary_ip4 else None
                }
                for d in devices
            ]
            print(json.dumps(devices_data, indent=2))
        else:
            table = Table(title="NetBox Devices")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Site", style="yellow")
            table.add_column("Role")
            table.add_column("Status")
            table.add_column("Primary IP")

            for device in devices:
                table.add_row(
                    str(device.id),
                    device.name,
                    device.site.name if device.site else "N/A",
                    device.device_role.name if device.device_role else "N/A",
                    device.status.value if hasattr(
                        device.status, 'value') else str(device.status),
                    str(device.primary_ip4.address) if device.primary_ip4 else "N/A"
                )

            console.print(table)
            console.print(
                f"\n[green]Total devices: {len(list(devices))}[/green]")

    except Exception as e:
        console.print(f"[red]Error listing devices: {e}[/red]")
        sys.exit(1)


@devices_app.command("get")
def devices_get(
    name: str = typer.Option(..., help="Device name"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Get device details including interfaces."""
    nb = get_netbox_client()

    try:
        device = nb.dcim.devices.get(name=name)

        if not device:
            console.print(f"[red]Device '{name}' not found[/red]")
            sys.exit(1)

        # Get interfaces
        interfaces = nb.dcim.interfaces.filter(device=name)

        if output == "json":
            import json
            device_data = {
                "id": device.id,
                "name": device.name,
                "site": device.site.name if device.site else None,
                "role": device.device_role.name if device.device_role else None,
                "status": device.status.value if hasattr(device.status, 'value') else str(device.status),
                "primary_ip4": str(device.primary_ip4.address) if device.primary_ip4 else None,
                "interfaces": [
                    {
                        "name": iface.name,
                        "type": iface.type.value if hasattr(iface.type, 'value') else str(iface.type),
                        "enabled": iface.enabled,
                        "mtu": iface.mtu
                    }
                    for iface in interfaces
                ]
            }
            print(json.dumps(device_data, indent=2))
        else:
            # Device info
            console.print(Panel(
                f"[green]Name:[/green] {device.name}\n"
                f"[green]Site:[/green] {device.site.name if device.site else 'N/A'}\n"
                f"[green]Role:[/green] {device.device_role.name if device.device_role else 'N/A'}\n"
                f"[green]Status:[/green] {device.status}\n"
                f"[green]Primary IP:[/green] {device.primary_ip4.address if device.primary_ip4 else 'N/A'}",
                title=f"Device: {device.name}",
                border_style="green"
            ))

            # Interfaces table
            if interfaces:
                iface_table = Table(title="Interfaces")
                iface_table.add_column("Name", style="cyan")
                iface_table.add_column("Type")
                iface_table.add_column("Enabled")
                iface_table.add_column("MTU")

                for iface in interfaces:
                    iface_table.add_row(
                        iface.name,
                        iface.type.value if hasattr(
                            iface.type, 'value') else str(iface.type),
                        "✓" if iface.enabled else "✗",
                        str(iface.mtu) if iface.mtu else "default"
                    )

                console.print("\n", iface_table)

    except Exception as e:
        console.print(f"[red]Error getting device: {e}[/red]")
        sys.exit(1)


# ============================================================================
# Virtual Machines Commands
# ============================================================================

vms_app = typer.Typer(help="Manage NetBox virtual machines")


@vms_app.command("list")
def vms_list(
    cluster: Optional[str] = typer.Option(None, help="Filter by cluster"),
    tag: Optional[str] = typer.Option(None, help="Filter by tag"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """List virtual machines."""
    nb = get_netbox_client()

    try:
        filters = {}
        if cluster:
            filters['cluster'] = cluster
        if tag:
            filters['tag'] = tag

        vms = nb.virtualization.virtual_machines.filter(
            **filters) if filters else nb.virtualization.virtual_machines.all()

        if output == "json":
            import json
            vms_data = [
                {
                    "id": vm.id,
                    "name": vm.name,
                    "cluster": vm.cluster.name if vm.cluster else None,
                    "vcpus": vm.vcpus,
                    "memory": vm.memory,
                    "status": vm.status.value if hasattr(vm.status, 'value') else str(vm.status),
                    "primary_ip": str(vm.primary_ip4.address) if vm.primary_ip4 else None
                }
                for vm in vms
            ]
            print(json.dumps(vms_data, indent=2))
        else:
            table = Table(title="NetBox Virtual Machines")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Cluster", style="yellow")
            table.add_column("vCPUs")
            table.add_column("Memory (MB)")
            table.add_column("Status")
            table.add_column("Primary IP")

            for vm in vms:
                table.add_row(
                    str(vm.id),
                    vm.name,
                    vm.cluster.name if vm.cluster else "N/A",
                    str(vm.vcpus) if vm.vcpus else "N/A",
                    str(vm.memory) if vm.memory else "N/A",
                    vm.status.value if hasattr(
                        vm.status, 'value') else str(vm.status),
                    str(vm.primary_ip4.address) if vm.primary_ip4 else "N/A"
                )

            console.print(table)
            console.print(f"\n[green]Total VMs: {len(list(vms))}[/green]")

    except Exception as e:
        console.print(f"[red]Error listing VMs: {e}[/red]")
        sys.exit(1)


@vms_app.command("get")
def vms_get(
    name: str = typer.Option(..., help="VM name"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Get VM details including interfaces and IPs."""
    nb = get_netbox_client()

    try:
        vm = nb.virtualization.virtual_machines.get(name=name)

        if not vm:
            console.print(f"[red]VM '{name}' not found[/red]")
            sys.exit(1)

        # Get interfaces
        interfaces = nb.virtualization.interfaces.filter(
            virtual_machine_id=vm.id)

        if output == "json":
            import json
            vm_data = {
                "id": vm.id,
                "name": vm.name,
                "cluster": vm.cluster.name if vm.cluster else None,
                "vcpus": vm.vcpus,
                "memory": vm.memory,
                "disk": vm.disk,
                "status": vm.status.value if hasattr(vm.status, 'value') else str(vm.status),
                "primary_ip4": str(vm.primary_ip4.address) if vm.primary_ip4 else None,
                "interfaces": [
                    {
                        "name": iface.name,
                        "enabled": iface.enabled,
                        "mtu": iface.mtu
                    }
                    for iface in interfaces
                ]
            }
            print(json.dumps(vm_data, indent=2))
        else:
            console.print(Panel(
                f"[green]Name:[/green] {vm.name}\n"
                f"[green]Cluster:[/green] {vm.cluster.name if vm.cluster else 'N/A'}\n"
                f"[green]vCPUs:[/green] {vm.vcpus or 'N/A'}\n"
                f"[green]Memory:[/green] {vm.memory or 'N/A'} MB\n"
                f"[green]Disk:[/green] {vm.disk or 'N/A'} GB\n"
                f"[green]Status:[/green] {vm.status}\n"
                f"[green]Primary IP:[/green] {vm.primary_ip4.address if vm.primary_ip4 else 'N/A'}",
                title=f"VM: {vm.name}",
                border_style="green"
            ))

            if interfaces:
                iface_table = Table(title="Interfaces")
                iface_table.add_column("Name", style="cyan")
                iface_table.add_column("Enabled")
                iface_table.add_column("MTU")

                for iface in interfaces:
                    iface_table.add_row(
                        iface.name,
                        "✓" if iface.enabled else "✗",
                        str(iface.mtu) if iface.mtu else "default"
                    )

                console.print("\n", iface_table)

    except Exception as e:
        console.print(f"[red]Error getting VM: {e}[/red]")
        sys.exit(1)


# ============================================================================
# IP Addresses Commands
# ============================================================================

ips_app = typer.Typer(help="Manage NetBox IP addresses")


@ips_app.command("query")
def ips_query(
    dns_name: Optional[str] = typer.Option(
        None, help="Filter by DNS name (partial match)"),
    address: Optional[str] = typer.Option(None, help="Filter by IP address"),
    tag: Optional[str] = typer.Option(None, help="Filter by tag"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Query IP addresses."""
    nb = get_netbox_client()

    try:
        filters = {}
        if dns_name:
            filters['dns_name__ic'] = dns_name  # Case-insensitive contains
        if address:
            filters['address'] = address
        if tag:
            filters['tag'] = tag

        if not filters:
            console.print(
                "[yellow]Please provide at least one filter[/yellow]")
            sys.exit(0)

        ips = nb.ipam.ip_addresses.filter(**filters)

        if output == "json":
            import json
            ips_data = [
                {
                    "id": ip.id,
                    "address": str(ip.address),
                    "dns_name": ip.dns_name or "",
                    "status": ip.status.value if hasattr(ip.status, 'value') else str(ip.status),
                    "assigned_to": ip.assigned_object.name if ip.assigned_object else None
                }
                for ip in ips
            ]
            print(json.dumps(ips_data, indent=2))
        else:
            table = Table(title="IP Addresses")
            table.add_column("ID", style="cyan")
            table.add_column("Address", style="green")
            table.add_column("DNS Name", style="yellow")
            table.add_column("Status")
            table.add_column("Assigned To")

            for ip in ips:
                table.add_row(
                    str(ip.id),
                    str(ip.address),
                    ip.dns_name or "",
                    ip.status.value if hasattr(
                        ip.status, 'value') else str(ip.status),
                    ip.assigned_object.name if ip.assigned_object else "N/A"
                )

            console.print(table)
            console.print(f"\n[green]Total IPs: {len(list(ips))}[/green]")

    except Exception as e:
        console.print(f"[red]Error querying IPs: {e}[/red]")
        sys.exit(1)


# ============================================================================
# Prefixes Commands
# ============================================================================

prefixes_app = typer.Typer(help="Manage NetBox prefixes")


@prefixes_app.command("available")
def prefixes_available(
    prefix: str = typer.Option(..., help="Prefix (e.g., 192.168.3.0/24)"),
    limit: int = typer.Option(10, help="Max results to show"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Get available IPs in a prefix."""
    nb = get_netbox_client()

    try:
        prefix_obj = nb.ipam.prefixes.get(prefix=prefix)

        if not prefix_obj:
            console.print(f"[red]Prefix '{prefix}' not found[/red]")
            sys.exit(1)

        available = prefix_obj.available_ips.list()[:limit]

        if output == "json":
            import json
            print(json.dumps([str(ip.address) for ip in available], indent=2))
        else:
            console.print(f"\n[green]Prefix:[/green] {prefix}")
            console.print(
                f"[green]Available IPs (showing first {limit}):[/green]\n")

            for ip in available:
                console.print(f"  • {ip.address}")

            console.print(
                f"\n[yellow]Total available: {len(available)}+[/yellow]")

    except Exception as e:
        console.print(f"[red]Error getting available IPs: {e}[/red]")
        sys.exit(1)


# ============================================================================
# Main App
# ============================================================================

app.add_typer(sites_app, name="sites")
app.add_typer(devices_app, name="devices")
app.add_typer(vms_app, name="vms")
app.add_typer(ips_app, name="ips")
app.add_typer(prefixes_app, name="prefixes")


@app.command("version")
def version():
    """Show version information."""
    console.print("[green]NetBox API Client v1.0.0[/green]")
    console.print("Part of Virgo-Core infrastructure automation")


if __name__ == "__main__":
    app()
