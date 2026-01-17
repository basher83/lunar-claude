# Architecture Decision Record Assistant Plugin

## Plugin: `adr-assistant`

### Structure

```text
adr-assistant/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   │   ├── new.md           # /adr-new - Stage 1
│   │   ├── analyze.md       # /adr-analyze - Stage 3
│   │   └── generate.md      # /adr-generate - Stage 5
├── skills/
│   └── adr-methodology/
│       ├── SKILL.md
│       └── references/
│           ├── templates.md
│           ├── criteria-frameworks.md
│           └── risk-ratings.md
└── README.md
```

### plugin.json

```json
{
  "name": "adr-assistant",
  "version": "1.0.0",
  "description": "Human-in-the-loop Architecture Decision Record workflow",
  "author": {
    "name": "basher83"
  },
  "license": "MIT"
}
```

---

### Commands

#### `/adr-new` (Stage 1: Context → Criteria)

```markdown
---
description: Start new ADR - gather context, generate assessment criteria
argument-hint: [decision-topic]
---

You are helping document an architectural decision about: $ARGUMENTS

Use the adr-methodology skill for criteria frameworks.

**Phase 1: Context Gathering**

Ask me to describe:
1. The architectural problem or choice being made
2. Key constraints (timeline, team size, existing stack, budget)
3. Stakeholders affected
4. Any options already under consideration

**Phase 2: Assessment Criteria Generation**

After I provide context, generate assessment criteria grouped by framework pillars. For each criterion:
- Name it clearly
- Explain why it matters for THIS decision
- Note what "good" looks like

Output as a reviewable list. Tell me to refine criteria in conversation before proceeding to `/adr/analyze`.
```

#### `/adr-analyze` (Stage 3: Options Matrix)

```markdown
---
description: Analyze options against criteria with risk ratings
---

Use the adr-methodology skill for risk rating definitions.

**Prerequisites check:**
If no criteria exist in conversation context, tell me to run `/adr-new` first.

**Phase 3: Options Analysis**

For each option under consideration, evaluate against every criterion:

| Criterion | Option A | Option B | ... |
|-----------|----------|----------|-----|
| [name]    | Risk: [L/M/H]. [Rationale] | Risk: [L/M/H]. [Rationale] | |

**Risk Ratings:**
- **Low**: Minimal risk to requirements, performance, or scale
- **Medium**: Manageable risk with proper governance
- **High**: Significant risk without mitigation

After generating the matrix, tell me to refine any assessments in conversation before proceeding to `/adr-generate`.
```

#### `/adr-generate` (Stage 5: Output ADR)

```markdown
---
description: Generate final ADR document from analysis
argument-hint: [output-path]
---

Use the adr-methodology skill for ADR templates.

**Prerequisites check:**
If no options analysis exists in conversation context, tell me to run `/adr-analyze` first.

**Phase 5: ADR Generation**

Generate ADR document using MADR template:

1. **Metadata**: Title, status (Draft), date, decision-makers
2. **AI Disclosure**: Note that Claude assisted with drafting; human reviewed all criteria and rationale
3. **Context**: Summarize the problem from conversation
4. **Options**: Each option with pros/cons from analysis matrix
5. **Decision**: Ask me which option I'm choosing and why
6. **Consequences**: What becomes easier, what becomes harder

Output path: $1 (default: `docs/adr/NNNN-[slugified-title].md`)

Write the file and confirm location.
```

---

### Skill: `adr-methodology`

#### SKILL.md

```markdown
---
name: adr-methodology
description: Use when working with Architecture Decision Records - provides templates, assessment frameworks, and risk rating systems for ADR workflows
---

# ADR Methodology

This skill provides structured frameworks for documenting architectural decisions with human-in-the-loop AI assistance.

## Core Principle

> "The AI can handle the repetitive, boring work of drafting and formatting, but your expertise is what drives quality decisions."

AI assists with:
- Research and enumeration of options
- Consistent formatting
- Risk/trade-off summarization

Humans provide:
- Project-specific context and constraints
- Stakeholder empathy and political nuance
- Final decision accountability

## When to Use This Skill

- Creating new ADRs (`/adr-new`)
- Analyzing architectural options (`/adr-analyze`)
- Generating ADR documents (`/adr-generate`)
- Reviewing or updating existing ADRs

## References

See subdirectory files for:
- `templates.md` - ADR document templates (MADR, Nygard, Y-statement)
- `criteria-frameworks.md` - Assessment criteria organization patterns
- `risk-ratings.md` - Risk rating definitions and usage
```

#### references/templates.md

```markdown
# ADR Templates

## MADR (Markdown Architectural Decision Records)

Primary template for comprehensive decisions.

### Structure

# [Title]

**Status:** [Draft | Proposed | Accepted | Deprecated | Superseded]
**Date:** YYYY-MM-DD
**Decision-makers:** [names]
**Consulted:** [names]
**Informed:** [names]

## AI Disclosure

This ADR was drafted with AI assistance (Claude). Assessment criteria and rationale were reviewed by decision-makers listed above. Final decision made by humans.

## Context and Problem Statement

[2-3 paragraphs describing the problem, constraints, and why a decision is needed]

## Decision Drivers

- [Driver 1]
- [Driver 2]
- ...

## Considered Options

### Option 1: [Name]

**Pros:**
- ...

**Cons:**
- ...

### Option 2: [Name]

...

## Decision

[Option chosen] because [rationale referencing decision drivers and assessment criteria].

## Consequences

### What becomes easier
- ...

### What becomes harder
- ...

## Appendix: Assessment Matrix

[Include full risk-rated matrix from analysis phase]


## Nygard Template

Minimal template for simpler decisions.

# [Title]

**Status:** [status]

## Context

[What is the issue motivating this decision?]

## Decision

[What is the change being proposed?]

## Consequences

[What becomes easier or harder?]


## Y-Statement

Single-sentence format for lightweight documentation.

In the context of [situation], facing [concern], we decided for [option] to achieve [quality], accepting [downside].
```

#### references/criteria-frameworks.md

```markdown
# Assessment Criteria Frameworks

## Salesforce Well-Architected (Trusted/Easy/Adaptable)

Use for enterprise decisions with security, UX, and scale concerns.

### Trusted
- Data security and privacy
- Compliance requirements
- Access control complexity
- Audit and governance

### Easy
- User experience impact
- Deployment complexity
- Integration effort
- Maintenance burden

### Adaptable
- Scalability path
- Future flexibility
- Cost trajectory
- Team skill alignment

## Technical Trade-off Framework

Use for infrastructure and tooling decisions.

### Operational
- Setup complexity
- Maintenance burden
- Monitoring/observability
- Failure modes

### Development
- Learning curve
- Development velocity
- Testing approach
- Documentation quality

### Integration
- Ecosystem compatibility
- Migration path
- Dependency management
- Lock-in risk

## Custom Framework

When neither standard framework fits:

1. Extract 3-5 key decision drivers from context
2. Create criteria that directly measure those drivers
3. Ensure criteria are evaluatable (not vague)
4. Include at least one "reversibility" criterion
```

#### references/risk-ratings.md

```markdown
# Risk Ratings

## Definitions

| Rating | Definition | Governance Required |
|--------|------------|---------------------|
| **Low** | Minimal risk to current or future requirements, performance, or scale | Standard review |
| **Medium** | Manageable risk with proper governance in place | Documented mitigation |
| **High** | Significant risk without active mitigation; may block requirements | Explicit acceptance |

## Usage Guidelines

### Assign Low when:
- Option aligns naturally with constraints
- No significant trade-offs identified
- Team has proven experience
- Reversible if wrong

### Assign Medium when:
- Trade-offs exist but are manageable
- Requires discipline to avoid pitfalls
- Some learning curve involved
- Partially reversible

### Assign High when:
- Directly conflicts with a stated requirement
- Requires significant mitigation effort
- Team lacks experience in area
- Difficult or expensive to reverse

## Rating Consistency

When rating the same criterion across options:
- At least one option should be Low or Medium (otherwise criterion may be irrelevant)
- If all options are High, consider whether the criterion is actually a blocker
- Ratings are relative to THIS decision's context, not absolute
```

---

### README.md

```markdown
# ADR Assistant Plugin

Human-in-the-loop Architecture Decision Record workflow for Claude Code.

## Philosophy

AI assists with research, formatting, and enumeration. Humans provide context, make judgments, and own decisions.

## Workflow

1. `/adr-new [topic]` - Gather context, generate assessment criteria
2. *Refine criteria in conversation*
3. `/adr-analyze` - Generate options matrix with risk ratings
4. *Refine analysis in conversation*
5. `/adr-generate [path]` - Output final ADR document

## Installation

Copy to `~/.claude/plugins/adr-assistant/` or your project's `.claude/plugins/`.

## Customization

Edit `skills/adr-methodology/references/criteria-frameworks.md` to add your organization's assessment frameworks.
```
