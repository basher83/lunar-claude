#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = ["proxmoxer", "requests"]
# ///
"""
Display Proxmox cluster health and resource usage.

Usage:
    ./cluster_status.py
    ./cluster_status.py --node foxtrot
    ./cluster_status.py --detailed

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


class ClusterMonitor:
    """Monitor Proxmox cluster health and resources."""

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

    def get_cluster_status(self):
        """Get cluster status and quorum info."""
        try:
            status = self.proxmox.cluster.status.get()
            return status
        except ResourceException as e:
            print(f"❌ Failed to get cluster status: {e}", file=sys.stderr)
            return None

    def get_node_status(self, node_name: str):
        """Get detailed node status."""
        try:
            status = self.proxmox.nodes(node_name).status.get()
            return status
        except ResourceException as e:
            print(f"❌ Failed to get node status: {e}", file=sys.stderr)
            return None

    def get_node_vms(self, node_name: str):
        """Get VMs on a node."""
        try:
            vms = self.proxmox.nodes(node_name).qemu.get()
            return vms
        except ResourceException as e:
            print(f"❌ Failed to get VMs: {e}", file=sys.stderr)
            return []

    def display_cluster_overview(self):
        """Display cluster overview."""
        print("🖥️  Proxmox Cluster Status")
        print("=" * 70)

        cluster_status = self.get_cluster_status()
        if not cluster_status:
            return

        # Find cluster info
        cluster_info = next((item for item in cluster_status if item['type'] == 'cluster'), None)
        if cluster_info:
            print(f"\n📊 Cluster: {cluster_info.get('name', 'N/A')}")
            print(f"   Quorum: {cluster_info.get('quorate', 0)} (nodes: {cluster_info.get('nodes', 0)})")

        # Node statuses
        nodes = [item for item in cluster_status if item['type'] == 'node']

        print(f"\n🔧 Nodes ({len(nodes)}):")
        print(f"{'Node':<15} {'Status':<10} {'CPU':<12} {'Memory':<20} {'VMs':<8}")
        print("-" * 70)

        for node_info in nodes:
            node_name = node_info['name']
            online = "✓ Online" if node_info.get('online', 0) == 1 else "✗ Offline"

            # Get detailed status
            detailed = self.get_node_status(node_name)
            if not detailed:
                print(f"{node_name:<15} {online:<10} {'N/A':<12} {'N/A':<20} {'N/A':<8}")
                continue

            # CPU usage
            cpu_pct = detailed.get('cpu', 0) * 100
            cpu_str = f"{cpu_pct:.1f}%"

            # Memory usage
            mem_used = detailed.get('memory', {}).get('used', 0) / (1024**3)  # GB
            mem_total = detailed.get('memory', {}).get('total', 0) / (1024**3)  # GB
            mem_pct = (mem_used / mem_total * 100) if mem_total > 0 else 0
            mem_str = f"{mem_used:.1f}/{mem_total:.1f}GB ({mem_pct:.1f}%)"

            # VM count
            vms = self.get_node_vms(node_name)
            vm_count = len(vms)
            running_vms = len([vm for vm in vms if vm.get('status') == 'running'])
            vm_str = f"{running_vms}/{vm_count}"

            print(f"{node_name:<15} {online:<10} {cpu_str:<12} {mem_str:<20} {vm_str:<8}")

        print("=" * 70)

    def display_node_detail(self, node_name: str):
        """Display detailed node information."""
        print(f"\n🔍 Node Details: {node_name}")
        print("=" * 70)

        status = self.get_node_status(node_name)
        if not status:
            return

        # System info
        print(f"\n💻 System:")
        print(f"   Uptime: {status.get('uptime', 0) / 86400:.1f} days")
        print(f"   Load Average: {status.get('loadavg', ['N/A', 'N/A', 'N/A'])[0]:.2f}")
        print(f"   CPU Cores: {status.get('cpuinfo', {}).get('cpus', 'N/A')}")

        # CPU
        cpu_pct = status.get('cpu', 0) * 100
        print(f"\n🖥️  CPU Usage: {cpu_pct:.1f}%")

        # Memory
        mem = status.get('memory', {})
        mem_used = mem.get('used', 0) / (1024**3)
        mem_total = mem.get('total', 0) / (1024**3)
        mem_free = mem.get('free', 0) / (1024**3)
        mem_pct = (mem_used / mem_total * 100) if mem_total > 0 else 0

        print(f"\n💾 Memory:")
        print(f"   Used: {mem_used:.2f} GB ({mem_pct:.1f}%)")
        print(f"   Free: {mem_free:.2f} GB")
        print(f"   Total: {mem_total:.2f} GB")

        # Storage
        root = status.get('rootfs', {})
        root_used = root.get('used', 0) / (1024**3)
        root_total = root.get('total', 0) / (1024**3)
        root_avail = root.get('avail', 0) / (1024**3)
        root_pct = (root_used / root_total * 100) if root_total > 0 else 0

        print(f"\n💿 Root Filesystem:")
        print(f"   Used: {root_used:.2f} GB ({root_pct:.1f}%)")
        print(f"   Available: {root_avail:.2f} GB")
        print(f"   Total: {root_total:.2f} GB")

        # VMs
        vms = self.get_node_vms(node_name)
        print(f"\n🖼️  Virtual Machines ({len(vms)}):")

        if vms:
            print(f"   {'VMID':<8} {'Name':<25} {'Status':<10} {'CPU':<8} {'Memory':<15}")
            print("   " + "-" * 66)

            for vm in vms:
                vmid = vm.get('vmid', 'N/A')
                name = vm.get('name', 'N/A')[:24]
                status = vm.get('status', 'unknown')
                cpu_pct = vm.get('cpu', 0) * 100 if vm.get('status') == 'running' else 0
                mem = vm.get('mem', 0) / (1024**2) if vm.get('status') == 'running' else 0  # MB

                status_icon = "▶️" if status == "running" else "⏸️"
                print(f"   {vmid:<8} {name:<25} {status_icon} {status:<8} {cpu_pct:>6.1f}% {mem:>8.0f} MB")
        else:
            print("   No VMs found")

        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Display Proxmox cluster health and resource usage"
    )
    parser.add_argument(
        "--node",
        help="Show detailed info for specific node"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed info for all nodes"
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
        monitor = ClusterMonitor(endpoint, "token", token=api_token)
    elif username and password:
        monitor = ClusterMonitor(endpoint, "password", user=username, password=password)
    else:
        print("❌ Authentication required: set PROXMOX_VE_API_TOKEN or PROXMOX_VE_USERNAME/PASSWORD", file=sys.stderr)
        sys.exit(1)

    # Display status
    if args.node:
        monitor.display_node_detail(args.node)
    elif args.detailed:
        monitor.display_cluster_overview()
        # Get all nodes and show details
        cluster_status = monitor.get_cluster_status()
        if cluster_status:
            nodes = [item['name'] for item in cluster_status if item['type'] == 'node']
            for node_name in nodes:
                monitor.display_node_detail(node_name)
    else:
        monitor.display_cluster_overview()


if __name__ == "__main__":
    main()
