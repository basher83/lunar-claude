# Skill Auditor SDK Application

Deterministic skill auditing using Claude Agent SDK.

## Architecture

**Problem Solved:** Previous skill-auditor agents had non-deterministic bash command
execution, causing agents to hallucinate different metric counts across runs. This
led to feedback loops where fixing issues flagged in one run would be contradicted
by the next run.

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

### Pattern Enhancement (v2 - Nov 20, 2025)

**Expanded B4 Detection:**

The SDK now detects implementation details including:

1. **File Extensions** (14 types)
   - Python, JavaScript, TypeScript, JSON, YAML, SQL, etc.

2. **Architecture Patterns**
   - multi-tier, 8-phase, three-stage, n-layer, etc.
   - Detects: `\w+-(?:tier|layer|phase|step|stage)`

3. **Tool/Library Names** (40+ common tools)
   - Web: firecrawl, scrapy, beautifulsoup, playwright
   - Data: pandas, numpy, tensorflow, scikit-learn
   - Infra: docker, kubernetes, postgresql, redis
   - Frontend: react, vue, angular, next.js

4. **Command Paths**
   - /commands:name, /agents:type

**Validation Results:**

Tested on skill-factory (Nov 20, 2025):

- Detected: 3/3 violations (firecrawl, multi-tier, 8-phase)
- Before enhancement: 0/3
- Improvement: 100%
- Determinism: 0pp variance across 5 runs
- Performance: <100ms per skill

## Module Structure

```bash
scripts/
├── skill-auditor.py              # Main SDK application (entry point)
└── skill_auditor/
    ├── metrics_extractor.py      # Deterministic metric extraction (Python regex/file I/O)
    ├── validation.py             # Metrics structure validation (ensures all required keys present)
    ├── test_metrics_extractor.py # Unit tests for extraction logic (21 tests)
    ├── test_skill_auditor.py     # Unit tests for main app logic (12 tests - blocker/warning calculations)
    └── test_determinism.py       # Integration tests for determinism (2 tests - verifies convergent behavior)
```

## Development

### Running Tests

All tests (35 total):

```bash
uv run scripts/skill_auditor/test_metrics_extractor.py  # 21 extraction tests
uv run scripts/skill_auditor/test_skill_auditor.py      # 12 application logic tests
uv run scripts/skill_auditor/test_determinism.py        # 2 determinism integration tests
```

Quick verification (all tests):

```bash
uv run scripts/skill_auditor/test_*.py
```

### Module Details

**metrics_extractor.py:**

- Extracts all audit metrics using deterministic Python
- 15 metrics: skill_name, description, quoted phrases, domain indicators,
  forbidden files, line count, YAML validation, etc.
- No bash commands - pure Python stdlib operations

**validation.py:**

- Validates metrics dictionary has all 14 required keys
- Prevents KeyError exceptions in main application
- Provides clear error messages identifying missing fields

**test_metrics_extractor.py:**

- 21 unit tests covering extraction edge cases
- Tests: YAML parsing, quoted phrase extraction, domain indicators, forbidden files, error handling
- Includes permission error and encoding error tests

**test_skill_auditor.py:**

- 12 unit tests for blocker/warning calculation logic
- Tests B1-B4 (blockers) and W1, W3 (warnings)
- Verifies PASS/FAIL status strings in analysis prompt

**test_determinism.py:**

- 2 integration tests verifying deterministic behavior
- Runs extraction 5 times, ensures identical results
- Validates core requirement: same inputs → same outputs

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
