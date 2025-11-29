# CodeRabbit GitHub Commands Reference

> Complete reference for all `@coderabbitai` commands used in GitHub pull requests and comments.

## Overview

CodeRabbit commands are triggered by mentioning `@coderabbitai` in pull request comments or descriptions. All commands must be used with the `@coderabbitai` mention to trigger CodeRabbit's response.

## Command Categories

- **Review Commands**: Trigger code reviews
- **Control Commands**: Manage review behavior
- **Content Commands**: Generate documentation and summaries
- **Management Commands**: Resolve comments and manage reviews
- **Info Commands**: Get configuration and help

## Review Commands

### @coderabbitai review

**Type:** Review
**Description:** Triggers an incremental review of new changes only
**Usage:** Post as a comment in your pull request
**When to use:**

- Automatic reviews are disabled
- You want to manually request a review of recent changes
- You've made updates and want focused feedback on new code

**Example:**

```

@coderabbitai review

```

**Response time:** Typically completes within a few minutes, depending on PR size and complexity.

### @coderabbitai full review

**Type:** Review
**Description:** Triggers a complete review from scratch
**Usage:** Post as a comment in your pull request
**When to use:**

- You want a comprehensive review of all changes
- Previous review context may be outdated
- You want fresh analysis of the entire PR

**Example:**

```

@coderabbitai full review

```

**Response time:** May take longer than incremental reviews as it analyzes all changes.

## Control Commands

### @coderabbitai pause

**Type:** Control
**Description:** Temporarily stops automatic reviews for this PR
**Usage:** Post as a comment in your pull request
**When to use:**

- You're making rapid changes and want to pause reviews temporarily
- You want to batch changes before review
- Reviews are interfering with your workflow

**Example:**

```

@coderabbitai pause

```

**Response time:** Takes effect immediately.

**Note:** Use `@coderabbitai resume` to restart reviews.

### @coderabbitai resume

**Type:** Control
**Description:** Restarts automatic reviews after pause
**Usage:** Post as a comment in your pull request
**When to use:**

- You've paused reviews and are ready to resume
- You want to re-enable automatic reviews

**Example:**

```

@coderabbitai resume

```

**Response time:** Takes effect immediately.

### @coderabbitai ignore

**Type:** Control
**Description:** Permanently disables automatic reviews for this PR
**Usage:** Add anywhere in the pull request **description** (not comments)
**When to use:**

- Want to handle the review process manually
- PR contains sensitive or experimental code
- Working on a hotfix that needs immediate deployment

**Example:**
Add to PR description:

```

This PR fixes the critical bug.

@coderabbitai ignore

```

**Important:**

- This command must be placed in the PR description, not in comments
- To re-enable reviews, remove this text from the description
- CodeRabbit will not automatically review any commits while this text remains

**Response time:** Takes effect immediately.

## Content Commands

### @coderabbitai summary

**Type:** Content
**Description:** Regenerates the PR summary
**Usage:** Post as a comment in your pull request
**When to use:**

- Summary is outdated after new changes
- You want a fresh summary of the PR
- Summary placeholder was missed initially

**Example:**

```

@coderabbitai summary

```

**Response time:** Typically completes within a few minutes.

**Configuration:** Controlled by `reviews.high_level_summary` and `reviews.high_level_summary_placeholder` settings.

### @coderabbitai generate docstrings

**Type:** Content
**Description:** Generates docstrings for functions and classes in the PR
**Usage:** Post as a comment in your pull request
**When to use:**

- Code lacks proper documentation
- Want consistent docstring formatting
- Need to improve code documentation quickly

**Example:**

```

@coderabbitai generate docstrings

```

**Requirements:**

- Must be enabled in configuration: `reviews.finishing_touches.docstrings.enabled: true`
- Requires Pro plan
- Feature must be enabled in CodeRabbit settings

**What happens:**
1. CodeRabbit scans your changes with ast-grep
2. Identifies functions needing documentation
3. Generates docstrings matching your codebase's format
4. Creates a new branch with changes
5. Opens a PR for your review

**Response time:** Varies based on number of functions and code complexity.

### @coderabbitai generate unit tests

**Type:** Content
**Description:** Generates unit tests for code in the PR
**Usage:** Post as a comment in your pull request
**When to use:**

- New code lacks test coverage
- Want to ensure edge cases are covered
- Need comprehensive test suite

**Example:**

```

@coderabbitai generate unit tests

```

**Requirements:**

- Must be enabled in configuration: `reviews.finishing_touches.unit_tests.enabled: true`
- Requires Pro plan
- Feature must be enabled in CodeRabbit settings

**What happens:**
1. CodeRabbit analyzes your code changes
2. Generates comprehensive test cases
3. Creates a new branch with tests
4. Opens a PR for your review

**Response time:** Varies based on code complexity and number of functions.

### @coderabbitai generate sequence diagram

**Type:** Content
**Description:** Creates a visual sequence diagram showing code flow
**Usage:** Post as a comment in your pull request
**When to use:**

- Want visual representation of code flow
- Need to understand system interactions
- Documentation requires diagrams

**Example:**

```

@coderabbitai generate sequence diagram

```

**Configuration:** Controlled by `reviews.sequence_diagrams` setting.

**Response time:** Typically completes within a few minutes.

## Management Commands

### @coderabbitai resolve

**Type:** Management
**Description:** Resolves all CodeRabbit review comments
**Usage:** Post as a comment in your pull request
**When to use:**

- All CodeRabbit comments have been addressed
- You want to mark all comments as resolved
- Preparing for merge

**Example:**

```

@coderabbitai resolve

```

**Response time:** Takes effect immediately.

**Note:** In GitLab, all discussions must be resolved for `request_changes_workflow` to work.

## Info Commands

### @coderabbitai configuration

**Type:** Info
**Description:** Shows current CodeRabbit configuration settings
**Usage:** Post as a comment in your pull request
**When to use:**

- Want to see what configuration is active
- Debugging configuration issues
- Exporting configuration to YAML file

**Example:**

```

@coderabbitai configuration

```

**Output:** Returns current configuration in YAML format, which can be copied to `.coderabbit.yaml`.

**Response time:** Typically completes within a few seconds.

### @coderabbitai help

**Type:** Info
**Description:** Shows command reference and guidance
**Usage:** Post as a comment in your pull request
**When to use:**

- Need command reference
- Troubleshooting command issues
- Learning available commands

**Example:**

```

@coderabbitai help

```

**Response time:** Takes effect immediately.

## Command Reference Table

| Command | Type | Description | Location |
|---------|------|-------------|----------|
| `@coderabbitai review` | Review | Incremental review of new changes | PR comment |
| `@coderabbitai full review` | Review | Complete review from scratch | PR comment |
| `@coderabbitai pause` | Control | Temporarily stop reviews | PR comment |
| `@coderabbitai resume` | Control | Restart reviews after pause | PR comment |
| `@coderabbitai ignore` | Control | Permanently disable reviews | PR description |
| `@coderabbitai summary` | Content | Regenerate PR summary | PR comment |
| `@coderabbitai generate docstrings` | Content | Generate function documentation | PR comment |
| `@coderabbitai generate unit tests` | Content | Generate test cases | PR comment |
| `@coderabbitai generate sequence diagram` | Content | Create visual diagram | PR comment |
| `@coderabbitai resolve` | Management | Resolve all CR comments | PR comment |
| `@coderabbitai configuration` | Info | Show current settings | PR comment |
| `@coderabbitai help` | Info | Show command reference | PR comment |

## Natural Language Interaction

Beyond commands, you can have natural conversations with CodeRabbit:

### Ask Questions

```

@coderabbitai Why do all of these functions need docstrings? Isn't it obvious enough what they do?

```

CodeRabbit will explain its reasoning and can adjust future behavior based on your feedback.

### Request Explanations

```

@coderabbitai Can you explain why you flagged this as a security issue?

```

### Provide Context

```

@coderabbitai This is a hotfix for production. Please focus on critical issues only.

```

CodeRabbit learns from these interactions and applies preferences to future reviews.

## Command Response Times

**Immediate commands** (take effect right away):

- `@coderabbitai pause`
- `@coderabbitai resume`
- `@coderabbitai ignore`
- `@coderabbitai resolve`
- `@coderabbitai help`

**Quick commands** (typically seconds to minutes):

- `@coderabbitai configuration`
- `@coderabbitai summary`

**Review commands** (typically minutes, depends on PR size):

- `@coderabbitai review`
- `@coderabbitai full review`

**Generation commands** (varies by complexity):

- `@coderabbitai generate docstrings` - Minutes to tens of minutes
- `@coderabbitai generate unit tests` - Minutes to tens of minutes
- `@coderabbitai generate sequence diagram` - Typically minutes

**Factors affecting response time:**

- PR size and complexity
- Number of files changed
- Codebase size and context
- Number of functions to document (for docstrings)
- Code structure complexity

## Troubleshooting

### Command Not Working

If a command doesn't seem to work:

1. **Check repository permissions**: Ensure CodeRabbit has necessary access
2. **Verify command syntax**: Use exact command format with `@coderabbitai`
3. **Look for responses**: Check PR comments for CodeRabbit's response
4. **Use help command**: Run `@coderabbitai help` for guidance
5. **Check configuration**: Some commands require specific settings

### Common Issues

**Command ignored:**

- Ensure `@coderabbitai` is mentioned exactly
- Check that CodeRabbit has repository access
- Verify the command is in the correct location (description vs comment)

**No response:**

- Wait a few minutes for processing
- Check if CodeRabbit is paused or ignored
- Verify repository permissions

**Feature not available:**

- Check if feature requires Pro plan
- Verify feature is enabled in configuration
- Ensure feature is enabled in CodeRabbit settings

## Configuration Dependencies

Many commands are affected by configuration settings:

- **Automatic reviews**: `reviews.auto_review.enabled`
- **Docstring generation**: `reviews.finishing_touches.docstrings.enabled`
- **Unit test generation**: `reviews.finishing_touches.unit_tests.enabled`
- **High-level summaries**: `reviews.high_level_summary`
- **Sequence diagrams**: `reviews.sequence_diagrams`

## Best Practices

1. **Use commands appropriately**: Use review commands when automatic reviews are disabled
2. **Provide context**: Use natural language to give CodeRabbit context about your PR
3. **Be specific**: When asking questions, be specific about what you want to know
4. **Review generated content**: Always review docstrings and tests before merging
5. **Use pause/resume**: Pause reviews during rapid development, resume when ready

## Related Resources

- [Configuration Guide](./configuration/yaml-configuration-guide.md) - Configure CodeRabbit behavior
- [Tools Reference](./configuration/tools-reference.md) - Supported linters and analyzers
- [CodeRabbit Chat Guide](https://docs.coderabbit.ai/guides/agent_chat) - Advanced chat features
- [Best Practices](https://docs.coderabbit.ai/guides/code-review-best-practices) - Code review best practices
