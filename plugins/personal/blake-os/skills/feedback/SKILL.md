---
name: feedback
description: Files a GitHub issue on this repo to tell Brent about anything worth his attention — confusion, something that didn't work, an idea or wish, or a new way the user phrased a request. Brent is a collaborator on this private repo and uses these issues to fix and improve the tools. Use this whenever the user sounds confused or frustrated, says something is broken or didn't work as expected, wishes something worked differently, or asks to tell Brent something — even if they never say "feedback" or "issue". Also invoked by blake-os:git-ops to log a request it could not cleanly route.
---

# Feedback (issues router)

File a GitHub issue on this repo whenever something is worth getting back to
**Brent** — friction, a bug, an idea, or a new way the user phrased a request.
He's a collaborator here and uses these issues to fix and improve the tools. The
user is **Blake** — not a developer; never make him deal with GitHub. File the
issue; speak to him in plain language.

## What to file, and how to label it

Match the signal to a type. The label is what lets Brent triage fast.

| What gets noticed… | Type | Label |
|-------------|------|-------|
| They're confused, lost, or "don't get" something | Friction | `friction` |
| Something errored, stopped, or didn't do what they expected | Bug | `bug` |
| "I wish it would…", an idea, a smoother way they wanted | Improvement | `improvement` |
| A phrase `git-ops` had to **guess** at to route (handed off to this skill) | Vocabulary | `vocabulary` |
| Anything else worth Brent seeing | Observation | `observation` |

Capture their **exact words, verbatim** — especially for **vocabulary**. Those
phrasings are what Brent feeds back into the router so it understands them next
time. Never paraphrase the quote.

## Before filing: don't duplicate

Search first. If the same friction or phrasing was already reported, don't open a
second issue — add a short comment so Brent sees it's recurring (frequency tells
him what to fix first).

```bash
gh issue list --search "<key words or the verbatim phrase>" --state all --limit 5
```

- Close match exists → `gh issue comment <number> --body "Heard again: \"<verbatim>\""` and stop.
- No match → file a new one (next section).

## Filing the issue

Confirm there's a repo context, make sure the label exists, then file:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # fails loudly if no repo / no auth

# ensure the label exists (harmless if it already does)
gh label create <label> --color ededed 2>/dev/null || true

gh issue create \
  --title "[<type>] <short scannable summary>" \
  --label "<label>" \
  --body "$(cat <<'EOF'
**What they were doing:** <the task in plain terms>

**What they said (verbatim):** "<their exact words>"

**What happened:** <the outcome, or where it got stuck>

**Their reaction:** <confused / annoyed / fine — only if observed>
EOF
)"
```

Title examples (scannable for Brent at a glance):

- `[vocabulary] "shove my stuff up to the cloud" → meant upload`
- `[friction] didn't understand what "sync" was doing`
- `[bug] stopped on a conflict and they didn't know what to do next`

If `gh` errors (auth, network, no repo), **stop and report the error verbatim** —
don't silently swallow it. A dropped report is worse than a loud failure.

## Talk to them in plain language

They don't need GitHub vocabulary, ever.

| Don't say | Say |
|-----------|-----|
| "I filed issue #42 with the `friction` label." | "Got it — I've let Brent know so he can make this clearer." |
| "Logged a vocabulary observation." | (say nothing — silent capture; see below) |
| "gh issue create failed with 422." | "I couldn't reach Brent's notes just now — I'll mention it: <plain reason>." |

**Friction / bug / improvement** → acknowledge it warmly so they know it landed:
"Thanks — I've passed that to Brent." **Vocabulary / observation** handed over by
the router → file it **silently**; there's no need to interrupt them to note
how they talk.

## Safety

An issue is shared and persistent. Never put **file contents, secrets, tokens,
API keys, or full file paths** in an issue body. Capture *phrasing and context*
only — what they were trying to do and the words they used, nothing from inside
their files.
