# Research Pipeline v2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the `/lunar-research` multi-agent research pipeline with 4 specialized researchers and knowledge base caching.

**Architecture:** Slash command orchestrates parallel sub-agents, each using dedicated MCP tools. Reports cached to knowledge base. Synthesis provides contextual integration advice.

**Tech Stack:** Claude Code sub-agents, MCP servers (GitHub, Tavily, DeepWiki, Exa), JSON cache

**Design Document:** `docs/plans/2025-12-01-research-pipeline-v2-design.md`

**Commit Strategy:** Commit at the end of each phase, not after each task.

---

## Phase 0: Setup

### Task 1: Create Directory Structure

**Step 1: Create all directories**

```bash
mkdir -p .claude/schemas .claude/agents/research .claude/research-cache .claude/scripts
```

**Step 2: Add to .gitignore**

Add these lines to `.gitignore`:

```text
# Research cache entries (but keep index)
.claude/research-cache/*/
!.claude/research-cache/index.json
```

**Step 3: Create empty index file**

```json
{
  "version": "1.0",
  "created": "2025-12-01T00:00:00Z",
  "entries": []
}
```

Write to `.claude/research-cache/index.json`

**Step 4: Commit**

```bash
git add .claude/ .gitignore
git commit -m "feat(research): initialize research pipeline directory structure"
```

---

## Phase 1: Foundation

### Task 2: Create Report Format Schema

**File:** `.claude/schemas/research-report.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "research-report.schema.json",
  "title": "Research Report",
  "description": "Standardized format for researcher sub-agent reports",
  "type": "object",
  "required": ["researcher", "query", "timestamp", "confidence", "completeness", "sources", "findings", "gaps", "summary", "tags"],
  "properties": {
    "researcher": {
      "type": "string",
      "enum": ["github", "tavily", "deepwiki", "exa"]
    },
    "query": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "completeness": { "type": "string", "enum": ["none", "partial", "comprehensive"] },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["url", "title", "type", "relevance"],
        "properties": {
          "url": { "type": "string", "format": "uri" },
          "title": { "type": "string" },
          "type": { "type": "string", "enum": ["repository", "article", "documentation", "discussion", "paper"] },
          "relevance": { "type": "string", "enum": ["high", "medium", "low"] },
          "metadata": { "type": "object" }
        }
      }
    },
    "findings": {
      "type": "object",
      "properties": {
        "implementations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "url", "approach"],
            "properties": {
              "name": { "type": "string" },
              "url": { "type": "string" },
              "approach": { "type": "string" },
              "maturity": { "type": "string", "enum": ["experimental", "beta", "production"] },
              "evidence": { "type": "string" }
            }
          }
        },
        "patterns": { "type": "array", "items": { "type": "string" } },
        "gotchas": { "type": "array", "items": { "type": "string" } },
        "alternatives": { "type": "array", "items": { "type": "string" } }
      }
    },
    "gaps": { "type": "array", "items": { "type": "string" } },
    "summary": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } }
  }
}
```

---

### Task 3: Create Researcher Agents

Create 4 researcher agents using this template. Only the frontmatter and specialization sections differ.

**Common Template Structure:**

```markdown
---
name: {researcher}-researcher
description: {description}
tools: {tools}
---

# {Name} Researcher

## Purpose

{Purpose description}

## Input

You will receive:
- **Query:** The research topic
- **Cache directory:** Where to write your report
- **Output file:** Your report filename

## Research Process

1. Search/explore using your specialized tools
2. Evaluate results for relevance and quality
3. Extract patterns, implementations, and gotchas
4. Write JSON report to the specified file

## Output Format

Write a JSON file matching `.claude/schemas/research-report.schema.json`

Set `"researcher": "{researcher}"` in your output.

## Quality Standards

{Quality standards specific to this researcher}
```

**Agent 1: `.claude/agents/research/github-agent.md`**

```yaml
name: github-researcher
description: Find repositories, implementations, and code patterns
tools: Read, Write, Edit, Grep, Glob, Bash
```

Specialization:
- Use `gh` CLI to search repositories
- Analyze README, code structure, issues
- Assess maturity (stars, activity, maintenance)

Quality Standards:
- Report ONLY what you found - do not fabricate sources
- Include direct URLs to everything referenced
- Confidence score reflects actual findings quality

**Agent 2: `.claude/agents/research/tavily-agent.md`**

```yaml
name: tavily-researcher
description: Find blog posts, tutorials, and community content
tools: mcp__tavily__search, mcp__tavily__extract, Read, Write, Edit
```

Specialization:
- Search for recent content (tutorials, guides, comparisons)
- Extract practical implementation guidance
- Identify community best practices

Quality Standards:
- Prefer recent content (last 1-2 years)
- Note when information might be outdated
- Include publication dates when available

**Agent 3: `.claude/agents/research/deepwiki-agent.md`**

```yaml
name: deepwiki-researcher
description: Find official documentation and project architecture
tools: mcp__deepwiki__read_wiki_structure, mcp__deepwiki__read_wiki_contents, mcp__deepwiki__ask_question, Read, Write, Edit
```

Specialization:
- Query official documentation via DeepWiki
- Extract architecture, API references, configuration
- Identify official best practices

Quality Standards:
- Report ONLY what official documentation says
- Include repo references for all documentation
- Official docs have highest authority

**Agent 4: `.claude/agents/research/exa-agent.md`**

```yaml
name: exa-researcher
description: Semantic search for conceptually related content
tools: mcp__exa__search, mcp__exa__find_similar, Read, Write, Edit
```

Specialization:
- Semantic/conceptual search for related approaches
- Find similar implementations and alternatives
- Discover technical papers and deep-dives

Quality Standards:
- Note when content is experimental vs proven
- Include similarity context when relevant
- Distinguish official from community content

---

### Task 4: Create Synthesizer Agent

**File:** `.claude/agents/research/synthesizer-agent.md`

**Frontmatter:**

```yaml
name: synthesizer-agent
description: Combines findings from all researcher reports into unified synthesis
tools: Read, Write, Edit
```

**Content sections:**

1. **Purpose:** Combine findings from all 4 researcher reports into unified synthesis
2. **Input:** Cache directory path + query; expects 4 report files (github, tavily, deepwiki, exa)
3. **Synthesis Process:**
   - Read all 4 reports
   - Identify consensus (findings in multiple sources)
   - Resolve conflicts: deepwiki > tavily > github > exa
   - Aggregate patterns, gotchas, alternatives
   - Calculate confidence based on agreement
   - Write `synthesis.md`
4. **Output Format:** `synthesis.md` with sections:
   - Executive Summary
   - Recommended Approach (best option, source, evidence)
   - Key Patterns (with source frequency)
   - Gotchas & Warnings (with sources)
   - Alternatives Considered (table)
   - All Sources (by relevance)
5. **Quality Standards:**
   - Read ALL 4 reports before synthesizing
   - Preserve source attribution
   - Higher confidence = more source agreement
   - Do not add information not in the reports

**Commit Phase 1:**

```bash
git add .claude/schemas/ .claude/agents/research/
git commit -m "feat(research): add report schema and 5 research agents"
```

---

## Phase 2: Orchestration

### Task 5: Create Slash Command

**File:** `.claude/commands/lunar-research.md`

**Frontmatter:**

```yaml
description: Research implementations, patterns, and best practices across multiple sources
allowed-tools: Task, Read, Write, Edit, Glob, Grep
argument-hint: [query]
```

**Content sections:**

1. **Header:** "# Lunar Research" - orchestrator for 3-tier research pipeline, COORDINATION ONLY

2. **Step 0: Check Knowledge Base**
   - Progress: "🔍 Checking knowledge base..."
   - Read index.json, check for matching entries < 30 days old
   - If found: ask user "Reuse, refresh, or new?"
   - If reuse: skip to Phase 3

3. **Phase 1: Dispatch Researchers**
   - Progress: "🚀 Dispatching 4 researcher agents..."
   - Normalize query to directory name
   - Create cache directory
   - Dispatch ALL 4 in SINGLE message with prompt: "Research: [query], Cache dir: [path], Output: [file]"
   - Agents: github → github-report.json, tavily → tavily-report.json, deepwiki → deepwiki-report.json, exa → exa-report.json
   - Progress after each: "✓ [agent] complete"

4. **Phase 2: Dispatch Synthesizer**
   - Progress: "🔄 Synthesizing findings..."
   - Dispatch synthesizer-agent with cache dir and query
   - Progress: "✓ Synthesis complete"

5. **Phase 3: Contextualize and Respond**
   - Progress: "🧠 Adding codebase context..."
   - Read synthesis.md
   - Check plugins/ for related patterns
   - Update index.json
   - Respond with synthesis + codebase integration suggestions

6. **Orchestration Rules:**
   - Dispatch agents, don't research yourself
   - Phase 1: ALL 4 in SINGLE message (parallel)
   - Phase 2: Synthesizer AFTER all complete
   - Phase 3: YOU add codebase context

---

### Task 6: End-to-End Test

**Test Query:**

```bash
/lunar-research "Python CLI best practices with Click"
```

**Verify:**

1. 4 Task tools called in parallel
2. Cache directory created with 4 reports + synthesis.md
3. index.json updated
4. Response includes synthesis + codebase context

**Commit Phase 2:**

```bash
git add .claude/commands/lunar-research.md
git commit -m "feat(research): add lunar-research orchestrator command"
```

---

## Phase 3: Validation

### Task 7: Create Validation Script

**File:** `.claude/scripts/validate_research_report.py`

```python
#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema"]
# ///
"""
Validate research reports against JSON schema.

Usage:
    ./validate_research_report.py <report.json>
    uv run validate_research_report.py <report.json>

Examples:
    ./validate_research_report.py .claude/research-cache/my-query/github-report.json
"""

import json
import sys
from pathlib import Path

from jsonschema import ValidationError, validate

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "research-report.schema.json"

def validate_report(report_path: str) -> bool:
    """Validate a research report against the schema."""
    report_file = Path(report_path)

    if not report_file.exists():
        print(f"ERROR: File not found: {report_path}")
        return False

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found: {SCHEMA_PATH}")
        return False

    try:
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
        with open(report_file, encoding="utf-8") as f:
            report = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return False

    try:
        validate(instance=report, schema=schema)
        print(f"✓ Valid: {report['researcher']} report")
        print(f"  Confidence: {report['confidence']}")
        print(f"  Sources: {len(report['sources'])}")
        print(f"  Tags: {report['tags']}")
        return True
    except ValidationError as e:
        print(f"ERROR: Schema validation failed: {e.message}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./validate_research_report.py <report.json>")
        sys.exit(1)

    success = validate_report(sys.argv[1])
    sys.exit(0 if success else 1)
```

**Commit Phase 3:**

```bash
git add .claude/scripts/validate_research_report.py
git commit -m "feat(research): add schema-based report validation"
```

---

## Verification Checklist

- [ ] Directory structure exists
- [ ] Schema file: `.claude/schemas/research-report.schema.json`
- [ ] 4 researcher agents in `.claude/agents/research/`
- [ ] Synthesizer agent: `.claude/agents/research/synthesizer-agent.md`
- [ ] Knowledge base index: `.claude/research-cache/index.json`
- [ ] Slash command: `.claude/commands/lunar-research.md`
- [ ] Validation script uses schema
- [ ] E2E test passes

---

## File Manifest

| Path | Purpose |
|------|---------|
| `.claude/schemas/research-report.schema.json` | Report format validation |
| `.claude/agents/research/github-agent.md` | GitHub researcher |
| `.claude/agents/research/tavily-agent.md` | Tavily researcher |
| `.claude/agents/research/deepwiki-agent.md` | DeepWiki researcher |
| `.claude/agents/research/exa-agent.md` | Exa researcher |
| `.claude/agents/research/synthesizer-agent.md` | Report synthesizer |
| `.claude/research-cache/index.json` | Knowledge base index |
| `.claude/commands/lunar-research.md` | Orchestration slash command |
| `.claude/scripts/validate_research_report.py` | Schema-based validation |
