---
name: generate-changelog
description: Generate changelog using git-cliff, optionally bump version tag
context: fork
agent: general-purpose
---

Generate or update CHANGELOG.md using git-cliff based on conventional commits.

Action: $ARGUMENTS

If no action was specified, determine the workflow by asking the user.

## Current State

Branch and status: !`git status -sb`

Recent commits: !`git log --oneline -10`

Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags yet"`

Unpushed commits: !`git log --oneline @{u}..HEAD 2>/dev/null || echo "No upstream or no unpushed commits"`

Working directory: !`git status --porcelain | head -5 || echo "Clean"`

Unreleased changes preview: !`git-cliff --unreleased 2>/dev/null | head -20 || echo "No unreleased changes or git-cliff not configured"`

## Pre-flight Check

If uncommitted changes exist (other than CHANGELOG.md), warn the user and ask whether to continue or abort.

If no conventional commits since last tag, inform user and stop.

## Actions

**preview**: Show unreleased changes with `git-cliff --unreleased`. Report summary and stop.

**generate**: Run `git-cliff -o CHANGELOG.md`, show diff with `git diff CHANGELOG.md`, commit with message `docs: update changelog`.

**release**:

1. Analyze unreleased commits to identify types of changes (breaking, features, fixes, docs, etc.)
2. Check git-cliff recommendation: `git-cliff --bump --bumped-version`
3. Recommend version bump level with reasoning (major/minor/patch) and show proposed version
4. Ask user to confirm or override the bump level
5. Generate changelog: `git-cliff --bump -o CHANGELOG.md`
6. Show diff, commit: `docs: update changelog for v<VERSION>`
7. Create annotated tag: `git tag -a v<VERSION> -m "Release v<VERSION>"`

## Summary

Report changelog diff summary, version change (if releasing), and next step:

- If committed: "Ready to push with `git push`"
- If released: "Ready to push with `git push && git push --tags`"
