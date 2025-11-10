# Issue #73 - Patch Verification Feedback

## Summary

Thank you for the quick response with PR #77! We've conducted extensive testing and analysis.

### Direct Answer to Your Question

You asked: *"Do you think these indirect changes will resolve the issue?"*

**Short answer: No, but they do help.**

**Evidence from testing:**
- ✅ **Framing improvements work** - Summaries are more honest about incomplete work, less pressure to report false completions
- ❌ **Core bug persists** - Still get false "file does not exist" reports with Haiku and Sonnet
- 🟡 **Opus compensates** - Works correctly, but through superior reasoning, not because the issue is fixed

The indirect changes improved checkpoint **quality** (more accurate about progress) but did not eliminate the false negative **problem** (claiming files don't exist when they do).

**Verdict:** PR #77 improves the user experience but **does not fix the root cause**. The bug persists with Haiku and Sonnet models, though Opus can work around it (at 10-20x cost).

---

### Your Framing Changes DID Help

The progress checkpoint framing reduced some symptoms:
- ✅ Early checkpoints can honestly say "no work yet" vs claiming failure
- ✅ Mid-session summaries accept incomplete work
- ✅ Less pressure to fabricate deliverables

But the spatial confusion remains - SDK agent still searches wrong repositories and can't match paths.

---

## What We Tested

**Environment:**
- Worker v5.3.0 (PR #77 applied)
- Test date: Nov 9, 2025 (19:21 PM EST worker restart)
- Models tested: Haiku 4.5 (default), Sonnet 4.5, Opus 4

**Test case:**
- Prompt: "Review and understand ai_docs/continuous-improvement/rules.md"
- File: EXISTS at `/Users/.../dev/personal/lunar-claude/ai_docs/continuous-improvement/rules.md`
- Expected: File successfully read, summarized as discovery/learning task

---

## Results

### Model Comparison

| Model | Observations | Summaries | Verdict |
|-------|-------------|-----------|---------|
| **Haiku** | ❌ Poor quality, self-contradictory | ❌ "file does not exist" | Complete failure |
| **Sonnet** | ✅ Accurate, correct paths | ❌ "file does not exist" | Observations work, summaries fail |
| **Opus** | ✅ Excellent, detailed | ✅ "Documentation review complete" | **SUCCESS** |

**Key finding:** Opus can compensate for the architectural issue through superior reasoning, but you're paying 10-20x more to work around a data plumbing problem.

---

## Root Causes Identified

We found **three interrelated issues**:

### 1. Original Issue (from #73) - Prompt Instruction Ambiguity
**Location:** `src/sdk/prompts.ts` line 60
```typescript
- If file related research comes back as empty or not found
```

**Problem:** SDK agent interprets "review and understand" tasks as "file related research" and skips them, leading to false "file not found" reports.

**Evidence:** Action-oriented prompts ("Search for, locate, and read") succeed while context-loading prompts ("Review and understand") fail.

### 2. Missing Working Directory Context (NEW - Critical)
**Location:** `src/hooks/save-hook.ts`
```typescript
// Line 14: cwd IS captured
export interface PostToolUseInput {
  cwd: string;  // ← Captured here
  tool_name: string;
  // ...
}

// Line 64-69: cwd DROPPED before sending to worker
body: JSON.stringify({
  tool_name,
  tool_input: ...,
  tool_response: ...,
  // cwd NOT included!
})
```

**Problem:** Working directory information exists at hook level but is deliberately not sent to SDK agent.

**Impact:**
- SDK agent cannot distinguish `/dev/personal/lunar-claude/` from `~/.claude/plugins/marketplaces/thedotmack/`
- Searches wrong repositories
- Cannot match user-requested paths to tool execution paths
- Creates false "file not found" reports even when file exists

**Evidence:** Summary #502 analyzed claude-mem repository instead of lunar-claude, confidently reporting success while looking at wrong codebase.

### 3. Observation Pollution (NEW)
**Problem:** False observations from prior sessions contaminate future processing.

**Evidence:** Observation #1012 created 21 seconds AFTER successfully reading file, claiming file doesn't exist based on "historical context" from prior false observations #999, #997.

---

## What PR #77 Did

**Improvements:**
- ✅ Changed framing from "final report" to "progress checkpoint"
- ✅ Added session lifecycle context
- ✅ Progressive tense allows incomplete work
- ✅ Better UX for ongoing sessions

**What it didn't address:**
- ❌ The "skip file related research" instruction (still present)
- ❌ Missing working directory context (cwd still dropped)
- ❌ No explicit guidance for context-loading tasks
- ❌ No path matching capabilities

---

## Recommendations

### Priority 1: Fix Data Plumbing (Missing CWD)
**Impact:** Enables spatial awareness for all models

```typescript
// src/hooks/save-hook.ts
body: JSON.stringify({
  tool_name,
  tool_input,
  tool_response,
  prompt_number,
  cwd: input.cwd  // ← ADD THIS
})
```

Then update worker API to accept and pass cwd to SDK agent in init prompt.

### Priority 2: Clarify Prompt Guidance
**Impact:** Reduces false categorization of context-loading tasks

Update `src/sdk/prompts.ts` to:
1. Clarify when to use `discovery` type (learning about existing systems)
2. Distinguish "routine file listings" from "user-requested file review"
3. Remove ambiguity in "skip file related research"

### Short-term Workaround
Set `CLAUDE_MEM_MODEL=claude-opus-4` to fix symptoms immediately, but note 10-20x cost increase.

---

## Detailed Documentation

Full analysis with evidence, code traces, and timeline reconstruction available:
- `docs/notes/issue-73-patch-verification.md`
- `docs/notes/issue-73-test-plan.md`

Key evidence includes:
- Code trace showing cwd dropped in save-hook.ts
- Session #713 self-contradictory observations
- Wrong repository analysis (claude-mem vs lunar-claude)
- Model comparison with same test prompt
- Timeline showing progressive SDK agent confusion

---

## Questions for Maintainer

1. Is there a reason `cwd` was deliberately excluded from worker API?
2. Would you prefer separate issues for "missing cwd" vs "prompt ambiguity"?
3. Any concerns with passing working directory to SDK agent?

Thank you for your work on this tool - these findings came from extensive debugging and we're happy to help test any fixes!
