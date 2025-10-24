# System Automation Patterns

> **Status**: 🚧 Placeholder - Content in development

## Overview

Patterns for system administration, monitoring, and automation using psutil, subprocess, and system libraries in UV single-file scripts.

## Topics to Cover

- [ ] psutil for system monitoring
- [ ] subprocess for command execution
- [ ] File system operations
- [ ] Process management
- [ ] SSH remote execution
- [ ] Cron/scheduled task integration
- [ ] Log file analysis

## Quick Example

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["psutil>=5.9.0", "rich>=13.0.0"]
# ///
import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def show_disk_usage():
    table = Table(title="Disk Usage")
    table.add_column("Device", style="cyan")
    table.add_column("Mount", style="magenta")
    table.add_column("Used", style="yellow")
    table.add_column("Free", style="green")

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        table.add_row(
            partition.device,
            partition.mountpoint,
            f"{usage.percent}%",
            f"{usage.free / (1024**3):.2f} GB"
        )

    console.print(table)
```

## TODO

This file will be expanded to include:

- Complete psutil monitoring patterns
- Safe subprocess execution
- SSH automation patterns
- System health checks
- Automated maintenance tasks
