#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests>=2.31.0",
#     "rich>=13.0.0",
# ]
# ///
"""NHTSA API integration for vehicle recalls, complaints, and TSBs."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from rich.console import Console
from rich.table import Table

console = Console()

# NHTSA API endpoints
NHTSA_BASE_URL = "https://api.nhtsa.gov"
COMPLAINTS_URL = f"{NHTSA_BASE_URL}/complaints/complaintsByVehicle"
RECALLS_URL = f"{NHTSA_BASE_URL}/SafetyRatings/modelyear"


class NHTSAClient:
    """Client for interacting with NHTSA API."""

    def __init__(self, plugin_root: Path):
        """Initialize NHTSA client.

        Args:
            plugin_root: Path to the plugin root directory
        """
        self.plugin_root = plugin_root
        self.data_dir = plugin_root / "data"
        self.vehicle_file = self.data_dir / "vehicle.json"

    def load_vehicle_data(self) -> dict[str, Any]:
        """Load vehicle data from JSON file."""
        if not self.vehicle_file.exists():
            console.print("[red]Error: vehicle.json not found[/red]")
            return {}

        with open(self.vehicle_file) as f:
            return json.load(f)

    def save_vehicle_data(self, data: dict[str, Any]) -> None:
        """Save vehicle data to JSON file."""
        with open(self.vehicle_file, "w") as f:
            json.dump(data, f, indent=2)

    def fetch_recalls(self, year: int, make: str, model: str) -> list[dict[str, Any]]:
        """Fetch recalls for a specific vehicle.

        Args:
            year: Vehicle year
            make: Vehicle make
            model: Vehicle model

        Returns:
            List of recall records
        """
        try:
            url = f"https://api.nhtsa.gov/recalls/recallsByVehicle"
            params = {"make": make, "model": model, "modelYear": year}

            console.print(f"[cyan]Fetching recalls for {year} {make} {model}...[/cyan]")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            recalls = data.get("results", [])
            console.print(f"[green]Found {len(recalls)} recall(s)[/green]")
            return recalls

        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching recalls: {e}[/red]")
            return []

    def fetch_complaints(self, year: int, make: str, model: str) -> list[dict[str, Any]]:
        """Fetch consumer complaints for a specific vehicle.

        Args:
            year: Vehicle year
            make: Vehicle make
            model: Vehicle model

        Returns:
            List of complaint records
        """
        try:
            url = f"https://api.nhtsa.gov/complaints/complaintsByVehicle"
            params = {"make": make, "model": model, "modelYear": year}

            console.print(f"[cyan]Fetching complaints for {year} {make} {model}...[/cyan]")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            complaints = data.get("results", [])
            console.print(f"[green]Found {len(complaints)} complaint(s)[/green]")
            return complaints

        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching complaints: {e}[/red]")
            return []

    def update_nhtsa_cache(self) -> None:
        """Update the NHTSA cache with latest recalls and complaints."""
        vehicle_data = self.load_vehicle_data()
        vehicle = vehicle_data.get("vehicle", {})

        year = vehicle.get("year")
        make = vehicle.get("make")
        model = vehicle.get("model")

        if not all([year, make, model]):
            console.print("[red]Error: Vehicle information incomplete[/red]")
            return

        # Fetch data from NHTSA
        recalls = self.fetch_recalls(year, make, model)
        complaints = self.fetch_complaints(year, make, model)

        # Update cache
        vehicle_data["nhtsa_cache"] = {
            "recalls": recalls,
            "complaints": complaints,
            "last_fetched": datetime.now().isoformat()
        }

        self.save_vehicle_data(vehicle_data)
        console.print("[green]✓ NHTSA cache updated successfully[/green]")

    def display_recalls(self) -> None:
        """Display recalls in a formatted table."""
        vehicle_data = self.load_vehicle_data()
        recalls = vehicle_data.get("nhtsa_cache", {}).get("recalls", [])

        if not recalls:
            console.print("[yellow]No recalls found for this vehicle[/yellow]")
            return

        table = Table(title="Safety Recalls")
        table.add_column("NHTSA ID", style="cyan")
        table.add_column("Component", style="magenta")
        table.add_column("Summary", style="white")
        table.add_column("Consequence", style="red")

        for recall in recalls:
            table.add_row(
                recall.get("NHTSACampaignNumber", "N/A"),
                recall.get("Component", "N/A"),
                recall.get("Summary", "N/A")[:100] + "...",
                recall.get("Conequence", "N/A")[:100] + "..."
            )

        console.print(table)

    def display_common_issues(self, limit: int = 10) -> None:
        """Display most common complaints.

        Args:
            limit: Maximum number of issues to display
        """
        vehicle_data = self.load_vehicle_data()
        complaints = vehicle_data.get("nhtsa_cache", {}).get("complaints", [])

        if not complaints:
            console.print("[yellow]No complaints found for this vehicle[/yellow]")
            return

        # Group by component
        component_counts: dict[str, int] = {}
        for complaint in complaints:
            component = complaint.get("components", "Unknown")
            component_counts[component] = component_counts.get(component, 0) + 1

        # Sort by frequency
        sorted_components = sorted(
            component_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        table = Table(title=f"Top {limit} Common Issues")
        table.add_column("Component", style="cyan")
        table.add_column("Complaints", justify="right", style="magenta")

        for component, count in sorted_components:
            table.add_row(component, str(count))

        console.print(table)


def main() -> None:
    """Main entry point."""
    import sys

    # Determine plugin root (assuming script is in tools/ subdirectory)
    script_path = Path(__file__).resolve()
    plugin_root = script_path.parent.parent

    client = NHTSAClient(plugin_root)

    if len(sys.argv) < 2:
        console.print("[yellow]Usage: nhtsa_api.py [update|recalls|issues][/yellow]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "update":
        client.update_nhtsa_cache()
    elif command == "recalls":
        client.display_recalls()
    elif command == "issues":
        client.display_common_issues()
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
