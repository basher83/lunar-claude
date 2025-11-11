# File System Scripts Approach Analysis

## 1. Progressive Disclosure Pattern
- **Script count:** 10 scripts total
- **Lines per script:**
  - Smallest: 157 lines (status.py)
  - Average: ~237 lines (2374 total / 10 scripts)
  - Largest: 465 lines (search.py - includes caching logic)
  - Most scripts: 196-254 lines
- **Token cost per script:** ~400-1200 tokens estimated (based on code density)
- **Loading mechanism:**
  - Scripts are NOT auto-loaded into context
  - Claude must explicitly `Read` a script to see its contents
  - README lists script purposes (~58 lines, 10 script descriptions)
  - Agent reads README, decides which script(s) to inspect

## 2. Discoverability vs Token Tradeoff
**The Core Tension:**
- Low context load = token efficient ✅
- Hidden capabilities = low discoverability ❌

**Assessment:**
- Can Claude discover scripts proactively? **Partial**
- Evidence:
  - README provides high-level directory (58 lines)
  - Each script description is 1 line: "When to use: [purpose]"
  - But implementation details hidden until read
  - SKILL.md explicitly says: "Don't read scripts unless absolutely needed"
- Tradeoff worth it? **Depends on usage pattern**
  - If user explicitly asks for Kalshi data → works well
  - If agent should proactively suggest capabilities → fails
  - Progressive disclosure requires prior knowledge of existence

## 3. Implementation Details
- **Self-contained:** ✅ Verified - each script includes complete HTTP client
- **Code duplication:** ✅ Extensive
  - KalshiClient class repeated in EVERY script (30-70 lines each)
  - Same imports, configuration, error handling patterns
  - search.py duplicates client + cache logic (465 lines total)
  - Estimated ~40% code duplication across scripts
- **HTTP client:** Embedded httpx client in each script
  - Same base URL, timeout, user agent
  - Context manager pattern repeated
  - Error handling duplicated
- **Dependencies:** Minimal
  - httpx (HTTP client)
  - click (CLI interface)
  - pandas (search.py only - for caching)
  - Declared via PEP 723 inline metadata

## 4. claude-mem Comparison
**Current claude-mem pattern:**
- Skills with operations/ docs
- Progressive disclosure active
- Claude loads operations on-demand
- Example: version-bump skill
  - SKILL.md: 96 lines (always loaded)
  - operations/workflow.md: 228 lines (loaded when needed)
  - operations/scenarios.md: 218 lines (loaded when needed)
  - operations/reference.md: 275 lines (loaded when needed)
  - Total: 817 lines, but only ~96 loaded initially

**Scripts pattern:**
- Similar progressive disclosure
- Executable vs documentation
- Token cost comparison:
  - SKILL.md (96 lines) vs README.md (58 lines)
  - operations/*.md (721 lines) vs scripts/*.py (2374 lines)
  - But scripts include implementation, not just instructions

**Key difference:**
- claude-mem: Procedural knowledge (how to do something)
- Scripts: Executable code (does the thing directly)
- claude-mem: Agent follows instructions to achieve goal
- Scripts: Agent executes pre-built tool to achieve goal

## 5. Discoverability Problem Hypothesis
**Theory:** Progressive disclosure reduces proactive usage

**Evidence:**
- **From scripts approach:**
  - SKILL.md line 13: "Don't read scripts unless absolutely needed"
  - Implies: Reading scripts is costly, avoid if possible
  - Consequence: Agent won't know detailed capabilities without reading
  - 10 scripts × ~200 lines = 2000+ lines hidden by default

- **From claude-mem current behavior:**
  - version-bump skill exists with clear description
  - Operations docs exist (721 lines total)
  - Pattern: SKILL.md loaded, operations/* loaded on-demand
  - Same progressive disclosure as file system scripts
  - **Question:** Does Claude proactively offer version-bump help? Unknown without testing

**Conclusion:** **Progressive disclosure likely reduces proactive discovery**
- Agent knows scripts/docs EXIST (from README/SKILL.md)
- Agent knows WHEN to use them (from descriptions)
- Agent DOESN'T know detailed capabilities without reading
- Tradeoff: Save tokens vs expose capabilities
- For explicit requests: works great
- For proactive suggestions: fails

## 6. Agent Autonomy Assessment
**Auto-invoked:** ❌ No (for file system scripts standalone)

**Why:**
- Scripts are files in the filesystem
- No MCP protocol exposure
- No automatic tool registration
- Agent must:
  1. Know scripts exist (read README)
  2. Decide to use one (based on user request)
  3. Run via Bash tool (`uv run scripts/status.py`)
- Requires explicit agent decision chain

**However:** When wrapped in a Skill (approach #4):
- Auto-invoked: ✅ Partial
- Skill description triggers activation
- But still requires agent to decide WHICH script
- Still requires reading script for advanced usage
- Progressive disclosure still limits proactive suggestions

**Confidence:** High - based on clear evidence from README and implementation patterns
