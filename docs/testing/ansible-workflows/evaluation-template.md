# Session Evaluation Template

Copy this template to `results/YYYY-MM-DD-scenario-name.md` after each session.

---

# Session: [Scenario Name]

**Date:** YYYY-MM-DD
**Environment:** [Empty repo / Established repo]
**Claude Code Version:** X.X.X

## Prompt Used

> [Exact prompt given to Claude - copy verbatim]

## Session Summary

**Pipeline completed:** [Yes / No / Partial]
**Total duration:** ~X minutes
**Files generated:**

- `path/to/file.yml` (X lines)
- `path/to/role/` (Y files)

**Agents observed:** [generator, validator, reviewer, debugger - which ran]

## Quality Evaluation

Use rubrics/quality-criteria.md as reference.

### Idempotency: [PASS / MINOR / FAIL]

- [ ] command/shell tasks have changed_when
- [ ] Check-before-create patterns used where appropriate
- [ ] Running twice would produce no changes

**Issues found:**

```text
[List specific violations with file:line]
```

### Security: [PASS / MINOR / FAIL]

- [ ] No hardcoded passwords/tokens/keys
- [ ] no_log: true on sensitive tasks
- [ ] Secrets use variables/vault pattern

**Issues found:**

```text
[List specific violations]
```

### Module Selection: [PASS / MINOR / FAIL]

- [ ] FQCN used for all modules
- [ ] Native modules preferred over shell
- [ ] Proxmox collection used (if applicable)

**Issues found:**

```text
[List specific violations]
```

### Error Handling: [PASS / MINOR / FAIL]

- [ ] Shell tasks use set -euo pipefail
- [ ] Validation with assert where appropriate
- [ ] State pattern supports present/absent (if applicable)

**Issues found:**

```text
[List specific violations]
```

### Structure: [PASS / MINOR / FAIL]

- [ ] Task names are descriptive
- [ ] Variable naming follows conventions
- [ ] Logical organization

**Issues found:**

```text
[List specific violations]
```

### Linting

**Errors:** X
**Warnings:** Y

<details>
<summary>Lint output</summary>

```text
[Paste ansible-lint output]
```

</details>

## Overall Assessment

**Rating:** [Production Ready / Needs Polish / Needs Rework]

**Would deploy to production:** [Yes / No / With changes]

**Strengths:**

- [What did the plugin do well?]

**Weaknesses:**

- [What patterns were missing or incorrect?]

## Plugin Observations

**Skills loaded:** [List if visible in output]

**Agent transitions:** [scaffolding -> generating -> validating -> reviewing]

**State management:** [Any issues with state files or bundles?]

**Unexpected behaviors:**

- [Anything surprising?]

## Improvement Opportunities

Based on this session, potential plugin improvements:

1. [Specific suggestion]
2. [Specific suggestion]
