---
description: Start new ADR - gather context, generate assessment criteria
argument-hint: [decision-topic]
---

Start an Architecture Decision Record workflow for: **$ARGUMENTS**

Use the adr-methodology skill for criteria frameworks and templates.

## Phase 1: Context Gathering

Ask the user to describe:

1. **The Problem**: What architectural decision needs to be made? What's driving the need for a decision now?
2. **Constraints**: Timeline, team size, existing technology stack, budget limitations, compliance requirements
3. **Stakeholders**: Who is affected? Who has decision authority? Who needs to be informed?
4. **Initial Options**: Any solutions already under consideration? Prior art or existing patterns?

Wait for user responses before proceeding. Ask follow-up questions if context is insufficient.

## Phase 2: Framework Selection

Based on the context, recommend an assessment framework:

- **Salesforce Well-Architected** (Trusted/Easy/Adaptable): For enterprise decisions with security, UX, and scale concerns
- **Technical Trade-off** (Operational/Development/Integration): For infrastructure and tooling decisions
- **Custom**: When neither fits, extract 3-5 key decision drivers and create custom criteria

Explain the recommendation and confirm with user.

## Phase 3: Criteria Generation

Generate assessment criteria grouped by the selected framework's pillars. For each criterion:

- **Name**: Clear, specific identifier
- **Rationale**: Why this criterion matters for THIS decision (not generic)
- **Good looks like**: What success means for this criterion

Present criteria as a reviewable list. Ask user to:
- Add missing criteria
- Remove irrelevant criteria
- Adjust importance of criteria

## Phase 4: Save State

After user confirms criteria, write to `.claude/adr-session.yaml`:

```yaml
topic: "[decision topic]"
status: "criteria_defined"
framework: "[salesforce|technical|custom]"
criteria:
  - name: "[criterion name]"
    pillar: "[framework pillar]"
    rationale: "[why it matters]"
    good_looks_like: "[definition of success]"
```

Create the `.claude/` directory if it doesn't exist.

Confirm state saved and instruct user to run `/adr-assistant:analyze` when ready to evaluate options.
