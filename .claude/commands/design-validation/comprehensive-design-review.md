---
description: Comprehensive Design Review - Parallel Multi-Agent Validation
argument-hint: [design-document-path]
---

# Purpose

Execute comprehensive design validation by launching 5 specialized review agents in parallel.
Each agent follows its respective command definition. The orchestrator combines all findings
into a unified report.

## Variables

DESIGN_DOCUMENT: $1
OUTPUT_DIR: `docs/reviews/design-validation/comprehensive/`
PARTS_DIR: `docs/reviews/design-validation/comprehensive/parts/`
FILE_NAME: `<design-document-slug>-comprehensive-review.md`

## Instructions

- IMPORTANT: If no `DESIGN_DOCUMENT` is provided, stop and ask the user to provide it.
- Verify `DESIGN_DOCUMENT` exists.
- Create `OUTPUT_DIR` and `PARTS_DIR` if they don't exist.
- Launch ALL 5 subagents in PARALLEL (single message, multiple Task tool calls).
- Wait for all to complete.
- Read results from `PARTS_DIR`.
- Synthesize into comprehensive report at `OUTPUT_DIR/FILE_NAME`.

## Workflow

### Step 1: Launch Parallel Validation Agents

Launch ALL 5 agents in a SINGLE message with multiple Task tool calls:

**Agent 1: Self-Critique Review**

```text
subagent_type: general-purpose
description: Self-critique design review

Prompt:
Read and follow the command definition at:
.claude/commands/design-validation/self-critique-design-review.md

DESIGN_DOCUMENT: [path from $1]
OUTPUT_DIR: docs/reviews/design-validation/comprehensive/parts/
FILE_NAME: self-critique.md

Execute the command exactly as defined.
```

**Agent 2: Pre-Mortem Analysis**

```text
subagent_type: general-purpose
description: Pre-mortem failure analysis

Prompt:
Read and follow the command definition at:
.claude/commands/design-validation/premortem-design-validation.md

DESIGN_DOCUMENT: [path from $1]
OUTPUT_DIR: docs/reviews/design-validation/comprehensive/parts/
FILE_NAME: premortem.md

Execute the command exactly as defined.
```

**Agent 3: Landscape Research**

```text
subagent_type: general-purpose
description: Landscape research

Prompt:
Read and follow the command definition at:
.claude/commands/design-validation/landscape-research-protocol.md

DESIGN_DOCUMENT: [path from $1]
OUTPUT_DIR: docs/reviews/design-validation/comprehensive/parts/
FILE_NAME: landscape.md

Extract the problem domain from the design document.
Execute the command exactly as defined.
```

**Agent 4: Build vs Integrate SWOT**

```text
subagent_type: general-purpose
description: Build vs integrate SWOT analysis

Prompt:
Read and follow the command definition at:
.claude/commands/design-validation/build-vs-integrate-swot.md

DESIGN_DOCUMENT: [path from $1]
OUTPUT_DIR: docs/reviews/design-validation/comprehensive/parts/
FILE_NAME: swot.md

Extract the capability being evaluated from the design document.
Execute the command exactly as defined.
```

**Agent 5: ADR Alternatives Analysis**

```text
subagent_type: general-purpose
description: ADR alternatives analysis

Prompt:
Read and follow the command definition at:
.claude/commands/design-validation/adr-alternatives-analysis.md

DESIGN_DOCUMENT: [path from $1]
OUTPUT_DIR: docs/reviews/design-validation/comprehensive/parts/
FILE_NAME: adr.md

Extract the decision title from the design document.
Execute the command exactly as defined.
```

### Step 2: Synthesize Results

After all 5 agents complete:

1. Read each report from `PARTS_DIR`
2. Identify common themes across reviews
3. Note contradictions or tensions
4. Determine overall recommendation
5. Compile unified validation plan

### Step 3: Generate Comprehensive Report

Create the final report at `OUTPUT_DIR/FILE_NAME`.

## Output Format

```markdown
# Comprehensive Design Review: [Design Title]

**Reviewed**: [date]
**Document**: [path]
**Method**: 5-agent parallel validation

---

## Executive Summary

**Overall Recommendation**: PROCEED / PROCEED WITH CAUTION / DO NOT PROCEED / NEED MORE RESEARCH

**Confidence Level**: High / Medium / Low

**Key Findings**:

1. [Finding from cross-review analysis]
2. [Finding from cross-review analysis]
3. [Finding from cross-review analysis]

**Critical Risks**:

- [Risk identified by multiple reviews]
- [Risk identified by multiple reviews]

**Required Actions**:

- [ ] [Action from validation plans]
- [ ] [Action from validation plans]

---

## Cross-Review Synthesis

### Common Themes

| Theme | Self-Critique | Pre-Mortem | Landscape | SWOT | ADR |
|-------|---------------|------------|-----------|------|-----|
| [theme] | [finding] | [finding] | [finding] | [finding] | [finding] |

### Contradictions

- [Where reviews disagree]

### Strongest Validations

- [What multiple reviews confirm]

---

## Build vs Integrate Decision

**Recommendation**: BUILD / INTEGRATE / HYBRID

| Factor | Build | Integrate | Winner |
|--------|-------|-----------|--------|
| Time | [est] | [est] | [choice] |
| Cost | [est] | [est] | [choice] |
| Fit | [%] | [%] | [choice] |

**Solutions to Leverage**:

- [solution]: [use for]

---

## Unified Validation Plan

| Validation | Source | Priority |
|------------|--------|----------|
| [item] | [review] | HIGH |
| [item] | [review] | MEDIUM |

---

## Individual Reviews

### Self-Critique
[Summary + link to parts/self-critique.md]

### Pre-Mortem
[Summary + link to parts/premortem.md]

### Landscape Research
[Summary + link to parts/landscape.md]

### SWOT Analysis
[Summary + link to parts/swot.md]

### ADR
[Summary + link to parts/adr.md]

---

## Decision

**Proceed**: YES / NO / CONDITIONAL

**If Conditional**:
- [ ] [validation required]

**Re-evaluate if**:
- [trigger]
```
