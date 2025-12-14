# Quality Evaluation Criteria

Objective criteria for evaluating generated Ansible code. Apply these AFTER sessions end.

## Scoring

Each dimension: **PASS** | **MINOR** (1-2 issues) | **FAIL** (3+ issues or critical missing)

Overall: **Production Ready** (all PASS/MINOR) | **Needs Polish** (any High=MINOR) | **Needs Rework** (any Critical/High=FAIL)

## Critical Dimensions

### Idempotency

| Criterion | Check |
|-----------|-------|
| command/shell tasks have `changed_when` | Grep for command/shell without changed_when |
| OR tasks have `creates`/`removes` | Alternative to changed_when for file operations |
| Check-before-create patterns | Register + when for conditional resource creation |
| Running twice produces no changes | Mental evaluation of task logic |

**Automated check:**

```bash
${CLAUDE_PLUGIN_ROOT}/skills/ansible-idempotency/scripts/check_idempotency.py <target>
```

### Security

| Criterion | Check |
|-----------|-------|
| No hardcoded passwords/tokens/keys | Grep for obvious patterns |
| `no_log: true` on credential tasks | Tasks with password, secret, token in name |
| Secrets use variables/vault/Infisical | Not inline strings |
| Sensitive files have proper permissions | 0600 for keys, 0640 for configs |

## High Priority Dimensions

### Module Selection

| Criterion | Check |
|-----------|-------|
| FQCN used for all modules | `ansible.builtin.*`, `community.*` |
| Native modules over shell commands | No shell for apt, file, service, user |
| Proxmox collection used where available | `community.proxmox.*` for PVE operations |

**Automated check:**

```bash
grep -E "^\s+-\s+\w+:" <target>  # Short module names (bad)
grep -E "ansible\.builtin\.|community\." <target>  # FQCN (good)
```

### Error Handling

| Criterion | Check |
|-----------|-------|
| Shell tasks use `set -euo pipefail` | In shell task content |
| Validation with `assert` at playbook start | For critical variables/state |
| State pattern supports present/absent | For reversible operations |
| `failed_when` used appropriately | For expected non-zero exits |

## Medium Priority Dimensions

### Structure & Maintainability

| Criterion | Check |
|-----------|-------|
| Task names are descriptive | Verb + object, not vague |
| Role variables use role prefix | `docker_*` not just `host` |
| Logical task organization | Follows execution flow |
| Handlers defined and notified | For service restarts |

### Linting

| Criterion | Check |
|-----------|-------|
| ansible-lint produces 0 errors | `uv run ansible-lint <target>` |
| Syntax check passes | `uv run ansible-playbook <target> --syntax-check` |
| Warnings are minimal | Not blocking but noted |

## Evaluation Checklist

```text
File: ___________________
Date: ___________________

IDEMPOTENCY:      [ ] PASS  [ ] MINOR  [ ] FAIL
  - changed_when present: ___
  - check-before-create: ___
  - issues: ___

SECURITY:         [ ] PASS  [ ] MINOR  [ ] FAIL
  - no hardcoded secrets: ___
  - no_log used: ___
  - issues: ___

MODULE SELECTION: [ ] PASS  [ ] MINOR  [ ] FAIL
  - FQCN everywhere: ___
  - native modules: ___
  - issues: ___

ERROR HANDLING:   [ ] PASS  [ ] MINOR  [ ] FAIL
  - set -euo pipefail: ___
  - validation: ___
  - issues: ___

STRUCTURE:        [ ] PASS  [ ] MINOR  [ ] FAIL
  - naming: ___
  - organization: ___
  - issues: ___

LINTING:          [ ] PASS  [ ] FAIL
  - errors: ___
  - warnings: ___

OVERALL:          [ ] Production Ready  [ ] Needs Polish  [ ] Needs Rework
```
