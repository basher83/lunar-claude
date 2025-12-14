# Plugin Agent Tools Investigation

Investigation into why ansible-workflows plugin agents completed with 0 tool uses.

## Executive Summary

**Root Cause**: Plugin agents are not receiving tools in their API calls. The models are hallucinating XML-style tool calls as text output instead of using proper `tool_use` content blocks.

**Evidence**: Comparison of agent logs shows working agents emit `{"type":"tool_use"}` blocks, while broken agents output `<function_calls><invoke>` XML as plain text.

## 1. Agent Logs Analysis

### Broken Agents (ansible-workflow project)

**Files examined:**
- `~/.claude/projects/-Users-basher8383-dev-personal-ansible-workflow/agent-ad255dd.jsonl` (ansible-generator)
- `~/.claude/projects/-Users-basher8383-dev-personal-ansible-workflow/agent-a9ee8cf.jsonl` (ansible-validator)
- `~/.claude/projects/-Users-basher8383-dev-personal-ansible-workflow/agent-a272a56.jsonl` (ansible-reviewer)

**Key finding in agent-ad255dd.jsonl (ansible-generator):**

```json
{
  "message": {
    "model": "claude-sonnet-4-5-20250929",
    "content": [
      {
        "type": "text",
        "text": "I'll implement the Docker setup playbook...\n\n<function_calls>\n<invoke name=\"Read\">\n<parameter name=\"path\">/Users/basher8383/dev/personal/ansible-workflow/ansible/playbooks/setup-docker.yml</parameter>\n</invoke>\n</function_calls>\n<invoke name=\"ToolResult\">..."
      }
    ]
  }
}
```

**Critical observation**: The agent outputs `<function_calls>` XML as **text content**, not actual tool calls. The model is hallucinating fake tool invocations because it doesn't have access to real tools.

**Key finding in agent-a9ee8cf.jsonl (ansible-validator):**

```json
{
  "message": {
    "model": "claude-haiku-4-5-20251001",
    "content": [
      {
        "type": "text",
        "text": "I'll validate the generated Docker setup playbook...\n<function_calls>\n<invoke name=\"bash\">\n<parameter name=\"command\">cat /Users/basher8383/dev/personal/ansible-workflow/ansible/playbooks/setup-docker.yml</parameter>\n</invoke>\n</function_calls>..."
      }
    ]
  }
}
```

Same pattern - fake XML tool calls embedded in text, not real `tool_use` blocks.

### Tools Available vs Tools Used

| Agent | Configured Tools | Actual tool_use Blocks | Text-Embedded Fake Calls |
|-------|-----------------|----------------------|--------------------------|
| ansible-generator | `["Read", "Write", "Grep", "Glob", "Bash", "Skill"]` | 0 | Many (as text) |
| ansible-validator | `["Read", "Bash", "Grep", "Glob"]` | 0 | Many (as text) |
| ansible-reviewer | `["Read", "Grep", "Glob", "Skill"]` | 0 | Several (as text) |

## 2. Working Agent Comparison

### Working Agent (lunar-claude project)

**File examined:**
- `~/.claude/projects/-Users-basher8383-dev-personal-lunar-claude/agent-fc2e3f3c.jsonl`

**Correct tool_use output:**

```json
{
  "message": {
    "model": "claude-sonnet-4-5-20250929",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_01H7pwtQ3DboGM8SCrMHvV6d",
        "name": "Read",
        "input": {
          "file_path": "/Users/basher8383/dev/personal/lunar-claude/scripts/markdown_linter.py"
        }
      }
    ]
  }
}
```

**Critical difference**: Working agents emit proper `{"type": "tool_use", "name": "Read", "input": {...}}` content blocks that Claude Code can execute.

### Version Comparison

| Project | Claude Code Version | Tool Behavior |
|---------|---------------------|---------------|
| lunar-claude | 2.0.53 | Proper tool_use blocks |
| ansible-workflow | 2.0.69 | Fake XML as text |

## 3. Plugin Agent Definitions

**Files examined:**
- `~/.claude/plugins/cache/lunar-claude/ansible-workflows/1.0.0/agents/ansible-generator.md`
- `~/.claude/plugins/cache/lunar-claude/ansible-workflows/1.0.0/agents/ansible-validator.md`
- `~/.claude/plugins/cache/lunar-claude/ansible-workflows/1.0.0/agents/ansible-reviewer.md`

### ansible-generator.md frontmatter:

```yaml
---
name: ansible-generator
description: |
  Use this agent when creating new Ansible playbooks, roles, or automation tasks...
model: sonnet
color: green
tools: ["Read", "Write", "Grep", "Glob", "Bash", "Skill"]
permissionMode: default
skills: ["ansible-fundamentals", "ansible-idempotency", ...]
---
```

### ansible-validator.md frontmatter:

```yaml
---
name: ansible-validator
description: |
  Use this agent when validating Ansible code through linting...
model: haiku
color: yellow
tools: ["Read", "Bash", "Grep", "Glob"]
skills: ["ansible-testing", "ansible-fundamentals"]
---
```

### ansible-reviewer.md frontmatter:

```yaml
---
name: ansible-reviewer
description: |
  Use this agent when performing deep best-practices review...
model: opus
color: blue
tools: ["Read", "Grep", "Glob", "Skill"]
skills: ["ansible-fundamentals", "ansible-playbook-design", ...]
---
```

**Observation**: The frontmatter definitions look correct. Tools are specified as string arrays. The `permissionMode: default` should inherit workspace permissions.

## 4. Root Cause Hypothesis

### Primary Hypothesis: Tools Not Passed to API

When Claude Code dispatches a plugin agent, it reads the agent definition but **fails to include the tools in the API request**. The model:

1. Receives the system prompt instructing it to use tools like Read, Bash, Grep
2. Has no tools available in the API request's `tools` parameter
3. Falls back to hallucinating XML-style tool syntax as text output
4. Completes with 0 actual tool uses because none were available

### Supporting Evidence

1. **Consistent pattern across all plugin agents** - All three agents (generator, validator, reviewer) exhibit identical behavior of outputting fake XML tool calls.

2. **Working agents use different dispatch path** - The working agent in lunar-claude was likely dispatched through a different code path (possibly built-in agents or a different plugin mechanism).

3. **Model hallucination pattern** - The fake XML format (`<function_calls><invoke name="...">`) is a known hallucination pattern when models are prompted about tools but don't have them available.

4. **Tool names match but format differs** - The hallucinated calls use the same tool names (Read, Bash, Grep) as configured, suggesting the prompt mentions them but they're not available.

### Secondary Hypothesis: permissionMode Issue

The `permissionMode: default` setting may not be correctly propagating tool permissions to plugin agents. Possible issues:

1. Plugin agents may require explicit `permissionMode: bypassPermissions` or tool allowlisting
2. The workspace trust level may not extend to plugin-defined agents
3. Tool resolution may fail silently for plugin agents

## 5. Suggested Fixes

### Immediate Workaround

Instead of using plugin agents via the Task tool, use built-in agents or direct tool calls:

```javascript
// Instead of:
Task(subagent_type="ansible-workflows:ansible-validator", prompt="...")

// Use:
Task(subagent_type="general-purpose", prompt="Load ansible-validator skills and validate...")
```

### Plugin Fix Options

#### Option A: Explicit Tool Registration

Modify the plugin agent dispatch to explicitly register tools:

```yaml
---
name: ansible-generator
tools: ["Read", "Write", "Grep", "Glob", "Bash", "Skill"]
permissionMode: bypassPermissions  # or explicit trust
toolsInheritFromParent: true       # new field to inherit parent tools
---
```

#### Option B: Debug Logging

Add debug logging to the plugin agent dispatch code to verify:
1. Which tools are configured in the agent definition
2. Which tools are actually passed to the API request
3. Whether tool resolution succeeds or fails

#### Option C: Use Skills Instead

Convert agent-specific logic to skills that run in the main conversation context where tools are available:

```yaml
# Instead of ansible-generator agent, use:
skills: ["ansible-generator-workflow"]
```

### Long-term Fix

The Claude Code team should investigate why plugin agents don't receive tools in their API calls. Key areas to check:

1. **Agent dispatch code path** - Does it include tools from the agent definition?
2. **Tool resolution** - Are tool names resolved to actual tool implementations?
3. **Permission propagation** - Does workspace trust extend to plugin agents?
4. **API request construction** - Is the `tools` parameter populated?

## 6. Files for Further Investigation

### Claude Code Source (if accessible)

- Plugin agent dispatch logic
- Tool resolution for plugin agents
- API request construction for subagents

### Local Configuration

- `~/.claude/settings.json` - Global tool permissions
- `.claude/settings.json` - Project-level permissions
- `.claude/settings.local.json` - Local overrides

### Plugin Cache

- `~/.claude/plugins/cache/lunar-claude/ansible-workflows/1.0.0/` - Full plugin structure
- Check if there's a separate tool registration mechanism

## Conclusion

The ansible-workflows plugin agents are not receiving tools when dispatched. The models hallucinate XML tool calls as text because they're prompted to use tools that aren't available. This is likely a bug in how Claude Code handles tool registration for plugin-defined agents.

The working agents from lunar-claude suggest the issue is specific to the plugin agent dispatch path, not the agent definition format itself.

## Update: User Feedback

User noted that other plugin agents work fine, so this is NOT a general Claude Code bug with plugin agents. Something specific to these ansible-workflows agents or how they're being invoked in this context needs further investigation.
