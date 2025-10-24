# DNS Naming Conventions

## Overview

Consistent DNS naming is critical for automation and infrastructure documentation. This document defines the naming conventions used in the Virgo-Core infrastructure.

## Standard Pattern

**Format:** `<service>-<number>-<purpose>.<domain>`

**Components:**

- `<service>` - Service type (docker, k8s, proxmox, storage, db, etc.)
- `<number>` - Instance number (01, 02, 03, etc.) - always 2 digits
- `<purpose>` - Specific purpose or application name
- `<domain>` - DNS domain (e.g., spaceships.work)

**Regex Pattern:**

```regex
^[a-z0-9-]+-\d{2}-[a-z0-9-]+\.[a-z0-9.-]+$
```

## Service Types

### Container Platforms

**Docker hosts:**

```text
docker-01-nexus.spaceships.work          # Nexus container registry
docker-02-gitlab.spaceships.work         # GitLab CI/CD
docker-03-monitoring.spaceships.work     # Monitoring stack (Prometheus, Grafana)
```

**Kubernetes nodes:**

```text
k8s-01-master.spaceships.work            # Control plane node 1
k8s-02-master.spaceships.work            # Control plane node 2
k8s-03-master.spaceships.work            # Control plane node 3
k8s-04-worker.spaceships.work            # Worker node 1
k8s-05-worker.spaceships.work            # Worker node 2
```

### Infrastructure

**Proxmox nodes:**

```text
proxmox-foxtrot-mgmt.spaceships.work     # Foxtrot management interface
proxmox-foxtrot-ceph.spaceships.work     # Foxtrot CEPH public interface
proxmox-golf-mgmt.spaceships.work        # Golf management interface
proxmox-hotel-mgmt.spaceships.work       # Hotel management interface
```

**Storage systems:**

```text
storage-01-nas.spaceships.work           # NAS storage (TrueNAS/FreeNAS)
storage-02-backup.spaceships.work        # Backup storage
storage-03-archive.spaceships.work       # Long-term archive storage
```

### Databases

```text
db-01-postgres.spaceships.work           # PostgreSQL primary
db-02-postgres.spaceships.work           # PostgreSQL replica
db-03-mysql.spaceships.work              # MySQL/MariaDB
db-04-redis.spaceships.work              # Redis cache
```

### Network Services

```text
network-01-pfsense.spaceships.work       # pfSense router
network-02-unifi.spaceships.work         # UniFi controller
network-03-dns.spaceships.work           # DNS server (PowerDNS)
network-04-dhcp.spaceships.work          # DHCP server
```

### Application Services

```text
app-01-netbox.spaceships.work            # NetBox IPAM
app-02-vault.spaceships.work             # HashiCorp Vault
app-03-consul.spaceships.work            # HashiCorp Consul
app-04-nomad.spaceships.work             # HashiCorp Nomad
```

## Special Cases

### Management Interfaces

For infrastructure with multiple interfaces, include interface purpose:

```text
proxmox-<node>-mgmt.spaceships.work      # Management network
proxmox-<node>-ceph.spaceships.work      # CEPH public network
proxmox-<node>-backup.spaceships.work    # Backup network
```

### Virtual IPs (FHRP/VIPs)

```text
vip-01-k8s-api.spaceships.work           # Kubernetes API VIP
vip-02-haproxy.spaceships.work           # HAProxy VIP
vip-03-postgres.spaceships.work          # PostgreSQL VIP
```

### Service Endpoints

```text
service-01-api.spaceships.work           # API endpoint
service-02-web.spaceships.work           # Web frontend
service-03-cdn.spaceships.work           # CDN endpoint
```

## Rules and Best Practices

### Mandatory Rules

1. **Always lowercase** - No uppercase letters
2. **Hyphens only** - No underscores or other special characters
3. **Two-digit numbers** - Use 01, 02, not 1, 2
4. **Descriptive purpose** - Purpose should clearly indicate function
5. **Valid DNS characters** - Only `a-z`, `0-9`, `-`, `.`

### Recommended Practices

1. **Consistent service names** - Stick to established service types
2. **Logical numbering** - Start at 01, increment sequentially
3. **Purpose specificity** - Be specific but concise (nexus, not nexus-container-registry)
4. **Avoid ambiguity** - Don't use `test-01-prod` or similar confusing names
5. **Document exceptions** - If you must break a rule, document why

## Validation

### Python Validation Script

```python
#!/usr/bin/env python3
# /// script
# dependencies = []
# ///

import re
import sys

PATTERN = r'^[a-z0-9-]+-\d{2}-[a-z0-9-]+\.[a-z0-9.-]+$'

def validate_dns_name(name: str) -> tuple[bool, str]:
    """Validate DNS name against convention."""
    if not re.match(PATTERN, name):
        return False, "Name doesn't match pattern: <service>-<NN>-<purpose>.<domain>"

    parts = name.split('.')
    if len(parts) < 2:
        return False, "Must include domain"

    hostname = parts[0]
    components = hostname.split('-')

    if len(components) < 3:
        return False, "Hostname must have at least 3 components: <service>-<NN>-<purpose>"

    # Check number component (should be 2 digits)
    number_component = components[1]
    if not number_component.isdigit() or len(number_component) != 2:
        return False, f"Number component '{number_component}' must be exactly 2 digits (01-99)"

    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_dns_naming.py <dns-name>")
        sys.exit(1)

    name = sys.argv[1]
    valid, message = validate_dns_name(name)

    if valid:
        print(f"✓ {name}: {message}")
        sys.exit(0)
    else:
        print(f"✗ {name}: {message}", file=sys.stderr)
        sys.exit(1)
```

**Usage:**

```bash
./tools/validate_dns_naming.py docker-01-nexus.spaceships.work
# ✓ docker-01-nexus.spaceships.work: Valid

./tools/validate_dns_naming.py Docker-1-Nexus.spaceships.work
# ✗ Docker-1-Nexus.spaceships.work: Name doesn't match pattern
```

## NetBox Integration

### Setting DNS Names in NetBox

**Via Web UI:**

IP Addresses → Add → DNS Name field: `docker-01-nexus.spaceships.work`

**Via Terraform:**

```hcl
resource "netbox_ip_address" "docker_nexus" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "docker-01-nexus.spaceships.work"
  description = "Docker host for Nexus container registry"

  tags = ["terraform", "production-dns"]
}
```

**Via Ansible:**

```yaml
- name: Create IP address in NetBox
  netbox.netbox.netbox_ip_address:
    netbox_url: "{{ netbox_url }}"
    netbox_token: "{{ netbox_token }}"
    data:
      address: "192.168.1.100/24"
      dns_name: "docker-01-nexus.spaceships.work"
      tags:
        - name: production-dns
```

### Tagging for Auto-DNS

Tag IP addresses to trigger automatic DNS record creation:

**Production DNS:**

```text
Tag: production-dns
Zone: spaceships.work
```

**Development DNS:**

```text
Tag: dev-dns
Zone: dev.spaceships.work
```

**Lab/Testing DNS:**

```text
Tag: lab-dns
Zone: lab.spaceships.work
```

## PowerDNS Record Generation

### Automatic Record Creation

When an IP address with correct tags is created in NetBox:

```text
IP: 192.168.1.100/24
DNS Name: docker-01-nexus.spaceships.work
Tag: production-dns

→ A record created: docker-01-nexus.spaceships.work → 192.168.1.100
→ PTR record created: 100.1.168.192.in-addr.arpa → docker-01-nexus.spaceships.work
```

### Sync Verification

```bash
# Verify DNS record exists
dig @192.168.3.1 docker-01-nexus.spaceships.work +short
# Should return: 192.168.1.100

# Verify PTR record
dig @192.168.3.1 -x 192.168.1.100 +short
# Should return: docker-01-nexus.spaceships.work
```

## Common Mistakes

### Wrong Number Format

```text
❌ docker-1-nexus.spaceships.work         # Single digit
✓  docker-01-nexus.spaceships.work        # Two digits

❌ docker-001-nexus.spaceships.work       # Three digits
✓  docker-01-nexus.spaceships.work        # Two digits
```

### Wrong Separators

```text
❌ docker_01_nexus.spaceships.work        # Underscores
✓  docker-01-nexus.spaceships.work        # Hyphens

❌ docker.01.nexus.spaceships.work        # Dots in hostname
✓  docker-01-nexus.spaceships.work        # Hyphens only
```

### Wrong Case

```text
❌ Docker-01-Nexus.spaceships.work        # Mixed case
✓  docker-01-nexus.spaceships.work        # Lowercase only

❌ DOCKER-01-NEXUS.SPACESHIPS.WORK        # Uppercase
✓  docker-01-nexus.spaceships.work        # Lowercase only
```

### Missing Components

```text
❌ docker-nexus.spaceships.work           # Missing number
✓  docker-01-nexus.spaceships.work        # Complete

❌ 01-nexus.spaceships.work               # Missing service
✓  docker-01-nexus.spaceships.work        # Complete

❌ docker-01.spaceships.work              # Missing purpose
✓  docker-01-nexus.spaceships.work        # Complete
```

## Migration Strategy

### From Legacy Names

If you have existing DNS names that don't follow the convention:

1. **Document current names** - Create inventory of legacy names
2. **Create new names** - Following convention
3. **Create CNAME records** - Point legacy names to new names
4. **Update configs gradually** - Migrate services to use new names
5. **Monitor usage** - Track legacy CNAME usage
6. **Deprecate legacy names** - Remove after migration complete

**Example migration:**

```text
Legacy:  nexus.spaceships.work
New:     docker-01-nexus.spaceships.work
CNAME:   nexus.spaceships.work → docker-01-nexus.spaceships.work

After 6 months: Remove CNAME, update all references to use new name
```

## Environment-Specific Domains

### Production

```text
Domain: spaceships.work
Example: docker-01-nexus.spaceships.work
```

### Development

```text
Domain: dev.spaceships.work
Example: docker-01-nexus.dev.spaceships.work
```

### Lab/Testing

```text
Domain: lab.spaceships.work
Example: docker-01-nexus.lab.spaceships.work
```

## Documentation

### In NetBox

Use the **Description** field to document:

- Primary purpose
- Hosted applications
- Related services
- Contact owner

**Example:**

```text
IP: 192.168.1.100/24
DNS Name: docker-01-nexus.spaceships.work
Description: Docker host for Nexus container registry.
             Serves Docker and Maven artifacts.
             Owner: Platform Team
             Related: docker-02-gitlab.spaceships.work
```

### In Infrastructure Code

**Terraform example:**

```hcl
resource "netbox_ip_address" "docker_nexus" {
  ip_address  = "192.168.1.100/24"
  dns_name    = "docker-01-nexus.spaceships.work"
  description = "Docker host for Nexus container registry"

  tags = ["terraform", "production-dns", "docker-host", "nexus"]
}
```

## Further Reading

- [RFC 1035 - Domain Names](https://www.rfc-editor.org/rfc/rfc1035)
- [DNS Best Practices](https://www.ietf.org/rfc/rfc1912.txt)
