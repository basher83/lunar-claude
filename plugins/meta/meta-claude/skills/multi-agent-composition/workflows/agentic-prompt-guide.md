# Agentic Prompt Guide

**A comprehensive guide for creating effective sub-agent prompts in Claude Code**

## Overview

When creating prompts for sub-agents (via the Task tool), use this proven 4-part structure to ensure agents understand their mission, have clear inputs, know their process, and deliver consistent outputs.

> "The best agentic prompts follow a clear structure: tell them WHY they exist, WHAT they're working with, HOW to do it, and WHAT to return."

## ⚠️ Critical Understanding: Stateless Execution

**Sub-agents are completely stateless:**

- You cannot send follow-up messages to the agent
- The agent cannot ask you clarifying questions
- They return exactly ONE message with their complete findings
- All required information MUST be included in the initial prompt

**This means:** Front-load ALL context, instructions, and specifications in your initial prompt. The agent gets one shot to complete the task autonomously.

---

## Task Tool Interface

When invoking the Task tool in Claude Code, you provide two parameters:

```typescript
{
  // A short (3-5 word) description for the UI label
  description: string;

  // The complete task prompt (your 4-part structure goes here)
  prompt: string;
}
```

**Example tool call:**

```json
{
  "description": "Review Python security",
  "prompt": "[Your complete Purpose/Variables/Workflow/Report goes here]"
}
```

The `description` appears in the Claude Code UI to help users track active sub-agents. The `prompt` contains your full instructions.

---

## Tools Available to Sub-Agents

Sub-agents have access to these Claude Code tools:

**File Operations:**

- `Read` - Read files with pagination support
- `Edit` - Make surgical edits to files
- `MultiEdit` - Make multiple edits to a file at once
- `Write` - Create or overwrite files
- `Glob` - Fast file pattern matching
- `LS` - List directory contents

**Search:**

- `Grep` - Fast content search with regex
- `Glob` - Find files by name patterns

**System:**

- `Bash` - Execute bash commands (use for tests, git operations, etc.)

**Specialized:**

- `NotebookRead` / `NotebookEdit` - Jupyter notebook operations
- `WebFetch` - Fetch and analyze web content
- `WebSearch` - Search the web
- `TodoRead` / `TodoWrite` - Task list management

**Note:** Sub-agents cannot spawn their own sub-agents (no recursive Task tool usage).

---

## The 4-Part Structure

### 1. Purpose

**What it is:** A clear statement of the agent's mission, role, and constraints.

**Why it matters:** Sets boundaries and focus. Prevents scope creep and ensures the agent knows what NOT to do.

**Template:**

```text
You are [specific role]. Your task is to [specific action].

Intent: [CODE WRITING | RESEARCH ONLY]

Constraints:
- [limitation 1]
- [limitation 2]
- [limitation 3]
```

**Critical: Specify Intent**

Always explicitly state whether the agent should:

- **Write/edit code** - Agent will use Write, Edit, MultiEdit tools
- **Only perform research** - Agent will use Read, Grep, Glob, WebFetch, WebSearch

The agent is not aware of the user's intent, so you must state it clearly.

**Example:**

```text
You are a code security reviewer. Your task is to identify security vulnerabilities
in Python files.

Intent: RESEARCH ONLY - Do not modify any code, only analyze and report findings.

Constraints:
- Focus only on security vulnerabilities, not style or performance
- Limit review to files provided in the inputs
- Only report vulnerabilities with severity >= threshold
- Include exact line numbers and remediation suggestions
```

---

### 2. Variables

**What it is:** The inputs and context the agent needs to complete its task.

**Why it matters:** Makes the agent's job deterministic. Clear inputs = clear outputs. Remember: the agent is stateless and cannot ask for missing information.

**Template:**

```text
Inputs:
- [input 1]: [description]
- [input 2]: [description]
- [input 3]: [description]

Context:
- [context fact 1]
- [context fact 2]
- [context fact 3]
```

**Example:**

```text
Inputs:
- file_paths: ["src/auth.py", "src/api/users.py", "src/db/queries.py"]
- severity_threshold: "high" (only report high and critical severity issues)
- codebase_type: "production web application with user authentication"

Context:
- This is a production codebase currently in use
- Security vulnerabilities have higher priority than performance issues
- The application handles sensitive user data
- Previous audit found SQL injection vulnerabilities that must be checked
```

---

### 3. Workflow

**What it is:** Step-by-step instructions for how to complete the task.

**Why it matters:** Ensures consistent execution. Prevents agents from skipping steps or going out of order. Since the agent is stateless, the workflow must be complete and unambiguous.

**Template:**

```text
Follow this workflow:

1. [Step 1 with specific tool usage]
2. [Step 2 with clear action]
3. [Step 3 with clear action]
4. [Final step leading to output]

Tool Usage:
- Use [ToolName] to [specific action]
- Use [ToolName] to [specific action]

Important considerations:
- [edge case 1]
- [consideration 2]
- [error handling approach]
```

**Example:**

```text
Follow this workflow:

1. Read each file using the Read tool:
   - Read src/auth.py
   - Read src/api/users.py
   - Read src/db/queries.py

2. For each file, identify these vulnerability types:
   - SQL injection (user input in queries without parameterization)
   - Command injection (user input in system commands)
   - Insecure cryptographic practices (weak algorithms, hardcoded keys)
   - Authentication bypasses (missing auth checks, weak token validation)

3. For each finding:
   - Note the exact file path and line number
   - Classify severity: low, medium, high, or critical
   - Write a clear description of the vulnerability
   - Draft a specific remediation suggestion with code example

4. Filter findings based on severity_threshold (only include >= "high")

5. Generate final report in the specified JSON format

Tool Usage:
- Use Read tool for all file access (do not use Bash cat/head/tail)
- Use Grep if you need to search for specific patterns across files
- Do not use Edit or Write tools (research only)

Important considerations:
- If a file doesn't exist or can't be read, note it in the report and continue
- If you find a critical vulnerability, ensure it's flagged with severity="critical"
- For SQL injection, look for f-strings or string concatenation in query building
- Check both direct vulnerabilities and potential attack vectors
```

---

### 4. Report

**What it is:** The exact format and structure of the agent's output.

**Why it matters:** Enables automated processing and makes results predictable. Since this is the agent's only communication, it must contain everything needed.

**Recommended: Structured JSON Output**

For programmatic processing and multi-agent orchestration, JSON is ideal:

```text
Report Format:

Return a JSON object with this structure:
{
  "field1": "description",
  "field2": 123,
  "field3": [
    {
      "nested_field1": "description",
      "nested_field2": "description"
    }
  ],
  "summary": "human-readable summary for context"
}

IMPORTANT:
- Return ONLY valid JSON, no markdown code blocks or additional text
- Ensure all strings are properly escaped
- Include a summary field for human readability
```

**Alternative: Structured Text Report**

For simpler use cases or when human readability is primary:

```text
Report Format:

Structure your response as:

# [Task Name] Results

## Summary
[1-2 sentence overview]

## Findings
1. [Finding 1 with details]
2. [Finding 2 with details]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]

## Statistics
- [Relevant metrics]
```

**Choose the format based on:**

- JSON: For automated processing, aggregation, or multi-agent workflows
- Text: For direct human consumption or simpler analysis tasks

**Complete Example:**

```text
Report Format:

Return a JSON object with this structure:
{
  "files_reviewed": 3,
  "total_findings": 5,
  "findings": [
    {
      "file": "src/auth.py",
      "line": 42,
      "severity": "critical",
      "type": "sql_injection",
      "description": "User input directly interpolated into SQL query without parameterization",
      "vulnerable_code": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "remediation": "Use parameterized queries: cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))"
    }
  ],
  "files_with_issues": ["src/auth.py", "src/db/queries.py"],
  "summary": "Reviewed 3 files and found 5 vulnerabilities: 2 critical, 2 high, 1 medium. Primary concerns are SQL injection in auth.py and weak password hashing in users.py."
}

IMPORTANT:
- Return ONLY the JSON object, no additional text or markdown formatting
- Ensure the JSON is valid and parseable
- Include ALL findings that meet the severity threshold
- If no findings, return empty findings array with appropriate summary
```

---

## Complete Example

Here's a full agentic prompt using all 4 parts:

```text
You are a code security reviewer. Your task is to identify security vulnerabilities
in Python files and provide detailed remediation guidance.

Intent: RESEARCH ONLY - Do not modify any code, only analyze and report findings.

Constraints:
- Focus only on security vulnerabilities, not style or performance
- Limit review to files provided in the inputs
- Only report vulnerabilities with severity >= threshold
- Include exact line numbers and remediation suggestions with code examples

Inputs:
- file_paths: ["src/auth.py", "src/api/users.py", "src/db/queries.py"]
- severity_threshold: "high" (only report high and critical severity issues)
- codebase_type: "production web application with user authentication"

Context:
- This is a production codebase currently in use
- Security vulnerabilities have higher priority than performance issues
- The application handles sensitive user data (passwords, email, payment info)
- Previous audit found SQL injection vulnerabilities that must be checked
- The application uses PostgreSQL database

Follow this workflow:

1. Read each file using the Read tool:
   - Read src/auth.py
   - Read src/api/users.py
   - Read src/db/queries.py

2. For each file, identify these vulnerability types:
   - SQL injection (user input in queries without parameterization)
   - Command injection (user input in system commands)
   - Insecure cryptographic practices (weak algorithms, hardcoded keys)
   - Authentication bypasses (missing auth checks, weak token validation)
   - Sensitive data exposure (passwords in logs, API keys in code)

3. For each finding:
   - Note the exact file path and line number
   - Classify severity: low, medium, high, or critical
   - Write a clear description of the vulnerability and attack vector
   - Quote the vulnerable code snippet
   - Draft a specific remediation suggestion with corrected code example

4. Filter findings based on severity_threshold (only include >= "high")

5. Generate final report in the specified JSON format

Tool Usage:
- Use Read tool for all file access (do not use Bash cat/head/tail)
- Use Grep if you need to search for specific patterns across files
- Do not use Edit or Write tools (research only)

Important considerations:
- If a file doesn't exist or can't be read, note it in the report and continue
- If you find a critical vulnerability, ensure it's flagged with severity="critical"
- For SQL injection, look for f-strings, %, or + operators in query building
- Check both direct vulnerabilities and potential attack vectors
- Include OWASP category references where applicable

Report Format:

Return a JSON object with this structure:
{
  "files_reviewed": 3,
  "total_findings": 5,
  "findings": [
    {
      "file": "src/auth.py",
      "line": 42,
      "severity": "critical",
      "type": "sql_injection",
      "description": "User input directly interpolated into SQL query without parameterization, allowing SQL injection attacks",
      "vulnerable_code": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "remediation": "Use parameterized queries with placeholders: cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))",
      "owasp": "A03:2021 - Injection"
    }
  ],
  "files_with_issues": ["src/auth.py", "src/db/queries.py"],
  "clean_files": ["src/api/users.py"],
  "summary": "Reviewed 3 files and found 5 vulnerabilities: 2 critical, 3 high. Primary concerns are SQL injection in auth.py (lines 42, 67) and weak password hashing in queries.py. No issues found in users.py."
}

IMPORTANT:
- Return ONLY the JSON object, no additional text or markdown formatting
- Ensure the JSON is valid and parseable
- Include ALL findings that meet the severity threshold
- If no findings, return empty findings array with summary stating "No vulnerabilities found"

---

Now review the files specified in the inputs above.
```

---

## Performance: Parallel Agent Execution

Launch multiple agents concurrently when tasks are independent to maximize performance.

**❌ Sequential (Slow):**

```text
1. Launch Agent 1 to search for authentication code
2. Wait for result
3. Launch Agent 2 to search for database queries
4. Wait for result
5. Launch Agent 3 to search for API endpoints
6. Wait for result
```

**✅ Parallel (Fast):**

```text
Launch all three agents in a single message with multiple tool uses:
- Agent 1: Search for authentication code
- Agent 2: Search for database queries
- Agent 3: Search for API endpoints

All execute concurrently, return results together
```

**Example use case:** When analyzing different aspects of a codebase, searching multiple directories, or fetching multiple web resources, launch agents in parallel.

---

## When NOT to Use Sub-Agents

Avoid sub-agents for tasks that are faster with direct tools:

**❌ Don't use sub-agents for:**

- Reading a specific known file → Use `Read` tool directly
- Searching for a specific class definition → Use `Glob` tool directly
- Searching within 2-3 known files → Use `Read` tool directly
- Simple pattern searches → Use `Grep` tool directly
- Single bash commands → Use `Bash` tool directly

**✅ DO use sub-agents for:**

- Open-ended searches where you're not confident in finding the right match quickly
- Searching for keywords like "config" or "logger" across unknown codebase structure
- Questions like "which file does X?" when structure is unclear
- Complex multi-step analysis requiring multiple tool uses
- Tasks that benefit from isolated context (avoiding context pollution)
- Parallel execution of independent operations

---

## Best Practices

### 1. Be Explicit About Tools

Always specify which Claude Code tools the agent should use:

```text
Tool Usage:
- Use the Read tool to access files (not Bash cat/head/tail)
- Use the Grep tool to search for patterns (not Bash grep)
- Use the Glob tool to find files by name
- Use the Bash tool only for running tests or git operations
```

**Why:** Agents may guess wrong about how to access resources. Explicit tool guidance prevents inefficient approaches.

### 2. Specify Output Format Strictly

Structured output enables automated processing:

**✅ Good:**

```text
Return JSON: {"status": "success", "count": 5, "items": [...]}
```

**❌ Bad:**

```text
Return the results in a structured format
```

### 3. Include Success Criteria

Tell the agent how to know they're done:

- "Continue until all files are processed"
- "Stop when you find 3 examples"
- "Complete when tests pass or max 3 attempts reached"
- "Search up to 10 files; if no matches, report none found"

### 4. Handle Edge Cases Explicitly

Anticipate failure modes and provide guidance:

```text
Edge cases:
- If a file doesn't exist, log it in the report and continue with others
- If tests fail, include the full error output in the report
- If no findings match the criteria, return an empty array with explanatory summary
- If you encounter permission errors, note which files were inaccessible
```

### 5. Front-Load All Information

Since agents are stateless and cannot ask questions:

```text
✅ Include in prompt:
- All required file paths
- All configuration values
- All search criteria
- All output requirements
- All edge case handling

❌ Don't assume agent can:
- Ask for missing information
- Remember previous context
- Access information not in prompt
```

### 6. Separate Instructions from Data

Put the 4-part structure first, then provide the actual inputs:

```text
[Purpose]
[Variables]
[Workflow]
[Report Format]

---

Now process this data:
- File 1: /path/to/file1.py
- File 2: /path/to/file2.py
- Search term: "authentication"
```

---

## Common Patterns

### Pattern 1: Multi-File Analysis

```text
Purpose: Analyze multiple files and aggregate results
Variables: file_paths, analysis_criteria, thresholds
Workflow: Read → Analyze → Filter → Aggregate → Report
Report: JSON with per-file results + aggregate summary
Tools: Read, Grep (if searching), Bash (if testing)
```

### Pattern 2: Iterative Search

```text
Purpose: Search for patterns across codebase
Variables: search_patterns, directories, max_results, file_types
Workflow: Grep → Filter by relevance → Read matching files → Extract → Report
Report: Structured list of matches with context and locations
Tools: Grep, Glob, Read
```

### Pattern 3: Research & Analysis

```text
Purpose: Research a topic using web and file resources
Variables: research_questions, file_paths, web_domains
Workflow: Read files → WebSearch → WebFetch → Synthesize → Report
Report: Structured findings with source attribution
Tools: Read, WebSearch, WebFetch
```

### Pattern 4: Code Generation

```text
Purpose: Generate code based on specification
Variables: specification, language, output_path, style_guide
Workflow: Parse spec → Generate → Validate syntax → Write → Report
Report: File paths created + validation results
Tools: Write, Bash (for syntax checking/linting)
```

### Pattern 5: Test Execution & Analysis

```text
Purpose: Run tests and analyze failures
Variables: test_command, test_files, retry_count
Workflow: Bash test → Parse output → Identify failures → Read relevant code → Report
Report: Test results with failure analysis and suggested fixes
Tools: Bash, Read, Grep
```

---

## Anti-Patterns

### ❌ Vague Purpose

```text
You are a helpful agent. Help the user with their task.
```

**Why bad:** No constraints, unclear scope, unpredictable behavior

**Fix:** Be specific about role, action, and constraints

---

### ❌ Missing Variables

```text
Analyze the files and find issues.
```

**Why bad:** Which files? What kinds of issues? What severity? How many?

**Fix:** Provide complete inputs and context

---

### ❌ No Workflow

```text
Your task is to review code for bugs.

Report: A report with findings.
```

**Why bad:** Agent invents their own workflow, leading to inconsistent results

**Fix:** Provide step-by-step workflow with tool usage

---

### ❌ Unstructured Report

```text
Report back with what you found.
```

**Why bad:** Can't parse output programmatically, hard to aggregate results

**Fix:** Specify exact output structure (JSON schema or text template)

---

### ❌ Missing Intent Specification

```text
You are a code assistant. Help with the authentication module.
```

**Why bad:** Agent doesn't know if it should write code or just research

**Fix:** Explicitly state: "Intent: RESEARCH ONLY" or "Intent: CODE WRITING"

---

### ❌ Assuming Agent Can Ask Questions

```text
Review the user authentication code and let me know if you need more information.
```

**Why bad:** Agent is stateless and cannot ask follow-up questions

**Fix:** Include ALL necessary information upfront in Variables section

---

## Advanced: Nested Context Pattern

When you need agents to work with different context windows or handle specialized subtasks:

```text
Main Agent Workflow:
1. Break task into N specialized subtasks
2. For each subtask, spawn a sub-agent with this structure:

   [Sub-agent Purpose - specialized role]
   [Sub-agent Variables - subset of data]
   [Sub-agent Workflow - specific to subtask]
   [Sub-agent Report - structured for aggregation]

3. Collect all sub-agent reports
4. Aggregate, deduplicate, and synthesize findings
5. Generate final unified report

Example:
- Main agent: "Analyze entire codebase for issues"
- Sub-agent 1: "Review authentication code"
- Sub-agent 2: "Review database queries"
- Sub-agent 3: "Review API endpoints"
- Main agent aggregates findings from all three
```

---

## Result Interpretation

After receiving sub-agent results:

**Agent outputs should generally be trusted** - Claude Code's guidance states sub-agent outputs are reliable.

**However, the main agent should:**

1. **Summarize for the user** - Sub-agent results are not automatically visible to users
2. **Extract key findings** - Present the most relevant information concisely
3. **Aggregate if multiple agents** - Combine results from parallel agents coherently
4. **Add context** - Explain what the findings mean in the broader context

**Example:**

```text
Sub-agent returned: [detailed JSON with 15 findings]

Main agent summarizes: "I found 15 security vulnerabilities across 3 files.
The most critical are 2 SQL injection points in auth.py (lines 42, 67) and
1 hardcoded API key in config.py (line 23). Would you like me to fix these
or see the full detailed report?"
```

---

## Quick Reference Checklist

When creating a sub-agent prompt, ensure you have:

- [ ] **Purpose**: Specific role, action, and intent (CODE or RESEARCH)
- [ ] **Variables**: All inputs, parameters, and context needed
- [ ] **Workflow**: Step-by-step process with explicit tool usage
- [ ] **Report**: Exact output format (JSON schema or text template)
- [ ] **Stateless design**: All info included, no assumptions about follow-up
- [ ] **Edge cases**: Guidance for errors, missing files, no results
- [ ] **Success criteria**: How agent knows task is complete
- [ ] **Tool specification**: Which tools to use for each step
- [ ] **Intent declaration**: Code writing vs research only

---

## Additional Resources

**Official Documentation:**

- Claude Code Best Practices: <https://www.anthropic.com/engineering/claude-code-best-practices>
- Claude 4 Prompting: <https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices>
- Building Agents with Claude: <https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk>

**Pattern Origin:**
This structure emerged from community best practices and practical experience with Claude Code. The 4-part framework (Purpose → Variables → Workflow → Report) has proven effective across diverse use cases, from code analysis to research tasks.

---

## Summary

Effective sub-agent prompts are:

- **Specific** - Clear role, action, and constraints
- **Complete** - All necessary information included upfront
- **Structured** - Organized workflow with explicit tool usage
- **Predictable** - Well-defined output format
- **Stateless** - No assumptions about follow-up communication

By following this template, you'll create sub-agents that execute tasks reliably, return consistent results, and integrate smoothly into multi-agent workflows.
