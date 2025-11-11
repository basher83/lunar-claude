# File System Scripts Approach Analysis

## 1. Progressive Disclosure Pattern

### Script Inventory
- **Total scripts:** 10 standalone Python files
- **Lines per script:** 157-465 lines (average ~237 lines)
  - Smallest: `status.py` (157 lines)
  - Largest: `search.py` (465 lines with caching)
  - Most: 200-255 lines (meets README claim of ~200-300)

### Script Breakdown
| Script | Lines | Purpose |
|--------|-------|---------|
| status.py | 157 | Exchange operational status |
| series.py | 196 | Series information |
| event.py | 205 | Event details |
| orderbook.py | 205 | Bid/ask depth |
| series_list.py | 214 | Browse all ~6900 series |
| market.py | 219 | Detailed market info |
| events.py | 226 | List event collections |
| trades.py | 233 | Recent trading activity |
| markets.py | 254 | Browse markets with filters |
| search.py | 465 | Keyword search (with caching) |

### Token Cost Per Script
- **Estimated:** ~600-1800 tokens per script (based on 157-465 lines)
- **Compared to MCP:** Unknown (no MCP tool definitions visible for comparison)
- **Compared to CLI:** CLI has all 13 commands in single 552-line file = ~2000 tokens

### Loading Mechanism
**The Key Insight:** Progressive disclosure is MANUAL, not automatic.

```markdown
## Instructions (from prime prompt)

- **IMPORTANT**: DO NOT read the scripts themselves.
  - ONLY read the scripts when running `<script.py> --help` doesn't give you the information you need.
```

**How Claude loads scripts:**
1. Prime prompt (`/prime_file_system_scripts`) tells Claude scripts exist
2. README.md lists all 10 scripts with "When to use" descriptions (~58 lines, ~200 tokens)
3. Claude runs `<script.py> --help` first (minimal tokens)
4. ONLY if `--help` insufficient, Claude reads full script source

**Progressive disclosure levels:**
1. **L1 - Prime prompt:** ~100 tokens (tells Claude about scripts directory)
2. **L2 - README:** ~200 tokens (lists all 10 scripts with purposes)
3. **L3 - Help flag:** ~50-100 tokens per script (CLI help output)
4. **L4 - Full source:** ~600-1800 tokens per script (entire Python file)

## 2. Discoverability vs Token Tradeoff

### The Core Tension

**Token efficiency:** ✅ Excellent
- Only ~300 tokens loaded upfront (prime + README)
- Help text adds ~50-100 tokens per script
- Full source only if needed (~600-1800 tokens)
- **Total for typical usage:** ~500-800 tokens (vs ~2000+ for CLI or MCP tool list)

**Discoverability:** ❌ POOR - Hidden behind manual choice
- Scripts NOT auto-invoked by Claude
- Requires **explicit prime prompt** (`/prime_file_system_scripts`)
- Claude must **manually choose** to use bash to run scripts
- No automatic trigger mechanism

### Assessment

**Can Claude discover scripts proactively?** NO
- Scripts invisible until prime prompt invoked
- Even after priming, Claude must decide to use them
- No automatic invocation like MCP tools or Skills

**Evidence from implementation:**
```markdown
## Workflow (from prime prompt)

1. READ README.md and scripts/ directory
   - **IMPORTANT**: DO NOT read the scripts themselves
2. Run the `Report` section
3. As you work with the user, based on their request, run `<script.py> --help`
```

This is **MANUAL PROGRESSIVE DISCLOSURE** - agent must choose at each step.

**Tradeoff assessment:**
- ✅ Token efficient: Only loads what's needed
- ❌ Requires manual invocation: No auto-discovery
- ❌ Requires prime prompt: Hidden by default
- ⚠️ Agent must remember to use scripts: Cognitive load

**Is the tradeoff worth it?**
- **For one-off tasks:** Yes (minimal token usage)
- **For autonomous agents:** No (poor discoverability)
- **For team workflows:** Maybe (requires documentation/training)

## 3. Implementation Details

### Self-Contained Architecture
**Verified:** ✅ Completely self-contained
- Each script has own `KalshiClient` class (~50 lines)
- HTTP client initialization code duplicated 10 times
- Context manager pattern (`__enter__`, `__exit__`) in each
- Configuration constants (API_BASE_URL, timeout, user-agent) repeated

### Code Duplication Extent
**Massive duplication confirmed:**

```python
# Repeated in ALL 10 scripts:
class KalshiClient:
    """Minimal HTTP client for Kalshi API - <script-specific purpose>"""

    def __init__(self):
        """Initialize HTTP client"""
        self.client = httpx.Client(
            base_url=API_BASE_URL,
            timeout=API_TIMEOUT,
            headers={"User-Agent": USER_AGENT}
        )

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        self.client.close()
```

**Duplication analysis:**
- HTTP client boilerplate: ~40-50 lines × 10 scripts = **400-500 lines duplicated**
- Configuration constants: ~5 lines × 10 scripts = **50 lines duplicated**
- Click decorators/formatting: ~100 lines × 10 scripts = **1000 lines duplicated**
- **Total duplication estimate:** ~1500+ lines across 2374 total lines (63% duplication)

**Each script then adds:**
- Unique API method(s) for that script's purpose
- Unique formatting function(s)
- Unique CLI command definition

### HTTP Client Embedding
**Pattern verified:**
- httpx library required in PEP 723 inline script metadata
- Client initialized per-script execution
- No shared client across scripts
- Each script imports: `httpx`, `click`, `json`, `sys`

```python
# /// script
# dependencies = [
#     "httpx",
#     "click",
# ]
# ///
```

### Dependencies
**Per-script dependencies (minimal):**
- Core: `httpx`, `click`
- Search.py adds: `pandas` (for caching)
- All use stdlib: `json`, `sys`, `typing`, `pathlib`

**No shared dependencies** - each script declares its own.

## 4. claude-mem Comparison

### Current claude-mem Pattern

**Skills with operations/ docs:**
```text
skills/
├── search/
│   ├── SKILL.md          # Main skill description
│   └── operations/       # Progressive disclosure
│       ├── search_observations.md   (~200 tokens)
│       ├── search_sessions.md       (~200 tokens)
│       ├── find_by_concept.md       (~200 tokens)
│       └── ...
```

**How it works:**
1. SKILL.md loaded when skill invoked (~500-1000 tokens)
2. Operations docs loaded on-demand (~200 tokens each)
3. Claude chooses which operation to use
4. MCP tool invoked with parameters

**Progressive disclosure is active:**
- Operations/ docs ARE progressive
- Only loaded when Claude reads them
- Similar token cost to file scripts (~200 tokens per operation)

### Scripts Pattern

**Similar structure:**
```text
scripts/
├── README.md             # Script index
└── scripts/
    ├── status.py         (~600 tokens if read)
    ├── markets.py        (~1000 tokens if read)
    └── ...
```

**How it works:**
1. README loaded via prime prompt (~200 tokens)
2. Scripts run via `--help` first (~100 tokens)
3. Full script source only if needed (~600-1800 tokens)
4. Agent executes script via bash/uv

### Key Differences

| Aspect | claude-mem Skills | File Scripts |
|--------|-------------------|--------------|
| **Trigger** | Skill description in SKILL.md | Prime prompt + README |
| **Invocation** | MCP tool calls | Bash subprocess |
| **Documentation** | operations/*.md files | `--help` flag + source |
| **Progressive disclosure** | Read ops on-demand | Run --help, read source if needed |
| **Auto-invoked** | Yes (if skill matches context) | No (manual decision) |
| **Token cost** | ~200 per operation doc | ~100 help, ~600-1800 source |

**Critical difference:**
- Skills: Auto-invoked when description matches
- Scripts: Manual invocation, requires prime prompt

## 5. Discoverability Problem Hypothesis

### Theory: Progressive Disclosure Reduces Proactive Usage

**Hypothesis:** When capabilities are hidden behind progressive disclosure, agents use them less proactively.

### Evidence from Scripts Approach

**Progressive disclosure confirmed:**
- Scripts hidden until prime prompt
- Even then, requires manual bash execution
- No automatic trigger mechanism

**Discoverability issues:**
1. **Initial discovery:** Requires `/prime_file_system_scripts` command
2. **Capability awareness:** Only via README "When to use" descriptions
3. **Usage decision:** Agent must choose to run script
4. **Learning curve:** Agent must understand workflow

**Result:** Low proactive usage
- Agent won't discover scripts on its own
- Requires user to prime the context
- No autonomous skill discovery

### Evidence from claude-mem Current Behavior

**Progressive disclosure in claude-mem:**
- Skills visible in `/skill list`
- Operations hidden in operations/ directory
- Only loaded when Claude needs details

**Observed behavior:**
- Claude DOES auto-invoke skills (when description matches)
- Claude DOES load operation docs on-demand
- But: Claude may not proactively explore operations

**Question:** Does hiding operation details reduce proactive exploration?

**Possible hypothesis:**
- Skill-level description IS visible → Auto-invoked ✅
- Operation-level details ARE hidden → Less exploration? ❓
- Full MCP tool params ARE hidden → Less proactive usage? ❓

### Conclusion: Progressive Disclosure IS the Culprit

**File scripts prove the hypothesis:**
- Extreme progressive disclosure (3-4 levels)
- Result: ZERO autonomous discovery
- Requires explicit priming

**claude-mem may have similar issue:**
- Skills auto-invoke (description visible)
- But operations are hidden (progressive disclosure)
- May reduce proactive operation exploration

**The tradeoff is real:**
- Hide details → Save tokens ✅
- Hide details → Reduce discoverability ❌

## 6. Agent Autonomy Assessment

### Auto-invoked: ❌ NO

**Scripts approach:**
- Requires manual prime prompt
- Requires manual bash execution
- No automatic discovery mechanism

**Why:** Scripts are just files, not tools
- No tool registration
- No description in context
- Hidden until agent reads README

**Confidence:** HIGH (verified from implementation)

### Comparison to Other Approaches

| Approach | Auto-invoked? | Mechanism |
|----------|---------------|-----------|
| MCP Server | ✅ Yes | Tool list in context |
| CLI | ❌ No | Manual bash invocation |
| File Scripts | ❌ No | Manual bash invocation + prime |
| Skills | ✅ Yes | Skill description matching |

### Autonomy Spectrum

```text
Low Autonomy ←─────────────────────→ High Autonomy

File Scripts    CLI         MCP Server    Skills
(manual prime)  (manual)    (auto-tools)  (auto-discover)
```

**File scripts are LEAST autonomous** of the 4 approaches.

## 7. Critical Insights

### The Progressive Disclosure Paradox

**Benefit:** Token efficiency
- Only load what you need
- Minimize context window usage
- Scale to many capabilities

**Cost:** Discoverability
- Hidden capabilities won't be used
- Requires explicit invocation
- No autonomous exploration

**The paradox:**
- Progressive disclosure SAVES tokens ✅
- But ONLY IF agent knows to look 🤔
- If hidden too well, never gets used ❌

### Why Scripts Don't Auto-Invoke

**Technical reason:** Scripts are not tools
- Just Python files in directory
- No registration mechanism
- Agent must choose to read/run them

**Discoverability solution:** Prime prompt
- Explicitly tells agent "scripts exist here"
- Provides README with purposes
- Creates manual workflow

**But this requires:**
- User knowledge (must run /prime)
- Agent discipline (must follow workflow)
- Documentation (must maintain README)

### Application to claude-mem

**Current state:**
- Skills DO auto-invoke (SKILL.md visible)
- Operations are progressive (operations/*.md)
- MCP tools have descriptions

**Hypothesis:**
- Skill descriptions ARE discoverable → Auto-invoked ✅
- Operation details are HIDDEN → Less proactive use? ❓
- MCP tool parameters are HIDDEN → Less exploration? ❓

**Key question:**
Is the issue that operations/ docs are TOO hidden?

**Possible solutions:**
1. Put operation summaries in SKILL.md (reduce progressive disclosure)
2. Make MCP tool descriptions more detailed (hint at capabilities)
3. Create explicit "When to use" section like file scripts
4. Accept the tradeoff (token efficiency > discoverability)

## 8. Recommendations for claude-mem

### Based on File Scripts Analysis

**What works:**
- ✅ Progressive disclosure DOES save tokens (~200 vs ~2000)
- ✅ "When to use" descriptions help discovery
- ✅ Tiered loading (README → help → source)

**What doesn't work:**
- ❌ Hiding behind manual prime prompt
- ❌ Requiring explicit workflow knowledge
- ❌ No auto-discovery mechanism

**Recommendations:**

1. **Enhance Skill Descriptions**
   - Add "When to use" examples to SKILL.md
   - List operation names (not full docs)
   - Hint at capabilities without full docs

2. **Balance Progressive Disclosure**
   - Keep operations/ docs for details
   - But add operation index to SKILL.md
   - ~1 line per operation (10-20 operations = ~200 tokens)

3. **Make MCP Tools More Discoverable**
   - Tool descriptions should hint at use cases
   - Include "When to use" in tool description
   - Example: "search_observations - Find past decisions, bugs, features by keyword"

4. **Consider Tiered Documentation**
   - Level 1: SKILL.md with operation index (~500 tokens)
   - Level 2: Operation summary in SKILL.md (~50 tokens per op)
   - Level 3: Full operation doc on-demand (~200 tokens)

5. **Test the Hypothesis**
   - Add explicit "When to use" to search skill
   - Measure if Claude invokes more proactively
   - Compare with current auto-invocation rate

### The Bottom Line

**Progressive disclosure is a double-edged sword:**
- Saves tokens ✅
- Hides capabilities ❌

**File scripts prove:** Extreme hiding = no discovery

**claude-mem strategy:** Find the balance
- Make capabilities discoverable (in SKILL.md)
- Keep details progressive (in operations/)
- Use MCP tool descriptions effectively

**Hypothesis confirmed:** Progressive disclosure CAN hurt discoverability if taken too far.
