# Proposal: Orchestrator-Managed Pipeline State

## Context

The SubagentStop hook was removed from ansible-workflows due to a Claude Code bug where the mere presence of the hook breaks tool injection for all plugin-defined subagents (see [#13951](https://github.com/anthropics/claude-code/issues/13951)).

This document proposes an alternative architecture that moves state management from hooks to the orchestrator.

## Problem Statement

The original design relied on SubagentStop hooks to:

1. Validate that agents wrote their bundle files before completing
2. Update pipeline phase state after each agent
3. Determine and trigger the next agent in the pipeline

Without SubagentStop, we need an alternative approach that doesn't depend on per-agent lifecycle hooks.

## Proposed Solution: Orchestrator-Managed State

Move all state management logic into the ansible-orchestrator agent. The orchestrator becomes the single source of truth for pipeline state.

### Architecture

```text
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                  ansible-orchestrator                    │
│                                                          │
│  1. Read/create state file                               │
│  2. Dispatch agent (generator/validator/debugger/etc)    │
│  3. Wait for agent completion                            │
│  4. Check bundle file exists                             │
│  5. Parse bundle for results (pass/fail)                 │
│  6. Update state file                                    │
│  7. Decide next action (next agent or complete)          │
│  8. Loop to step 2 or exit                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Key Changes

| Component | Before (Hook-Based) | After (Orchestrator-Managed) |
|-----------|---------------------|------------------------------|
| State updates | SubagentStop hook | Orchestrator after each dispatch |
| Bundle validation | Hook checks file exists | Orchestrator checks file exists |
| Next agent decision | Hook updates current_agent | Orchestrator reads bundle, decides |
| Error handling | Hook blocks agent stop | Orchestrator retries or escalates |

### Implementation Details

#### State File Format (unchanged)

```yaml
---
active: true
pipeline_phase: validating
current_agent: ansible-validator
task_description: "Create Docker deployment role"
validation_attempts: 1
last_validation_passed: false
---

[2025-12-14 03:00:00 UTC] Pipeline started
[2025-12-14 03:01:00 UTC] ansible-generator completed -> validating
```

#### Orchestrator Logic

```python
# Pseudocode for orchestrator flow
def run_pipeline(task_description):
    state = load_or_create_state(task_description)

    while state.active:
        agent = state.current_agent

        # Dispatch agent
        result = dispatch_agent(agent, get_bundle_context())

        # Validate bundle was written
        bundle_path = get_bundle_path(agent)
        if not bundle_path.exists():
            # Agent didn't write bundle - error or retry
            handle_missing_bundle(agent)
            continue

        # Parse bundle for results
        bundle = parse_bundle(bundle_path)

        # Determine next phase
        next_phase = determine_next_phase(agent, bundle)

        # Update state
        state.pipeline_phase = next_phase
        state.current_agent = get_agent_for_phase(next_phase)

        if next_phase == "complete":
            state.active = False

        save_state(state)

    return "Pipeline complete"
```

### Benefits

1. **Simpler architecture**: No hook coordination, single control flow
2. **Better error handling**: Orchestrator can retry, skip, or escalate
3. **Full context**: Orchestrator knows the task, history, and can make informed decisions
4. **No Claude Code bugs**: Avoids SubagentStop and related hook issues
5. **Easier debugging**: All logic in one place, easier to trace

### Drawbacks

1. **Orchestrator complexity**: More logic in the orchestrator agent
2. **Sequential only**: Can't easily parallelize agents (but this was true before)
3. **Agent independence**: Agents must trust orchestrator to manage state

## Affected Files

| File | Change |
|------|--------|
| `.claude/agents/ansible-orchestrator.md` | Add state management logic |
| `hooks/hooks.json` | Keep only Stop hook (already done) |
| `hooks/subagent-complete.py` | Delete or archive |
| `.claude/commands/*.md` | Update to use new orchestrator flow |

## Migration Path

1. Update ansible-orchestrator agent with state management logic
2. Test end-to-end pipeline without SubagentStop
3. Archive subagent-complete.py (keep for reference)
4. Update documentation

## Open Questions

1. Should the orchestrator be a single long-running agent or dispatch itself recursively?
2. How to handle orchestrator crashes mid-pipeline? (State file provides recovery point)
3. Should bundle validation be strict (block) or advisory (warn and continue)?

## Related

- Bug report: [bugs/subagent-stop-breaks-plugin-agents.md](../bugs/subagent-stop-breaks-plugin-agents.md)
- GitHub issue: [#13951](https://github.com/anthropics/claude-code/issues/13951)
- Original design: [plans/fuzzy-weaving-hedgehog.md](../plans/fuzzy-weaving-hedgehog.md)
