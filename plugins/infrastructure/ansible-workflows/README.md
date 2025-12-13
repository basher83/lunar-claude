# Ansible Workflows Plugin

End-to-end Ansible workflow automation for Claude Code. Design, create, validate,
and review playbooks and roles with orchestrated multi-agent pipelines.

## Features

- **Orchestrated Pipeline**: Commands → Generator → Validator → Reviewer with automatic handoffs
- **8 Focused Skills**: Modular knowledge for different aspects of Ansible development
- **4 Specialized Agents**: Generator, Validator, Reviewer, Debugger with clear responsibilities
- **Structured Reviews**: Measurable ratings, categorized findings, actionable narrative feedback

## Workflow Pipeline

```text
/ansible:create-* ──► ansible-generator ──► ansible-validator ──► ansible-reviewer
                                                    │
                                                  FAIL?
                                                    │
                                                    ▼
                                            ansible-debugger
                                                    │
                                                    └──► Loop back to generator
```

## Components

### Skills

| Skill | Purpose |
|-------|---------|
| `ansible-fundamentals` | Golden rules, FQCN, module selection, uv run |
| `ansible-playbook-design` | State-based playbooks, play structure, imports |
| `ansible-role-design` | Role structure, vars/defaults, handlers, meta |
| `ansible-idempotency` | changed_when, failed_when, check-before-create |
| `ansible-secrets` | Infisical integration, no_log, security |
| `ansible-error-handling` | Try/rescue, fail module, validation patterns |
| `ansible-testing` | ansible-lint configuration, integration testing |
| `ansible-proxmox` | community.proxmox modules, avoid raw CLI |

### Commands

| Command | Description |
|---------|-------------|
| `/ansible:create-role` | Scaffold a new Ansible role with standard structure |
| `/ansible:create-playbook` | Scaffold a state-based playbook |
| `/ansible:lint` | Run ansible-lint with fix guidance |
| `/ansible:analyze` | Analyze existing code or suggest enhancements |

### Agents

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `ansible-generator` | From commands or explicit request | Generate idempotent Ansible code |
| `ansible-validator` | After generation | Run lint, syntax checks |
| `ansible-reviewer` | After validation passes | Deep best-practices review |
| `ansible-debugger` | Validation/execution failures | Root cause analysis and fixes |

## Installation

Install from the lunar-claude marketplace:

```bash
/plugin install ansible-workflows@lunar-claude
```

## Usage Examples

### Create a New Role

```bash
/ansible:create-role proxmox-vm
```

### Create a Playbook

```bash
/ansible:create-playbook create-k8s-cluster --hosts proxmox
```

### Analyze for Improvements

```bash
/ansible:analyze ansible/playbooks/network-setup.yml --mode review
```

### Get Enhancement Suggestions

```bash
/ansible:analyze ansible/roles/proxmox_network --mode enhance
```

## Review Report Format

The ansible-reviewer agent outputs structured reports:

```yaml
## Summary
overall_rating: 4.0/5
recommendation: APPROVED_WITH_CHANGES

## Findings by Category
- IDEMPOTENCY, SECURITY, STRUCTURE, PERFORMANCE, MAINTAINABILITY, PROXMOX

## Metrics
- Scores per category (0.0-1.0)
- Overall confidence rating

## Narrative Assessment
- What's working well
- Recommended improvements
- Rationale for recommendation
```

## Configuration

Create `.claude/ansible-workflows.local.md` for workflow state tracking (auto-managed).

## Dependencies

- ansible-lint (configured in `ansible/.ansible-lint`)
- uv for Python/Ansible execution
- Infisical for secrets management (optional)

## Migration from ansible-best-practices

This plugin replaces the monolithic `.claude/skills/ansible-best-practices/` skill
with focused, modular skills. After enabling, the old skill can be removed.
