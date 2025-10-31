#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "polars>=0.20.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Data processing template using Polars.

Demonstrates reading, transforming, and analyzing data with
modern data processing libraries.

Usage:
    python data-processor.py input.csv
    python data-processor.py data/*.csv --output results/
"""

import sys
from pathlib import Path
import polars as pl
from rich.console import Console
from rich.table import Table

console = Console()


def process_csv(file_path: Path) -> pl.DataFrame:
    """Read and process a CSV file."""
    try:
        df = pl.read_csv(file_path)
        console.print(f"[cyan]Loaded {len(df)} rows from {file_path.name}[/cyan]")

        # Example transformations
        # df = df.filter(pl.col("status") == "active")
        # df = df.with_columns(pl.col("amount").cast(pl.Float64))

        return df

    except Exception as e:
        console.print(f"[red]Error processing {file_path}: {e}[/red]")
        sys.exit(1)


def display_summary(df: pl.DataFrame):
    """Display data summary using Rich tables."""
    table = Table(title="Data Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Rows", str(len(df)))
    table.add_row("Columns", str(len(df.columns)))

    # Example statistics
    # if "amount" in df.columns:
    #     table.add_row("Total Amount", f"${df['amount'].sum():,.2f}")

    console.print(table)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[red]Usage: python data-processor.py <input.csv>[/red]")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        console.print(f"[red]Error: {input_path} not found[/red]")
        sys.exit(1)

    df = process_csv(input_path)
    display_summary(df)

    # Optional: Save results
    # output_path = Path("output.csv")
    # df.write_csv(output_path)
    # console.print(f"[green]✓ Saved to {output_path}[/green]")


if __name__ == "__main__":
    main()
