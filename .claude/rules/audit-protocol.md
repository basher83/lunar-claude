# Audit Agent Protocol

When invoking ANY audit agent (skill-auditor, command-audit, pr-review, etc.):

1. Provide the file path - Nothing else
2. Do not mention what you just fixed - No context about recent changes
3. Do not hint at what to look for - No expectations or guidance
4. Do not use words like "test", "verify", "check" - Taints the agent's objectivity
5. Do not explain why you're auditing - Let the agent form independent conclusions

## Correct Audit Invocation

```text
plugins/meta/meta-claude/skills/skill-factory
```

## BAD - Tainted Audit Invocation

```text
We just fixed effectiveness issues. Can you audit plugins/meta/meta-claude/skills/skill-factory
to verify the triggers are now concrete?
```

## Why This Matters

Tainted context skews audit results. The agent will look for what you mentioned
instead of finding issues independently. This creates false positives and missed
violations.

**Remember:** Trust but verify. Always audit with untainted context.
