#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Proxmox Cluster Health Checker

Validates Proxmox cluster health including:
- Cluster quorum status
- Node membership and status
- Corosync ring health
- Resource manager status
- Configuration version sync

Usage:
    python check_cluster_health.py [--node NODE] [--json]

Examples:
    # Check cluster health (requires SSH access to cluster node)
    python check_cluster_health.py --node foxtrot

    # Output as JSON for parsing
    python check_cluster_health.py --node foxtrot --json
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class NodeStatus:
    """Cluster node status"""
    name: str
    online: bool
    node_id: int
    ip: str


@dataclass
class CorosyncStatus:
    """Corosync ring status"""
    ring_id: int
    nodes: List[str]
    status: str


@dataclass
class ClusterHealth:
    """Overall cluster health"""
    cluster_name: str
    quorate: bool
    node_count: int
    expected_votes: int
    total_votes: int
    nodes: List[NodeStatus]
    corosync_rings: List[CorosyncStatus]
    config_version: Optional[int]
    warnings: List[str]
    errors: List[str]

    @property
    def is_healthy(self) -> bool:
        """Check if cluster is in healthy state"""
        return self.quorate and len(self.errors) == 0


class ClusterHealthChecker:
    """Check Proxmox cluster health via SSH"""

    def __init__(self, node: str):
        # Validate node is a valid hostname or IP address
        if not self._validate_node(node):
            raise ValueError(f"Invalid node name or IP address: {node}")
        self.node = node
        self.health = ClusterHealth(
            cluster_name="",
            quorate=False,
            node_count=0,
            expected_votes=0,
            total_votes=0,
            nodes=[],
            corosync_rings=[],
            config_version=None,
            warnings=[],
            errors=[]
        )

    def _validate_node(self, node: str) -> bool:
        """Validate node is a valid hostname or IP address"""
        import re
        # Allow valid hostnames and IPv4/IPv6 addresses
        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
        return bool(
            re.match(hostname_pattern, node) or
            re.match(ipv4_pattern, node) or
            re.match(ipv6_pattern, node)
        )

    def run_command(self, command: str) -> str:
        """Execute command on remote node via SSH"""
        try:
            # Use -- to prevent SSH option injection
            result = subprocess.run(
                ["ssh", "-o", "BatchMode=yes", f"root@{self.node}", "--", command],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            self.health.errors.append(f"Command timed out: {command}")
            return ""
        except subprocess.CalledProcessError as e:
            self.health.errors.append(f"Command failed: {command}: {e.stderr}")
            return ""

    def check_cluster_status(self):
        """Check pvecm status output"""
        output = self.run_command("pvecm status")
        if not output:
            self.health.errors.append("Failed to get cluster status")
            return

        # Parse cluster name
        cluster_match = re.search(r'Cluster name:\s+(\S+)', output)
        if cluster_match:
            self.health.cluster_name = cluster_match.group(1)

        # Parse quorum status
        quorum_match = re.search(r'Quorate:\s+(\w+)', output)
        if quorum_match:
            self.health.quorate = quorum_match.group(1).lower() == 'yes'

        if not self.health.quorate:
            self.health.errors.append("Cluster does not have quorum!")

        # Parse node count
        node_match = re.search(r'Nodes:\s+(\d+)', output)
        if node_match:
            self.health.node_count = int(node_match.group(1))

        # Parse expected votes
        expected_match = re.search(r'Expected votes:\s+(\d+)', output)
        if expected_match:
            self.health.expected_votes = int(expected_match.group(1))

        # Parse total votes
        total_match = re.search(r'Total votes:\s+(\d+)', output)
        if total_match:
            self.health.total_votes = int(total_match.group(1))

        # Check if we have majority
        if self.health.total_votes < (self.health.expected_votes // 2 + 1):
            self.health.errors.append(
                f"Insufficient votes: {self.health.total_votes}/{self.health.expected_votes}"
            )

    def check_nodes(self):
        """Check node membership"""
        output = self.run_command("pvecm nodes")
        if not output:
            self.health.warnings.append("Failed to get node list")
            return

        # Parse node list (skip header)
        lines = output.strip().split('\n')[1:]  # Skip header
        for line in lines:
            if not line.strip():
                continue

            # Example: "   1 0x00000001 foxtrot 192.168.3.5"
            parts = line.split()
            if len(parts) >= 3:
                try:
                    node_id = int(parts[0])
                    name = parts[2] if len(parts) >= 3 else "unknown"
                    ip = parts[3] if len(parts) >= 4 else "unknown"
                    online = True  # If in list, assumed online

                    self.health.nodes.append(NodeStatus(
                        name=name,
                        online=online,
                        node_id=node_id,
                        ip=ip
                    ))
                except (ValueError, IndexError) as e:
                    self.health.warnings.append(f"Failed to parse node line: {line}: {e}")

        # Verify expected node count
        if len(self.health.nodes) != self.health.node_count:
            self.health.warnings.append(
                f"Node count mismatch: expected {self.health.node_count}, found {len(self.health.nodes)}"
            )

    def check_corosync(self):
        """Check corosync ring status"""
        output = self.run_command("corosync-cfgtool -s")
        if not output:
            self.health.warnings.append("Failed to get corosync status")
            return

        # Parse corosync status
        # Example output:
        # Printing ring status.
        # Local node ID 1
        # RING ID 0
        #     id  = 192.168.8.5
        #     status  = ring 0 active with no faults

        current_ring = None
        for line in output.split('\n'):
            line = line.strip()

            if line.startswith('RING ID'):
                ring_match = re.search(r'RING ID (\d+)', line)
                if ring_match:
                    current_ring = int(ring_match.group(1))

            elif 'status' in line.lower() and current_ring is not None:
                status_match = re.search(r'status\s*=\s*(.+)', line)
                if status_match:
                    status = status_match.group(1)

                    # Check for faults
                    if 'no faults' not in status.lower():
                        self.health.errors.append(f"Corosync ring {current_ring}: {status}")

                    self.health.corosync_rings.append(CorosyncStatus(
                        ring_id=current_ring,
                        nodes=[],  # Could parse this if needed
                        status=status
                    ))

    def check_config_version(self):
        """Check cluster configuration version"""
        output = self.run_command("corosync-cmapctl -b totem.config_version")
        if output:
            try:
                self.health.config_version = int(output.strip())
            except ValueError:
                self.health.warnings.append("Failed to parse config version")

    def check_resource_manager(self):
        """Check pve-cluster service status"""
        output = self.run_command("systemctl is-active pve-cluster")
        if output.strip() != "active":
            self.health.errors.append("pve-cluster service is not active")

        # Check pmxcfs filesystem
        output = self.run_command("pvecm status | grep -i 'cluster filesystem'")
        if output and 'online' not in output.lower():
            self.health.warnings.append("Cluster filesystem may not be online")

    def run_all_checks(self) -> ClusterHealth:
        """Run all health checks"""
        self.check_cluster_status()
        self.check_nodes()
        self.check_corosync()
        self.check_config_version()
        self.check_resource_manager()

        return self.health


def main():
    parser = argparse.ArgumentParser(
        description="Check Proxmox cluster health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--node',
        default='foxtrot',
        help='Cluster node to check (default: foxtrot)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Run health checks
    checker = ClusterHealthChecker(args.node)
    health = checker.run_all_checks()

    if args.json:
        # Output as JSON
        print(json.dumps(asdict(health), indent=2))
    else:
        # Human-readable output
        print(f"Cluster Health Check: {health.cluster_name}")
        print("=" * 60)
        print(f"Quorum Status: {'✓ YES' if health.quorate else '✗ NO'}")
        print(f"Nodes: {health.node_count} ({health.total_votes}/{health.expected_votes} votes)")

        if health.config_version:
            print(f"Config Version: {health.config_version}")

        print("\nNodes:")
        for node in health.nodes:
            status = "✓" if node.online else "✗"
            print(f"  {status} {node.name} (ID: {node.node_id}, IP: {node.ip})")

        print("\nCorosync Rings:")
        for ring in health.corosync_rings:
            print(f"  Ring {ring.ring_id}: {ring.status}")

        if health.warnings:
            print("\nWarnings:")
            for warning in health.warnings:
                print(f"  ⚠ {warning}")

        if health.errors:
            print("\nErrors:")
            for error in health.errors:
                print(f"  ✗ {error}")

        print("\n" + "=" * 60)
        if health.is_healthy:
            print("Status: ✓ HEALTHY")
            sys.exit(0)
        else:
            print("Status: ✗ UNHEALTHY")
            sys.exit(1)


if __name__ == '__main__':
    main()
