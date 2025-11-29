---
name: coderabbit
description: >
  AI-powered code review using CodeRabbit CLI and GitHub integration. Use when running
  local code reviews before commits ("run coderabbit", "review my changes"), configuring
  .coderabbit.yaml files, integrating CodeRabbit with Claude Code for autonomous review
  workflows, or using @coderabbitai commands in pull requests.
---

# CodeRabbit Integration

Run AI code reviews locally and integrate with Claude Code for autonomous fix-and-review workflows.

## Quick Start

### Run Local Review

```bash
# Interactive mode (default)
coderabbit

# Plain text for reading output
coderabbit --plain

# For Claude Code integration (token-efficient)
coderabbit --prompt-only
```

### Specify What to Review

```bash
# Only uncommitted changes
coderabbit --type uncommitted

# Only committed changes (vs base branch)
coderabbit --type committed

# Specify base branch (if not main)
coderabbit --base develop
```

## Claude Code Integration Workflow

When implementing features with CodeRabbit review:

```text
Implement [feature] and then run coderabbit --prompt-only,
let it run as long as it needs (run it in the background) and fix any issues.
```

**Key components:**

1. Use `--prompt-only` for AI-optimized output
2. Run in background (reviews take 7-30+ minutes)
3. Fix critical issues, ignore nits
4. Run verification pass if needed

**Workflow details:** See [references/claude-code-integration.md](references/claude-code-integration.md)

## Configuration

Create `.coderabbit.yaml` in repository root:

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
reviews:
  profile: chill  # or "assertive" for comprehensive feedback
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
    enabled: true  # Auto-detects CLAUDE.md, .cursorrules, etc.
```

**Full configuration guide:** See [references/yaml-configuration-guide.md](references/yaml-configuration-guide.md)

## GitHub PR Commands

Use `@coderabbitai` in PR comments:

| Command | Description |
|---------|-------------|
| `@coderabbitai review` | Trigger incremental review |
| `@coderabbitai full review` | Complete review from scratch |
| `@coderabbitai pause` | Stop automatic reviews |
| `@coderabbitai resume` | Restart reviews |
| `@coderabbitai resolve` | Mark all comments resolved |
| `@coderabbitai generate docstrings` | Generate documentation |
| `@coderabbitai generate unit tests` | Generate tests |

**Full command reference:** See [references/github-commands.md](references/github-commands.md)

## Supported Tools

CodeRabbit integrates 40+ linters and security analyzers:

- **JavaScript/TypeScript:** ESLint, Biome, Oxlint
- **Python:** Ruff, Pylint, Flake8
- **Go:** golangci-lint
- **Security:** Gitleaks, Semgrep, OSV Scanner
- **Infrastructure:** Checkov, Hadolint
- **CI/CD:** actionlint, CircleCI

**Full tools reference:** See [references/tools-reference.md](references/tools-reference.md)

## Troubleshooting

**CodeRabbit not finding issues:**

1. Check auth: `coderabbit auth status`
2. Verify git status: `git status`
3. Specify review type: `--type uncommitted`
4. Specify base branch: `--base develop`

**Claude Code not applying fixes:**

1. Use `--prompt-only` mode
2. Include "run in background" in prompt
3. Explicitly ask to "fix issues found by CodeRabbit"
