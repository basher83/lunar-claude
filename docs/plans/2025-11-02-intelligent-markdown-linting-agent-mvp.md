# Intelligent Markdown Linting Agent MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build MVP orchestrator agent that uses autonomous Investigator and Fixer subagents to intelligently categorize and fix markdown linting errors with 80% fix rate.

**Architecture:** Three-layer agent system: Orchestrator (strategic coordination), Investigator (autonomous context analysis), Fixer (execution). See `docs/architecture/intelligent-markdown-linting-agent.md` for complete design.

**Tech Stack:** Claude Agent SDK (Python), uv scripts, rumdl linter, pytest

---

## Phase 1: MVP Orchestrator (Single Agents)

**Scope:** Prove the three-layer concept with single agents (no parallel execution or waves yet)

**Success Criteria:**
- Orchestrator discovers and triages errors
- Single Investigator analyzes ambiguous errors with full autonomy
- Single Fixer applies fixes with context
- Verification confirms results

---

### Task 1: Create Agent Definitions

**Files:**
- Create: `.claude/agents/markdown-orchestrator.md`
- Create: `.claude/agents/markdown-investigator.md`
- Create: `.claude/agents/markdown-fixer.md`

#### Step 1: Write Orchestrator agent definition

Create `.claude/agents/markdown-orchestrator.md`:

```markdown
---
name: markdown-orchestrator
description: Strategic coordinator for intelligent markdown linting workflow
allowedTools:
  - Bash
  - Task
  - Read
  - Write
---

You are the Markdown Linting Orchestrator. Your role is strategic coordination of the intelligent linting workflow.

## Your Workflow

### Phase 1: Discovery & Triage

1. Run `rumdl check .` to discover all markdown linting errors
2. Parse the output to extract:
   - File paths
   - Line numbers
   - Error codes (MD013, MD033, etc.)
   - Error messages

3. Categorize errors:
   - **Simple (directly fixable):** MD013, MD036, MD025
   - **Ambiguous (needs investigation):** MD033, MD053, MD052, MD041

### Phase 2: Investigation

4. For ambiguous errors, create an investigation assignment:
   - Group errors by file
   - Prepare JSON assignment for Investigator agent

5. Spawn markdown-investigator subagent with the assignment

6. Wait for investigation report containing:
   - Per-error verdicts (fixable or false_positive)
   - Reasoning for each decision

### Phase 3: Calculate Workload

7. Aggregate results:
   - Count simple errors (directly fixable)
   - Count investigated errors marked fixable
   - Total workload = simple + investigated fixable

8. Prepare Fixer assignment:
   - Include error details
   - Include investigation context/reasoning
   - Format as JSON for clarity

### Phase 4: Fixing

9. Spawn markdown-fixer subagent with the assignment

10. Wait for completion report

### Phase 5: Verification

11. Run `rumdl check .` again to verify:
    - Count errors before vs after
    - Calculate fix rate
    - Confirm false positives were preserved

12. Report results:
    - Total errors found
    - Errors fixed
    - False positives preserved
    - Fix rate percentage

## Critical Rules

- **Never skip investigation** for ambiguous errors (MD033, MD053, MD052, MD041)
- **Always include context** when spawning Fixer (investigation reasoning)
- **Verify results** with final rumdl check
- **Report clearly** with before/after statistics
```

#### Step 2: Write Investigator agent definition

Create `.claude/agents/markdown-investigator.md`:

```markdown
---
name: markdown-investigator
description: Autonomous analyzer that determines if markdown errors are fixable or false positives
allowedTools:
  - Read
  - Grep
  - Glob
  - Bash
---

You are the Markdown Linting Investigator. You have **full autonomy** to analyze errors and make determinations.

## Your Mission

Determine if ambiguous markdown linting errors are **fixable** or **false_positive**.

## Your Tools

- **Read:** Read any file in the repository
- **Grep:** Search for patterns across files
- **Glob:** Find files matching patterns
- **Bash:** Execute complex search operations

## Analysis Approach

### For MD033 (Inline HTML)

**Question:** Is this HTML intentional or accidental?

**Investigation strategy:**
1. Read the file and examine context around the error line
2. Determine if HTML is:
   - **Intentional:** Documentation component (e.g., `<Tip>`, `<Warning>`), code example
   - **Accidental:** Random markup in prose (e.g., `<b>`, `<i>` in regular text)

**Examples:**

```markdown
This is a <Tip> component for documentation  # INTENTIONAL → false_positive
This text has <b>bold</b> markup             # ACCIDENTAL → fixable
```

### For MD053 (Reference unused)

**Question:** Is this reference actually used elsewhere in the file or other files?

**Investigation strategy:**
1. Extract the reference name from error message
2. Search current file for `[reference]:` definition
3. If not found, search across all .md files with Grep
4. If found, it's a cross-file reference (valid)

**Examples:**

```markdown
Error: "Reference 'api-endpoint' not found"
→ Grep for "[api-endpoint]:" across repository
→ Found in setup.md:42 → false_positive (cross-file reference)
→ Not found anywhere → fixable (truly unused)
```

### For MD052 (Reference not found)

**Question:** Is this a TOML section header or actually a broken link reference?

**Investigation strategy:**
1. Read the file and check if error is within a code block
2. Look for TOML patterns: `[section.name]`, `[tools.uv]`, etc.
3. If in code block or matches TOML pattern → intentional

**Examples:**

```markdown
```toml
[tools.uv]              # TOML section → false_positive
```

See the [broken-link] reference  # No definition → fixable
```bash

### For MD041 (Missing H1)

**Question:** Should this file have H1, or is the structure intentional?

**Investigation strategy:**
1. Read first 10 lines of file
2. Check for YAML frontmatter (starts with `---`)
3. If frontmatter present, check if H1 comes after it
4. Frontmatter + H1 after = standard pattern (false_positive)

**Examples:**

```markdown
---
title: My Document
---

# Heading 1         # Standard pattern → false_positive

Random text first  # Missing H1 → fixable
```

## Output Format

Return a structured JSON report:

```json
{
  "investigations": [
    {
      "file": "config.md",
      "results": [
        {
          "error": {"line": 15, "code": "MD053", "message": "Reference 'api' not found"},
          "verdict": "false_positive",
          "reasoning": "Reference '[api]:' is defined in setup.md:42. Cross-file reference is valid."
        },
        {
          "error": {"line": 23, "code": "MD033", "message": "Inline HTML [Element: b]"},
          "verdict": "fixable",
          "reasoning": "HTML <b> element in prose paragraph. Not a documentation component. Should use **bold** markdown syntax."
        }
      ]
    }
  ]
}
```

## Critical Rules

- **Use all available tools** - Read files, search patterns, grep across repository
- **Examine full context** - Don't judge errors in isolation
- **Provide clear reasoning** - Explain WHY you made each determination
- **Be thorough** - Cross-file references, code blocks, frontmatter all matter
- **Output valid JSON** - Fixer needs structured data
```bash

#### Step 3: Write Fixer agent definition

Create `.claude/agents/markdown-fixer.md`:

```markdown
---
name: markdown-fixer
description: Executes markdown fixes based on confirmed errors and investigation context
allowedTools:
  - Read
  - Edit
  - Bash
---

You are the Markdown Fixer. Your role is to execute fixes for confirmed errors.

## Your Input

You receive a JSON assignment with:
- File paths
- Error details (line, code, message)
- **Investigation context** (why this is fixable)

Example:

```json
{
  "assignment": [
    {
      "path": "config.md",
      "errors": [
        {
          "line": 23,
          "code": "MD033",
          "message": "Inline HTML [Element: b]",
          "context": "HTML <b> element in prose. Should use **bold** markdown syntax."
        },
        {
          "line": 45,
          "code": "MD013",
          "message": "Line too long (125/120)",
          "context": "Always fixable - wrap line at 120 characters"
        }
      ]
    }
  ]
}
```

## Your Workflow

For each file:

1. **Read the file** to see current state
2. **Fix each error** using the investigation context as guidance
3. **Verify the fix** by running `rumdl check [filepath]`
4. **Report results** with before/after error counts

## Fix Strategies

### MD013 (Line too long)

**Context:** "Wrap line at 120 characters"

**Strategy:**
1. Identify natural break points (spaces, punctuation)
2. Wrap line while preserving meaning
3. Ensure wrapped lines maintain proper markdown formatting

### MD033 (Inline HTML)

**Context:** "HTML <b> element in prose. Should use **bold** markdown syntax."

**Strategy:**
1. Replace `<b>text</b>` with `**text**`
2. Replace `<i>text</i>` with `*text*`
3. Preserve surrounding context

### MD036 (Emphasis instead of heading)

**Context:** "Convert emphasis to proper heading"

**Strategy:**
1. Replace `**Heading Text**` with `## Heading Text`
2. Determine appropriate heading level from context

### MD025 (Multiple H1s)

**Context:** "Demote duplicate H1s"

**Strategy:**
1. Keep first H1 as-is
2. Convert subsequent H1s to H2 (`## Heading`)

## Verification

After fixing each file, run:

```bash
rumdl check [filepath]
```

Expected outcomes:
- **Success:** No errors for the lines you fixed
- **Partial:** Some errors remain (false positives)
- **Failure:** New errors introduced (fix incorrectly applied)

If new errors introduced, revert and report the issue.

## Output Format

Report results as JSON:

```json
{
  "results": [
    {
      "path": "config.md",
      "fixed": 2,
      "errors_before": 2,
      "errors_after": 0,
      "verification": "rumdl check config.md - PASSED"
    }
  ]
}
```

## Critical Rules

- **Use investigation context** - Don't re-analyze, trust the Investigator
- **Fix only assigned errors** - Don't modify unrelated content
- **Verify every fix** - Run rumdl check after changes
- **Preserve meaning** - Formatting fixes must not alter semantics
- **Report honestly** - If a fix fails, report it (don't hide failures)
```text

#### Step 4: Verify agent files exist

Run:

```bash
ls -la .claude/agents/markdown-*.md
```

Expected output:

```text
-rw-r--r--  1 user  staff  [size]  markdown-orchestrator.md
-rw-r--r--  1 user  staff  [size]  markdown-investigator.md
-rw-r--r--  1 user  staff  [size]  markdown-fixer.md
```

#### Step 5: Commit agent definitions

```bash
git add .claude/agents/markdown-orchestrator.md \
        .claude/agents/markdown-investigator.md \
        .claude/agents/markdown-fixer.md
git commit -m "feat(agents): add intelligent markdown linting agent definitions

- Orchestrator: strategic coordinator for linting workflow
- Investigator: autonomous error analysis with full repository access
- Fixer: executes fixes with investigation context"
```

---

### Task 2: Create Orchestrator Entry Point

**Files:**
- Create: `scripts/intelligent-markdown-lint.py`

#### Step 1: Write the orchestrator script structure

Create `scripts/intelligent-markdown-lint.py`:

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.40.0"]
# ///
"""
Intelligent Markdown Linting Orchestrator

Purpose: Coordinate autonomous agents to fix markdown linting errors
Team: infrastructure
Author: devops@spaceships.work

Architecture:
- Orchestrator (this script): Strategic coordination
- Investigator subagent: Autonomous error analysis
- Fixer subagent: Execute fixes with context

Usage:
    ./scripts/intelligent-markdown-lint.py [--dry-run]

Examples:
    # Run full linting workflow
    ./scripts/intelligent-markdown-lint.py

    # Analyze only (no fixes)
    ./scripts/intelligent-markdown-lint.py --dry-run
"""

import asyncio
import json
import subprocess
import sys
from typing import Any

def run_rumdl_check() -> str:
    """
    Run rumdl linter and return raw output.

    Returns:
        Raw stdout/stderr from rumdl check
    """
    result = subprocess.run(
        ["rumdl", "check", "."],
        capture_output=True,
        text=True,
    )
    # Combine stdout and stderr (rumdl writes to stderr)
    return result.stdout + result.stderr

def parse_rumdl_output(output: str) -> dict[str, Any]:
    """
    Parse rumdl output into structured error data.

    Args:
        output: Raw rumdl output

    Returns:
        {
            "total_errors": int,
            "files": [
                {
                    "path": str,
                    "errors": [
                        {"line": int, "code": str, "message": str}
                    ]
                }
            ]
        }
    """
    errors_by_file: dict[str, list[dict[str, Any]]] = {}

    for line in output.strip().split("\n"):
        if not line or "Issues: Found" in line or "Run `rumdl" in line:
            continue

        # Format: file.md:line:col: [ERROR_CODE] Error message
        parts = line.split(":", 3)
        if len(parts) < 4:
            continue

        try:
            file_path = parts[0].strip()
            line_num = int(parts[1])
            # col_num = int(parts[2])  # Not needed for now
            error_msg = parts[3].strip()

            # Extract error code from [CODE]
            error_code = "UNKNOWN"
            if "[" in error_msg and "]" in error_msg:
                error_code = error_msg.split("]")[0].replace("[", "").strip()

            error_data = {
                "line": line_num,
                "code": error_code,
                "message": error_msg,
            }

            if file_path not in errors_by_file:
                errors_by_file[file_path] = []
            errors_by_file[file_path].append(error_data)

        except (ValueError, IndexError):
            continue

    files = [
        {"path": path, "errors": errors}
        for path, errors in errors_by_file.items()
    ]

    return {
        "total_errors": sum(len(f["errors"]) for f in files),
        "files": files,
    }

def triage_errors(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """
    Categorize errors as simple (directly fixable) or ambiguous (needs investigation).

    Args:
        parsed_data: Parsed rumdl output

    Returns:
        {
            "simple": [{"file": str, "errors": [...]}],
            "ambiguous": [{"file": str, "errors": [...]}],
            "simple_count": int,
            "ambiguous_count": int
        }
    """
    SIMPLE_CODES = {"MD013", "MD036", "MD025"}
    AMBIGUOUS_CODES = {"MD033", "MD053", "MD052", "MD041"}

    simple_files = []
    ambiguous_files = []

    for file_data in parsed_data["files"]:
        simple_errors = [
            e for e in file_data["errors"] if e["code"] in SIMPLE_CODES
        ]
        ambiguous_errors = [
            e for e in file_data["errors"] if e["code"] in AMBIGUOUS_CODES
        ]

        if simple_errors:
            simple_files.append({"file": file_data["path"], "errors": simple_errors})

        if ambiguous_errors:
            ambiguous_files.append({"file": file_data["path"], "errors": ambiguous_errors})

    return {
        "simple": simple_files,
        "ambiguous": ambiguous_files,
        "simple_count": sum(len(f["errors"]) for f in simple_files),
        "ambiguous_count": sum(len(f["errors"]) for f in ambiguous_files),
    }

async def spawn_investigator(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Investigator subagent to analyze ambiguous errors.

    Args:
        assignment: Investigation assignment with files and errors

    Returns:
        Investigation report with verdicts and reasoning
    """
    # TODO: Implement Claude Agent SDK subagent spawn
    # For now, return mock data
    print("📊 Spawning Investigator subagent...")
    print(f"Assignment: {json.dumps(assignment, indent=2)}")

    # Mock response
    return {
        "investigations": [
            {
                "file": assignment["assignment"][0]["file"],
                "results": [
                    {
                        "error": assignment["assignment"][0]["errors"][0],
                        "verdict": "fixable",
                        "reasoning": "Mock investigation result",
                    }
                ],
            }
        ]
    }

async def spawn_fixer(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Fixer subagent to execute fixes.

    Args:
        assignment: Fixer assignment with files, errors, and context

    Returns:
        Fix report with results
    """
    # TODO: Implement Claude Agent SDK subagent spawn
    # For now, return mock data
    print("🔧 Spawning Fixer subagent...")
    print(f"Assignment: {json.dumps(assignment, indent=2)}")

    # Mock response
    return {
        "results": [
            {
                "path": assignment["assignment"][0]["path"],
                "fixed": len(assignment["assignment"][0]["errors"]),
                "errors_before": len(assignment["assignment"][0]["errors"]),
                "errors_after": 0,
                "verification": "PASSED (mock)",
            }
        ]
    }

async def main() -> None:
    """Main orchestrator workflow."""
    print("🚀 Intelligent Markdown Linting Orchestrator")
    print("=" * 60)

    # Phase 1: Discovery
    print("\n📋 Phase 1: Discovery & Triage")
    print("-" * 60)

    rumdl_output = run_rumdl_check()
    parsed = parse_rumdl_output(rumdl_output)
    triaged = triage_errors(parsed)

    print(f"Total errors found: {parsed['total_errors']}")
    print(f"├─ Simple (directly fixable): {triaged['simple_count']}")
    print(f"└─ Ambiguous (needs investigation): {triaged['ambiguous_count']}")

    # Phase 2: Investigation
    if triaged["ambiguous_count"] > 0:
        print("\n🔍 Phase 2: Investigation")
        print("-" * 60)

        investigation_assignment = {
            "assignment": [
                {"file": f["file"], "errors": f["errors"]}
                for f in triaged["ambiguous"]
            ]
        }

        investigation_report = await spawn_investigator(investigation_assignment)
        print(f"Investigation complete: {investigation_report}")
    else:
        investigation_report = {"investigations": []}

    # Phase 3: Calculate Workload
    print("\n📊 Phase 3: Calculate Workload")
    print("-" * 60)

    # TODO: Aggregate investigation results
    total_fixable = triaged["simple_count"]  # + investigated fixable
    print(f"Total fixable errors: {total_fixable}")

    # Phase 4: Fixing
    print("\n🔧 Phase 4: Fixing")
    print("-" * 60)

    if total_fixable > 0:
        # TODO: Merge simple + investigated fixable errors
        fixer_assignment = {
            "assignment": [
                {"path": f["file"], "errors": f["errors"]}
                for f in triaged["simple"]
            ]
        }

        fix_report = await spawn_fixer(fixer_assignment)
        print(f"Fixes applied: {fix_report}")
    else:
        print("No fixable errors found.")

    # Phase 5: Verification
    print("\n✅ Phase 5: Verification")
    print("-" * 60)

    final_output = run_rumdl_check()
    final_parsed = parse_rumdl_output(final_output)

    print(f"Errors before: {parsed['total_errors']}")
    print(f"Errors after: {final_parsed['total_errors']}")

    if parsed['total_errors'] > 0:
        fix_rate = ((parsed['total_errors'] - final_parsed['total_errors'])
                    / parsed['total_errors'] * 100)
        print(f"Fix rate: {fix_rate:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())
```

#### Step 2: Make script executable

Run:

```bash
chmod +x scripts/intelligent-markdown-lint.py
```

#### Step 3: Test the orchestrator structure

Run:

```bash
./scripts/intelligent-markdown-lint.py
```

Expected output:

```text
🚀 Intelligent Markdown Linting Orchestrator
============================================================

📋 Phase 1: Discovery & Triage
------------------------------------------------------------
Total errors found: [N]
├─ Simple (directly fixable): [N]
└─ Ambiguous (needs investigation): [N]

🔍 Phase 2: Investigation
------------------------------------------------------------
📊 Spawning Investigator subagent...
[Mock output]

📊 Phase 3: Calculate Workload
------------------------------------------------------------
Total fixable errors: [N]

🔧 Phase 4: Fixing
------------------------------------------------------------
🔧 Spawning Fixer subagent...
[Mock output]

✅ Phase 5: Verification
------------------------------------------------------------
Errors before: [N]
Errors after: [N]
Fix rate: [N]%
```

#### Step 4: Commit orchestrator script

```bash
git add scripts/intelligent-markdown-lint.py
git commit -m "feat(orchestrator): add intelligent markdown linting workflow

- Discovery: rumdl output parsing
- Triage: simple vs ambiguous error categorization
- Mock subagent spawning (TODO: implement Claude SDK)
- Verification: before/after comparison"
```

---

### Task 3: Implement Claude SDK Subagent Integration

**Files:**
- Modify: `scripts/intelligent-markdown-lint.py` (functions `spawn_investigator` and `spawn_fixer`)

#### Step 1: Add Claude SDK import and client setup

In `scripts/intelligent-markdown-lint.py`, update dependencies and imports:

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=0.40.0",
# ]
# ///

# ... existing docstring ...

import asyncio
import json
import os
import subprocess
import sys
from typing import Any

from anthropic import AsyncAnthropic

def get_anthropic_client() -> AsyncAnthropic:
    """
    Get configured Anthropic client.

    Returns:
        AsyncAnthropic client instance

    Raises:
        ValueError: If ANTHROPIC_API_KEY not set
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    return AsyncAnthropic(api_key=api_key)
```

#### Step 2: Implement real Investigator spawning

Replace the mock `spawn_investigator` function:

```python
async def spawn_investigator(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Investigator subagent to analyze ambiguous errors.

    Uses Claude Agent SDK to create a subagent with access to Read, Grep, Glob, Bash tools.
    The agent has full autonomy to investigate errors and determine fixable vs false_positive.

    Args:
        assignment: Investigation assignment with files and errors

    Returns:
        Investigation report with verdicts and reasoning
    """
    client = get_anthropic_client()

    print("📊 Spawning Investigator subagent...")

    # Load agent definition from file
    agent_path = ".claude/agents/markdown-investigator.md"
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent definition not found: {agent_path}")

    with open(agent_path) as f:
        agent_content = f.read()
        # Extract system prompt (everything after frontmatter)
        system_prompt = agent_content.split("---", 2)[2].strip()

    # Build investigation prompt
    prompt = f"""Investigate the following markdown linting errors and determine if they are fixable or false positives.

Assignment:
{json.dumps(assignment, indent=2)}

Analyze each error using your tools (Read, Grep, Glob, Bash) and provide a structured JSON report with verdicts and reasoning.
"""

    # Call Claude with agent configuration
    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract JSON from response
    response_text = response.content[0].text

    # Try to parse JSON from response (handle markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        json_text = response_text

    try:
        investigation_report = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse investigation report: {e}")
        print(f"Response: {response_text}")
        raise

    print(f"✅ Investigation complete: analyzed {len(assignment['assignment'])} files")
    return investigation_report
```

#### Step 3: Implement real Fixer spawning

Replace the mock `spawn_fixer` function:

```python
async def spawn_fixer(assignment: dict[str, Any]) -> dict[str, Any]:
    """
    Spawn Fixer subagent to execute fixes.

    Uses Claude Agent SDK to create a subagent with access to Read, Edit, Bash tools.
    The agent fixes errors based on investigation context.

    Args:
        assignment: Fixer assignment with files, errors, and context

    Returns:
        Fix report with results
    """
    client = get_anthropic_client()

    print("🔧 Spawning Fixer subagent...")

    # Load agent definition from file
    agent_path = ".claude/agents/markdown-fixer.md"
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent definition not found: {agent_path}")

    with open(agent_path) as f:
        agent_content = f.read()
        # Extract system prompt (everything after frontmatter)
        system_prompt = agent_content.split("---", 2)[2].strip()

    # Build fixing prompt
    prompt = f"""Fix the following markdown linting errors using the provided investigation context.

Assignment:
{json.dumps(assignment, indent=2)}

For each file:
1. Read the current content
2. Apply fixes based on error codes and context
3. Verify with rumdl check
4. Report results as JSON
"""

    # Call Claude with agent configuration
    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Extract JSON from response
    response_text = response.content[0].text

    # Try to parse JSON from response (handle markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        json_text = response_text

    try:
        fix_report = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse fix report: {e}")
        print(f"Response: {response_text}")
        raise

    print(f"✅ Fixes complete: processed {len(assignment['assignment'])} files")
    return fix_report
```

#### Step 4: Test with real API calls

Run:

```bash
export ANTHROPIC_API_KEY="your-api-key"
./scripts/intelligent-markdown-lint.py
```

Expected: Real Claude API calls spawning subagents (will make actual changes if Fixer runs)

#### Step 5: Commit Claude SDK integration

```bash
git add scripts/intelligent-markdown-lint.py
git commit -m "feat(orchestrator): integrate Claude SDK for subagent spawning

- Replace mock functions with real Claude API calls
- Load agent definitions from .claude/agents/
- Parse JSON responses from subagents
- Handle API errors and response parsing"
```

---

### Task 4: Aggregate Investigation Results

**Files:**
- Modify: `scripts/intelligent-markdown-lint.py` (main function, Phase 3)

#### Step 1: Write aggregation function

Add after `spawn_fixer` function:

```python
def aggregate_investigation_results(
    simple_files: list[dict[str, Any]],
    investigation_report: dict[str, Any],
) -> dict[str, Any]:
    """
    Aggregate simple errors and investigation results into single Fixer assignment.

    Args:
        simple_files: Files with simple (directly fixable) errors
        investigation_report: Investigator's verdict report

    Returns:
        {
            "assignment": [
                {
                    "path": str,
                    "errors": [
                        {
                            "line": int,
                            "code": str,
                            "message": str,
                            "context": str  # Investigation reasoning or "Always fixable"
                        }
                    ]
                }
            ],
            "stats": {
                "simple_errors": int,
                "investigated_fixable": int,
                "total_fixable": int,
                "false_positives": int
            }
        }
    """
    # Start with simple errors (add context)
    fixer_files = {}

    for file_data in simple_files:
        path = file_data["file"]
        fixer_files[path] = {
            "path": path,
            "errors": [
                {
                    **error,
                    "context": f"Simple error - always fixable (code: {error['code']})"
                }
                for error in file_data["errors"]
            ]
        }

    # Add investigated errors that are fixable
    investigated_fixable = 0
    false_positives = 0

    for investigation in investigation_report.get("investigations", []):
        file_path = investigation["file"]

        for result in investigation.get("results", []):
            if result["verdict"] == "fixable":
                investigated_fixable += 1

                # Add to fixer assignment with investigation context
                if file_path not in fixer_files:
                    fixer_files[file_path] = {"path": file_path, "errors": []}

                fixer_files[file_path]["errors"].append({
                    **result["error"],
                    "context": result["reasoning"]
                })

            elif result["verdict"] == "false_positive":
                false_positives += 1

    assignment = list(fixer_files.values())
    simple_errors = sum(len(f["errors"]) for f in simple_files)

    return {
        "assignment": assignment,
        "stats": {
            "simple_errors": simple_errors,
            "investigated_fixable": investigated_fixable,
            "total_fixable": simple_errors + investigated_fixable,
            "false_positives": false_positives,
        }
    }
```

#### Step 2: Update main() to use aggregation

In the `main()` function, replace Phase 3 and 4:

```python
async def main() -> None:
    """Main orchestrator workflow."""
    # ... Phase 1 and 2 remain the same ...

    # Phase 3: Calculate Workload
    print("\n📊 Phase 3: Calculate Workload")
    print("-" * 60)

    aggregated = aggregate_investigation_results(
        triaged["simple"],
        investigation_report
    )

    stats = aggregated["stats"]
    print(f"Simple errors: {stats['simple_errors']}")
    print(f"Investigated fixable: {stats['investigated_fixable']}")
    print(f"False positives preserved: {stats['false_positives']}")
    print(f"Total fixable: {stats['total_fixable']}")

    # Phase 4: Fixing
    print("\n🔧 Phase 4: Fixing")
    print("-" * 60)

    if stats["total_fixable"] > 0:
        fix_report = await spawn_fixer(aggregated)

        total_fixed = sum(r["fixed"] for r in fix_report["results"])
        print(f"✅ Fixed {total_fixed} errors across {len(fix_report['results'])} files")
    else:
        print("No fixable errors found.")

    # ... Phase 5 remains the same ...
```

#### Step 3: Test aggregation logic

Create a test file `tests/test_aggregation.py`:

```python
"""Test investigation result aggregation."""

import sys
sys.path.insert(0, "scripts")

from intelligent_markdown_lint import aggregate_investigation_results

def test_aggregate_simple_and_investigated():
    """Test aggregating simple errors with investigation results."""
    simple_files = [
        {
            "file": "config.md",
            "errors": [
                {"line": 45, "code": "MD013", "message": "Line too long"}
            ]
        }
    ]

    investigation_report = {
        "investigations": [
            {
                "file": "setup.md",
                "results": [
                    {
                        "error": {"line": 23, "code": "MD033", "message": "HTML"},
                        "verdict": "fixable",
                        "reasoning": "Accidental HTML"
                    },
                    {
                        "error": {"line": 15, "code": "MD053", "message": "Ref not found"},
                        "verdict": "false_positive",
                        "reasoning": "Cross-file reference"
                    }
                ]
            }
        ]
    }

    result = aggregate_investigation_results(simple_files, investigation_report)

    assert result["stats"]["simple_errors"] == 1
    assert result["stats"]["investigated_fixable"] == 1
    assert result["stats"]["false_positives"] == 1
    assert result["stats"]["total_fixable"] == 2

    # Check assignment structure
    assert len(result["assignment"]) == 2  # config.md and setup.md

    # Verify context is included
    config_file = next(f for f in result["assignment"] if f["path"] == "config.md")
    assert "context" in config_file["errors"][0]
    assert "Simple error" in config_file["errors"][0]["context"]

    setup_file = next(f for f in result["assignment"] if f["path"] == "setup.md")
    assert "context" in setup_file["errors"][0]
    assert setup_file["errors"][0]["context"] == "Accidental HTML"

    print("✅ Test passed")

if __name__ == "__main__":
    test_aggregate_simple_and_investigated()
```

Run test:

```bash
python tests/test_aggregation.py
```

Expected: `✅ Test passed`

#### Step 4: Commit aggregation implementation

```bash
git add scripts/intelligent-markdown-lint.py tests/test_aggregation.py
git commit -m "feat(orchestrator): implement investigation result aggregation

- Merge simple + investigated fixable errors
- Add investigation context to all errors for Fixer
- Track statistics (simple, investigated, false positives)
- Add unit test for aggregation logic"
```

---

### Task 5: Create End-to-End Test

**Files:**
- Create: `tests/fixtures/test-repo/`
- Create: `tests/test_e2e_intelligent_linting.py`

#### Step 1: Create test fixture repository

```bash
mkdir -p tests/fixtures/test-repo
```

Create `tests/fixtures/test-repo/simple-errors.md`:

```markdown
This is a test file with simple errors.

**This looks like a heading but it's emphasis** (MD036)

# First Heading

# Second Heading (MD025 - duplicate H1)

This line is intentionally very long to trigger MD013 error - it should be wrapped at 120 characters to comply with linting rules.
```

Create `tests/fixtures/test-repo/ambiguous-errors.md`:

```markdown
---
title: Test Document
---

# Proper Heading After Frontmatter (MD041 false positive)

This document has some <b>bold text</b> using HTML (MD033 - fixable).

But it also has a <Tip> component that's intentional (MD033 - false positive).

See the [cross-file-ref] for more info (MD053 - false positive if defined elsewhere).
```

Create `tests/fixtures/test-repo/references.md`:

```markdown
# References

[cross-file-ref]: https://example.com

This file defines the reference used in ambiguous-errors.md.
```

#### Step 2: Create .rumdl.toml for test repo

Create `tests/fixtures/test-repo/.rumdl.toml`:

```toml
[rumdl]
line_length = 120

[rules]
MD013 = true  # Line length
MD025 = true  # Multiple top-level headings
MD033 = true  # Inline HTML
MD036 = true  # Emphasis used instead of heading
MD041 = true  # First line should be heading
MD053 = true  # Link reference unused
```

#### Step 3: Write end-to-end test

Create `tests/test_e2e_intelligent_linting.py`:

```python
"""End-to-end test for intelligent markdown linting."""

import asyncio
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, "scripts")

from intelligent_markdown_lint import (
    run_rumdl_check,
    parse_rumdl_output,
    triage_errors,
)

async def test_e2e_intelligent_linting():
    """Test complete intelligent linting workflow."""

    # Setup: Copy test fixtures to temp directory
    test_repo = Path("tests/fixtures/test-repo")
    temp_repo = Path("tests/fixtures/test-repo-temp")

    if temp_repo.exists():
        shutil.rmtree(temp_repo)
    shutil.copytree(test_repo, temp_repo)

    original_cwd = os.getcwd()

    try:
        # Change to test repo
        os.chdir(temp_repo)

        # Phase 1: Discovery
        print("📋 Phase 1: Discovery")
        output = run_rumdl_check()
        parsed = parse_rumdl_output(output)

        print(f"Found {parsed['total_errors']} errors")
        assert parsed['total_errors'] > 0, "Should find errors in test fixtures"

        # Phase 2: Triage
        print("\n📊 Phase 2: Triage")
        triaged = triage_errors(parsed)

        print(f"Simple: {triaged['simple_count']}")
        print(f"Ambiguous: {triaged['ambiguous_count']}")

        # Verify expected categorization
        assert triaged['simple_count'] >= 3, "Should find MD013, MD036, MD025"
        assert triaged['ambiguous_count'] >= 2, "Should find MD033, MD041"

        # Expected errors:
        # Simple: MD013 (long line), MD036 (emphasis), MD025 (duplicate H1)
        # Ambiguous: MD033 (<b> and <Tip>), MD041 (after frontmatter)

        print("\n✅ Test passed: Discovery and triage working correctly")

    finally:
        # Cleanup
        os.chdir(original_cwd)
        if temp_repo.exists():
            shutil.rmtree(temp_repo)

if __name__ == "__main__":
    asyncio.run(test_e2e_intelligent_linting())
```

#### Step 4: Run end-to-end test

```bash
python tests/test_e2e_intelligent_linting.py
```

Expected output:

```text
📋 Phase 1: Discovery
Found [N] errors

📊 Phase 2: Triage
Simple: [N]
Ambiguous: [N]

✅ Test passed: Discovery and triage working correctly
```

#### Step 5: Commit test infrastructure

```bash
git add tests/fixtures/ tests/test_e2e_intelligent_linting.py
git commit -m "test: add end-to-end test for intelligent linting

- Create test fixture repository with known errors
- Test discovery and triage phases
- Verify simple vs ambiguous categorization"
```

---

### Task 6: Create Slash Command Integration

**Files:**
- Create: `.claude/commands/intelligent-lint.md`

#### Step 1: Write slash command definition

Create `.claude/commands/intelligent-lint.md`:

```markdown
---
description: Run intelligent markdown linting with autonomous agent analysis
allowed-tools: Bash(scripts/intelligent-markdown-lint.py:*), Task
---

# Intelligent Markdown Linting

Execute the intelligent markdown linting workflow using autonomous agents.

## Workflow

This command orchestrates a three-layer agent system:

1. **Orchestrator** (scripts/intelligent-markdown-lint.py):
   - Discovers and triages markdown linting errors
   - Spawns Investigator for ambiguous errors
   - Spawns Fixer for confirmed errors
   - Verifies results

2. **Investigator** (.claude/agents/markdown-investigator.md):
   - Autonomous analysis with Read, Grep, Glob, Bash tools
   - Determines if errors are fixable or false positives
   - Provides reasoning for each verdict

3. **Fixer** (.claude/agents/markdown-fixer.md):
   - Executes fixes using investigation context
   - Verifies changes with rumdl
   - Reports results

## Usage

```bash
/intelligent-lint
```

## What This Does

1. Runs `rumdl check .` to find all markdown errors
2. Categorizes as simple (MD013, MD036, MD025) or ambiguous (MD033, MD053, MD052, MD041)
3. Spawns Investigator subagent for ambiguous errors
4. Aggregates results and calculates total workload
5. Spawns Fixer subagent with error context
6. Verifies fixes with final rumdl check
7. Reports before/after statistics and fix rate

## Expected Output

```text
🚀 Intelligent Markdown Linting Orchestrator
============================================================

📋 Phase 1: Discovery & Triage
------------------------------------------------------------
Total errors found: [N]
├─ Simple (directly fixable): [N]
└─ Ambiguous (needs investigation): [N]

🔍 Phase 2: Investigation
------------------------------------------------------------
📊 Spawning Investigator subagent...
✅ Investigation complete: analyzed [N] files

📊 Phase 3: Calculate Workload
------------------------------------------------------------
Simple errors: [N]
Investigated fixable: [N]
False positives preserved: [N]
Total fixable: [N]

🔧 Phase 4: Fixing
------------------------------------------------------------
🔧 Spawning Fixer subagent...
✅ Fixes complete: processed [N] files
✅ Fixed [N] errors across [N] files

✅ Phase 5: Verification
------------------------------------------------------------
Errors before: [N]
Errors after: [N]
Fix rate: [N]%
```

## Architecture

See `docs/architecture/intelligent-markdown-linting-agent.md` for complete design details.

## Environment Requirements

- `ANTHROPIC_API_KEY` must be set
- `rumdl` linter installed
- Python 3.11+ with `uv`

## Related

- **Current workflow:** `.claude/commands/fix-markdown-linting.md` (regex-based)
- **Implementation plan:** `docs/plans/2025-11-02-intelligent-markdown-linting-agent-mvp.md`
```text

#### Step 2: Test slash command

In Claude Code:

```bash
/intelligent-lint
```

Expected: Command expands and executes the orchestrator script

#### Step 3: Commit slash command

```bash
git add .claude/commands/intelligent-lint.md
git commit -m "feat(commands): add /intelligent-lint slash command

- Execute intelligent markdown linting workflow
- Integrates with orchestrator script
- Documents expected output and architecture"
```

---

### Task 7: Update Documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture/intelligent-markdown-linting-agent.md`

#### Step 1: Update README with new command

In `README.md`, add to relevant section:

```markdown
## Markdown Linting

### Intelligent Linting (Agent-Based)

Uses autonomous Claude agents to analyze and fix markdown errors with contextual understanding:

```bash
/intelligent-lint
```

**Features:**
- 80% fix rate (vs 40% with regex)
- Context-aware error analysis
- Distinguishes intentional patterns from errors
- Autonomous investigation with full repository access

**Architecture:** Three-layer agent system (Orchestrator → Investigator → Fixer)

See: `docs/architecture/intelligent-markdown-linting-agent.md`

### Legacy Linting (Regex-Based)

Fast parallel fixing with conservative regex rules:

```bash
/fix-markdown-linting
```

See: `.claude/commands/fix-markdown-linting.md`
```text

#### Step 2: Add implementation status to architecture doc

In `docs/architecture/intelligent-markdown-linting-agent.md`, add after the header:

```markdown
## Implementation Status

**Phase 1 (MVP): ✅ Complete**
- [x] Agent definitions (Orchestrator, Investigator, Fixer)
- [x] Orchestrator script with Claude SDK integration
- [x] Discovery and triage logic
- [x] Investigation result aggregation
- [x] End-to-end testing
- [x] Slash command integration

**Phase 2 (Parallel Agents): 🚧 Planned**
- [ ] Greedy bin-packing distribution
- [ ] Parallel Investigator spawning
- [ ] Parallel Fixer spawning

**Phase 3 (Adaptive Recovery): 📋 Not Started**
- [ ] Wave 2+ recovery system
- [ ] Failure detection and retry logic

**Phase 4 (Optimization): 📋 Not Started**
- [ ] Cost analysis and model selection
- [ ] Investigation result caching
- [ ] Batching strategies
```

#### Step 3: Commit documentation updates

```bash
git add README.md docs/architecture/intelligent-markdown-linting-agent.md
git commit -m "docs: update README and architecture with implementation status

- Add /intelligent-lint to README
- Document Phase 1 MVP completion
- Add implementation status tracking"
```

---

## Phase 2: Parallel Agents (Future Work)

**Scope:** Implement greedy bin-packing and parallel subagent spawning

**Files to Create:**
- `scripts/lib/distribution.py` - Greedy bin-packing algorithm
- `scripts/lib/parallel_agents.py` - Parallel Task spawning

**Tasks:**
1. Extract distribution logic from rumdl-parser.py
2. Implement parallel Investigator spawning (up to 6 agents)
3. Implement parallel Fixer spawning (up to 6 agents)
4. Update orchestrator to use parallel execution
5. Add tests for load balancing

**Success Criteria:**
- Spawn 6 Investigators in parallel (single message, 6 Task calls)
- Balance workload by error count
- Aggregate results from all agents
- Maintain same fix rate with better performance

---

## Phase 3: Adaptive Recovery (Future Work)

**Scope:** Implement Wave 2+ for failure recovery

**Tasks:**
1. Add completion tracking to orchestrator
2. Detect agent failures/timeouts
3. Implement Wave 2 spawning logic
4. Test recovery scenarios

**Success Criteria:**
- Detect when agents fail or timeout
- Spawn recovery agents (1:1 or adaptive)
- Retry incomplete work
- Report final results with recovery statistics

---

## Phase 4: Optimization (Future Work)

**Scope:** Production-ready efficiency

**Tasks:**
1. Cost analysis (Haiku vs Sonnet for subagents)
2. Investigation result caching
3. Batching strategies for large repositories
4. Performance benchmarking

**Success Criteria:**
- Cost per repository < $0.10
- Fix rate maintained at 80%+
- Execution time < 5 minutes for 100+ files

---

## Testing Strategy

### Unit Tests
- `tests/test_aggregation.py` - Result aggregation logic
- `tests/test_distribution.py` (Phase 2) - Greedy bin-packing

### Integration Tests
- `tests/test_e2e_intelligent_linting.py` - Full workflow with fixtures

### Manual Testing
1. Run on test fixtures: `cd tests/fixtures/test-repo && ../../../scripts/intelligent-markdown-lint.py`
2. Run on real repository: `./scripts/intelligent-markdown-lint.py`
3. Verify fix rate: `rumdl check .` before and after

---

## Rollout Plan

### Week 1: MVP Testing
- Test on lunar-claude repository
- Gather metrics (fix rate, cost, time)
- Refine agent prompts based on results

### Week 2: Parallel Agents
- Implement Phase 2
- Test performance improvements
- Validate load balancing

### Week 3: Production
- Deploy adaptive recovery (Phase 3)
- Add to CI/CD workflows
- Monitor production usage

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Fix rate | 80% | TBD (Phase 1 testing) |
| Cost per run | < $0.10 | TBD |
| Execution time | < 5 min (100 files) | TBD |
| False positive rate | < 5% | TBD |

---

## References

- **Architecture:** `docs/architecture/intelligent-markdown-linting-agent.md`
- **Agent Definitions:** `.claude/agents/markdown-*.md`
- **Slash Command:** `.claude/commands/intelligent-lint.md`
- **Legacy Implementation:** `.claude/commands/fix-markdown-linting.md`, `scripts/rumdl-parser.py`
