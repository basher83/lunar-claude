# Skill Auditor SDK Application Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a deterministic skill-auditor using Claude Agent SDK that extracts metrics with Python and provides convergent, actionable feedback without bash hallucination.

**Architecture:** Python script extracts all audit metrics deterministically from SKILL.md files, then uses Claude Agent SDK's `query()` function (no tools allowed) to analyze the pre-extracted metrics and generate audit reports. This eliminates bash command hallucination and ensures same metrics = same analysis.

**Tech Stack:**
- Claude Agent SDK (Python) >=0.1.6
- Python 3.11+ with uv script headers
- anyio for async runtime
- pathlib for file operations
- re for deterministic regex extraction
- json for structured data passing

---

## Task 1: Create Metrics Extraction Module

**Files:**
- Create: `scripts/skill_auditor/metrics_extractor.py`
- Test: `scripts/skill_auditor/test_metrics_extractor.py`

### Step 1: Write the failing test for description extraction

Create test file first (TDD):

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for metrics_extractor module."""

import pytest
from pathlib import Path
from metrics_extractor import extract_skill_metrics

def test_extract_description_from_skill_md(tmp_path):
    """Test extraction of description field from YAML frontmatter."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: >
  This is a test skill with "quoted phrases" for testing.
  It has multiple lines.
---

# Test Skill

Content here.
""")

    metrics = extract_skill_metrics(tmp_path)

    assert "description" in metrics
    assert "test skill" in metrics["description"].lower()
    assert "quoted phrases" in metrics["description"]
```

### Step 2: Run test to verify it fails

```bash
cd /workspaces/lunar-claude
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: FAIL with "ModuleNotFoundError: No module named 'metrics_extractor'"

### Step 3: Write minimal implementation for description extraction

```python
#!/usr/bin/env python3
"""Deterministic metrics extraction from SKILL.md files."""

import re
from pathlib import Path
from typing import Dict, Any

def extract_skill_metrics(skill_path: Path) -> Dict[str, Any]:
    """
    Extract all audit metrics from a skill directory.

    Args:
        skill_path: Path to skill directory containing SKILL.md

    Returns:
        Dictionary of extracted metrics
    """
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Extract description (between 'description: >' and '---')
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    return {
        "description": description,
    }
```

### Step 4: Run test to verify it passes

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: PASS

### Step 5: Commit description extraction

```bash
git add scripts/skill_auditor/
git commit -m "feat(skill-auditor): add description extraction from SKILL.md"
```

---

## Task 2: Add Quoted Phrase Extraction

**Files:**
- Modify: `scripts/skill_auditor/metrics_extractor.py`
- Modify: `scripts/skill_auditor/test_metrics_extractor.py`

### Step 1: Write failing test for quoted phrases

Add to test file:

```python
def test_extract_quoted_phrases(tmp_path):
    """Test extraction of quoted phrases from description."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: >
  Use when "creating skills", "validating SKILL.md",
  or "auditing against specs".
---
""")

    metrics = extract_skill_metrics(tmp_path)

    assert "quoted_phrases" in metrics
    assert len(metrics["quoted_phrases"]) == 3
    assert "creating skills" in metrics["quoted_phrases"]
    assert "validating SKILL.md" in metrics["quoted_phrases"]
    assert "auditing against specs" in metrics["quoted_phrases"]

def test_quoted_phrase_count(tmp_path):
    """Test quoted phrase count metric."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: Test with "phrase one" and "phrase two"
---
""")

    metrics = extract_skill_metrics(tmp_path)

    assert metrics["quoted_count"] == 2
```

### Step 2: Run test to verify it fails

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: FAIL with "KeyError: 'quoted_phrases'"

### Step 3: Implement quoted phrase extraction

Update `extract_skill_metrics` function:

```python
def extract_skill_metrics(skill_path: Path) -> Dict[str, Any]:
    """Extract all audit metrics from a skill directory."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Extract description
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract quoted phrases (deterministic regex)
    quoted_phrases = re.findall(r'"([^"]+)"', description)

    return {
        "description": description,
        "quoted_phrases": quoted_phrases,
        "quoted_count": len(quoted_phrases),
    }
```

### Step 4: Run test to verify it passes

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: PASS

### Step 5: Commit quoted phrase extraction

```bash
git add scripts/skill_auditor/
git commit -m "feat(skill-auditor): add quoted phrase extraction"
```

---

## Task 3: Add Domain Indicators and Binary Checks

**Files:**
- Modify: `scripts/skill_auditor/metrics_extractor.py`
- Modify: `scripts/skill_auditor/test_metrics_extractor.py`

### Step 1: Write failing test for domain indicators

Add to test file:

```python
def test_extract_domain_indicators(tmp_path):
    """Test extraction of domain-specific indicators."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: >
  Create SKILL.md files with YAML frontmatter for Claude Code.
  Validate skill structure and compliance.
---
""")

    metrics = extract_skill_metrics(tmp_path)

    assert "domain_indicators" in metrics
    # Should find: SKILL.md, YAML, frontmatter, Claude Code, skill, compliance
    assert len(metrics["domain_indicators"]) >= 5
    assert "SKILL.md" in metrics["domain_indicators"]
    assert "domain_count" in metrics
    assert metrics["domain_count"] >= 5
```

### Step 2: Run test to verify it fails

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: FAIL with "KeyError: 'domain_indicators'"

### Step 3: Implement domain indicator extraction

Update `extract_skill_metrics`:

```python
def extract_skill_metrics(skill_path: Path) -> Dict[str, Any]:
    """Extract all audit metrics from a skill directory."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Extract description
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract quoted phrases
    quoted_phrases = re.findall(r'"([^"]+)"', description)

    # Extract domain indicators (exact regex from v5 agent)
    domain_pattern = (
        r'\b(SKILL\.md|\.skill|YAML|Claude Code|Anthropic|'
        r'skill|research|validation|compliance|specification|frontmatter)\b'
    )
    domain_matches = re.findall(domain_pattern, description, re.IGNORECASE)
    domain_indicators = list(set(domain_matches))  # Unique only

    return {
        "description": description,
        "quoted_phrases": quoted_phrases,
        "quoted_count": len(quoted_phrases),
        "domain_indicators": domain_indicators,
        "domain_count": len(domain_indicators),
    }
```

### Step 4: Run test to verify it passes

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: PASS

### Step 5: Commit domain indicator extraction

```bash
git add scripts/skill_auditor/
git commit -m "feat(skill-auditor): add domain indicator extraction"
```

---

## Task 4: Add File-Level Binary Checks

**Files:**
- Modify: `scripts/skill_auditor/metrics_extractor.py`
- Modify: `scripts/skill_auditor/test_metrics_extractor.py`

### Step 1: Write failing tests for binary checks

Add to test file:

```python
def test_forbidden_files_detection(tmp_path):
    """Test detection of forbidden files."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("---\nname: test\n---")

    # Create forbidden file
    (tmp_path / "README.md").write_text("Forbidden")

    metrics = extract_skill_metrics(tmp_path)

    assert "forbidden_files" in metrics
    assert len(metrics["forbidden_files"]) == 1
    assert "README.md" in metrics["forbidden_files"]

def test_line_count(tmp_path):
    """Test SKILL.md line count."""
    skill_md = tmp_path / "SKILL.md"
    content = "---\nname: test\n---\n" + "\n".join([f"Line {i}" for i in range(100)])
    skill_md.write_text(content)

    metrics = extract_skill_metrics(tmp_path)

    assert "line_count" in metrics
    assert metrics["line_count"] > 100

def test_implementation_details_detection(tmp_path):
    """Test detection of implementation details in description."""
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: Uses script.py and helper.sh with /slash:command
---
""")

    metrics = extract_skill_metrics(tmp_path)

    assert "implementation_details" in metrics
    assert len(metrics["implementation_details"]) >= 2  # .py, .sh, /slash:command
```

### Step 2: Run test to verify it fails

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: FAIL with "KeyError: 'forbidden_files'"

### Step 3: Implement binary checks

Update `extract_skill_metrics`:

```python
def extract_skill_metrics(skill_path: Path) -> Dict[str, Any]:
    """Extract all audit metrics from a skill directory."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text()

    # Extract YAML frontmatter fields
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    skill_name = name_match.group(1).strip() if name_match else "unknown"

    # Extract description
    desc_match = re.search(
        r'description:\s*>\s*(.*?)^---',
        content,
        re.MULTILINE | re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract quoted phrases
    quoted_phrases = re.findall(r'"([^"]+)"', description)

    # Extract domain indicators
    domain_pattern = (
        r'\b(SKILL\.md|\.skill|YAML|Claude Code|Anthropic|'
        r'skill|research|validation|compliance|specification|frontmatter)\b'
    )
    domain_matches = re.findall(domain_pattern, description, re.IGNORECASE)
    domain_indicators = list(set(domain_matches))

    # Check for forbidden files (B1)
    forbidden_patterns = ["README*", "INSTALL*", "CHANGELOG*", "QUICK*"]
    forbidden_files = []
    for pattern in forbidden_patterns:
        forbidden_files.extend([f.name for f in skill_path.glob(pattern)])

    # Check for implementation details in description (B4)
    impl_pattern = r'\w+\.(py|sh|js|md|txt|json)|/[a-z-]+:[a-z-]+'
    implementation_details = re.findall(impl_pattern, description)

    # Line count (B3)
    line_count = len(content.split('\n'))

    # Check for YAML frontmatter (B2)
    has_frontmatter = content.startswith('---')
    yaml_delimiters = len(re.findall(r'^---$', content, re.MULTILINE))
    has_name = name_match is not None
    has_description = desc_match is not None

    return {
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "description": description,
        "quoted_phrases": quoted_phrases,
        "quoted_count": len(quoted_phrases),
        "domain_indicators": domain_indicators,
        "domain_count": len(domain_indicators),
        "forbidden_files": forbidden_files,
        "implementation_details": implementation_details,
        "line_count": line_count,
        "has_frontmatter": has_frontmatter,
        "yaml_delimiters": yaml_delimiters,
        "has_name": has_name,
        "has_description": has_description,
    }
```

### Step 4: Run test to verify it passes

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

Expected: PASS

### Step 5: Commit binary checks

```bash
git add scripts/skill_auditor/
git commit -m "feat(skill-auditor): add forbidden files, line count, and implementation detail checks"
```

---

## Task 5: Create Main SDK Application

**Files:**
- Create: `scripts/skill-auditor.py`

### Step 1: Write the SDK application skeleton

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
# ]
# ///
"""
Skill Auditor - Claude Agent SDK Application

Deterministic skill auditing with Python extraction and Claude analysis.

Usage:
    ./scripts/skill-auditor.py /path/to/skill/directory
"""

import sys
import json
from pathlib import Path

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage

# Import metrics extractor
sys.path.insert(0, str(Path(__file__).parent / "skill_auditor"))
from metrics_extractor import extract_skill_metrics

async def audit_skill(skill_path: Path):
    """
    Audit a skill using deterministic Python extraction + Claude analysis.

    Args:
        skill_path: Path to skill directory
    """
    print(f"🔍 Auditing skill: {skill_path}")
    print("=" * 60)

    # Step 1: Extract metrics deterministically (Python, no bash)
    print("\n📊 Extracting metrics...")
    try:
        metrics = extract_skill_metrics(skill_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return

    print(f"✅ Extracted {len(metrics)} metrics")
    print(f"   - Quoted phrases: {metrics['quoted_count']}")
    print(f"   - Domain indicators: {metrics['domain_count']}")
    print(f"   - Line count: {metrics['line_count']}")

    # Step 2: Configure SDK with NO tools (analysis only)
    options = ClaudeAgentOptions(
        system_prompt="""You are a skill auditor analyzing pre-extracted metrics.

CRITICAL RULES:
- DO NOT re-extract metrics
- DO NOT run bash commands
- DO NOT make up data
- ONLY analyze the JSON provided

Apply binary checks to the metrics and generate an audit report.""",
        allowed_tools=[],  # NO TOOLS - prevents hallucination
        model="claude-sonnet-4-5",
        max_turns=1  # Single analysis, no conversation
    )

    # Step 3: Build analysis prompt with metrics
    prompt = build_analysis_prompt(metrics)

    # Step 4: Query Claude for analysis
    print("\n🤖 Analyzing metrics with Claude...")

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

        elif isinstance(message, ResultMessage):
            if message.total_cost_usd:
                print(f"\n💰 Cost: ${message.total_cost_usd:.4f}")
            if message.duration_ms:
                print(f"⏱️  Duration: {message.duration_ms}ms")

def build_analysis_prompt(metrics: dict) -> str:
    """
    Build the analysis prompt with extracted metrics.

    Args:
        metrics: Extracted skill metrics

    Returns:
        Formatted prompt for Claude
    """
    # Calculate binary check results
    b1_pass = len(metrics["forbidden_files"]) == 0
    b2_pass = (metrics["yaml_delimiters"] == 2 and
               metrics["has_name"] and
               metrics["has_description"])
    b3_pass = metrics["line_count"] < 500
    b4_pass = len(metrics["implementation_details"]) == 0

    w1_pass = metrics["quoted_count"] >= 3
    w3_pass = metrics["domain_count"] >= 3

    prompt = f"""Audit the following skill metrics:

## Extracted Metrics

```json
{json.dumps(metrics, indent=2)}
```

## Binary Check Results

**BLOCKERS (Official Requirements):**
- B1: No forbidden files → {"✅ PASS" if b1_pass else "❌ FAIL"}
- B2: Valid YAML frontmatter → {"✅ PASS" if b2_pass else "❌ FAIL"}
- B3: SKILL.md under 500 lines → {"✅ PASS" if b3_pass else "❌ FAIL"}
- B4: No implementation details in description → {"✅ PASS" if b4_pass else "❌ FAIL"}

**WARNINGS (Effectiveness):**
- W1: ≥3 quoted phrases → {"✅ PASS" if w1_pass else "❌ FAIL"}
- W3: ≥3 domain indicators → {"✅ PASS" if w3_pass else "❌ FAIL"}

## Your Task

Generate a skill audit report following this format:

# Skill Audit Report: {metrics["skill_name"]}

**Status:** [🔴 BLOCKED | 🟡 READY WITH WARNINGS | 🟢 READY]

**Breakdown:**
- Blockers: [X] ❌
- Warnings: [X] ⚠️

## BLOCKERS ❌ ([X])

[List failed blocker checks with specific evidence from metrics]

## WARNINGS ⚠️ ([X])

[List failed warning checks with specific evidence from metrics]

## Next Steps

[Specific, actionable fixes based on failed checks]

---

IMPORTANT: Base your analysis ONLY on the metrics provided above. Do not re-extract or assume additional data.
"""

    return prompt

async def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: ./scripts/skill-auditor.py /path/to/skill/directory")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"❌ Error: Path does not exist: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        sys.exit(1)

    await audit_skill(skill_path)

if __name__ == "__main__":
    anyio.run(main)
```text

### Step 2: Make script executable

```bash
chmod +x scripts/skill-auditor.py
```

### Step 3: Test on skill-factory (manual verification)

```bash
./scripts/skill-auditor.py plugins/meta/meta-claude/skills/skill-factory
```

Expected output:
- Metrics extraction succeeds
- Claude analyzes the metrics
- Report shows status and checks

### Step 4: Verify determinism by running 3 times

```bash
for i in 1 2 3; do
  echo "=== Run $i ==="
  ./scripts/skill-auditor.py plugins/meta/meta-claude/skills/skill-factory | grep "Status:"
done
```

Expected: Same status in all 3 runs (convergent results)

### Step 5: Commit SDK application

```bash
git add scripts/skill-auditor.py
git commit -m "feat(skill-auditor): add Claude Agent SDK application with deterministic analysis"
```

---

## Task 6: Add Documentation

**Files:**
- Create: `scripts/skill_auditor/README.md`

### Step 1: Write README

```markdown
# Skill Auditor SDK Application

Deterministic skill auditing using Claude Agent SDK.

## Architecture

**Problem Solved:** Previous skill-auditor agents had non-deterministic bash command execution, causing agents to hallucinate different metric counts across runs. This led to feedback loops where fixing issues flagged in one run would be contradicted by the next run.

**Solution:**
1. **Python extracts all metrics** - Deterministic regex/file operations, no bash
2. **Claude analyzes pre-extracted data** - No tool access, can't hallucinate new extractions
3. **Same metrics = same analysis** - Convergent feedback across runs

## Usage

```bash
# Audit a skill
./scripts/skill-auditor.py /path/to/skill/directory

# Example
./scripts/skill-auditor.py plugins/meta/meta-claude/skills/skill-factory
```

## What It Checks

### Blockers (Must Fix)
- **B1:** No forbidden files (README.md, CHANGELOG.md, etc.)
- **B2:** Valid YAML frontmatter (delimiters, name, description)
- **B3:** SKILL.md under 500 lines
- **B4:** No implementation details in description (.py files, /commands, etc.)

### Warnings (Should Fix)
- **W1:** ≥3 quoted trigger phrases in description
- **W3:** ≥3 domain-specific indicators

## Module Structure

```bash
scripts/
├── skill-auditor.py              # Main SDK application
└── skill_auditor/
    ├── metrics_extractor.py      # Deterministic Python extraction
    └── test_metrics_extractor.py # Tests for extraction logic
```

## Development

Run tests:
```bash
uv run scripts/skill_auditor/test_metrics_extractor.py
```

## Design Decisions

**Why query() not ClaudeSDKClient?**
- Skill auditing is one-shot analysis (not multi-turn conversation)
- No need for conversation memory
- Simpler code with query()

**Why no tools for Claude?**
- Prevents hallucinated bash command outputs
- Forces Claude to analyze only pre-extracted data
- Eliminates root cause of non-determinism

**Why Python extraction?**
- Python stdlib file I/O is deterministic
- Regex patterns are consistent across runs
- No agent interpretation of bash results
```text

### Step 2: Commit documentation

```bash
git add scripts/skill_auditor/README.md
git commit -m "docs(skill-auditor): add architecture and usage documentation"
```

---

## Task 7: Verification Testing

**Files:**
- Create: `scripts/test-skill-auditor-determinism.sh`

### Step 1: Create determinism test script

```bash
#!/bin/bash
# Test skill-auditor for deterministic output across multiple runs

set -e

SKILL_PATH="${1:-plugins/meta/meta-claude/skills/skill-factory}"
RUNS=3

echo "Testing skill-auditor determinism with $RUNS runs on: $SKILL_PATH"
echo "="

 60

# Run auditor multiple times and capture key outputs
for i in $(seq 1 $RUNS); do
    echo "Run $i..."
    ./scripts/skill-auditor.py "$SKILL_PATH" > "/tmp/audit-run-$i.txt" 2>&1

    # Extract status line
    grep "Status:" "/tmp/audit-run-$i.txt" || echo "No status found"

    # Extract metric counts
    grep "Quoted phrases:" "/tmp/audit-run-$i.txt" || echo "No quoted phrases count"
    grep "Domain indicators:" "/tmp/audit-run-$i.txt" || echo "No domain indicators count"
done

echo ""
echo "Comparing runs for consistency..."

# Compare run outputs
if diff -q /tmp/audit-run-1.txt /tmp/audit-run-2.txt && \
   diff -q /tmp/audit-run-2.txt /tmp/audit-run-3.txt; then
    echo "✅ PASS: All runs produced identical output (deterministic)"
    exit 0
else
    echo "❌ FAIL: Runs produced different output (non-deterministic)"
    echo ""
    echo "Differences:"
    diff /tmp/audit-run-1.txt /tmp/audit-run-2.txt || true
    exit 1
fi
```

### Step 2: Make test script executable

```bash
chmod +x scripts/test-skill-auditor-determinism.sh
```

### Step 3: Run determinism test

```bash
./scripts/test-skill-auditor-determinism.sh
```

Expected: ✅ PASS - All runs identical

### Step 4: Commit verification test

```bash
git add scripts/test-skill-auditor-determinism.sh
git commit -m "test(skill-auditor): add determinism verification test"
```

---

## Success Criteria

✅ Python extracts all metrics deterministically (no bash)
✅ Claude analyzes pre-extracted metrics (no tool access)
✅ Same skill produces same metrics across runs
✅ Same metrics produce same analysis across runs
✅ No hallucinated bash outputs
✅ Convergent feedback (no contradictory advice)
✅ Tests pass for extraction logic
✅ Determinism test passes

## References

- **@claude-agent-sdk** - SDK patterns and best practices
- `examples/quick_start.py` - query() usage pattern
- `assets/sdk-template.py` - uv script headers
- `references/best-practices.md` - SDK anti-patterns
