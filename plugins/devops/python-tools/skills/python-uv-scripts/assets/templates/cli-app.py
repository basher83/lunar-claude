#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.9.0",
#   "rich>=13.0.0",
# ]
# ///
"""
CLI application template using Typer and Rich.

Demonstrates command-line argument parsing, subcommands, and formatted output.

Usage:
    python cli-app.py --help
    python cli-app.py greet "World"
    python cli-app.py process input.txt --output output.txt
"""

import typer
from rich import print
from rich.console import Console
from pathlib import Path

app = typer.Typer()
console = Console()


@app.command()
def greet(name: str):
    """Greet someone by name."""
    print(f"[green]Hello, {name}![/green]")


@app.command()
def process(
    input_file: Path = typer.Argument(..., help="Input file to process"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file path"),
):
    """Process a file and optionally write results."""
    if not input_file.exists():
        console.print(f"[red]Error: {input_file} not found[/red]")
        raise typer.Exit(code=1)

    # Process file
    with open(input_file) as f:
        content = f.read()

    console.print(f"[cyan]Processing {input_file}...[/cyan]")

    # Your processing logic here
    result = content.upper()  # Example transformation

    if output:
        output.write_text(result)
        console.print(f"[green]✓ Written to {output}[/green]")
    else:
        print(result)


if __name__ == "__main__":
    app()
