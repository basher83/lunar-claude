# git-cliff Configuration Guide

## Overview

This repository uses [git-cliff](https://git-cliff.org/) to automatically generate and maintain `CHANGELOG.md` from Git
commit history. The configuration follows best practices for conventional commits, GitHub integration, and semantic
versioning.

## Why git-cliff?

**git-cliff** was chosen for several key reasons:

1. **Conventional Commits Support**: Native parsing of conventional commit format without complex regex
2. **Flexibility**: Powerful template system using Tera templates for complete customization
3. **GitHub Integration**: First-class support for PR numbers, contributors, and issue linking
4. **Keep a Changelog Compatible**: Produces output following the Keep a Changelog format
5. **Automation-Friendly**: Integrates seamlessly with CI/CD and release workflows
6. **Performance**: Written in Rust, extremely fast even with large repositories

## Configuration Philosophy

The `cliff.toml` configuration is designed with these principles:

### 1. Conventional Commits as Source of Truth

```toml
[git]
conventional_commits = true
filter_unconventional = true
```

**Why**: Conventional commits provide a structured format that enables automated changelog generation, semantic
versioning, and clear communication about change types.

**Supported commit types**:

- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `docs:` - Documentation changes
- `perf:` - Performance improvements
- `refactor:` - Code refactoring without feature/fix changes
- `test:` - Test additions or modifications
- `ci:` - CI/CD configuration changes
- `build:` - Build system changes
- `chore:` - Maintenance tasks (dependencies, tooling)
- `style:` - Code style changes (formatting, whitespace)

**Breaking changes**: Use `!` suffix (e.g., `feat!:`, `fix!:`) or `BREAKING CHANGE:` footer for major version bumps.

### 2. Hierarchical Grouping with Visual Indicators

```toml
commit_parsers = [
  { message = "^\\w+\\(.*\\)!:", group = "<!-- 0 -->🏗️ Breaking Changes" },
  { message = "^fix.*security", group = "<!-- 1 -->🔒 Security" },
  { message = "^feat", group = "<!-- 2 -->🚀 Features" },
  { message = "^fix", group = "<!-- 3 -->🐛 Bug Fixes" },
  # ... more groups
]
```

**Why**:

- **HTML comments** (`<!-- N -->`) control display order without showing in rendered output
- **Emojis** provide visual scanning for quick category identification
- **Priority ordering** surfaces critical changes first (breaking changes, security fixes)

### 3. Smart Filtering and Noise Reduction

```toml
commit_parsers = [
  # Skip noise commits
  { message = "^chore\\(release\\):", skip = true },
  { message = "^chore\\(deps\\):", skip = true },
  { footer = "^changelog: ?ignore", skip = true },
]
```

**Why**: Release commits and automated dependency updates clutter changelogs. Contributors can explicitly skip commits
using `changelog: ignore` in the commit footer.

**Dependency updates exception**: While automated dependency PRs (like Renovate) are skipped by default, significant
dependency upgrades should use `feat(deps):` or `fix(deps):` to be included.

### 4. GitHub Integration for Attribution

```toml
[remote.github]
owner = "basher83"
repo = "lunar-claude"
```

**Why**: GitHub API integration provides:

- **Author attribution**: Every commit shows the GitHub username
- **PR linking**: Commits from PRs automatically link back to the discussion
- **Contributor recognition**: First-time contributors are highlighted
- **Issue linking**: `#123` references become clickable links

**Security note**: GitHub token should be provided via `GITHUB_TOKEN` environment variable, never hardcoded in
`cliff.toml`.

### 5. Template Customization for Context

```jinja
{%- if commit.scope %}
- **{{ commit.scope }}**: {{ commit.message | upper_first }}\
{%- else %}
- {{ commit.message | upper_first }}\
{%- endif %}
```

**Why**:

- **Scope highlighting**: Scopes (e.g., `feat(api):`) are bolded for clarity
- **Capitalization**: First letter capitalized for professional appearance
- **Merge commit filtering**: `filter(attribute="merge_commit", value=false)` removes noisy merge
  entries

### 6. Preprocessing for Clean Messages

```toml
commit_preprocessors = [
  # Remove gitmoji
  { pattern = ' *(:\w+:|[\p{Emoji_Presentation}\p{Extended_Pictographic}](?:\u{FE0F})?\u{200D}?) *', replace = "" },
  # Clean merge messages
  { pattern = 'Merge pull request #([0-9]+) from.*', replace = "Merged PR #$1" },
]
```

**Why**:

- **Gitmoji removal**: While emojis are useful in commits, they're redundant in the changelog (we use group emojis
  instead)
- **Message normalization**: Standardize merge commit messages for consistency

### 7. Link Parsers for Navigation

```toml
link_parsers = [
  { pattern = "#(\\d+)", href = "https://github.com/basher83/lunar-claude/issues/$1" },
  { pattern = "@([\\w-]+)", href = "https://github.com/$1" },
]
```

**Why**: Converts plain text references into clickable links:

- `#123` → Links to issue/PR #123
- `@username` → Links to GitHub profile

## mise Task Integration

The repository includes two mise tasks for changelog management:

### `mise run changelog`

**Purpose**: Update `CHANGELOG.md` with unreleased commits

**When to use**:

- After committing new changes
- Before creating a pull request
- To preview what will be in the next release

**What it does**:

```bash
git-cliff -o CHANGELOG.md
```

This regenerates the entire changelog, adding new commits to the "Unreleased" section.

### `mise run changelog-bump <version>`

**Purpose**: Create a new release with version number

**When to use**:

- When ready to tag a new release
- As part of the release workflow

**Arguments**:

- `<version>`: Semantic version number (e.g., `0.1.4`)

**What it does**:

```bash
git-cliff --tag "v$VERSION" -o CHANGELOG.md
```

This:

1. Moves unreleased commits to a new version section
2. Adds release date timestamp
3. Prepares the changelog for tagging

**Version validation**: The task validates version format matches `X.Y.Z` pattern.

## Workflow Examples

### Daily Development Workflow

```bash
# 1. Make changes and commit following conventional commits
git add .
git commit -m "feat(plugins): add terraform-provider-netbox plugin"

# 2. Update changelog to see your changes
mise run changelog

# 3. Review CHANGELOG.md
cat CHANGELOG.md

# 4. Create PR or continue development
```

### Release Workflow

```bash
# 1. Ensure all changes are committed
git status

# 2. Update changelog and create release version
mise run changelog-bump 0.2.0

# 3. Review CHANGELOG.md
cat CHANGELOG.md

# 4. Update version in marketplace.json and plugin manifests
# (Manual step - update version fields)

# 5. Commit release
git add CHANGELOG.md .claude-plugin/
git commit -m "chore: release v0.2.0"

# 6. Create annotated tag
git tag -a v0.2.0 -m "Release v0.2.0"

# 7. Push to GitHub
git push && git push --tags
```

### Using GitHub Token for Rich Attribution

```bash
# Export GitHub token (for CI/CD)
export GITHUB_TOKEN="ghp_..."

# Generate changelog with GitHub data
mise run changelog
```

**Token permissions**: No special permissions required - even a token with no scopes works (just for rate limit
increase from 60 to 5000 requests/hour).

### Skipping Commits from Changelog

Sometimes you want to commit something that shouldn't appear in the changelog:

```bash
git commit -m "chore: update local dev notes

This is just updating my personal development notes.

changelog: ignore"
```

The `changelog: ignore` footer tells git-cliff to skip this commit.

## Configuration Breakdown

### [changelog] Section

| Option | Value | Purpose |
|--------|-------|---------|
| `header` | Changelog title + Keep a Changelog link | One-time header at file top |
| `body` | Tera template | Renders each release section |
| `footer` | HTML comment | Attribution footer |
| `trim` | `true` | Remove leading/trailing whitespace |

### [git] Section - Commit Parsing

| Option | Value | Purpose |
|--------|-------|---------|
| `conventional_commits` | `true` | Parse conventional commit format |
| `filter_unconventional` | `true` | Hide non-conventional commits |
| `sort_commits` | `"oldest"` | Display commits chronologically |
| `protect_breaking_commits` | `true` | Never skip breaking changes |
| `tag_pattern` | `"v[0-9]+\\.[0-9]+\\.[0-9]+"` | Match semantic version tags |

### [git.commit_parsers] - Grouping Rules

Evaluated **in order** - first match wins:

1. **Breaking changes** (`!` suffix or `BREAKING CHANGE:` footer) → 🏗️ Breaking Changes
2. **Security fixes** (`fix.*security` or `security` in body) → 🔒 Security
3. **Features** (`feat:`) → 🚀 Features
4. **Bug fixes** (`fix:`) → 🐛 Bug Fixes
5. **Performance** (`perf:`) → ⚡ Performance
6. **Documentation** (`docs:`) → 📚 Documentation
7. **Refactoring** (`refactor:`) → ♻️ Refactor
8. **Testing** (`test:`) → 🧪 Testing
9. **CI/CD** (`ci:`, `build:`) → 👷 CI/CD
10. **Miscellaneous** (`chore:`, `style:`) → 🔧 Miscellaneous

**Skip rules** (bottom of list):

- `chore(release):` - Release commits
- `chore(deps):` - Automated dependency updates
- `changelog: ignore` footer - Explicit skip

## Best Practices

### Writing Good Commit Messages

**Good examples**:

```bash
# Feature with scope
git commit -m "feat(netbox): add PowerDNS integration plugin"

# Bug fix with scope
git commit -m "fix(terraform): correct variable type in proxmox module"

# Breaking change with scope
git commit -m "feat(api)!: change plugin manifest schema to v2"

# Documentation without scope
git commit -m "docs: add git-cliff configuration guide"

# Performance improvement
git commit -m "perf(search): optimize plugin discovery algorithm"
```

**Bad examples**:

```bash
# ❌ Too vague
git commit -m "fix: fix bug"

# ❌ Not conventional
git commit -m "updated the readme"

# ❌ Missing type
git commit -m "add new feature"

# ❌ Missing description
git commit -m "feat(plugin):"
```

### Commit Message Structure

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**Type**: Determines changelog group and semantic version impact

**Scope**: Component/area affected (e.g., `netbox`, `terraform`, `api`, `docs`)

**!**: Breaking change indicator (optional)

**Description**: Imperative mood, lowercase, no period (e.g., "add feature" not "Added feature.")

**Body**: Detailed explanation (optional but recommended for complex changes)

**Footer**: Additional metadata:

- `BREAKING CHANGE: <description>` - Breaking change details
- `Fixes #123` - Links to issue
- `changelog: ignore` - Skip this commit

### Semantic Versioning Impact

Based on commit types:

- **MAJOR** (1.0.0 → 2.0.0): `feat!:`, `fix!:`, or `BREAKING CHANGE:` footer
- **MINOR** (0.1.0 → 0.2.0): `feat:`
- **PATCH** (0.1.0 → 0.1.1): `fix:`, `perf:`
- **No version change**: `docs:`, `chore:`, `refactor:`, `test:`, `ci:`, `build:`, `style:`

**Note**: git-cliff itself doesn't bump versions - it generates changelogs. Version bumping must be done manually via
`mise run changelog-bump <version>`.

## Customization

### Adding New Commit Types

To add a custom commit type:

1. **Add to commit_parsers**:

```toml
{ message = "^design", group = "<!-- 4 -->🎨 Design" },
```

1. **Update this documentation** with the new type

2. **Communicate to team** about the new convention

### Changing Group Order

Modify the HTML comment numbers in `commit_parsers`:

```toml
# Lower numbers appear first
{ message = "^feat", group = "<!-- 0 -->🚀 Features" },  # Now first
{ message = "^fix", group = "<!-- 1 -->🐛 Bug Fixes" },
```

### Removing Emojis

Remove emoji prefixes from group names:

```toml
{ message = "^feat", group = "<!-- 2 -->Features" },
```

### Custom Templates

The `body` template can be completely customized. See
[git-cliff configuration documentation](https://git-cliff.org/docs/configuration/) for available variables and
filters.

## Troubleshooting

### "Error: No commits found"

**Cause**: No conventional commits in range

**Solution**:

- Check if commits follow conventional format
- Disable `filter_unconventional` temporarily to see all commits
- Run `git log --oneline` to verify commit messages

### "TOML parse error"

**Cause**: Special characters in TOML strings need escaping

**Solution**: Escape backslashes and quotes:

- `\` → `\\`
- `"` → `\"`

### Empty PR numbers in changelog

**Cause**: Commits were pushed directly, not via pull request

**Solution**: This is normal for direct commits. The template handles this gracefully by showing "made their first
contribution" without PR link.

### GitHub rate limit errors

**Cause**: Unauthenticated requests limited to 60/hour

**Solution**: Set `GITHUB_TOKEN` environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
mise run changelog
```

## References

- [git-cliff Documentation](https://git-cliff.org/docs/)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

## Summary

The git-cliff configuration in this repository is optimized for:

- **Developer experience**: Clear commit conventions and automated changelog updates
- **Release management**: Semantic versioning support and release workflow integration
- **Transparency**: Contributor attribution and issue/PR linking
- **Flexibility**: Customizable grouping and filtering for different needs
- **Professionalism**: Clean, consistent changelog format following industry standards

By following conventional commits and using the provided mise tasks, changelog maintenance becomes a natural part of
the development workflow rather than a manual chore.
