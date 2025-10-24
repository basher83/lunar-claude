#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
CEPH Cluster Health Checker

Validates CEPH storage cluster health including:
- Cluster health status
- Monitor and manager status
- OSD status and distribution
- Pool configuration and usage
- PG state verification

Usage:
    python check_ceph_health.py [--node NODE] [--json]

Examples:
    # Check CEPH health (requires SSH access to cluster node)
    python check_ceph_health.py --node foxtrot

    # Output as JSON for parsing
    python check_ceph_health.py --node foxtrot --json

    # Check minimum OSD count
    python check_ceph_health.py --node foxtrot --min-osds 12
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional


@dataclass
class OSDStatus:
    """OSD status information"""
    osd_id: int
    host: str
    status: str  # up/down
    in_cluster: bool
    weight: float
    device_class: str


@dataclass
class PoolStatus:
    """Pool status information"""
    name: str
    pool_id: int
    size: int
    min_size: int
    pg_num: int
    pgp_num: int
    used_bytes: int
    max_avail_bytes: int
    percent_used: float


@dataclass
class MonitorStatus:
    """Monitor status"""
    name: str
    rank: int
    address: str
    in_quorum: bool


@dataclass
class ManagerStatus:
    """Manager status"""
    name: str
    active: bool
    address: str


@dataclass
class CEPHHealth:
    """Overall CEPH health"""
    status: str  # HEALTH_OK, HEALTH_WARN, HEALTH_ERR
    num_osds: int
    num_up_osds: int
    num_in_osds: int
    num_pgs: int
    num_active_clean_pgs: int
    monitors: List[MonitorStatus] = field(default_factory=list)
    managers: List[ManagerStatus] = field(default_factory=list)
    osds: List[OSDStatus] = field(default_factory=list)
    pools: List[PoolStatus] = field(default_factory=list)
    data_bytes: int = 0
    used_bytes: int = 0
    avail_bytes: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def is_healthy(self) -> bool:
        """Check if CEPH is in healthy state"""
        return (
            self.status == 'HEALTH_OK' and
            self.num_up_osds == self.num_osds and
            self.num_in_osds == self.num_osds and
            self.num_active_clean_pgs == self.num_pgs and
            len(self.errors) == 0
        )

    @property
    def percent_used(self) -> float:
        """Calculate cluster usage percentage"""
        if self.data_bytes == 0:
            return 0.0
        return (self.used_bytes / self.data_bytes) * 100


class CEPHHealthChecker:
    """Check CEPH cluster health via SSH"""

    def __init__(self, node: str):
        # Validate node is a valid hostname or IP address
        if not self._validate_node(node):
            raise ValueError(f"Invalid node name or IP address: {node}")
        self.node = node
        self.health = CEPHHealth(
            status="UNKNOWN",
            num_osds=0,
            num_up_osds=0,
            num_in_osds=0,
            num_pgs=0,
            num_active_clean_pgs=0
        )

    def _validate_node(self, node: str) -> bool:
        """Validate node is a valid hostname or IP address"""
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
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after 30s: {command}"
            self.health.errors.append(error_msg)
            raise RuntimeError(error_msg) from e
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {command}: {e.stderr}"
            self.health.errors.append(error_msg)
            raise RuntimeError(error_msg) from e

    def check_ceph_status(self):
        """Check ceph status output"""
        output = self.run_command("ceph status --format json")
        if not output:
            self.health.errors.append("Failed to get CEPH status")
            return

        try:
            status_data = json.loads(output)

            # Parse overall health
            self.health.status = status_data.get('health', {}).get('status', 'UNKNOWN')

            # Parse OSD map
            osd_map = status_data.get('osdmap', {}).get('osdmap', {})
            self.health.num_osds = osd_map.get('num_osds', 0)
            self.health.num_up_osds = osd_map.get('num_up_osds', 0)
            self.health.num_in_osds = osd_map.get('num_in_osds', 0)

            # Parse PG map
            pg_map = status_data.get('pgmap', {})
            self.health.num_pgs = pg_map.get('num_pgs', 0)

            # Parse PG states
            pg_states = pg_map.get('pgs_by_state', [])
            for state in pg_states:
                if state.get('state_name') == 'active+clean':
                    self.health.num_active_clean_pgs = state.get('count', 0)

            # Parse storage usage
            self.health.data_bytes = pg_map.get('data_bytes', 0)
            self.health.used_bytes = pg_map.get('bytes_used', 0)
            self.health.avail_bytes = pg_map.get('bytes_avail', 0)

            # Check for health warnings
            health_checks = status_data.get('health', {}).get('checks', {})
            for check_name, check_data in health_checks.items():
                severity = check_data.get('severity', '')
                summary = check_data.get('summary', {}).get('message', '')

                if severity == 'HEALTH_ERR':
                    self.health.errors.append(f"{check_name}: {summary}")
                elif severity == 'HEALTH_WARN':
                    self.health.warnings.append(f"{check_name}: {summary}")

        except (json.JSONDecodeError, KeyError) as e:
            self.health.errors.append(f"Failed to parse CEPH status: {e}")

    def check_monitors(self):
        """Check monitor status"""
        output = self.run_command("ceph mon dump --format json")
        if not output:
            self.health.warnings.append("Failed to get monitor status")
            return

        try:
            mon_data = json.loads(output)
            quorum = set()

            # Get quorum members
            quorum_output = self.run_command("ceph quorum_status --format json")
            if quorum_output:
                quorum_data = json.loads(quorum_output)
                quorum = set(quorum_data.get('quorum', []))

            # Parse monitors
            for mon in mon_data.get('mons', []):
                self.health.monitors.append(MonitorStatus(
                    name=mon.get('name', ''),
                    rank=mon.get('rank', -1),
                    address=mon.get('addr', ''),
                    in_quorum=mon.get('rank', -1) in quorum
                ))

            # Check if all monitors are in quorum
            not_in_quorum = [m.name for m in self.health.monitors if not m.in_quorum]
            if not_in_quorum:
                self.health.warnings.append(
                    f"Monitors not in quorum: {', '.join(not_in_quorum)}"
                )

        except (json.JSONDecodeError, KeyError) as e:
            self.health.warnings.append(f"Failed to parse monitor status: {e}")

    def check_managers(self):
        """Check manager status"""
        output = self.run_command("ceph mgr dump --format json")
        if not output:
            self.health.warnings.append("Failed to get manager status")
            return

        try:
            mgr_data = json.loads(output)

            # Active manager
            active_name = mgr_data.get('active_name', '')
            active_addr = mgr_data.get('active_addr', '')
            if active_name:
                self.health.managers.append(ManagerStatus(
                    name=active_name,
                    active=True,
                    address=active_addr
                ))

            # Standby managers
            for standby in mgr_data.get('standbys', []):
                self.health.managers.append(ManagerStatus(
                    name=standby.get('name', ''),
                    active=False,
                    address=standby.get('gid', '')
                ))

        except (json.JSONDecodeError, KeyError) as e:
            self.health.warnings.append(f"Failed to parse manager status: {e}")

    def check_osds(self):
        """Check OSD status"""
        output = self.run_command("ceph osd tree --format json")
        if not output:
            self.health.warnings.append("Failed to get OSD tree")
            return

        try:
            osd_data = json.loads(output)

            # Parse OSD nodes
            for node in osd_data.get('nodes', []):
                if node.get('type') == 'osd':
                    osd_id = node.get('id', -1)
                    status = node.get('status', 'unknown')
                    in_cluster = node.get('exists', 0) == 1

                    self.health.osds.append(OSDStatus(
                        osd_id=osd_id,
                        host=node.get('name', 'unknown'),
                        status=status,
                        in_cluster=in_cluster,
                        weight=node.get('crush_weight', 0.0),
                        device_class=node.get('device_class', 'unknown')
                    ))

            # Check for down OSDs
            down_osds = [o.osd_id for o in self.health.osds if o.status != 'up']
            if down_osds:
                self.health.errors.append(f"OSDs down: {down_osds}")

        except (json.JSONDecodeError, KeyError) as e:
            self.health.warnings.append(f"Failed to parse OSD tree: {e}")

    def check_pools(self):
        """Check pool status"""
        output = self.run_command("ceph osd pool ls detail --format json")
        if not output:
            self.health.warnings.append("Failed to get pool information")
            return

        try:
            pool_data = json.loads(output)

            for pool in pool_data:
                pool_name = pool.get('pool_name', '')

                # Get pool stats
                stats_output = self.run_command(f"ceph osd pool stats {pool_name} --format json")
                if stats_output:
                    stats = json.loads(stats_output)
                    pool_stats = stats[0] if stats else {}

                    self.health.pools.append(PoolStatus(
                        name=pool_name,
                        pool_id=pool.get('pool', 0),
                        size=pool.get('size', 0),
                        min_size=pool.get('min_size', 0),
                        pg_num=pool.get('pg_num', 0),
                        pgp_num=pool.get('pgp_num', 0),
                        used_bytes=pool_stats.get('bytes_used', 0),
                        max_avail_bytes=pool_stats.get('max_avail', 0),
                        percent_used=pool_stats.get('percent_used', 0.0) * 100
                    ))

        except (json.JSONDecodeError, KeyError) as e:
            self.health.warnings.append(f"Failed to parse pool information: {e}")

    def check_pg_state(self):
        """Verify all PGs are active+clean"""
        if self.health.num_active_clean_pgs != self.health.num_pgs:
            self.health.errors.append(
                f"Not all PGs active+clean: {self.health.num_active_clean_pgs}/{self.health.num_pgs}"
            )

    def run_all_checks(self) -> CEPHHealth:
        """Run all health checks"""
        self.check_ceph_status()
        self.check_monitors()
        self.check_managers()
        self.check_osds()
        self.check_pools()
        self.check_pg_state()

        return self.health


def human_readable_size(bytes_val: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} EB"


def main():
    parser = argparse.ArgumentParser(
        description="Check CEPH cluster health",
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
    parser.add_argument(
        '--min-osds',
        type=int,
        help='Minimum expected OSD count (error if below this)'
    )

    args = parser.parse_args()

    # Run health checks
    checker = CEPHHealthChecker(args.node)
    health = checker.run_all_checks()

    # Check minimum OSD count
    if args.min_osds and health.num_osds < args.min_osds:
        health.errors.append(
            f"OSD count below minimum: {health.num_osds} < {args.min_osds}"
        )

    if args.json:
        # Output as JSON
        print(json.dumps(asdict(health), indent=2))
        # Exit with appropriate code based on health status
        sys.exit(0 if health.is_healthy else 1)
    else:
        # Human-readable output
        print("CEPH Cluster Health Check")
        print("=" * 60)
        print(f"Overall Status: {health.status}")
        print(f"OSDs: {health.num_up_osds}/{health.num_osds} up, {health.num_in_osds}/{health.num_osds} in")
        print(f"PGs: {health.num_active_clean_pgs}/{health.num_pgs} active+clean")
        print(f"Usage: {health.percent_used:.1f}% ({human_readable_size(health.used_bytes)}/{human_readable_size(health.data_bytes)})")

        print("\nMonitors:")
        for mon in health.monitors:
            quorum_status = "✓" if mon.in_quorum else "✗"
            print(f"  {quorum_status} {mon.name} (rank: {mon.rank}, {mon.address})")

        print("\nManagers:")
        for mgr in health.managers:
            active_status = "ACTIVE" if mgr.active else "STANDBY"
            print(f"  {mgr.name} ({active_status}, {mgr.address})")

        print("\nOSDs:")
        for osd in health.osds:
            status = "✓" if osd.status == 'up' else "✗"
            in_status = "in" if osd.in_cluster else "out"
            print(f"  {status} osd.{osd.osd_id} on {osd.host} ({in_status}, {osd.device_class})")

        print("\nPools:")
        for pool in health.pools:
            print(f"  {pool.name}: size={pool.size}, min_size={pool.min_size}, "
                  f"pgs={pool.pg_num}, used={pool.percent_used:.1f}%")

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
