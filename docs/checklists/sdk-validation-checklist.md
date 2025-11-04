# Claude Agent SDK Validation Checklist

This checklist helps validate SDK applications against official patterns and best practices from the claude-agent-sdk skill documentation.

## Quick Validation

Use this checklist when:

- Creating new SDK applications
- Reviewing SDK code
- Debugging SDK issues
- Ensuring alignment with best practices

---

## 1. Imports & Dependencies

### Required Checks

- [ ] **Async runtime import**
  - Uses `import anyio` (preferred) or `import asyncio`
  - Comment indicates choice: `# or: import asyncio`
  - **Reference:** SKILL.md line 47

- [ ] **Claude SDK imports are accurate**
  - `ClaudeAgentOptions` for configuration
  - `ClaudeSDKClient` for continuous conversations OR `query` for one-shot tasks
  - `AgentDefinition` if using programmatic agents
  - Message types: `AssistantMessage`, `ResultMessage`, `TextBlock`
  - Permission types if using callbacks: `PermissionResultAllow`, `PermissionResultDeny`
  - **Reference:** `references/api-reference.md`

- [ ] **UV script headers (if applicable)**
  - Uses `#!/usr/bin/env -S uv run --script --quiet`
  - Has PEP 723 dependencies block with `claude-agent-sdk>=0.1.6`
  - **Reference:** `assets/sdk-template.py` lines 1-7

---

## 2. Async Runtime

### Required Checks

- [ ] **Runtime execution is correct**
  - Uses `anyio.run(main)` (preferred) or `asyncio.run(main())`
  - Comment shows alternative: `# or: asyncio.run(main())`
  - **Reference:** SKILL.md lines 54-71, 88-124

- [ ] **Async/await patterns are correct**
  - Functions marked as `async def`
  - Uses `await` for SDK calls
  - Uses `async for` for message streaming
  - Uses `async with` for ClaudeSDKClient context manager
  - **Reference:** `references/best-practices.md` lines 82-94

---

## 3. Choosing query() vs ClaudeSDKClient

### Required Checks

- [ ] **Correct approach for use case**
  - `query()`: One-shot tasks, no conversation memory
  - `ClaudeSDKClient`: Multi-turn conversations, context retention
  - **Reference:** SKILL.md lines 29-44

- [ ] **Hooks/Custom tools only with ClaudeSDKClient**
  - NOT using hooks with `query()` (not supported)
  - NOT using custom tools with `query()` (not supported)
  - **Reference:** SKILL.md line 45 (important warning)

---

## 4. Orchestrator Configuration

### Required Checks

- [ ] **System prompt is set correctly**
  - Uses `system_prompt="claude_code"` for orchestrators
  - OR uses `{"type": "preset", "preset": "claude_code"}` (equivalent)
  - Custom prompts only for non-orchestrators
  - **Reference:** SKILL.md lines 226-242, `references/system-prompts.md`

- [ ] **Task tool is included**
  - `allowed_tools` includes `"Task"` for orchestrators
  - Orchestrators cannot delegate without Task tool
  - **Reference:** SKILL.md line 39, `references/best-practices.md` lines 72-80

- [ ] **Agent definitions are programmatic**
  - Agents defined in `agents={}` parameter (preferred)
  - Clear `description` (when to use agent)
  - Specific `prompt` (agent instructions)
  - Minimal `tools` list (principle of least privilege)
  - **Reference:** SKILL.md lines 195-217, `references/agent-patterns.md`

---

## 5. Agent Definitions

### Required Checks

- [ ] **Agent definition structure is correct**

  ```python
  AgentDefinition(
      description="...",  # When to use this agent
      prompt="...",       # Agent instructions
      tools=[...],        # Minimal tool set
      model="sonnet"      # or "opus", "haiku", "inherit"
  )
  ```

  - **Reference:** SKILL.md lines 195-217

- [ ] **Agent names match references**
  - Names in `agents={}` match Task tool usage
  - No naming mismatches between definition and invocation
  - **Reference:** `references/best-practices.md` lines 43-52

- [ ] **Tools are restricted to minimum needed**
  - Read-only agents: `["Read", "Grep", "Glob"]`
  - Code modifiers: `["Read", "Edit", "Bash"]`
  - No excessive tool permissions
  - **Reference:** SKILL.md lines 248-256, `references/best-practices.md` lines 54-71

---

## 6. Permission Control

### Required Checks

- [ ] **Permission strategy is appropriate**
  - Simple use case → `permission_mode` only
  - Complex logic → `can_use_tool` callback
  - **Reference:** `references/tool-permissions.md` lines 13-114

- [ ] **Permission mode is valid**
  - One of: `"acceptEdits"`, `"rejectEdits"`, `"plan"`, `"bypassPermissions"`, `"default"`
  - Appropriate for use case (e.g., CI/CD uses `"acceptEdits"`)
  - **Reference:** `references/tool-permissions.md` lines 64-70

- [ ] **Permission callback (if used) is correct**
  - Signature: `async def(tool_name, input_data, context) -> PermissionResultAllow | PermissionResultDeny`
  - Returns early for unmatched tools
  - Uses `.get()` for safe input_data access
  - Clear denial messages
  - **Reference:** `references/tool-permissions.md` lines 120-344, `examples/tool_permission_callback.py`

---

## 7. Hooks (if used)

### Required Checks

- [ ] **Hooks ONLY used with ClaudeSDKClient**
  - NOT using hooks with `query()` function
  - **Reference:** SKILL.md line 45 (critical warning)

- [ ] **Hook types are supported**
  - Using ONLY: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`
  - NOT using unsupported: `SessionStart`, `SessionEnd`, `Notification`
  - **Reference:** `references/hooks-guide.md` line 14 (important warning)

- [ ] **Hook signature is correct**
  - `async def(input_data, tool_use_id, context) -> HookJSONOutput`
  - Returns empty `{}` when hook doesn't apply
  - Uses `HookMatcher` for tool filtering
  - **Reference:** `references/hooks-guide.md` lines 46-68, `examples/hooks.py`

- [ ] **Hook output structure is valid**
  - Includes `hookEventName` in `hookSpecificOutput`
  - PreToolUse: includes `permissionDecision` ("allow" or "deny")
  - Includes clear `reason` and `systemMessage` fields
  - **Reference:** `references/hooks-guide.md` lines 70-144

---

## 8. ClaudeSDKClient Usage

### Required Checks

- [ ] **Context manager pattern is used**

  ```python
  async with ClaudeSDKClient(options=options) as client:
      await client.query(...)
      async for message in client.receive_response():
          ...
  ```

  - **Reference:** SKILL.md lines 88-124

- [ ] **Query → receive_response flow**
  - Calls `await client.query(prompt)` first
  - Then iterates `async for message in client.receive_response()`
  - Does NOT interleave queries and receives incorrectly
  - **Reference:** `examples/streaming_mode.py`

- [ ] **Interrupts (if used) are correct**
  - Uses `await client.interrupt()` to stop execution
  - Only available with ClaudeSDKClient (not query())
  - **Reference:** SKILL.md lines 139-162

---

## 9. Message Handling

### Required Checks

- [ ] **Message types are checked correctly**

  ```python
  if isinstance(message, AssistantMessage):
      for block in message.content:
          if isinstance(block, TextBlock):
              print(block.text)
  elif isinstance(message, ResultMessage):
      # Handle completion
  ```

  - **Reference:** SKILL.md lines 77-91, `examples/streaming_mode.py`

- [ ] **TextBlock extraction is correct**
  - Iterates through `message.content`
  - Checks `isinstance(block, TextBlock)` before accessing `.text`
  - **Reference:** `references/best-practices.md` lines 95-113

- [ ] **ResultMessage handling**
  - Checks for `message.duration_ms`, `message.total_cost_usd`
  - Uses optional access (fields may be None)
  - **Reference:** `assets/sdk-template.py` lines 86-93

---

## 10. Error Handling

### Required Checks

- [ ] **API key validation**
  - Checks `os.getenv("ANTHROPIC_API_KEY")` before SDK calls
  - Provides clear error message if missing
  - **Reference:** `assets/sdk-template.py` lines 58-63

- [ ] **Safe dictionary access**
  - Uses `.get()` for input_data, tool_response fields
  - Handles missing/None values gracefully
  - **Reference:** `references/tool-permissions.md` lines 297-344

- [ ] **Async exception handling**
  - Try/except blocks for critical sections
  - Proper cleanup in exception cases
  - **Reference:** `references/best-practices.md`

---

## 11. Settings & Configuration

### Required Checks

- [ ] **setting_sources is configured (if needed)**
  - Default behavior: NO settings loaded (isolated environment)
  - Explicitly set to load: `["user"]`, `["project"]`, `["user", "project"]`
  - Understands isolation vs loading tradeoff
  - **Reference:** `examples/setting_sources.py`

- [ ] **Model selection is appropriate**
  - Orchestrator: `"claude-sonnet-4-5-20250929"` or latest
  - Subagents: `"sonnet"`, `"opus"`, `"haiku"`, or `"inherit"`
  - **Reference:** SKILL.md line 51, `references/agent-patterns.md`

- [ ] **Budget limits (if needed)**
  - Uses `max_budget_usd` for cost control
  - Appropriate for CI/CD and automated workflows
  - **Reference:** `examples/max_budget_usd.py`

---

## 12. Best Practices Compliance

### Required Checks

- [ ] **Follows DRY principle**
  - Options extracted to function (e.g., `get_sdk_options()`)
  - Reusable patterns not duplicated
  - **Reference:** `assets/sdk-template.py` lines 33-55

- [ ] **Clear comments and documentation**
  - Docstrings for functions
  - Inline comments for complex logic
  - Usage notes in module docstring
  - **Reference:** `assets/sdk-template.py` lines 8-17

- [ ] **Type hints are used**
  - Function return types specified
  - Parameter types for clarity
  - **Reference:** `assets/sdk-template.py` line 36

- [ ] **No anti-patterns**
  - Not using agents for simple tasks (use query() instead)
  - Not giving excessive tool permissions
  - Not bypassing permissions without reason
  - **Reference:** `references/best-practices.md`, skill SKILL.md

---

## Validation Summary Template

After reviewing, fill out this summary:

### ✅ Passed Checks

- [ ] Imports & Dependencies
- [ ] Async Runtime
- [ ] Orchestrator Configuration
- [ ] Agent Definitions
- [ ] Permission Control
- [ ] Message Handling
- [ ] Best Practices

### ❌ Issues Found

- Issue 1: [Description]
- Issue 2: [Description]

### 🔧 Fixes Required

1. [Specific fix with line reference]
2. [Specific fix with line reference]

### 📊 Overall Assessment

- **Accuracy:** [%]
- **Alignment with docs:** [High/Medium/Low]
- **Production ready:** [Yes/No]

---

## Quick Reference Links

**Core Documentation:**

- Main skill: `SKILL.md`
- API reference: `references/api-reference.md`
- Best practices: `references/best-practices.md`

**Pattern Guides:**

- Agent patterns: `references/agent-patterns.md`
- Hooks: `references/hooks-guide.md`
- Permissions: `references/tool-permissions.md`
- System prompts: `references/system-prompts.md`
- Subagents: `references/subagents.md`

**Examples:**

- Quick start: `examples/quick_start.py`
- Template: `assets/sdk-template.py`
- Complete examples: `examples/*.py`
