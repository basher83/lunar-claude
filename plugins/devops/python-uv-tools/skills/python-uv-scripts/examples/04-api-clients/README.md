# API Client Examples

Production-ready API client scripts demonstrating modern Python patterns with uv.

## Examples

### netbox_client.py

Complete NetBox API client showing all best practices:

**Features:**

- PEP 723 inline dependency management
- Infisical secrets integration (Virgo-Core security pattern)
- Type hints and dataclasses
- Input validation
- Comprehensive error handling
- Rich formatted output (tables, panels)
- Argparse CLI interface
- Proper documentation

**Usage:**

```bash
# List all VMs in Matrix cluster
./netbox_client.py

# Query specific VM
./netbox_client.py --vm docker-01

# Show help
./netbox_client.py --help
```

**Key Patterns Demonstrated:**

1. **Secrets Management (Infisical):**

   ```python
   client = InfisicalClient()
   token = client.get_secret(
       secret_name="NETBOX_API_TOKEN",
       project_id="7b832220-24c0-45bc-a5f1-ce9794a31259",
       environment="prod",
       path="/matrix"
   ).secret_value
   ```

2. **Input Validation:**

   ```python
   def validate_vm_name(name: str) -> bool:
       """Validate VM name format."""
       pattern = r'^[a-z0-9-]+$'
       return bool(re.match(pattern, name))
   ```

3. **Error Handling:**

   ```python
   try:
       vm = nb.virtualization.virtual_machines.get(name=vm_name)
       if not vm:
           console.print(f"[yellow]VM not found[/yellow]")
           return None
   except Exception as e:
       console.print(f"[red]Error: {e}[/red]")
       return None
   ```

4. **Rich Output:**

   ```python
   table = Table(title="Matrix Cluster VMs")
   table.add_column("ID", style="cyan")
   table.add_column("Name", style="green")
   # ... add rows ...
   console.print(table)
   ```

5. **Type Hints:**

   ```python
   def get_vm_details(nb: pynetbox.api, vm_name: str) -> Optional[dict]:
       """Get detailed VM information."""
       ...
   ```

## When to Use This Pattern

✅ **Use API client scripts when:**

- Querying external APIs (NetBox, GitHub, cloud providers)
- Building CLI tools for infrastructure automation
- Creating reusable automation utilities
- Need formatted output (tables, JSON)

✅ **Benefits:**

- Self-contained (uv handles dependencies)
- Secure (Infisical for secrets)
- Fast to run (uv caching)
- Easy to distribute (single file)

## Dependencies

The example uses:

- `pynetbox>=7.0.0` - NetBox API client
- `infisical-python>=2.3.3` - Secrets management
- `rich>=13.0.0` - Terminal formatting

All managed via PEP 723 inline metadata - no manual installation needed!

## Security

**✅ DO:**

- Use Infisical for API tokens
- Validate all input
- Handle errors gracefully
- Use HTTPS only

**❌ DON'T:**

- Hardcode API tokens
- Skip input validation
- Ignore errors
- Use HTTP in production

## Related Documentation

- [Main Skill Documentation](../../SKILL.md)
- [Security Patterns](../../reference/security-patterns.md)
- [NetBox API Guide](../../../netbox-powerdns-integration/reference/netbox-api-guide.md)
- [NetBox Best Practices](../../../netbox-powerdns-integration/reference/netbox-best-practices.md)

## Testing

```bash
# Dry run (will attempt to connect to NetBox)
./netbox_client.py

# Test with specific VM
./netbox_client.py --vm docker-01

# Check script syntax
python3 -m py_compile netbox_client.py
```

## Extending

To create your own API client based on this example:

1. Copy `netbox_client.py` to your new script
2. Update PEP 723 dependencies for your API
3. Replace NetBox client with your API client (e.g., GitHub, AWS, etc.)
4. Adjust validation and output formatting
5. Update documentation

Example for GitHub API:

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "PyGithub>=2.0.0",
#   "infisical-python>=2.3.3",
#   "rich>=13.0.0",
# ]
# ///

from github import Github
from infisical import InfisicalClient

# Get token
client = InfisicalClient()
token = client.get_secret(
    secret_name="GITHUB_TOKEN",
    ...
).secret_value

# Connect
gh = Github(token)

# Query
repos = gh.get_user().get_repos()
for repo in repos:
    print(repo.name)
```
