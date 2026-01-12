---
allowed-tools: Bash, Read
description: Load context for a new agent session by analyzing codebase structure and README
---

# Prime

This command loads essential context for a new agent session.

## Instructions

- Run `git ls-files` to understand the codebase structure and file organization
- Read the README.md to understand the project purpose, setup instructions, and key information
- Provide a concise overview of the project based on the gathered context

## Context

- Codebase structure git accessible: !`git ls-files`
- Codebase structure all: !`eza . --tree`
- Project README: @${CLAUDE_PROJECT_DIR}/README.md
- Kernel context: @${CLAUDE_PLUGIN_ROOT}/references/kernel.md

## Tool Usage Patterns

### MCP Kubernetes Tools

Use `mcp__plugin_omni-scale_kubernetes__*` for cluster operations.

**Validation checks — gather this data:**

- **ArgoCD:** Sync status + health status (per app). Flag any NOT Synced+Healthy.
- **External Secrets:** ClusterSecretStore health, ExternalSecret sync status. Flag failures.
- **Longhorn:** Volume state (attached/detached) + robustness (healthy/degraded). Flag unhealthy.

Use MCP first. Fall back to kubectl CLI only if MCP output lacks required fields.

### Helm via MCP

Limited to: install, upgrade, uninstall. ArgoCD handles Helm for this stack — MCP Helm rarely needed.

## Cross-Repo Gotchas

| Issue | Cause | Resolution |
|-------|-------|------------|
| ArgoCD drift on ESO resources | ESO adds default fields | Add `ignoreDifferences` in Application |
| Pods Pending (privileged workload) | Missing PSA label | `pod-security.kubernetes.io/enforce: privileged` |
| `mcp__plugin_omni-scale_kubernetes__kubectl_get` lacks CRD status | Basic output, not CRD fields | Use `mcp__plugin_omni-scale_kubernetes__kubectl_generic` with jsonpath or CLI fallback |
