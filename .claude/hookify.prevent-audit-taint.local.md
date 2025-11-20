---
name: prevent-audit-taint
enabled: true
event: all
tool_matcher: Task
conditions:
  - field: subagent_type
    operator: contains
    pattern: skill-auditor
  - field: prompt
    operator: regex_match
    pattern: ^(?!^[\w\-/\.]+$).+
action: block
---

# ⛔ Audit Context Taint Detected

## CLAUDE.md Audit Protocol Violation

You are attempting to launch an audit agent with a tainted prompt.

## The Problem

**Your prompt string contains more than just the file path.**

The prompt parameter will be sent to the audit agent. Any words beyond the path (like "test", "check if it catches X", "verify the fix") bias the agent's analysis.

**From CLAUDE.md:**

> 1. **ONLY provide the file path** - Nothing else
> 2. **DO NOT mention what you just fixed** - No context about recent changes
> 3. **DO NOT hint at what to look for** - No expectations or guidance
> 4. **DO NOT use words like "test", "verify", "check"** - Taints the agent's objectivity
> 5. **DO NOT explain why you're auditing** - Let the agent form independent conclusions

## What You Should Do

**Correct audit invocation (ONLY the path in prompt):**

```text
Task(subagent_type="meta-claude:skill:skill-auditor-v6", prompt="plugins/meta/meta-claude/skills/skill-factory")
```

**Or:**

```text
@agent-meta-claude:skill:skill-auditor-v6 plugins/meta/meta-claude/skills/skill-factory
```

**Just the path. Nothing else.**

## Why This Matters

The prompt string becomes the agent's task instruction. If you write:

❌ `prompt="Test skill-factory to see if it catches the firecrawl violation"`

The agent will:

- Focus on finding "firecrawl" (confirmation bias)
- May report what you suggested even if not actually violated
- Miss other violations because it's looking for what you mentioned

**Trust but verify. Always audit with untainted prompts.**

---

*This rule enforces the Audit Agent Protocol from CLAUDE.md to ensure objective, unbiased audit results.*
