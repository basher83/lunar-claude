---
description: Generate final ADR document from analysis
argument-hint: [output-path]
---

Generate the final Architecture Decision Record document.

Use the adr-methodology skill for ADR templates.

## Prerequisites Check

Read `.claude/adr-session.yaml` to retrieve session state.

If file doesn't exist or status is not `analyzed`:
- Inform user that options analysis must be completed first
- Instruct them to run `/adr-assistant:analyze` to complete the analysis
- Stop processing

## Phase 1: Decision Capture

Display the options matrix summary from state.

Ask user:
1. **Which option are you choosing?**
2. **Why?** (Reference specific criteria and trade-offs)
3. **Who are the decision-makers?** (Names for the ADR header)

## Phase 2: Consequences Analysis

Based on the chosen option and its ratings, generate:

**What becomes easier:**
- Benefits from Low-risk ratings
- Advantages over rejected options

**What becomes harder:**
- Trade-offs from Medium/High ratings
- Capabilities lost by rejecting alternatives

Present for user review and refinement.

## Phase 3: ADR Number Detection

Scan `docs/adr/` directory for existing ADR files.

If directory exists:
- Find highest numbered ADR (pattern: `NNNN-*.md`)
- Next number = highest + 1

If directory doesn't exist:
- Create `docs/adr/` directory
- Start at 0001

## Phase 4: Generate ADR

Use MADR template format. Generate complete ADR including:

1. **Header**: Number, title, status (Accepted), date, decision-makers
2. **AI Disclosure**: Note that Claude assisted; humans reviewed and decided
3. **Context**: Summarize problem and constraints from session
4. **Decision Drivers**: Key criteria that influenced the decision
5. **Considered Options**: Each option with pros/cons from analysis
6. **Decision**: Chosen option with rationale
7. **Consequences**: What becomes easier/harder
8. **Appendix**: Full assessment matrix from analysis

## Phase 5: Output Path

Determine output path:

If `$1` provided:
- Use `$1` as the output path

If no argument:
- Generate path: `docs/adr/NNNN-[slugified-title].md`
- Slugify: lowercase, hyphens for spaces, remove special characters

## Phase 6: Write and Cleanup

1. Write the ADR file to the determined path
2. Delete `.claude/adr-session.yaml` to clear session state
3. Confirm:
   - ADR file location
   - Suggest next steps (commit, share with stakeholders, update ADR index)

## Output Format Reference

```markdown
# [ADR-NNNN] [Title]

**Status:** Accepted
**Date:** [YYYY-MM-DD]
**Decision-makers:** [names]

## AI Disclosure

This ADR was drafted with AI assistance (Claude). Assessment criteria and
rationale were reviewed by decision-makers listed above. Final decision
made by humans.

## Context and Problem Statement

[From session context]

## Decision Drivers

- [Key criteria that influenced decision]

## Considered Options

### Option 1: [Name]

[Description]

**Pros:**
- [From Low ratings]

**Cons:**
- [From Medium/High ratings]

### Option 2: [Name]

...

## Decision

Chosen option: **[Name]**

[Rationale referencing criteria and trade-offs]

## Consequences

### What becomes easier
- [Benefits]

### What becomes harder
- [Trade-offs]

## Appendix: Assessment Matrix

[Full matrix from analysis]
```
