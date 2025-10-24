# Common Mistakes and Anti-Patterns

DNS naming convention violations and NetBox/PowerDNS integration pitfalls based on the `spaceships.work` infrastructure.

## DNS Naming Convention Violations

### Infrastructure Overview

**Root Domain**: `spaceships.work`

**Cluster Domains**:
- `matrix.spaceships.work` - Nexus cluster (3 nodes)
- `quantum.spaceships.work` - Quantum cluster (3 nodes)
- `nexus.spaceships.work` - (Legacy naming reference)

**Proxmox Node Domains** (with master node designations):

**Matrix Cluster** (nexus.spaceships.work):
- `foxtrot.nexus.spaceships.work` - **Master Node** (API Target)
- `golf.nexus.spaceships.work`
- `hotel.nexus.spaceships.work`

**Quantum Cluster** (quantum.spaceships.work):
- `charlie.quantum.spaceships.work`
- `delta.quantum.spaceships.work` - **Master Node** (API Target)
- `echo.quantum.spaceships.work`

**Matrix Cluster** (matrix.spaceships.work):
- `alpha.matrix.spaceships.work`
- `bravo.matrix.spaceships.work` - **Master Node** (API Target)
- `charlie.matrix.spaceships.work`

---

## ❌ Wrong Root Domain

**Problem**: Using incorrect root domain in DNS records.

```python
# BAD - Wrong domain
hostname = "docker-01-nexus.internal.lan"
hostname = "k8s-master.homelab.local"
```

**Solution**: Always use `spaceships.work` as root domain.

```python
# GOOD
hostname = "docker-01-nexus.spaceships.work"
hostname = "k8s-01-master.matrix.spaceships.work"
```

---

## ❌ Wrong Cluster Subdomain

**Problem**: Using non-existent cluster domains.

```python
# BAD - Invalid cluster domains
hostname = "docker-01.homelab.spaceships.work"  # No 'homelab' cluster
hostname = "vm-01.lab.spaceships.work"          # No 'lab' cluster
hostname = "test.prod.spaceships.work"          # No 'prod' cluster
```

**Solution**: Use only valid cluster domains.

```python
# GOOD - Valid cluster domains
hostname = "docker-01-nexus.matrix.spaceships.work"
hostname = "k8s-01-worker.quantum.spaceships.work"
hostname = "storage-01-ceph.nexus.spaceships.work"
```

**Valid Clusters**:
- `matrix.spaceships.work`
- `quantum.spaceships.work`
- `nexus.spaceships.work`

---

## ❌ Wrong Node Domain

**Problem**: Using incorrect Proxmox node FQDNs.

```python
# BAD - Incorrect node names
proxmox_host = "node1.spaceships.work"          # Not the naming pattern
proxmox_host = "foxtrot.spaceships.work"        # Missing cluster subdomain
proxmox_host = "foxtrot.matrix.spaceships.org"  # Wrong TLD
```

**Solution**: Use correct node FQDN pattern.

```python
# GOOD - Correct node FQDNs
proxmox_host = "foxtrot.nexus.spaceships.work"    # Nexus cluster master
proxmox_host = "delta.quantum.spaceships.work"    # Quantum cluster master
proxmox_host = "bravo.matrix.spaceships.work"     # Matrix cluster master
```

---

## ❌ Targeting Non-Master Nodes

**Problem**: Sending API calls to non-master nodes in cluster.

```python
# BAD - Not a master node
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(
    'golf.nexus.spaceships.work',  # ❌ Not the master!
    user='root@pam',
    password='...'
)
```

**Solution**: Always target the designated master node for API operations.

```python
# GOOD - Target master nodes
from proxmoxer import ProxmoxAPI

# Nexus cluster
proxmox_nexus = ProxmoxAPI(
    'foxtrot.nexus.spaceships.work',  # ✅ Master node
    user='root@pam',
    password='...'
)

# Quantum cluster
proxmox_quantum = ProxmoxAPI(
    'delta.quantum.spaceships.work',  # ✅ Master node
    user='root@pam',
    password='...'
)

# Matrix cluster
proxmox_matrix = ProxmoxAPI(
    'bravo.matrix.spaceships.work',  # ✅ Master node
    user='root@pam',
    password='...'
)
```

**Master Nodes Quick Reference**:
- **Nexus**: `foxtrot.nexus.spaceships.work`
- **Quantum**: `delta.quantum.spaceships.work`
- **Matrix**: `bravo.matrix.spaceships.work`

---

## ❌ Violating Service-Number-Purpose Pattern

**Problem**: Not following the `service-NN-purpose` naming convention.

```python
# BAD - Violates naming pattern
hostname = "nexus.spaceships.work"              # Missing service number
hostname = "docker-nexus.spaceships.work"       # Missing number
hostname = "docker1-nexus.spaceships.work"      # Wrong number format (1 vs 01)
hostname = "nexus-docker-01.spaceships.work"    # Wrong order
```

**Solution**: Follow `service-NN-purpose.domain` pattern.

```python
# GOOD - Correct naming pattern
hostname = "docker-01-nexus.spaceships.work"      # ✅ service-01-purpose
hostname = "k8s-02-worker.matrix.spaceships.work" # ✅ service-02-purpose
hostname = "storage-03-ceph.nexus.spaceships.work"# ✅ service-03-purpose
```

**Pattern**: `<service>-<NN>-<purpose>.<cluster>.<root-domain>`

Components:
- **service**: Infrastructure type (`docker`, `k8s`, `proxmox`, `storage`, `db`)
- **NN**: Two-digit number (`01`, `02`, `03`, ... `99`)
- **purpose**: Specific role (`nexus`, `master`, `worker`, `ceph`, `postgres`)
- **cluster**: Cluster subdomain (`matrix`, `quantum`, `nexus`)
- **root-domain**: `spaceships.work`

---

## ❌ Improper Case in Hostnames

**Problem**: Using uppercase letters in DNS names.

```python
# BAD - Uppercase not allowed
hostname = "Docker-01-Nexus.spaceships.work"
hostname = "K8S-01-MASTER.matrix.spaceships.work"
```

**Solution**: Always use lowercase.

```python
# GOOD
hostname = "docker-01-nexus.spaceships.work"
hostname = "k8s-01-master.matrix.spaceships.work"
```

---

## NetBox Integration Issues

### ❌ Not Setting DNS Name in NetBox

**Problem**: Creating IP address in NetBox without `dns_name` field.

```python
# BAD - Missing DNS name
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.100/24",
    description="Docker host",
    # Missing dns_name!
)
```

**Solution**: Always set `dns_name` when creating IPs.

```python
# GOOD
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.100/24",
    dns_name="docker-01-nexus.matrix.spaceships.work",  # ✅
    description="Docker host for Nexus registry",
    tags=["production-dns"]  # Triggers PowerDNS sync
)
```

---

### ❌ Missing PowerDNS Sync Tags

**Problem**: DNS record not created automatically because missing trigger tag.

```python
# BAD - No sync tag
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.100/24",
    dns_name="docker-01-nexus.matrix.spaceships.work",
    tags=["docker", "production"]  # Missing 'production-dns' tag!
)
# PowerDNS record NOT created automatically
```

**Solution**: Include appropriate sync tag.

```python
# GOOD
ip = nb.ipam.ip_addresses.create(
    address="192.168.3.100/24",
    dns_name="docker-01-nexus.matrix.spaceships.work",
    tags=[
        "docker",
        "production",
        "production-dns"  # ✅ Triggers PowerDNS sync
    ]
)
```

**Sync Tags**:
- `production-dns` - Auto-create in PowerDNS production zone
- `lab-dns` - Auto-create in PowerDNS lab zone

---

### ❌ Inconsistent DNS Naming Between Tools

**Problem**: Different naming in OpenTofu vs NetBox vs Proxmox.

**Note**: Use `tofu` CLI (not `terraform`).

```hcl
# OpenTofu
resource "proxmox_virtual_environment_vm" "docker_host" {
  name = "docker-nexus-01"  # ❌ Wrong order
}

# NetBox
dns_name = "nexus-docker-01.spaceships.work"  # ❌ Different order

# Proxmox
hostname = "docker01-nexus"  # ❌ Missing hyphen
```

**Solution**: Consistent naming everywhere.

```hcl
# OpenTofu
resource "proxmox_virtual_environment_vm" "docker_host" {
  name = "docker-01-nexus"  # ✅ Consistent
}
```

```python
# NetBox
dns_name = "docker-01-nexus.matrix.spaceships.work"  # ✅ Consistent
```

```yaml
# Proxmox (via OpenTofu)
initialization {
  user_data_file_id = "local:snippets/user-data.yaml"
  # Inside user-data.yaml:
  # hostname: docker-01-nexus  # ✅ Consistent
  # fqdn: docker-01-nexus.matrix.spaceships.work
}
```

---

## Validation Tools

### Check DNS Naming Convention

```bash
# Validate hostname format
./tools/validate_dns_naming.py --name "docker-01-nexus.matrix.spaceships.work"
# ✅ Valid

./tools/validate_dns_naming.py --name "docker-nexus.spaceships.work"
# ❌ Invalid: Missing number in service-NN-purpose pattern
```

### Check NetBox DNS Records

```bash
# Query NetBox for DNS records
./tools/netbox_api_client.py ips query --dns-name docker-01

# Verify PowerDNS sync
./tools/powerdns_sync_check.py --zone spaceships.work --verbose
```

---

## Quick Reference

### Correct Naming Patterns

**VM Hostnames**:
```
docker-01-nexus.matrix.spaceships.work
k8s-01-master.quantum.spaceships.work
storage-01-ceph.nexus.spaceships.work
db-01-postgres.matrix.spaceships.work
```

**Proxmox Nodes**:
```
foxtrot.nexus.spaceships.work (master)
delta.quantum.spaceships.work (master)
bravo.matrix.spaceships.work (master)
```

**Service Types**:
- `docker-NN-<app>` - Docker hosts
- `k8s-NN-<role>` - Kubernetes nodes (master, worker)
- `proxmox-<node>-<iface>` - Proxmox infrastructure
- `storage-NN-<type>` - Storage systems (ceph, nas)
- `db-NN-<dbtype>` - Database servers (postgres, mysql)

### Valid Domains

**Clusters**:
- `matrix.spaceships.work`
- `quantum.spaceships.work`
- `nexus.spaceships.work`

**Master Nodes** (API targets):
- Nexus: `foxtrot.nexus.spaceships.work`
- Quantum: `delta.quantum.spaceships.work`
- Matrix: `bravo.matrix.spaceships.work`

---

## Troubleshooting

### DNS Record Not Created in PowerDNS

**Check**:
1. ✅ DNS name follows pattern? `service-NN-purpose.cluster.spaceships.work`
2. ✅ Has `production-dns` or `lab-dns` tag in NetBox?
3. ✅ NetBox PowerDNS sync plugin enabled?
4. ✅ Zone exists in NetBox and matches domain?

### Can't Connect to Proxmox API

**Check**:
1. ✅ Using master node FQDN?
   - Nexus: `foxtrot.nexus.spaceships.work`
   - Quantum: `delta.quantum.spaceships.work`
   - Matrix: `bravo.matrix.spaceships.work`
2. ✅ DNS resolves correctly? `dig <master-node-fqdn>`
3. ✅ Cluster subdomain included? (not just `<node>.spaceships.work`)

### Validation Script Fails

**Common Issues**:
```bash
# Missing number
❌ docker-nexus.spaceships.work
✅ docker-01-nexus.matrix.spaceships.work

# Wrong number format
❌ docker-1-nexus.spaceships.work
✅ docker-01-nexus.matrix.spaceships.work

# Missing cluster subdomain
❌ docker-01-nexus.spaceships.work
✅ docker-01-nexus.matrix.spaceships.work

# Wrong domain
❌ docker-01-nexus.local
✅ docker-01-nexus.matrix.spaceships.work
```

Run validation:
```bash
./tools/validate_dns_naming.py --name "your-hostname-here"
```
