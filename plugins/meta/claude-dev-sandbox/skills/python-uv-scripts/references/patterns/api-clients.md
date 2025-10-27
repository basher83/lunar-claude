# API Client Patterns

Patterns for building API clients with uv scripts.

## Basic GET Request

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx

response = httpx.get("https://api.github.com/users/octocat")
response.raise_for_status()
data = response.json()
print(f"Name: {data['name']}")
```

## Authenticated Requests

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
# ]
# ///

import httpx
import os
import sys

api_token = os.getenv("API_TOKEN")
if not api_token:
    print("Error: API_TOKEN not set", file=sys.stderr)
    sys.exit(1)

headers = {"Authorization": f"Bearer {api_token}"}

response = httpx.get(
    "https://api.example.com/data",
    headers=headers,
    timeout=10.0
)
response.raise_for_status()
print(response.json())
```

## POST with JSON

```python
import httpx

data = {
    "name": "example",
    "status": "active"
}

response = httpx.post(
    "https://api.example.com/resources",
    json=data,
    headers={"Authorization": f"Bearer {token}"},
    timeout=10.0
)
response.raise_for_status()
result = response.json()
print(f"Created: {result['id']}")
```

## Query Parameters

```python
import httpx

params = {
    "q": "python",
    "sort": "stars",
    "order": "desc"
}

response = httpx.get(
    "https://api.github.com/search/repositories",
    params=params
)
response.raise_for_status()
repos = response.json()
```

## Error Handling

```python
import httpx
import sys

try:
    with httpx.Client(timeout=10.0) as client:
        response = client.get("https://api.example.com/data")
        response.raise_for_status()
        data = response.json()

except httpx.HTTPStatusError as e:
    status = e.response.status_code
    if status == 401:
        print("Error: Unauthorized - check API key", file=sys.stderr)
    elif status == 404:
        print("Error: Resource not found", file=sys.stderr)
    elif status >= 500:
        print(f"Error: Server error ({status})", file=sys.stderr)
    else:
        print(f"Error: HTTP {status}", file=sys.stderr)
    sys.exit(1)

except httpx.RequestError as e:
    print(f"Error: Request failed - {type(e).__name__}", file=sys.stderr)
    sys.exit(1)
```

## Retry Logic

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.27.0",
#   "tenacity>=8.2.0",
# ]
# ///

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_data(url: str):
    """Fetch data with automatic retry."""
    response = httpx.get(url, timeout=10.0)
    response.raise_for_status()
    return response.json()

data = fetch_data("https://api.example.com/data")
```

## Pagination

```python
import httpx

def fetch_all_pages(base_url: str, headers: dict):
    """Fetch all pages from paginated API."""
    all_results = []
    next_url = base_url

    with httpx.Client(headers=headers, timeout=10.0) as client:
        while next_url:
            response = client.get(next_url)
            response.raise_for_status()
            data = response.json()

            all_results.extend(data["results"])

            # Get next page URL
            next_url = data.get("next")

    return all_results
```

## Rate Limiting

```python
import httpx
import time

def fetch_with_rate_limit(urls: list[str], requests_per_second: int = 2):
    """Fetch URLs respecting rate limit."""
    delay = 1.0 / requests_per_second
    results = []

    for url in urls:
        response = httpx.get(url)
        response.raise_for_status()
        results.append(response.json())

        time.sleep(delay)

    return results
```

## Complete Example

For a complete API client template, see: `assets/templates/api-client.py`

## Best Practices

- Always set timeouts (default: 10 seconds)
- Use `with httpx.Client()` for multiple requests
- Handle specific HTTP status codes (401, 404, 500)
- Don't log sensitive data (tokens, responses)
- Use environment variables for credentials
- Implement retry logic for transient failures
- Respect rate limits
