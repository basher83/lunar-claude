# Specs

Declarative infrastructure specifications defining desired state.

## Philosophy

Specs are the **source of truth** for what should exist. They capture:

- Target architecture and configuration
- Constraints and locked decisions
- Dependencies between components
- Optionally, current deployment status

Specs do NOT contain implementation details (that's what `terraform/`, `ansible/`, etc. are for).

## Schema

```yaml
apiVersion: homelab/v1
kind: <ComponentType>
metadata:
  name: <unique-identifier>
  description: <human-readable description>

spec:
  # Component-specific configuration
  # This varies by kind

dependencies:
  # Optional: explicit dependencies
  - name: <other-component>
    type: <hard|soft>  # hard = blocker, soft = preferred order

decisions:
  # Locked decisions that are non-negotiable
  - key: <decision-name>
    value: <decision-value>
    rationale: <why this decision was made>

status:
  # Optional: track deployment state in spec
  phase: Planning | Implementing | Deployed | Deprecated
  lastUpdated: <ISO-8601 date>
  blockedBy: <optional: what's blocking progress>
  notes: <optional: current state notes>
```

## Component Types (kind)

| Kind | Description |
|------|-------------|
| `Platform` | Top-level platform (e.g., Omni, Kubernetes distribution) |
| `Cluster` | Kubernetes cluster definition |
| `Node` | Individual node (VM, LXC, bare metal) |
| `Provider` | Infrastructure provider (Proxmox provider, cloud provider) |
| `Network` | Network configuration (VLANs, routes, DNS) |
| `Storage` | Storage configuration (CEPH, NFS, local) |
| `Service` | Deployed service/application |

## Example: Omni Platform Spec

See `omni.yaml` for the full production spec. Abbreviated example:

```yaml
apiVersion: homelab/v1
kind: Platform
metadata:
  name: omni
  description: Sidero Omni Kubernetes management platform

spec:
  hub:
    host: holly
    cluster: quantum
    ip: 192.168.10.20
    access:
      tailscale: omni.spaceships.work
      lan: 192.168.10.20 (split-horizon DNS)

  provider:
    name: omni-provider
    type: lxc
    host: foxtrot
    cluster: matrix
    ip: 192.168.3.10/24

decisions:
  - key: provider-location
    value: foxtrot (Matrix cluster)
    rationale: Provider must be L2-adjacent to booting VMs for SideroLink registration
  - key: auth-provider
    value: Auth0
    rationale: Simpler than self-hosted tsidp, managed service reliability

status:
  phase: Deployed
  lastUpdated: 2026-01-03
  notes: Infrastructure FMC. Production cluster ready to deploy.
```

## Usage

Analyze a spec and generate deployment plan:

```bash
claude
> /analyze-spec specs/omni.yaml
```

## Files

| File | Description | Status |
|------|-------------|--------|
| `omni.yaml` | Omni platform deployment | Infrastructure Operational |
