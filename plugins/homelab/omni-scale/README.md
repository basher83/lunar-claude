# omni-scale

Sidero Omni + Talos Kubernetes infrastructure management on Proxmox with GitOps deployment patterns.

## Overview

This plugin provides Claude with knowledge and tooling for managing:

- **Omni-Scale repo** - Talos cluster provisioning via Sidero Omni on Proxmox
- **mothership-gitops repo** - ArgoCD-based workload deployment

## Components

### Skills

- **omni-proxmox** - Sidero Omni architecture, machine classes, cluster templates, provider config, troubleshooting

### Commands

| Command | Description |
|---------|-------------|
| `/omni-scale:omni-prime` | Load infrastructure context (kernel, codebase structure) |
| `/omni-scale:status` | Check cluster and GitOps health |
| `/omni-scale:analyze-spec` | Analyze spec file and generate deployment plan |
| `/omni-scale:bootstrap-gitops` | Bootstrap GitOps stack onto existing Talos cluster |
| `/omni-scale:disaster-recovery` | Execute DR drill (destroy/recreate cluster) |

### Scripts

| Script | Location | Description |
|--------|----------|-------------|
| `provider-ctl.py` | `skills/omni-proxmox/scripts/` | Manage Omni Proxmox Provider container via SSH |

**provider-ctl.py usage:**

```bash
# Restart provider container (idempotent, 30s timeout)
./skills/omni-proxmox/scripts/provider-ctl.py --restart

# Show last 25 log lines (filtered, human-readable)
./skills/omni-proxmox/scripts/provider-ctl.py --logs

# Show last N log lines
./skills/omni-proxmox/scripts/provider-ctl.py --logs 50

# Raw JSON output (unfiltered)
./skills/omni-proxmox/scripts/provider-ctl.py --logs 10 --raw
```

### Agents

| Agent | Scope | Purpose |
|-------|-------|---------|
| omni-reviewer | Omni-Scale repo | Validate machine classes, cluster templates, provider configs |
| gitops-reviewer | mothership-gitops | Validate ArgoCD apps, Helm values, Tailscale Ingress |

### MCP Servers

- **kubernetes** - mcp-server-kubernetes for kubectl operations

## Prerequisites

- `omnictl` CLI installed and authenticated
- `kubectl` configured for talos-prod-01
- Access to Omni console: [https://omni.spaceships.work](https://omni.spaceships.work)

## Architecture

```text
Omni-Scale (how cluster exists)     mothership-gitops (what runs on cluster)
├── machine-classes/                ├── apps/
├── clusters/                       │   ├── argocd/
├── proxmox-provider/               │   ├── external-secrets/
└── specs/                          │   ├── longhorn/
                                    │   └── ...
        ↓                                   ↓
   omni-reviewer                      gitops-reviewer
```

## Usage

### Check cluster health

```text
/omni-scale:status
```

### Review infrastructure changes

```text
"Review my machine class changes before I commit"
→ Triggers omni-reviewer agent
```

### Review GitOps changes

```text
"Check my ArgoCD app before deploying"
→ Triggers gitops-reviewer agent
```

### DR drill

```text
/omni-scale:disaster-recovery
```

## Key Constraints

These are encoded in the reviewer agents:

| Constraint | Impact |
|------------|--------|
| CEL `type` keyword | Cannot use in storage selectors |
| Provider hostname bug | Must use `:local-fix` image tag |
| VM migration | Breaks Talos state, don't migrate |
| Web UI exposure | ALL UIs must have Tailscale Ingress |
| ESO drift | Use ignoreDifferences for ESO resources |
