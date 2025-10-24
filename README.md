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
