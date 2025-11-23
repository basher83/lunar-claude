# skill-auditor Determinism: Root Cause Analysis

**Date:** 2025-01-19
**Issue:** Audit agents produce inconsistent effectiveness scores (40-100% variance) across parallel runs on identical skills
**Status:** Unresolved after v3 and v4 attempts

---

## Test Results Summary

### Original skill-auditor (v2)
- Variance: 50-100% effectiveness
- Critical detection: ✅ Consistent (all 3 runs found violations)
- Technical compliance: 77-89% (12pp variance)

### skill-auditor-v3 (added deterministic scoring section)
- Variance: 33-100% effectiveness (67pp - **worse**)
- Critical detection: ❌ Inconsistent (0-1 violations found)
- Result: **Made problem worse**

### skill-auditor-v4 (surgical fix, exact bash formulas)
- Variance: 40-100% effectiveness (60pp - **still worse**)
- Critical detection: ✅ Consistent
- Quoted phrase extraction: 0 vs 5 (completely inconsistent)
- Operation counts: 3 vs 5 vs 5 (same file, different counts)

---

## Root Cause

**Problem is NOT calculation logic - it's DATA EXTRACTION**

Agents running identical bash commands on the same file get different results:

```bash
# Same command, different outputs across runs:
grep -oP '"[^"]+"' <(grep -A 10 "^description:" SKILL.md)
# Run 1: 0 results
# Run 2: 5 results
# Run 3: 0 results
```

**Why:**
1. Bash process substitution (`<(...)`) may fail silently in agent environments
2. File reading timing issues (caching, stale reads)
3. Agent execution environments aren't fully isolated
4. grep/sed/awk commands have subtle environment dependencies

**Evidence:**
- Same regex, same file → different counts
- Adding explicit formulas didn't help
- More detailed instructions made it worse (not better)

---

## Failed Approaches

❌ **v3**: Added 112 lines of deterministic scoring methodology
- Made variance worse (33-100% vs 50-100%)
- Over-specified → agents confused

❌ **v4**: Exact bash commands + binary PASS/FAIL checks
- Still 60pp variance
- Bash extraction remains unreliable

---

## Recommendation: Hybrid Approach

**Separate extraction from analysis**

### Architecture:
```text
Python Script (deterministic)     Agent (intelligent)
─────────────────────────        ─────────────────────
1. Read SKILL.md with stdlib     3. Read metrics.json
2. Extract all metrics           4. Apply thresholds
   → Output JSON                 5. Categorize issues
                                 6. Generate report
```

### Implementation:
```bash
# Step 1: Extract metrics (deterministic)
python scripts/extract_skill_metrics.py plugins/meta/meta-claude/skills/skill-factory
# → Creates skill-factory.metrics.json

# Step 2: Agent reads JSON (same data every run)
agent-skill-auditor-v5 skill-factory.metrics.json
```

### Benefits:
- ✅ **100% deterministic metrics** (Python stdlib file I/O is consistent)
- ✅ **Keeps agent intelligence** (analysis, recommendations, reporting)
- ✅ **Debuggable** (inspect JSON to see what agents received)
- ✅ **Fast** (preprocessing once, multiple agent runs on same data)

---

## Alternative: Accept Variance

If hybrid approach too complex:

1. Keep critical issue detection (already consistent)
2. Remove effectiveness percentage from reports
3. Make effectiveness qualitative: "STRONG triggers, EXCELLENT visibility"
4. Document variance in reports: "Effectiveness metrics may vary ±30%"

---

## Next Steps

**Recommended:** Implement hybrid approach
1. Create `scripts/extract_skill_metrics.py`
2. Define JSON schema for metrics
3. Create skill-auditor-v5 that consumes JSON
4. Test: 3 parallel runs → expect 0% variance

**Timeline:** 2-3 hours implementation + testing

**Success Criteria:**
- 3 parallel audit runs produce identical effectiveness scores
- Critical issue detection remains consistent
- Agent can still provide intelligent analysis and recommendations
