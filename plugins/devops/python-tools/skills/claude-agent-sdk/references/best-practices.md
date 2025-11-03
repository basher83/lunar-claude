# Claude Agent SDK Best Practices

This guide captures best practices and common patterns for building effective SDK applications.

## Agent Definition

### ✅ Use Programmatic Registration

**Recommended:** Define agents via `agents` parameter
```python
options = ClaudeAgentOptions(
    agents={
        "investigator": AgentDefinition(
            description="Analyzes errors autonomously",
            prompt="You are an error investigator...",
            tools=["Read", "Grep", "Glob", "Bash"]
        )
    }
)
```

**Not Recommended:** Relying on filesystem auto-discovery
```python
# SDK can auto-discover .claude/agents/*.md
# but programmatic registration is clearer and more maintainable
options = ClaudeAgentOptions()
```

### ✅ Set Orchestrator System Prompt

**Critical:** Orchestrators must use `system_prompt="claude_code"`
```python
options = ClaudeAgentOptions(
    system_prompt="claude_code",  # Knows how to use Task tool
    allowed_tools=["Bash", "Task", "Read", "Write"],
    agents={...}
)
```

**Why:** The claude_code preset includes knowledge of the Task tool for delegating to subagents.

### ✅ Match Agent Names

Ensure agent names in `agents={}` match references in prompts:
```python
# Define agent
options = ClaudeAgentOptions(
    agents={"markdown-investigator": AgentDefinition(...)}
)

# Reference in prompt
await client.query("Use the 'markdown-investigator' subagent...")
```

## Tool Configuration

### ✅ Restrict Subagent Tools

Limit subagent tools to minimum needed:
```python
# Read-only analyzer
"analyzer": AgentDefinition(
    tools=["Read", "Grep", "Glob"]
)

# Code modifier
"fixer": AgentDefinition(
    tools=["Read", "Edit", "Bash"]
)
```

### ✅ Give Orchestrator Task Tool

Orchestrators need Task tool to delegate:
```python
options = ClaudeAgentOptions(
    allowed_tools=["Bash", "Task", "Read", "Write"],  # Include Task
    agents={...}
)
```

## Async/Await Patterns

### ✅ Use async with for Streaming

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query(prompt)

    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            # Process messages
            pass
```

### ✅ Handle Multiple Message Types

```python
async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                text = block.text

    elif isinstance(message, ResultMessage):
        print(f"Cost: ${message.total_cost_usd:.4f}")
        print(f"Duration: {message.duration_ms}ms")
```

## Error Handling

### ✅ Validate Agent Responses

Don't assume agents return expected format:
```python
investigation_report = None

async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                # Try to extract JSON
                try:
                    investigation_report = json.loads(block.text)
                except json.JSONDecodeError:
                    # Handle non-JSON response
                    continue

if not investigation_report:
    raise RuntimeError("Agent did not return valid report")
```

### ✅ Use uv Script Headers

For standalone SDK scripts, use uv inline script metadata:
```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
# ]
# ///
```

## Project Structure

### ✅ Organize Agent Definitions

Option 1: Store in markdown files, load programmatically
```text
project/
├── .claude/
│   └── agents/
│       ├── investigator.md
│       └── fixer.md
├── main.py
```

```python
def load_agent_definition(path: str) -> AgentDefinition:
    # Parse frontmatter and content
    # Return AgentDefinition

investigator = load_agent_definition(".claude/agents/investigator.md")
options = ClaudeAgentOptions(agents={"investigator": investigator})
```

Option 2: Define inline
```python
options = ClaudeAgentOptions(
    agents={
        "investigator": AgentDefinition(
            description="...",
            prompt="...",
            tools=[...]
        )
    }
)
```

## Permission Management

### ✅ Choose Appropriate Permission Mode

```python
# Automated workflows (auto-approve edits)
options = ClaudeAgentOptions(
    permission_mode="acceptEdits"
)

# Interactive development (ask for approval)
options = ClaudeAgentOptions(
    permission_mode="default",
    can_use_tool=permission_callback
)

# Read-only mode (use tool restrictions)
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob"]  # Only read tools
)
```

### ✅ Use Hooks for Complex Logic

Prefer hooks over permission callbacks for:
- Adding context
- Reviewing outputs
- Stopping on errors

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_command])
        ],
        "PostToolUse": [
            HookMatcher(matcher="Bash", hooks=[review_output])
        ]
    }
)
```

## Common Anti-Patterns

### ❌ Missing System Prompt on Orchestrator

```python
# Orchestrator won't know how to use Task tool
options = ClaudeAgentOptions(
    agents={...}
    # Missing system_prompt="claude_code"
)
```

### ❌ Tool/Prompt Mismatch

```python
# Tells agent to modify files but only allows read tools
options = ClaudeAgentOptions(
    system_prompt="Fix any bugs you find",
    allowed_tools=["Read", "Grep"]  # Can't actually fix
)
```

### ❌ Assuming Agent Output Format

```python
# Assumes agent returns JSON
json_data = json.loads(message.content[0].text)  # May crash
```

### ❌ Not Validating Agent Names

```python
# Define as "investigator" but reference as "markdown-investigator"
options = ClaudeAgentOptions(
    agents={"investigator": AgentDefinition(...)}
)
await client.query("Use 'markdown-investigator'...")  # Won't work
```

## Performance Optimization

### ✅ Use Appropriate Models

```python
# Fast, cheap tasks
"simple-agent": AgentDefinition(model="haiku", ...)

# Complex reasoning
"complex-agent": AgentDefinition(model="sonnet", ...)

# Inherit from main agent
"helper-agent": AgentDefinition(model="inherit", ...)
```

### ✅ Set Budget Limits

```python
options = ClaudeAgentOptions(
    max_budget_usd=1.00  # Stop after $1
)
```

### ✅ Limit Turns for Simple Tasks

```python
options = ClaudeAgentOptions(
    max_turns=3  # Prevent infinite loops
)
```

## Testing

### ✅ Validate Agent Definitions

```python
def test_agent_configuration():
    """Ensure agent definitions are valid."""
    options = get_sdk_options()

    # Check orchestrator has claude_code preset
    assert options.system_prompt == "claude_code"

    # Check orchestrator has Task tool
    assert "Task" in options.allowed_tools

    # Check agents are registered
    assert "investigator" in options.agents
    assert "fixer" in options.agents
```

### ✅ Test Tool Restrictions

```python
def test_subagent_tools():
    """Ensure subagents have correct tools."""
    options = get_sdk_options()

    investigator = options.agents["investigator"]
    assert "Read" in investigator.tools
    assert "Write" not in investigator.tools  # Read-only
```

## Documentation

### ✅ Document Agent Purposes

```python
options = ClaudeAgentOptions(
    agents={
        "investigator": AgentDefinition(
            # Clear, specific description
            description=(
                "Autonomous analyzer that determines if markdown errors "
                "are fixable or false positives"
            ),
            prompt="...",
            tools=[...]
        )
    }
)
```

### ✅ Document Workflow

```python
"""
Intelligent Markdown Linting Orchestrator

Architecture:
- Orchestrator (main): Strategic coordination
- Investigator subagent: Autonomous error analysis
- Fixer subagent: Execute fixes with context

Workflow:
1. Discovery: Run linter, parse output
2. Triage: Classify errors (simple vs ambiguous)
3. Investigation: Investigator analyzes ambiguous errors
4. Fixing: Fixer applies fixes based on investigation
5. Verification: Re-run linter to confirm fixes
"""
```

## Debugging

### ✅ Log Agent Communication

```python
all_response_text = []

async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                all_response_text.append(block.text)
                print(f"Agent: {block.text}")

# Save full transcript for debugging
with open("debug_transcript.txt", "w") as f:
    f.write("\n\n".join(all_response_text))
```

### ✅ Track Costs

```python
async for message in client.receive_response():
    if isinstance(message, ResultMessage):
        if message.total_cost_usd:
            print(f"Total cost: ${message.total_cost_usd:.4f}")
        if message.duration_ms:
            print(f"Duration: {message.duration_ms}ms")
```
