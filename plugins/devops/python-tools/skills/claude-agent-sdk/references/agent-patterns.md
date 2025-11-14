# Agent and Subagent Definition Patterns

This guide covers how to define agents and subagents programmatically using the Claude Agent SDK.

## Core Concepts

**AgentDefinition** - Defines a specialized agent with specific tools, prompts, and model configuration.

**Programmatic Definition** - SDK best practice is to define agents programmatically using the `agents` parameter in `ClaudeAgentOptions`, not filesystem auto-discovery.

## Basic Agent Definition

```python
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions

options = ClaudeAgentOptions(
    agents={
        "agent-name": AgentDefinition(
            description="When to use this agent",
            prompt="System prompt defining role and behavior",
            tools=["Read", "Grep", "Glob"],
            model="sonnet"  # or "opus", "haiku", "inherit"
        )
    }
)
```

## AgentDefinition Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | `str` | Yes | Natural language description of when to use this agent |
| `prompt` | `str` | Yes | Agent's system prompt defining role and behavior |
| `tools` | `list[str]` | No | Array of allowed tool names. If omitted, inherits all tools |
| `model` | `str` | No | Model override: "sonnet", "opus", "haiku", or "inherit" |

## Common Patterns

### Read-Only Analyzer Agent

For code review, architecture analysis, or documentation review:

```python
"code-reviewer": AgentDefinition(
    description="Reviews code for best practices, security, and performance",
    prompt="""You are a code reviewer. Analyze code for:
    - Security vulnerabilities
    - Performance issues
    - Best practice adherence
    - Potential bugs

    Provide constructive, specific feedback.""",
    tools=["Read", "Grep", "Glob"],
    model="sonnet"
)
```

### Code Modification Agent

For implementing features or fixing bugs:

```python
"code-writer": AgentDefinition(
    description="Implements features and fixes bugs",
    prompt="""You are a code implementation specialist.
    Write clean, tested, well-documented code.
    Follow project conventions and best practices.""",
    tools=["Read", "Write", "Edit", "Grep", "Glob"],
    model="sonnet"
)
```

### Test Execution Agent

For running tests and analyzing results:

```python
"test-runner": AgentDefinition(
    description="Runs tests and analyzes results",
    prompt="""You are a testing specialist.
    Execute tests, analyze failures, and provide clear diagnostics.
    Focus on actionable feedback.""",
    tools=["Bash", "Read", "Grep"],
    model="sonnet"
)
```

### Multiple Agents Pattern

Orchestrator with specialized subagents:

```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",  # Orchestrator needs Task tool knowledge
    allowed_tools=["Bash", "Task", "Read", "Write"],
    agents={
        "analyzer": AgentDefinition(
            description="Analyzes code structure and patterns",
            prompt="You are a code analyzer. Examine structure, patterns, and architecture.",
            tools=["Read", "Grep", "Glob"]
        ),
        "fixer": AgentDefinition(
            description="Fixes identified issues",
            prompt="You are a code fixer. Apply fixes based on analysis results.",
            tools=["Read", "Edit", "Bash"],
            model="sonnet"
        )
    }
)
```

## Loading Agent Definitions from Files

While programmatic definition is recommended, you can still store agent prompts in markdown files:

```python
import yaml

def load_agent_definition(path: str) -> AgentDefinition:
    """Load agent definition from markdown file with YAML frontmatter."""
    with open(path) as f:
        content = f.read()

    parts = content.split("---")
    frontmatter = yaml.safe_load(parts[1])
    system_prompt = parts[2].strip()

    # Parse tools (can be comma-separated string or array)
    tools_value = frontmatter.get("tools", [])
    if isinstance(tools_value, str):
        tools = [t.strip() for t in tools_value.split(",")]
    else:
        tools = tools_value

    return AgentDefinition(
        description=frontmatter["description"],
        prompt=system_prompt,
        tools=tools,
        model=frontmatter.get("model", "inherit")
    )

# Load and register programmatically
investigator = load_agent_definition(".claude/agents/investigator.md")

options = ClaudeAgentOptions(
    agents={"investigator": investigator}
)
```

## Best Practices

1. **Use programmatic registration** - Define agents via `agents` parameter, not filesystem auto-discovery
2. **Set orchestrator system_prompt** - Main agent needs `system_prompt="claude_code"` to use Task tool
3. **Specific descriptions** - Agent descriptions determine when they're used
4. **Restrict tools** - Limit agent tools to minimum needed for safety and clarity
5. **Match agent names** - Ensure agent names in `agents={}` match what orchestrator references

## Anti-Patterns

❌ **Relying on filesystem auto-discovery**

```python
# SDK will auto-discover .claude/agents/*.md but this is NOT recommended
options = ClaudeAgentOptions()  # Missing explicit agents={}
```

✅ **Programmatic registration**

```python
options = ClaudeAgentOptions(
    agents={"agent-name": AgentDefinition(...)}
)
```

❌ **Missing orchestrator system prompt**

```python
options = ClaudeAgentOptions(
    agents={...}
    # Missing system_prompt="claude_code"
)
```

✅ **Proper orchestrator configuration**

```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",  # Orchestrator knows how to use Task tool
    agents={...}
)
```
