---
description: Check Omni cluster and GitOps health status
allowed-tools: Bash, mcp__kubernetes__*
argument-hint: "(no arguments)"
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

Use the kubernetes MCP server or:

```bash
kubectl get nodes -o wide
```

Report: Node Ready status, roles, versions.

### 4. ArgoCD Application Health

```bash
kubectl get applications -n argocd -o custom-columns='NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status'
```

Report: Any apps not Synced/Healthy.

### 5. Longhorn Status

```bash
kubectl get volumes.longhorn.io -A -o custom-columns='NAME:.metadata.name,STATE:.status.state,ROBUSTNESS:.status.robustness'
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

### Storage (Longhorn)
- Volumes: [N]
- Healthy: [N]
- Degraded: [list if any]

### Issues Found
[List any problems or "None"]
```

## Tips

If omnictl auth fails, re-authenticate:

```bash
omnictl --omni-url https://omni.spaceships.work get clusters
```

This triggers browser-based OIDC flow with Auth0.
