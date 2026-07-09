#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Omni Proxmox Provider container management via Tailscale SSH and Proxmox pct.

Purpose: provider-management
Team: homelab
Author: infrastructure@spaceships.work

Usage:
    provider-ctl.py --status
    provider-ctl.py --restart
    provider-ctl.py --logs [N]
    provider-ctl.py --logs [N] --raw

Examples:
    provider-ctl.py --status
    provider-ctl.py --restart
    provider-ctl.py --logs 25
    provider-ctl.py --logs 50 --raw
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime
from typing import Any

TAILSCALE_HOST = os.environ.get("OMNI_PROVIDER_HOST", "root@foxtrot")
PROVIDER_CT = os.environ.get("OMNI_PROVIDER_CT", "200")
PROVIDER_SERVICE = os.environ.get("OMNI_PROVIDER_SERVICE", "proxmox-provider")
CONTAINER_OVERRIDE = os.environ.get("OMNI_PROVIDER_CONTAINER")
DEFAULT_LOG_LINES = 25
MAX_LOG_LINES = 100
RESTART_TIMEOUT = 30
LOG_TIMEOUT = 10
STATUS_TIMEOUT = 10


def provider_command(cmd: str, timeout: int) -> tuple[int, str, str]:
    """Execute a command in the provider LXC through the Foxtrot Tailscale peer."""
    remote_cmd = shlex.join(["pct", "exec", PROVIDER_CT, "--", "sh", "-lc", cmd])

    try:
        result = subprocess.run(
            ["tailscale", "ssh", TAILSCALE_HOST, remote_cmd],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"Timeout after {timeout} seconds"
    except FileNotFoundError:
        return 127, "", "tailscale command not found"


def discover_container(timeout: int) -> tuple[int, str | None]:
    """Resolve the provider container by override or Docker Compose service label."""
    if CONTAINER_OVERRIDE:
        return 0, CONTAINER_OVERRIDE

    service_filter = shlex.quote(f"label=com.docker.compose.service={PROVIDER_SERVICE}")
    rc, out, err = provider_command(
        f"docker ps -a --filter {service_filter} --format '{{{{.Names}}}}'",
        timeout,
    )

    if rc != 0:
        print(f"Error: Failed to discover provider container: {err or out}", file=sys.stderr)
        return 1, None

    containers = [line.strip() for line in out.splitlines() if line.strip()]
    if not containers:
        print(
            f"Error: No container found for Compose service '{PROVIDER_SERVICE}'",
            file=sys.stderr,
        )
        return 1, None

    if len(containers) > 1:
        print(
            f"Error: Multiple containers found for Compose service '{PROVIDER_SERVICE}': "
            f"{', '.join(containers)}",
            file=sys.stderr,
        )
        return 1, None

    return 0, containers[0]


def restart_container() -> int:
    """Restart the provider container idempotently."""
    rc, container = discover_container(RESTART_TIMEOUT)
    if rc != 0 or container is None:
        return 1

    quoted_container = shlex.quote(container)
    rc, out, err = provider_command(f"docker restart {quoted_container}", RESTART_TIMEOUT)

    if rc != 0:
        print(f"Error: Failed to restart container: {err}", file=sys.stderr)
        return 1

    # Verify container is running
    rc, out, err = provider_command(
        f"docker ps --filter name={quoted_container} --filter status=running "
        "--format '{{.Status}}'",
        RESTART_TIMEOUT,
    )

    if rc != 0 or not out.strip():
        print("Error: Container failed to start after restart", file=sys.stderr)
        return 1

    print(f"Container '{container}' restarted successfully")
    return 0


def format_timestamp(ts: float | str) -> str:
    """Convert Unix timestamp or ISO string to human-readable format."""
    try:
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts)
        else:
            try:
                dt = datetime.fromtimestamp(float(ts))
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError, OSError):
        return str(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_container_inspect() -> tuple[int, dict[str, Any] | None]:
    """Fetch container inspect data."""
    rc, container = discover_container(STATUS_TIMEOUT)
    if rc != 0 or container is None:
        return 1, None

    inspect_format = "{{json .}}"
    rc, out, err = provider_command(
        f"docker inspect --format '{inspect_format}' {shlex.quote(container)}",
        STATUS_TIMEOUT,
    )

    if rc == 124:
        print(f"Error: Status retrieval timed out after {STATUS_TIMEOUT}s", file=sys.stderr)
        return 1, None

    if rc != 0:
        message = err or out
        if "No such object" in message or "No such container" in message:
            print(f"Error: Container '{container}' not found", file=sys.stderr)
        else:
            print(f"Error: Failed to inspect container: {message}", file=sys.stderr)
        return 1, None

    try:
        return 0, json.loads(out)
    except json.JSONDecodeError:
        print("Error: Failed to parse container inspect output", file=sys.stderr)
        return 1, None


def get_status() -> int:
    """Report container status and return non-zero if unhealthy."""
    rc, inspect_data = get_container_inspect()
    if rc != 0 or inspect_data is None:
        return 1

    state = inspect_data.get("State", {})
    running = bool(state.get("Running"))
    status = state.get("Status", "unknown")
    health = state.get("Health", {}).get("Status")
    started_at = format_timestamp(state.get("StartedAt", ""))
    finished_at = format_timestamp(state.get("FinishedAt", ""))
    exit_code = state.get("ExitCode")

    print(f"Host: {TAILSCALE_HOST} (CT {PROVIDER_CT})")
    print(f"Container: {inspect_data.get('Name', '').lstrip('/')}")
    print(f"Status: {status}")
    if health:
        print(f"Health: {health}")
    print(f"Running: {'yes' if running else 'no'}")
    print(f"Started: {started_at}")
    if not running and finished_at and finished_at != "0001-01-01 00:00:00":
        print(f"Finished: {finished_at}")
    if exit_code is not None:
        print(f"Exit code: {exit_code}")

    if not running:
        return 1

    if health and health != "healthy":
        return 1

    return 0


def should_include_schematic(entry: dict) -> bool:
    """Check if schematic field should be included based on level and message."""
    level = entry.get("level", "").lower()
    msg = entry.get("msg", "").lower()

    if level not in ("error", "warn", "warning"):
        return False

    keywords = ("schematic", "extension", "kernel")
    return any(kw in msg for kw in keywords)


def format_log_entry(entry: dict) -> str:
    """Format a single log entry for display."""
    level = entry.get("level", "unknown").upper()
    ts = format_timestamp(entry.get("ts", ""))
    machine_id = entry.get("id", "-")
    step = entry.get("step", "-")
    job = entry.get("job", "")
    msg = entry.get("msg", "")

    job_segment = f"{job} | " if job else ""
    line = f"[{level:5}] {ts} | {machine_id} | {step} | {job_segment}{msg}"

    # Conditionally add schematic on next line
    if should_include_schematic(entry) and "schematic" in entry:
        line += f"\n        schematic: {entry['schematic']}"

    return line


def get_logs(count: int, raw: bool) -> int:
    """Retrieve and display container logs."""
    count = min(count, MAX_LOG_LINES)
    rc, container = discover_container(LOG_TIMEOUT)
    if rc != 0 or container is None:
        return 1

    rc, out, err = provider_command(
        f"docker logs --tail {count} {shlex.quote(container)} 2>&1", LOG_TIMEOUT
    )

    if rc == 124:
        print(f"Error: Log retrieval timed out after {LOG_TIMEOUT}s", file=sys.stderr)
        return 1

    if rc != 0:
        if "No such container" in err or "No such container" in out:
            print(f"Error: Container '{container}' not found", file=sys.stderr)
        else:
            print(f"Error: Failed to retrieve logs: {err or out}", file=sys.stderr)
        return 1

    if not out.strip():
        print("No logs available")
        return 0

    if raw:
        print(out)
        return 0

    # Parse and filter JSON logs
    for line in out.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        try:
            entry = json.loads(line)
            print(format_log_entry(entry))
        except json.JSONDecodeError:
            # Non-JSON line, print as-is
            print(line)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage Omni Proxmox Provider container",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status           Show provider container status
  %(prog)s --restart          Restart the provider container
  %(prog)s --logs             Show last 25 log lines (filtered)
  %(prog)s --logs 50          Show last 50 log lines (filtered)
  %(prog)s --logs 10 --raw    Show last 10 log lines (unfiltered JSON)
        """,
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show provider container status",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart the provider container",
    )
    parser.add_argument(
        "--logs",
        nargs="?",
        type=int,
        const=DEFAULT_LOG_LINES,
        metavar="N",
        help=f"Show last N log lines (default: {DEFAULT_LOG_LINES}, max: {MAX_LOG_LINES})",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Show raw JSON logs without filtering (requires --logs)",
    )

    args = parser.parse_args()

    if args.raw and args.logs is None:
        print("Error: --raw requires --logs", file=sys.stderr)
        return 1

    actions = [args.status, args.restart, args.logs is not None]

    if sum(bool(action) for action in actions) == 0:
        parser.print_help()
        return 1

    if sum(bool(action) for action in actions) > 1:
        print("Error: --status, --restart, and --logs are mutually exclusive", file=sys.stderr)
        return 1

    if args.status:
        return get_status()

    if args.restart:
        return restart_container()

    if args.logs is not None:
        return get_logs(args.logs, args.raw)

    return 0


if __name__ == "__main__":
    sys.exit(main())
