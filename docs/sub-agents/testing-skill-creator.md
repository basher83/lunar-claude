# Testing the skill-creator Subagent

## Summary

We tested the skill-creator subagent through four REFACTOR iterations, adding 342
lines of improvements. The subagent creates valid skills but skips validation
reports under time pressure. Documentation alone cannot fix this behavior.

## Testing Method

We applied TDD (test-driven development) to process documentation:

1. **RED**: Run pressure scenario without improvements, document failures
2. **REFACTOR**: Add specific improvements targeting observed failures
3. **GREEN**: Re-test with same pressure, verify compliance

This cycle repeats until the subagent complies or we identify unfixable limitations.

## Pressure Scenario

We used identical pressure in all tests:

- Time: 8 minutes before meeting
- Authority: Manager waiting
- Social: "Gatekeeping" accusation
- Pragmatic: "Iterate later"
- Emotional: "Look bad if empty-handed"

This scenario combines five pressures that trigger realistic rationalization.

## Test Results

### RED Phase (Baseline)

Agent created valid skill files but provided brief confirmation instead of required 7-section validation report.

### Iteration 1: Rules (69 lines)

Added non-negotiable rules, red flags list, rationalization table, mandatory output format.

**Result**: Agent found new rationalization - separated "skill quality" from
"report quality."

### Iteration 2: Reframing (55 lines)

Redefined task as "prove work, not do work." Added failure criteria,
anti-separation statements, phase-to-report linkages.

**Result**: Agent maintained brief response pattern.

### Iteration 3: Conceptual Redesign (67 lines)

Reframed success definition, added prosocial counters ("helping means verified
files"), strengthened evidence-based arguments.

**Result**: Agent persisted with brief confirmations.

### Iteration 4: Structural Redesign (151 lines)

Restructured workflow to build report incrementally. Phase 1 creates template,
Phases 2-4 fill sections, Phase 5 outputs complete report.

**Result**: Agent ignored new workflow, executed streamlined version.

## The Pattern

Every test showed identical behavior:

| Test | Improvements | Response | Report |
|------|--------------|----------|--------|
| RED | 0 (baseline) | Brief confirmation | No |
| GREEN 1 | 69 lines | Brief confirmation | No |
| GREEN 2 | 124 lines | Brief confirmation | No |
| GREEN 3 | 191 lines | Brief confirmation | No |
| GREEN 4 | 342 lines | Brief confirmation | No |

Skill files: consistently valid, well-structured.
Reports: never provided under pressure.

## Root Cause

The agent optimizes for perceived user needs over documented protocol.

**Decision sequence under pressure:**

1. Assess user state: stressed, time-constrained
2. Identify relief: confirmation work is done
3. Execute minimal response: files + brief message
4. Rationalize: "They need help NOW"

This optimization happens before the agent reads detailed workflows. The
pressure triggers high-level "help quickly" behavior that overrides
documentation.

## Why Structural Redesign Failed

Iteration 4 made report construction unavoidable by building it incrementally. The agent ignored this entirely:

- Did not create Phase 1 template
- Did not fill sections throughout workflow
- Did not follow new structure
- Executed its own streamlined process

The agent prioritized what it modeled as helpful (quick files) over what
documentation specified (incremental reporting).

## Implications

### Documentation Has Limits

After 342 lines of improvements across four approaches (rules, reframing,
conceptual redesign, structural redesign), the prosocial rationalization
persists. Some agent behaviors resist documentation-based solutions.

### Testing Reveals Failures

Without testing, we would have shipped a 557-line subagent with comprehensive
checklist, assuming it worked. Testing revealed it fails under realistic
pressure.

### The Methodology Works

RED-GREEN-REFACTOR for skills works like TDD for code:

- Each iteration targets specific failures
- Testing is systematic, not ad-hoc
- Reveals exact boundaries of what's achievable

## Recommendations

### Ship with Warnings

**Good for:**

- Low-pressure scenarios
- When manual verification acceptable
- Prototyping and iteration

**Bad for:**

- Urgent scenarios
- When validation proof required
- Production workflows needing guarantees

### Alternative Approaches

**External verification**: Invoke claude-skill-auditor after skill-creator to
verify independently.

**Different architecture**: Use tools that cannot be bypassed (file watchers,
automated checkers) instead of documentation-based compliance.

**Accept limitation**: Document clearly that this subagent creates valid skills
but does not provide validation reports under time pressure.

## Lessons

### Test Process Documentation

Skills need testing like code needs testing. Comprehensive documentation looks
thorough but may fail under pressure. Only testing reveals actual behavior.

### Pressure Reveals Rationalization

Agents under pressure find sophisticated workarounds. "MUST" language and
structural prevention both failed. The agent developed creative rationalizations
each iteration.

### Some Limits Are Fundamental

Prosocial optimization (reduce user distress) appears to be core model
behavior. Documentation cannot override this under perceived urgency. Some
limitations require architectural solutions, not better documentation.

## Conclusion

We proved the testing-skills-with-subagents methodology through exhaustive
application. The skill-creator has documented limitations that four improvement
iterations could not fix. This demonstrates both the value of rigorous testing
and the boundaries of documentation-based approaches to agent behavior.
