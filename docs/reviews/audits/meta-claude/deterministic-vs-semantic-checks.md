# Deterministic vs Semantic Checks

## The Fundamental Challenge

Skill auditing requires both **mechanical verification** (syntax, structure) and **semantic analysis** (meaning, intent). The goal is to maximize determinism while acknowledging that some checks fundamentally require interpretation.

## Architecture Split

```text
┌─────────────────────────────────────────────────────┐
│  DETERMINISTIC (Python Script)                      │
├─────────────────────────────────────────────────────┤
│ ✅ B1: File existence (forbidden files)             │
│ ✅ B2: YAML structure (delimiters, fields)          │
│ ✅ B3: Line count (mechanical threshold)            │
│ ✅ B6: Backslash detection (character matching)     │
│ ✅ B7: Reserved words (exact string match)          │
│ ✅ W1: Quoted phrase count (regex count)            │
│ ✅ W3: Domain indicator count (pattern matching)    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  SEMANTIC (Agent Must Analyze)                      │
├─────────────────────────────────────────────────────┤
│ ⚠️ B4: Implementation details (WHAT vs HOW)         │
│ ⚠️ B5: Content duplication (meaning comparison)     │
│ ⚠️ W2: Quote specificity (quality assessment)       │
│ ⚠️ W4: Decision guide (existence vs usefulness)     │
└─────────────────────────────────────────────────────┘
```

## Why This Split Matters

**Deterministic checks:**
- Always produce identical results
- No interpretation required
- Scriptable via regex, file operations, counting

**Semantic checks:**
- Require understanding context and intent
- Cannot be reduced to pattern matching
- Need LLM analysis or human judgment

**Example: B4 Implementation Details**

```yaml
# Violation - reveals WHICH tool
"firecrawl-powered research"

# Valid - describes WHAT capability
"automated research"
```

Both describe research. The difference is **semantic intent**, not syntactic pattern. A regex list of forbidden tools is "writing tests to pass tests" - it doesn't solve the root problem.

## Implications for Hybrid Architecture

**Python Script:**
- Extracts all mechanical metrics
- Flags semantic checks as "AGENT REVIEW REQUIRED"
- Never claims PASS/FAIL on semantic checks

**v6 Agent:**
- Trusts script's deterministic results
- Performs semantic analysis on flagged checks
- Provides evidence-based reports

## Trade-offs

We **cannot eliminate** semantic checks - the task itself requires them. But we **can isolate** them so users know:
- Which results are deterministic (always consistent)
- Which results are contextual (require interpretation)
- What evidence supports each finding

This is the balancing act from v1-v6: maximizing determinism while accepting that some aspects fundamentally require semantic understanding.
