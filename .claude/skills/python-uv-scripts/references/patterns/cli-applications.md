# CLI Application Patterns

Patterns for building command-line applications with uv scripts.

## Basic CLI with Typer

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///

import typer
from rich import print

app = typer.Typer()

@app.command()
def main(
    name: str = typer.Argument(..., help="Your name"),
    greeting: str = typer.Option("Hello", "--greeting", "-g"),
):
    """Greet someone."""
    print(f"[green]{greeting}, {name}![/green]")

if __name__ == "__main__":
    app()
```

## Multiple Subcommands

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a new resource."""
    print(f"Creating: {name}")

@app.command()
def delete(name: str):
    """Delete a resource."""
    print(f"Deleting: {name}")

if __name__ == "__main__":
    app()
```

Usage:

```bash
./script.py create foo
./script.py delete bar
```

## File Input/Output

```python
import typer
from pathlib import Path

def process_file(
    input_file: Path = typer.Argument(..., exists=True),
    output: Path = typer.Option(None, "--output", "-o"),
):
    """Process a file."""
    content = input_file.read_text()

    # Process
    result = content.upper()

    if output:
        output.write_text(result)
        print(f"Written to: {output}")
    else:
        print(result)
```

## Progress Bars

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "rich>=13.0.0",
# ]
# ///

from rich.progress import track
import time

for item in track(range(100), description="Processing..."):
    time.sleep(0.01)  # Simulate work
```

## Formatted Tables

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "rich>=13.0.0",
# ]
# ///

from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Results")
table.add_column("Name", style="cyan")
table.add_column("Status", style="green")

table.add_row("Task 1", "✓ Complete")
table.add_row("Task 2", "⏳ Pending")

console.print(table)
```

For complete template, see: `assets/templates/cli-app.py`
