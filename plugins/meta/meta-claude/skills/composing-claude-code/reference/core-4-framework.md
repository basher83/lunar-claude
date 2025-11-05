# The Core 4 Framework

> "Keep track of the core four. If you understand the core 4 and how each element flows and controls your agent, you will understand compute and you'll understand how to scale your compute."

The Core 4 Framework is the foundation of all agentic systems. Every agent—whether base, custom, or sub-agent—operates on these four pillars:

1. **Context** - What information does the agent have?
2. **Model** - What capabilities does the model provide?
3. **Prompt** - What instruction are you giving?
4. **Tools** - What actions can the agent take?

## Why the Core 4 Matters

**Understanding compute = Understanding the Core 4**

When you analyze any agent configuration, isolate the Core 4:
- How is context being managed?
- Which model is selected and why?
- What are the system prompts vs user prompts?
- What tools are available?

**Everything comes down to just four pieces. If you understand these, you will win.**

## The Four Pillars in Detail

### 1. Context - What Information Does the Agent Have?

Context is the information available to your agent at any given moment.

**Types of Context:**

```text
Static Context (always loaded):
├── CLAUDE.md (global instructions)
├── System prompt (agent definition)
└── MCP servers (tool descriptions)

Dynamic Context (accumulated during session):
├── Conversation history
├── File reads
├── Tool execution results
└── User prompts
```

**Context Management Strategies:**

| Strategy | When to Use | Token Cost |
|----------|-------------|------------|
| Minimal CLAUDE.md | Always | 500-1k tokens |
| Context priming | Task-specific setup | 2-5k tokens |
| Context bundles | Agent handoffs | 10-20k tokens |
| Sub-agent delegation | Parallel work | Isolated per agent |

**Key Principle:** A focused agent is a performant agent.

**Anti-pattern:** Loading all context upfront regardless of relevance.

### 2. Model - What Capabilities Does the Model Provide?

The model determines intelligence, speed, and cost characteristics.

**Model Selection:**

```text
Claude Opus:
├── Use: Complex reasoning, large codebases, architectural decisions
├── Cost: Highest
└── Speed: Slower

Claude Sonnet:
├── Use: Balanced tasks, general development
├── Cost: Medium
└── Speed: Medium

Claude Haiku:
├── Use: Simple tasks, fast iteration, text transformation
├── Cost: Lowest (pennies)
└── Speed: Fastest
```

**Example: Echo Agent (Custom Agents)**
```python
model: "claude-3-haiku-20240307"  # Downgraded for simple text manipulation
# Result: Much faster, much cheaper, still effective for the task
```

**Key Principle:** Match model capability to task complexity. Don't pay for Opus when Haiku will do.

### 3. Prompt - What Instruction Are You Giving?

Prompts are the fundamental unit of knowledge work and programming.

**Critical Distinction: System Prompts vs User Prompts**

```text
System Prompts:
├── Define agent identity and capabilities
├── Loaded once at agent initialization
├── Affect every user prompt that follows
├── Used in: Custom agents, sub-agents
└── Not visible in conversation history

User Prompts:
├── Request specific work from the agent
├── Added to conversation history
├── Build on system prompt foundation
├── Used in: Interactive Claude Code sessions
└── Visible in conversation history
```

**The Pong Agent Example:**

```python
# System prompt (3 lines):
"You are a pong agent. Always respond exactly with 'pong'. That's it."

# Result: No matter what user prompts ("hello", "summarize codebase", "what can you do?")
# Agent always responds: "pong"
```

**Key Insight:** "As soon as you touch the system prompt, you change the product, you change the agent."

**Information Flow in Multi-Agent Systems:**

```text
User Prompt → Primary Agent (System + User Prompts)
                    ↓
              Primary prompts Sub-Agent (System Prompt + Primary's instructions)
                    ↓
              Sub-Agent responds → Primary Agent (not to user!)
                    ↓
              Primary Agent → User
```

**Why this matters:** Sub-agents respond to your primary agent, not to you. This changes how you write sub-agent prompts.

### 4. Tools - What Actions Can the Agent Take?

Tools are the agent's ability to interact with the world.

**Tool Sources:**

```text
Built-in Claude Code Tools:
├── Read, Write, Edit files
├── Bash commands
├── Grep, Glob searches
├── Git operations
└── ~15 standard tools

MCP Servers (External):
├── APIs, databases, services
├── Added via mcp.json
└── Can consume 24k+ tokens if not managed

Custom Tools (SDK):
├── Built with @mcptool decorator
├── Passed to create_sdk_mcp_server()
└── Integrated with system prompt
```

**Example: Custom Echo Agent Tool**

```python
@mcptool(
    name="text_transformer",
    description="Transform text with reverse, uppercase, repeat operations"
)
def text_transformer(params: dict) -> dict:
    text = params["text"]
    operation = params["operation"]
    # Do whatever you want inside your tool
    return {"result": transformed_text}
```

**Key Principle:** Tools consume context. The `/context` command shows what's loaded—every tool takes space in your agent's mind.

## The Core 4 in Different Agent Types

### Base Claude Code Agent

```text
Context: CLAUDE.md + conversation history
Model: User-selected (Opus/Sonnet/Haiku)
Prompt: User prompts → system prompt
Tools: All 15 built-in + loaded MCP servers
```

### Custom Agent (SDK)

```text
Context: Can be customized (override or extend)
Model: Specified in options (can use Haiku for speed)
Prompt: Custom system prompt (can override completely)
Tools: Custom tools + optionally built-in tools
```

**Example:** The Pong agent completely overrides Claude Code's system prompt—it's no longer Claude Code, it's a custom agent.

### Sub-Agent

```text
Context: Isolated context window (no history from primary)
Model: Inherits from primary or can be specified
Prompt: System prompt (in .md file) + primary agent's instructions
Tools: Configurable (can restrict to subset)
```

**Key distinction:** Sub-agents have no context history. They only have what the primary agent prompts them with.

## Information Flow Between Agents

### Single Agent Flow

```text
User Prompt
    ↓
Primary Agent (Context + Model + Prompt + Tools)
    ↓
Response to User
```

### Multi-Agent Flow

```text
User Prompt
    ↓
Primary Agent
    ├→ Sub-Agent 1 (isolated context)
    ├→ Sub-Agent 2 (isolated context)
    └→ Sub-Agent 3 (isolated context)
    ↓
Aggregates responses
    ↓
Response to User
```

**Critical Understanding:**
- Your sub-agents respond to your primary agent, not to you
- Each sub-agent has its own Core 4
- You must track multiple sets of (Context, Model, Prompt, Tools)

## Context Preservation vs Context Isolation

### Context Preservation (Benefit)

```text
Primary Agent:
├── Conversation history maintained
├── Can reference previous work
├── Builds on accumulated knowledge
└── Uses client class in SDK for multi-turn conversations
```

### Context Isolation (Feature + Limitation)

```text
Sub-Agent:
├── Fresh context window (no pollution from main conversation)
├── Focused on single purpose
├── Cannot access primary agent's full history
└── Operates on what primary agent passes it
```

**The Trade-off:** Context isolation makes agents focused (good) but limits information flow (limitation).

## The 12 Leverage Points of Agent Coding

While the Core 4 are foundational, experienced engineers track 12 leverage points:

1. **Context** (Core 4)
2. **Model** (Core 4)
3. **Prompt** (Core 4)
4. **Tools** (Core 4)
5. System prompt structure
6. Tool permission management
7. Context window monitoring
8. Model selection per task
9. Multi-agent orchestration
10. Information flow design
11. Debugging and observability
12. Dependency coupling management

**Key Principle:** "Whenever you see Claude Code options, isolate the Core 4. How will the Core 4 be managed given this setup?"

## Practical Applications

### Application 1: Choosing the Right Model

```text
Task: Simple text transformation
Core 4 Analysis:
├── Context: Minimal (just the text to transform)
├── Model: Haiku (fast, cheap, sufficient)
├── Prompt: Simple instruction ("reverse this text")
└── Tools: Custom text_transformer tool

Result: Pennies cost, sub-second response
```

### Application 2: Managing Context Explosion

```text
Problem: Primary agent context at 180k tokens
Core 4 Analysis:
├── Context: Too much accumulated history
├── Model: Opus (expensive at high token count)
├── Prompt: Gets diluted in massive context
└── Tools: All 15 + 5 MCP servers (24k tokens)

Solution: Delegate to sub-agents
├── Context: Split work across 3 sub-agents (60k each)
├── Model: Keep Opus only where needed
├── Prompt: Focused sub-agent system prompts
└── Tools: Restrict to relevant subset per agent

Result: Work completed, context manageable
```

### Application 3: Custom Agent for Specialized Workflow

```text
Use Case: Plan-Build-Review-Ship task board
Core 4 Design:
├── Context: Task board state + file structure
├── Model: Sonnet (balanced for coding + reasoning)
├── Prompt: Custom system prompt defining PBRS workflow
└── Tools: Built-in file ops + custom task board tools

Implementation: SDK with custom system prompt and tools
Result: Specialized agent that understands your specific workflow
```

## System Prompts vs User Prompts in Practice

### The Confusion

Many engineers treat sub-agent `.md` files as user prompts. **This is wrong.**

```markdown
# ❌ Wrong: Writing sub-agent prompt like a user prompt
Please analyze this codebase and tell me what it does.
```

```markdown
# ✅ Correct: Writing sub-agent prompt as system prompt
Purpose: Analyze codebases and provide concise summaries

When called, you will receive a user's request from the PRIMARY AGENT.
Your job is to read relevant files and create a summary.

Report Format:
Respond to the PRIMARY AGENT (not the user) with:
"Claude, tell the user: [your summary]"
```

### Why the Distinction Matters

```text
System Prompt:
├── Defines WHO the agent is
├── Loaded once (persistent)
└── Affects all user interactions

User Prompt:
├── Defines WHAT work to do
├── Changes with each interaction
└── Builds on system prompt foundation
```

## Debugging with the Core 4

When an agent misbehaves, audit the Core 4:

```text
1. Check Context:
   └── Run /context to see what's loaded
   └── Are unused MCP servers consuming tokens?

2. Check Model:
   └── Is Haiku trying to do Opus-level reasoning?
   └── Is cost/speed appropriate for task?

3. Check Prompt:
   └── Is system prompt clear and focused?
   └── Are sub-agents responding to primary, not user?

4. Check Tools:
   └── Run /all-tools to see available options
   └── Are too many tools creating choice paralysis?
```

## Key Takeaways

1. **Everything is Core 4** - Every agent configuration comes down to Context, Model, Prompt, Tools

2. **System ≠ User** - System prompts define agent identity; user prompts define work requests

3. **Information flows matter** - In multi-agent systems, understand who's talking to whom

4. **Focused agents perform better** - Like engineers, agents work best with clear, bounded context

5. **Model selection is strategic** - Don't overpay for Opus when Haiku will work

6. **Tools consume context** - Every MCP server and tool takes space in the agent's mind

7. **Context isolation is powerful** - Sub-agents get fresh starts, preventing context pollution

## Source Attribution

**Primary sources:**
- Custom Agents transcript (Core 4 framework, system prompts, SDK usage)
- Sub-Agents transcript (information flow, context preservation, multi-agent systems)

**Key quotes:**
- "Keep track of the core four. If you understand the core 4 and how each element flows and controls your agent, you will understand compute." (Custom Agents)
- "Context, model, prompt, and specifically the flow of the context, model, and prompt between different agents." (Sub-Agents)

## Related Documentation

- [Progressive Disclosure](progressive-disclosure.md) - Managing context (Core 4 pillar #1)
- [Architecture Reference](architecture.md) - How components use the Core 4
- [Decision Framework](../patterns/decision-framework.md) - Choosing components based on Core 4 needs
- [Context Window Protection](../patterns/context-window-protection.md) - Advanced context management

---

**Remember:** Context, Model, Prompt, Tools. Master these four, and you master Claude Code.
