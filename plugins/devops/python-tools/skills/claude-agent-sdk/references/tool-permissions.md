# Tool Permission Callbacks

This guide covers tool permission callbacks for fine-grained control over tool usage.

## Overview

Tool permission callbacks allow you to:
- Approve or deny tool usage
- Modify tool inputs before execution
- Implement complex permission logic
- Log tool usage

## Choosing Your Permission Strategy

The SDK provides two ways to control tool permissions: **permission modes** (simple) and **permission callbacks** (advanced).

### Quick Decision Guide

**Use `permission_mode` when:**
- You have simple, consistent permission policies
- You want to auto-approve/deny all file edits
- You don't need conditional logic
- You want minimal code

**Use `can_use_tool` callback when:**
- You need conditional approval logic
- You want to modify tool inputs before execution
- You need to block specific commands or patterns
- You want to log tool usage
- You need fine-grained control per tool

### Permission Mode Options

```python
from claude_agent_sdk import ClaudeAgentOptions

# Option 1: Auto-accept file edits (for automated workflows)
options = ClaudeAgentOptions(
    permission_mode="acceptEdits",
    allowed_tools=["Read", "Write", "Edit", "Bash"]
)

# Option 2: Require approval for edits (read-only automation)
options = ClaudeAgentOptions(
    permission_mode="rejectEdits",
    allowed_tools=["Read", "Grep", "Glob"]
)

# Option 3: Plan mode (no execution, just planning)
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Write", "Bash"]
)

# Option 4: Bypass all permissions (use with extreme caution)
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    allowed_tools=["Read", "Write", "Bash"]
)
```

### When to Use Each Mode

| Mode | Behavior | Best For |
|------|----------|----------|
| `"acceptEdits"` | Auto-approves file edits (Write, Edit, etc.) | CI/CD pipelines, automated refactoring, code generation |
| `"rejectEdits"` | Auto-rejects file edits, allows reads | Analysis tasks, read-only auditing, code review |
| `"plan"` | No execution, planning only | Previewing changes, cost estimation, planning phase |
| `"bypassPermissions"` | Bypasses all permission checks | Testing, trusted environments only (⚠️ dangerous) |
| `"default"` | Uses `can_use_tool` callback if provided | Custom permission logic (see below) |

### Combining Mode + Callback

You can use both together - the mode provides baseline behavior and the callback adds custom logic:

```python
async def custom_permissions(tool_name, input_data, context):
    """Custom logic on top of permission mode."""
    # Block dangerous bash commands even if acceptEdits is set
    if tool_name == "Bash":
        command = input_data.get("command", "")
        if "rm -rf /" in command:
            return PermissionResultDeny(message="Dangerous command blocked")

    return PermissionResultAllow()

options = ClaudeAgentOptions(
    permission_mode="acceptEdits",  # Auto-approve file edits
    can_use_tool=custom_permissions,  # But add custom bash validation
    allowed_tools=["Read", "Write", "Edit", "Bash"]
)
```

### Simple Use Cases: Just Use permission_mode

```python
# Example 1: Automated code generation (accept all edits)
options = ClaudeAgentOptions(
    permission_mode="acceptEdits",
    allowed_tools=["Read", "Write", "Edit"]
)

# Example 2: Code analysis (read-only)
options = ClaudeAgentOptions(
    permission_mode="rejectEdits",
    allowed_tools=["Read", "Grep", "Glob"]
)

# Example 3: Planning phase (no execution)
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Write", "Bash"]
)
```

## Permission Callbacks (Advanced)

For complex permission logic, use the `can_use_tool` callback.

## Callback Signature

```python
from claude_agent_sdk import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext
)

async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """
    Args:
        tool_name: Name of the tool being used
        input_data: Tool input parameters
        context: Additional context (suggestions, etc.)

    Returns:
        PermissionResultAllow or PermissionResultDeny
    """
    pass
```

## Permission Results

### Allow

```python
# Simple allow
return PermissionResultAllow()

# Allow with modified input
return PermissionResultAllow(
    updated_input={"file_path": "/safe/output.txt"}
)
```

### Deny

```python
return PermissionResultDeny(
    message="Cannot write to system directories"
)
```

## Common Patterns

### 1. Allow Read-Only Tools

```python
async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Auto-allow read-only operations."""

    # Always allow read operations
    if tool_name in ["Read", "Glob", "Grep"]:
        return PermissionResultAllow()

    # Deny or ask for other tools
    return PermissionResultDeny(
        message=f"Tool {tool_name} requires approval"
    )
```

### 2. Block Dangerous Commands

```python
async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Block dangerous bash commands."""

    if tool_name == "Bash":
        command = input_data.get("command", "")
        dangerous = ["rm -rf", "sudo", "chmod 777", "dd if=", "mkfs"]

        for pattern in dangerous:
            if pattern in command:
                return PermissionResultDeny(
                    message=f"Dangerous command pattern: {pattern}"
                )

    return PermissionResultAllow()
```

### 3. Redirect File Writes

```python
async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Redirect writes to safe directory."""

    if tool_name in ["Write", "Edit", "MultiEdit"]:
        file_path = input_data.get("file_path", "")

        # Block system directories
        if file_path.startswith("/etc/") or file_path.startswith("/usr/"):
            return PermissionResultDeny(
                message=f"Cannot write to system directory: {file_path}"
            )

        # Redirect to safe directory
        if not file_path.startswith("./safe/"):
            safe_path = f"./safe/{file_path.split('/')[-1]}"
            modified_input = input_data.copy()
            modified_input["file_path"] = safe_path

            return PermissionResultAllow(
                updated_input=modified_input
            )

    return PermissionResultAllow()
```

### 4. Log Tool Usage

```python
tool_usage_log = []

async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Log all tool usage."""

    # Log the request
    tool_usage_log.append({
        "tool": tool_name,
        "input": input_data,
        "suggestions": context.suggestions
    })

    print(f"Tool: {tool_name}")
    print(f"Input: {input_data}")

    return PermissionResultAllow()
```

### 5. Interactive Approval

```python
async def permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Ask user for permission on unknown tools."""

    # Auto-allow safe tools
    if tool_name in ["Read", "Grep", "Glob"]:
        return PermissionResultAllow()

    # Auto-deny dangerous tools
    if tool_name == "Bash":
        command = input_data.get("command", "")
        if "rm -rf" in command:
            return PermissionResultDeny(message="Dangerous command")

    # Ask user for other tools
    print(f"\nTool: {tool_name}")
    print(f"Input: {input_data}")
    user_input = input("Allow? (y/N): ").strip().lower()

    if user_input in ("y", "yes"):
        return PermissionResultAllow()
    else:
        return PermissionResultDeny(message="User denied permission")
```

## Configuration

Set the callback in `ClaudeAgentOptions`:

```python
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

options = ClaudeAgentOptions(
    can_use_tool=permission_callback,
    permission_mode="default",  # Ensure callbacks are invoked
    cwd="."
)

async with ClaudeSDKClient(options) as client:
    await client.query("List files and create hello.py")
    async for message in client.receive_response():
        # Process messages
        pass
```

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `"default"` | Invokes callback for every tool | Fine-grained control |
| `"acceptEdits"` | Auto-approves file edits | Automated workflows |
| `"rejectEdits"` | Auto-rejects file edits | Read-only mode |

## Complete Example

```python
import asyncio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

# Track usage
tool_log = []

async def safe_permission_callback(
    tool_name: str,
    input_data: dict,
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    """Safe permission callback with logging."""

    # Log usage
    tool_log.append({"tool": tool_name, "input": input_data})

    # Always allow read operations
    if tool_name in ["Read", "Glob", "Grep"]:
        print(f"✅ Auto-allow: {tool_name}")
        return PermissionResultAllow()

    # Check writes to system directories
    if tool_name in ["Write", "Edit"]:
        file_path = input_data.get("file_path", "")
        if file_path.startswith("/etc/"):
            print(f"❌ Blocked: write to {file_path}")
            return PermissionResultDeny(
                message=f"Cannot write to system directory"
            )

    # Check dangerous bash commands
    if tool_name == "Bash":
        command = input_data.get("command", "")
        if "rm -rf" in command or "sudo" in command:
            print(f"❌ Blocked: dangerous command")
            return PermissionResultDeny(
                message="Dangerous command pattern detected"
            )

    print(f"✅ Allowed: {tool_name}")
    return PermissionResultAllow()

async def main():
    options = ClaudeAgentOptions(
        can_use_tool=safe_permission_callback,
        permission_mode="default",
        allowed_tools=["Read", "Write", "Bash"]
    )

    async with ClaudeSDKClient(options) as client:
        await client.query("List files and create hello.py")

        async for message in client.receive_response():
            # Process messages
            pass

    # Print usage summary
    print("\nTool Usage Summary:")
    for entry in tool_log:
        print(f"  {entry['tool']}: {entry['input']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

1. **Return early** - Check tool_name first and return quickly for unmatched tools
2. **Be defensive** - Use `.get()` to safely access input_data fields
3. **Log decisions** - Track what was allowed/denied for debugging
4. **Clear messages** - Denial messages should explain why
5. **Test thoroughly** - Verify callback logic with different tool types

## Anti-Patterns

❌ **Assuming input structure**
```python
# Crashes if command key doesn't exist
command = input_data["command"]
```

✅ **Safe access**
```python
command = input_data.get("command", "")
```

❌ **Silent denials**
```python
return PermissionResultDeny()  # No message
```

✅ **Informative denials**
```python
return PermissionResultDeny(
    message="Cannot write to system directories for safety"
)
```

❌ **Checking all tools for Bash-specific logic**
```python
# This crashes on non-Bash tools
async def callback(tool_name, input_data, context):
    command = input_data["command"]  # Only Bash has "command"
```

✅ **Filter by tool_name first**
```python
async def callback(tool_name, input_data, context):
    if tool_name != "Bash":
        return PermissionResultAllow()

    command = input_data.get("command", "")
    # Now safe to check command
```
