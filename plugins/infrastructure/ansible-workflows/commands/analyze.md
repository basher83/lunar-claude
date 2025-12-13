---
description: Analyze Ansible code for improvements or suggest enhancements
argument-hint: <path> [--mode review|enhance]
allowed-tools: ["Read", "Grep", "Glob", "Bash", "WebSearch"]
model: sonnet
---

Analyze Ansible code at `$1` in mode `$2` (default: review).

Load ALL ansible-* skills before analyzing.

**Mode: review** (analyze existing code)

Check for:
- **Idempotency:** changed_when on commands, check-before-create patterns
- **Security:** no_log on secrets, no hardcoded credentials
- **Structure:** FQCN, descriptive task names, role-prefixed variables
- **Error handling:** Validation, graceful failures, clear messages
- **Proxmox:** Native modules over CLI where possible

Output findings as structured report with file:line references and fixes.

**Mode: enhance** (suggest forward-looking improvements)

Identify:
- Automation gaps (manual processes to automate)
- Best practice upgrades (newer patterns not adopted)
- Integration opportunities (additional Proxmox automation)
- Scalability improvements (role refactoring, variable organization)

Output prioritized enhancement roadmap.

After analysis:
- **review mode:** Hand findings to `ansible-reviewer` for formal report
- **enhance mode:** Present roadmap for user prioritization

Report: scope analyzed, mode used, key findings, recommendations.
