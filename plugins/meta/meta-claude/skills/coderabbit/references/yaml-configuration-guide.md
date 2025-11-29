# CodeRabbit YAML Configuration Guide

> Comprehensive guide to configuring CodeRabbit using `.coderabbit.yaml` with detailed examples and best practices.

## Overview

CodeRabbit's behavior can be customized using a `.coderabbit.yaml` file in your repository root. This file provides version-controlled, team-visible configuration that follows infrastructure-as-code principles.

**Configuration Priority (highest to lowest):**

1. Repository `.coderabbit.yaml` file (highest priority)
2. Central configuration repository (`coderabbit/.coderabbit.yaml`)
3. Repository web interface settings
4. Organization web interface settings
5. Default values (lowest priority)

**Important:** Configuration sources don't merge. The highest priority source completely replaces all lower priority sources.

## Basic Structure

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
tone_instructions: "Be concise and focus on critical issues only"
early_access: false

reviews:
  profile: chill
  high_level_summary: true
  auto_review:
    enabled: true
    drafts: false
  tools:
    eslint:
      enabled: true
    gitleaks:
      enabled: true

knowledge_base:
  opt_out: false
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - "**/CODING_STANDARDS.md"

```

## Global Settings

### Language

Set the language for reviews using ISO language codes:

```yaml
language: en-US  # Options: en-US, en-GB, de-DE, fr-FR, es-ES, ja-JP, etc.

```

### Tone Instructions

Customize the tone and style of CodeRabbit's reviews:

```yaml
tone_instructions: "You are a principal engineer with natural teaching abilities. You detect issues and clearly explain why."

```

**Example tones:**

- `"Be concise and focus on critical issues only"`
- `"Provide detailed explanations with code examples"`
- `"Use a friendly, encouraging tone for junior developers"`

### Early Access

Enable early-access features:

```yaml
early_access: false  # Set to true to enable beta features

```

## Reviews Configuration

### Profile

Control review strictness:

```yaml
reviews:
  profile: chill  # Options: "chill" or "assertive"

```

- **chill**: Focuses on critical issues, reduces noise from minor style violations
- **assertive**: Provides comprehensive feedback including style and best practice suggestions

### High-Level Summary

Generate AI summaries of PR changes:

```yaml
reviews:
  high_level_summary: true
  high_level_summary_placeholder: "@coderabbitai summary"  # Placeholder in PR description
  high_level_summary_in_walkthrough: false  # Include summary in walkthrough comment

```

### Auto Review

Configure automatic review behavior:

```yaml
reviews:
  auto_review:
    enabled: true
    auto_incremental_review: true  # Review on each push
    drafts: false  # Review draft PRs
    ignore_title_keywords:
      - "wip"
      - "draft"
      - "do not review"
    labels:
      - "bug"
      - "!wip"  # Negative match: review all except WIP
    base_branches:
      - "main"
      - "develop"
      - ".*"  # Regex: match all branches
    ignore_usernames:
      - "dependabot[bot]"
      - "renovate[bot]"
      - "ci-bot"

```

**Label matching examples:**

- `['bug', 'feature']` - reviews PRs with 'bug' OR 'feature' label
- `['!wip']` - reviews all PRs except those with 'wip' label
- `['bug', '!wip']` - reviews PRs with 'bug' label but not if they have 'wip' label

### Path Filters

Exclude or include specific file patterns:

```yaml
reviews:
  path_filters:
    - "!node_modules/**"      # Exclude node_modules
    - "!dist/**"              # Exclude dist directory
    - "!**/*.min.js"          # Exclude minified files
    - "src/**"                # Include only src directory
    - "**/*.test.js"          # Include test files

```

**Pattern syntax:**

- `!` prefix excludes files/directories
- `**` matches any directory level
- `*` matches any characters except `/`

### Path Instructions

Provide specific review guidelines for different file paths:

```yaml
reviews:
  path_instructions:
    - path: "src/**/*.{ts,tsx,js}"
      instructions: "Review React.js, TypeScript, JavaScript code for best practices. Check for security vulnerabilities like SQL injection, insecure dependencies, and sensitive data exposure."
    - path: "**/*.py"
      instructions: "Follow PEP 8 style guide. Check for type hints, docstrings, and proper error handling."
    - path: "infrastructure/**/*.tf"
      instructions: "Verify Terraform best practices: use variables, avoid hardcoded values, include descriptions for all resources."

```

**Important:** Path instructions are for HOW to review files, not for referencing guideline files. For coding standards from files, use `knowledge_base.code_guidelines` instead.

### Review Status and Commit Status

Control status reporting:

```yaml
reviews:
  review_status: true        # Post review details on each review
  commit_status: true        # Set commit status to 'pending'/'success'
  fail_commit_status: false   # Set commit status to 'failure' on errors

```

### Walkthrough Options

Customize walkthrough comment content:

```yaml
reviews:
  collapse_walkthrough: false           # Generate in collapsible section
  changed_files_summary: true           # Summary of changed files
  sequence_diagrams: true               # Generate sequence diagrams
  estimate_code_review_effort: true     # Estimate review effort
  assess_linked_issues: true            # Assess how changes address linked issues
  related_issues: true                  # Include related issues
  related_prs: true                     # Include related PRs
  suggested_labels: true                 # Suggest labels
  suggested_reviewers: true              # Suggest reviewers
  auto_apply_labels: false              # Automatically apply suggested labels
  auto_assign_reviewers: false          # Automatically assign reviewers
  poem: true                            # Generate poem in walkthrough
  in_progress_fortune: true             # Post fortune message while reviewing

```

### Labeling Instructions

Provide guidelines for label suggestions:

```yaml
reviews:
  labeling_instructions:
    - label: "frontend"
      instructions: "Apply when the PR contains changes to React components, CSS, or frontend JavaScript files."
    - label: "backend"
      instructions: "Apply when the PR contains changes to API endpoints, database schemas, or server-side logic."
    - label: "security"
      instructions: "Apply when the PR addresses security vulnerabilities or adds security features."

```

### Auto Title Generation

Automatically generate PR titles:

```yaml
reviews:
  auto_title_placeholder: "@coderabbitai"  # Placeholder in PR title
  auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"

```

### Request Changes Workflow

Approve reviews automatically when comments are resolved:

```yaml
reviews:
  request_changes_workflow: false  # Auto-approve when comments resolved

```

**Note:** In GitLab, all discussions must be resolved for this to work.

### Abort on Close

Stop reviews if PR is closed or merged:

```yaml
reviews:
  abort_on_close: true  # Abort in-progress review if PR closed/merged

```

### Cache Control

Disable caching for fresh code downloads:

```yaml
reviews:
  disable_cache: false  # Force fresh download each time

```

## Finishing Touches

Configure automatic docstring and unit test generation:

```yaml
reviews:
  finishing_touches:
    docstrings:
      enabled: true  # Generate docstrings for functions/classes
    unit_tests:
      enabled: true  # Generate unit tests

```

**Note:** These features require Pro plan and can be triggered with `@coderabbitai generate docstrings` or `@coderabbitai generate unit tests`.

## Pre-Merge Checks

Configure quality gates that run before merging:

```yaml
reviews:
  pre_merge_checks:
    docstrings:
      mode: "error"      # Options: "off", "warning", "error"
      threshold: 85      # Percentage threshold (0-100)
    title:
      mode: "warning"
      requirements: "Start with an imperative verb; keep under 50 characters."
    description:
      mode: "error"      # Require PR description
    issue_assessment:
      mode: "warning"    # Assess linked issues
    custom_checks:
      - name: "Undocumented Breaking Changes"
        mode: "error"
        instructions: "All breaking changes to public APIs, CLI flags, environment variables, configuration keys, database schemas, or HTTP/GraphQL endpoints must be documented in the Breaking Change section of the PR description and in CHANGELOG.md."
      - name: "Test Coverage"
        mode: "warning"
        instructions: "New features must include unit tests with at least 80% coverage."

```

**Mode options:**

- `off`: Disabled
- `warning`: Generates warning, doesn't block merge
- `error`: Blocks merge until resolved (if `request_changes_workflow` enabled)

## Tools Configuration

Configure linters and security analyzers. See [Tools Reference](./tools-reference.md) for complete list.

### Basic Tool Configuration

```yaml
reviews:
  tools:
    eslint:
      enabled: true
    ruff:
      enabled: true
    gitleaks:
      enabled: true

```

### Tool-Specific Configuration

Many tools support custom configuration files:

```yaml
reviews:
  tools:
    eslint:
      enabled: true
      # Uses .eslintrc.js, .eslintrc.json, or eslint.config.js automatically
    ruff:
      enabled: true
      config_file: "pyproject.toml"  # Custom config file path
    golangci-lint:
      enabled: true
      config_file: ".golangci.yml"   # Custom config file
    pmd:
      enabled: true
      config_file: "/pmd-config/*.yml"
    swiftlint:
      enabled: true
      config_file: ".swiftlint.yml"
    semgrep:
      enabled: true
      config_file: ".semgrep.yml"

```

### Advanced Tool Configuration

Some tools have additional options:

```yaml
reviews:
  tools:
    ast-grep:
      enabled: true
      rule_dirs: ["rules/"]
      util_dirs: ["utils/"]
      essential_rules: true
      packages: ["common-patterns"]
    languagetool:
      enabled: true
      enabled_rules: ["EN_QUOTES"]
      disabled_rules: ["EN_UNPAIRED_BRACKETS"]
      enabled_categories: ["TYPOS"]
      disabled_categories: ["CASING"]
      enabled_only: false
      level: "default"  # Options: "default", "picky"
    phpstan:
      enabled: true
      level: "max"  # Options: "default", "0"-"9", "max"
    github-checks:
      enabled: true
      timeout_ms: 90000  # Wait up to 90 seconds for GitHub Checks

```

## Knowledge Base Configuration

### Opt Out

Disable all knowledge base features:

```yaml
knowledge_base:
  opt_out: false  # Set to true to disable all knowledge base features

```

**Warning:** If you opt out after opting in, all existing knowledge base data will be removed.

### Web Search

Enable web search for additional context:

```yaml
knowledge_base:
  web_search:
    enabled: true  # Fetch up-to-date information about libraries/frameworks

```

### Code Guidelines

Automatically detect and apply coding standards:

```yaml
knowledge_base:
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - "**/CODING_STANDARDS.md"
      - "**/architecture-pattern.md"
      - "**/technology-stack-and-usage.md"
      - ".github/copilot-instructions.md"
      - "**/CLAUDE.md"
      - "**/GEMINI.md"
      - "**/.cursor/rules/**"
      - "**/.windsurfrules"
      - "**/.clinerules/**"
      - "**/.rules/**"
      - "**/AGENT.md"
      - "**/AGENTS.md"

```

**Auto-detected files (included by default):**

- `**/.cursorrules`
- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `**/CLAUDE.md`
- `**/GEMINI.md`
- `**/.cursor/rules/**`
- `**/.windsurfrules`
- `**/.clinerules/**`
- `**/.rules/**`
- `**/AGENT.md`
- `**/AGENTS.md`

### Learnings

Configure scope of learnings (adaptive configuration from team interactions):

```yaml
knowledge_base:
  learnings:
    scope: "auto"  # Options: "local", "global", "auto"

```

- **local**: Repository-specific learnings only
- **global**: Organization-wide learnings
- **auto**: Repository learnings for public repos, organization learnings for private repos

### Issues

Configure issue tracking scope:

```yaml
knowledge_base:
  issues:
    scope: "auto"  # Options: "local", "global", "auto"

```

### Pull Requests

Configure PR history scope:

```yaml
knowledge_base:
  pull_requests:
    scope: "auto"  # Options: "local", "global", "auto"

```

### Jira Integration

Connect Jira for issue tracking:

```yaml
knowledge_base:
  jira:
    usage: "auto"  # Options: "auto", "enabled", "disabled"
    project_keys:
      - "PROJ"
      - "DEV"

```

**Note:** `auto` disables integration for public repositories.

### Linear Integration

Connect Linear for issue tracking:

```yaml
knowledge_base:
  linear:
    usage: "enabled"  # Options: "auto", "enabled", "disabled"
    team_keys:
      - "ENG"
      - "PROD"

```

### MCP Integration

Configure Model Context Protocol servers:

```yaml
knowledge_base:
  mcp:
    usage: "auto"  # Options: "auto", "enabled", "disabled"
    disabled_servers:
      - "server-name"  # Case-insensitive server labels to disable

```

## Chat Configuration

Configure chat features and integrations:

```yaml
chat:
  art: true              # Generate ASCII/Emoji art in responses
  auto_reply: true       # Reply automatically without @mention
  integrations:
    jira:
      usage: "auto"      # Options: "auto", "enabled", "disabled"
    linear:
      usage: "enabled"   # Options: "auto", "enabled", "disabled"

```

## Code Generation Configuration

Configure docstring and unit test generation:

```yaml
code_generation:
  docstrings:
    language: "en-US"     # ISO language code
    path_instructions:
      - path: "**/*.py"
        instructions: "Use Google-style docstrings with type hints."
      - path: "**/*.js"
        instructions: "Use JSDoc format with @param and @returns tags."
  unit_tests:
    path_instructions:
      - path: "**/*.py"
        instructions: "Use pytest with fixtures. Aim for 90% coverage."
      - path: "**/*.ts"
        instructions: "Use Jest with TypeScript. Mock external dependencies."

```

## Configuration Examples

### Minimal Configuration

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
reviews:
  profile: chill
  auto_review:
    enabled: true

```

### Standard Configuration

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
reviews:
  profile: assertive
  high_level_summary: true
  auto_review:
    enabled: true
    drafts: false
  path_filters:
    - "!node_modules/**"
    - "!dist/**"
  tools:
    eslint:
      enabled: true
    ruff:
      enabled: true
    gitleaks:
      enabled: true
knowledge_base:
  code_guidelines:
    enabled: true

```

### Advanced Configuration

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
tone_instructions: "You are a principal engineer with natural teaching abilities. You detect issues and clearly explain why."
reviews:
  profile: assertive
  high_level_summary: true
  high_level_summary_in_walkthrough: true
  auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"
  collapse_walkthrough: true
  path_filters:
    - "!node_modules/**"
    - "!dist/**"
    - "src/**"
  path_instructions:
    - path: "src/**/*.{ts,tsx}"
      instructions: "Review for React best practices, TypeScript type safety, and security vulnerabilities."
    - path: "**/*.py"
      instructions: "Follow PEP 8, include type hints and docstrings, handle errors properly."
  auto_review:
    enabled: true
    drafts: false
    ignore_title_keywords:
      - "wip"
      - "draft"
    base_branches:
      - "main"
      - "develop"
  tools:
    eslint:
      enabled: true
    ruff:
      enabled: true
      config_file: "pyproject.toml"
    gitleaks:
      enabled: true
    checkov:
      enabled: true
  finishing_touches:
    docstrings:
      enabled: true
    unit_tests:
      enabled: true
  pre_merge_checks:
    docstrings:
      mode: "warning"
      threshold: 80
    title:
      mode: "error"
      requirements: "Use conventional commits: <type>[scope]: <description>"
    description:
      mode: "error"
    custom_checks:
      - name: "Breaking Changes Documentation"
        mode: "error"
        instructions: "All breaking changes must be documented in PR description and CHANGELOG.md"
knowledge_base:
  web_search:
    enabled: true
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - "**/CODING_STANDARDS.md"
      - "**/architecture-pattern.md"
  learnings:
    scope: "global"
  issues:
    scope: "global"
  linear:
    usage: "enabled"
    team_keys:
      - "ENG"
chat:
  art: false
  auto_reply: true
code_generation:
  docstrings:
    language: "en-US"
    path_instructions:
      - path: "**/*.py"
        instructions: "Use Google-style docstrings with type hints."

```

### Team Collaboration Configuration

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
reviews:
  profile: chill
  high_level_summary: true
  suggested_reviewers: true
  auto_assign_reviewers: false
  suggested_labels: true
  auto_apply_labels: false
  finishing_touches:
    docstrings:
      enabled: true
    unit_tests:
      enabled: true
  pre_merge_checks:
    title:
      mode: "error"
      requirements: "Title should follow conventional commit structure"
    description:
      mode: "warning"
chat:
  art: false
  auto_reply: true
  integrations:
    linear:
      usage: "enabled"
knowledge_base:
  web_search:
    enabled: true
  learnings:
    scope: "global"
  issues:
    scope: "global"

```

## Central Configuration

Create organization-wide defaults using a dedicated `coderabbit` repository:

1. Create a repository named `coderabbit` in your organization
2. Add `.coderabbit.yaml` file with organization defaults
3. CodeRabbit automatically applies these settings to repositories without their own config

**Repository override example:**

```yaml
# Repository-specific config (overrides central config)
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
reviews:
  profile: assertive
  tools:
    eslint:
      enabled: true

```

## Remote Configuration

For self-hosted CodeRabbit in air-gapped environments:

```yaml
remote_config:
  url: "https://your-config-location/.coderabbit.yaml"

```

## Best Practices

1. **Use YAML files**: Version-controlled configuration is preferred over UI settings
2. **Start simple**: Begin with minimal config and add complexity as needed
3. **Path filters**: Exclude generated files and dependencies to speed up reviews
4. **Code guidelines**: Let CodeRabbit auto-detect common guideline files
5. **Central config**: Use central configuration for organization defaults
6. **Review regularly**: Update configuration based on team feedback

## Validation

Use CodeRabbit's YAML validator to check your configuration:

- Online: <https://docs.coderabbit.ai/configuration/yaml-validator>
- VS Code: Install YAML extension with schema validation

## Getting Current Configuration

To export your current UI configuration to YAML:

1. Comment `@coderabbitai configuration` on any PR
2. Copy the YAML output
3. Save to `.coderabbit.yaml` in your repository root

## Related Resources

- [Configuration Reference](../referance/configuration.md) - Complete schema reference
- [Tools Reference](./tools-reference.md) - All supported tools and options
- [GitHub Commands Reference](../referance/github-commands.md) - PR command reference
- [Best Practices Guide](https://docs.coderabbit.ai/guides/setup-best-practices) - Official best practices
