---
description: Analyze a spec file and generate a deployment plan (flexible structure)
allowed-tools: Bash(git:*), Bash(eza:*), Bash(test:*), Read, Write, Glob, Grep, AskUserQuestion
argument-hint: [spec1.yaml] [spec2.yaml]
---

# Analyze Spec

Generate a deployment plan using soft guidelines with anchored outputs.

## Variables

PLAN_OUTPUT_DIRECTORY: `${CLAUDE_PROJECT_DIR}/.claude/`

## Context

Up to two specs may be given, only one spec is required to proceed.

Spec files:
@${CLAUDE_PLUGIN_ROOT}/specs/$1
@${CLAUDE_PLUGIN_ROOT}/specs/$2

Plan template: @${CLAUDE_PLUGIN_ROOT}/templates/plan-template.md

## Instructions

- Create an implementation plan that is:
  - Concise enough to scan quickly
  - Detailed enough to execute effectively
  - Structured however best fits the content
- Cover: problem, solution, constraints, phases, blockers, risks
- **Required sections must appear exactly as specified:**

```markdown
## Next Action

**Phase:** [N]
**Task:** [Specific, concrete step]
**Command:** [Actual command or file to create]

## Critical Files

| File | Why Critical |
|------|--------------|
| [path] | [reason] |
```

- Save the complete implementation plan to `PLAN_OUTPUT_DIRECTORY/plan.local.md`

## Workflow

0. **Readiness Check** (output before proceeding):
   - What do I know from loaded context? (structure, patterns, constraints)
   - What's unclear or missing for this spec?
   - Key risks I can already identify
   - **Confidence: X/5** - If < 4, use AskUserQuestion to clarify before proceeding

1. **Understand**: Focus on the requirements provided and apply your assigned perspective throughout the design process

2. **Explore Thoroughly**:
   - Read any files provided to you in the initial prompt
   - Find existing patterns and conventions using GLOB, GREP, and READ tools
   - Understand the current architecture

3. **Design**:
   - Create implementation approach based on your perspective
   - Determine phases, dependencies, execution order
   - Consider trade-offs and architectural decisions

4. **Detail the Plan**:
   - Provide step-by-step implementation strategy
   - Identify dependencies and sequencing
   - Anticipate potential challenges
   - Let structure adapt to content—don't force sections that don't fit

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```text
✅ Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/plan.local.md
Topic: <brief description of what the plan covers>
Key Components:
- <main component 1>
- <main component 2>
- <main component 3>
```
