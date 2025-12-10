---
description: Self-Critique Enhanced Design Review
argument-hint: [design-document-path]
---

# Purpose

Conduct a rigorous two-phase design review with explicit self-critique to reduce
confirmation bias. This process forces you to challenge your own assessment,
identify blind spots, and produce a validated recommendation with clear confidence levels.

Use this command BEFORE committing to implementation to catch design flaws early.

## Variables

DESIGN_DOCUMENT: $1
OUTPUT_DIR: `docs/reviews/design-validation/self-critique-design-review/`
FILE_NAME: `<two-to-three-words-from-DESIGN_DOCUMENT-filename>.md`

## Instructions

- IMPORTANT: If no `DESIGN_DOCUMENT` is provided, stop and ask the user to provide it.
- Verify `OUTPUT_DIR` exists, create it if it doesn't.
- Save output from review to `OUTPUT_DIR/FILE_NAME`.
- Conduct a two-phase review with explicit self-critique to reduce confirmation bias.

## Workflow

### Phase 1: Initial Assessment

Analyze the design document and produce:

**1.1 Design Strengths** (identify exactly 3)

For each strength, document:

- What aspect of the design is strong
- Why it effectively addresses requirements
- Specific evidence or examples supporting this

**1.2 Design Concerns** (identify exactly 3)

For each concern, document:

- What assumption or decision needs scrutiny
- Why this could be a risk or limitation
- What research or validation would address it

**1.3 Integration vs. Build Analysis**

Answer these questions explicitly:

- Have we identified existing solutions that solve this or parts of it?
- What specific evidence shows existing solutions won't work?
- What are we planning to build that might already exist?

### Phase 2: Self-Critique

Challenge your Phase 1 assessment by working through each category:

**2.1 Bias Check**

- Am I defending this design because I created it vs. objectively evaluating it?
- What assumptions am I making without evidence?
- Have I researched alternatives thoroughly enough?
- Am I overestimating our ability to build vs. integrate?

**2.2 Blind Spots**

- What did I miss in the landscape research?
- What edge cases or failure scenarios haven't been considered?
- What stakeholder perspectives aren't represented?
- What technical constraints haven't been validated?

**2.3 Reality Check**

- Is this the best use of engineering time vs. other priorities?
- Have I justified "build" vs. "integrate" with real evidence?
- What would a senior engineer from outside our team challenge?
- If we had to ship in half the time, what would we cut?

**2.4 Validation Gaps**

- What research still needs to be done?
- What proof-of-concept work would validate core assumptions?
- What experts or stakeholders should review this?
- What would make me confident proceeding vs. hesitant?

### Phase 3: Revised Assessment

Based on self-critique, produce final recommendations.

## Output Format

Save the review to `OUTPUT_DIR/FILE_NAME` using this structure:

```markdown
# Design Review: [Design Document Name]

**Reviewed**: [date]
**Document**: [path to design document]
**Reviewer**: Claude (self-critique method)

---

## Phase 1: Initial Assessment

### Strengths

1. **[Strength Title]**
   - Aspect: [what]
   - Why effective: [reasoning]
   - Evidence: [specific examples]

2. **[Strength Title]**
   - Aspect: [what]
   - Why effective: [reasoning]
   - Evidence: [specific examples]

3. **[Strength Title]**
   - Aspect: [what]
   - Why effective: [reasoning]
   - Evidence: [specific examples]

### Concerns

1. **[Concern Title]**
   - Assumption/Decision: [what needs scrutiny]
   - Risk: [why this could be a problem]
   - Validation needed: [how to address]

2. **[Concern Title]**
   - Assumption/Decision: [what needs scrutiny]
   - Risk: [why this could be a problem]
   - Validation needed: [how to address]

3. **[Concern Title]**
   - Assumption/Decision: [what needs scrutiny]
   - Risk: [why this could be a problem]
   - Validation needed: [how to address]

### Integration vs. Build

| Question | Answer |
|----------|--------|
| Existing solutions identified? | [yes/no + details] |
| Evidence against existing solutions | [specifics] |
| Custom build justified? | [yes/no + reasoning] |

---

## Phase 2: Self-Critique Findings

### Biases Identified

- [bias 1]
- [bias 2]

### Blind Spots Discovered

- [blind spot 1]
- [blind spot 2]

### Reality Check Results

- [finding 1]
- [finding 2]

### Validation Gaps

- [gap 1]
- [gap 2]

---

## Phase 3: Revised Assessment

### Strengthened Justification

[Decisions that survived critique with evidence]

### Required Mitigations

| Risk | Mitigation | Owner |
|------|------------|-------|
| [risk] | [action] | [who] |

### Integration Strategy (Refined)

| Component | Decision | Evidence |
|-----------|----------|----------|
| [component] | Build / Integrate / Configure | [why] |

### Decision Confidence

**Confidence Level**: High / Medium / Low

**What would increase confidence**:

- [item 1]
- [item 2]

**Re-evaluation triggers**:

- [condition 1]
- [condition 2]

---

## Final Checklist

- [ ] Challenged my own assumptions explicitly
- [ ] Identified and addressed potential biases
- [ ] Validated that existing solutions truly don't meet needs
- [ ] Confirmed justification for custom development vs. integration
- [ ] Surfaced blind spots and created mitigation plan
- [ ] Obtained external perspective or review
- [ ] Ready to proceed OR identified what research is still needed
```
