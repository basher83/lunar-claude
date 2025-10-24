# lunar-claude

Personal Claude Code plugin marketplace for homelab and infrastructure automation.

## Structure

This marketplace organizes plugins into four categories:

- **meta** - Tools for creating Claude Code components
- **infrastructure** - Infrastructure as Code tools (Terraform, Ansible, Proxmox)
- **devops** - Container orchestration and DevOps tools (Kubernetes, Docker)
- **homelab** - Homelab-specific utilities (Netbox, PowerDNS)

## Installation

Add this marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

## Available Plugins

### meta-claude

Meta tools for creating skills, agents, hooks, and commands.

**Install:**

```bash
/plugin install meta-claude@lunar-claude
```

**Features:**

- Four creator skills (skill-creator, agent-creator, hook-creator, command-creator)
- Interactive `/new-plugin` command
- References official Claude Code documentation

See [plugins/meta/meta-claude/README.md](plugins/meta/meta-claude/README.md) for details.

### ansible-best-practices

Ansible playbook refactoring, role development, testing, and best practices with Infisical secrets management.

**Install:**

```bash
/plugin install ansible-best-practices@lunar-claude
```

**Features:**

- Comprehensive ansible-best-practices skill
- Infisical secret management integration
- State-based playbook patterns
- Idempotency and error handling patterns
- Testing with ansible-lint and Molecule
- Python analysis tools (complexity, idempotency checks)

See [plugins/infrastructure/ansible-best-practices/README.md](plugins/infrastructure/ansible-best-practices/README.md) for details.

### proxmox-infrastructure

Proxmox VE cluster management including VM provisioning, templates, VLAN networking, and CEPH storage.

**Install:**

```bash
/plugin install proxmox-infrastructure@lunar-claude
```

**Features:**

- Comprehensive proxmox-infrastructure skill
- Cloud-init template creation patterns
- VLAN-aware bridge configuration
- CEPH storage deployment
- VM provisioning with Terraform/Ansible
- Python cluster management tools

See [plugins/infrastructure/proxmox-infrastructure/README.md](plugins/infrastructure/proxmox-infrastructure/README.md) for details.

### python-uv-tools

Python single-file script development using uv and PEP 723 inline metadata.

**Install:**

```bash
/plugin install python-uv-tools@lunar-claude
```

**Features:**

- Comprehensive python-uv-scripts skill
- Script creation patterns and best practices
- Testing, security, and CI/CD guidance
- Extensive reference documentation

See [plugins/devops/python-uv-tools/README.md](plugins/devops/python-uv-tools/README.md) for details.

### netbox-powerdns-integration

NetBox IPAM and PowerDNS integration for automated DNS record management and infrastructure documentation.

**Install:**

```bash
/plugin install netbox-powerdns-integration@lunar-claude
```

**Features:**

- Comprehensive netbox-powerdns-integration skill
- NetBox API usage and IPAM management
- DNS naming convention validation
- PowerDNS sync plugin configuration
- Terraform NetBox provider integration
- Ansible dynamic inventory patterns
- Python API clients and automation tools

See [plugins/homelab/netbox-powerdns-integration/README.md](plugins/homelab/netbox-powerdns-integration/README.md) for details.

## Development

### Creating New Plugins

Use the meta-claude plugin:

```bash
/new-plugin
```

Or manually:

1. Copy template: `cp -r templates/plugin-template/ plugins/<category>/<name>/`
2. Customize plugin.json and README.md
3. Add to .claude-plugin/marketplace.json
4. Commit changes

### Template Structure

The plugin template includes:

- Complete plugin.json with placeholders
- README.md with standard sections
- Example agent, skill, and hooks
- All required directories

### Verification

Run structure verification:

```bash
./scripts/verify-structure.sh
```

### Local Testing

```bash
# Add marketplace
/plugin marketplace add /path/to/lunar-claude

# Install plugin
/plugin install plugin-name@lunar-claude
```

## Design Documentation

See [docs/plans/](docs/plans/) for detailed design and implementation documentation.

## Version History

- 0.1.0 - Initial marketplace with meta-claude plugin
