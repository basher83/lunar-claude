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
NetBox VM Creator

Create a complete VM in NetBox with automatic IP assignment and DNS configuration.
Follows Matrix cluster naming conventions and integrates with PowerDNS sync.

Usage:
    # Create VM with auto-assigned IP
    ./netbox_vm_create.py --name docker-02 --cluster matrix --vcpus 4 --memory 8192

    # Create VM with specific IP
    ./netbox_vm_create.py --name k8s-01-master --cluster matrix --ip 192.168.3.50

    # Create VM with custom DNS name
    ./netbox_vm_create.py --name app-01 --cluster matrix --dns-name app-01-web.spaceships.work

Example:
    ./netbox_vm_create.py \\
        --name docker-02 \\
        --cluster matrix \\
        --vcpus 4 \\
        --memory 8192 \\
        --disk 100 \\
        --description "Docker host for GitLab"
"""

import ipaddress
import os
import sys
import re
from typing import Optional
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.panel import Panel
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


def validate_dns_name(name: str) -> bool:
    """
    Validate DNS naming convention.

    Pattern: <service>-<number>[-<purpose>].<domain>
    Examples: docker-01.spaceships.work, docker-01-nexus.spaceships.work
    """
    pattern = r'^[a-z0-9-]+-\d{2}(-[a-z0-9-]+)?\.[a-z0-9.-]+$'
    return bool(re.match(pattern, name.lower()))


def validate_vm_name(name: str) -> bool:
    """
    Validate VM name (without domain).

    Pattern: <service>-<number> or <service>-<number>-<purpose>
    - service: one or more lowercase letters, digits, or hyphens
    - number: exactly two digits (00-99)
    - purpose (optional): one or more lowercase letters/numbers/hyphens

    Example: docker-01, k8s-01-master, or docker-proxy-01
    """
    pattern = r'^[a-z0-9-]+\-\d{2}(-[a-z0-9-]+)?$'
    return bool(re.match(pattern, name.lower()))


@app.command()
def main(
    name: str = typer.Option(...,
                             help="VM name (e.g., docker-02, k8s-01-master)"),
    cluster: str = typer.Option("matrix", help="Cluster name"),
    vcpus: int = typer.Option(2, help="Number of vCPUs"),
    memory: int = typer.Option(2048, help="Memory in MB"),
    disk: int = typer.Option(20, help="Disk size in GB"),
    ip: Optional[str] = typer.Option(
        None, help="Specific IP address (e.g., 192.168.3.50/24)"),
    prefix: str = typer.Option(
        "192.168.3.0/24", help="Prefix for auto IP assignment"),
    dns_name: Optional[str] = typer.Option(
        None, help="Custom DNS name (FQDN)"),
    description: Optional[str] = typer.Option(None, help="VM description"),
    tags: str = typer.Option("terraform,production-dns",
                             help="Comma-separated tags"),
    dry_run: bool = typer.Option(
        False, help="Show what would be created without creating")
):
    """
    Create a VM in NetBox with automatic IP assignment and DNS.

    This tool follows Matrix cluster conventions and integrates with PowerDNS sync.
    """
    # Validate VM name
    if not validate_vm_name(name):
        console.print(f"[red]Invalid VM name: {name}[/red]")
        console.print(
            "[yellow]VM name must contain only lowercase letters, numbers, and hyphens[/yellow]")
        raise typer.Exit(1)

    # Generate DNS name if not provided
    if not dns_name:
        dns_name = f"{name}.spaceships.work"

    # Validate DNS name
    if not validate_dns_name(dns_name):
        console.print(f"[red]Invalid DNS name: {dns_name}[/red]")
        console.print(
            "[yellow]DNS name must follow pattern: service-NN[-purpose].domain[/yellow]")
        console.print(
            "[yellow]Examples: docker-01.spaceships.work or docker-01-nexus.spaceships.work[/yellow]")
        raise typer.Exit(1)

    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

    # Show configuration
    console.print(Panel(
        f"[green]VM Name:[/green] {name}\n"
        f"[green]Cluster:[/green] {cluster}\n"
        f"[green]vCPUs:[/green] {vcpus}\n"
        f"[green]Memory:[/green] {memory} MB\n"
        f"[green]Disk:[/green] {disk} GB\n"
        f"[green]IP:[/green] {ip or f'Auto (from {prefix})'}\n"
        f"[green]DNS Name:[/green] {dns_name}\n"
        f"[green]Description:[/green] {description or 'N/A'}\n"
        f"[green]Tags:[/green] {', '.join(tag_list)}",
        title="VM Configuration",
        border_style="cyan"
    ))

    if dry_run:
        console.print("\n[yellow]Dry run - no changes made[/yellow]")
        raise typer.Exit(0)

    # Confirm
    if not typer.confirm("\nCreate this VM in NetBox?"):
        console.print("[yellow]Aborted[/yellow]")
        raise typer.Exit(0)

    nb = get_netbox_client()

    try:
        # 1. Get cluster
        console.print(f"\n[cyan]1. Looking up cluster '{cluster}'...[/cyan]")
        cluster_obj = nb.virtualization.clusters.get(name=cluster)
        if not cluster_obj:
            console.print(f"[red]Cluster '{cluster}' not found[/red]")
            raise typer.Exit(1)
        console.print(f"[green]✓ Found cluster: {cluster_obj.name}[/green]")

        # 2. Check if VM already exists
        console.print(
            f"\n[cyan]2. Checking if VM '{name}' already exists...[/cyan]")
        existing_vm = nb.virtualization.virtual_machines.get(name=name)
        if existing_vm:
            console.print(
                f"[red]VM '{name}' already exists (ID: {existing_vm.id})[/red]")
            raise typer.Exit(1)
        console.print("[green]✓ VM name available[/green]")

        # 3. Create VM
        console.print(f"\n[cyan]3. Creating VM '{name}'...[/cyan]")
        vm = nb.virtualization.virtual_machines.create(
            name=name,
            cluster=cluster_obj.id,
            status='active',
            vcpus=vcpus,
            memory=memory,
            disk=disk,
            description=description or "VM created via netbox_vm_create.py",
            tags=[{"name": tag} for tag in tag_list]
        )
        console.print(f"[green]✓ Created VM (ID: {vm.id})[/green]")

        # 4. Create VM interface
        console.print("\n[cyan]4. Creating network interface 'eth0'...[/cyan]")
        vm_iface = nb.virtualization.interfaces.create(
            virtual_machine=vm.id,
            name='eth0',
            type='virtual',
            enabled=True,
            mtu=1500
        )
        console.print(
            f"[green]✓ Created interface (ID: {vm_iface.id})[/green]")

        # 5. Assign IP
        # Validate IP format if provided
        if ip:
            try:
                ipaddress.ip_interface(ip)
            except ValueError:
                console.print(f"[red]Invalid IP address format: {ip}[/red]")
                console.print(
                    "[yellow]Expected format: 192.168.3.50/24[/yellow]")
                # Rollback
                vm_iface.delete()
                vm.delete()
                raise typer.Exit(1)

        try:
            if ip:
                # Use specific IP
                console.print(f"\n[cyan]5. Creating IP address {ip}...[/cyan]")
                vm_ip = nb.ipam.ip_addresses.create(
                    address=ip,
                    dns_name=dns_name,
                    status='active',
                    assigned_object_type='virtualization.vminterface',
                    assigned_object_id=vm_iface.id,
                    tags=[{"name": tag} for tag in tag_list]
                )
            else:
                # Auto-assign from prefix
                console.print(
                    f"\n[cyan]5. Getting next available IP from {prefix}...[/cyan]")
                prefix_obj = nb.ipam.prefixes.get(prefix=prefix)
                if not prefix_obj:
                    console.print(f"[red]Prefix '{prefix}' not found[/red]")
                    # Rollback
                    vm_iface.delete()
                    vm.delete()
                    raise typer.Exit(1)

                vm_ip = prefix_obj.available_ips.create(
                    dns_name=dns_name,
                    status='active',
                    assigned_object_type='virtualization.vminterface',
                    assigned_object_id=vm_iface.id,
                    tags=[{"name": tag} for tag in tag_list]
                )

            console.print(f"[green]✓ Assigned IP: {vm_ip.address}[/green]")
        except Exception as e:
            console.print(f"[red]Failed to assign IP: {e}[/red]")
            console.print(
                "[yellow]Rolling back: deleting interface and VM...[/yellow]")
            try:
                vm_iface.delete()
                vm.delete()
            except Exception as rollback_error:
                console.print(f"[red]Rollback failed: {rollback_error}[/red]")
            raise typer.Exit(1)

        # 6. Set as primary IP
        console.print(
            f"\n[cyan]6. Setting {vm_ip.address} as primary IP...[/cyan]")
        vm.primary_ip4 = vm_ip.id
        vm.save()
        console.print("[green]✓ Set primary IP[/green]")

        # Success summary
        console.print("\n" + "="*60)
        console.print(Panel(
            f"[green]VM Name:[/green] {vm.name}\n"
            f"[green]ID:[/green] {vm.id}\n"
            f"[green]Cluster:[/green] {cluster_obj.name}\n"
            f"[green]IP Address:[/green] {vm_ip.address}\n"
            f"[green]DNS Name:[/green] {vm_ip.dns_name}\n"
            f"[green]vCPUs:[/green] {vm.vcpus}\n"
            f"[green]Memory:[/green] {vm.memory} MB\n"
            f"[green]Disk:[/green] {vm.disk} GB\n"
            f"[green]Tags:[/green] {', '.join(tag_list)}",
            title="✓ VM Created Successfully",
            border_style="green"
        ))

        console.print(
            "\n[yellow]Note:[/yellow] DNS record will be automatically created by NetBox PowerDNS sync plugin")
        console.print(
            f"[yellow]DNS:[/yellow] {dns_name} → {vm_ip.address.split('/')[0]}")

    except pynetbox.RequestError as e:
        console.print(f"\n[red]NetBox API Error: {e.error}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
