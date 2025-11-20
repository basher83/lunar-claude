# Skill Auditor Agent Evolution Matrix

**Purpose:** Comparative analysis of all skill-auditor agent versions to understand architectural decisions and trade-offs.

## Agent Versions Overview

| Version | File | Purpose | Key Innovation | Status |
|---------|------|---------|----------------|--------|
| v1 | skill-auditor.md | Original comprehensive agent | Full semantic analysis | ⚠️ Non-deterministic |
| v3 | skill-auditor-v3.md | Added deterministic scoring | 112-line scoring methodology | ❌ Made variance worse |
| v4 | skill-auditor-v4.md | Surgical determinism fix | Exact bash formulas | ⚠️ Still non-deterministic |
| v5 | skill-auditor-v5.md | Convergent feedback architecture | Reads pre-extracted JSON | 🔍 Testing needed |
| v6 | skill-auditor-v6.md | Hybrid Python + Agent | Runs Python script first | ✅ Deterministic metrics |
| SDK | scripts/skill-auditor.py | Pure Python implementation | Claude SDK for analysis | ✅ Fully deterministic |

## The Core Problem

**Non-deterministic bash execution in agent environments:**
- Same grep command → different results across runs
- Process substitution (`<(...)`) fails silently
- File caching/timing issues
- Environment dependencies in bash tools

**Impact:**
- Effectiveness scores: 17-100% variance on same skill
- Contradictory feedback across runs
- Users stuck in fix/audit loops

## Evolution Timeline

### v1: Original skill-auditor (Pre-Nov 2025)
**Architecture:** Full-featured agent with bash commands for all checks
**Strengths:**
- ✅ Caught critical issues (e.g., "firecrawl" in skill-factory description)
- ✅ Comprehensive semantic analysis
**Weaknesses:**
- ❌ 50-100% variance in effectiveness scores
- ❌ Bash extraction unreliable

### v3: First Determinism Attempt (Nov 19, 2025)
**Innovation:** Added 112-line "Deterministic Scoring Methodology" section
**Theory:** More explicit instructions would reduce variance
**Result:** ❌ MADE IT WORSE (33-100% variance, up from 50-100%)
**Learning:** Over-specification confuses agents; problem is data extraction, not calculation

### v4: Surgical Fix (Nov 19, 2025)
**Innovation:** Exact bash command formulas with binary PASS/FAIL
**Theory:** Precise bash commands would be consistent
**Result:** ⚠️ Still 40-100% variance
**Learning:** Bash commands themselves are the problem, not how they're specified

### v5: JSON Pre-extraction (Nov 19, 2025)
**Innovation:** Convergent feedback architecture
**Architecture:**
```text
Python Script → metrics.json → Agent reads JSON → Report
```

**Theory:** Agent reads pre-computed metrics, can't re-extract
**Status:** 🔍 Unclear if implemented/tested
**Location:** plugins/meta/meta-claude/agents/skill/skill-auditor-v5.md

### v6: Hybrid Approach (Nov 19, 2025)
**Innovation:** Agent runs Python script, then reads files for evidence
**Architecture:**
```bash
Agent → Run skill-auditor.py → Get binary results → Read files for context → Report
```

**Strengths:**
- ✅ Deterministic binary checks (Python)
- ✅ Rich evidence collection (agent reads files)
- ✅ Cross-references official specs
**Status:** ✅ Current recommended approach

### SDK: Pure Python (Nov 19, 2025)
**Innovation:** Claude Agent SDK application with NO tools
**Architecture:**
```text
Python: Extract metrics → Claude: Analyze (no tools) → Output
```

**Strengths:**
- ✅ 100% deterministic (Python extraction)
- ✅ Simple, testable (35 unit tests)
- ✅ Fast (single-shot query)
**Weaknesses:**
- ⚠️ Limited to hardcoded checks (B1-B4, W1, W3)
- ⚠️ No file reading for evidence
- ⚠️ Less comprehensive than v1

**Location:** scripts/skill-auditor.py + scripts/skill_auditor/

## The Convergence Question

**User's Dilemma:**
- v1: ✅ Caught glaring errors | ❌ Non-deterministic
- v6/SDK: ✅ Deterministic | ❌ Missed glaring errors?

**Critical Test Case:**
skill-factory SKILL.md description contains "firecrawl" (implementation detail)
- v1: ✅ Caught this violation
- v6: ❓ Did it catch this?

**Test needed:** Run v6 on current skill-factory to verify it catches the "firecrawl" violation.

## Architectural Insights

### What Worked
1. **Python extraction** - 100% deterministic
2. **Binary checks** - PASS/FAIL reduces variance vs percentages
3. **Hybrid approach** - Combine deterministic metrics + semantic analysis

### What Failed
1. **More detailed instructions** - Made variance worse
2. **Exact bash formulas** - Still unreliable
3. **Percentage scoring** - Amplifies small variations

### What's Unclear
1. **Effectiveness validation in v6** - Does it still catch semantic violations?
2. **Coverage gaps** - Which checks are missing in SDK vs v1?
3. **Best convergence path** - v6 hybrid or SDK + enhancement?

## Key Documents Reference

- Architecture: `01-architecture-deterministic-vs-semantic.md`
- Root cause: `02-root-cause-analysis.md`
- Test results: `03-determinism-test-results.md`
- Git history: `07-git-history-timeline.txt`

---

**Next Steps for Analysis:**
1. Compare v1 checks vs v6/SDK checks (coverage matrix)
2. Test v6 on skill-factory (does it catch "firecrawl"?)
3. Identify semantic checks that can't be scripted
4. Design convergent solution that keeps v1's effectiveness + v6's determinism
