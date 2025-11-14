# Hook Patterns and Configuration

This guide covers hook patterns for intercepting and modifying Claude Agent SDK behavior.

## Overview

Hooks allow you to intercept SDK events and modify behavior at key points in execution. Common uses:

- Control tool execution (approve/deny/modify)
- Add context to prompts
- Review tool outputs
- Stop execution on errors
- Log activity

> **⚠️ IMPORTANT:** The Python SDK does **NOT** support `SessionStart`, `SessionEnd`, or `Notification` hooks due to setup limitations. Only the 6 hook types listed below are supported. Attempting to use unsupported hooks will result in them never firing.

## Hook Types

| Hook | When It Fires | Common Uses |
|------|---------------|-------------|
| `PreToolUse` | Before tool execution | Approve/deny/modify tool calls |
| `PostToolUse` | After tool execution | Review output, add context, stop on errors |
| `UserPromptSubmit` | Before processing user prompt | Add context, modify prompt |
| `Stop` | When execution stops | Cleanup, final logging |
| `SubagentStop` | When a subagent stops | Capture subagent results, cleanup |
| `PreCompact` | Before message compaction | Review/modify messages before compaction |

## Hook Configuration

Hooks are configured via the `hooks` parameter in `ClaudeAgentOptions`:

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_bash_command]),
        ],
        "PostToolUse": [
            HookMatcher(matcher="Bash", hooks=[review_output]),
        ],
    }
)
```

## Hook Function Signature

All hooks have the same signature:

```python
from claude_agent_sdk.types import HookInput, HookContext, HookJSONOutput

async def hook_function(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """
    Args:
        input_data: Hook-specific data (tool_name, tool_input, etc.)
        tool_use_id: Unique ID for this tool use (if applicable)
        context: Additional context about the execution

    Returns:
        HookJSONOutput: Dict with hook-specific fields
    """
    return {}  # Empty dict = no action
```

## HookJSONOutput Fields

| Field | Type | Use Case | Description |
|-------|------|----------|-------------|
| `continue_` | `bool` | Stop execution | Set to `False` to halt execution |
| `stopReason` | `str` | Stop execution | Explanation for why execution stopped |
| `reason` | `str` | Logging/debugging | Explanation of hook decision |
| `systemMessage` | `str` | User feedback | Message shown to user |
| `hookSpecificOutput` | `dict` | Hook-specific data | Additional hook-specific fields |

### PreToolUse Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow" | "deny",  # Control tool execution
        "permissionDecisionReason": "Explanation for decision",
        "modifiedInput": {...}  # Optional: Modified tool input
    }
}
```

### PostToolUse Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Extra context based on tool output"
    }
}
```

### UserPromptSubmit Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "updatedPrompt": "Modified prompt text"
    }
}
```

### Stop Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "Stop"
    }
}
```

### SubagentStop Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "SubagentStop"
    }
}
```

### PreCompact Hook-Specific Fields

```python
{
    "hookSpecificOutput": {
        "hookEventName": "PreCompact",
        "additionalContext": "Context to preserve during compaction"
    }
}
```

## Common Patterns

### 1. Block Dangerous Commands (PreToolUse)

```python
async def check_bash_command(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """Prevent dangerous bash commands."""
    if input_data["tool_name"] != "Bash":
        return {}

    command = input_data["tool_input"].get("command", "")
    dangerous_patterns = ["rm -rf", "sudo", "chmod 777", "dd if="]

    for pattern in dangerous_patterns:
        if pattern in command:
            return {
                "reason": f"Blocked dangerous command pattern: {pattern}",
                "systemMessage": f"🚫 Blocked: {pattern}",
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Command contains: {pattern}"
                }
            }

    return {}  # Allow by default
```

### 2. Review Tool Output (PostToolUse)

```python
async def review_tool_output(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """Add context based on tool output."""
    tool_response = input_data.get("tool_response", "")

    if "error" in str(tool_response).lower():
        return {
            "systemMessage": "⚠️ Command produced an error",
            "reason": "Tool execution failed",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "Consider checking command syntax or permissions."
            }
        }

    return {}
```

### 4. Stop on Critical Errors (PostToolUse)

```python
async def stop_on_critical_error(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """Halt execution on critical errors."""
    tool_response = input_data.get("tool_response", "")

    if "critical" in str(tool_response).lower():
        return {
            "continue_": False,
            "stopReason": "Critical error detected - halting for safety",
            "systemMessage": "🛑 Execution stopped: critical error"
        }

    return {"continue_": True}
```

### 5. Redirect File Writes (PreToolUse)

```python
async def safe_file_writes(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """Redirect writes to safe directory."""
    if input_data["tool_name"] not in ["Write", "Edit"]:
        return {}

    file_path = input_data["tool_input"].get("file_path", "")

    # Block writes to system directories
    if file_path.startswith("/etc/") or file_path.startswith("/usr/"):
        return {
            "reason": f"Blocked write to system directory: {file_path}",
            "systemMessage": "🚫 Cannot write to system directories",
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "System directory protection"
            }
        }

    # Redirect to safe directory
    if not file_path.startswith("./safe/"):
        safe_path = f"./safe/{file_path.split('/')[-1]}"
        modified_input = input_data["tool_input"].copy()
        modified_input["file_path"] = safe_path

        return {
            "reason": f"Redirected write from {file_path} to {safe_path}",
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Redirected to safe directory",
                "modifiedInput": modified_input
            }
        }

    return {}
```

## Hook Matcher Patterns

`HookMatcher` determines when hooks fire:

```python
# Match specific tool
HookMatcher(matcher="Bash", hooks=[check_bash])

# Match all tools
HookMatcher(matcher=None, hooks=[log_all_tools])

# Multiple hooks for same matcher
HookMatcher(
    matcher="Write",
    hooks=[check_permissions, log_write, backup_file]
)
```

## Complete Example

```python
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, HookMatcher

async def block_dangerous_bash(input_data, tool_use_id, context):
    if input_data["tool_name"] != "Bash":
        return {}

    command = input_data["tool_input"].get("command", "")
    if "rm -rf" in command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Dangerous rm -rf detected"
            }
        }
    return {}

options = ClaudeAgentOptions(
    allowed_tools=["Bash", "Read", "Write"],
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[block_dangerous_bash])
        ]
    }
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Run a safe bash command")
    async for message in client.receive_response():
        # Process messages
        pass
```

## Best Practices

1. **Return early** - Return empty dict `{}` when hook doesn't apply
2. **Be specific** - Clear `reason` and `systemMessage` fields help debugging
3. **Use matchers** - Filter hooks to relevant tools with `matcher` parameter
4. **Chain hooks** - Multiple hooks can process same event
5. **Handle errors** - Hooks should be defensive and handle missing data
6. **Log decisions** - Use `reason` field to explain hook decisions

## Anti-Patterns

❌ **Blocking without explanation**

```python
return {
    "hookSpecificOutput": {
        "permissionDecision": "deny"
        # Missing permissionDecisionReason
    }
}
```

✅ **Clear explanations**

```python
return {
    "reason": "Command contains dangerous pattern: rm -rf",
    "systemMessage": "🚫 Blocked dangerous command",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Safety: rm -rf detected"
    }
}
```

❌ **Ignoring tool_name in PreToolUse**

```python
# This will fire for ALL tools
async def hook(input_data, tool_use_id, context):
    command = input_data["tool_input"]["command"]  # Crashes on non-Bash tools
```

✅ **Filter by tool_name**

```python
async def hook(input_data, tool_use_id, context):
    if input_data["tool_name"] != "Bash":
        return {}
    command = input_data["tool_input"].get("command", "")
```
