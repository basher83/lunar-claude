# Lessons Learned - 2025-11-08

**Search Period:** Last 3 days (2025-11-05 to 2025-11-08)
**Report Generated:** 2025-11-08
**Total Incidents Found:** 12

---

## Search Strategy

This report combines three search methods:

1. User correction phrases in prompts
2. Problem-solution concept observations
3. Bugfix type observations

---

## Incidents

### Incident 1: Skill Selection Without Analysis

**Timestamp:** 2025-11-08 19:50:55

**Source:** claude-mem://user-prompt/481

**User Correction:**
> no stop. slow down and think this through. 1) take inventory of all skills available to you 2) identify what is the relevant context from the users message that we need to attempt to match to a skill. If the context matches more than one skill what skill is BEST suited to complete the current task? Should we load more than one skill? Do not load anything, pls just think and respond with what you should do here. I'm just trying to help walk you through my process

**Context:**
User requested help with "agentic composition" for continuous improvement system. Agent immediately loaded agent-creator skill without first analyzing which skill was most relevant. User stopped execution and walked through proper skill selection process: 1) inventory available skills, 2) identify relevant context, 3) determine best match. This led to discovering multi-agent-composition skill was the better match for the task.

---

### Incident 2: Context Pollution from Incorrect Task Ordering

**Timestamp:** 2025-11-08 20:31:30

**Source:** claude-mem://user-prompt/499

**User Correction:**
> hold up. we need to Create command implementation at .claude/commands/improve.md first. This has to go first because we have to load a skill for writing documentation and we don't want to load that skill before the command, it may pollute the context

**Context:**
Agent was about to write documentation before creating the command implementation. User corrected to create implementation first, then load writing skill for documentation. This prevents loading unnecessary context (writing skill) before completing the primary artifact (command file).

---

### Incident 3: TODO Placeholder Breaking Script (Historical - Nov 6)

**Timestamp:** 2025-11-06 23:55:57

**Source:** claude-mem://observation/777

**Context:**
Critical bug in jina_mcp_docs.py where TODO placeholder at lines 189-206 caused script to write identical duplicate content to every output file instead of unique content per URL. Root cause was incomplete implementation that concatenated entire MCP response into combined_content variable. Fix implemented structured JSON parsing to extract {url, content} objects and map each URL to its specific content. This broke coding challenge submission and required re-submission after fix.

**Learning:** TODO placeholders in production code paths break core functionality. Never leave TODOs that affect execution flow without explicit safeguards or validation.

---

### Incident 4: MCP Response Parsing - Ignored ToolResultBlock

**Timestamp:** 2025-11-07 00:15:34

**Source:** claude-mem://observation/779

**Context:**
jina_mcp_docs.py only processed TextBlock from AssistantMessage while completely ignoring ToolResultBlock from UserMessage which contained the actual MCP tool response data. This architectural misunderstanding caused the duplicate content bug. Fix added imports for ToolResultBlock and UserMessage, then rewrote response collection logic to handle both message types correctly.

**Learning:** When working with MCP tools, must process BOTH AssistantMessage (TextBlock) and UserMessage (ToolResultBlock) to capture complete tool response data.

---

### Incident 5: Missing Import - API Key Validation

**Timestamp:** 2025-11-06 22:59:39

**Source:** claude-mem://observation/763

**Context:**
jina_mcp_docs.py was missing the `os` module import required by validate_api_keys() function. This caused runtime errors when the validation function attempted to access environment variables. Fix added missing import and enhanced error handling.

**Learning:** Always verify imports when adding new function dependencies. End-to-end verification catches these issues before production.

---

### Incident 6: Hardcoded Path - Cross-Platform Compatibility

**Timestamp:** 2025-11-06 22:59:39

**Source:** claude-mem://observation/763

**Context:**
test_firecrawl_mcp_docs.py used hardcoded Path("/tmp") which breaks portability across operating systems (Windows doesn't have /tmp). Fix changed to use pytest's tmp_path fixture for cross-platform temporary directory handling.

**Learning:** Never hardcode OS-specific paths. Use pytest fixtures (tmp_path) or pathlib for cross-platform compatibility.

---

### Incident 7: Emoji Symbols Breaking Terminal Compatibility

**Timestamp:** 2025-11-06 22:41:30

**Source:** claude-mem://observation/756

**Context:**
jina_reader_docs.py used emoji symbols (⚠, ✓, ✗, 💡) in output messages which caused terminal compatibility issues across different environments. Project standards require text-based status messages. Fix replaced emojis with text equivalents: WARNING:, SUCCESS:, ERROR:, NOTE:.

**Learning:** Avoid emoji symbols in CLI output. Use text-based status prefixes for terminal compatibility.

---

### Incident 8: SessionStart Hook Context Injection Failure

**Timestamp:** 2025-11-05 03:34:10

**Source:** claude-mem://observation/698

**Context:**
Critical bug where npm install output was polluting SessionStart hook's JSON response, corrupting the hookSpecificOutput field. Claude Code hooks require clean JSON output, but npm's stderr/stdout messages (even with --loglevel=error) were written before hook's JSON output. This caused context injection to fail silently. Fix changed npm loglevel to silent ensuring completely clean output.

**Learning:** Hook integration points require strict output formatting. Any unexpected output (even from dependency installation) breaks the communication protocol between plugin and Claude Code.

---

### Incident 9: Multi-Agent Composition Skill Naming Violation

**Timestamp:** 2025-11-05 03:15:20

**Source:** claude-mem://observation/679

**Context:**
Skill was originally named "composing-claude-code" which violated reserved word rules (cannot use "claude" in skill names). Audit identified this as critical issue dropping compliance from 100% to 91%. Fix renamed skill to "multi-agent-composition" and corrected grammar issues, achieving 100% compliance.

**Learning:** Skill names cannot contain reserved words like "claude". Always verify skill naming conventions before creating.

---

### Incident 10: Worker Startup Race Condition

**Timestamp:** 2025-11-04 23:28:58

**Source:** claude-mem://observation/554

**Context:**
Critical race condition where hooks attempted to communicate with worker before it was fully initialized. ensureWorkerRunning() was synchronous and didn't verify worker health after PM2 start. This led to startup failures especially on cold starts and system resumes. Fix made ensureWorkerRunning() async with health check verification (retries for up to 10 seconds).

**Learning:** Always verify service health after startup, don't just assume PM2 start means ready. Async health checks with retry logic prevent race conditions.

---

### Incident 11: Prompt Engineering Impact Discovery

**Timestamp:** 2025-11-06 23:37:28

**Source:** claude-mem://observation/775

**Context:**
Analysis showed how prime-mind-v2.md's actionable framing and progressive disclosure pattern led to fundamentally different planning outcomes compared to prime-mind.md. The v2 approach naturally scaffolded TDD methodology and more structured planning. This demonstrates prompt structure has measurable impact on problem-solving methodology selection.

**Learning:** Prompt engineering structure (actionable framing, progressive disclosure) significantly influences planning behavior and methodology selection. Document and analyze prompt variations to understand impact.

---

### Incident 12: API Key Validation Missing in Main Flow

**Timestamp:** 2025-11-06 22:52:16

**Source:** claude-mem://observation/760

**Context:**
firecrawl_mcp_docs.py was missing API key validation in main() function, leading to cryptic errors during execution when environment variables were not set. Fix added validate_api_keys() call with proper try-except error handling and formatted output for both rich and JSON modes.

**Learning:** Validate environment variables and API keys early in main() execution flow. Fail fast with clear error messages rather than cryptic SDK initialization errors.

---

## Search Results Summary

**Total searches performed:** 3 strategies

**Results by strategy:**

- User correction phrases: 2 relevant incidents (searched 6 terms: "wrong", "stop", "why did you", "not what I asked", "no", "what are you")
- Problem-solution concepts: 1 observation (prompt engineering analysis)
- Bugfix observations: 10 observations (MCP parsing, API validation, worker health, etc.)

**Note:** This report shows ALL incidents in the time window. Manual reconciliation with existing lessons-learned files is required to identify truly new incidents.

---

## Patterns Observed

**Common themes across incidents:**

1. **Incomplete error handling** - Missing imports, validation, health checks
2. **Output formatting issues** - Emojis, JSON pollution from subprocess output
3. **Cross-platform compatibility** - Hardcoded paths, OS-specific assumptions
4. **Process violations** - TODOs in production, skipping validation steps
5. **Race conditions** - Async operations without health verification
6. **Naming conventions** - Reserved word violations in skill names
