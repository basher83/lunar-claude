# Plan: ansible-workflows Plugin Integration Enhancement

## Objective

Enhance the ansible-workflows plugin with proper state tracking, hooks, and context bundles to support robust multi-agent pipeline orchestration.

## Current State

The plugin has:
- 4 agents: ansible-generator, ansible-validator, ansible-reviewer, ansible-debugger
- 4 commands: create-role, create-playbook, lint, analyze
- 8 skills: fundamentals, playbook-design, role-design, idempotency, secrets, error-handling, testing, proxmox
- .gitignore prepared for `*.local.md` files

Missing:
- No `hooks/` directory or hooks.json
- No state file implementation (`.claude/ansible-workflows.local.md`)
- No context bundle pattern between agents
- Agent handoff instructions assume sub-agents can spawn sub-agents (they cannot)

## Key Insight

Sub-agents cannot spawn other sub-agents. The main Claude Code session is the orchestrator. The "hand off to validator" instruction in agents is guidance for the MAIN SESSION, not an executable action by the sub-agent.

## Research Validation (lunar-research, confidence: 0.85)

**Validated patterns:**
- ✅ Stop hook for pipeline completion validation
- ✅ `.local.md` files with YAML frontmatter for state (documented pattern)
- ✅ Command hooks with Python scripts (hookify pattern)
- ✅ `${CLAUDE_PLUGIN_ROOT}` for portable paths
- ✅ Agent handoffs with "path, files created, context"

**New insight - SubagentStop:**
A dedicated `SubagentStop` hook event exists for validating subagent completion. Consider using this instead of/in addition to Stop hook for per-agent validation.

**Gotchas from research:**
- Hooks execute in parallel within same event - design for independence
- Hook changes require Claude Code restart
- Use `session_id` from hook input for state files (not $$)
- Exit code 0 = success, exit code 2 = blocking error

**Gaps we address:**
- "No standardized format for pipeline state files" → Our state file structure
- "No built-in retry mechanisms" → Our validation_attempts counter

## Reference Patterns

From hookify plugin:
- hooks.json delegates to Python scripts with 10s timeout
- Python scripts read stdin JSON, output JSON to stdout, always exit 0
- State files use `.claude/hookify.*.local.md` with YAML frontmatter
- config_loader.py parses frontmatter and message body

From multi-agent-swarm:
- State file tracks: agent_name, task_number, coordinator_session, enabled
- Stop hook reads state and sends notifications
- Each agent session has its own state file

---

## Implementation Design

### Architecture Overview

Three interconnected components:

1. **State File** (`.claude/ansible-workflows.local.md`) - Tracks pipeline phase, target, attempts
2. **Context Bundles** (`.claude/ansible-workflows.*.bundle.md`) - Agent outputs for next agent
3. **Stop Hook** (`hooks/check-pipeline-state.py`) - Reminds main session to continue pipeline

### Files to Create

#### 1. `hooks/hooks.json`

```json
{
  "description": "Ansible workflows pipeline state management",
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/subagent-complete.py",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/check-pipeline-state.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

#### 2. `hooks/subagent-complete.py` (NEW)

Python script for per-agent validation:
- Read JSON from stdin (includes which subagent just completed)
- Check if this was an ansible-* agent
- Validate agent wrote its context bundle
- Update state file with current phase
- Output JSON to stdout (can add system message about next steps)
- Always exit 0

#### 3. `hooks/check-pipeline-state.py`

Python script for session stop validation:
- Read JSON from stdin
- Check for `.claude/ansible-workflows.local.md`
- If active pipeline, block stop with instructions for next agent
- Output JSON to stdout
- Always exit 0

Key function: Map pipeline_phase to next_agent:
- scaffolding → ansible-generator
- generating → ansible-validator
- validating → ansible-reviewer (if passed) / ansible-debugger (if failed)
- debugging → ansible-validator
- reviewing → complete

### State File Structure

`.claude/ansible-workflows.local.md`:

```yaml
---
active: true
pipeline_phase: generating
target_path: ansible/playbooks/setup-docker.yml
current_agent: ansible-generator
started_at: "2024-01-15T10:30:00Z"
validation_attempts: 0
last_validation_passed: true
---

# Pipeline State

[Human-readable status and notes]
```

### Context Bundle Structure

`.claude/ansible-workflows.<phase>.bundle.md`:

```yaml
---
source_agent: ansible-generator
target_agent: ansible-validator
timestamp: "2024-01-15T10:35:00Z"
target_path: ansible/playbooks/setup-docker.yml
---

# Generator Output Bundle

## Files Created
- [list of files]

## Validation Command
[command to run]

## Specific Concerns
[any flags for next agent]
```

Bundle naming:
- `.scaffolding.bundle.md` - Command → Generator
- `.generating.bundle.md` - Generator → Validator
- `.validating.bundle.md` - Validator → Reviewer/Debugger
- `.debugging.bundle.md` - Debugger → Validator

### Files to Modify

#### Commands (Initialize Pipeline)

**commands/create-playbook.md** and **commands/create-role.md**:
- Create state file with `active: true`, `pipeline_phase: scaffolding`
- Write scaffolding bundle with target path and user requirements
- Update state to `pipeline_phase: generating`
- Hand off to ansible-generator

#### Agents (Read/Write Bundles)

**agents/ansible-generator.md**:
- Read scaffolding bundle if exists
- Write generating bundle with files created, patterns applied, concerns
- Update state to `pipeline_phase: validating`

**agents/ansible-validator.md**:
- Read generating or debugging bundle
- On PASS: Write validating bundle, update state to `reviewing`
- On FAIL: Write validating bundle with errors, update state to `debugging`

**agents/ansible-debugger.md**:
- Read validating bundle for error list
- Apply fixes
- Write debugging bundle with fixes summary
- Update state to `validating`, increment attempts
- Check retry limit (max 3)

**agents/ansible-reviewer.md**:
- Read validating bundle
- On APPROVED: Set `active: false`, pipeline complete
- On NEEDS_REWORK: Write reviewing bundle, hand to debugger

#### Update .gitignore

Add `*.bundle.md` pattern (already has `*.local.md`)

### Implementation Order

1. Create `hooks/hooks.json`
2. Create `hooks/subagent-complete.py`
3. Create `hooks/check-pipeline-state.py`
4. Update `commands/create-playbook.md`
5. Update `commands/create-role.md`
6. Update `agents/ansible-generator.md`
7. Update `agents/ansible-validator.md`
8. Update `agents/ansible-debugger.md`
9. Update `agents/ansible-reviewer.md`
10. Update `.gitignore`

### Critical Files

| File | Action | Purpose |
|------|--------|---------|
| `hooks/hooks.json` | Create | Register SubagentStop + Stop hooks |
| `hooks/subagent-complete.py` | Create | Per-agent completion validation |
| `hooks/check-pipeline-state.py` | Create | Session stop pipeline reminder |
| `commands/create-playbook.md` | Modify | Initialize state |
| `commands/create-role.md` | Modify | Initialize state |
| `agents/ansible-generator.md` | Modify | Bundle read/write |
| `agents/ansible-validator.md` | Modify | Bundle read/write |
| `agents/ansible-debugger.md` | Modify | Bundle read/write |
| `agents/ansible-reviewer.md` | Modify | Bundle read/write, complete |
| `.gitignore` | Modify | Add bundle pattern |

### Testing Scenarios

1. **Happy path**: create-playbook → generator → validator (PASS) → reviewer (APPROVED)
2. **Validation failure**: generator → validator (FAIL) → debugger → validator (PASS)
3. **Review rejection**: validator (PASS) → reviewer (NEEDS_REWORK) → debugger
4. **Stop hook test**: Interrupt mid-pipeline, verify block message
5. **Max retries**: 3 validation failures → escalate to user
