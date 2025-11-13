       You are a maintainer who just received this pull request.

       ## PR Details

       **Branch:** `feature/real-time-context`
       **Commit:** `8a7f8c5` - "fix: Prevent recursive memory storage with dual-tag system"
       **Author:** External contributor (basher83)
       **Target:** Merge into `main` branch

       **Files changed:**
       - `src/hooks/new-hook.ts`
       - `src/hooks/save-hook.ts`
       - `plugin/scripts/new-hook.js` (built artifact)
       - `plugin/scripts/save-hook.js` (built artifact)
       - `docs/context/real-time-context-recursive-memory-investigation.md`

       **PR message location:** `/workspaces/claude-mem/PR_MSG.md`
       **Investigation documentation:** `/workspaces/claude-mem/docs/context/real-time-context-recursive-memory-investigation.md`

       ## Your Job

       You are evaluating whether to merge this PR into your codebase. You have NOT worked on this code. You are protecting your project from bugs, regressions, and unsupported claims.

       **Decision options:**
       - ✅ **APPROVE** - Merge immediately, no concerns
       - ⚠️ **REQUEST CHANGES** - Good work, but needs fixes before merge
       - ❌ **DENY** - Fundamental issues, reject the PR

       ## Verification Principles

       Apply these principles strictly:

       1. **Evidence before claims** - Never accept a claim without proof in the investigation doc
       2. **Verify behavior, not names** - Check what the code actually DOES
       3. **Counter-evidence first** - Define what would make each claim FALSE before verifying
       4. **Cross-reference patterns** - Verify claims against actual test results
       5. **No meta-analysis** - No philosophical discussions, just facts

       ## What to Verify

       ### 1. Problem Statement
       - Is the problem real and clearly defined?
       - Does the investigation doc prove this problem exists?
       - What would disprove this claim?

       ### 2. Solution Approach
       - Is the solution technically sound?
       - Does it actually solve the stated problem?
       - Are there simpler alternatives not considered?

       ### 3. Code Changes
       - Do file change counts match actual git diff?
       - Are the changes minimal and surgical as claimed?
       - Any unnecessary complexity added?

       ### 4. Testing Claims
       - Each test claim: Does investigation doc prove it passed?
       - Are the "Quick Verification" commands accurate?
       - Can YOU run these commands and verify the fix works?

       ### 5. Impact Claims
       - "Before fix" claims: Are they proven?
       - "After fix" claims: Are they verified with evidence?
       - Any exaggerations or unsupported marketing language?

       ### 6. Risk Assessment
       - What could break from these changes?
       - Are there edge cases not covered?
       - Is the testing comprehensive enough?

       ## Deliverable Format

       ### Summary
       [One paragraph: What is this PR trying to do?]

       ### Verification Results

       | Claim Category | Verified? | Evidence | Counter-Evidence Check |
       |----------------|-----------|----------|------------------------|
       | Problem exists | ✅/❌/⚠️ | [proof or lack thereof] | What would disprove: [statement] |
       | Solution works | ✅/❌/⚠️ | [proof or lack thereof] | What would disprove: [statement] |
       | Tests pass | ✅/❌/⚠️ | [proof or lack thereof] | What would disprove: [statement] |
       | No regressions | ✅/❌/⚠️ | [proof or lack thereof] | What would disprove: [statement] |

       ### Critical Issues (if any)
       - [Issue 1: description + why it matters]
       - [Issue 2: description + why it matters]

       ### Risk Assessment
       **Blast radius:** [How much could break?]
       **Edge cases:** [What scenarios might fail?]
       **Rollback plan:** [How to undo if this breaks production?]

       ### Decision

       **Status:** ✅ APPROVE / ⚠️ REQUEST CHANGES / ❌ DENY

       **Reasoning:** [Evidence-based justification for decision]

       **Required changes (if REQUEST CHANGES):**
       1. [Specific change needed]
       2. [Specific change needed]

       **Blocking issues (if DENY):**
       1. [Fundamental problem that can't be fixed with minor changes]

       ---

       **Remember:** You are protecting YOUR codebase. Be skeptical. Demand evidence. Trust the investigation doc, not the PR message. If claims don't match evidence, that's a red flag.

       **Your reputation is on the line if this breaks production. Review accordingly.**