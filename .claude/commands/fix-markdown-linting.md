---
description: Fix markdown linting errors across repository using adaptive parallel subagents
allowed-tools: Bash(rumdl:*), Bash(scripts/rumdl-parser.py:*), Task
---

# Fix Markdown Linting Errors

Intelligently distribute markdown linting fixes across parallel subagents based on discovered errors.

## Workflow

### Step 1: Discovery

Run the rumdl parser in summary mode to analyze errors:

```bash
rumdl check . 2>&1 | scripts/rumdl-parser.py --summary
```

This outputs clean JSON with just the essentials:

- `total_files`: Number of files with errors
- `total_errors`: Total error count
- `files`: Array with file paths and error counts (sorted highest first, no detailed error info)

### Step 2: Decide Distribution Strategy

Based on the `total_files` count from Step 1:

**Decision criteria:**

- **0 files** → Done, no action needed
- **1 file** → Fix directly (no subagents needed)
- **2-5 files** → Run parser with `--distribute N` where N = total_files (one subagent per file)
- **6+ files** → Run parser with `--distribute 6` for balanced workload

**Example for 6+ files:**

```bash
rumdl check . 2>&1 | scripts/rumdl-parser.py --distribute 6
```

This adds a `distribution` array with balanced subagent assignments.

### Step 3: Parallel Execution

Using the exact file paths from the JSON distribution, launch all subagents in **a single message with multiple Task tool calls** to maximize efficiency.

### Step 4: Final Verification

After all subagents complete, verify the actual results:

```bash
rumdl check . 2>&1 | scripts/rumdl-parser.py --summary
```

Compare with Step 1 results:
- Total errors before vs after
- Files remaining with errors
- Actual reduction achieved

This confirms the fixes were successful and identifies any remaining issues.

## Instructions for Each Subagent

Each subagent receives:

**Assignment**: `[FILE_PATH]` or `[LIST_OF_FILE_PATHS]`

**Task**:

1. Run `rumdl check [FILE_PATH]` to verify current errors
2. Analyze the linting errors reported
3. Fix ONLY formatting/linting issues (line length, blank lines, list formatting, etc.)
4. DO NOT alter the semantic content of the file
5. DO NOT modify YAML frontmatter if errors are reported there
6. After fixing, run `rumdl check [FILE_PATH]` again to verify resolution
7. Report what was fixed

**Critical Constraints**:

- Only fix formatting/linting violations
- Never change the meaning or content of the documentation
- Skip frontmatter fixes entirely
- Verify fixes with `rumdl check` before completing

## Expected Outcome

All fixable markdown linting errors are resolved through efficient parallel execution.

## Report

After completing Steps 1-4, provide a comprehensive summary report:

**Example format:**

```markdown
## Fix Markdown Linting Report

**Before (Step 1)**:
- Total files checked: [NUMBER]
- Files with errors: [NUMBER]
- Total errors found: [NUMBER]

**After (Step 4)**:
- Files with errors: [NUMBER]
- Total errors remaining: [NUMBER]

**Changes**:
- Total errors fixed: [NUMBER]
- Total errors skipped: [NUMBER]
- Subagents created: [NUMBER]
- Success rate: [PERCENTAGE]%

**Details by File**:
- [FILE_PATH]: [COUNT] fixed, [COUNT] skipped
```
