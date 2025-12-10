---
description: Build vs. Integrate SWOT Analysis
argument-hint: [capability-description] [business-context-or-doc]
---

# Purpose

Conduct a structured SWOT analysis comparing **Build Custom** vs. **Integrate/Extend Existing**
approaches for a specific capability. This framework surfaces trade-offs systematically
to support an evidence-based build-vs-buy decision.

Use this command when you have a specific capability to implement and need to decide
whether to build it yourself or use existing solutions.

## Variables

CAPABILITY: $1 (e.g., "authentication system", "data pipeline", "notification service")
BUSINESS_CONTEXT: $2 (file path to context doc OR brief description)
OUTPUT_DIR: `docs/reviews/design-validation/build-vs-integrate/`
FILE_NAME: `<capability-slug>-swot.md`

## Instructions

- IMPORTANT: If no `CAPABILITY` is provided, stop and ask the user to provide it.
- If `BUSINESS_CONTEXT` is a file path, read it first.
- Verify `OUTPUT_DIR` exists, create it if it doesn't.
- Save analysis to `OUTPUT_DIR/FILE_NAME`.
- Be specific - generic SWOT is useless. Cite real solutions, real costs, real timelines.
- Challenge the assumption that building is better - most teams overestimate their ability to build.

## Workflow

### Step 1: Define the Capability

Clearly articulate:

- What capability is being evaluated
- Business context and constraints
- Key requirements it must satisfy

### Step 2: Build Custom SWOT

Analyze the **Build Custom** approach:

**Strengths** (3 minimum) - Internal advantages:

- What you gain by building (control, customization, IP)
- Specific capabilities enabled
- Long-term strategic benefits

**Weaknesses** (3 minimum) - Internal disadvantages:

- Development time and cost
- Maintenance burden
- Missing features vs. mature solutions

**Opportunities** - External factors favoring build:

- Market gaps existing solutions don't address
- Competitive advantage from unique implementation
- Emerging technologies enabling novel approaches

**Threats** - External factors against build:

- Existing solutions improving/adding features
- Industry standards you'd have to conform to
- Opportunity cost of not focusing on core business

### Step 3: Integrate/Extend SWOT

Analyze the **Integrate/Extend Existing** approach:

**Strengths** (3 minimum) - Advantages of integration:

- Time to production
- Proven reliability/security
- Features included out-of-box

**Weaknesses** (3 minimum) - Limitations:

- Gaps vs. requirements
- Integration complexity
- Cost/vendor dependency

**Opportunities** - Benefits from ecosystem:

- Community plugins/extensions
- Vendor roadmap alignment
- Established patterns to follow

**Threats** - Risks from dependencies:

- Vendor viability/pricing changes
- Lock-in concerns
- Limited control over critical aspects

### Step 4: Recommendation

Based on analysis, recommend: **Build | Integrate | Hybrid**

Include:

- Justification with specific trade-offs
- Hybrid breakdown if applicable
- Validation checklist

## Output Format

Save the analysis to `OUTPUT_DIR/FILE_NAME` using this structure:

```markdown
# Build vs. Integrate SWOT: [Capability]

**Analyzed**: [date]
**Capability**: [what's being evaluated]
**Context**: [business context summary]

---

## Capability Definition

**What**: [capability description]

**Requirements**:

- [requirement 1]
- [requirement 2]
- [requirement 3]

**Constraints**:

- [constraint 1]
- [constraint 2]

---

## Build Custom Approach

### Strengths (Internal Advantages)

1. **[Strength]**
   - Why it matters: [explanation]
   - Example: [concrete benefit]

2. **[Strength]**
   - Why it matters: [explanation]
   - Example: [concrete benefit]

3. **[Strength]**
   - Why it matters: [explanation]
   - Example: [concrete benefit]

### Weaknesses (Internal Disadvantages)

1. **[Weakness]**
   - Impact: [real-world effect]
   - Example: [specific cost/timeline]

2. **[Weakness]**
   - Impact: [real-world effect]
   - Example: [specific cost/timeline]

3. **[Weakness]**
   - Impact: [real-world effect]
   - Example: [specific cost/timeline]

### Opportunities (External Factors Favoring Build)

- [opportunity 1]
- [opportunity 2]

### Threats (External Factors Against Build)

- [threat 1]
- [threat 2]

---

## Integrate/Extend Approach

### Existing Solutions Evaluated

| Solution | Type | Feature Match | Cost | Maturity |
|----------|------|---------------|------|----------|
| [solution 1] | [OSS/SaaS] | [%] | [cost] | [status] |
| [solution 2] | [OSS/SaaS] | [%] | [cost] | [status] |
| [solution 3] | [OSS/SaaS] | [%] | [cost] | [status] |

### Strengths (Advantages of Integration)

1. **[Strength]**
   - Evidence: [track record/data]
   - Example: [specific solution capability]

2. **[Strength]**
   - Evidence: [track record/data]
   - Example: [specific solution capability]

3. **[Strength]**
   - Evidence: [track record/data]
   - Example: [specific solution capability]

### Weaknesses (Limitations)

1. **[Weakness]**
   - Workaround: [if any]
   - Example: [specific gap]

2. **[Weakness]**
   - Workaround: [if any]
   - Example: [specific gap]

3. **[Weakness]**
   - Workaround: [if any]
   - Example: [specific gap]

### Opportunities (Ecosystem Benefits)

- [opportunity 1]
- [opportunity 2]

### Threats (Dependency Risks)

- [threat 1]
- [threat 2]

---

## Cost Comparison

| Factor | Build | Integrate |
|--------|-------|-----------|
| Initial Development | [estimate] | [cost] |
| Time to Production | [estimate] | [estimate] |
| Annual Maintenance | [estimate] | [cost] |
| 3-Year TCO | [total] | [total] |

---

## Recommendation

**Approach**: BUILD / INTEGRATE / HYBRID

### Justification

[Why this approach given the SWOT analysis]

### Trade-offs Accepted

- Prioritizing [X] over [Y]
- Accepting [limitation] in exchange for [benefit]

### Hybrid Breakdown (if applicable)

| Component | Decision | Rationale |
|-----------|----------|-----------|
| [component 1] | Build | [why] |
| [component 2] | Integrate | [why + which solution] |
| [component 3] | Extend | [base + modifications] |

---

## Validation Checklist

- [ ] Evaluated 3+ existing solutions with evidence
- [ ] Calculated total cost of ownership (build vs. integrate)
- [ ] Validated existing solutions can't meet needs with config/extension
- [ ] Confirmed team has capacity and expertise for chosen approach
- [ ] Identified reusable components regardless of approach

---

## Decision Confidence

**Confidence Level**: High / Medium / Low

**What would change this decision**:

- [condition 1]
- [condition 2]
```
