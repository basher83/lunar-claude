---
description: Verify factual claims in documents against code repository using git evidence
allowed-tools: Bash(git:*), Bash(grep:*), Bash(wc:*)
argument-hint: <document-path>
---

# Task: Verify Claims About Code

**Document to verify:** $ARGUMENTS

**Purpose:** Verify factual claims in documents about code implementations, features, tests, or PRs.

**Core 4 Foundation:**
- **Context:** Document with claims + git repository state
- **Model:** Semantic verification capabilities
- **Prompt:** This systematic verification process
- **Tools:** Git commands, file operations

---

## Instructions

You are verifying claims in the document specified above. Your job is to check facts against source truth, not provide philosophical insights.

### Core Principles

1. **Evidence before claims:** Never mark verified without git command output proving it
2. **Verify behavior, not names:** Check what code DOES. Different filenames can provide same functionality.
3. **Counter-evidence first:** Define what would disprove claim BEFORE checking
4. **Cross-reference patterns:** If "X missing Y but Z has Y," check what Y IS in Z first
5. **No meta-analysis:** No recursive patterns, cognitive dynamics, or turtles

### Verification Process

For each claim:

1. **Extract claim:** Quote exactly
2. **Identify verification need:** What file/code would prove/disprove?
3. **Define counter-evidence:** "This claim would be FALSE if I found [specific evidence]"
   - Focus on FUNCTIONALITY not filenames
4. **Cross-reference if comparing:** Check what feature IS in reference first
5. **Run verification:** Use git show/diff/grep
6. **Show evidence:** Paste relevant output
7. **State verdict:** ✅ Verified / ❌ Incorrect / ⚠️ Partially true
8. **Move to next claim:** No commentary, just next verification

### Example: The Naming vs Functionality Pattern

**Claim:** "PR #7 missing Jina Reader direct API variation"

**What this means:** PR #7 lacks script making direct HTTP calls to r.jina.ai (not using MCP)

**Counter-evidence:** ANY script in PR #7 that:
- Uses httpx/requests (not MCP dependencies)
- Calls https://r.jina.ai/
- Downloads docs directly

**Commands:**

```bash
# Check what files exist
git diff --name-only main...feature-branch

# Check dependencies
git show feature-branch:path/to/script.py | head -20

# Check for API calls
git show feature-branch:path/to/script.py | grep "r.jina.ai"
```

**Evidence:**

```text
Files: scripts/claude_docs_jina.py exists
Dependencies: httpx>=0.27.0 (not MCP)
API calls: jina_url = f"https://r.jina.ai/{url}"
```

**Verdict:** ❌ Incorrect - PR #7 DOES have Jina direct API in `claude_docs_jina.py` (different naming but same functionality)

---

## Anti-Patterns (What NOT to Do)

❌ "This reveals interesting meta-patterns about..."
❌ "The analysis exhibits what it analyzes..."
❌ "I notice my own cognitive patterns..."
❌ "Turtles all the way down..."
❌ Any claim without git command evidence
❌ Verifying filename existence without checking what code does
❌ Assuming different filenames = missing functionality
❌ Marking verified without understanding what claim means

---

## Common Verification Scenarios

### Feature Implementation Claims

**Claim type:** "PR implements feature X"

**Verify:**
- Feature exists in code (not just mentioned in PR description)
- Implementation matches claimed approach
- Tests exist for feature (if claimed)

**Commands:**

```bash
git diff main...branch -- path/to/feature
git grep -n "feature_name" branch
git show branch:path/to/tests
```

### Test Coverage Claims

**Claim type:** "All features have tests"

**Verify:**
- Test files actually exist
- Tests actually test the claimed functionality
- Tests pass (if claimed)

**Commands:**

```bash
git diff --name-only main...branch | grep test
git show branch:path/to/test.py | grep "def test_"
git show branch:path/to/test.py | grep -A 10 "test_feature_name"
```

### Comparison Claims

**Claim type:** "PR A has X but PR B doesn't"

**Verify:**
- Check what X actually IS in PR A (dependencies, API calls, functionality)
- Look for EQUIVALENT functionality in PR B (any filename)
- Compare behavior, not names

**Commands:**

```bash
# Check PR A implementation
git show branch-a:file.py | grep "key_functionality"

# Look for equivalent in PR B (any file)
git grep -n "key_functionality" branch-b
```

### Line Count Claims

**Claim type:** "File has N lines"

**Verify:**
```bash
git show branch:path/to/file.py | wc -l
```

### Dependency Claims

**Claim type:** "Uses library X version Y"

**Verify:**
```bash
git show branch:requirements.txt | grep library
git show branch:pyproject.toml | grep library
git show branch:package.json | grep library
```

---

## Deliverable Format

### Verification Results

| Claim | Verified? | Evidence |
|-------|-----------|----------|
| [exact quote] | ✅/❌/⚠️ | git command + key output |

### Summary

- Total claims checked: N
- Verified correct: N
- Found incorrect: N
- Critical errors: [list]

### Recommendation

[One paragraph based solely on verified facts]

---

**Remember:** Your value is catching errors, not sounding sophisticated. Boring verification is success. Meta-analysis is failure.

**Foundation:** Context (document + repo), Model (verification), Prompt (this process), Tools (git commands).
