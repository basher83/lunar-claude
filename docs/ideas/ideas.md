# Ideas

## Plugins

### meta-claude

A plugin for Claude to help with meta tasks.

- Skills creator skill that expands upon <https://github.com/anthropics/skills/tree/main/skill-creator>. The Anthropic skill creator is a great starting point, but it could be improved with referances from offical docs.
- Agent creator
- Hooks creator
- Slash commands creator

## Agents

- AI docs updater agent that updates the AI docs with the latest information from offical sources. [Example](examples/agents/fetch-docs.md)
- Documentation maintanence agent that Validates and fixes markdown syntax, link rot, and outdated information in the documentation. [Example](examples/agents/docs-maint-agent.md)

## Hooks

- Claude Code Hook: Bash Command Validator. [Example](examples/hooks/bash_cmd_validator/hook.json) This hook runs as a PreToolUse hook for the Bash tool. It validates bash commands against a set of rules before execution. In this case it changes grep calls to using rg.
- Claude Code Hook: Lint on Save. [Example](examples/hooks/lint-on-save/lint-on-save.json) This hook runs as a PostToolUse hook for the Edit and MultiEdit tools. It runs the Ruff linter on Python files after they are edited.

## Slash commands

## Skills

## Topics

- Ansible
- Terraform
  - Scalr
- Docker
- Kubernetes
- Proxmox
- PowerDNS
- Netbox
- Homelab
- Devtools expertise
  - git-cliff (<https://git-cliff.org/docs/>)
  - infisical (<https://infisical.com/docs/>)
  - mise (<https://mise.readthedocs.io/en/latest/>)

## Use Cases

- Deploy a 3 node microk8s cluster via Opentofu to a Proxmox cluster.
  - Knowledge Requirements:
    - Cluster Proxmox nodes
    - OpenTofu configuration, settings, nuances (i.e. tofu does not yet support emphemeral resources while terraform does)
    - Ansible devops knowledge
    - Infisical secrets management integration for ansible, terraform, tofu, python sdk, cli
    - Microk8s cluster configuration, settings, nuances
    - HA considerations for networking, storage, and other resources
    - DNS management for the cluster
    - Network management for the cluster (IPAM, routing, etc.)
