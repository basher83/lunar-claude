#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.8",
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
