# PR #24 Review: Multi-Agent Research Pipeline

## PR Overview

| Field | Value |
|-------|-------|
| PR Number | #24 |
| Title | feat(research): add multi-agent research pipeline |
| Base Branch | main |
| Head Branch | claude/implement-research-pipeline-v2-01TmAAs7JtGc2kVpgBbNJYji |
| Files Changed | 10 |
| Commits | 4 |
| Additions | 787 |
| Deletions | 0 |

---

## Claims Verification

### Claims Extracted

**From PR Summary:**

1. Add `/lunar-research` command that orchestrates 4 parallel researcher agents
2. Create synthesizer agent with source authority hierarchy
3. Include knowledge base caching with 30-day TTL
4. Add JSON schema and validation script for report standardization

**From "What's Included":**

5. Directory structure: `.claude/schemas/`, `.claude/agents/research/`, `.claude/research-cache/`, `.claude/scripts/`
6. 4 researcher agents with MCP tool access
7. Synthesizer agent with authority hierarchy (deepwiki > tavily > github > exa)
8. Orchestrator command with cache check, parallel dispatch, and codebase context
9. Validation script using jsonschema

### Verification Results

| Claim | Source | Verified | Evidence |
|-------|--------|----------|----------|
| 4 researcher agents | PR body | ✅ | Files exist: `github-agent.md`, `tavily-agent.md`, `deepwiki-agent.md`, `exa-agent.md` |
| GitHub agent uses gh CLI | PR body | ✅ | tools: `Read, Write, Edit, Grep, Glob, Bash` - uses `gh search repos` |
| Tavily agent uses MCP | PR body | ✅ | tools: `mcp__tavily__search, mcp__tavily__extract` |
| DeepWiki agent uses MCP | PR body | ✅ | tools: `mcp__deepwiki__read_wiki_structure, mcp__deepwiki__read_wiki_contents, mcp__deepwiki__ask_question` |
| Exa agent uses MCP | PR body | ✅ | tools: `mcp__exa__search, mcp__exa__find_similar` |
| Synthesizer with authority hierarchy | PR body | ✅ | Documented: "deepwiki (official docs) > tavily (community) > github (code) > exa (semantic)" |
| `/lunar-research` orchestrator | PR body | ✅ | File exists: `.claude/commands/lunar-research.md` |
| Parallel dispatch (single message) | PR body | ✅ | Command states: "Dispatch ALL 4 researchers in a SINGLE message" |
| Cache check with 30-day TTL | PR body | ✅ | Step 0: "Check if any matching entry is less than 30 days old" |
| JSON schema for reports | PR body | ✅ | File exists: `.claude/schemas/research-report.schema.json` |
| Schema has required fields | PR body | ✅ | Required: researcher, query, timestamp, confidence, completeness, sources, findings, gaps, summary, tags |
| Validation script uses jsonschema | PR body | ✅ | Dependencies: `["jsonschema"]`, uses `from jsonschema import ValidationError, validate` |
| Knowledge base index | PR body | ✅ | `.claude/research-cache/index.json` with version, created, entries structure |
| Gitignore for cache management | Commit | ✅ | Cache entries ignored, but `index.json` tracked |

### Verification Summary

| Metric | Count |
|--------|-------|
| Total claims checked | 14 |
| Verified correct | 14 |
| Found incorrect | 0 |
| Critical mismatches | None |

---

## PR Comments Summary

### Comments Overview

| Source | Count | Type |
|--------|-------|------|
| CodeRabbit (automated) | 12 | Review comments |
| Owner (basher83) | 2 | Discussion + Issues |

---

## Critical Issues

### 1. Python Script Error Handling

**File:** `.claude/scripts/validate_research_report.py`

**Issue 1: Ambiguous JSON Error Source (lines 38-45)**

The try-catch loads both schema AND report files but catches `JSONDecodeError` with a single generic message. Users cannot determine which file failed to parse.

**Current:**

```python
try:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    with open(report_file, encoding="utf-8") as f:
        report = json.load(f)
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON: {e}")
    return False
```

**Fix:** Separate into distinct try-catch blocks with specific error messages:

```python
try:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
except json.JSONDecodeError as e:
    print(f"ERROR: Schema file contains invalid JSON: {SCHEMA_PATH}")
    print(f"  Parse error at line {e.lineno}, column {e.colno}: {e.msg}")
    return False

try:
    with open(report_file, encoding="utf-8") as f:
        report = json.load(f)
except json.JSONDecodeError as e:
    print(f"ERROR: Report file contains invalid JSON: {report_path}")
    print(f"  Parse error at line {e.lineno}, column {e.colno}: {e.msg}")
    return False
```

**Issue 2: Missing I/O Error Handling (lines 39-42)**

The `open()` and `json.load()` operations can raise `PermissionError`, `OSError`, and `UnicodeDecodeError` - none are caught. Users get Python tracebacks instead of helpful messages.

**Fix:** Add explicit I/O error handling for each file operation:

```python
except PermissionError:
    print(f"ERROR: Permission denied reading file")
    return False
except OSError as e:
    print(f"ERROR: Cannot read file: {e.strerror}")
    return False
except UnicodeDecodeError:
    print(f"ERROR: File is not valid UTF-8")
    return False
```

**Issue 3: Truncated Validation Error Details (lines 54-56)**

`ValidationError` contains rich diagnostic info but only `e.message` is printed. For nested failures like `findings.implementations[3].maturity`, users can't see WHERE the error occurred.

**Fix:**

```python
except ValidationError as e:
    print(f"ERROR: Schema validation failed")
    if e.absolute_path:
        path = ".".join(str(p) for p in e.absolute_path)
        print(f"  Location: {path}")
    print(f"  Error: {e.message}")
    return False
```

---

### 2. Orchestrator Error Handling

**File:** `.claude/commands/lunar-research.md` (lines 153-157)

**Current:**

```markdown
## Error Handling

- If a researcher fails, note it and continue with available reports
- If fewer than 2 reports available, warn user about limited findings
- If synthesis fails, provide raw reports to user
```

**Problem:** The phrase "note it" is ambiguous and could enable silent failures. The guidance is correct but lacks clarity on user communication.

**Fix:** Replace with conditional prose that Claude interprets naturally:

```markdown
## Error Handling

If a researcher agent fails:
  Tell the user which researcher failed and why
  Continue with remaining researchers

If fewer than 2 researchers succeed:
  Stop and tell the user how many researchers returned valid reports
  Ask if they want to continue with limited data or abort

If synthesis fails:
  Show the user the individual report summaries
  Provide key findings from available reports yourself
```

This follows slash command best practices: commands are instructions for Claude, not application code. Claude interprets conditional prose intelligently without needing message templates or interactive command syntax.

---

### 3. Should Be a Plugin, Not Direct Integration

**Files:** All files in `.claude/agents/research/`, `.claude/commands/`, `.claude/schemas/`, `.claude/scripts/`, `.claude/research-cache/`

The research pipeline is implemented directly in `.claude/` which is intended for project-level configuration. This creates several problems:

1. **Portability:** Cannot be installed in other projects without copying files
2. **Versioning:** No plugin.json manifest for version tracking
3. **Isolation:** Cache and schemas mixed with project config
4. **Path references:** Hardcoded `.claude/` paths throughout

**Fix:** Restructure as a plugin under `plugins/meta/research-pipeline/`:

```text
plugins/meta/research-pipeline/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── lunar-research.md
├── agents/
│   ├── github-agent.md
│   ├── tavily-agent.md
│   ├── deepwiki-agent.md
│   ├── exa-agent.md
│   └── synthesizer-agent.md
├── schemas/
│   └── research-report.schema.json
├── scripts/
│   └── validate_research_report.py
└── README.md
```

All path references must use `${CLAUDE_PLUGIN_ROOT}` instead of hardcoded `.claude/` paths:

- `${CLAUDE_PLUGIN_ROOT}/schemas/research-report.schema.json`
- `${CLAUDE_PLUGIN_ROOT}/agents/github-agent.md`

The cache directory should use a project-relative location like `.claude/research-cache/` (configurable) since cache is per-project, not per-plugin.

---

## Major Issues

### ~~1. Schema Missing Required Fields~~ (Not an Issue)

**File:** `.claude/schemas/research-report.schema.json`

**Original concern:** The `findings` object has no `required` properties, so `findings: {}` passes validation.

**Assessment:** This is intentional and correct. Different researchers find different things - a GitHub search might find implementations but no patterns, while Exa might find patterns but no implementations. Requiring all sub-fields would force researchers to output empty arrays for things they didn't find. The schema already requires `findings` at the top level; optional sub-fields provide appropriate flexibility.

### 2. Implementation URL Missing Format (Quick Fix)

The `url` field in implementations (line 41) uses plain `string` without `format: uri` validation, unlike `sources[].url` which correctly uses format validation. One-line fix for consistency.

### ~~3. Cache Reuse Flow Unclear~~ (Not an Issue)

**File:** `.claude/commands/lunar-research.md` (lines 21-27)

**Original concern:** No mechanism for capturing user input when presenting cache options.

**Assessment:** This is standard slash command behavior. Claude presents options as text, waits for user response, and acts on their choice. No special input capture syntax is needed - it's a prompt, not application code.

### ~~4. Agency Confusion in Command Spec~~ (Not an Issue)

**Original concern:** Lines 11, 149-151 use "You are a COORDINATOR" which blurs agency.

**Assessment:** This is correct slash command style. Commands are instructions TO Claude, so "You" directly addresses Claude and tells it what role to play. The command-development best practices explicitly state: "Write commands as directives TO Claude about what to do." Using third-person ("The coordinator dispatches...") would actually obscure that these are instructions for Claude.

---

## Minor Issues (Nitpicks from CodeRabbit)

| Agent/File | Issue | Recommendation |
|------------|-------|----------------|
| DeepWiki agent | No handling for unindexed repos | Add: "If DeepWiki returns 'repository not indexed' or similar, fail fast with confidence 0.0 and note the gap. Do not retry with alternate queries." |
| ~~Exa agent~~ | ~~Semantic metadata expectations implicit~~ | Not an issue - example shows `similarityScore` and `contentType` in metadata (lines 55-58), and line 96 mentions including similarity scores |
| GitHub agent | Uses `gh` CLI instead of GitHub MCP | Should use `mcp__github__search_repositories`, `mcp__github__get_file_contents`, etc. for consistency with other researchers. Update tools list and research process to use MCP. |
| Exa agent | Wrong MCP tool names | Uses `mcp__exa__search`, `mcp__exa__find_similar` which don't exist. Actual tools: `web_search_exa`, `get_code_context_exa`, `deep_researcher_start/check`. See https://docs.exa.ai/reference/exa-mcp |
| ~~Tavily agent~~ | ~~No untrusted content handling~~ | Not an issue - agent only reads and reports, has no execution capability. Generic security advice doesn't apply. |
| ~~Synthesizer agent~~ | ~~Confidence algorithm undefined~~ | Not an issue - lines 106-110 define the algorithm (+0.2 for 4/4, +0.1 for 3/4, -0.1 for 1 source), lines 112-115 cover missing reports |
| ~~Synthesizer agent~~ | ~~Write scope unlimited~~ | Not an issue - lines 37 and 41 explicitly specify writing only `synthesis.md` to the cache directory |
| ~~Cache directory creation~~ | ~~No error handling~~ | Not an issue - Claude handles `mkdir -p` gracefully, permission errors are system issues outside prompt scope |
| ~~index.json~~ | ~~Structure undocumented~~ | Low priority - structure is documented inline in command (lines 117-128), separate schema is polish not a requirement |

---

## Comparison: This PR vs Anthropic's research-agent Demo

The owner asked CodeRabbit to compare against `anthropics/claude-agent-sdk-demos/research-agent`.

| Aspect | Anthropic Demo | This PR |
|--------|----------------|---------|
| **Foundation** | TypeScript/SDK runtime | Declarative Markdown specs |
| **Strategy** | Dynamic subtopic decomposition | Fixed 4 sources by type |
| **Agent Spawning** | Variable count per query complexity | Fixed 4 researchers always |
| **Caching** | Ephemeral sessions | 30-day TTL persistent cache |
| **Validation** | Demo flexibility | JSON Schema + Python validation |
| **Authority** | Not specified | Explicit hierarchy (deepwiki > tavily > github > exa) |
| **Setup Complexity** | Higher (SDK, TypeScript) | Lower (Markdown specs) |
| **Extensibility** | Add tool capabilities | Add source-specific researchers |

**Trade-offs:**

- Anthropic's approach: More dynamic, better for varying query complexity
- This PR: More deterministic, better for reproducible research with caching

---

## Recommendations

### Before Merge (Required)

1. **Critical:** Restructure as a plugin
   - Move from `.claude/` to `plugins/meta/research-pipeline/`
   - Update all paths to use `${CLAUDE_PLUGIN_ROOT}`
   - Add `plugin.json` manifest

2. ~~**Critical:** Fix GitHub agent to use GitHub MCP~~ → ✅ **FIXED**
   - Now uses `mcp__github__search_repositories`, `mcp__github__search_code`, etc.

3. ~~**Critical:** Fix Exa agent tool names~~ → ✅ **FIXED**
   - Now uses `mcp__exa__web_search_exa`, `mcp__exa__get_code_context_exa`, `mcp__exa__crawling_exa`

4. ~~**Important:** Improve orchestrator error handling~~ → ✅ **FIXED**
   - Error handling now uses clear conditional prose
   - Added tiered thresholds: 3-4 success (normal), 2 success (warn), 0-1 (stop)

5. ~~**Important:** Add validation path to error output~~ → ✅ **FIXED**
   - `ValidationError` now shows `e.absolute_path` for nested errors

6. **New:** Integrate schema validation into orchestrator → ✅ **FIXED**
   - Phase 1 now validates each report after completion
   - Invalid reports marked as failed and excluded from synthesis

7. **New:** Document subagent prerequisites → ✅ **FIXED**
   - Added Prerequisites section listing required agent registrations

### After Merge (Follow-up)

1. Reframe authority hierarchy as content-type authority (not tool authority)
2. Expand DeepWiki agent to leverage `ask_question` for architectural insights
3. Add DeepWiki fail-fast handling for unindexed repos
4. Add `format: uri` to implementation URL field (one-line fix)

---

## Comment Analysis (Documentation Review)

Additional issues identified by analyzing documentation comments for accuracy and maintainability.

### Critical Documentation Issues

**1. Authority Hierarchy Needs Reframing**

**File:** `synthesizer-agent.md`

The documented hierarchy `deepwiki > tavily > github > exa` conflates tool names with content authority. GitHub repositories ARE often the official source for OSS projects.

**Fix:** Reframe as content type authority, not tool authority:

```text
official documentation > architectural insights > community tutorials > code implementations > semantic matches
```

A GitHub README that IS official documentation should be treated as official docs. The hierarchy should guide conflict resolution based on what TYPE of content was found, not which tool found it.

**2. DeepWiki Agent Underutilizes Key Capability**

**File:** `deepwiki-agent.md`

The agent is framed as "find official documentation" but the real power of DeepWiki is `mcp__deepwiki__ask_question` - an LLM with an indexed codebase that can provide architectural insights impossible to get from file-level tools.

**Missing use cases:**
- Architectural questions: "How does the authentication flow work?"
- Design rationale: "Why did they choose this pattern?"
- Cross-cutting concerns: "Where is error handling implemented?"
- Integration insights: "How do these components interact?"

**Fix:** Expand the agent's purpose beyond documentation retrieval to include architectural analysis and codebase-level insights. The agent should leverage `ask_question` for synthesis questions that require understanding across multiple files.

**3. Agent Path Format in Orchestrator**

**File:** `lunar-research.md`

Agent references use backtick-quoted paths (`` `.claude/agents/research/github-agent.md` ``) which may not work with the Task tool's expected format.

### Documentation Improvement Opportunities

| File | Issue | Suggestion |
|------|-------|------------|
| deepwiki-agent.md | Missing repository context | Add guidance for non-repository queries |
| ~~github-agent.md~~ | ~~Missing prerequisite~~ | Stale - gh CLI being replaced with GitHub MCP |
| lunar-research.md | Index edge cases | Document duplicate handling, entry updates |
| ~~synthesizer-agent.md~~ | ~~Undefined formula~~ | Not an issue - confidence algorithm is defined at lines 106-110 |

### Recommended Removals (Reduce Maintenance Burden)

1. **Redundant confidence guidance** - Same rubric repeated in all 4 researcher agents. Consider extracting to shared reference if agents move to plugin structure.

### Additional Observations

| Observation | Assessment |
|-------------|------------|
| ~~Output format asymmetry~~ | Not an issue - JSON for programmatic synthesis, Markdown for human consumption is intentional |
| ~~Missing validation~~ | Low priority - synthesis.md is freeform, index.json documented inline |
| Race condition risk | Edge case - unlikely in single-user context, note for future if shared |

### Positive Documentation Findings

- Well-structured YAML frontmatter in all agents
- Explicit quality standards sections
- Clear phase-based orchestration
- Good error handling section (though vague)
- Self-documenting PEP 723 script header

---

## Review Tools Used

| Tool | Focus | Result |
|------|-------|--------|
| `/verify-pr` | Claims vs implementation | 14/14 claims verified ✅ |
| `code-reviewer` agent | Logic bugs, plan alignment | No critical issues |
| `comment-analyzer` agent | Documentation accuracy | 3 critical, 6 improvements |

---

## Final Assessment

**Verification Status:** All 14 claims verified correct ✅

**Code Review:** ~~Architecture needs restructuring~~ → All critical issues resolved

**Documentation Review:** Several original concerns were invalid; real issues identified and fixed

**Merge Readiness:** Needs plugin restructuring

The implementation matches the PR description and the multi-agent research pipeline concept is sound.

**Resolved issues:**
1. ~~GitHub agent uses `gh` CLI~~ → Now uses GitHub MCP tools
2. ~~Exa agent uses non-existent tool names~~ → Fixed to correct MCP tool names
3. ~~Orchestrator error handling vague~~ → Clear conditional prose with tiered thresholds
4. ~~Validation script missing error path~~ → Shows `absolute_path` for nested errors
5. ~~No schema validation in orchestrator~~ → Reports validated after each researcher completes
6. ~~Subagent prerequisites undocumented~~ → Prerequisites section added

**Remaining before merge:**
1. Restructure as a plugin under `plugins/meta/research-pipeline/`

**Follow-up (after merge):**
1. Authority hierarchy should be reframed as content-type authority
2. DeepWiki agent underutilizes `ask_question` for architectural insights
3. Minor schema fix (URL format validation)

The original review overstated several issues (schema required fields, cache flow, agency confusion, various CodeRabbit nitpicks) that were actually non-issues when evaluated against slash command best practices.
