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
