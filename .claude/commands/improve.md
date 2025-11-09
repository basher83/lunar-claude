---
description: Analyze recent sessions for failures and generate improvement report
argument-hint: [days]
allowed-tools: mcp__plugin_claude-mem_claude-mem-search__search_user_prompts, mcp__plugin_claude-mem_claude-mem-search__find_by_concept, mcp__plugin_claude-mem_claude-mem-search__find_by_type, Write
---

# Continuous Improvement Analysis

You are analyzing recent Claude Code sessions to identify failures, corrections, and learning opportunities.

## Configuration

**Search window:** ${1:-7} days back from today
**Output file:** `ai_docs/continuous-improvement/lessons-learned-<TODAY>.md` (use ISO date format)

## Task Instructions

### Step 1: Calculate Date Range

Today's date is available in your `<env>` context. Calculate:
- **End date:** Today
- **Start date:** Today minus ${1:-7} days
- Use ISO format (YYYY-MM-DD) for all date operations

### Step 2: Search for Incidents (Multi-Strategy)

Execute the following searches in parallel for the calculated date range:

**A) User Corrections (search_user_prompts)**
Search for these phrases indicating something went wrong:
- "wrong"
- "stop"
- "why did you"
- "not what I asked"
- "no"
- "what are you"

Use `format: "index"` first, then fetch full details only for relevant matches.

**B) Problem-Solution Patterns (find_by_concept)**
Query for observations tagged with concept: "problem-solution"

**C) Bug Fixes (find_by_type)**
Query for observations of type: "bugfix"

### Step 3: Aggregate and Deduplicate

- Collect all findings from the three search strategies
- Note: This command does NOT deduplicate across previous reports
- Include all incidents found in the time window
- For each incident, capture:
  - Timestamp (ISO format with time if available)
  - Source (claude-mem URI or reference)
  - User correction (exact quote if from prompts)
  - Context (what was happening, what went wrong)

### Step 4: Generate Report

Write the report to `ai_docs/continuous-improvement/lessons-learned-<TODAY>.md`:

**Report structure:**

```markdown
# Lessons Learned - <DATE>

**Search Period:** Last ${1:-7} days (<START-DATE> to <END-DATE>)
**Report Generated:** <TODAY>
**Total Incidents Found:** <COUNT>

---

## Search Strategy

This report combines three search methods:
1. User correction phrases in prompts
2. Problem-solution concept observations
3. Bugfix type observations

---

## Incidents

### Incident 1: <Title/Summary>

**Timestamp:** YYYY-MM-DD HH:MM:SS

**Source:** <claude-mem URI or session reference>

**User Correction:** (if applicable)
> <exact quote>

**Context:**
<What was happening, what went wrong, what was learned>

---

### Incident 2: ...

[Continue for all incidents...]

---

## Search Results Summary

**Total searches performed:** 3 strategies

**Results by strategy:**
- User correction phrases: <COUNT> results
- Problem-solution concepts: <COUNT> results
- Bugfix observations: <COUNT> results

**Note:** This report shows ALL incidents in the time window. Manual reconciliation with existing lessons-learned files is required to identify truly new incidents.
```

### Step 5: Completion

After writing the report, inform the user:
- Number of incidents found
- File location
- Reminder that manual reconciliation is needed
