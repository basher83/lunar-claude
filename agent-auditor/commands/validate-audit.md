---
argument-hint: [skill-path]
description: Run comprehensive skill audit using skill-auditor agent (non-blocking)
---

# Skill Validate Audit

Run comprehensive skill audit using skill-auditor agent (non-blocking).

## Usage

```bash
/meta-claude:skill:validate-audit <skill-path>
```

## What This Does

Invokes the skill-auditor agent to perform comprehensive analysis against official Anthropic specifications:

- Structure validation
- Content quality assessment
- Best practice compliance
- Progressive disclosure design
- Frontmatter completeness

**Note:** This is non-blocking validation - provides recommendations even if prior validation failed.

## Instructions

Your task is to invoke the skill-auditor agent using the Agent tool to audit the skill at `$ARGUMENTS`.

Call the Agent tool with the following prompt:

```text
I need to audit the skill at $ARGUMENTS for compliance with official Claude Code specifications.

Please review:
- SKILL.md structure and organization
- Frontmatter quality and completeness
- Progressive disclosure patterns
- Content clarity and usefulness
- Adherence to best practices

Provide a detailed audit report with recommendations.
```

## Expected Output

The agent will provide:

- Overall assessment (compliant/needs improvement)
- Specific recommendations by category
- Best practice suggestions
- Priority levels for improvements

## Error Handling

**Always succeeds** - audit is purely informational.

Even if the skill has validation failures, the audit provides debugging feedback.

## Examples

**Audit a new skill:**

```bash
/meta-claude:skill:validate-audit plugins/meta/meta-claude/skills/docker-master
# Output: Comprehensive audit report with recommendations
```

**Audit after fixes:**

```bash
/meta-claude:skill:validate-audit plugins/meta/meta-claude/skills/docker-master
# Output: Updated audit showing improvements
```
