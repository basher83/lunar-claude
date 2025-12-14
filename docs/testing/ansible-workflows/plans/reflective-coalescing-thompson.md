# Testing Plan: ansible-workflows Plugin

## Problem Statement

The current test scenarios in `docs/testing/ansible-workflows/` are fundamentally flawed:

1. **Vague prompts** - "install-packages" tells the generator nothing useful
2. **Infrastructure focus** - Tests verify state files exist, not code quality
3. **Context contamination** - Test documents would taint Claude's awareness
4. **No quality metrics** - Success is "did files get created" not "is code production-ready"

These tests verify the plugin's plumbing, not its actual value proposition: **generating production-ready Ansible code**.

## Design Principles

1. **Test real value** - Does the plugin produce useful, working Ansible code?
2. **No contamination** - Claude should not know it's being tested
3. **Objective metrics** - Measurable criteria, not subjective checklists
4. **Post-session evaluation** - Analyze results after sessions end, not during
5. **Minimal infrastructure** - Simple structure, not over-engineered harnesses

## Implementation Plan

### Phase 1: Scrap Existing Tests

**Files to delete:**
- `docs/testing/ansible-workflows/scenario-01-simple-playbook-empty.md`
- `docs/testing/ansible-workflows/scenario-02-orchestrator-empty.md`
- `docs/testing/ansible-workflows/scenario-03-role-established.md`
- `docs/testing/ansible-workflows/scenario-04-complex-orchestrator.md`
- `docs/testing/ansible-workflows/scenario-05-validation-failure.md`
- `docs/testing/ansible-workflows/scenario-06-review-rejection.md`
- `docs/testing/ansible-workflows/scenario-07-interruption-recovery.md`
- `docs/testing/ansible-workflows/README.md`

### Phase 2: Create Quality Rubrics

Create evaluation criteria that measure actual code quality:

**File: `docs/testing/ansible-workflows/rubrics/quality-criteria.md`**

Quality dimensions to evaluate:
- **Idempotency**: command/shell have changed_when, check-before-create patterns
- **Security**: no_log on secrets, no hardcoded credentials, proper file permissions
- **Module selection**: FQCN everywhere, native modules over shell, Proxmox collection used
- **Error handling**: set -euo pipefail in shell, validation assertions, state patterns
- **Structure**: descriptive task names, role variable prefixes, logical organization
- **Linting**: 0 errors, minimal warnings

Scoring: PASS / MINOR (1-2 issues) / FAIL (3+ issues or critical missing)

### Phase 3: Define Realistic Scenarios

Create a catalog of natural user prompts (NOT loaded during sessions):

**File: `docs/testing/ansible-workflows/scenarios.md`**

| ID | User Need | Complexity |
|----|-----------|------------|
| R01 | Install Docker CE on Ubuntu 22.04 with GPG key verification | Simple |
| R02 | Configure Proxmox cloud-init templates with custom user-data | Medium |
| R03 | Setup UFW firewall with SSH, HTTP, HTTPS, Proxmox ports | Simple |
| R04 | Deploy Nginx with Let's Encrypt SSL via certbot | Complex |
| R05 | Configure VLAN-aware bridges on Proxmox hosts | Medium |
| R06 | Manage system users with SSH keys and sudo access | Medium |

### Phase 4: Create Post-Session Evaluation Template

**File: `docs/testing/ansible-workflows/evaluation-template.md`**

Template for recording observations AFTER sessions:
- Date, environment, exact prompt used
- Files generated, pipeline completion
- Quality evaluation for each dimension
- Overall assessment (Production Ready / Needs Polish / Needs Rework)
- Strengths, weaknesses, real-world usability
- Improvement opportunities identified

### Phase 5: Set Up Test Environment

The test repo at `/Users/basher8383/dev/personal/ansible-workflow/` is already minimal and clean. No changes needed - it correctly simulates a fresh user repo.

### Phase 6: Create Automated Checks

**File: `docs/testing/ansible-workflows/scripts/evaluate.sh`**

Post-session script to run:
```bash
# Run lint check
uv run ansible-lint <target>

# Run syntax check
uv run ansible-playbook <target> --syntax-check

# Run idempotency check
${CLAUDE_PLUGIN_ROOT}/skills/ansible-idempotency/scripts/check_idempotency.py <target>
```

## Testing Protocol

### Before Session
1. Ensure test repo is clean (no state files, no generated playbooks)
2. Memorize the prompt to use (do NOT load scenario docs)
3. Start fresh Claude session in test repo

### During Session
1. Give natural prompt exactly as a real user would
2. Let plugin run through its workflow
3. Do NOT mention testing, do NOT open test documents
4. Observe behavior mentally, do NOT document during session

### After Session
1. Exit session completely
2. Run automated checks on generated code
3. Fill out evaluation template
4. Record observations and quality scores

## Directory Structure

```text
docs/testing/ansible-workflows/
├── README.md                    # Framework overview (this plan, condensed)
├── rubrics/
│   └── quality-criteria.md      # Objective quality dimensions and scoring
├── scenarios.md                 # Catalog of realistic prompts (reference only)
├── evaluation-template.md       # Post-session analysis template
├── scripts/
│   └── evaluate.sh              # Automated quality checks
└── results/                     # Completed evaluations (gitignored)
```

## Success Criteria for Testing Framework

The framework works if:
1. Generated code can be objectively evaluated
2. Sessions produce unbiased results (no contamination)
3. Results identify specific plugin improvements
4. Process is simple enough to actually use

## Files to Modify

| File | Action |
|------|--------|
| `docs/testing/ansible-workflows/scenario-*.md` (7 files) | Delete |
| `docs/testing/ansible-workflows/README.md` | Replace with framework overview |
| `docs/testing/ansible-workflows/rubrics/quality-criteria.md` | Create |
| `docs/testing/ansible-workflows/scenarios.md` | Create |
| `docs/testing/ansible-workflows/evaluation-template.md` | Create |
| `docs/testing/ansible-workflows/scripts/evaluate.sh` | Create |
