# B4 Pattern Gap Analysis

**Finding:** SDK's B4 check has incomplete pattern coverage, causing false negatives.

---

## Current SDK Pattern (Line 78 of metrics_extractor.py)

```python
impl_pattern = r"\w+\.(py|sh|js|md|json)|/[a-z-]+:[a-z-]+"
```

**What it catches:**
- ✅ File extensions: `something.py`, `script.sh`, `config.json`
- ✅ Command paths: `/commands:something`, `/agents:something`

**What it misses:**
- ❌ Tool names: `firecrawl`, `pdfplumber`, `pandas`, `react`
- ❌ Architecture terms: `multi-tier`, `8-phase`, `three-layer`
- ❌ Technology stacks: `PostgreSQL`, `Redis`, `Docker`
- ❌ Framework names: `Django`, `FastAPI`, `Next.js`
- ❌ System components: `PM2-managed`, `systemd-controlled`

---

## Test Case: skill-factory Description

**Description text:**
```text
Research-backed skill creation workflow with automated firecrawl research
gathering, multi-tier validation, and comprehensive auditing...
```

**Violations present:**
1. "firecrawl" - tool name (implementation detail)
2. "multi-tier" - architecture term (implementation detail)
3. "8-phase" (later in description) - process detail (implementation detail)

**SDK B4 result:** `implementation_details: []` ❌ **MISS**

**Why missed:** None of these match the pattern `\w+\.(py|sh|js|md|json)|/[a-z-]+:[a-z-]+`

---

## v1 Agent vs SDK

### How v1 Caught It

**v1 uses semantic analysis:**
- Reads description
- Understands "what is WHAT vs HOW"
- Identifies tools, architecture, processes as implementation details
- **Does NOT use fixed patterns**

**Example from v1 output (from test results):**
```bash
Critical Issue: Progressive Disclosure Violation
- Location: SKILL.md:3-9 (description field)
- Violation: Implementation details in Level 1 metadata
- Evidence: "firecrawl" (2×), "multi-tier", "8-phase"
- Fix: Remove tool names and architecture patterns
```

### How SDK Missed It

**SDK uses regex patterns:**
- Checks for literal string matches
- Pattern doesn't include "firecrawl", "multi-tier", "8-phase"
- **Cannot understand semantic meaning**

**Trade-off:**
- ✅ Deterministic (same pattern = same result every time)
- ❌ Limited to known patterns (can't reason about unknowns)

---

## The Pattern Coverage Problem

### Can't Enumerate All Possible Tool Names

**There are thousands of tools:**
- Python: pandas, numpy, scikit-learn, tensorflow, pytorch, flask, django, fastapi, streamlit...
- JavaScript: react, vue, angular, next.js, express, socket.io, webpack, vite...
- DevOps: docker, kubernetes, terraform, ansible, jenkins, github-actions, pm2...
- Databases: postgresql, mysql, mongodb, redis, elasticsearch, neo4j, cassandra...
- Cloud: aws, azure, gcp, cloudflare, vercel, netlify, heroku...
- APIs: stripe, twilio, sendgrid, mailchimp, jira, salesforce, hubspot...

**Maintaining an exhaustive list is impractical.**

### Can't Enumerate All Architecture Terms

**Architecture vocabulary is unbounded:**
- Tier patterns: "multi-tier", "three-tier", "n-tier"
- Layer patterns: "3-layer", "layered architecture"
- Phase patterns: "8-phase", "5-step", "multi-stage"
- Component patterns: "microservices", "monolithic", "serverless"
- Topology patterns: "hub-and-spoke", "mesh", "star"

**Every domain has its own architectural terminology.**

---

## Possible Solutions

### Solution 1: Comprehensive Pattern Library (Deterministic)

**Approach:** Build extensive pattern lists

**Pros:**
- ✅ Still deterministic
- ✅ Catches more violations over time

**Cons:**
- ❌ Never complete (new tools constantly released)
- ❌ High maintenance burden
- ❌ False positives (legitimate use of tool names in WHEN clauses)

**Example enhanced pattern:**
```python
# Tools (sample - would need 1000+)
tools = "firecrawl|pandas|react|docker|postgresql|redis|..."

# Architecture terms (sample)
architecture = "multi-tier|three-tier|n-tier|8-phase|5-step|microservices|..."

# Combined pattern
impl_pattern = f"({tools}|{architecture}|\w+\.(py|sh|js|md|json)|/[a-z-]+:[a-z-]+)"
```

**Problem:** Still brittle, still incomplete.

### Solution 2: Heuristic Patterns (Semi-Deterministic)

**Approach:** Use heuristic patterns that capture categories

**Example patterns:**
```python
# Technology names (usually TitleCase or lowercase single words)
r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b"  # TitleCase: PostgreSQL, FastAPI

# Hyphenated architecture terms
r"\b\w+-(?:tier|layer|phase|step|stage)\b"  # multi-tier, 8-phase

# Process managers
r"\b\w+-managed\b"  # PM2-managed, systemd-managed
```

**Pros:**
- ✅ Catches categories, not just specific terms
- ✅ More maintainable than exhaustive lists

**Cons:**
- ⚠️ Less deterministic (heuristics can have edge cases)
- ⚠️ False positives (legitimate domain terms)

### Solution 3: Hybrid Deterministic + Semantic (v6 Approach)

**Approach:** SDK runs deterministic checks, v6 agent adds semantic analysis

**Architecture:**
```text
1. SDK: Run deterministic patterns → Catch obvious violations
2. v6 Agent: Read description → Semantic analysis → Catch subtle violations
3. Report: Combined findings
```

**Pros:**
- ✅ SDK provides deterministic baseline
- ✅ Agent catches what patterns miss
- ✅ Agent can explain WHY something is a violation

**Cons:**
- ⚠️ Agent analysis may vary (not fully deterministic)
- ⚠️ More complex architecture

**Implementation:**
- SDK B4: Keep current pattern (catches .py, .sh, /commands:)
- v6 Agent: Add semantic B4 check after running SDK
- v6 reports BOTH SDK results AND agent findings

### Solution 4: LLM-as-Judge (Deterministic via Caching)

**Approach:** Use LLM with prompt caching for pattern detection

**Architecture:**
```python
# In metrics_extractor.py
def check_implementation_details(description: str) -> list[str]:
    """Use Claude to detect implementation details with prompt caching."""
    # Cached system prompt (99.9% cache hit rate)
    system = """You are an implementation detail detector.

    Return ONLY a JSON array of implementation details found in the description.
    Implementation details include: tool names, architecture terms, file extensions, etc.

    Examples:
    - "firecrawl" → ["firecrawl"]
    - "multi-tier system" → ["multi-tier"]
    - "8-phase workflow" → ["8-phase"]
    """

    response = claude_api(system, description)
    return json.loads(response)
```

**Pros:**
- ✅ Semantic understanding
- ✅ Near-deterministic with caching (same input → same cached response)
- ✅ No pattern maintenance

**Cons:**
- ❌ API dependency
- ❌ Not truly deterministic (model updates, cache misses)
- ❌ Latency

---

## Recommendation

**Immediate fix: Solution 2 (Heuristic Patterns)**

Add these patterns to `metrics_extractor.py`:

```python
# Enhanced B4 pattern
impl_patterns = [
    r"\w+\.(py|sh|js|md|json)",           # File extensions (current)
    r"/[a-z-]+:[a-z-]+",                   # Command paths (current)
    r"\b\w+-(?:tier|layer|phase|step|stage|managed)\b",  # Architecture terms
    r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b",    # TitleCase names (FastAPI, PostgreSQL)
]

impl_pattern = "|".join(impl_patterns)
implementation_details = re.findall(impl_pattern, description)
```

**This would catch:**
- ✅ "firecrawl" (no, wait - it's lowercase, not TitleCase)
- ✅ "multi-tier" (matches `\w+-tier`)
- ✅ "8-phase" (matches `\w+-phase`)
- ✅ "PM2-managed" (matches `\w+-managed`)

**Actually, "firecrawl" still wouldn't match.** We need:

```python
# Add lowercase tool names pattern (common single-word tools)
r"\b(?:firecrawl|pandas|numpy|redis|docker|kubernetes|terraform|ansible)\b"
```

**But this brings us back to the enumeration problem.**

---

## Long-term Solution: Hybrid (Solution 3)

**Accept that B4 has two types of checks:**

1. **Deterministic patterns (SDK):** Catch obvious violations
   - File extensions
   - Command paths
   - Common architecture patterns

2. **Semantic analysis (v6 Agent):** Catch subtle violations
   - Tool names not in pattern list
   - Architecture terms not in pattern list
   - Context-dependent violations

**v6 workflow:**
```text
1. Run SDK → Get B4=PASS (patterns only)
2. Agent reads description → Semantic B4 check
3. Agent finds "firecrawl", "multi-tier" → B4=FAIL
4. Report: "SDK missed implementation details, agent found 3 violations"
```

**This is CONVERGENT:**
- Same SDK patterns → Same SDK result (deterministic)
- Agent re-analyzes → May vary, but documents specific findings
- User gets BOTH deterministic baseline + comprehensive coverage

---

## Test Strategy for v6

**To test v6 properly (untainted):**

1. Create fresh skill with known B4 violation
2. In separate clean session, run v6 agent
3. NO context about what we're looking for
4. See if v6 catches it

**Or:**

1. Wait until conversation ends
2. In new session tomorrow, run: `@agent-meta-claude:skill:skill-auditor-v6 plugins/meta/meta-claude/skills/skill-factory`
3. Document findings

**Critical:** Follow CLAUDE.md protocol - path only, no taint.

---

## Key Insight

**The gap isn't deterministic vs semantic.**

**The gap is pattern coverage:**
- SDK has deterministic patterns but incomplete coverage
- v1 has semantic understanding but non-deterministic execution

**Best solution: Hybrid with explicit boundary:**
- SDK: Deterministic baseline (catches obvious)
- Agent: Semantic supplement (catches subtle)
- Both documented in report with evidence

This gives us:
- ✅ Deterministic baseline (SDK never varies)
- ✅ Comprehensive coverage (agent fills gaps)
- ✅ Convergent feedback (same SDK result + agent explains findings)
