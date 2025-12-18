---
description: Generate changelog using git-cliff, optionally bump version tag
allowed-tools: Bash(git:*), Bash(git-cliff:*), AskUserQuestion, Read
---

# Generate Changelog

Generate or update CHANGELOG.md using git-cliff based on conventional commits.

**Typical workflow:** Run after `/git-commit` or commit-craft agent, before pushing to remote.

## Current State

- Branch and status: !`git status -sb`
- Recent commits: !`git log --oneline -10`
- Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags yet"`
- Unpushed commits: !`git log --oneline @{u}..HEAD 2>/dev/null || echo "No upstream or no unpushed commits"`
- Working directory: !`git status --porcelain | head -5 || echo "Clean"`
- Unreleased changes preview: !`git-cliff --unreleased 2>/dev/null | head -20 || echo "No unreleased changes or git-cliff not configured"`

## Workflow

### Phase 1: Pre-flight Check

1. If working directory has uncommitted changes (other than CHANGELOG.md), use AskUserQuestion:
   - header: "Uncommitted"
   - question: "You have uncommitted changes. Continue with changelog generation?"
   - options:
     - Continue (Proceed anyway)
     - Abort (Stop and commit changes first)

2. If no conventional commits since last tag, inform user and stop

### Phase 2: Choose Action

Use AskUserQuestion to determine workflow:

- header: "Action"
- question: "What would you like to do with the changelog?"
- options:
  - Preview (Show what would be generated without writing)
  - Generate (Create/update CHANGELOG.md)
  - Release (Generate changelog and create version tag)

### Phase 3: Execute Action

#### If Preview

Show unreleased changes: `git-cliff --unreleased`

Report summary and stop.

#### If Generate

1. Generate changelog: `git-cliff -o CHANGELOG.md`

2. Show diff: `git diff CHANGELOG.md`

3. Commit: `git add CHANGELOG.md && git commit -m "docs: update changelog"`

#### If Release

1. Analyze unreleased commits to provide a recommendation:
   - Review the commits shown in Current State
   - Identify the types of changes (breaking, features, fixes, docs, etc.)
   - Check git-cliff's detection: `git-cliff --bump --bumped-version`

2. Provide a recommendation with reasoning:
   - Summarize what's being released (e.g., "3 features, 5 bug fixes, 2 docs updates")
   - Explain the recommended bump level based on semantic versioning:
     - Major: if breaking changes or `BREAKING CHANGE:` commits present
     - Minor: if new features (`feat:`) without breaking changes
     - Patch: if only fixes, docs, refactors, etc.
   - Show the proposed version: "[CURRENT] → [RECOMMENDED]"

3. Use AskUserQuestion to confirm:
   - header: "Release"
   - question: "Proceed with [RECOMMENDED_LEVEL] release to v[VERSION]?"
   - options:
     - Yes (Create release with recommended version)
     - Patch (Override: bump patch instead)
     - Minor (Override: bump minor instead)
     - Major (Override: bump major instead)

4. Generate changelog with confirmed version: `git-cliff --bump [level] -o CHANGELOG.md`

5. Show diff: `git diff CHANGELOG.md`

6. Commit: `git add CHANGELOG.md && git commit -m "docs: update changelog for v[VERSION]"`

7. Create annotated tag: `git tag -a v[VERSION] -m "Release v[VERSION]"`

8. Report: Previous version → New version

### Phase 4: Summary

Provide completion summary:

- Changelog diff summary (categories and entry count)
- Version change (if releasing): `v0.1.0 → v0.2.0`
- Next step reminder:
  - If committed: "Ready to push with `git push`"
  - If released: "Ready to push with `git push && git push --tags`"
