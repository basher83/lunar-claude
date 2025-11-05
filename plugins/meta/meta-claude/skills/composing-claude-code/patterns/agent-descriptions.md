# Agent Description Best Practices

**How to write descriptions that trigger agents effectively** - Clear patterns for skill, agent, and tool descriptions.

## Overview

Agent descriptions are the primary mechanism Claude Code uses to decide when to invoke skills, sub-agents, and tools. A good description acts as a **trigger condition** that clearly states when the component should be used.

> "The description field is your agent's job posting. It needs to be specific enough to trigger when needed, but broad enough to handle variations of the same problem."

## The Description Formula

### Basic Structure

```text
[Action verb] when [specific condition or use case]. [Additional context about capabilities].
```

**Example:**

```text
Use when analyzing Python code for security vulnerabilities. Supports static analysis, dependency scanning, and OWASP Top 10 detection.
```

### Key Components

1. **Trigger phrase** - "Use when", "Apply to", "Invoke for"
2. **Specific use case** - What problem does this solve?
3. **Context/scope** - What's included/excluded?
4. **Capabilities** - What can it do?

## Skill Descriptions

Skills appear in SKILL.md frontmatter and help Claude decide which skills to activate.

### Pattern 1: Problem-Focused

**Format:** `Use when [problem] requires [approach]`

**Examples:**

✅ **Good:**

```yaml
description: Use when implementing features requires test-driven development workflow with RED-GREEN-REFACTOR cycle
```

✅ **Good:**

```yaml
description: Apply when debugging issues requires systematic root cause analysis through hypothesis testing
```

❌ **Bad:**

```yaml
description: A skill for testing
```

*Why: Too vague, doesn't specify when to use it*

❌ **Bad:**

```yaml
description: Helps with TDD and testing and writing tests and ensuring code quality
```

*Why: Keyword stuffing, no clear trigger condition*

### Pattern 2: Domain-Focused

**Format:** `Expert guidance for [domain] when [specific task]`

**Examples:**

✅ **Good:**

```yaml
description: Expert guidance for Kubernetes deployments when configuring production clusters with high availability
```

✅ **Good:**

```yaml
description: Infrastructure as code patterns for Terraform when managing multi-region AWS deployments
```

### Pattern 3: Workflow-Focused

**Format:** `[Workflow name] workflow for [outcome] including [steps]`

**Examples:**

✅ **Good:**

```yaml
description: Git worktree workflow for isolated feature development including branch creation, isolation verification, and cleanup
```

✅ **Good:**

```yaml
description: Documentation generation workflow for Python codebases including docstring extraction, type hint analysis, and markdown generation
```

## Sub-Agent Descriptions

Sub-agent descriptions help Claude know when to spawn specialized agents via the Task tool.

### Pattern 1: Task-Specific

**Format:** `[Specific task] that requires [isolation/parallelization/specialization]`

**Examples:**

✅ **Good:**

```yaml
description: Code review agent that analyzes Python files for security and performance issues in isolation
```

✅ **Good:**

```yaml
description: Parallel test runner that executes test suites across multiple files simultaneously
```

### Pattern 2: Scope-Limited

**Format:** `[Role] agent limited to [specific domain/scope]`

**Examples:**

✅ **Good:**

```yaml
description: Documentation analyzer agent limited to markdown files in /docs directory
```

✅ **Good:**

```yaml
description: Dependency audit agent scoped to package.json and requirements.txt analysis
```

### Pattern 3: Capability-Focused

**Format:** `Agent specialized in [capability] without [limitation]`

**Examples:**

✅ **Good:**

```yaml
description: Agent specialized in TypeScript interface generation without modifying existing code
```

✅ **Good:**

```yaml
description: Agent specialized in log parsing and error extraction without executing commands
```

## Common Description Anti-Patterns

### ❌ Anti-Pattern 1: Too Vague

**Bad:**

```yaml
description: Helps with coding tasks
```

**Why:** Claude won't know when to trigger this. Everything is a "coding task."

**Fix:**

```yaml
description: Use when refactoring JavaScript code requires extracting reusable components with minimal API changes
```

### ❌ Anti-Pattern 2: Feature List Without Trigger

**Bad:**

```yaml
description: Provides linting, formatting, type checking, testing, and deployment capabilities
```

**Why:** No clear trigger condition. When should Claude use this vs. individual tools?

**Fix:**

```yaml
description: Use when preparing code for production requires comprehensive quality checks including linting, formatting, type safety, and test coverage
```

### ❌ Anti-Pattern 3: Marketing Speak

**Bad:**

```yaml
description: The ultimate solution for all your DevOps needs with cutting-edge automation
```

**Why:** No specifics. Sounds like marketing copy, not a technical trigger.

**Fix:**

```yaml
description: Use when CI/CD pipeline setup requires GitHub Actions workflow configuration for multi-environment deployments
```

### ❌ Anti-Pattern 4: Tool/Tech List Without Purpose

**Bad:**

```yaml
description: Works with Docker, Kubernetes, Terraform, Ansible, AWS, GCP, Azure
```

**Why:** Lists technologies but not when/why to use them.

**Fix:**

```yaml
description: Use when containerized application deployment requires orchestrating Docker images across Kubernetes clusters in AWS or GCP
```

### ❌ Anti-Pattern 5: Circular Definition

**Bad:**

```yaml
description: Testing skill for when you need to test things
```

**Why:** Defines term using itself. No new information.

**Fix:**

```yaml
description: Use when implementing features requires writing tests first, watching them fail, then writing minimal code to pass (TDD workflow)
```

## Writing Effective Descriptions

### Step 1: Identify the Trigger

Ask: "When would Claude need this?"

**Example thought process:**

- ❌ "When doing Python stuff" → Too vague
- ❌ "When working with APIs" → Still too broad
- ✅ "When validating API responses require JSON schema enforcement" → Specific trigger

### Step 2: Define the Scope

Ask: "What's included? What's excluded?"

**Example:**

```yaml
description: Use when API testing requires schema validation. Includes JSON Schema v7 validation, response structure checking. Excludes load testing and authentication flows.
```

### Step 3: Specify Capabilities

Ask: "What can this actually do?"

**Example:**

```yaml
description: Use when analyzing security vulnerabilities in Python code. Capabilities: SQL injection detection, command injection analysis, crypto weakness identification. Outputs JSON report with CVE references.
```

### Step 4: Test the Trigger

Ask: "Would Claude know when to use this?"

**Test cases:**

- User says: "Check this Python code for SQL injection"
  - Should trigger: ✅ "analyzing security vulnerabilities in Python code"
  - Should not trigger: ❌ "helps with coding tasks"

- User says: "Make this code faster"
  - Should trigger: ✅ "performance optimization for Python applications"
  - Should not trigger: ❌ "helps with coding tasks"

## Examples: Before & After

### Example 1: Generic → Specific

❌ **Before:**

```yaml
name: git-helper
description: Helps with git operations
```

✅ **After:**

```yaml
name: git-worktree-manager
description: Use when feature isolation requires git worktrees with automated branch creation, directory selection, and cleanup verification
```

### Example 2: Feature List → Trigger + Context

❌ **Before:**

```yaml
name: code-quality
description: Linting, formatting, type checking, security scanning, and documentation generation
```

✅ **After:**

```yaml
name: pre-commit-validator
description: Use when committing code requires comprehensive quality gates including linting (ruff), formatting (black), type safety (mypy), and security checks (bandit)
```

### Example 3: Vague Scope → Clear Boundaries

❌ **Before:**

```yaml
name: test-runner
description: Runs tests for your code
```

✅ **After:**

```yaml
name: pytest-parallel-runner
description: Use when test execution requires parallel pytest runs across multiple files with coverage reporting and failure isolation
```

## Description Templates

### Template 1: Problem-Solution

```text
Use when [problem description] requires [solution approach]. Includes [key capabilities]. Excludes [what it doesn't do].
```

### Template 2: Workflow-Oriented

```text
[Workflow name] workflow for [outcome]. Process: [step 1], [step 2], [step 3]. Outputs [result format].
```

### Template 3: Domain-Specific

```text
Expert guidance for [domain/technology] when [specific use case]. Covers [scope]. Follows [standard/best practice].
```

### Template 4: Agent-Specific

```text
[Agent role] specialized in [capability] for [context]. Operates in [mode: isolation/parallel]. Returns [output format].
```

## Testing Your Descriptions

### The Specificity Test

Can you answer these questions clearly?

1. **When:** When would Claude invoke this?
2. **What:** What does it actually do?
3. **Scope:** What's included and excluded?
4. **Output:** What does it produce?

If you can't answer all four clearly, your description needs work.

### The Collision Test

If you have multiple skills/agents, check for overlap:

**Example conflict:**

```yaml
skill-1:
  description: Use when analyzing code for issues

skill-2:
  description: Use when checking code quality
```

Both could trigger for the same request. Make them distinct:

```yaml
skill-1:
  description: Use when analyzing code requires security vulnerability detection (OWASP Top 10, CVE scanning)

skill-2:
  description: Use when checking code requires style/formatting compliance (PEP 8, type hints, docstrings)
```

### The Negative Test

Write descriptions that should NOT trigger for certain requests:

**Example:**

```yaml
description: Use when deploying containerized applications requires Kubernetes manifest generation
```

**Should trigger for:**

- "Create Kubernetes deployment for my app"
- "Generate k8s manifests for production"

**Should NOT trigger for:**

- "Help me write a function" (not deployment)
- "Deploy to Heroku" (not Kubernetes)
- "Check my Docker image" (not manifests/deployment)

## Advanced Patterns

### Pattern: Conditional Triggers

Include multiple trigger conditions:

```yaml
description: Use when (1) implementing features requires TDD workflow, OR (2) existing tests need refactoring for better coverage, OR (3) debugging requires test-based hypothesis validation
```

### Pattern: Explicit Exclusions

State what it doesn't do:

```yaml
description: Use when API integration requires HTTP client setup with auth, retry logic, and error handling. Excludes API design, schema validation, and load testing.
```

### Pattern: Technology-Specific

Target specific tech stacks:

```yaml
description: Use when React component development requires TypeScript strict mode, hooks best practices, and accessibility compliance (WCAG 2.1 AA)
```

### Pattern: Output-Focused

Emphasize what it produces:

```yaml
description: Use when documentation generation requires structured markdown with navigation, API references, and code examples. Outputs Hugo-compatible markdown.
```

## Key Takeaways

1. **Be specific** - Vague descriptions lead to incorrect triggering or no triggering
2. **Focus on the trigger** - Start with "Use when", "Apply when", "Invoke when"
3. **Define scope** - Say what's included AND excluded
4. **Test thoroughly** - Verify trigger conditions with real user requests
5. **Avoid keyword stuffing** - Write clear sentences, not search engine bait
6. **Think about collisions** - Make sure similar skills have distinct triggers

## Reference Examples

### Excellent Descriptions from Real Skills

```yaml
# From superpowers:test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code - write the test first, watch it fail, write minimal code to pass; ensures tests actually verify behavior by requiring failure first
```

```yaml
# From superpowers:systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions
```

```yaml
# From superpowers:brainstorming
description: Use when creating or developing, before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning, alternative exploration, and incremental validation. Don't use during clear 'mechanical' processes
```

These descriptions:

- ✅ State clear trigger conditions
- ✅ Explain when and why to use them
- ✅ Distinguish themselves from other skills
- ✅ Provide context about the workflow

## Next Steps

- See [workflows/agentic-prompt-template.md](../workflows/agentic-prompt-template.md) for prompt structure
- See [anti-patterns/common-mistakes.md](../anti-patterns/common-mistakes.md) for what to avoid
- See [examples/multi-agent-case-studies.md](../examples/multi-agent-case-studies.md) for real implementations
