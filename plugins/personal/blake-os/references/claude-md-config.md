# Setting up CLAUDE.md for blake-os

This is a one-time setup note for the `blake-os` tools. If Brent pointed you
here, the goal is to add a few lines to this project's `CLAUDE.md` file so the
tools fire reliably. Have your Claude read this and walk you through it — it can
make the change for you.

## Why this matters

The `blake-os` tools — saving, syncing, backing up, and reporting feedback — are
built as Claude Code *skills*. A skill is offered to Claude with a short
description, and Claude decides on its own whether to use it. The catch is that
Claude will often skip a skill for a task it figures it can just do itself, and
plain git commands are exactly that kind of task. So when you say "save my work,"
Claude might quietly run raw git instead of going through the safe
`blake-os:git-ops` helper — and you'd lose the safety checks, the careful
ordering, and the plain-language explanations these tools exist to give you.

A `CLAUDE.md` file fixes this. Claude reads it at the start of every session and
treats it as standing instructions. By naming the tools there, you turn "Claude
might use the safe helper" into "Claude always does."

## What to add

Add the following to the `CLAUDE.md` file at the top level of this project. If
that file doesn't exist yet, create it; if it already has content, add this as a
new section at the end.

```markdown
## Working with this project

For anything that involves saving, updating, backing up, or putting this project
online, use the `blake-os:git-ops` skill. Do not run git commands directly — the
skill keeps the work safe and explains what it is doing in plain language.

If something is confusing, doesn't work the way it should, breaks, or could be
better, use the `blake-os:feedback` skill so Brent hears about it. He maintains
these tools and uses that feedback to improve them.
```

## What this means in plain terms

Two simple things. First, whenever you want to save or back up your project,
Claude goes through the safe helper instead of doing it the raw way — so your
work is protected and you get told what happened in normal words. Second, if
anything trips you up or feels off, Claude quietly passes a note to Brent so he
can make it better. You don't have to do anything differently; this just makes
the tools dependable.
