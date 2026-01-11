---
description: Check Omni cluster and GitOps health status
allowed-tools: Bash(omnictl:*), mcp__kubernetes__*
---

# Cluster Status

Quick health check for Omni-managed Talos cluster and GitOps stack.

## Instructions

Run these checks in sequence and report results:

### 1. Omni Cluster Status

```bash
omnictl cluster status talos-prod-01
```

Report: Cluster phase, node count, health status.

### 2. Node Health

```bash
omnictl get machines --cluster talos-prod-01
```

Report: Machine count, states (running/provisioning/failed).

### 3. Kubernetes Nodes

```text
mcp__kubernetes__kubectl_get(resourceType: "nodes")
```

Report: Node Ready status, roles, versions.

### 4. ArgoCD Application Health

```text
mcp__kubernetes__kubectl_get(resourceType: "applications", namespace: "argocd")
```

Report: Any apps not Synced/Healthy.

### 5. External Secrets

```text
mcp__kubernetes__kubectl_get(resourceType: "externalsecrets", allNamespaces: true)
mcp__kubernetes__kubectl_get(resourceType: "clustersecretstore")
```

Report: SecretStore health, any secrets not syncing.

### 6. Longhorn Status

```text
mcp__kubernetes__kubectl_get(resourceType: "volumes.longhorn.io", allNamespaces: true)
```

Report: Volume health and robustness.

## Output Format

```text
## Omni-Scale Status Report

### Omni Cluster: talos-prod-01
- Phase: [Running/Provisioning/etc]
- Nodes: [X] control plane, [Y] workers
- Health: [Healthy/Degraded/etc]

### Kubernetes
- Nodes Ready: [X/Y]
- Version: [version]

### ArgoCD Applications
- Total: [N]
- Healthy: [N]
- Degraded: [list if any]

### External Secrets
- ClusterSecretStores: [N] healthy
- ExternalSecrets: [N] synced, [N] failed
- Issues: [list if any]

### Storage (Longhorn)
- Volumes: [N]
- Healthy: [N]
- Degraded: [list if any]

### Issues Found
[List any problems or "None"]
```
