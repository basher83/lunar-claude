# Lessons Learned - Raw Data

**Purpose:** Collection of instances where things went wrong during Claude Code
sessions. This is raw data only - no analysis.

**Data Collection Date:** 2025-11-08

**Search Terms Used:**

- "wrong"
- "stop"
- "why did you"
- "not what I asked"
- "no"
- "what are you"

---

## Incident 1: Incorrect Response

**Timestamp:** 2025-11-08 19:05:37 (7:05:37 PM)

**User Correction:** "No, wrong. what did I tell you?"

**Source:** claude-mem://user-prompt/471

**Context:** User prompt #2 in session. Previous context involved agent performance
evaluation and skill-reviewer being removed/deleted.

---

## Incident 2: TODO Placeholder Breaking Script

**Timestamp:** 2025-11-06 23:55:13 (11:55:13 PM)

**User Correction:**

> well your entry ito the challange was rejected due to a oversight on your part.
> You left a TODO placeholder that breaks
> plugins/meta/claude-docs/scripts/jina_mcp_docs.py. Right now the TODO placeholder
> glues the entire MCP response together and writes that same blob into every output
> file, so nothing ends up with its own page content. That breaks the core promise
> of the script—running it today produces duplicates instead of the actual docs.
> around lines 189 to 206, the code currently concatenates the entire MCP response
> into combined_content and writes that same blob to every output file; update it to
> parse the MCP tool response as a structured JSON array of objects with {url,
> content}, build a mapping from URL (or normalized page name) to its specific
> content, then iterate the urls list and for each url look up its corresponding
> content and write only that content to the file; if an entry is missing or writing
> fails, append a failure result (url, False, error_message) and log the problem,
> otherwise append success (url, True, written_content). Ensure robust error
> handling around JSON parsing and file I/O so each file is independently marked
> success/failure. I was able to convince the judges to give you a chance to fix it
> and re-submit it. I don't know if they will give you a third chance so we need to
> make this one count! You better make sure you triple check your work! Also In
> plugins/meta/claude-docs/tests/test_firecrawl_mcp_docs.py around lines 66 to 76,
> the test uses a hardcoded Path("/tmp") and leaves variables unused which causes
> portability and linter issues; change the test function signature to accept
> pytest's tmp_path fixture, pass tmp_path (not Path("/tmp")) into
> download_page_firecrawl, and rename any intentionally unused variables with a
> leading underscore (e.g., _success, _content, _metadata or use_ for ones you don't
> need) so the test is portable across OSes and removes unused-variable warnings.

**Source:** claude-mem://user-prompt/458

**Context:** User prompt #13 in session. Related to coding challenge submission that
was rejected.

---

## Incident 3: Agent Output Destination Misunderstanding

**Timestamp:** 2025-11-08 04:44:42 (4:44:42 AM)

**User Correction:** "no, it reports to YOU not me. then you tell me the info i need from the audit"

**Source:** claude-mem://user-prompt/463

**Context:** User prompt #5 in session. Discussion about claude-skill-auditor agent
and where audit reports should be sent.

---

## Incident 4: File Location Misunderstanding

**Timestamp:** 2025-11-08 04:41:40 (4:41:40 AM)

**User Correction:** "no no, i put the audit-report.md there earlier and forgot to
move it! currently the agent is designed to just report results to you directly"

**Source:** claude-mem://user-prompt/462

**Context:** User prompt #4 in session. Confusion about audit-report.md file placement.

---

## Incident 5: Wrong Git Branch

**Timestamp:** 2025-11-06 23:14:37 (11:14:37 PM)

**User Correction:** "uh, what? it shouldn't be on main!"

**Source:** claude-mem://user-prompt/453

**Context:** User prompt #8 in session. Code was committed to wrong branch (main
instead of feature branch).

---

## Incident 6: Skill Not Used

**Timestamp:** 2025-11-03 21:11:00 (9:11:00 PM)

**User Correction:** "why did you not use your skill?"

**Source:** Session S186 context

**Context:** Converting scripts/note_smith.py to a uv single file script. Agent did
not use the python-uv-scripts skill that was available.

---

## Incident 7: Skill Misunderstanding

**Timestamp:** 2025-11-03 23:46:00 (11:46:00 PM)

**User Correction:** "I think you misundersttod me. I meant use the
testing-skills-with-subagents skill"

**Source:** Session S200 context (claude-mem://user-prompt reference in timeline)

**Context:** User requested testing of a skill, but agent misunderstood which skill to use.

---

## Incident 8: Wrong Selection/Resume Request

**Timestamp:** 2025-11-08 04:31:20 (4:31:20 AM)

**User Correction:** "sry, wrong selection, pls resume"

**Source:** claude-mem://user-prompt/460

**Context:** User prompt #2 in session. User made wrong selection and requested to
resume previous action.

---

## Incident 9: Skill Usage Learning Moment

**Timestamp:** 2025-11-03 21:19:00 (9:19:00 PM)

**User Correction:** "well we learned a few things, you skipped the
using-superpowers process and highlighted that convert..."

**Source:** Session S187 context

**Context:** Agent skipped the using-superpowers mandatory workflow check before
proceeding with task.

---

## Incident 10: Ignoring Documented Troubleshooting Process

**Timestamp:** 2025-11-08 19:16:00 (7:16:00 PM)

**User Correction:**

> Yes, exactly. That is the issue: you made an assumption without verification. The
> part that comes before that is I gave you the exact troubleshooting guide you
> needed to troubleshoot and fix the situation, but you did not follow that either.
> Arguably, not following the workflow I gave you is a bigger problem than you just
> assuming.

**Source:** Current session (viewer UI troubleshooting)

**Context:** User requested help troubleshooting claude-mem viewer UI not loading and
provided path to troubleshooting.mdx guide. Agent read the complete troubleshooting
guide which contained explicit numbered steps for "Viewer UI Not Loading" (steps 1-4:
check port, verify health, check logs, restart worker). Agent completed steps 1-2
correctly, then skipped steps 3-4, read source code instead, assumed rebuild was
needed without verification, ran `npm run build`, then finally ran step 4 (restart
worker). The troubleshooting guide already contained the correct solution but agent
chose to improvise rather than follow the documented workflow.

---

## Search Results Summary

**Total searches performed:** 6

**Search terms and result counts:**

- "wrong": 20 results
- "stop": 20 results
- "why did you": 20 results
- "not what I asked": 20 results (no exact matches beyond current request)
- "no": 20 results
- "what are you": 20 results

**Key patterns observed in raw data:**

- Multiple corrections related to agent misunderstanding output destinations
- Git workflow issues (wrong branch)
- Skill usage protocol violations
- Code quality issues (TODO placeholders left in production code)
- Misunderstanding user intent
