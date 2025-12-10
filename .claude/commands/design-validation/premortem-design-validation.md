---
description: Pre-Mortem Design Validation (Failure Scenario Analysis)
argument-hint: [design-document-path]
---

# Purpose

Conduct a pre-mortem analysis by imagining the design has failed catastrophically,
then working backward to identify what went wrong. This technique surfaces risks
and blind spots that optimistic forward-thinking often misses.

Use this command to stress-test a design BEFORE committing to implementation.

## Variables

DESIGN_DOCUMENT: $1
OUTPUT_DIR: `docs/reviews/design-validation/premortem/`
FILE_NAME: `<two-to-three-words-from-DESIGN_DOCUMENT-filename>.md`

## Instructions

- IMPORTANT: If no `DESIGN_DOCUMENT` is provided, stop and ask the user to provide it.
- Read and understand the design document thoroughly before starting.
- Verify `OUTPUT_DIR` exists, create it if it doesn't.
- Save output from analysis to `OUTPUT_DIR/FILE_NAME`.
- Adopt a pessimistic mindset - assume failure happened and work backward.

## Workflow

### Step 1: Extract Design Context

From the design document, identify and summarize:

- **Design Summary**: What is being proposed (1-2 sentences)
- **Problem Statement**: What problem this solves
- **Key Components**: Main technical pieces

### Step 2: Pre-Mortem Exercise

Imagine this design has been implemented and **failed catastrophically**.

Working backward from this imagined failure, identify **exactly 3 critical failure scenarios**.

For each scenario, document:

1. **Failure Point**: The specific technical limitation, wrong assumption, or missing requirement
2. **Root Cause**: What we missed during design that led to this failure
3. **Warning Signs**: Early indicators we should have noticed
4. **Precedent**: Similar projects/tools that failed this way (cite specific examples)

### Step 3: Research Gaps Analysis

Identify what should have been researched first:

- Existing solutions, tools, or patterns not investigated
- Technical constraints or limitations not validated
- Stakeholder needs or edge cases not explored
- Industry standards or best practices overlooked

### Step 4: Build vs. Integrate Reality Check

Answer explicitly:

| Question | Answer |
|----------|--------|
| What existing solutions address parts of this problem? | [list] |
| Why build instead of integrate/extend? | [justification] |
| What gaps justify custom development? | [specifics] |
| What components could we leverage? | [list] |

### Step 5: Validation Actions

For EACH failure scenario from Step 2, define:

- **Research Needed**: Technologies, tools, approaches to investigate
- **Proof-of-Concept**: Validation experiments to run
- **Questions to Answer**: Before committing to implementation
- **Success Criteria**: Must be met to proceed

## Output Format

Save the analysis to `OUTPUT_DIR/FILE_NAME` using this structure:

```markdown
# Pre-Mortem Analysis: [Design Document Name]

**Analyzed**: [date]
**Document**: [path to design document]
**Method**: Pre-mortem failure scenario analysis

---

## Design Context

**Summary**: [1-2 sentence description]

**Problem Statement**: [what problem this solves]

**Key Components**:

- [component 1]
- [component 2]
- [component 3]

---

## Failure Scenarios

### Scenario 1: [Failure Title]

| Aspect | Details |
|--------|---------|
| **Failure Point** | [specific technical limitation/wrong assumption/missing requirement] |
| **Root Cause** | [what we missed during design] |
| **Warning Signs** | [early indicators we should have noticed] |
| **Precedent** | [similar project that failed this way + citation] |

### Scenario 2: [Failure Title]

| Aspect | Details |
|--------|---------|
| **Failure Point** | [specific technical limitation/wrong assumption/missing requirement] |
| **Root Cause** | [what we missed during design] |
| **Warning Signs** | [early indicators we should have noticed] |
| **Precedent** | [similar project that failed this way + citation] |

### Scenario 3: [Failure Title]

| Aspect | Details |
|--------|---------|
| **Failure Point** | [specific technical limitation/wrong assumption/missing requirement] |
| **Root Cause** | [what we missed during design] |
| **Warning Signs** | [early indicators we should have noticed] |
| **Precedent** | [similar project that failed this way + citation] |

---

## Research Gaps

### Not Investigated

- [gap 1]
- [gap 2]

### Not Validated

- [constraint 1]
- [constraint 2]

### Not Explored

- [edge case 1]
- [edge case 2]

### Overlooked Standards

- [standard 1]
- [standard 2]

---

## Build vs. Integrate Analysis

| Question | Answer |
|----------|--------|
| Existing solutions? | [list with links] |
| Why build? | [justification with evidence] |
| Gaps justifying custom dev? | [specifics] |
| Components to leverage? | [list] |

---

## Validation Plan

### For Scenario 1: [Title]

- **Research**: [what to investigate]
- **PoC**: [experiment to run]
- **Questions**: [must answer before proceeding]
- **Success Criteria**: [measurable conditions]

### For Scenario 2: [Title]

- **Research**: [what to investigate]
- **PoC**: [experiment to run]
- **Questions**: [must answer before proceeding]
- **Success Criteria**: [measurable conditions]

### For Scenario 3: [Title]

- **Research**: [what to investigate]
- **PoC**: [experiment to run]
- **Questions**: [must answer before proceeding]
- **Success Criteria**: [measurable conditions]

---

## Recommendation

**Proceed**: YES / NO / CONDITIONAL

**If Conditional, requires**:

- [ ] [validation item 1]
- [ ] [validation item 2]
- [ ] [validation item 3]

**Confidence Level**: High / Medium / Low
```
