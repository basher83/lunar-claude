---
description: Analyze options against criteria with risk ratings
---

Continue the ADR workflow by analyzing options against established criteria.

Use the adr-methodology skill for risk rating definitions.

## Prerequisites Check

Read `.claude/adr-session.yaml` to retrieve session state.

If file doesn't exist or status is not `criteria_defined`:
- Inform user that criteria must be defined first
- Instruct them to run `/adr-assistant:new [topic]` to start the workflow
- Stop processing

## Phase 1: Options Enumeration

Display the topic and criteria from state file.

Ask user to list the options under consideration. For each option:
- Name/identifier
- Brief description (1-2 sentences)

If user hasn't identified options, help brainstorm based on the decision context and constraints.

## Phase 2: Risk Assessment

For each option, evaluate against every criterion using risk ratings:

| Rating | Definition |
|--------|------------|
| **Low** | Minimal risk to requirements, performance, or scale |
| **Medium** | Manageable risk with proper governance |
| **High** | Significant risk without active mitigation |

For each rating, include:
- Risk level (L/M/H)
- Brief rationale (1-2 sentences)
- Mitigation strategy (for Medium/High)

## Phase 3: Generate Matrix

Present the analysis as a comparison matrix:

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [name] | Risk: L. [rationale] | Risk: M. [rationale] | Risk: H. [rationale] |

After the matrix, summarize:
- Strongest option per pillar
- Key trade-offs between top options
- Any blocking concerns (High risk on critical criteria)

## Phase 4: Refinement

Ask user to review and refine:
- Adjust any ratings that seem off
- Add missing considerations
- Clarify trade-off priorities

## Phase 5: Save State

After user confirms analysis, update `.claude/adr-session.yaml`:

```yaml
topic: "[decision topic]"
status: "analyzed"
framework: "[framework]"
criteria:
  # ... existing criteria ...
options:
  - name: "[option name]"
    description: "[brief description]"
    ratings:
      "[criterion name]":
        risk: "[Low|Medium|High]"
        rationale: "[explanation]"
        mitigation: "[if Medium/High]"
```

Confirm state saved and instruct user to run `/adr-assistant:generate` when ready to create the ADR document.
