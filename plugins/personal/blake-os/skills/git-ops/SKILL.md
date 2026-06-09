---
name: git-ops
description: Single front door for everything git and GitHub — saving work, getting the latest, backing up, and putting changes online. Routes plain-language requests to the right operation in the correct order, even when the user does not use git terms. Use whenever the user wants to save, back up, update, sync, upload, publish, or check on their project's files — phrases like "save my work", "back it up", "I'm done", "get the latest", "put it online", "did it save?".
---

# Git Ops (router)

The single front door for all git operations in this repo. The user is **Blake** —
not a developer, so expect plain language, not "commit", "push", or "merge". For
every request:

1. **Translate** what Blake said into one of the three operations (or the full backup).
2. **Run** the right skill(s) in the order that cannot get stuck.
3. **Report back in plain language** — never make Blake read git jargon.

Don't reimplement the git operations here — invoke the leaf skills with the Skill
tool and follow their workflows; they own the actual commands. Decide *which* run
and *in what order*. (Exception: the read-only status check below runs git
directly, since it only looks and changes nothing.)

## The three operations

| Skill | Plain meaning | Run it when Blake wants to… |
|-------|---------------|-----------------------------|
| `blake-os:git-commit` | Save his work into the project's history | save, lock in, record what he did |
| `blake-os:git-sync`   | Pull down the newest version from GitHub | get the latest, see others' changes, refresh |
| `blake-os:git-push`   | Send his saved work up to GitHub | upload, publish, put it online, make it live |

## Read what he meant (intent map)

Match Blake's words to an intent. When more than one could fit, prefer the
**fuller** action — a non-dev who says "save it" usually means "make sure it's
safe," which is the full backup, not just a local commit.

| He says something like… | Intent | What to run |
|-------------------------|--------|-------------|
| "back it up", "save everything", "I'm done", "make sure this is safe", "done for the day", "save and upload" | **Full backup** | the full chain below |
| "save my work", "save this", "record this", "lock it in" (and he clearly means *local only*) | Save | `git-commit` |
| "get the latest", "update", "what changed?", "did anything change online?", "refresh" | Get latest | `git-sync` |
| "upload", "send it", "put it online", "publish", "make it live", "push it up" | Upload | commit first if there are unsaved edits, then `git-push` |
| "is it saved?", "did it work?", "is it backed up?", "what's the status?" | Check | status check (below), then offer the fitting action |
| Anything vague or unclear | **Full backup** | the full chain below — it's always safe |

When in doubt, do the full backup. It never loses work and never gets stuck.

## Capture phrasings that didn't cleanly match

When a request's wording wasn't in the table above and had to be **inferred**
rather than matched, that's a genuinely new phrase worth learning. After the git
work is done, silently hand it to **`blake-os:feedback`** as a `vocabulary` item:
Blake's exact words and the meaning taken from them. Don't ask permission and
don't interrupt — it runs in the background so Brent can fold that wording in for
next time. Skip phrasings the table already covers; `blake-os:feedback` de-dupes,
but there's no need to hand it repeats.

## The full backup chain

Run the leaf skills in **this order** — it is the order that always completes in
one pass:

1. **`blake-os:git-commit`** — save his work first. This is safe even if GitHub
   has newer changes; committing while behind is fine.
2. **`blake-os:git-sync`** — now the working area is clean, so pulling the latest
   always merges cleanly (a dirty working area is the one thing that makes sync
   stall, and step 1 already cleared it).
3. **`blake-os:git-push`** — now everything's up to date, so the upload always succeeds.

Do **not** sync before committing. If there are unsaved edits *and* GitHub also
moved, sync-first hits a dead end ("commit first") and needs a second pass.
Commit-first avoids that every time.

If any step stops and hands off, **stop the chain** — explain in plain language,
and don't push partial state.

## Checking status (no changes made)

When Blake just wants to know where things stand, don't run a leaf skill — read it
directly and translate:

```bash
git fetch origin 2>/dev/null || true
git status --short --branch
git rev-list --left-right --count @{u}...HEAD 2>/dev/null   # "<behind>	<ahead>"
```

Then tell him, for example:

- ahead 0 / behind 0, clean → "Everything's saved and backed up. You're all set."
- ahead 2 / behind 0 → "Your work is saved on this computer but not yet on GitHub. Want me to upload it?"
- behind 3 / ahead 0 → "GitHub has 3 newer changes you don't have yet. Want me to grab them?"
- dirty tree → "You have edits that aren't saved yet. Want me to save and back them up?"

## Speak plain — always

Translate every outcome out of git-speak before reporting it:

| Don't say | Say |
|-----------|-----|
| "Fast-forwarded, behind 0 ahead 0" | "Got the latest — you're up to date." |
| "Created 2 atomic commits" | "Saved your work in 2 chunks." |
| "Pushed to origin, branch current" | "Backed up to GitHub. All safe." |
| "Diverged, created merge commit" | "GitHub had some newer changes — I pulled them in alongside yours." |
| "Working tree dirty" | "You've got edits that aren't saved yet." |
| "Automatic merge hit conflicts, reverted" | "GitHub has a change that overlaps with yours — nothing's lost, your work is saved here. Combining them safely needs a person, so I stopped instead of guessing." |

End a full backup with one reassuring line, e.g. **"All done — your work is saved
and backed up to GitHub."**

## Guardrails — never work around these

When a leaf skill stops, surface it in plain language and end the turn — for an
error, put the exact text beneath the plain summary so Blake can forward it to
Brent. Don't work around a stop by retrying, hand-editing, or dropping to raw git,
and don't reclassify a real stop as "a person needs to do this" to keep moving.
The operations never to run, in any case:

- Never force-push, reset, or rebase.
- Never auto-resolve a merge conflict — guessing a side can silently delete Blake's work.
- Never stage `.env`, keys, tokens, or credential files.
- Never invent a remote or create branches — everything goes to the current branch.
