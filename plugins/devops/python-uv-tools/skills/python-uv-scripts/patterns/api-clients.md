# API Client Patterns

> **Status**: 🚧 Placeholder - Content in development

## Overview

Patterns for building API clients using httpx, requests, and handling authentication in UV single-file scripts.

## Topics to Cover

- [ ] httpx async patterns (recommended)
- [ ] requests synchronous patterns
- [ ] Authentication strategies (Bearer, API keys, OAuth)
- [ ] Rate limiting and retry logic
- [ ] Error handling for HTTP errors
- [ ] Response validation
- [ ] Session management

## Quick Example

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27.0", "rich>=13.0.0"]
# ///
import httpx
from rich.console import Console

console = Console()

def fetch_data(url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

## TODO

This file will be expanded to include:

- Complete httpx patterns (sync and async)
- Authentication best practices
- Retry strategies with exponential backoff
- Rate limiting implementation
- Response caching
