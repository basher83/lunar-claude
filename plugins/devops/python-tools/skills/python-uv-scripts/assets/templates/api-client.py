#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "rich>=13.0.0",
# ]
# ///
"""
API client template using httpx.

Demonstrates HTTP requests, error handling, and structured output.
Includes environment variable usage for API credentials.

Usage:
    export API_URL="https://api.example.com"
    export API_TOKEN="your-token"
    python api-client.py
"""

import httpx
import os
import sys
from rich import print
from rich.console import Console

console = Console()


def get_env_var(name: str) -> str:
    """Get required environment variable or exit with error."""
    value = os.getenv(name)
    if not value:
        console.print(f"[red]Error: {name} environment variable not set[/red]")
        sys.exit(1)
    return value


def fetch_data(api_url: str, token: str):
    """Fetch data from API with error handling."""
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with httpx.Client() as client:
            response = client.get(api_url, headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        console.print(f"[red]HTTP error {e.response.status_code}[/red]")
        console.print(f"Response: {e.response.text}")
        sys.exit(1)
    except httpx.RequestError as e:
        console.print(f"[red]Request failed: {e}[/red]")
        sys.exit(1)


def main():
    """Main entry point."""
    api_url = get_env_var("API_URL")
    api_token = get_env_var("API_TOKEN")

    console.print(f"[cyan]Fetching data from {api_url}...[/cyan]")

    data = fetch_data(api_url, api_token)

    # Process and display data
    print(data)


if __name__ == "__main__":
    main()
