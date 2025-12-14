# ansible-workflows Plugin Evaluation

Framework for evaluating whether the ansible-workflows plugin produces production-ready Ansible code.

## Core Principle

Test **output quality**, not infrastructure mechanics.

The plugin's value is generating useful Ansible code. Evaluation measures code quality against objective criteria, not whether state files were created.

## Critical: Workspace Trust Required

**DO NOT use `claude --dangerously-skip-permissions` for plugin testing.**

This flag skips the workspace trust prompt, which causes plugin agents to spawn
without tools available. The model will output XML-style pseudo-tool calls
(`<write_file>`, `<skill>`, etc.) as text instead of actual tool invocations,
resulting in 0 tool uses and no files created.

**Symptoms of this issue:**

- Agent completes with "0 tool uses"
- Agent response contains XML tags like `<write_file>...</write_file>`
- No files are actually written despite detailed output
- All agents in the project show 0 tool uses (systemic)

**Fix:** Start Claude normally and accept the workspace trust prompt.

## Evaluation Protocol

### Before Session

1. Ensure target repo is clean (no state files, no prior playbooks)
2. Memorize the prompt from `scenarios.md` - do NOT load it in session
3. Start fresh Claude session in target repo **without `--dangerously-skip-permissions`**
4. Accept the workspace trust prompt if shown

### During Session

1. Run the slash command (e.g., `/ansible-workflows:create-playbook setup-docker`)
2. After scaffolding completes, provide the follow-up requirements
3. Let the plugin run through its full pipeline
4. Do NOT mention evaluation, do NOT open these documents
5. Observe behavior mentally - note which agents run

### After Session

1. Exit session completely
2. Verify pipeline executed (check for state files):

   ```bash
   ls -la /path/to/repo/.claude/ansible-workflows*.md
   ```

3. Run automated checks:

   ```bash
   ./scripts/evaluate.sh ansible/playbooks/generated-file.yml
   ```

4. Copy `evaluation-template.md` to `results/YYYY-MM-DD-scenario.md`
5. Fill out quality assessment using `rubrics/quality-criteria.md`

## Directory Structure

```text
docs/testing/ansible-workflows/
├── README.md                 # This file
├── scenarios.md              # Prompts catalog (reference only)
├── evaluation-template.md    # Post-session template
├── rubrics/
│   └── quality-criteria.md   # Objective quality dimensions
├── scripts/
│   └── evaluate.sh           # Automated checks
└── results/                  # Completed evaluations (gitignored)
```

## Quality Dimensions

Evaluated criteria (see `rubrics/quality-criteria.md` for details):

| Dimension | Priority | Key Checks |
|-----------|----------|------------|
| Idempotency | Critical | changed_when, check-before-create |
| Security | Critical | no_log, no hardcoded secrets |
| Module Selection | High | FQCN, native modules |
| Error Handling | High | set -euo pipefail, validation |
| Structure | Medium | Naming, organization |
| Linting | Baseline | 0 errors |

## Scoring

- **PASS**: Meets all criteria
- **MINOR**: 1-2 issues, easily fixed
- **FAIL**: 3+ issues or critical pattern missing

**Overall Assessment:**

- **Production Ready**: All Critical/High = PASS, Medium = PASS/MINOR
- **Needs Polish**: Any High = MINOR
- **Needs Rework**: Any Critical/High = FAIL

## Target Environments

- **Empty repo**: `/Users/basher8383/dev/personal/ansible-workflow/` - Minimal structure
- **Established repo**: Virgo-Core or similar with existing patterns

## Running Evaluations

```bash
# 1. Clean target repo
rm -f /path/to/repo/.claude/ansible-workflows.local.md
rm -f /path/to/repo/.claude/ansible-workflows.*.bundle.md
rm -rf /path/to/repo/ansible/playbooks/*.yml
rm -rf /path/to/repo/ansible/roles/*/

# 2. Start session in target repo (NO --dangerously-skip-permissions!)
cd /path/to/repo
claude
# Accept workspace trust prompt if shown

# 3. Give prompt (memorized from scenarios.md)
# 4. Exit session
# 5. Evaluate
./docs/testing/ansible-workflows/scripts/evaluate.sh ansible/playbooks/file.yml
```
