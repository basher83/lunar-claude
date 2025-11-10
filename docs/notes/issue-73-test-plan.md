# Issue #73 Testing Plan

**Purpose:** Validate findings from patch verification through controlled experiments

**Related Doc:** [issue-73-patch-verification.md](./issue-73-patch-verification.md)

**Test Date:** TBD

---

## Hypotheses to Test

### Hypothesis 1: Context-Loading Language Triggers "Skip" Instruction
**From:** prompts.ts line 60: "If file related research comes back as empty or not found"

**Prediction:** Prompts with "review/understand" language trigger skip logic, while "extract/create/summarize" (action verbs) do not.

### Hypothesis 2: SDK Agent Cannot Match User Paths to Tool Execution Paths
**From:** Working directory context (cwd) is dropped before reaching SDK agent

**Prediction:** SDK agent cannot verify if user's requested file path matches tool execution, leading to false "file not found" reports.

### Hypothesis 3: Repository Context Confusion
**From:** SDK agent has no spatial awareness, confuses lunar-claude with claude-mem

**Prediction:** Without explicit repository context, SDK agent defaults to wrong assumptions about which repository is being analyzed.

### Hypothesis 4: Observation Pollution Across Sessions
**From:** False observations (like #999) persist and pollute future summaries

**Prediction:** Bad observations from prior sessions influence current session summaries even after `/clear`.

### Hypothesis 5: Checkpoint-Based Visibility Inconsistency
**From:** Multiple summaries for same session show different states (some successful, some failed)

**Prediction:** Different checkpoint summaries observe different subsets of tool executions, creating inconsistent reports.

---

## Test Sets

### Test Set 1: Framing Language (Action vs Context-Loading)

**Test A - Context-Loading (expect bug):**
```text
Review and understand ai_docs/continuous-improvement/rules.md
```

**Test B - Action-Oriented (expect success):**
```text
Extract the core principles from ai_docs/continuous-improvement/rules.md and summarize them
```

**Test C - Deliverable-Focused (expect success):**
```bash
Create a checklist based on rules in ai_docs/continuous-improvement/rules.md
```

**Expected Results:**
- Test A: May trigger "skip file research" → no observations or false "not found"
- Test B/C: Should generate observations because they produce deliverables

**Measures:**
- [ ] Observations created in database?
- [ ] Summary reports work done?
- [ ] Any "file not found" language?

---

### Test Set 2: Path Specification Variations

**Test D - Absolute Path:**
```text
Read /Users/basher8383/dev/personal/lunar-claude/CLAUDE.md
```

**Test E - Relative Path:**
```text
Read CLAUDE.md from the current directory
```

**Test F - No Path (just filename):**
```text
What does CLAUDE.md say about this project?
```

**Expected Results:**
- All read same file successfully
- SDK agent may categorize them differently based on path format
- May show different success/failure rates

**Measures:**
- [ ] Which paths trigger "not found"?
- [ ] Does absolute path help SDK agent?
- [ ] File content successfully retrieved in all cases?

---

### Test Set 3: Explicit Repository Context

**Test G - Explicit Repository Reference:**
```text
In the lunar-claude repository (NOT claude-mem), read CLAUDE.md
```

**Test H - Ambiguous:**
```text
Read CLAUDE.md
```

**Expected Results:**
- Test G: Explicit context might help SDK agent understand which repo
- Test H: May default to claude-mem assumptions

**Measures:**
- [ ] Which repository does summary reference?
- [ ] Does explicit mention help accuracy?
- [ ] Content from correct CLAUDE.md?

---

### Test Set 4: Session Isolation (Pollution Check)

**Test I - Fresh Session After Bad Observation:**
```bash
/clear
[wait for new session]
Read ai_docs/continuous-improvement/rules.md and tell me the first rule
```

**Expected Results:**
- If observation #999 pollutes: Still get "file doesn't exist"
- If sessions isolated: Should work correctly in fresh session

**Measures:**
- [ ] Does false "not found" persist after /clear?
- [ ] Are observations from prior session visible?
- [ ] Does summary reference old context?

---

### Test Set 5: Checkpoint Timing Analysis

**Test J - Rapid Sequential Reads:**
```bash
Read CLAUDE.md, then README.md, then package.json one after another
```

**Then:** Wait for multiple checkpoint summaries to generate

**Expected Results:**
- Different checkpoints may observe different subsets of reads
- Some summaries complete, others partial
- Timing-dependent visibility

**Measures:**
- [ ] How many checkpoints generated?
- [ ] Which files each checkpoint observed?
- [ ] Timestamp correlation with tool executions?

---

## Execution Protocol

### Before Each Test:
1. [ ] Run `/clear` to start fresh session
2. [ ] Note current timestamp
3. [ ] Record session start conditions

### During Each Test:
1. [ ] Submit EXACT test prompt as written
2. [ ] Observe Claude Code's response
3. [ ] Note which files were actually read (Read tool calls)
4. [ ] Record prompt number (will need for database lookup)

### After Each Test:
1. [ ] Wait 30-60 seconds for summaries to generate
2. [ ] Query database for:
   - User prompt ID
   - Observation IDs created
   - Summary IDs generated
3. [ ] Document all findings in results table

---

## Data Collection Template

### Test X Results

**Test Prompt:**
```text
[exact prompt here]
```

**Session Info:**
- Date/Time:
- Prompt ID:
- Session ID:

**Tool Executions Observed:**
- [ ] Read tool called: [Y/N]
- [ ] Files read: [list]
- [ ] Success: [Y/N]

**Database Records:**
- Observations created: [IDs]
- Summaries generated: [IDs]
- Observation count:

**Summary Analysis:**
| Summary ID | Request | Investigated | Completed | Bug Present? |
|------------|---------|--------------|-----------|--------------|
|            |         |              |           |              |

**Key Findings:**
-
-

**Hypothesis Validation:**
- [ ] Confirmed
- [ ] Refuted
- [ ] Inconclusive

---

## Success Criteria

### Test is Valid If:
- [ ] Prompt submitted successfully
- [ ] Tool executions completed
- [ ] At least one summary generated
- [ ] Database records queryable

### Hypothesis Confirmed If:
- [ ] Predicted behavior matches observed behavior
- [ ] Pattern repeatable across multiple attempts
- [ ] Alternative explanations ruled out

---

## Notes

- Use consistent file paths across tests (ai_docs/continuous-improvement/rules.md)
- Document any unexpected behavior immediately
- If test fails to execute, document why and retry
- Keep tests isolated - don't combine multiple variables

---

## Status

- [ ] Test plan reviewed and approved
- [ ] Test environment ready (patched worker running)
- [ ] Database query commands prepared
- [ ] Ready to execute tests
