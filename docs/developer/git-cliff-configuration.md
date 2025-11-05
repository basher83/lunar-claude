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

**Commit Processing Pipeline**: git-cliff processes commits through a well-defined pipeline:

1. **Preprocessing** (`commit_preprocessors`): Modify raw commit messages (e.g., remove gitmoji, normalize text)
2. **Conventional Parsing** (if `conventional_commits = true`): Parse commits according to Conventional Commits spec
3. **Custom Parsing** (`commit_parsers`): Apply regex-based parsers to group, scope, or skip commits
4. **Link Extraction** (`link_parsers`): Convert text references to clickable links

**When to use Conventional Commits vs Custom Parsers**:

- **Use Conventional Commits** when your project strictly follows the Conventional Commits specification. This provides structured, automated changelog generation with semantic versioning support.
- **Use Custom Parsers** when you need flexibility beyond Conventional Commits, such as:
  - Grouping commits by custom criteria (author, keywords, etc.)
  - Filtering commits that don't fit conventional categories
  - Extracting specific information not covered by conventional commits
  - Supporting legacy commit message formats

**Hybrid Approach**: You can use both! Conventional commits parse first, then custom parsers can override groups or add additional categorization. This is useful for projects transitioning to conventional commits or needing extra categorization.

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

**Authentication Methods**: GitHub integration supports multiple authentication methods (in order of precedence):

1. **Environment variable** (recommended): `GITHUB_TOKEN`
2. **Command-line argument**: `--github-token`
3. **Configuration file**: `token = "..."` (not recommended for security)

**Token Permissions**: No special permissions required. Even a token with no scopes works, providing rate limit increase from 60 to 5000 requests/hour. For private repositories, use a token with `repo` scope.

**Rate Limiting**:

- Unauthenticated: 60 requests/hour
- Authenticated: 5000 requests/hour
- If you hit rate limits, git-cliff will show clear error messages

**Self-Hosted GitHub Enterprise**: Configure custom API URL:

```toml
[remote.github]
owner = "my-org"
repo = "my-repo"
api_url = "https://github.example.com/api/v3"
```

Or via environment variable:

```bash
export GITHUB_API_URL="https://github.example.com/api/v3"
```

**Troubleshooting Authentication**:

- Verify token is valid: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`
- Check rate limit status: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit`
- Ensure repository is accessible with the provided token
- For Enterprise instances, verify `api_url` is correct

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

**Available Template Context Variables**:

**Release-level variables**:

- `version` - Release version string (e.g., "v1.0.0")
- `message` - Tag message (if annotated tag)
- `commits` - Array of commit objects
- `commit_id` - SHA of the release commit
- `timestamp` - Release timestamp (Unix epoch)
- `previous` - Previous release object (if exists)
- `repository` - Repository path

**Commit-level variables**:

- `id` - Commit hash
- `group` - Commit group (from parsers)
- `scope` - Commit scope (from conventional commits or parsers)
- `message` - Commit message
- `body` - Commit body
- `footers` - Array of footer objects
- `breaking` - Boolean indicating breaking change
- `breaking_description` - Description of breaking change
- `conventional` - Boolean indicating conventional commit
- `merge_commit` - Boolean indicating merge commit
- `author` - Author object (`name`, `email`, `timestamp`)
- `committer` - Committer object (`name`, `email`, `timestamp`)
- `remote` - Remote platform data (if enabled):
  - `username` - GitHub/GitLab username
  - `pr_number` - Associated PR/MR number
  - `pr_title` - PR/MR title
  - `pr_labels` - Array of PR/MR labels
  - `is_first_time` - Boolean for first-time contributor

**Platform-specific variables** (when remote integration enabled):

- `github.contributors` - Array of contributor objects
- `gitlab.contributors` - Array of contributor objects
- `gitea.contributors` - Array of contributor objects
- `bitbucket.contributors` - Array of contributor objects

**Useful Tera Template Filters**:

- `upper_first` - Capitalize first letter
- `trim` - Remove leading/trailing whitespace
- `striptags` - Remove HTML tags
- `date(format="%Y-%m-%d")` - Format timestamp
- `group_by(attribute="group")` - Group commits by attribute
- `filter(attribute="merge_commit", value=false)` - Filter commits
- `length` - Get array/string length
- `trim_start_matches(pat="v")` - Remove prefix pattern

**Advanced Template Patterns**:

```jinja
{# Conditional rendering based on version #}
{% if version %}
## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}
## [Unreleased]
{% endif %}

{# Group commits by type #}
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | striptags | trim | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }}
{% endfor %}
{% endfor %}

{# Handle breaking changes #}
{% if commit.breaking %}
**BREAKING CHANGE**: {{ commit.breaking_description }}
{% endif %}

{# Use remote data when available #}
{% if commit.remote.pr_number %}
{{ commit.message }} ([#{{ commit.remote.pr_number }}]({{ repo_url }}/pull/{{ commit.remote.pr_number }}))
{% endif %}

{# Show first-time contributors #}
{% if github.contributors | filter(attribute="is_first_time", value=true) | length != 0 %}
### New Contributors
{% for contributor in github.contributors | filter(attribute="is_first_time", value=true) %}
- @{{ contributor.username }} made their first contribution
{% endfor %}
{% endif %}
```

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

### Configuration Sources and Precedence

git-cliff loads configuration from multiple sources in order of precedence (later sources override earlier ones):

1. **Command-line arguments** - Highest precedence
2. **Environment variables** - Using `GIT_CLIFF__` prefix with `__` as separator
3. **Configuration file** (`cliff.toml`) - Primary configuration source
4. **Project manifests** - `Cargo.toml` (for Rust projects) or `pyproject.toml` (for Python projects)
5. **Default configuration** - Built-in defaults

**Environment variable syntax**: Use double underscores (`__`) to represent nested configuration:

```bash
# Override changelog footer
export GIT_CLIFF__CHANGELOG__FOOTER="Custom footer"

# Override GitHub repository
export GIT_CLIFF__REMOTE__GITHUB__OWNER="my-org"
export GIT_CLIFF__REMOTE__GITHUB__REPO="my-repo"

# Override tag pattern
export GIT_CLIFF__GIT__TAG_PATTERN="v[0-9]+\\.[0-9]+\\.[0-9]+"
```

**Project manifest configuration** (optional):

```toml
# Cargo.toml
[package.metadata.git-cliff]
[package.metadata.git-cliff.git]
conventional_commits = true

# pyproject.toml
[tool.git-cliff]
[tool.git-cliff.git]
conventional_commits = true
```

### [changelog] Section

| Option | Value | Purpose |
|--------|-------|---------|
| `header` | Changelog title + Keep a Changelog link | One-time header at file top |
| `body` | Tera template | Renders each release section |
| `footer` | HTML comment | Attribution footer |
| `trim` | `true` | Remove leading/trailing whitespace |
| `render_always` | `false` | Render body even when no releases exist |
| `postprocessors` | Array of text processors | Apply regex replacements after rendering |
| `output` | File path (optional) | Custom output file location |

### [git] Section - Commit Parsing

| Option | Value | Purpose |
|--------|-------|---------|
| `conventional_commits` | `true` | Parse conventional commit format |
| `filter_unconventional` | `true` | Hide non-conventional commits |
| `require_conventional` | `false` | Fail if non-conventional commits found |
| `split_commits` | `false` | Treat each line as separate commit |
| `sort_commits` | `"oldest"` | Display commits chronologically |
| `protect_breaking_commits` | `true` | Never skip breaking changes |
| `filter_commits` | `false` | Exclude commits not matched by parsers |
| `tag_pattern` | `"v[0-9]+\\.[0-9]+\\.[0-9]+"` | Match semantic version tags |
| `skip_tags` | Regex (optional) | Tags to skip (pre-releases) |
| `ignore_tags` | Regex (optional) | Tags to ignore completely |
| `topo_order` | `false` | Sort tags topologically |
| `topo_order_commits` | `false` | Sort commits topologically |
| `limit_commits` | Number (optional) | Maximum commits to include |
| `recurse_submodules` | `false` | Process submodule commits |

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

## Common Configuration Mistakes

New developers often encounter these configuration pitfalls:

### Forgetting to Enable Conventional Commits

**Problem**: Commits aren't being parsed correctly, or changelog is empty.

**Solution**: Ensure `conventional_commits = true` is set in `[git]` section:

```toml
[git]
conventional_commits = true  # Must be explicitly enabled
```

### Misunderstanding `filter_unconventional` vs `require_conventional`

**Problem**: Confusion about which setting to use.

**Solution**:

- `filter_unconventional = true`: Silently excludes non-conventional commits (default behavior)
- `require_conventional = true`: **Fails** changelog generation if any non-conventional commits are found (stricter)

Use `require_conventional` only when you want to enforce strict compliance. For gradual adoption, use `filter_unconventional`.

### Incorrect Regex Patterns in Commit Parsers

**Problem**: Commits not matching expected patterns, or parser errors.

**Common mistakes**:

- Forgetting to escape special characters: `^feat(` should be `^feat\(`
- Using wrong regex syntax: TOML strings need double backslashes for regex escapes
- Case sensitivity: `^Feat` won't match `feat:`

**Solution**: Test regex patterns carefully:

```toml
# Correct: Escaped parentheses
{ message = "^feat\\(.*\\):", group = "Features" }

# Correct: Double backslash for regex
{ message = "^fix.*security", group = "Security" }

# Wrong: Unescaped parentheses
{ message = "^feat(.*):", group = "Features" }  # TOML parse error
```

### Order of Commit Parsers Matters

**Problem**: Commits appearing in wrong groups or being skipped unexpectedly.

**Solution**: Parsers are evaluated **in order** - first match wins. Place more specific patterns before general ones:

```toml
commit_parsers = [
  # Specific patterns first
  { message = "^fix.*security", group = "Security" },
  { message = "^feat\\(.*\\)!:", group = "Breaking Changes" },

  # General patterns after
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },

  # Skip rules at the end
  { message = "^chore\\(release\\):", skip = true },
]
```

### Environment Variable Format Mistakes

**Problem**: Environment variables not being applied.

**Solution**: Use double underscores (`__`) for nested configuration:

```bash
# Correct
export GIT_CLIFF__CHANGELOG__FOOTER="Custom footer"
export GIT_CLIFF__GIT__TAG_PATTERN="v[0-9]+\\.[0-9]+\\.[0-9]+"

# Wrong (single underscore)
export GIT_CLIFF_CHANGELOG_FOOTER="Custom footer"  # Won't work
```

### Breaking Changes Being Skipped

**Problem**: Breaking changes not appearing in changelog.

**Solution**: Ensure `protect_breaking_commits = true` is set:

```toml
[git]
protect_breaking_commits = true  # Prevents breaking changes from being skipped
```

This ensures breaking changes are never excluded, even if they match a `skip = true` parser.

### Filter Commits Too Aggressively

**Problem**: Important commits missing from changelog.

**Solution**: Be careful with `filter_commits = true`. When enabled, commits not matched by any parser are excluded:

```toml
[git]
filter_commits = false  # Keep false unless you have comprehensive parser coverage
```

Only enable `filter_commits = true` when you have parsers that match all commit types you want to include.

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

**Template Postprocessors**: After rendering, you can apply regex-based postprocessors to modify the final output:

```toml
[changelog]
postprocessors = [
  # Replace placeholder with actual URL
  { pattern = '<REPO>', replace = "https://github.com/user/repo" },
  # Replace date placeholder
  { pattern = '<DATE>', replace = "2024-01-01" },
]
```

This is useful for:

- Replacing placeholders with dynamic values
- Formatting text that matches specific patterns
- Running external commands for complex transformations

## Troubleshooting

### "Error: No commits found"

**Causes and Solutions**:

1. **No conventional commits in range**:
   - Check if commits follow conventional format: `git log --oneline`
   - Disable `filter_unconventional` temporarily to see all commits
   - Verify commit range: `git log --oneline HEAD~5..HEAD`

2. **All commits filtered out**:
   - Check if `filter_commits = true` and parsers don't match your commits
   - Review `commit_parsers` patterns for correctness
   - Temporarily disable `filter_commits` to debug

3. **Tag pattern mismatch**:
   - Verify tags match `tag_pattern`: `git tag -l`
   - Check if `skip_tags` or `ignore_tags` are excluding your tags
   - Ensure tag format matches regex pattern

4. **Empty commit range**:
   - Check if you're using `--latest` or `--current` with no tags
   - Verify commit range syntax: `git log --oneline v1.0.0..v2.0.0`

### "TOML parse error"

**Cause**: Special characters in TOML strings need escaping

**Solution**: Escape backslashes and quotes:

- `\` → `\\` (in regex patterns)
- `"` → `\"` (in strings)
- Parentheses in regex: `(` → `\(`

**Example**:

```toml
# Correct
{ message = "^feat\\(.*\\):", group = "Features" }

# Wrong
{ message = "^feat(.*):", group = "Features" }  # Parse error
```

### Regex Pattern Errors

**Symptoms**: Commits not matching expected patterns, or parser errors.

**Common issues**:

- Unescaped special characters in regex
- Incorrect TOML string escaping
- Case sensitivity mismatches

**Solution**:

- Test regex patterns outside git-cliff first
- Use regex testing tools to verify patterns
- Remember TOML requires double backslashes for regex escapes
- Check git-cliff logs with `--verbose` flag for detailed error messages

### Template Rendering Errors

**Symptoms**: Changelog generation fails with template-related errors.

**Common issues**:

- Undefined variables in template
- Incorrect filter usage
- Syntax errors in Tera template

**Solution**:

- Verify all template variables exist in context
- Check Tera template syntax documentation
- Use `--debug` flag to see template context
- Test template changes incrementally

### Empty PR numbers in changelog

**Cause**: Commits were pushed directly, not via pull request

**Solution**: This is normal for direct commits. The template handles this gracefully by showing "made their first
contribution" without PR link.

**To get PR numbers**: Ensure commits come from merged pull requests, not direct pushes to main branch.

### GitHub Rate Limit Errors

**Symptoms**: Errors about API rate limits or 403 Forbidden responses.

**Causes**:

- Unauthenticated requests (60/hour limit)
- Token expired or invalid
- Rate limit exceeded

**Solutions**:

1. **Set GitHub token**:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
mise run changelog
```

1. **Check rate limit status**:

```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

1. **Verify token permissions**: For private repos, ensure token has `repo` scope

2. **Wait for rate limit reset**: Check reset time in rate limit response

### Remote API Errors

**Symptoms**: Errors fetching contributor data or PR information.

**Common causes**:

- Invalid repository configuration
- Network connectivity issues
- Self-hosted instance URL incorrect

**Solutions**:

- Verify `owner` and `repo` in `[remote.github]` section
- Check `api_url` for self-hosted instances
- Test API access: `curl https://api.github.com/repos/owner/repo`
- Check git-cliff logs with `--verbose` for detailed error messages

### Permission Errors

**Symptoms**: Cannot write to CHANGELOG.md or access repository.

**Solutions**:

- Check file permissions: `ls -l CHANGELOG.md`
- Ensure repository is accessible
- Verify Git repository is initialized: `git status`
- Check if running in correct directory

### Tag Pattern Not Matching

**Symptoms**: Tags not appearing in changelog or wrong tags included.

**Solutions**:

- List all tags: `git tag -l`
- Verify tag format matches `tag_pattern` regex
- Check if `skip_tags` or `ignore_tags` are excluding tags
- Test regex pattern: `echo "v1.0.0" | grep -E "v[0-9]+\.[0-9]+\.[0-9]+"`

### Commits in Wrong Groups

**Symptoms**: Commits appearing in unexpected groups.

**Solutions**:

- Check parser order (first match wins)
- Verify regex patterns match intended commits
- Review `commit_preprocessors` - they modify messages before parsing
- Use `--debug` flag to see how commits are being parsed

## Advanced Examples

### Monorepo Configuration

For monorepos, you can filter commits by path patterns:

```bash
# Generate changelog for specific package
git-cliff --include-path "packages/my-package/**/*"

# Exclude certain directories
git-cliff --exclude-path "**/tests/**/*" --exclude-path "**/docs/**/*"
```

Or configure in `cliff.toml`:

```toml
[git]
# Note: Path filtering is typically done via CLI args
# But you can use commit parsers to filter by commit message patterns
```

### Complex Commit Grouping

Group commits by multiple criteria:

```toml
[git]
commit_parsers = [
  # Group by type and scope
  { message = "^feat\\(api\\)", group = "API Features" },
  { message = "^feat\\(ui\\)", group = "UI Features" },
  { message = "^feat", group = "Features" },  # Catch-all

  # Group by security relevance
  { message = ".*security.*", group = "Security", scope = "security" },

  # Group by author (if needed)
  # Note: This requires custom logic or preprocessing
]
```

### Custom Versioning Strategies

While git-cliff doesn't automatically bump versions, you can use it to determine version increments:

```bash
# Check what type of changes exist
git-cliff --latest

# Based on output, manually bump version:
# - Breaking changes → Major version
# - Features → Minor version
# - Fixes → Patch version
```

### Integration with CI/CD Pipelines

**GitHub Actions example**:

```yaml
- name: Generate Changelog
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    mise run changelog

- name: Create Release
  if: startsWith(github.ref, 'refs/tags/')
  run: |
    mise run changelog-bump ${GITHUB_REF#refs/tags/v}
    git add CHANGELOG.md
    git commit -m "chore: update changelog for release"
```

**GitLab CI example**:

```yaml
generate_changelog:
  script:
    - export GITLAB_TOKEN=$CI_JOB_TOKEN
    - git-cliff --gitlab-repo $CI_PROJECT_PATH -o CHANGELOG.md
  artifacts:
    paths:
      - CHANGELOG.md
```

### Multi-Repository Setup

For projects spanning multiple repositories:

```bash
# Generate changelog for main repo
cd main-repo && git-cliff -o CHANGELOG.md

# Generate changelog for submodule
cd submodule && git-cliff -o CHANGELOG.md

# Combine manually or use scripts
```

### Custom Release Workflow

Advanced release workflow with validation:

```bash
#!/bin/bash
set -e

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Version must match X.Y.Z format"
  exit 1
fi

# Generate changelog
mise run changelog-bump "$VERSION"

# Review changelog
cat CHANGELOG.md

# Confirm before proceeding
read -p "Proceed with release? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  exit 1
fi

# Commit and tag
git add CHANGELOG.md
git commit -m "chore: release v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

echo "Release v$VERSION prepared. Push with: git push && git push --tags"
```

## References

- [git-cliff Documentation](https://git-cliff.org/docs/)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Tera Template Documentation](https://tera.netlify.app/docs/)

## Summary

The git-cliff configuration in this repository is optimized for:

- **Developer experience**: Clear commit conventions and automated changelog updates
- **Release management**: Semantic versioning support and release workflow integration
- **Transparency**: Contributor attribution and issue/PR linking
- **Flexibility**: Customizable grouping and filtering for different needs
- **Professionalism**: Clean, consistent changelog format following industry standards

By following conventional commits and using the provided mise tasks, changelog maintenance becomes a natural part of
the development workflow rather than a manual chore.
