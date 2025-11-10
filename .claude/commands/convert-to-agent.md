---
argument-hint: [slash-command-file-path]
description: Convert a slash command to a sub-agent definition (project)
---

# Convert Slash Command to Sub-Agent

You are tasked with converting a slash command to a sub-agent definition. This conversion should ONLY happen when appropriate based on the decision criteria.

## Input

You will receive a file path to a slash command file via `$ARGUMENTS`.

## Decision Criteria - MUST VALIDATE FIRST

Before converting, you MUST validate that conversion is appropriate. A slash command should become a sub-agent ONLY when:

**Convert when:**
- ✅ **Parallelization is needed** - "Whenever you see parallel, you should always just think sub-agents"
- ✅ **Context isolation is required** - You want to protect the main context window
- ✅ **Scale/batch operations** - Running the same task multiple times in parallel
- ✅ **You're okay losing context afterward** - Sub-agent context doesn't persist (unless resumable)

**Do NOT convert when:**
- ❌ **One-off task** - Keep as slash command
- ❌ **Context matters later** - Use main conversation instead
- ❌ **Sequential operations** - Keep as slash command or consider skill
- ❌ **Simple repeatable actions** - Keep as slash command

## Critical Anti-Pattern Warning

From official guidance:
> "There are a lot of engineers right now that are going all in on skills. They're converting all their slash commands to skills. I think that's a huge mistake."

The same applies to sub-agents. Do not convert slash commands to sub-agents unless there's a clear need for parallelization or context isolation.

## Conversion Process

### Step 1: Read the slash command file

```bash
Read the file at $ARGUMENTS
```

### Step 2: Orchestrator Detection (Check FIRST)

Immediately after reading the file, analyze the content to detect if this is an orchestrator:

**Check frontmatter:**
- Does `allowed-tools` field contain `Task`?

**Check body content for these keywords:**
- "Task tool"
- "subagent" / "sub-agent"
- "spawn"
- "parallel agent"
- "multiple Task tool"
- "launch all subagents"
- "orchestrate"

**If ANY orchestrator indicator is found:**

**STOP immediately** and inform the user:

```text
⚠️ **Conversion REFUSED: Orchestrator Detected**

This slash command orchestrates other agents (uses Task tool or spawns subagents).

**Problem:** Converting this to a sub-agent would violate the architectural constraint:
"Sub-agents cannot spawn other sub-agents."

**What was detected:**
- [List specific indicators found, e.g., "allowed-tools contains Task", "content mentions 'spawn subagents'"]

**Recommendation:**
- Keep as slash command (orchestrators work well as commands)
- OR convert to a Skill (skills CAN orchestrate sub-agents)

❌ Conversion STOPPED - Do NOT convert orchestrators to sub-agents.
```

Do not proceed if orchestrator is detected. The conversion process ends here.

### Step 3: Ask validation questions

**REQUIRED:** Must use AskUserQuestion tool to ask these questions.

**IMPORTANT:** Do NOT analyze or form an opinion about whether conversion is appropriate. Do NOT show the user your orchestrator detection analysis. Ask the user these questions WITHOUT stating whether you think it's a good candidate:

1. **Need to run multiple instances in parallel?**
2. **Need context isolation from main conversation?**
3. **Can task context be discarded after completion?**
4. **Is this a recurring/repeatable task?**

Use the AskUserQuestion tool to present these questions cleanly to the user. Wait for user answers before proceeding.

### Step 3a: Evaluate based on user answers

After receiving user answers:

If the answer to questions 1 or 2 is NO, **STOP** and inform the user that conversion is not appropriate. Recommend keeping it as a slash command.

If answers indicate conversion is appropriate, proceed to Step 4.

### Step 4: Transform the structure

If conversion is validated, perform the following transformation:

**From Slash Command Format:**
```markdown
---
allowed-tools: tool1, tool2
argument-hint: [args]
description: Brief description
model: model-name
disable-model-invocation: false
---

Prompt content here
```

**To Sub-Agent Format:**
```markdown
---
name: agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2
model: model-name
---

System prompt adapted from original prompt content
```

**Field Mapping:**

| Slash Command Field | Sub-Agent Field | Transformation |
|---------------------|-----------------|----------------|
| N/A (derive from filename) | `name` (REQUIRED) | Convert filename to lowercase with hyphens |
| `description` | `description` (REQUIRED) | Enhance to include "when to use" trigger language. Add phrases like "use PROACTIVELY" if appropriate |
| `allowed-tools` | `tools` (OPTIONAL) | Direct copy. Omit if it should inherit all tools |
| `model` | `model` (OPTIONAL) | Direct copy or use 'inherit'. Omit to default to sonnet |
| `argument-hint` | N/A | Remove - sub-agents don't use this field |
| `disable-model-invocation` | N/A | Remove - sub-agents don't use this field |
| Prompt body | System prompt body | Adapt prompt to be a system prompt. Change from task-oriented to role-oriented language |

**Prompt Adaptation Guidelines:**

1. **Task → Role**: Convert from "Do this task" to "You are an expert who does this"
2. **Add structure**: Include sections like "When invoked:", "Process:", "Provide:", etc.
3. **Be explicit**: Sub-agents need clear guidance on their role and approach
4. **Remove arguments**: Sub-agents receive prompts, not CLI-style arguments

### Step 5: Output location

Determine output location:

- **Project sub-agent**: `.claude/agents/[agent-name].md` (available in current project)
- **User sub-agent**: `~/.claude/agents/[agent-name].md` (available across all projects)

Ask the user which scope they prefer.

### Step 6: Create the sub-agent file

Write the converted content to the appropriate location using the Write tool.

### Step 7: Inform user

Provide summary:

```bash
✓ Converted slash command to sub-agent

  Location: [path]
  Name: [agent-name]
  Description: [description]

  Usage:
  - Automatic: Claude will invoke when appropriate based on description
  - Explicit: "Use the [agent-name] subagent to [task]"

  Note: This sub-agent operates with isolated context. Results won't persist in main conversation unless you use resumable sub-agents.
```

## Example Conversion

**Input (slash command):**
```markdown
---
description: Review code for security and quality
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
```

**Output (sub-agent):**
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

## Remember

**Golden Rule:** "Always start with prompts. Master the primitive first."

Only convert when there's a clear need for parallelization or context isolation. When in doubt, keep it as a slash command.
