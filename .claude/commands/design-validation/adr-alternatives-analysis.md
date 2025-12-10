---
description: Architecture Decision Record - Alternatives Analysis
argument-hint: [decision-title] [context-doc-or-description]
---

# Purpose

Create a formal Architecture Decision Record (ADR) with rigorous alternatives analysis.
This ensures architectural decisions are documented with context, alternatives considered,
and rationale preserved for future reference.

Use this command when making significant architectural decisions that need to be
documented and justified with evidence.

## Variables

DECISION_TITLE: $1 (e.g., "API Gateway Selection", "Database Migration Strategy")
CONTEXT: $2 (file path to context doc OR brief description)
OUTPUT_DIR: `docs/reviews/design-validation/adr/`
FILE_NAME: `adr-<decision-title-slug>.md`

## Instructions

- IMPORTANT: If no `DECISION_TITLE` is provided, stop and ask the user to provide it.
- If `CONTEXT` is a file path, read it first.
- Verify `OUTPUT_DIR` exists, create it if it doesn't.
- Save ADR to `OUTPUT_DIR/FILE_NAME`.
- CRITICAL: Evaluate minimum 3 alternatives, including "do nothing" and existing solutions.
- Be specific with evidence - links, benchmarks, case studies. Generic pros/cons are worthless.

## Workflow

### Step 1: Define Decision Context

Document:

- What decision needs to be made
- Business and technical context
- Decision drivers (requirements, constraints, forces)

### Step 2: Research Alternatives

For EACH alternative (minimum 3):

1. **Description**: What it is, technologies involved
2. **Examples**: Real implementations, tools, or patterns
3. **Pros**: Specific technical benefits with evidence
4. **Cons**: Specific limitations with evidence
5. **Evidence**: Links, benchmarks, case studies

Required alternatives:

- "Do nothing" / status quo
- At least one existing solution (OSS or commercial)
- The proposed custom approach (if any)

### Step 3: Landscape Research

Summarize research across:

- Open-source solutions
- Commercial/SaaS options
- Academic/research findings
- Key insights learned

### Step 4: Decision Rationale

Document:

- Why chosen approach over alternatives
- Specific trade-offs being made
- What you're NOT building (reusing instead)

### Step 5: Validation & Consequences

Define:

- Validation plan before full implementation
- Success criteria
- Positive, negative, and neutral consequences

## Output Format

Save the ADR to `OUTPUT_DIR/FILE_NAME` using this structure:

```markdown
# ADR: [Decision Title]

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: [YYYY-MM-DD]
**Deciders**: [who is involved]

---

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

### Decision Drivers

- [driver 1: e.g., business requirement]
- [driver 2: e.g., technical constraint]
- [driver 3: e.g., timeline pressure]
- [driver 4: e.g., team capability]
- [driver 5: e.g., integration requirement]

---

## Considered Alternatives

### Alternative 1: Do Nothing / Status Quo

**Description**: [Current state and what happens if we don't act]

**Pros**:

- No development effort required
- No new risks introduced
- [other benefits of inaction]

**Cons**:

- [Problem that persists]
- [Opportunity cost]
- [Technical debt accumulation]

**Evidence**: [Current metrics, pain points, incidents]

---

### Alternative 2: [Existing Solution Name]

**Description**: [What it is and how it would work]

**Technologies**: [Specific tools, frameworks, services]

**Examples**: [Real implementations - links to repos, products, case studies]

**Pros**:

- [Specific benefit with evidence]
- [Specific benefit with evidence]
- [Specific benefit with evidence]

**Cons**:

- [Specific limitation with evidence]
- [Specific limitation with evidence]
- [Why rejected, if rejected]

**Evidence**:

- [Link to documentation]
- [Benchmark data]
- [Adoption metrics / community size]

---

### Alternative 3: [Another Option]

**Description**: [What it is and how it would work]

**Technologies**: [Specific tools, frameworks, services]

**Examples**: [Real implementations]

**Pros**:

- [Specific benefit with evidence]
- [Specific benefit with evidence]
- [Specific benefit with evidence]

**Cons**:

- [Specific limitation with evidence]
- [Specific limitation with evidence]
- [Why rejected, if rejected]

**Evidence**:

- [Link to documentation]
- [Benchmark data]
- [Adoption metrics]

---

### Alternative N: [Proposed/Chosen Approach]

**Description**: [What it is and how it would work]

**Technologies**: [Specific tools, frameworks, services]

**Pros**:

- [Specific benefit with evidence]
- [Specific benefit with evidence]
- [Specific benefit with evidence]

**Cons**:

- [Specific limitation - accepted trade-off]
- [Specific limitation - accepted trade-off]

**Evidence**:

- [Supporting research]
- [Similar successful implementations]

---

## Landscape Research Summary

### Open-Source Solutions

| Project | Maturity | Fit | Notes |
|---------|----------|-----|-------|
| [project] | [status] | [%] | [key insight] |

### Commercial/SaaS Options

| Product | Cost | Fit | Notes |
|---------|------|-----|-------|
| [product] | [pricing] | [%] | [key insight] |

### Key Insights

- [What we learned from research]
- [Patterns that work]
- [Anti-patterns to avoid]

---

## Decision

**Chosen Alternative**: [Alternative N]

### Rationale

[Why this alternative best addresses the decision drivers]

### Trade-offs

| Prioritizing | Over |
|--------------|------|
| [value 1] | [value 2] |
| [value 3] | [value 4] |

### What We're NOT Building

| Component | Approach | Source |
|-----------|----------|--------|
| [component] | Reuse | [which solution] |
| [component] | Integrate | [which solution] |
| [component] | Follow standard | [which standard] |

---

## Validation Plan

### Before Full Implementation

- [ ] [PoC experiment]
- [ ] [Technical validation]
- [ ] [Performance test]
- [ ] [Integration test]

### Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| [metric] | [value] | [how measured] |

### Re-evaluation Triggers

- [Condition that would trigger reconsidering]
- [Timeline for review: e.g., 6 months]

---

## Consequences

### Positive

- [Expected benefit]
- [Problem solved]
- [Future opportunity enabled]

### Negative

- [Technical debt accepted]
- [Flexibility reduced]
- [Maintenance burden]

### Neutral

- [Workflow change]
- [Learning curve]

---

## Review Schedule

**Next Review**: [date]
**Review Trigger**: [condition]

---

*This ADR follows the format from [adr.github.io](https://adr.github.io/)*
```
