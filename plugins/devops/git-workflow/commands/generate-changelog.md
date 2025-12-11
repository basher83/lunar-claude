---
description: Generate changelog using git-cliff, optionally bump version tag
argument-hint: "[--preview] | [--commit] | [--release patch|minor|major]"
allowed-tools: Bash(git-cliff:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Bash(git tag:*), Bash(git describe:*), Read
model: sonnet
---

# Generate Changelog

Generate or update CHANGELOG.md using git-cliff based on conventional commits.

**Typical workflow:** Run after `/git-commit` or commit-craft agent, before pushing to remote.

## Current State

- Recent commits: !`git log --oneline -10`
- Current branch: !`git branch --show-current`
- Latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "No tags yet"`
- Unpushed commits: !`git log --oneline @{u}..HEAD 2>/dev/null || echo "No upstream or no unpushed commits"`

## Arguments

| Argument | Description |
|----------|-------------|
| `--preview` | Show what would be generated without writing |
| `--commit` | Generate changelog and commit it |
| `--release patch` | Changelog + commit + patch tag (0.1.0 → 0.1.1) |
| `--release minor` | Changelog + commit + minor tag (0.1.0 → 0.2.0) |
| `--release major` | Changelog + commit + major tag (0.1.0 → 1.0.0) |
| (no args) | Generate changelog, show diff, prompt before committing |

## Task

Based on `$ARGUMENTS`:

### If `--preview`

Show unreleased changes without writing to file:

```bash
git-cliff --unreleased
```

### If `--commit`

1. Generate the full changelog:

   ```bash
   git-cliff -o CHANGELOG.md
   ```

2. Show what changed:

   ```bash
   git diff CHANGELOG.md
   ```

3. Commit the changelog:

   ```bash
   git add CHANGELOG.md && git commit -m "docs: update changelog"
   ```

### If `--release <level>`

1. Determine new version using git-cliff's native bump:

   ```bash
   # For explicit level (patch/minor/major):
   git-cliff --bump <level> --bumped-version

   # Example outputs:
   # --bump patch → 0.1.1
   # --bump minor → 0.2.0
   # --bump major → 1.0.0
   ```

2. Generate changelog with bumped version:

   ```bash
   git-cliff --bump <level> -o CHANGELOG.md
   ```

3. Show what changed:

   ```bash
   git diff CHANGELOG.md
   ```

4. Commit the changelog:

   ```bash
   git add CHANGELOG.md && git commit -m "docs: update changelog for v<VERSION>"
   ```

5. Create the annotated tag:

   ```bash
   git tag -a v<VERSION> -m "Release v<VERSION>"
   ```

6. Report:
   - Previous version → New version
   - Changelog entries added
   - Remind: `git push && git push --tags`

### Default (no args)

1. Generate the changelog:

   ```bash
   git-cliff -o CHANGELOG.md
   ```

2. Show the diff:

   ```bash
   git diff CHANGELOG.md
   ```

3. Report what was added and ask if user wants to commit or release

## Output

After completion, provide:

- Changelog diff summary (categories and entry count)
- Version change (if releasing): `v0.1.0 → v0.2.0`
- Next step reminder:
  - If committed: "Ready to push with `git push`"
  - If released: "Ready to push with `git push && git push --tags`"
