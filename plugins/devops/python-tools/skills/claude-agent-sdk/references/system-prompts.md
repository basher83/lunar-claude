# System Prompt Configuration Patterns

This guide covers different ways to configure system prompts in the Claude Agent SDK.

## Overview

System prompts define Claude's role, behavior, and capabilities. The SDK supports multiple configuration patterns.

## Configuration Types

### 1. No System Prompt (Vanilla Claude)

Claude operates without additional instructions:

```python
from claude_agent_sdk import query

async for message in query(prompt="What is 2 + 2?"):
    # Process messages
    pass
```

**Use when:** You want vanilla Claude behavior without specialized instructions.

### 2. String System Prompt

Custom instructions as a simple string:

```python
from claude_agent_sdk import ClaudeAgentOptions, query

options = ClaudeAgentOptions(
    system_prompt="You are a helpful Python expert. Explain concepts simply."
)

async for message in query(prompt="Explain async/await", options=options):
    pass
```

**Use when:** You need custom behavior for a specific task or domain.

### 3. Preset System Prompt

Use the official Claude Code preset:

```python
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"}
)
```

The `"claude_code"` preset includes:
- Tool usage patterns (Bash, Read, Write, Edit, etc.)
- Best practices for code modification
- Knowledge of the Task tool for delegating to subagents
- Git commit and PR workflows
- Security guidelines

**Use when:** Building SDK applications that orchestrate subagents or use file tools.

### 4. Preset with Append

Extend the Claude Code preset with additional instructions:

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Always explain your reasoning before implementing changes."
    }
)
```

**Use when:** You need Claude Code behavior plus domain-specific instructions.

## Common Patterns

### Orchestrator Agent

Main agent that delegates to subagents:

```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",  # Knows how to use Task tool
    allowed_tools=["Bash", "Task", "Read", "Write"],
    agents={
        "subagent-1": AgentDefinition(...),
        "subagent-2": AgentDefinition(...)
    }
)
```

**Critical:** Orchestrators must use `system_prompt="claude_code"` to understand how to delegate to subagents.

### Domain Expert

Specialized behavior for specific tasks:

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": """You are a security auditor for Python applications.

Focus on:
- SQL injection vulnerabilities
- Command injection risks
- Authentication/authorization flaws
- Secrets management issues

Provide specific, actionable security recommendations."""
    },
    allowed_tools=["Read", "Grep", "Glob"]
)
```

### Constrained Agent

Agent with specific behavioral constraints:

```python
options = ClaudeAgentOptions(
    system_prompt="""You are a read-only code analyzer.

IMPORTANT:
- Never modify files
- Never execute code
- Only analyze and report findings

Provide detailed analysis with file/line references.""",
    allowed_tools=["Read", "Grep", "Glob"]
)
```

## Shorthand vs Dict Format

The SDK accepts both shorthand and dictionary formats for the `claude_code` preset:

```python
# Shorthand for preset (recommended for simplicity)
system_prompt="claude_code"

# Equivalent dict format (official API)
system_prompt={"type": "preset", "preset": "claude_code"}

# With append (dict only)
system_prompt={
    "type": "preset",
    "preset": "claude_code",
    "append": "Additional instructions here"
}
```

**Note:** The shorthand `system_prompt="claude_code"` is a convenience that's equivalent to the full dict format. Both are valid and produce identical behavior. Use shorthand for cleaner code, or the dict format when you need to add `append` instructions.

## Best Practices

1. **Use preset for orchestrators** - Orchestrators need `system_prompt="claude_code"` for Task tool knowledge
2. **Use append for specialization** - Extend preset with domain-specific instructions
3. **Match tools to prompt** - System prompt should align with allowed_tools
4. **Be specific** - Clear, specific instructions produce better results
5. **Test variations** - Experiment with different prompts for your use case

## Examples

### File Processing Agent

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": """Process CSV files with these requirements:
        - Validate data types
        - Handle missing values
        - Generate summary statistics
        - Create visualizations using matplotlib"""
    },
    allowed_tools=["Read", "Write", "Bash"]
)
```

### Documentation Generator

```python
options = ClaudeAgentOptions(
    system_prompt="""You are a technical documentation specialist.

Generate clear, comprehensive documentation with:
- Overview and purpose
- API reference with types
- Usage examples
- Common pitfalls and troubleshooting

Use Google-style Python docstrings.""",
    allowed_tools=["Read", "Write", "Edit", "Grep"]
)
```

### Test Writer

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": """Write pytest-based tests following these patterns:
        - Use fixtures for setup/teardown
        - Parametrize tests when appropriate
        - Include edge cases and error conditions
        - Aim for >90% code coverage"""
    },
    allowed_tools=["Read", "Write", "Bash"]
)
```

## Anti-Patterns

❌ **Orchestrator without claude_code preset**
```python
# Orchestrator won't know how to use Task tool
options = ClaudeAgentOptions(
    agents={...}
    # Missing system_prompt="claude_code"
)
```

✅ **Proper orchestrator configuration**
```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",
    agents={...}
)
```

❌ **Conflicting instructions**
```python
# Tells agent to modify files but only allows read tools
options = ClaudeAgentOptions(
    system_prompt="Fix any bugs you find",
    allowed_tools=["Read", "Grep"]  # Can't actually fix anything
)
```

✅ **Aligned tools and instructions**
```python
options = ClaudeAgentOptions(
    system_prompt="Analyze code for bugs and report findings",
    allowed_tools=["Read", "Grep", "Glob"]
)
```
