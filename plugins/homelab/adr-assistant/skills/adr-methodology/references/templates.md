# ADR Templates

## MADR (Markdown Architectural Decision Records)

Primary template for comprehensive decisions. Use for significant architectural choices affecting multiple teams or long-term system direction.

### Complete Structure

```markdown
# [ADR-NNNN] [Title]

**Status:** [Draft | Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]
**Date:** YYYY-MM-DD
**Decision-makers:** [names]
**Consulted:** [names]
**Informed:** [names]

## AI Disclosure

This ADR was drafted with AI assistance (Claude). Assessment criteria and
rationale were reviewed by decision-makers listed above. Final decision
made by humans.

## Context and Problem Statement

[2-3 paragraphs describing the problem, constraints, and why a decision is needed.
Include relevant background, timeline pressures, and scope boundaries.]

## Decision Drivers

- [Driver 1: What matters most]
- [Driver 2: Key constraint]
- [Driver 3: Stakeholder requirement]

## Considered Options

### Option 1: [Name]

[Brief description of the option]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

### Option 2: [Name]

[Brief description]

**Pros:**
- [...]

**Cons:**
- [...]

## Decision

Chosen option: **[Option Name]**

[Rationale explaining why this option was selected, referencing decision drivers
and assessment criteria. Be specific about which trade-offs were accepted and why.]

## Consequences

### What becomes easier

- [Benefit 1]
- [Benefit 2]

### What becomes harder

- [Trade-off 1]
- [Trade-off 2]

### Action items

- [ ] [Implementation step 1]
- [ ] [Implementation step 2]

## Appendix: Assessment Matrix

| Criterion | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|
| [Name]    | Risk: L. [rationale] | Risk: M. [rationale] | Risk: H. [rationale] |

## Related Decisions

- [ADR-XXXX: Related decision]
- [ADR-YYYY: Superseded decision]
```

### Status Values

- **Draft**: Under active discussion
- **Proposed**: Ready for review
- **Accepted**: Approved and active
- **Deprecated**: No longer relevant
- **Superseded**: Replaced by another ADR (link to successor)

## Nygard Template

Minimal template for simpler, contained decisions. Use when context is clear and options are limited.

```markdown
# [Title]

**Status:** [status]
**Date:** YYYY-MM-DD

## Context

[What is the issue that's motivating this decision or change?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

[What becomes easier or more difficult to do because of this change?]
```

## Y-Statement

Single-sentence format for lightweight documentation. Use for small decisions or as summaries.

```text
In the context of [situation],
facing [concern],
we decided for [option]
to achieve [quality],
accepting [downside].
```

### Example

```text
In the context of the user authentication service,
facing scalability concerns with session storage,
we decided for JWT tokens with Redis blacklist
to achieve stateless horizontal scaling,
accepting the complexity of token refresh flows.
```

## Template Selection Guide

| Scenario | Template |
|----------|----------|
| Major architectural change | MADR |
| Cross-team impact | MADR |
| Significant trade-offs | MADR |
| Simple technology choice | Nygard |
| Internal team decision | Nygard |
| Quick reference summary | Y-Statement |
| ADR index entries | Y-Statement |

## File Naming Convention

ADRs should be numbered and named:

```text
docs/adr/
├── 0001-use-postgresql-for-user-data.md
├── 0002-adopt-event-sourcing-for-orders.md
├── 0003-migrate-to-kubernetes.md
└── README.md  # Index of decisions
```

Auto-detect next number by scanning existing files.
