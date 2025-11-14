---
description: Verify that PR claims match actual implementation
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [PR-number|branch-name]
---

# Task: Verify Pull Request Claims

**PR to verify:** $ARGUMENTS

**Purpose:** Verify that a PR's description, commits, and plan match actual implementation.

**Core 4 Foundation:**
- **Context:** PR metadata + git changes + plan documents
- **Model:** Semantic verification capabilities
- **Prompt:** This systematic verification process
- **Tools:** Git commands, gh CLI, file operations

---

## Instructions

You are verifying a pull request. Check that claims in PR description, commits, and plans match actual code changes.

### Core Principles

1. **Evidence before claims:** Never mark verified without git command output proving it
2. **Verify behavior, not names:** Check what code DOES. Different filenames can provide same functionality.
3. **Counter-evidence first:** Define what would disprove claim BEFORE checking
4. **Cross-reference patterns:** If comparing implementations, check what feature IS first

---

## Step 1: Identify PR and Extract Claims

### Determine PR Type

The argument could be:
- Branch name: `cursor/implement-plan-from-cu-plan-md-11ba`
- PR number: `#7` or `7`
- Comparison: `main...feature-branch`

**Commands to identify:**

```bash
# If branch name given, check if it exists
git show-ref --verify refs/heads/$ARGUMENTS 2>/dev/null || git show-ref --verify refs/remotes/origin/$ARGUMENTS

# If looks like PR number, try gh
gh pr view $ARGUMENTS 2>/dev/null

# Get comparison syntax
git log --oneline main...$ARGUMENTS | head -10
```

### Extract Claims

**From PR description (if available):**

```bash
gh pr view $ARGUMENTS --json body -q .body
```

**From commit messages:**

```bash
git log --format="%s%n%b" main...$ARGUMENTS
```

**From referenced plan documents:**

```bash
# Look for plan references in commits or PR description
git log main...$ARGUMENTS | grep -i "plan\|spec\|requirement"
```

**Common claim patterns to extract:**
- "Adds feature X"
- "Fixes bug Y"
- "Implements Z from plan"
- "Includes tests"
- "Updates documentation"
- "Breaking change"
- "Closes #123"

---

## Step 2: Verify Claims Against Implementation

### Feature Implementation Claims

**Claim pattern:** "Adds/Implements feature X"

**Verify:**

```bash
# What files changed?
git diff --name-only main...$ARGUMENTS

# Does feature exist in code?
git diff main...$ARGUMENTS -- path/to/feature

# Search for feature implementation
git show $ARGUMENTS:path/to/file | grep -A 10 "feature_name"
```

**Counter-evidence:** "This would be FALSE if no implementation exists for claimed feature"

### Test Coverage Claims

**Claim pattern:** "Includes tests" or "Adds test coverage"

**Verify:**

```bash
# Test files added?
git diff --name-only main...$ARGUMENTS | grep -i test

# Test functions added?
git diff main...$ARGUMENTS -- tests/ | grep "^+.*def test_"

# Count tests added
git show $ARGUMENTS:path/to/test.py | grep -c "def test_"
```

**Counter-evidence:** "This would be FALSE if no test files or test functions were added"

### Bug Fix Claims

**Claim pattern:** "Fixes bug #123" or "Resolves issue"

**Verify:**

```bash
# Related code changes?
git diff main...$ARGUMENTS | grep -A 5 -B 5 "bug_context"

# Issue referenced?
git log main...$ARGUMENTS | grep -i "#123\|issue"

# If gh available, check issue status
gh issue view 123 --json state,closedAt
```

### Plan/Requirement Verification

**Claim pattern:** "Implements plan from X" or "Follows requirements in Y"

**Verify:**

```bash
# Read plan document
cat path/to/plan.md

# Check each requirement against implementation
git diff main...$ARGUMENTS -- path/matching/requirement
```

**Counter-evidence:** "This would be FALSE if plan requirement X is not implemented"

### Breaking Change Claims

**Claim pattern:** "Breaking change" or "API change"

**Verify:**

```bash
# Check for removed/renamed functions
git diff main...$ARGUMENTS | grep "^-.*def \|^-.*class "

# Check for signature changes
git diff main...$ARGUMENTS -- path/to/api | grep -A 3 "^-.*def \|^+.*def "
```

### Documentation Claims

**Claim pattern:** "Updates documentation" or "Adds README"

**Verify:**

```bash
# Documentation files changed?
git diff --name-only main...$ARGUMENTS | grep -E "\.md$|docs/"

# Check actual changes
git diff main...$ARGUMENTS -- "*.md" docs/
```

---

## Step 3: Verify Line Counts and Stats

If PR claims specific statistics:

```bash
# Total lines changed
git diff --stat main...$ARGUMENTS

# Lines per file
git diff --numstat main...$ARGUMENTS

# Files changed count
git diff --name-only main...$ARGUMENTS | wc -l
```

---

## Step 4: Cross-Reference with Other PRs

If claims involve comparisons (e.g., "Different from PR #8"):

**Process:**
1. Verify what the claimed difference IS in the reference PR
2. Check if difference actually exists
3. Compare functionality, not just filenames

```bash
# Compare file structures
git diff --name-only main...pr-8-branch | sort > /tmp/pr8-files
git diff --name-only main...pr-9-branch | sort > /tmp/pr9-files
diff /tmp/pr8-files /tmp/pr9-files

# Compare implementations
git show pr-8-branch:path/to/file > /tmp/pr8-impl
git show pr-9-branch:path/to/file > /tmp/pr9-impl
diff /tmp/pr8-impl /tmp/pr9-impl
```

---

## Anti-Patterns (What NOT to Do)

❌ Trusting PR description without verifying code
❌ Verifying filename existence without checking implementation
❌ Assuming different filenames = missing functionality
❌ Claiming "tests added" without counting actual test functions
❌ Marking "implements plan" without checking each requirement
❌ Meta-analysis about the PR's philosophical meaning
❌ Comparing commits without comparing actual functionality

---

## Deliverable Format

## PR Overview

- **PR identifier:** $ARGUMENTS
- **Base branch:** [detected]
- **Files changed:** [count]
- **Commits:** [count]

## Claims Extracted

1. [Claim from PR description]
2. [Claim from commit message]
3. [Claim from plan reference]

## Verification Results

| Claim | Source | Verified? | Evidence |
|-------|--------|-----------|----------|
| [exact quote] | PR desc/commit/plan | ✅/❌/⚠️ | git command + key output |

## Summary

- Total claims checked: N
- Verified correct: N
- Found incorrect: N
- Critical mismatches: [list]

## Recommendation

[Based on verification: ready to merge / needs fixes / claims don't match implementation]

---

## Example: Verifying PR Implementation

**Given:** `/verify-pr cursor/implement-plan-from-cu-plan-md-11ba`

**Extract claims:**

```bash
# Check commits
git log --oneline main...cursor/implement-plan-from-cu-plan-md-11ba

# Find referenced plan
git log main...cursor/implement-plan-from-cu-plan-md-11ba | grep -i "plan"
# → References cu-plan.md
```

**Verify against cu-plan.md requirements:**

**Claim 1:** "Creates Jina MCP server"
```bash
git diff --name-only main...cursor/... | grep "jina.*mcp"
# → plugins/meta/claude-docs/mcp/jina_docs_mcp.py
```
✅ Verified

**Claim 2:** "Creates Jina direct API script"
```bash
git diff --name-only main...cursor/... | grep -i jina | grep scripts
# → plugins/meta/claude-docs/scripts/claude_docs_jina.py

# Verify it's direct API (not MCP)
git show cursor/...:plugins/meta/claude-docs/scripts/claude_docs_jina.py | grep "dependencies"
# → httpx>=0.27.0 (direct HTTP, not MCP)
```
✅ Verified

---

**Remember:** Your value is verifying that code matches claims. Boring verification is success. Trust the code, not the description.

**Foundation:** Context (PR + plans), Model (verification), Prompt (this process), Tools (git + gh).
