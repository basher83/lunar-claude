# Converting Bash Scripts to Python uv Scripts

This document guides the conversion of bash scripts to Python uv scripts.

## When Conversion Makes Sense

### ✅ Good Candidates for Conversion

**Convert when**:

- Script needs better error handling
- Cross-platform compatibility required
- Complex data processing needed
- API interactions involved
- Script will grow in complexity

**Examples**:

```bash
# Good candidate - API interaction
curl -X POST https://api.example.com/data \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "active"}'

# Good candidate - Data processing
cat data.json | jq '.users[] | select(.active == true)'

# Good candidate - Complex logic
for file in $(find /data -name "*.log"); do
  count=$(grep -c "ERROR" "$file")
  if [ $count -gt 100 ]; then
    # Complex processing
  fi
done
```

### ❌ Keep as Bash When

**Don't convert when**:

- Simple file operations (cp, mv, mkdir)
- Shell-specific features heavily used (job control, pipes)
- System administration tasks
- Script is <10 lines and works fine
- Team primarily knows bash

**Examples**:

```bash
# Keep as bash - Simple operations
#!/bin/bash
mkdir -p /var/log/app
cp config.yaml /etc/app/

# Keep as bash - Shell-specific
#!/bin/bash
find /data -name "*.tmp" -mtime +7 -delete

# Keep as bash - System admin
#!/bin/bash
systemctl restart nginx
journalctl -u nginx -f
```

## Common Conversions

### File Operations

**Bash**:

```bash
#!/bin/bash
if [ -f "/etc/config.yaml" ]; then
  cp /etc/config.yaml /backup/
fi
```

**Python**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from pathlib import Path
import shutil

config = Path("/etc/config.yaml")
if config.exists():
    shutil.copy(config, "/backup/")
```

### Environment Variables

**Bash**:

```bash
#!/bin/bash
API_URL=${API_URL:-"https://api.example.com"}
if [ -z "$API_TOKEN" ]; then
  echo "Error: API_TOKEN not set" >&2
  exit 1
fi
```

**Python**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import os
import sys

API_URL = os.getenv("API_URL", "https://api.example.com")
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    print("Error: API_TOKEN not set", file=sys.stderr)
    sys.exit(1)
```

### Running Commands

**Bash**:

```bash
#!/bin/bash
set -euo pipefail

output=$(systemctl status nginx)
if [ $? -ne 0 ]; then
  echo "Error: nginx not running"
  exit 1
fi
```

**Python**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import subprocess
import sys

try:
    result = subprocess.run(
        ["systemctl", "status", "nginx"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
except subprocess.CalledProcessError:
    print("Error: nginx not running", file=sys.stderr)
    sys.exit(1)
```

### HTTP Requests

**Bash**:

```bash
#!/bin/bash
response=$(curl -s -X GET https://api.github.com/users/octocat)
name=$(echo "$response" | jq -r '.name')
echo "Name: $name"
```

**Python**:

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

### JSON Processing

**Bash**:

```bash
#!/bin/bash
jq '.users[] | select(.active == true) | .name' data.json
```

**Python**:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
from pathlib import Path

data = json.loads(Path("data.json").read_text())
active_names = [
    user["name"]
    for user in data["users"]
    if user.get("active")
]
print("\n".join(active_names))
```

## Decision Framework

```text
Should I convert this bash script?

├─ Is it >50 lines? → Consider conversion
├─ Does it process JSON/YAML? → Strong candidate
├─ Does it make API calls? → Strong candidate
├─ Does it have complex logic? → Consider conversion
├─ Does it need better error handling? → Consider conversion
├─ Is it mostly shell commands? → Keep as bash
└─ Is it <10 lines and works? → Keep as bash
```

## Hybrid Approach

Sometimes the best solution is calling bash from Python:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Hybrid: Use Python for logic, bash for system commands.
"""

import subprocess

def backup_with_rsync(source: str, dest: str):
    """Use rsync (better than reimplementing in Python)."""
    subprocess.run(
        ["rsync", "-av", "--delete", source, dest],
        check=True
    )

# Python logic here
# ...

# Leverage bash tools where appropriate
backup_with_rsync("/data/", "/backup/")
```

## Summary

**Convert to Python when**:

- Complex logic or data processing
- API interactions
- Cross-platform needs
- Better error handling required
- Will grow in complexity

**Keep as Bash when**:

- Simple file operations
- System administration
- Heavily uses shell features
- Works well and won't change
- Team expertise is bash

**Consider Hybrid**:

- Complex Python logic + system commands
- Leverage both Python libraries and shell tools
