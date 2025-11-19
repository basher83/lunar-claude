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
