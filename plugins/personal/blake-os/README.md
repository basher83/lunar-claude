# blake-os

Git workflow automation built as a single, plain-language front door — for
someone who isn't a developer. Instead of exposing git terms, blake-os reads what
the user actually means ("save my work", "back it up", "put it online"), runs the
right operations in an order that can't get stuck, and reports back without git
jargon.

## Skills

| Skill | Purpose |
|-------|---------|
| `git-ops` | The front door. Routes plain-language requests to the right operation — or the full backup — and reports back without git jargon. |
| `git-sync` | Brings the branch up to date with origin: fast-forward when behind, merge when diverged. Never rebases or force-pushes. |
| `git-commit` | Creates atomic commits on the current branch, scanning for secrets before staging. |
| `git-push` | Publishes commits to origin only when the branch is current. Never force-pushes. |
| `feedback` | Files a GitHub issue on the repo to report friction, bugs, ideas, and new phrasings, so the maintainer can improve the tools. |

`git-ops` is the only skill the user reaches by intent. The three git operations
are internal steps it sequences, and `feedback` is the channel back to the
maintainer.

## Usage

Just say what you want in plain language — "save my work", "back it up", "get the
latest", "put it online". `git-ops` works out which operation that maps to, runs
it, and explains what happened in normal words. "Back it up" or "I'm done" runs
the full save-and-upload pass.

For a plain-language tour of what to ask for, written to be read aloud to a
non-developer, see [references/what-i-can-do.md](references/what-i-can-do.md).

## Setup

Claude can skip a skill for a task it thinks it can do itself, and plain git is
exactly that kind of task — so add a hard-route to the project's `CLAUDE.md` to
make the tools fire reliably. See
[references/claude-md-config.md](references/claude-md-config.md) for the exact
block and why it matters.

## Safety guarantees

- **No force.** Never `git push --force`, `--force-with-lease`, `reset --hard`, or `rebase`.
- **Fast-forward or merge — never rebase or force.** On a merge conflict, `git-sync` aborts cleanly and hands off rather than guessing.
- **No blind staging.** Commits stage explicit paths only — never `git add -A` or `git add .` — and exclude `.env`, credentials, `*.pem`, `*.key`, and token files.
- **No phantom remotes or branches.** Everything commits to the current branch; no invented `origin`, no feature branches.
- **Loud failure.** Auth errors, rejected pushes, and fetch failures are reported verbatim; the tool stops rather than working around the problem.

## Authorship

Commits are written as if the user wrote them — no co-author trailers, no AI
attribution.

## Installation

```bash
/plugin marketplace add basher83/lunar-claude
/plugin install blake-os@lunar-claude
```
