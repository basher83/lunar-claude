# CEL Storage Selectors Reference

The Proxmox infrastructure provider uses CEL (Common Expression Language) to dynamically select storage pools for VM disk placement.

## Syntax

Storage selectors are simple CEL expressions that evaluate against each available storage pool:

```text
<condition>
```

The expression filters available storage pools and selects one that matches.

## Available Fields

Use these fields in selector conditions:

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `name` | string | Storage pool name | `"local-lvm"`, `"vm_ssd"`, `"local"` |

> **Warning:** The `type` field (for storage backend type like "rbd", "lvmthin") is **not currently usable** because `type` is a reserved keyword in CEL. Use `name` for storage selection until this is resolved. See [debugging](debugging.md#cel-type-keyword-error).

## Common Patterns

### Select by Name

Exact match on storage pool name:

```text
name == "vm_ssd"
```

```text
name == "local-lvm"
```

```text
name == "local"
```

## CEL Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equals | `name == "local-lvm"` |
| `!=` | Not equals | `name != "local"` |

## Debugging

### List Available Storage

Check what storage pools exist on Proxmox:

```bash
# On Proxmox node (Foxtrot)
pvesh get /storage

# Or via API
curl -k https://192.168.3.5:8006/api2/json/storage \
  -H "Authorization: PVEAPIToken=terraform@pam!automation=<secret>"
```

### Test Selector Logic

If a selector returns empty, verify:

1. Storage pool exists with expected name
2. Storage type matches (lvmthin vs lvm vs zfspool)
3. No typos in storage name

### Common Issues

**Empty result:**

The selector matched no storage pools. Check storage pool name spelling.

**Wrong storage selected:**

Multiple pools matched the filter. Use exact name match.

**CEL type keyword error:**

If using `type == "..."`, you'll get a type mismatch. `type` is a reserved CEL keyword. Use `name` field only.

## Examples in MachineClass

**CEPH RBD storage (Matrix cluster):**

```yaml
providerdata: |
  storage_selector: name == "vm_ssd"
```

**Local LVM-thin storage:**

```yaml
providerdata: |
  storage_selector: name == "local-lvm"
```

**ZFS pool by name:**

```yaml
providerdata: |
  storage_selector: name == "tank"
```
