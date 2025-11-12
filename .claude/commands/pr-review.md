# Task: Verify PR Comparison Analysis Claims

**Document to review:** `docs/plans/claude-docs-upgrade/pr-comparison-analysis.md`

**Success criteria:** Accurate verification of factual claims through
code inspection.

**Failure mode to avoid:** Meta-analysis without verification.

## Instructions

You are reviewing a PR comparison analysis document. Your job is to
verify factual claims, not provide philosophical insights.

### Core Rules

1. **Evidence before claims:** Never mark a claim as verified without
   showing the git command and output that proves it
2. **No meta-analysis:** Do not write about recursive patterns,
   cognitive dynamics, or turtles. That's a distraction.
3. **Boring is good:** Methodical verification beats sophisticated
   commentary
4. **Show your work:** Every verification must include the command you
   ran
5. **Verify behavior, not names:** Don't just check if a file exists -
   check what the code DOES. A script named differently can still
   fulfill the requirement. Compare functionality across PRs, not just
   filenames.

### Required Process

For each major claim in the analysis:

1. **Extract the claim:** Quote it exactly
2. **Identify what would prove/disprove it:** What file/code would
   verify this?
3. **Define the counter-evidence:** Before running commands, explicitly
   state: "This claim would be FALSE if I found [specific evidence]"
   Focus on FUNCTIONALITY, not filenames.
4. **Cross-reference if needed:** If claim says "PR X missing Y but PR
   Z has Y", verify what Y actually IS in PR Z first, then look for
   equivalent functionality in PR X (any filename).
5. **Run the verification command:** Use git show/diff/grep
6. **Show the evidence:** Paste relevant output
7. **State verdict:** ✅ Verified / ❌ Incorrect / ⚠️ Partially true
8. **Move to next claim:** No commentary, just next verification

### Example Verification Format

**Claim:** "PR #7 missing Jina Reader direct API variation"

**What this means:** PR #7 lacks a script that makes direct HTTP calls
to r.jina.ai (not using MCP)

**Counter-evidence that would disprove:** Finding ANY script in PR #7 that:
- Uses httpx/requests (not MCP dependencies)
- Calls https://r.jina.ai/
- Downloads docs directly

**Commands:**
```bash
# Check what files PR #7 added
git diff --name-only main...cursor/implement-plan-from-cu-plan-md-11ba

# Check each script's dependencies
git show cursor/implement-plan-from-cu-plan-md-11ba:plugins/meta/claude-docs/scripts/claude_docs_jina.py | head -20

# Look for direct API calls
git show cursor/implement-plan-from-cu-plan-md-11ba:plugins/meta/claude-docs/scripts/claude_docs_jina.py | grep "r.jina.ai"
```

**Evidence:**
```text
Files: scripts/claude_docs_jina.py exists
Dependencies: httpx>=0.27.0 (not MCP)
API calls: jina_url = f"https://r.jina.ai/{url}"
```

**Verdict:** ❌ Incorrect - PR #7 DOES have Jina direct API in
`claude_docs_jina.py` (different naming than PR #8 but same functionality)

**Next claim...**

## What NOT to Do

❌ "This reveals interesting meta-patterns about..."
❌ "The analysis exhibits what it analyzes..."
❌ "I notice my own cognitive patterns..."
❌ "Turtles all the way down..."
❌ Any claim without git command evidence
❌ Verifying filename existence without checking what the code does
❌ Assuming different filenames = missing functionality
❌ Marking claims verified without understanding what they mean

## Deliverable Format

### Verification Results

| Claim   | Verified? | Evidence                 |
|---------|-----------|--------------------------|
| [quote] | ✅/❌/⚠️    | git command + key output |
| ...     | ...       | ...                      |

### Summary

- Total claims checked: N
- Verified correct: N
- Found incorrect: N
- Critical errors: [list]

### Recommendation

[One paragraph based solely on verified facts]

---
Remember: Your value is in catching errors, not in sounding
sophisticated. Boring verification is success. Meta-analysis is failure.
