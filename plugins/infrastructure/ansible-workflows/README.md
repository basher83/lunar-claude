# Ansible Workflows Plugin

End-to-end Ansible workflow automation for Claude Code. Design, create, validate,
and review playbooks and roles with orchestrated multi-agent pipelines and
automatic state tracking.

## Features

- **Orchestrated Pipeline**: Commands → Generator → Validator → Reviewer with automatic handoffs
- **Pipeline State Tracking**: Persistent state via `.local.md` files with YAML frontmatter
- **Context Bundles**: Structured handoff data between agents via `.bundle.md` files
- **Stop Hooks**: Prevents session termination when pipeline is active
- **Retry Logic**: Automatic validation retry with configurable limit (max 3 attempts)
- **8 Focused Skills**: Modular knowledge for different aspects of Ansible development
- **4 Specialized Agents**: Generator, Validator, Reviewer, Debugger with clear responsibilities

## Workflow Pipeline

```text
/ansible:create-* ──► ansible-generator ──► ansible-validator
        │                    │                      │
        │                    │              ┌───────┴───────┐
        ▼                    ▼              ▼               ▼
   Initialize          Write bundle     PASS?            FAIL?
   state file          (.generating)      │               │
                                          ▼               ▼
                                   ansible-reviewer  ansible-debugger
                                          │               │
                                   ┌──────┴──────┐        │
                                   ▼             ▼        ▼
                               APPROVED    NEEDS_REWORK   │
                                   │             │        │
                                   ▼             └────────┤
                              Complete                    │
                           (active: false)                │
                                                          ▼
                                                  Loop back to validator
                                                  (max 3 attempts)
```

## Pipeline State Management

The plugin tracks pipeline progress through two mechanisms:

### State File

Location: `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.local.md`

```yaml
---
active: true
pipeline_phase: validating
target_path: ansible/playbooks/setup-docker.yml
current_agent: ansible-validator
started_at: "2024-01-15T10:30:00Z"
validation_attempts: 1
last_validation_passed: false
---

# Ansible Workflows Pipeline

Target: ansible/playbooks/setup-docker.yml
Type: playbook

[2024-01-15 10:35:00 UTC] ansible-generator completed -> validating
```

### Context Bundles

Agents pass structured context via bundle files:

| Bundle | Source | Target | Purpose |
|--------|--------|--------|---------|
| `.scaffolding.bundle.md` | Command | Generator | User requirements, target path |
| `.generating.bundle.md` | Generator | Validator | Files created, patterns applied |
| `.validating.bundle.md` | Validator | Reviewer/Debugger | Validation results, errors |
| `.debugging.bundle.md` | Debugger | Validator | Fixes applied, re-validation command |
| `.reviewing.bundle.md` | Reviewer | Debugger | Required fixes for NEEDS_REWORK |

All bundles are stored in `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.<phase>.bundle.md`.

## Hooks

The plugin registers two hooks for pipeline orchestration:

### SubagentStop Hook

Triggers when any subagent completes. Validates that the agent wrote its
context bundle and updates the state file with the next pipeline phase.

### Stop Hook

Blocks session termination when an active pipeline exists. Provides guidance
on continuing the pipeline or aborting by setting `active: false`.

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
| `/ansible-workflows:create-role <name>` | Scaffold a new Ansible role with standard structure |
| `/ansible-workflows:create-playbook <name>` | Scaffold a state-based playbook |
| `/ansible-workflows:lint [path]` | Run ansible-lint with fix guidance |
| `/ansible-workflows:analyze <path> [--mode]` | Analyze existing code or suggest enhancements |

### Agents

| Agent | Model | Trigger | Purpose |
|-------|-------|---------|---------|
| `ansible-generator` | sonnet | From commands or explicit request | Generate idempotent Ansible code |
| `ansible-validator` | haiku | After generation | Run lint, syntax checks |
| `ansible-reviewer` | opus | After validation passes | Deep best-practices review |
| `ansible-debugger` | sonnet | Validation/review failures | Root cause analysis and fixes |

## Installation

Install from the lunar-claude marketplace:

```bash
/install ansible-workflows@lunar-claude
```

## Usage Examples

### Create a New Role

```bash
/ansible-workflows:create-role proxmox-vm
```

This initializes the pipeline state and hands off to ansible-generator.

### Create a Playbook

```bash
/ansible-workflows:create-playbook create-k8s-cluster --hosts proxmox
```

### Find Issues in Existing Code

```bash
/ansible-workflows:analyze ansible/playbooks/network-setup.yml --mode review
```

Review mode checks for problems: missing idempotency controls, security issues,
FQCN violations, error handling gaps. Outputs a structured report with
file:line references and fixes.

### Plan Future Improvements

```bash
/ansible-workflows:analyze ansible/roles/proxmox_network --mode enhance
```

Enhance mode identifies opportunities: automation gaps, newer patterns to
adopt, integration possibilities, scalability improvements. Outputs a
prioritized roadmap.

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

## Aborting a Pipeline

If you need to stop an active pipeline:

1. Edit `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.local.md`
2. Set `active: false` in the YAML frontmatter
3. The Stop hook will no longer block session termination

## Automatic Gitignore Setup

The plugin automatically adds gitignore patterns to your project when the
pipeline is initialized. The following patterns are appended to
`$CLAUDE_PROJECT_DIR/.gitignore`:

```text
# Ansible Workflows plugin state (auto-added)
.claude/ansible-workflows.local.md
.claude/ansible-workflows.*.bundle.md
```

This happens at two points for defense in depth:

1. When commands (`create-playbook`, `create-role`) initialize the pipeline
2. When hooks run during pipeline execution

## Dependencies

- ansible-lint (configured in `ansible/.ansible-lint`)
- uv for Python/Ansible execution
- Python 3.13+ for hook scripts
- Infisical for secrets management (optional)

## Architecture Notes

**Key insight**: Sub-agents cannot spawn other sub-agents. The main Claude
Code session acts as the orchestrator, dispatching agents in sequence based on
pipeline state. The "hand off to validator" instructions in agents are
guidance for the main session, not executable actions by the sub-agent itself.

**State isolation**: Each project maintains its own pipeline state via
`$CLAUDE_PROJECT_DIR/.claude/`. Multiple projects can run independent
pipelines without interference.

**Retry limit**: After 3 failed validation attempts, the pipeline escalates
to the user for manual intervention rather than continuing indefinitely.
