# Intelligent Markdown Linting Agent Architecture

**Status:** Design Phase
**Created:** 2025-11-02
**Purpose:** Replace regex-based markdown linting with intelligent Claude Agent SDK orchestration

## Implementation Status

### Phase 1 (MVP): ✅ Complete

- [x] Agent definitions (Orchestrator, Investigator, Fixer)
- [x] Orchestrator script with Claude SDK integration
- [x] Discovery and triage logic
- [x] Investigation result aggregation
- [x] End-to-end testing
- [x] Slash command integration

### Phase 2 (Parallel Agents): 🚧 Planned

- [ ] Greedy bin-packing distribution
- [ ] Parallel Investigator spawning
- [ ] Parallel Fixer spawning

### Phase 3 (Adaptive Recovery): 📋 Not Started

- [ ] Wave 2+ recovery system
- [ ] Failure detection and retry logic

### Phase 4 (Optimization): 📋 Not Started

- [ ] Cost analysis and model selection
- [ ] Investigation result caching
- [ ] Batching strategies

## Overview

A three-layer agent system that uses Claude's contextual understanding to accurately categorize and fix markdown linting
errors. Achieves 80% fix rate (vs 40% with regex) through autonomous investigation and adaptive workload distribution.

## Problem Statement

Regex-based categorization fails for context-dependent errors:

- **MD033 (Inline HTML):** Is `<tip>` intentional or accidental?
- **MD053 (Reference unused):** Is the reference actually used in another file?
- **MD052 (Reference not found):** Is `[tools.uv]` a TOML section or broken link?
- **MD041 (Missing H1):** Does YAML frontmatter make this acceptable?

**Solution:** Autonomous Investigator agents with full repository access make these determinations.

## Architecture Diagram

```text
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR (Strategic Layer)                          │
│ - Discovery: Run rumdl, collect all errors              │
│ - Triage: Simple errors vs ambiguous errors             │
│ - Spawn: Investigators (Wave 1)                         │
│ - Aggregate: Collect verdicts + reasoning               │
│ - Calculate: Real workload (drop false positives)       │
│ - Distribute: Greedy bin-packing by error count         │
│ - Spawn: Fixers (balanced workload)                     │
│ - Recovery: Adaptive Wave 2+ for failures/incomplete    │
│ - Verify: Final rumdl check                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ INVESTIGATORS (Intelligence Layer) - Full Autonomy      │
│ Tools: Read, Grep, Glob, Bash                           │
│                                                          │
│ Assignment: "Determine if these errors are fixable"     │
│                                                          │
│ Freedom to:                                              │
│ - Read current file for context                         │
│ - Search across entire repository                       │
│ - Read related files                                    │
│ - Use any logic needed                                  │
│ - Make the final call                                   │
│                                                          │
│ Report back: Per-error verdict + reasoning              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ FIXERS (Execution Layer)                                │
│                                                          │
│ Receive: Errors + investigation context                 │
│ Task: Fix confirmed errors, verify with rumdl           │
└─────────────────────────────────────────────────────────┘
```

## Three-Layer System

### Layer 1: Orchestrator (Strategic)

**Responsibilities:**

1. **Discovery:** Execute `rumdl check .` to find all errors
2. **Triage:** Categorize errors as simple (directly fixable) or ambiguous (needs investigation)
3. **Spawn Investigators:** Launch Wave 1 with balanced workload
4. **Aggregate Results:** Collect investigation verdicts and reasoning
5. **Calculate Workload:** Total fixable errors (simple + investigated)
6. **Distribute Work:** Greedy bin-packing to balance Fixer workload
7. **Spawn Fixers:** Launch with error assignments + context
8. **Adaptive Recovery:** Spawn Wave 2+ for failures/incomplete work
9. **Verification:** Run final `rumdl check .` to confirm results

**Autonomy:** Makes all strategic decisions about agent spawning, workload distribution, and recovery strategies.

### Layer 2: Investigators (Intelligence)

**Tools Available:**

- `Read` - Read any file in repository
- `Grep` - Search for patterns across files
- `Glob` - Find files matching patterns
- `Bash` - Execute complex search operations

**Mission:** Determine if ambiguous errors are fixable or false positives.

**Full Autonomy Means:**

- Search current file for context
- Search entire repository for cross-references
- Read related files to understand intent
- Use any reasoning/logic needed
- Make the final determination

**Example Investigation Process:**

```text
Error: MD053 "Reference 'api-endpoint' not found" in config.md

Investigator thinks:
1. "Let me grep for [api-endpoint]: in config.md"
2. "Not found. Let me search all .md files"
3. "Found in setup.md:42. This is a cross-file reference"
4. "Verdict: false_positive - reference exists in setup.md"
```

**Report Format:**

```json
{
  "file": "config.md",
  "investigations": [
    {
      "error": {"line": 15, "code": "MD053", "message": "Reference 'api-endpoint' not found"},
      "verdict": "false_positive",
      "reasoning": "Reference defined in setup.md:42 as [api-endpoint]: https://..."
    },
    {
      "error": {"line": 23, "code": "MD033", "message": "Inline HTML [Element: b]"},
      "verdict": "fixable",
      "reasoning": "Accidental HTML in prose. Should use **bold** markdown syntax instead."
    }
  ]
}
```

### Layer 3: Fixers (Execution)

**Input Format:**

```json
{
  "files": [
    {
      "path": "config.md",
      "errors": [
        {
          "line": 23,
          "code": "MD033",
          "message": "Inline HTML [Element: b]",
          "context": "Accidental HTML in prose. Should use **bold** markdown syntax instead."
        },
        {
          "line": 45,
          "code": "MD013",
          "message": "Line too long (125/120)",
          "context": "Always fixable - wrap line at 120 characters"
        }
      ]
    }
  ]
}
```

**Task:**

1. Read file
2. Fix errors using provided context
3. Verify fixes with `rumdl check [file]`
4. Report completion

**Why context matters:** Without investigation reasoning, Fixers might re-investigate or make incorrect
assumptions about WHY errors are fixable.

## Error Triage Strategy

### Simple Errors (Directly Fixable)

These skip investigation and go straight to Fixers:

- **MD013** (Line length) → Always fixable, wrap at configured limit
- **MD036** (Emphasis instead of heading) → Always fixable, convert to proper heading
- **MD025** (Multiple H1s) → Always fixable, demote duplicate H1s

### Ambiguous Errors (Require Investigation)

These need Investigator autonomy:

- **MD033** (Inline HTML) → Intentional component or accidental markup?
- **MD053** (Reference unused) → Actually used in another file?
- **MD052** (Reference not found) → TOML section `[tools.uv]` or broken link?
- **MD041** (Missing H1) → Frontmatter present? Documentation pattern?

## Load Balancing: Greedy Bin-Packing

**Balance by ERROR COUNT, not file count.**

### Example Scenario

```text
Total: 100 errors across 10 files
├─ File A: 91 errors
├─ File B-J: 1 error each

Distribution (6 agents):
├─ Agent 1: File A (91 errors)
├─ Agent 2: Files B, C (2 errors)
├─ Agent 3: Files D, E (2 errors)
├─ Agent 4: Files F, G (2 errors)
├─ Agent 5: Files H, I (2 errors)
└─ Agent 6: File J (1 error)
```

### Algorithm

```python
def distribute_workload(files, max_agents=6):
    """
    Greedy bin-packing: assign each file to least-loaded agent.

    Args:
        files: List of {path, error_count, errors}
        max_agents: Maximum agents to spawn

    Returns:
        List of agent assignments with balanced workload
    """
    agents = [[] for _ in range(max_agents)]
    workloads = [0] * max_agents

    # Sort files by error_count descending (largest first)
    sorted_files = sorted(files, key=lambda f: f['error_count'], reverse=True)

    for file_info in sorted_files:
        # Find agent with minimum current workload
        min_idx = workloads.index(min(workloads))

        # Assign file to that agent
        agents[min_idx].append(file_info)

        # Update workload
        workloads[min_idx] += file_info['error_count']

    return agents
```

## Wave System: Adaptive Recovery

### Wave 1 (Initial Execution)

```text
1. Distribute work across up to 6 agents
2. Spawn all agents in parallel (single message, multiple Task calls)
3. Wait for completion
```

### Wave 2+ (Sequential Recovery)

**After Wave 1, Orchestrator assesses:**

**Scenario A - Perfect Completion:**

```text
All 6 agents: ✅ Completed successfully
Result: No Wave 2 needed
```

**Scenario B - Partial Failure:**

```text
Agent 1: ✅ Completed (15 errors)
Agent 2: ✅ Completed (17 errors)
Agent 3: ❌ Failed/timeout (12 errors NOT done)
Agent 4: ✅ Completed (14 errors)
Agent 5: ⚠️ Partial (10/18 errors done, 8 incomplete)
Agent 6: ✅ Completed (16 errors)

Orchestrator decides:
├─ Spawn 1 Investigator for Agent 3's 12 errors
└─ Spawn 1 Investigator for Agent 5's 8 incomplete errors

Wave 2: 2 agents (not 6)
```

**Key:** Orchestrator has autonomy to decide recovery strategy (1:1, N:M, or other) based on actual failures.

### Why Sequential Waves?

**Alternative considered:** Spawn all waves upfront (parallel)

```text
Total: 100 errors to investigate
Math: 100 ÷ 6 = 16.7 per agent (over threshold)
Action: Spawn Wave 1 (6 agents) + Wave 2 (6 agents) upfront
```

**Rejected because:** This is just "spawn 12 agents" with extra steps. True waves mean **wait and adapt**
based on actual results.

## Agent Contracts

### Investigator Assignment

```json
{
  "assignment": [
    {
      "file": "config.md",
      "errors": [
        {
          "line": 15,
          "code": "MD053",
          "message": "Reference 'api' not found"
        },
        {
          "line": 23,
          "code": "MD033",
          "message": "Inline HTML [Element: tip]"
        }
      ]
    },
    {
      "file": "setup.md",
      "errors": [
        {
          "line": 8,
          "code": "MD041",
          "message": "First line in a file should be a top-level heading"
        }
      ]
    }
  ]
}
```

### Investigator Report

```json
{
  "investigations": [
    {
      "file": "config.md",
      "results": [
        {
          "error": {"line": 15, "code": "MD053", "message": "..."},
          "verdict": "false_positive",
          "reasoning": "Reference '[api]:' is defined in setup.md:42. Cross-file reference is valid."
        },
        {
          "error": {"line": 23, "code": "MD033", "message": "..."},
          "verdict": "fixable",
          "reasoning": "HTML <tip> element in prose paragraph. Not a documentation component. Should use markdown blockquote or emphasis."
        }
      ]
    },
    {
      "file": "setup.md",
      "results": [
        {
          "error": {"line": 8, "code": "MD041", "message": "..."},
          "verdict": "false_positive",
          "reasoning": "File has YAML frontmatter (lines 1-6). H1 starts at line 8 after frontmatter, which is standard pattern."
        }
      ]
    }
  ]
}
```

### Fixer Assignment

```json
{
  "assignment": [
    {
      "path": "config.md",
      "errors": [
        {
          "line": 23,
          "code": "MD033",
          "message": "Inline HTML [Element: tip]",
          "context": "HTML <tip> element in prose paragraph. Not a documentation component. Should use markdown blockquote or emphasis."
        },
        {
          "line": 45,
          "code": "MD013",
          "message": "Line too long (125/120)",
          "context": "Always fixable - wrap line at 120 characters preserving meaning"
        }
      ]
    }
  ]
}
```

### Fixer Report

```json
{
  "results": [
    {
      "path": "config.md",
      "fixed": 2,
      "errors_before": 2,
      "errors_after": 0,
      "verification": "rumdl check config.md - PASSED"
    }
  ]
}
```

## Complete Workflow Example

### Initial State

```text
Repository: 28 markdown files
Linting errors: 100 total
├─ MD013 (line length): 45 errors
├─ MD036 (emphasis): 15 errors
├─ MD033 (HTML): 18 errors (ambiguous)
├─ MD053 (reference unused): 12 errors (ambiguous)
├─ MD052 (reference not found): 8 errors (ambiguous)
└─ MD041 (missing H1): 2 errors (ambiguous)
```

### Step 1: Discovery & Triage

```text
Orchestrator runs: rumdl check .

Triage results:
├─ Simple (directly fixable): 60 errors
│   └─ MD013 (45) + MD036 (15)
│
└─ Ambiguous (needs investigation): 40 errors
    └─ MD033 (18) + MD053 (12) + MD052 (8) + MD041 (2)
    └─ Spread across 12 files
```

### Step 2: Investigation (Wave 1)

```text
Orchestrator distributes 40 ambiguous errors across 6 Investigators:

Agent 1: 7 errors (files: A, B)
Agent 2: 7 errors (files: C, D)
Agent 3: 7 errors (files: E, F)
Agent 4: 7 errors (files: G, H)
Agent 5: 6 errors (files: I, J)
Agent 6: 6 errors (files: K, L)

All spawn in parallel (single message, 6 Task calls)
```

### Step 3: Investigation Results

```text
Agent 1: ✅ 7 errors → 5 fixable, 2 false positives
Agent 2: ✅ 7 errors → 6 fixable, 1 false positive
Agent 3: ❌ Timeout (7 errors not investigated)
Agent 4: ✅ 7 errors → 4 fixable, 3 false positives
Agent 5: ✅ 6 errors → 6 fixable, 0 false positives
Agent 6: ✅ 6 errors → 3 fixable, 3 false positives

Aggregated:
├─ Investigated: 33 errors (missing 7 from Agent 3)
├─ Fixable: 24 errors
└─ False positives: 9 errors
```

### Step 4: Recovery (Wave 2)

```text
Orchestrator spawns Wave 2:
├─ 1 Investigator for Agent 3's 7 uninvestigated errors

Wave 2 result:
└─ 7 errors → 5 fixable, 2 false positives

Final investigation totals:
├─ Investigated: 40 errors
├─ Fixable: 29 errors
└─ False positives: 11 errors
```

### Step 5: Calculate Total Workload

```text
Simple errors (from Step 1): 60
Investigated fixable (from Step 4): 29
Total to fix: 89 errors
```

### Step 6: Fixing (Wave 1)

```text
Orchestrator distributes 89 errors across 6 Fixers:

Agent 1: 15 errors (files: A, B, C)
Agent 2: 15 errors (files: D, E)
Agent 3: 15 errors (files: F, G, H)
Agent 4: 15 errors (files: I, J)
Agent 5: 15 errors (files: K, L, M)
Agent 6: 14 errors (files: N, O)

All spawn in parallel
```

### Step 7: Fixing Results

```text
All Fixers: ✅ Completed successfully

Total fixed: 89 errors
False positives preserved: 11 errors
```

### Step 8: Verification

```text
Orchestrator runs: rumdl check .

Results:
├─ Errors before: 100
├─ Errors after: 11 (all false positives)
├─ Fix rate: 89% (89/100)
└─ Manual review: 0 (all false positives correctly identified)
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Three layers** | Separates strategy (Orchestrator), intelligence (Investigator), execution (Fixer) |
| **Full Investigator autonomy** | Regex can't handle context; Claude needs freedom to search/analyze |
| **Context flows to Fixers** | Prevents re-investigation and wrong decisions |
| **Load balance by error count** | Prevents one agent getting stuck with 91 errors while others have 1 |
| **Sequential waves** | Adaptive recovery, not just "spawn 12 agents with extra steps" |
| **Orchestrator decides recovery** | Autonomy to spawn 1:1 or N:M based on actual failures |
| **Investigators can read multiple files** | Critical for MD053 (references), MD052 (links), cross-file context |
| **Max 6 agents per wave** | Balance parallelism with API rate limits and coordination overhead |
| **Greedy bin-packing** | Proven algorithm for load balancing, simple and effective |

## Success Metrics

**Target:** 80% fix rate (vs 40% with regex)

- Zero manual review needed after running
- Handles context-dependent errors (MD033, MD053, MD052, MD041)
- Adaptive to new error patterns without code changes
- Accurate false positive detection (preserves intentional patterns)

## Implementation Phases

### Phase 1: MVP Orchestrator

- Discovery and triage
- Spawn single Investigator (no waves yet)
- Spawn single Fixer
- Verification
- **Goal:** Prove the three-layer concept works

### Phase 2: Parallel Agents

- Greedy bin-packing distribution
- Spawn multiple Investigators/Fixers in parallel
- **Goal:** Achieve performance at scale

### Phase 3: Adaptive Recovery

- Wave 2+ for failures/incomplete work
- Orchestrator autonomy for recovery decisions
- **Goal:** Robust production system

### Phase 4: Optimization

- Cost analysis and model selection (Haiku vs Sonnet)
- Batching strategies
- Caching investigation results
- **Goal:** Production-ready efficiency

## Related Work

- **Phase 1 regex approach:** `scripts/rumdl-parser.py` (current implementation)
- **Original ideas:** `docs/ideas/markdown-agent.md`, `docs/ideas/docs-maint-agent.md`
- **Current workflow:** `.claude/commands/fix-markdown-linting.md`

## Next Steps

1. **Document validation:** Review this architecture with stakeholders
2. **MVP implementation:** Build Phase 1 (Orchestrator + single agents)
3. **Test cases:** Create representative markdown files with known errors
4. **Iterate:** Refine based on real-world results

---

**This architecture replaces regex with intelligence.** The Orchestrator coordinates, Investigators think,
and Fixers execute—each with clear boundaries and autonomy.
