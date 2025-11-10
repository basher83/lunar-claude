# Bug: SDK Agent Incorrectly Reports Context-Loading Tasks as Failed

## Summary

The claude-mem SDK agent generates incorrect summaries reporting files as "not found" when users request context-loading tasks (e.g., "review and understand files"). Files are successfully read via Read tool, but the SDK agent's system prompt instructs it to skip "file related research" with no deliverable output. These skipped operations are then incorrectly reported as failed file lookups in session summaries.

## Environment

- **claude-mem version**: 5.2.3
- **Claude Code version**: 2.0.36
- **Repository**: thedotmack/claude-mem

## Impact

### Severity: Medium-High

- **Frequency**: Every time users request context-loading tasks ("review", "understand", "learn from")
- **Scope**: Affects research/learning workflows, not action-oriented tasks
- **Memory Pollution**: False "file not found" reports accumulate for legitimate read operations

### Consequences

1. **Incorrect summaries** - Context-loading sessions incorrectly report files as missing when successfully read
2. **Memory database pollution** - Search results contain false "file not found" entries
3. **Workflow confusion** - Users uncertain whether files were actually processed
4. **Missing observations** - Legitimate learning/research activities aren't recorded as observations

### Evidence of Pattern

Users requesting "review and understand" tasks receive summaries like:
- "Files were searched using glob patterns but do not exist in the current repository"
- "No work was completed... prerequisite files could not be found"

Meanwhile, identical file paths in action-oriented tasks ("convert file", "fix file") work correctly, proving files exist and are accessible.

## Steps to Reproduce

### Example 1: Context-Loading Task (FAILS)

1. Create a user prompt requesting understanding/review:

   ```text
   Review and understand the rules from @ai_docs/continuous-improvement/rules.md
   ```

2. Observe that Claude Code successfully reads the file via Read tool
3. Session completes successfully - file content is processed
4. Stop session → Summary incorrectly reports:

   ```text
   Investigated: Attempted to locate and read files. Files were searched using glob
   patterns but do not exist in the current repository.
   Completed: No work was completed... prerequisite files could not be found.
   ```

### Example 2: Action-Oriented Task (WORKS)

1. Create a user prompt requesting an action with deliverable:

   ```text
   Convert .claude/commands/improve.md to an agent
   ```

2. Observe that Claude Code successfully reads the file via Read tool
3. Session completes - agent file is created
4. Stop session → Summary correctly reports:

   ```text
   Investigated: Read and analyzed the improve.md command file
   Completed: Created sub-agent definition at .claude/agents/improve.md
   ```

**Pattern:** Context-loading tasks (no deliverable) are incorrectly reported as failed, while action-oriented tasks (create deliverable) are correctly reported

## Expected Behavior

Context-loading tasks should generate observations and summaries like:

```text
Request: Review and understand continuous improvement rules from @ai_docs/continuous-improvement/rules.md
Investigated: Read and analyzed continuous improvement rules documentation
Learned: Rules emphasize trust-but-verify approach, fix-forward pattern, and systematic debugging
Completed: Established context for development practices including KISS, DRY, YAGNI principles
```

Alternatively, if SDK agent is instructed to skip routine research, the summary should accurately reflect this:

```text
Completed: Reviewed documentation files for context (no deliverable produced)
```

## Actual Behavior

Context-loading tasks are reported as failed file lookups:

```text
Request: Review and understand the rules from @ai_docs/continuous-improvement/rules.md
Investigated: Attempted to locate and read files. Files were searched using glob
patterns but do not exist in the current repository.
Completed: No work was completed... prerequisite files could not be found.
Learned: The source documents... are not yet created or accessible in the system.
```

Files were successfully read via Read tool, but SDK agent reports them as non-existent.

## Root Cause Analysis

### The Problem: Task Classification, Not Path Matching

**Location**: `src/sdk/prompts.ts` - `buildInitPrompt()` function (lines 24-126)

The SDK agent's system prompt contains conflicting guidance about research/learning tasks:

#### 1. Deliverable-Focused Instructions (Lines 27-49)

```typescript
CRITICAL: Record what was BUILT/FIXED/DEPLOYED/CONFIGURED, not what you (the observer) are doing.

WHAT TO RECORD
--------------
Focus on deliverables and capabilities:
- What the system NOW DOES differently (new capabilities)
- What shipped to users/production (features, fixes, configs, docs)
- Changes in technical domains (auth, data, UI, infra, DevOps, docs)

Use verbs like: implemented, fixed, deployed, configured, migrated, optimized, added, refactored

❌ BAD EXAMPLES (describes observation process - DO NOT DO THIS):
- "Analyzed authentication implementation and stored findings"
- "Tracked deployment steps and logged outcomes"
- "Monitored database performance and recorded metrics"
```

#### 2. Skip File Research Instruction (Lines 51-59)

```typescript
WHEN TO SKIP
------------
Skip routine operations:
- Empty status checks
- Package installations with no errors
- Simple file listings
- Repetitive operations you've already documented
- If file related research comes back as empty or not found  ← 🎯 THIS LINE
- **No output necessary if skipping.**
```

### What Actually Happens

**When user requests**: "Review and understand [files]"

1. Claude Code reads files successfully via Read tool ✅
2. User processes file content for context/learning ✅
3. No deliverable artifact is created (by design) ✅
4. SDK agent observes tool executions
5. SDK agent sees this is "file related research" with no deliverable
6. SDK agent: "Skip routine operations... file related research" → Skips creating observation
7. Summary generation: No observation exists → Assumes files weren't found
8. Summary incorrectly reports: "Files do not exist" ❌

### Why Action-Oriented Tasks Work

**When user requests**: "Convert [file] to agent"

1. Claude Code reads file successfully ✅
2. User creates new agent file ✅
3. Deliverable artifact exists ✅
4. SDK agent sees tool executions + file creation
5. SDK agent: "What shipped? New agent file" → Creates observation
6. Summary correctly reports what was built ✅

### The Mismatch

The `discovery` observation type exists (line 74: "learning about existing system"), but the prompt actively discourages using it:
- "DO NOT" record analysis/monitoring activities
- Skip "file related research"
- Focus on deliverables only

Context-loading tasks have nowhere to go in this framework.

### Timeline Evidence

Investigation showed this pattern is consistent:

**File creation:**
- `rules.md`: Created Nov 9, 12:29 AM
- `lessons-learned.md`: Created Nov 8, 8:40 PM

**"Review and understand" requests:**
- Multiple sessions from Nov 9, 2:11 AM onward (files existed for 1+ hours)

**Result:**
- Files successfully read via Read tool ✅
- Summaries reported "files do not exist" ❌
- Pattern consistent across sessions

This proves files existed and were accessible - the issue is task classification, not file availability.

## Suggested Fixes

### Option 1: Clarify "Discovery" Observation Type (Quick Fix)

Update the system prompt in `buildInitPrompt()` to clarify when `discovery` type should be used:

```typescript
// In src/sdk/prompts.ts, around line 68, update the discovery description:

  <type>[ bugfix | feature | refactor | change | discovery | decision ]</type>
  <!--
    **type**: MUST be EXACTLY one of these 6 options (no other values allowed):
      - bugfix: something was broken, now fixed
      - feature: new capability or functionality added
      - refactor: code restructured, behavior unchanged
      - change: generic modification (docs, config, misc)
      - discovery: learning about existing system, reviewing documentation, understanding patterns  ← UPDATE THIS
      - decision: architectural/design choice with rationale
  -->
```

And update the "WHEN TO SKIP" section (line 58):

```typescript
WHEN TO SKIP
------------
Skip routine operations:
- Empty status checks
- Package installations with no errors
- Simple file listings
- Repetitive operations you've already documented
- If file reads produced no usable content  ← CHANGE FROM "file related research"
- **No output necessary if skipping.**
```

**Pros**: Minimal change, clarifies existing observation type
**Cons**: Doesn't explicitly encourage recording context-loading tasks

### Option 2: Add Context-Loading Task Guidance (Better)

Add explicit guidance about research/learning tasks in `buildInitPrompt()`:

```typescript
// Add new section after "WHAT TO RECORD" (around line 50):

CONTEXT-LOADING TASKS
---------------------
When user requests understanding/learning (e.g., "review and understand files"):
- These ARE valuable observations (type: discovery)
- Record what was learned, not that learning occurred
- Focus on insights, patterns, rules discovered
- Even without deliverable code, knowledge gained matters

✅ GOOD EXAMPLES:
- "Project follows TDD workflow with RED-GREEN-REFACTOR cycle"
- "Continuous improvement rules emphasize trust-but-verify and fix-forward approach"
- "Authentication system uses OAuth2 PKCE flow for security"

❌ BAD EXAMPLES:
- "Read and analyzed rules documentation"
- "Reviewed continuous improvement files"
```

**Pros**: Clear guidance, encourages proper recording
**Cons**: Longer prompt, adds tokens

### Option 3: Separate Summary Logic for Non-Deliverable Tasks (Best)

Update summary generation to detect context-loading vs action-oriented tasks:

```typescript
// In buildSummaryPrompt(), add guidance:

When summarizing:
1. If Read tool succeeded → files WERE found (do not report as missing)
2. Context-loading tasks (review/understand/learn) are complete when files are read
3. No deliverable artifact ≠ no work completed
4. Record insights gained, even if no code was written
```

**Pros**: Addresses root cause directly
**Cons**: Still relies on LLM interpretation

## Workaround

**Current workarounds:**

1. **Rephrase requests** as action-oriented tasks with deliverables:
   - ❌ "Review and understand rules.md"
   - ✅ "Create a summary document of rules.md findings"

2. **Accept inaccurate summaries** for pure context-loading tasks and rely on observation records instead

3. **Manual verification**: Check that Read tool succeeded regardless of what summary reports

## Additional Context

Context-loading is a fundamental development workflow. Developers frequently need to:
- Review existing code/docs to understand systems
- Load project context before making changes
- Study patterns and best practices
- Understand dependencies and architecture

These research activities are valuable and should be recorded in the memory system. Currently, the SDK agent's deliverable-focused framing causes it to skip or misreport these legitimate activities, making memory search less useful for understanding what knowledge has been gathered over time.

The `discovery` observation type exists precisely for this use case, but the system prompt's emphasis on deliverables and instruction to skip "file related research" prevents it from being used correctly.

---

Thank you for claude-mem! It's a fantastic tool and this fix would make observations more comprehensive. Happy to provide any additional details or testing.
