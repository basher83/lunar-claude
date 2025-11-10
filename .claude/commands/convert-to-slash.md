---
argument-hint: [agent-file-path]
description: Convert a sub-agent to a slash command (project)
---

# Convert Sub-Agent to Slash Command

You are tasked with converting a sub-agent definition back to a slash command. This conversion should happen when parallelization or context isolation is no longer needed.

## Input

You will receive a file path to a sub-agent file via `$ARGUMENTS`.

## Decision Criteria - MUST VALIDATE FIRST

Before converting, you MUST validate that conversion is appropriate. A sub-agent should become a slash command when:

**Convert when:**
- ✅ **No parallelization needed** - Task runs once, not in parallel batches
- ✅ **Context isolation not required** - Results can stay in main conversation
- ✅ **Simple repeatable action** - One-off or simple recurring task
- ✅ **Sequential operation** - Not part of batch/parallel workflow
- ✅ **Realized it was over-engineered** - Fell into the "converting all commands to agents" anti-pattern

**Do NOT convert when:**
- ❌ **Parallelization is still needed** - Multiple instances running simultaneously
- ❌ **Context isolation is required** - Need to protect main context window
- ❌ **Batch operations at scale** - Processing multiple items in parallel
- ❌ **Complex multi-step workflows** - Might actually need a skill instead

## Recovery Strategy

This command helps recover from the anti-pattern of converting all slash commands to sub-agents. From official guidance:

> "There are a lot of engineers right now that are going all in on skills. They're converting all their slash commands to skills. I think that's a huge mistake."

The same applies to sub-agents. Many tasks work better as simple slash commands.

## Conversion Process

### Step 1: Read the sub-agent file

```bash
Read the file at $ARGUMENTS
```

### Step 2: Analyze and validate

Ask the user these questions to validate conversion is appropriate:

1. **Do you no longer need parallelization** (running multiple instances)?
2. **Do you no longer need context isolation** (results can stay in main conversation)?
3. **Is this actually a simple repeatable task** (not complex orchestration)?
4. **Would this work better as a slash command?**

If the answer to questions 1 and 2 is NO (meaning you still need parallelization/isolation), **STOP** and inform the user that conversion is not appropriate. Recommend keeping it as a sub-agent.

### Step 3: Transform the structure

If conversion is validated, perform the following transformation:

**From Sub-Agent Format:**
```markdown
---
name: agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2
model: model-name
---

System prompt with role-oriented language
```

**To Slash Command Format:**
```markdown
---
description: Brief description of what the command does
allowed-tools: tool1, tool2
model: model-name
---

Task-oriented prompt content
```

**Field Mapping:**

| Sub-Agent Field | Slash Command Field | Transformation |
|-----------------|---------------------|----------------|
| `name` | Filename | Use agent name as filename: `[name].md` |
| `description` | `description` | Simplify and make task-oriented. Remove trigger language like "use PROACTIVELY", "when to invoke", etc. Focus on WHAT it does, not WHEN to use it |
| `tools` | `allowed-tools` | Direct copy |
| `model` | `model` | Direct copy |
| System prompt body | Prompt body | Adapt from role-oriented to task-oriented (see below) |

**Optional Slash Command Fields:**

You may add these fields if appropriate:
- `argument-hint: [args]` - If the command should accept arguments
- `disable-model-invocation: true` - If Claude shouldn't invoke via SlashCommand tool

**Prompt Adaptation Guidelines:**

1. **Role → Task**: Convert from "You are an expert who does this" to "Do this task"
2. **Remove structure**: Remove sections like "When invoked:", "Process:", "Provide:", etc.
3. **Be direct**: Make it action-oriented and concise
4. **Add clarity**: Focus on what to do, not how to be

**Examples:**

| Sub-Agent Prompt | Slash Command Prompt |
|------------------|----------------------|
| "You are a senior code reviewer..." | "Review this code for:" |
| "When invoked: 1. Run git diff..." | "Run git diff and review changes for:" |
| "You are an expert debugger specializing in..." | "Debug this error by:" |

### Step 4: Output location

Determine output location:

- **Project command**: `.claude/commands/[command-name].md` (available in current project)
- **User command**: `~/.claude/commands/[command-name].md` (available across all projects)

Ask the user which scope they prefer. Default to the same scope as the original sub-agent (project → project, user → user).

### Step 5: Create the slash command file

Write the converted content to the appropriate location using the Write tool.

### Step 6: Ask about cleanup

Ask the user: "Do you want to delete the original sub-agent file at [path]?"

If yes, delete the sub-agent file.

### Step 7: Inform user

Provide summary:

```bash
✓ Converted sub-agent to slash command

  Location: [path]
  Command: /[command-name]
  Description: [description]

  Usage:
  - Manual: /[command-name]
  - Via SlashCommand tool: Claude can invoke automatically if description is populated

  Note: This slash command executes in the main conversation context. Results will persist.
```

## Example Conversion

**Input (sub-agent):**
```markdown
---
name: code-reviewer
description: Expert code review specialist. Use proactively after writing or modifying code to review for security, quality, and maintainability.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Security vulnerabilities
- Performance issues
- Code style violations
- Proper error handling
- No exposed secrets or API keys

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

**Output (slash command):**
```markdown
---
description: Review code for security, quality, and maintainability
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
- Proper error handling
- Exposed secrets or API keys

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

## Remember

**Golden Rule:** "Always start with prompts. Master the primitive first."

**Anti-Pattern Recovery:** "Have a strong bias towards slash commands."

Slash commands are the primitive foundation of Claude Code. Many tasks work better as simple commands than as sub-agents.
