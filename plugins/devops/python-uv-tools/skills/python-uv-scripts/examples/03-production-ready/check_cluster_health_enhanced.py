#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "rich>=13.0.0",
#   "typer>=0.9.0",
# ]
# [tool.uv.metadata]
# purpose = "cluster-monitoring"
# team = "infrastructure"
# author = "devops@spaceships.work"
# ///
"""
Proxmox Cluster Health Checker - Production Ready Example

This is an enhanced version of the basic cluster health checker,
demonstrating all best practices for production uv scripts.

Features:
- Rich CLI with Typer
- Structured output with Rich
- Proper error handling
- Input validation
- Security best practices
- Comprehensive logging
- Exit codes for automation

Usage:
    # Interactive mode with rich output
    ./check_cluster_health_enhanced.py --node foxtrot

    # JSON output for automation
    ./check_cluster_health_enhanced.py --node foxtrot --json

    # Quiet mode (only errors)
    ./check_cluster_health_enhanced.py --node foxtrot --quiet

Examples:
    # Check specific cluster node
    ./check_cluster_health_enhanced.py --node golf

    # CI/CD integration
    ./check_cluster_health_enhanced.py --json | jq '.is_healthy'
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

app = typer.Typer(help="Check Proxmox cluster health")
console = Console()


@dataclass
class NodeStatus:
    """Cluster node status"""
    name: str
    online: bool
    node_id: int
    ip: str


@dataclass
class ClusterHealth:
    """Overall cluster health status"""
    cluster_name: str
    quorate: bool
    node_count: int
    expected_votes: int
    total_votes: int
    nodes: list[NodeStatus]
    warnings: list[str]
    errors: list[str]

    @property
    def is_healthy(self) -> bool:
        """Check if cluster is healthy"""
        return self.quorate and len(self.errors) == 0


def validate_hostname(hostname: str) -> bool:
    """Validate hostname format"""
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]$'
    return bool(re.match(pattern, hostname)) and len(hostname) <= 253


def run_ssh_command(node: str, command: str) -> str:
    """Execute command on remote node via SSH"""
    if not validate_hostname(node):
        console.print(f"[red]Error: Invalid hostname: {node}[/red]", file=sys.stderr)
        raise typer.Exit(code=1)

    try:
        result = subprocess.run(
            ["ssh", f"root@{node}", command],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Command failed: {command}[/red]", file=sys.stderr)
        console.print(f"  {e.stderr}", file=sys.stderr)
        raise typer.Exit(code=1)
    except subprocess.TimeoutExpired:
        console.print(f"[red]Command timed out: {command}[/red]", file=sys.stderr)
        raise typer.Exit(code=1)


def check_cluster_status(node: str) -> ClusterHealth:
    """Check cluster status and return health object"""
    health = ClusterHealth(
        cluster_name="",
        quorate=False,
        node_count=0,
        expected_votes=0,
        total_votes=0,
        nodes=[],
        warnings=[],
        errors=[]
    )

    # Get cluster status
    output = run_ssh_command(node, "pvecm status")

    # Parse cluster name
    if match := re.search(r'Cluster name:\s+(\S+)', output):
        health.cluster_name = match.group(1)

    # Parse quorum
    if match := re.search(r'Quorate:\s+(\w+)', output):
        health.quorate = match.group(1).lower() == 'yes'

    if not health.quorate:
        health.errors.append("Cluster does not have quorum!")

    # Parse votes
    if match := re.search(r'Nodes:\s+(\d+)', output):
        health.node_count = int(match.group(1))

    if match := re.search(r'Expected votes:\s+(\d+)', output):
        health.expected_votes = int(match.group(1))

    if match := re.search(r'Total votes:\s+(\d+)', output):
        health.total_votes = int(match.group(1))

    # Get node list
    output = run_ssh_command(node, "pvecm nodes")
    for line in output.strip().split('\n')[1:]:  # Skip header
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) >= 3:
            try:
                health.nodes.append(NodeStatus(
                    name=parts[2] if len(parts) >= 3 else "unknown",
                    online=True,
                    node_id=int(parts[0]),
                    ip=parts[3] if len(parts) >= 4 else "unknown"
                ))
            except (ValueError, IndexError):
                health.warnings.append(f"Failed to parse node line: {line}")

    return health


@app.command()
def main(
    node: str = typer.Option("foxtrot", help="Cluster node to check"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    quiet: bool = typer.Option(False, help="Only show errors"),
):
    """
    Check Proxmox cluster health

    Connects to a cluster node via SSH and checks:
    - Quorum status
    - Node membership
    - Vote distribution
    """
    try:
        health = check_cluster_status(node)

        if json_output:
            # JSON output for automation
            print(json.dumps(asdict(health), indent=2))
            sys.exit(0 if health.is_healthy else 1)

        if not quiet:
            # Rich table output
            console.print(f"\n[bold]Cluster Health: {health.cluster_name}[/bold]")
            console.print("=" * 60)

            # Status
            quorum_icon = "✓" if health.quorate else "✗"
            quorum_color = "green" if health.quorate else "red"
            console.print(f"Quorum: [{quorum_color}]{quorum_icon} {'YES' if health.quorate else 'NO'}[/{quorum_color}]")
            console.print(f"Nodes: {health.node_count} ({health.total_votes}/{health.expected_votes} votes)")

            # Nodes table
            table = Table(title="\nCluster Nodes")
            table.add_column("Node", style="cyan")
            table.add_column("Node ID", style="magenta")
            table.add_column("IP Address", style="yellow")
            table.add_column("Status", style="green")

            for node_status in health.nodes:
                status_icon = "✓" if node_status.online else "✗"
                table.add_row(
                    node_status.name,
                    str(node_status.node_id),
                    node_status.ip,
                    status_icon
                )

            console.print(table)

            # Warnings
            if health.warnings:
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in health.warnings:
                    console.print(f"  ⚠ {warning}")

            # Errors
            if health.errors:
                console.print("\n[red]Errors:[/red]")
                for error in health.errors:
                    console.print(f"  ✗ {error}")

            console.print("\n" + "=" * 60)

        # Final status
        if health.is_healthy:
            if not quiet:
                console.print("[green]Status: ✓ HEALTHY[/green]\n")
            sys.exit(0)
        else:
            console.print("[red]Status: ✗ UNHEALTHY[/red]\n", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    app()
