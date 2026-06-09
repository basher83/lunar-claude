---
paths: plugins/**/skills/**/*.md
---

# SKILL.md Authoring Standards

A SKILL.md body is instructions to the agent that runs the skill. Write it as
directives, not description.

## Directive prose

Write instructions in the imperative: "Translate the request", "Stop and report",
"Stage explicit paths". Don't address the agent in the second person ("You are…",
"Your job is…", "you must…") or narrate passively.

Reserve "you/your" for text the skill tells the agent to **say to the end user** —
quoted, user-facing messages. There, second person is correct.

## No meta-narration

Instruct; don't announce what a section is for. Cut sentences like "This section
exists to…", "The job is…", "This skill will help you…", and headings like
"(the important part)". If a sentence describes the section instead of telling the
agent what to do, delete it. Keep a short "why" only where the reasoning changes
behavior.

## Fold redundancy

State a rule or rationale in one authoritative place. Don't restate it across
sections or files — point to the owner instead. When a skill delegates detail to a
`references/` file, link to it rather than re-summarizing its contents.

Exception: a terse guardrail block near the bottom that restates the critical
"never" rules is deliberate anchoring, not redundancy.

## Anchor guardrails top or bottom

Put behavioral guardrails, safety constraints, and critical stop-conditions at the
top or bottom of the file — never buried in the middle, where attention is weakest.
A stop-condition bound to a specific step may stay inline in that step.

## Don't over-guard

A guard should be explicit, bounded, and observable. Don't pile on brittle
procedural rules. Test each constraint: does it protect a real risk, or a
hypothetical one? Over-constraining a capable model reduces performance.
