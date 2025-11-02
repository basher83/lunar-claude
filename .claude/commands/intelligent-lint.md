---
description: Run intelligent markdown linting with autonomous agent analysis
allowed-tools: Bash(scripts/intelligent-markdown-lint.py:*), Task
---

# Intelligent Markdown Linting

Execute the intelligent markdown linting workflow using autonomous agents.

## Workflow

This command orchestrates a three-layer agent system:

1. **Orchestrator** (scripts/intelligent-markdown-lint.py):
   - Discovers and triages markdown linting errors
   - Spawns Investigator for ambiguous errors
   - Spawns Fixer for confirmed errors
   - Verifies results

2. **Investigator** (.claude/agents/markdown-investigator.md):
   - Autonomous analysis with Read, Grep, Glob, Bash tools
   - Determines if errors are fixable or false positives
   - Provides reasoning for each verdict

3. **Fixer** (.claude/agents/markdown-fixer.md):
   - Executes fixes using investigation context
   - Verifies changes with rumdl
   - Reports results

## Usage

```bash
/intelligent-lint
```

## What This Does

1. Runs `rumdl check .` to find all markdown errors
2. Categorizes as simple (MD013, MD036, MD025) or ambiguous (MD033, MD053, MD052, MD041)
3. Spawns Investigator subagent for ambiguous errors
4. Aggregates results and calculates total workload
5. Spawns Fixer subagent with error context
6. Verifies fixes with final rumdl check
7. Reports before/after statistics and fix rate

## Expected Output

```text
🚀 Intelligent Markdown Linting Orchestrator
============================================================

📋 Phase 1: Discovery & Triage
------------------------------------------------------------
Total errors found: [N]
├─ Simple (directly fixable): [N]
└─ Ambiguous (needs investigation): [N]

🔍 Phase 2: Investigation
------------------------------------------------------------
📊 Spawning Investigator subagent...
✅ Investigation complete: analyzed [N] files

📊 Phase 3: Calculate Workload
------------------------------------------------------------
Simple errors: [N]
Investigated fixable: [N]
False positives preserved: [N]
Total fixable: [N]

🔧 Phase 4: Fixing
------------------------------------------------------------
🔧 Spawning Fixer subagent...
✅ Fixes complete: processed [N] files
✅ Fixed [N] errors across [N] files

✅ Phase 5: Verification
------------------------------------------------------------
Errors before: [N]
Errors after: [N]
Fix rate: [N]%
```

## Architecture

See `docs/architecture/intelligent-markdown-linting-agent.md` for complete design details.

## Environment Requirements

- `ANTHROPIC_API_KEY` must be set
- `rumdl` linter installed
- Python 3.11+ with `uv`

## Related

- **Current workflow:** `.claude/commands/fix-markdown-linting.md` (regex-based)
- **Implementation plan:** `docs/plans/2025-11-02-intelligent-markdown-linting-agent-mvp.md`
