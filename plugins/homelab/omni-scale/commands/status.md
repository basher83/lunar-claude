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

- Total application count
- Sync status breakdown (Synced vs OutOfSync)
- Health status breakdown (Healthy vs Degraded)
- **List any apps NOT both Synced AND Healthy**

### External Secrets

- ClusterSecretStore count and health
- ExternalSecret count, sync status
- **List any secrets failing to sync**

### Storage (Longhorn)

- Volume count
- Volume state (attached/detached)
- Robustness status
- **List any volumes not healthy**

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
