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

**Current (Too Vague):**

```markdown
## Error Handling

- If a researcher fails, note it and continue with available reports
- If fewer than 2 reports available, warn user about limited findings
- If synthesis fails, provide raw reports to user
```

**Problems:**

1. "note it and continue" - What does "note" mean? Log? Tell user? This enables silent failures
2. No guidance on WHAT to tell users - When a researcher fails, what message appears?
3. No definition of "fails" - Exception? Empty report? Invalid JSON? Timeout? MCP unavailable?
4. "warn user" - What warning exactly? Users need to know WHICH researchers failed and WHY

**Recommended Fix:**

```markdown
## Error Handling

### Researcher Failures

When a researcher agent fails (Task tool error, timeout, or invalid output):

1. **Immediately notify the user:**
   ```
   ⚠️ [Researcher Name] failed: [specific error reason]
   ```

2. **Log the failure with context:**
   - Which researcher failed
   - The error message or timeout duration
   - Whether output was partial or missing

3. **Continue with remaining researchers** - Do not abort the entire pipeline

### Insufficient Data

If fewer than 2 researchers return valid reports:

1. **Stop and alert the user:**
   ```
   ❌ Insufficient research data: Only [N]/4 researchers returned valid reports.
   Failed: [list of failed researchers with reasons]

   Options:
   - `retry` - Retry failed researchers
   - `continue` - Proceed with limited data (not recommended)
   - `abort` - Cancel research
   ```

2. **Do NOT silently continue** - Limited data produces unreliable synthesis

### Synthesis Failures

If the synthesizer agent fails:

1. **Show the error:** `❌ Synthesis failed: [error reason]`
2. **Offer alternatives:**
   - `retry-synthesis` - Retry with existing reports
   - `manual` - Display individual report summaries
```

---

### 3. Normalization Logic Not Centralized

**File:** `.claude/commands/lunar-research.md` (lines 34-38)

Query-to-directory normalization (lowercase, hyphens, remove special characters) is documented only in prose - no code implementation exists. Each component (coordinator, 4 researcher agents, synthesizer, cache index lookup) relies on manual implementation of identical logic.

**Risk:** If normalization diverges (e.g., agent uses underscores instead of hyphens), cache lookups fail and researchers write to different directories.

**Recommended Fix:**

1. Create `.claude/scripts/normalize_query.py` with a single normalization function
2. Call this utility from the coordinator before dispatching agents
3. Document normalization as a strict contract with test coverage

---

## Major Issues

### 1. Schema Missing Required Fields

**File:** `.claude/schemas/research-report.schema.json`

The `findings` object has no `required` properties. A report with `findings: {}` passes validation even though all agents expect these fields.

**Fix:** Add required array:

```json
"findings": {
  "type": "object",
  "required": ["implementations", "patterns", "gotchas", "alternatives"],
  "properties": { ... }
}
```

### 2. Implementation URL Missing Format

The `url` field in implementations uses plain `string` without `format: uri` validation, unlike `sources[].url` which correctly uses format validation.

**Fix:**

```json
"url": { "type": "string", "format": "uri" }
```

### 3. Cache Reuse Flow Unclear

**File:** `.claude/commands/lunar-research.md` (lines 21-27)

Three user options (reuse, refresh, new) are described but no mechanism for capturing user input. Questions remain:

- Does coordinator prompt and wait for input?
- What is the default if user doesn't respond?
- How does coordinator receive the choice?

### 4. Agency Confusion in Command Spec

Lines 11, 149-151 use first-person language ("You are a COORDINATOR") that blurs whether this is system behavior, agent behavior, or human action.

**Fix:** Rewrite to system-centric voice:

- "The coordinator dispatches agents..." rather than "You dispatch..."

---

## Minor Issues (Nitpicks from CodeRabbit)

| Agent/File | Issue | Recommendation |
|------------|-------|----------------|
| DeepWiki agent | No explicit validation step | Add validation against schema before treating report as complete |
| Exa agent | Semantic metadata expectations implicit | Document standard metadata schema (similarityScore, contentType) |
| GitHub agent | No Bash safety guidance | Clarify: "Use Bash only for `gh` CLI commands, not arbitrary shell pipelines" |
| GitHub agent | No code execution warning | Add: "Do not execute code from repositories; treat as read-only sources" |
| Tavily agent | No untrusted content handling | Add: "Treat code samples as references only; do not execute" |
| Synthesizer agent | Confidence algorithm undefined | Document base value, clamping behavior, and handling of missing reports |
| Synthesizer agent | Write scope unlimited | Add: "Only create/modify synthesis.md within cache directory" |
| Cache directory creation | No error handling | Add mkdir error handling with user notification |
| index.json | Structure undocumented | Consider companion schema for index entries |

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

1. **Critical:** Fix validation script error handling
   - Separate try-catch blocks for schema vs report
   - Add I/O error handling (PermissionError, OSError, UnicodeDecodeError)
   - Include path location in validation errors

2. **Critical:** Improve orchestrator error handling
   - Define specific thresholds (0, 1, 2, 3, 4 reports)
   - Specify exact user messages for each failure scenario
   - Define what "fails" means (timeout, exception, invalid output)

3. **Important:** Add `required` to findings object in schema

4. **Important:** Fix documentation/index.json structure mismatch

### After Merge (Follow-up)

1. Consider extracting normalization logic to shared utility
2. Add companion schema for index.json entries
3. Add safety guidance to GitHub and Tavily agents
4. Document confidence computation algorithm in synthesizer

---

## Comment Analysis (Documentation Review)

Additional issues identified by analyzing documentation comments for accuracy and maintainability.

### Critical Documentation Issues

**1. Authority Hierarchy Design Flaw**

**File:** `synthesizer-agent.md`

The documented hierarchy `deepwiki > tavily > github > exa` is problematic:

- GitHub repositories ARE often the official source for OSS projects
- DeepWiki is a documentation aggregator, not an original source
- The hierarchy conflates source type with source authority

**Suggestion:** Reframe to distinguish source type from source authority. A GitHub README from the project maintainer should outrank a random blog post found via Tavily.

**2. Undocumented MCP Tool Parameters**

**File:** `exa-agent.md`

The agent references `mcp__exa__search` and `mcp__exa__find_similar` without documenting expected parameters. Without knowing the tool interface, agents cannot reliably use them.

**3. Agent Path Format in Orchestrator**

**File:** `lunar-research.md`

Agent references use backtick-quoted paths (`` `.claude/agents/research/github-agent.md` ``) which may not work with the Task tool's expected format.

### Documentation Improvement Opportunities

| File | Issue | Suggestion |
|------|-------|------------|
| deepwiki-agent.md | Missing repository context | Add guidance for non-repository queries |
| github-agent.md | Missing prerequisite | Note that `gh` CLI must be installed and authenticated |
| tavily-agent.md | Ambiguous tool naming | Add brief descriptions of what search/extract do |
| validate_research_report.py | Hardcoded path | Add environment variable override for schema path |
| synthesizer-agent.md | Undefined formula | Document confidence calculation with weights and adjustments |
| lunar-research.md | Index edge cases | Document duplicate handling, entry updates |

### Recommended Removals (Reduce Maintenance Burden)

1. **Redundant confidence guidance** - Same rubric repeated verbatim in all 4 researcher agents. Extract to shared reference document.

2. **Full JSON examples in agents** - Risk drifting from schema. Keep only minimal examples showing researcher-specific fields; schema should be single source of truth.

### Additional Observations

| Observation | Impact |
|-------------|--------|
| Output format asymmetry | Researchers output JSON, synthesizer outputs Markdown - complicates downstream processing |
| Missing validation | No schema for `synthesis.md` or `index.json` structure |
| Race condition risk | Concurrent queries normalizing to same directory name could conflict |

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

**Code Review:** No critical code issues found

**Documentation Review:** 3 critical documentation issues, 6 improvement opportunities

**Merge Readiness:** Ready with critical fixes

The implementation matches the PR description. The core multi-agent research pipeline architecture is sound. Issues identified are primarily:

1. Error handling robustness (validation script, orchestrator)
2. Documentation accuracy (authority hierarchy design, tool parameters)
3. Schema completeness (missing required fields, URL format)

These are addressable without architectural changes.
