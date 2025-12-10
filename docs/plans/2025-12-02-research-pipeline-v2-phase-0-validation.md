# Research Pipeline v2 - Phase 0 Validation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Validate critical assumptions before committing to 80-100 hour Research Pipeline v2 build.

**Architecture:** Five focused validation experiments testing parallel execution, schema validation, multi-agent quality, cache lookup, and user need. Each produces a concrete go/no-go signal.

**Tech Stack:** Claude Code Task tool, Python (jsonschema), MCP tools (Firecrawl, GitHub), markdown files for cache simulation

**Time Budget:** 8 hours total

**Decision Point:** After Phase 0, if 4/5 validations pass → proceed with hybrid MVP. If <4 pass → pivot to simpler architecture.

---

## Task 1: Parallel Agent Dispatch PoC

**Time:** 2 hours
**Success Criteria:** Demonstrate 2× speedup with parallel agents vs sequential

**Files:**

- Create: `.claude/commands/research-validation/parallel-poc.md`
- Create: `docs/plans/phase-0-results/parallel-dispatch-results.md`

**Step 1: Create minimal parallel dispatch command**

Create `.claude/commands/research-validation/parallel-poc.md`:

```markdown
---
description: Test parallel agent dispatch timing
---

# Parallel Dispatch PoC

## Purpose

Test whether Claude Code's Task tool supports true parallel execution with measurable time savings.

## Instructions

1. Record start time
2. Launch 2 agents in PARALLEL (single message, multiple Task tool calls)
3. Each agent performs a 10-second simulated task (web fetch + processing)
4. Record end time
5. Calculate: parallel time vs expected sequential time (20s)

## Workflow

### Test 1: Parallel Execution

Launch both agents in ONE message:

**Agent A:**
```text
subagent_type: general-purpose
description: Agent A - web research

Prompt:
1. Use WebSearch to search for "Claude Code parallel agents"
2. Read the first result
3. Summarize in 2 sentences
4. Return: "Agent A complete: [summary]"
```

**Agent B:**
```text
subagent_type: general-purpose
description: Agent B - web research

Prompt:
1. Use WebSearch to search for "multi-agent orchestration patterns"
2. Read the first result
3. Summarize in 2 sentences
4. Return: "Agent B complete: [summary]"
```

### Test 2: Sequential Baseline (for comparison)

Run same two searches sequentially (one after the other) and record time.

## Output

Record results in `docs/plans/phase-0-results/parallel-dispatch-results.md`:

- Parallel execution time: [X seconds]
- Sequential execution time: [Y seconds]
- Speedup ratio: [Y/X]
- Go/No-Go: [PASS if speedup > 1.5x, FAIL otherwise]
```sql

**Step 2: Create results directory**

```bash
mkdir -p docs/plans/phase-0-results
```

**Step 3: Execute the PoC command**

Run: `/research-validation:parallel-poc`

**Step 4: Record results**

Create `docs/plans/phase-0-results/parallel-dispatch-results.md` with actual timing data.

**Step 5: Commit**

```bash
git add .claude/commands/research-validation/ docs/plans/phase-0-results/
git commit -m "feat(phase-0): add parallel dispatch PoC with results"
```

---

## Task 2: JSON Schema Validation Tooling

**Time:** 1 hour
**Success Criteria:** Identify validation tool accessible to Claude agents with working example

**Files:**

- Create: `scripts/validate_research_schema.py`
- Create: `docs/plans/phase-0-results/schema-validation-results.md`

**Step 1: Create Python validation script**

Create `scripts/validate_research_schema.py`:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.20.0"]
# ///
"""
Validate research report JSON against schema.

Usage:
    uv run scripts/validate_research_schema.py <json_file>
    uv run scripts/validate_research_schema.py --test
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, ValidationError

# Research Report Schema (from design doc Task 1.1)
RESEARCH_REPORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["query", "source", "findings", "confidence", "timestamp"],
    "properties": {
        "query": {"type": "string", "minLength": 1},
        "source": {
            "type": "string",
            "enum": ["github", "tavily", "deepwiki", "exa"]
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "url", "summary", "relevance"],
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string", "format": "uri"},
                    "summary": {"type": "string"},
                    "relevance": {"type": "number", "minimum": 0, "maximum": 1},
                    "code_snippets": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "timestamp": {"type": "string", "format": "date-time"}
    }
}

def validate_report(json_data: dict) -> tuple[bool, list[str]]:
    """Validate JSON against research report schema."""
    validator = Draft7Validator(RESEARCH_REPORT_SCHEMA)
    errors = list(validator.iter_errors(json_data))

    if errors:
        error_messages = [f"{e.json_path}: {e.message}" for e in errors]
        return False, error_messages
    return True, []

def run_self_test() -> bool:
    """Run self-test with valid and invalid examples."""
    print("Running self-test...\n")

    # Valid example
    valid_report = {
        "query": "kubernetes deployment patterns",
        "source": "github",
        "findings": [
            {
                "title": "K8s Best Practices",
                "url": "https://github.com/example/k8s-patterns",
                "summary": "Production-ready Kubernetes patterns",
                "relevance": 0.95,
                "code_snippets": ["apiVersion: apps/v1"]
            }
        ],
        "confidence": 0.85,
        "timestamp": "2025-12-01T10:00:00Z"
    }

    is_valid, errors = validate_report(valid_report)
    print(f"Valid report test: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        print(f"  Errors: {errors}")

    # Invalid example (missing required field)
    invalid_report = {
        "query": "test",
        "source": "github",
        # missing: findings, confidence, timestamp
    }

    is_valid, errors = validate_report(invalid_report)
    print(f"Invalid report test: {'PASS' if not is_valid else 'FAIL'}")
    if not is_valid:
        print(f"  Caught errors: {len(errors)} validation errors (expected)")

    # Invalid enum
    invalid_source = {
        "query": "test",
        "source": "invalid_source",  # Not in enum
        "findings": [],
        "confidence": 0.5,
        "timestamp": "2025-12-01T10:00:00Z"
    }

    is_valid, errors = validate_report(invalid_source)
    print(f"Invalid source test: {'PASS' if not is_valid else 'FAIL'}")

    print("\nSelf-test complete.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/validate_research_schema.py <json_file>")
        print("       uv run scripts/validate_research_schema.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    is_valid, errors = validate_report(data)

    if is_valid:
        print(f"✓ Valid: {json_path}")
        sys.exit(0)
    else:
        print(f"✗ Invalid: {json_path}")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Step 2: Run self-test to verify script works**

```bash
uv run scripts/validate_research_schema.py --test
```

Expected output:

```text
Running self-test...

Valid report test: PASS
Invalid report test: PASS
  Caught errors: 3 validation errors (expected)
Invalid source test: PASS

Self-test complete.
```

**Step 3: Document results**

Create `docs/plans/phase-0-results/schema-validation-results.md`:

```markdown
# Schema Validation Results

**Tool:** Python jsonschema library (v4.20+)
**Integration:** UV script callable via `uv run scripts/validate_research_schema.py`

## Test Results

- Valid report validation: PASS
- Invalid report detection: PASS
- Enum constraint enforcement: PASS

## Integration Pattern

Claude agents can validate output by:
1. Write JSON to temp file
2. Run: `uv run scripts/validate_research_schema.py /tmp/report.json`
3. Check exit code (0 = valid, 1 = invalid)

## Go/No-Go

**PASS** - jsonschema library works, UV script pattern integrates with Claude agents
```

**Step 4: Commit**

```bash
git add scripts/validate_research_schema.py docs/plans/phase-0-results/schema-validation-results.md
git commit -m "feat(phase-0): add JSON schema validation script with self-test"
```

---

## Task 3: Multi-Agent vs Single-Agent Quality Test

**Time:** 3 hours
**Success Criteria:** Determine if 4-agent research provides measurably better results than single-agent

**Files:**

- Create: `docs/plans/phase-0-results/ab-test-queries.md`
- Create: `docs/plans/phase-0-results/ab-test-results.md`

**Step 1: Define test queries**

Create `docs/plans/phase-0-results/ab-test-queries.md`:

```markdown
# A/B Test Queries

## Query Selection Criteria

- Mix of simple and complex research tasks
- Relevant to lunar-claude homelab use cases
- Measurable quality dimensions

## Test Queries

1. **Simple Fact**: "What is the default port for Proxmox VE web interface?"
2. **How-To**: "How to configure cloud-init for Proxmox VM templates?"
3. **Comparison**: "Ansible vs Terraform for Proxmox infrastructure management"
4. **Best Practices**: "Production-ready Kubernetes on Proxmox with Ceph storage"
5. **Integration**: "NetBox integration with PowerDNS for automated DNS management"

## Evaluation Criteria (1-5 scale)

- **Completeness**: Does it answer the full question?
- **Accuracy**: Are the facts correct?
- **Actionability**: Can I implement this directly?
- **Source Quality**: Are sources authoritative and current?
- **Relevance**: Is it specific to my use case (homelab/infrastructure)?
```

**Step 2: Run single-agent baseline (5 queries)**

For each query, use a single Firecrawl search + Claude synthesis:

```bash
For query: "[query]"
1. WebSearch for the query
2. Read top 3 results
3. Synthesize into answer
4. Record time and quality scores
```

**Step 3: Run multi-agent version (5 queries)**

For each query, use 4 parallel searches (GitHub + Firecrawl + DeepWiki simulation + Exa simulation):

```text
For query: "[query]"
1. Launch 4 parallel searches (different sources)
2. Collect all results
3. Synthesize with cross-validation
4. Record time and quality scores
```

**Step 4: Blind evaluation**

Present both answers (A and B, randomized) without knowing which is single vs multi-agent.
Score each on the 5 criteria.

**Step 5: Document results**

Create `docs/plans/phase-0-results/ab-test-results.md`:

```markdown
# A/B Test Results: Multi-Agent vs Single-Agent Research

## Summary

| Query | Single-Agent Score | Multi-Agent Score | Winner |
|-------|-------------------|-------------------|--------|
| Q1: Proxmox port | X/25 | Y/25 | [A/B/Tie] |
| Q2: Cloud-init | X/25 | Y/25 | [A/B/Tie] |
| Q3: Ansible vs TF | X/25 | Y/25 | [A/B/Tie] |
| Q4: K8s on Proxmox | X/25 | Y/25 | [A/B/Tie] |
| Q5: NetBox + DNS | X/25 | Y/25 | [A/B/Tie] |
| **Average** | X/25 | Y/25 | **[Winner]** |

## Time Comparison

| Query | Single-Agent Time | Multi-Agent Time |
|-------|-------------------|------------------|
| Q1 | Xs | Ys |
| Q2 | Xs | Ys |
| Q3 | Xs | Ys |
| Q4 | Xs | Ys |
| Q5 | Xs | Ys |
| **Average** | Xs | Ys |

## Quality Breakdown

### Where Multi-Agent Won
- [specific advantages observed]

### Where Single-Agent Won
- [specific advantages observed]

### No Difference
- [query types where results were equivalent]

## Go/No-Go

**[PASS/FAIL]** - Multi-agent provides [X%] quality improvement, justifying [Y%] additional complexity

## Recommendation

[Based on results: proceed with 4 agents / reduce to 2 agents / use single agent with caching]
```

**Step 6: Commit**

```bash
git add docs/plans/phase-0-results/ab-test-*.md
git commit -m "feat(phase-0): add multi-agent vs single-agent A/B test results"
```

---

## Task 4: Cache Lookup Precision Test

**Time:** 1 hour
**Success Criteria:** Cache lookup achieves >70% precision with tag-based matching

**Files:**

- Create: `docs/plans/phase-0-results/cache-test-data.md`
- Create: `docs/plans/phase-0-results/cache-precision-results.md`

**Step 1: Create test cache entries**

Create `docs/plans/phase-0-results/cache-test-data.md`:

```markdown
# Cache Test Data

## Simulated Cache Entries

### Entry 1: proxmox-cloud-init.md
```yaml
---
query: "Proxmox cloud-init template configuration"
tags: [proxmox, cloud-init, vm-templates, infrastructure]
confidence: 0.85
date: 2025-11-15
---
```

### Entry 2: ansible-proxmox-automation.md
```yaml
---
query: "Ansible automation for Proxmox cluster"
tags: [ansible, proxmox, automation, infrastructure, iac]
confidence: 0.90
date: 2025-11-20
---
```

### Entry 3: kubernetes-ceph-storage.md
```yaml
---
query: "Kubernetes persistent storage with Ceph"
tags: [kubernetes, ceph, storage, k8s, persistent-volumes]
confidence: 0.88
date: 2025-11-10
---
```

### Entry 4: netbox-dns-integration.md
```yaml
---
query: "NetBox PowerDNS integration for IPAM"
tags: [netbox, powerdns, dns, ipam, automation]
confidence: 0.82
date: 2025-11-25
---
```

### Entry 5: terraform-proxmox-provider.md
```yaml
---
query: "Terraform Proxmox provider VM provisioning"
tags: [terraform, proxmox, iac, vm-provisioning, infrastructure]
confidence: 0.87
date: 2025-11-18
---
```

## Test Queries

| Query | Expected Match | Match Type |
|-------|---------------|------------|
| "cloud-init for Proxmox VMs" | Entry 1 | Direct |
| "Proxmox automation with Ansible" | Entry 2 | Direct |
| "Ceph storage for K8s" | Entry 3 | Direct |
| "DNS automation with NetBox" | Entry 4 | Direct |
| "Terraform infrastructure on Proxmox" | Entry 5 | Direct |
| "VM templates in Proxmox" | Entry 1 | Semantic |
| "Infrastructure as Code for virtualization" | Entry 2 or 5 | Semantic |
| "Container storage solutions" | Entry 3 | Semantic |
| "IPAM and DNS management" | Entry 4 | Semantic |
| "Homelab automation" | Multiple | Broad |
```bash

**Step 2: Implement simple cache lookup**

Test with grep-based tag matching:

```bash
# For query "cloud-init for Proxmox VMs"
# Extract keywords: cloud-init, proxmox, vms
# Search cache entries for tag overlap

grep -l "cloud-init\|proxmox" docs/plans/phase-0-results/cache-test-data.md
```

**Step 3: Score precision**

For each test query:

1. Run cache lookup
2. Record: Did it find the expected entry?
3. Record: Did it return false positives?

**Step 4: Document results**

Create `docs/plans/phase-0-results/cache-precision-results.md`:

```markdown
# Cache Precision Test Results

## Methodology

- 10 test queries against 5 cache entries
- Tag-based matching with keyword extraction
- Scored: True Positive, False Positive, False Negative

## Results

| Query | Expected | Found | Result |
|-------|----------|-------|--------|
| Q1 | Entry 1 | [actual] | TP/FP/FN |
| Q2 | Entry 2 | [actual] | TP/FP/FN |
| ... | ... | ... | ... |

## Metrics

- **Precision**: TP / (TP + FP) = X%
- **Recall**: TP / (TP + FN) = X%
- **F1 Score**: 2 * (P * R) / (P + R) = X%

## Go/No-Go

**[PASS/FAIL]** - Precision [X%] [meets/does not meet] >70% threshold

## Recommendations

- [Keep simple tag matching / Add embedding-based similarity / Hybrid approach]
```

**Step 5: Commit**

```bash
git add docs/plans/phase-0-results/cache-*.md
git commit -m "feat(phase-0): add cache precision test with results"
```

---

## Task 5: User Validation Interviews

**Time:** 1 hour
**Success Criteria:** 2+ users confirm research system would be valuable

**Files:**

- Create: `docs/plans/phase-0-results/user-validation-results.md`

**Step 1: Define interview questions**

Questions to ask potential users:

1. How often do you research technical topics for your projects?
2. What's your current research workflow? (Tools, time spent)
3. What are your biggest pain points with technical research?
4. Would a cached, multi-source research system save you time?
5. What would make you actually use this vs. ChatGPT/Perplexity?
6. What's the minimum quality bar for research results?

**Step 2: Conduct interviews**

Interview 2-3 potential users (can be self-reflection if solo project):

- User 1: [Name/Role]
- User 2: [Name/Role]

**Step 3: Document results**

Create `docs/plans/phase-0-results/user-validation-results.md`:

```markdown
# User Validation Results

## Interview Summary

### User 1: [Name/Role]

**Research Frequency:** [daily/weekly/monthly]
**Current Workflow:** [description]
**Pain Points:**
- [pain point 1]
- [pain point 2]

**Would Use Research Pipeline:** [Yes/No/Maybe]
**Key Requirements:**
- [requirement 1]
- [requirement 2]

### User 2: [Name/Role]

[Same structure]

## Synthesis

### Common Pain Points
- [shared pain point 1]
- [shared pain point 2]

### Must-Have Features
- [feature 1]
- [feature 2]

### Nice-to-Have Features
- [feature 1]

### Dealbreakers
- [what would prevent adoption]

## Go/No-Go

**[PASS/FAIL]** - [X/2] users would use this system

## Recommendations

- [Adjust scope based on feedback]
- [Prioritize features based on user needs]
```

**Step 4: Commit**

```bash
git add docs/plans/phase-0-results/user-validation-results.md
git commit -m "feat(phase-0): add user validation interview results"
```

---

## Phase 0 Decision Point

**After completing all 5 tasks, create final decision document:**

Create `docs/plans/phase-0-results/DECISION.md`:

```markdown
# Phase 0 Validation Decision

**Date:** YYYY-MM-DD
**Total Time Spent:** X hours

## Validation Results

| Task | Result | Go/No-Go |
|------|--------|----------|
| 1. Parallel Dispatch PoC | [speedup ratio] | [PASS/FAIL] |
| 2. Schema Validation | [tool identified] | [PASS/FAIL] |
| 3. A/B Quality Test | [quality delta] | [PASS/FAIL] |
| 4. Cache Precision | [precision %] | [PASS/FAIL] |
| 5. User Validation | [users confirmed] | [PASS/FAIL] |

**Overall:** [X/5] validations passed

## Decision

### If 4-5 PASS: Proceed with Hybrid MVP

- Start with 2 agents (GitHub + Tavily)
- Integrate M2 Deep Research synthesis patterns
- Build Claude Code wrapper + cache layer
- Target: 40 hours for 80% value

### If 2-3 PASS: Proceed with Reduced Scope

- Single agent with aggressive caching
- Focus on codebase contextualization as differentiator
- Target: 20 hours for MVP

### If 0-1 PASS: Pivot

- Abandon multi-agent approach
- Consider: Enhanced single-agent with memory
- Consider: Integration with existing tool (Perplexity API)

## Chosen Path

**[Decision]**: [Rationale based on results]

## Next Steps

1. [Immediate next action]
2. [Following action]
3. [Timeline adjustment if needed]
```

**Final Commit:**

```bash
git add docs/plans/phase-0-results/DECISION.md
git commit -m "feat(phase-0): add final validation decision document"
```

---

## Summary

| Task | Time | Deliverable |
|------|------|-------------|
| 1. Parallel Dispatch PoC | 2h | Timing measurements, go/no-go |
| 2. Schema Validation | 1h | Working UV script, integration pattern |
| 3. A/B Quality Test | 3h | Quality scores, recommendation |
| 4. Cache Precision | 1h | Precision metrics, algorithm choice |
| 5. User Validation | 1h | Interview results, requirements |
| **Total** | **8h** | **Decision document** |

**After Phase 0:** Clear go/no-go decision with evidence, not assumptions.
