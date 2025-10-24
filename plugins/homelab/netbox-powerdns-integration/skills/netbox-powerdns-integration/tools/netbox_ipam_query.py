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
NetBox IPAM Query Tool

Advanced IPAM queries for the Matrix cluster infrastructure.
Query available IPs, prefix utilization, IP assignments, and VLAN information.

Usage:
    # Get available IPs in prefix
    ./netbox_ipam_query.py available --prefix 192.168.3.0/24

    # Check prefix utilization
    ./netbox_ipam_query.py utilization --site matrix

    # Find IP assignments
    ./netbox_ipam_query.py assignments --prefix 192.168.3.0/24

    # List VLANs
    ./netbox_ipam_query.py vlans --site matrix

Example:
    ./netbox_ipam_query.py available --prefix 192.168.3.0/24 --limit 5
    ./netbox_ipam_query.py utilization --site matrix --output json
"""

import os
import sys
from typing import Optional
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import pynetbox
from infisical_sdk import InfisicalSDKClient

app = typer.Typer()
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
            console.print("[red]INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET environment variables required[/red]")
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


@app.command("available")
def available_ips(
    prefix: str = typer.Option(..., help="Prefix (e.g., 192.168.3.0/24)"),
    limit: int = typer.Option(10, help="Number of IPs to show"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Get available IPs in a prefix."""
    nb = get_netbox_client()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                f"Querying prefix {prefix}...", total=None)

            prefix_obj = nb.ipam.prefixes.get(prefix=prefix)

            if not prefix_obj:
                console.print(f"[red]Prefix '{prefix}' not found[/red]")
                sys.exit(1)

            progress.update(task, description="Getting available IPs...")
            available = prefix_obj.available_ips.list()[:limit]

        if output == "json":
            import json
            data = {
                "prefix": str(prefix),
                "total_shown": len(available),
                "available_ips": [str(ip.address) for ip in available]
            }
            print(json.dumps(data, indent=2))
        else:
            console.print(f"\n[green]Prefix:[/green] {prefix}")
            console.print(
                f"[green]Site:[/green] {prefix_obj.site.name if prefix_obj.site else 'N/A'}")
            console.print(
                f"[green]Description:[/green] {prefix_obj.description or 'N/A'}\n")

            table = Table(title="Available IP Addresses")
            table.add_column("IP Address", style="cyan")
            table.add_column("Ready for Assignment")

            for ip in available:
                table.add_row(str(ip.address), "✓")

            console.print(table)
            console.print(
                f"\n[yellow]Showing first {limit} available IPs[/yellow]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command("utilization")
def prefix_utilization(
    site: Optional[str] = typer.Option(None, help="Filter by site slug"),
    role: Optional[str] = typer.Option(None, help="Filter by prefix role"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Show prefix utilization statistics."""
    nb = get_netbox_client()

    try:
        filters = {}
        if site:
            filters['site'] = site
        if role:
            filters['role'] = role

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Querying prefixes...", total=None)
            prefixes = nb.ipam.prefixes.filter(
                **filters) if filters else nb.ipam.prefixes.all()

        if output == "json":
            import json
            data = [
                {
                    "prefix": str(p.prefix),
                    "site": p.site.name if p.site else None,
                    "role": p.role.name if p.role else None,
                    "utilization": float(p.utilization) if hasattr(p, 'utilization') else 0.0,
                    "description": p.description or ""
                }
                for p in prefixes
            ]
            print(json.dumps(data, indent=2))
        else:
            table = Table(title="Prefix Utilization")
            table.add_column("Prefix", style="cyan")
            table.add_column("Site", style="yellow")
            table.add_column("Role")
            table.add_column("Utilization", justify="right")
            table.add_column("Description")

            for p in prefixes:
                utilization = p.utilization if hasattr(p, 'utilization') else 0
                util_pct = f"{utilization}%"

                # Color code based on utilization
                if utilization >= 90:
                    util_color = "red"
                elif utilization >= 75:
                    util_color = "yellow"
                else:
                    util_color = "green"

                table.add_row(
                    str(p.prefix),
                    p.site.name if p.site else "N/A",
                    p.role.name if p.role else "N/A",
                    f"[{util_color}]{util_pct}[/{util_color}]",
                    p.description or ""
                )

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command("assignments")
def ip_assignments(
    prefix: str = typer.Option(..., help="Prefix (e.g., 192.168.3.0/24)"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """Show IP assignments in a prefix."""
    nb = get_netbox_client()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                f"Querying prefix {prefix}...", total=None)

            prefix_obj = nb.ipam.prefixes.get(prefix=prefix)
            if not prefix_obj:
                console.print(f"[red]Prefix '{prefix}' not found[/red]")
                sys.exit(1)

            progress.update(task, description="Getting IP assignments...")
            # Get IPs by parent prefix (materialize once to avoid re-fetching)
            ips = list(nb.ipam.ip_addresses.filter(parent=prefix))

        if output == "json":
            import json
            data = [
                {
                    "address": str(ip.address),
                    "dns_name": ip.dns_name or "",
                    "status": ip.status.value if hasattr(ip.status, 'value') else str(ip.status),
                    "assigned_to": {
                        "type": ip.assigned_object_type if ip.assigned_object else None,
                        "name": ip.assigned_object.name if ip.assigned_object else None
                    },
                    "description": ip.description or ""
                }
                for ip in ips
            ]
            print(json.dumps(data, indent=2))
        else:
            table = Table(title=f"IP Assignments in {prefix}")
            table.add_column("IP Address", style="cyan")
            table.add_column("DNS Name", style="green")
            table.add_column("Status")
            table.add_column("Assigned To")
            table.add_column("Description")

            for ip in ips:
                assigned_to = "N/A"
                if ip.assigned_object:
                    obj_type = ip.assigned_object_type.split(
                        '.')[-1] if ip.assigned_object_type else "unknown"
                    assigned_to = f"{ip.assigned_object.name} ({obj_type})"

                table.add_row(
                    str(ip.address),
                    ip.dns_name or "",
                    ip.status.value if hasattr(
                        ip.status, 'value') else str(ip.status),
                    assigned_to,
                    ip.description or ""
                )

            console.print(table)
            console.print(f"\n[green]Total IPs: {len(ips)}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command("vlans")
def list_vlans(
    site: Optional[str] = typer.Option(None, help="Filter by site slug"),
    output: str = typer.Option("table", help="Output format: table or json")
):
    """List VLANs."""
    nb = get_netbox_client()

    try:
        filters = {}
        if site:
            filters['site'] = site

        # Materialize once to avoid re-fetching on len() call
        vlans = list(nb.ipam.vlans.filter(**filters)
                     if filters else nb.ipam.vlans.all())

        if output == "json":
            import json
            data = [
                {
                    "id": vlan.id,
                    "vid": vlan.vid,
                    "name": vlan.name,
                    "site": vlan.site.name if vlan.site else None,
                    "status": vlan.status.value if hasattr(vlan.status, 'value') else str(vlan.status),
                    "description": vlan.description or ""
                }
                for vlan in vlans
            ]
            print(json.dumps(data, indent=2))
        else:
            table = Table(title="VLANs")
            table.add_column("ID", style="cyan")
            table.add_column("VID", justify="right", style="yellow")
            table.add_column("Name", style="green")
            table.add_column("Site")
            table.add_column("Status")
            table.add_column("Description")

            for vlan in vlans:
                table.add_row(
                    str(vlan.id),
                    str(vlan.vid),
                    vlan.name,
                    vlan.site.name if vlan.site else "N/A",
                    vlan.status.value if hasattr(
                        vlan.status, 'value') else str(vlan.status),
                    vlan.description or ""
                )

            console.print(table)
            console.print(f"\n[green]Total VLANs: {len(vlans)}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@app.command("summary")
def ipam_summary(
    site: str = typer.Option(..., help="Site slug")
):
    """Show IPAM summary for a site."""
    nb = get_netbox_client()

    try:
        site_obj = nb.dcim.sites.get(slug=site)
        if not site_obj:
            console.print(f"[red]Site '{site}' not found[/red]")
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Gathering IPAM data...", total=None)

            # Get prefixes
            prefixes = list(nb.ipam.prefixes.filter(site=site))

            # Get IPs
            ips = list(nb.ipam.ip_addresses.filter(site=site)
                       if hasattr(nb.ipam.ip_addresses, 'filter') else [])

            # Get VLANs
            vlans = list(nb.ipam.vlans.filter(site=site))

        # Display summary
        console.print(Panel(
            f"[green]Site:[/green] {site_obj.name}\n"
            f"[green]Prefixes:[/green] {len(prefixes)}\n"
            f"[green]IP Addresses:[/green] {len(ips)}\n"
            f"[green]VLANs:[/green] {len(vlans)}",
            title="IPAM Summary",
            border_style="cyan"
        ))

        # Prefix details
        if prefixes:
            console.print("\n[yellow]Prefixes:[/yellow]")
            for p in prefixes:
                utilization = p.utilization if hasattr(p, 'utilization') else 0
                console.print(
                    f"  • {p.prefix} - {p.description or 'No description'} ({utilization}% used)")

        # VLAN details
        if vlans:
            console.print("\n[yellow]VLANs:[/yellow]")
            for v in vlans:
                console.print(
                    f"  • VLAN {v.vid} ({v.name}) - {v.description or 'No description'}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    app()
