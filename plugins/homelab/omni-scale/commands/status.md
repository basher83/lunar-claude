---
description: Check Omni cluster and GitOps health status
allowed-tools: Bash(omnictl:*), mcp__plugin_omni-scale_kubernetes__*
---

# Cluster Status

Quick health check for Omni-managed Talos cluster and GitOps stack.

## Required Data

### Omni Cluster

- Cluster phase (Running/Provisioning/etc)
- Node count (control plane vs workers)
- Overall health status

### Kubernetes Nodes

- Ready status for each node
- Role (control-plane vs worker)
- Kubernetes version
- Talos version
- Node IPs

### ArgoCD Applications

- Sync status: Synced, OutOfSync, Unknown
- Health status: Healthy, Progressing, Degraded, Suspended, Missing, Unknown
- **List any apps NOT Synced+Healthy**

### External Secrets

- ClusterSecretStore count and health
- ExternalSecret count, sync status
- **List any secrets failing to sync**

### Storage (Longhorn)

- State: attached, detached, attaching, detaching
- Robustness: healthy, degraded, faulted, unknown
- **List any volumes not attached+healthy**

## Output Format

```text
## Omni-Scale Status Report

### Omni Cluster: talos-prod-01
- Phase: [status]
- Nodes: [X] control plane, [Y] workers
- Health: [status]

### Kubernetes
- Nodes Ready: [X/Y]
- Version: [version]
- Talos: [version]

[Node table with roles and IPs]

### ArgoCD Applications
- Total: [N]
- Synced: [N], OutOfSync: [N]
- Healthy: [N], Degraded: [N]

[Table showing any non-healthy/non-synced apps]

### External Secrets
- ClusterSecretStores: [N] healthy
- ExternalSecrets: [N] synced, [N] failed

[List any failing secrets]

### Storage (Longhorn)
- Volumes: [N]
- Healthy: [N]
- Degraded: [N]

[List any unhealthy volumes]

### Issues Found
[List problems or "None"]
```
