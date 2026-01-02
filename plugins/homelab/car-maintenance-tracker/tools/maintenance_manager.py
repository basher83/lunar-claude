#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "rich>=13.0.0",
# ]
# ///
"""Maintenance tracking and scheduling for vehicle maintenance records."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


class MaintenanceManager:
    """Manager for vehicle maintenance records."""

    def __init__(self, plugin_root: Path):
        """Initialize maintenance manager.

        Args:
            plugin_root: Path to the plugin root directory
        """
        self.plugin_root = plugin_root
        self.data_dir = plugin_root / "data"
        self.vehicle_file = self.data_dir / "vehicle.json"
        self.maintenance_file = self.data_dir / "maintenance-records.json"

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

    def load_maintenance_data(self) -> dict[str, Any]:
        """Load maintenance records from JSON file."""
        if not self.maintenance_file.exists():
            console.print("[red]Error: maintenance-records.json not found[/red]")
            return {}

        with open(self.maintenance_file) as f:
            return json.load(f)

    def save_maintenance_data(self, data: dict[str, Any]) -> None:
        """Save maintenance records to JSON file."""
        with open(self.maintenance_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_work_order(
        self,
        description: str,
        mileage: int,
        cost: float,
        provider: str,
        notes: str = ""
    ) -> None:
        """Add a new work order to the maintenance records.

        Args:
            description: Description of work performed
            mileage: Vehicle mileage at time of service
            cost: Cost of service
            provider: Service provider name
            notes: Additional notes
        """
        maintenance_data = self.load_maintenance_data()
        vehicle_data = self.load_vehicle_data()

        work_order = {
            "id": len(maintenance_data.get("work_orders", [])) + 1,
            "date": datetime.now().isoformat(),
            "description": description,
            "mileage": mileage,
            "cost": cost,
            "provider": provider,
            "notes": notes
        }

        maintenance_data.setdefault("work_orders", []).append(work_order)
        self.save_maintenance_data(maintenance_data)

        # Update current mileage if higher
        current_mileage = vehicle_data.get("vehicle", {}).get("current_mileage", 0)
        if mileage > current_mileage:
            vehicle_data["vehicle"]["current_mileage"] = mileage
            vehicle_data["vehicle"]["last_updated"] = datetime.now().isoformat()
            self.save_vehicle_data(vehicle_data)

        console.print(f"[green]✓ Work order #{work_order['id']} added successfully[/green]")

    def update_maintenance_item(
        self,
        item_id: str,
        mileage: int,
        date: str | None = None
    ) -> None:
        """Update when a maintenance item was last completed.

        Args:
            item_id: ID of the maintenance item
            mileage: Mileage at completion
            date: Date of completion (defaults to today)
        """
        maintenance_data = self.load_maintenance_data()
        upcoming = maintenance_data.get("upcoming_maintenance", [])

        for item in upcoming:
            if item["id"] == item_id:
                item["last_completed_mileage"] = mileage
                item["last_completed_date"] = date or datetime.now().date().isoformat()
                self.save_maintenance_data(maintenance_data)
                console.print(f"[green]✓ Updated {item['name']}[/green]")
                return

        console.print(f"[red]Error: Maintenance item '{item_id}' not found[/red]")

    def check_due_maintenance(self) -> None:
        """Check and display maintenance items that are due or coming due."""
        vehicle_data = self.load_vehicle_data()
        maintenance_data = self.load_maintenance_data()

        current_mileage = vehicle_data.get("vehicle", {}).get("current_mileage", 0)
        current_date = datetime.now().date()

        upcoming = maintenance_data.get("upcoming_maintenance", [])

        due_items = []
        soon_items = []

        for item in upcoming:
            is_due = False
            is_soon = False

            # Check mileage-based intervals
            if item.get("interval_miles"):
                last_mileage = item.get("last_completed_mileage", 0)
                miles_since = current_mileage - last_mileage
                interval = item["interval_miles"]

                if miles_since >= interval:
                    is_due = True
                elif miles_since >= interval * 0.8:  # 80% threshold
                    is_soon = True

            # Check time-based intervals
            if item.get("interval_months"):
                last_date_str = item.get("last_completed_date")
                if last_date_str:
                    last_date = datetime.fromisoformat(last_date_str).date()
                    months_since = (current_date.year - last_date.year) * 12 + \
                                   (current_date.month - last_date.month)
                    interval = item["interval_months"]

                    if months_since >= interval:
                        is_due = True
                    elif months_since >= interval * 0.8:
                        is_soon = True
                else:
                    # Never completed, mark as due
                    is_due = True

            if is_due:
                due_items.append(item)
            elif is_soon:
                soon_items.append(item)

        # Display due items
        if due_items:
            table = Table(title="[red]⚠ Maintenance DUE Now[/red]", show_header=True)
            table.add_column("Item", style="cyan")
            table.add_column("Last Done", style="yellow")
            table.add_column("Notes", style="white")

            for item in due_items:
                last_info = []
                if item.get("last_completed_mileage"):
                    last_info.append(f"{item['last_completed_mileage']:,} mi")
                if item.get("last_completed_date"):
                    last_info.append(item["last_completed_date"])

                table.add_row(
                    item["name"],
                    " / ".join(last_info) if last_info else "Never",
                    item.get("notes", "")
                )

            console.print(table)

        # Display coming due items
        if soon_items:
            table = Table(title="[yellow]⚡ Maintenance Coming Due Soon[/yellow]", show_header=True)
            table.add_column("Item", style="cyan")
            table.add_column("Last Done", style="yellow")
            table.add_column("Notes", style="white")

            for item in soon_items:
                last_info = []
                if item.get("last_completed_mileage"):
                    last_info.append(f"{item['last_completed_mileage']:,} mi")
                if item.get("last_completed_date"):
                    last_info.append(item["last_completed_date"])

                table.add_row(
                    item["name"],
                    " / ".join(last_info) if last_info else "Never",
                    item.get("notes", "")
                )

            console.print(table)

        if not due_items and not soon_items:
            console.print("[green]✓ All maintenance is up to date![/green]")

    def list_work_orders(self, limit: int = 10) -> None:
        """Display recent work orders.

        Args:
            limit: Maximum number of work orders to display
        """
        maintenance_data = self.load_maintenance_data()
        work_orders = maintenance_data.get("work_orders", [])

        if not work_orders:
            console.print("[yellow]No work orders recorded yet[/yellow]")
            return

        # Sort by date (most recent first)
        sorted_orders = sorted(
            work_orders,
            key=lambda x: x.get("date", ""),
            reverse=True
        )[:limit]

        table = Table(title=f"Recent Work Orders (Last {limit})")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Date", style="magenta")
        table.add_column("Mileage", justify="right", style="yellow")
        table.add_column("Description", style="white")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Provider", style="blue")

        for order in sorted_orders:
            date_str = order.get("date", "")
            if date_str:
                date_obj = datetime.fromisoformat(date_str)
                date_display = date_obj.strftime("%Y-%m-%d")
            else:
                date_display = "N/A"

            table.add_row(
                str(order.get("id", "")),
                date_display,
                f"{order.get('mileage', 0):,}",
                order.get("description", ""),
                f"${order.get('cost', 0):.2f}",
                order.get("provider", "")
            )

        console.print(table)


def main() -> None:
    """Main entry point."""
    import sys

    script_path = Path(__file__).resolve()
    plugin_root = script_path.parent.parent

    manager = MaintenanceManager(plugin_root)

    if len(sys.argv) < 2:
        console.print("[yellow]Usage: maintenance_manager.py [check-due|list-orders|add-order|update-item][/yellow]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "check-due":
        manager.check_due_maintenance()
    elif command == "list-orders":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        manager.list_work_orders(limit)
    elif command == "add-order":
        # Interactive mode would go here
        console.print("[yellow]Use the slash command /car-add-work-order for interactive entry[/yellow]")
    elif command == "update-item":
        console.print("[yellow]Use the slash command /car-update-maintenance for interactive entry[/yellow]")
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
