# Ansible Best Practices

Expert guidance for writing maintainable, idempotent, and testable Ansible playbooks based on real-world patterns.

## Installation

Add the lunar-claude marketplace:

```bash
/plugin marketplace add basher83/lunar-claude
```

Install ansible-best-practices:

```bash
/plugin install ansible-best-practices@lunar-claude
```

## Components

### Skills

- **ansible-best-practices** - Comprehensive skill for Ansible development
  - Infisical secret management integration
  - State-based playbooks (single playbook for create/delete via `state` variable)
  - Hybrid module approach (native modules + command when needed)
  - Proper error handling and idempotency patterns
  - Network automation with community modules
  - Task organization and reusable patterns
  - Variable organization and precedence
  - Module selection (ansible.builtin vs community)
  - Testing with ansible-lint and Molecule
  - Anti-patterns and common mistakes

## Usage

### Autonomous Mode

Simply ask Claude to help with Ansible development:

```
"Refactor this Ansible playbook for idempotency"
"Create a role for deploying Docker containers"
"Help me add Infisical secret management to my playbook"
"Review my Ansible playbook for best practices"
```

Claude will automatically use the ansible-best-practices skill.

## How It Works

The ansible-best-practices skill provides comprehensive guidance on:

- **Core Patterns**: Real-world patterns from production infrastructure
  - Infisical secret management
  - State-based playbooks (not separate create/delete)
  - Hybrid module approach (native + command)
  - Proper error handling with changed_when/failed_when
  - Network automation patterns
  - Task organization strategies

- **Variable Management**: Complete understanding of precedence and organization
- **Module Selection**: When to use ansible.builtin vs community collections
- **Testing**: Integration with ansible-lint and Molecule
- **Anti-Patterns**: Common mistakes and how to avoid them

## Supporting Documentation

The skill includes extensive reference material:
- `/patterns/` - Production patterns (secrets, roles, network, cluster, CEPH)
- `/reference/` - Core reference guides (variables, idempotency, testing, collections)
- `/anti-patterns/` - Mistakes to avoid and refactoring guides
- `/examples/` - Real-world examples
- `/tools/` - Python analysis tools (uv-based)
  - `analyze_playbook.py` - Complexity metrics
  - `check_idempotency.py` - Find non-idempotent patterns
  - `lint-all.sh` - Run all linters

## Key Features

### Infisical Secret Management

Reusable task pattern for Infisical integration with proper validation and fallbacks.

### State-Based Playbooks

Single playbook handles both create and remove operations via `state` variable - follows community role patterns.

### Idempotency First

Check before create, verify after - comprehensive patterns for `changed_when` and `failed_when`.

### Production-Ready

Based on real-world patterns from production homelab infrastructure, analyzed against geerlingguy community roles.

## Version History

- 1.0.0 - Initial release with comprehensive Ansible best practices guidance
