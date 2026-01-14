# lunar-claude

Personal Claude Code plugin marketplace for homelab and infrastructure automation.

## Installation

```bash
/plugin marketplace add basher83/lunar-claude
/plugin install <plugin-name>@lunar-claude
```

## Plugins

### meta

| Plugin | Description |
|--------|-------------|
| [meta-claude](plugins/meta/meta-claude/) | Skill creation and multi-agent composition patterns |
| [plugin-dev](plugins/meta/plugin-dev/) | Plugin development toolkit (skills, agents, commands, hooks) |
| [hookify](plugins/meta/hookify/) | Conversation pattern hooks for behavior control |
| [claude-dev-sandbox](plugins/meta/claude-dev-sandbox/) | Development sandbox for testing components |

### infrastructure

| Plugin | Description |
|--------|-------------|
| [ansible-workflows](plugins/infrastructure/ansible-workflows/) | End-to-end Ansible automation with multi-agent pipelines |
| [proxmox-infrastructure](plugins/infrastructure/proxmox-infrastructure/) | Proxmox VE cluster management, CEPH, VLAN networking |

### devops

| Plugin | Description |
|--------|-------------|
| [python-tools](plugins/devops/python-tools/) | Python toolkit: uv scripts, ruff/pyright, Agent SDK |
| [git-workflow](plugins/devops/git-workflow/) | Atomic commits, branch cleanup, conventional commits |

### homelab

| Plugin | Description |
|--------|-------------|
| [netbox-powerdns-integration](plugins/homelab/netbox-powerdns-integration/) | NetBox IPAM and PowerDNS automation |
| [omni-scale](plugins/homelab/omni-scale/) | Sidero Omni + Talos Kubernetes on Proxmox |

### research

| Plugin | Description |
|--------|-------------|
| [lunar-research](https://github.com/basher83/lunar-research) | Multi-agent research pipeline (external repo) |

## Development

Structure validation:

```bash
uv run scripts/verify-structure.py
```

Local testing:

```bash
/plugin marketplace add /path/to/lunar-claude
/plugin install plugin-name@lunar-claude
```

See individual plugin READMEs for details.
