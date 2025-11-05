# Agentic Prompt Format Template

**The canonical structure for sub-agent prompts** - Purpose → Variables → Workflow → Report

## Overview

When creating prompts for sub-agents (via the Task tool), use this proven 4-part structure to ensure agents understand their mission, have clear inputs, know their process, and deliver consistent outputs.

> "The best agentic prompts follow a clear structure: tell them WHY they exist, WHAT they're working with, HOW to do it, and WHAT to return."

## The 4-Part Structure

### 1. Purpose

**What it is:** A clear statement of the agent's mission and constraints.

**Why it matters:** Sets boundaries and focus. Prevents scope creep.

**Template:**

```text
You are [role]. Your task is to [specific action].

Constraints:
- [limitation 1]
- [limitation 2]
- [limitation 3]
```

**Example:**

```text
You are a code reviewer agent. Your task is to review Python code for security vulnerabilities and performance issues.

Constraints:
- Focus only on security and performance, not style
- Do not modify code, only report findings
- Limit review to files provided in the prompt
```

---

### 2. Variables

**What it is:** The inputs and context the agent needs to complete its task.

**Why it matters:** Makes the agent's job deterministic. Clear inputs = clear outputs.

**Template:**

```text
Inputs:
- [input 1]: [description]
- [input 2]: [description]
- [input 3]: [description]

Context:
- [context fact 1]
- [context fact 2]
```

**Example:**

```text
Inputs:
- file_paths: List of Python files to review
- severity_threshold: Minimum severity level to report (low, medium, high, critical)

Context:
- This is a production codebase
- Security vulnerabilities have higher priority than performance issues
- All findings must include line numbers and remediation suggestions
```

---

### 3. Workflow

**What it is:** Step-by-step instructions for how to complete the task.

**Why it matters:** Ensures consistent execution. Prevents agents from skipping steps or going out of order.

**Template:**

```text
Follow this workflow:

1. [Step 1 with clear action]
2. [Step 2 with clear action]
3. [Step 3 with clear action]
4. [Final step leading to output]

Important considerations:
- [consideration 1]
- [consideration 2]
```

**Example:**

```text
Follow this workflow:

1. Read each provided file using the Read tool
2. For each file, identify:
   - SQL injection vulnerabilities
   - Command injection points
   - Insecure cryptographic practices
   - Performance bottlenecks (N+1 queries, inefficient loops)
3. For each finding:
   - Classify severity (low, medium, high, critical)
   - Note the exact line number
   - Draft a remediation suggestion
4. Filter findings based on severity_threshold
5. Generate final report (see Report Format)

Important considerations:
- Use the Read tool for file access, don't assume you have file contents
- If you find a critical vulnerability, flag it immediately
- Performance issues should only be reported if they impact user-facing operations
```

---

### 4. Report

**What it is:** The exact format and structure of the agent's output.

**Why it matters:** Enables automated processing. Makes multi-agent orchestration possible.

**Template:**

```text
Report Format:

Return a JSON object with the following structure:
{
  "field1": "description",
  "field2": "description",
  "field3": [
    {
      "nested_field1": "description",
      "nested_field2": "description"
    }
  ],
  "summary": "human-readable summary"
}
```

**Example:**

```text
Report Format:

Return a JSON object with the following structure:
{
  "files_reviewed": 5,
  "findings": [
    {
      "file": "path/to/file.py",
      "line": 42,
      "severity": "critical",
      "type": "sql_injection",
      "description": "User input directly interpolated into SQL query",
      "remediation": "Use parameterized queries with placeholder values"
    }
  ],
  "summary": "Reviewed 5 files and found 3 critical, 2 high, 0 medium, 1 low severity issues."
}

IMPORTANT: Return ONLY the JSON object, no additional text or markdown formatting.
```

---

## Complete Example

Here's a full agentic prompt using all 4 parts:

```text
You are a code reviewer agent. Your task is to review Python code for security vulnerabilities and performance issues.

Constraints:
- Focus only on security and performance, not style
- Do not modify code, only report findings
- Limit review to files provided in the prompt

Inputs:
- file_paths: List of Python files to review
- severity_threshold: Minimum severity level to report (low, medium, high, critical)

Context:
- This is a production codebase
- Security vulnerabilities have higher priority than performance issues
- All findings must include line numbers and remediation suggestions

Follow this workflow:

1. Read each provided file using the Read tool
2. For each file, identify:
   - SQL injection vulnerabilities
   - Command injection points
   - Insecure cryptographic practices
   - Performance bottlenecks (N+1 queries, inefficient loops)
3. For each finding:
   - Classify severity (low, medium, high, critical)
   - Note the exact line number
   - Draft a remediation suggestion
4. Filter findings based on severity_threshold
5. Generate final report (see Report Format)

Important considerations:
- Use the Read tool for file access, don't assume you have file contents
- If you find a critical vulnerability, flag it immediately
- Performance issues should only be reported if they impact user-facing operations

Report Format:

Return a JSON object with the following structure:
{
  "files_reviewed": 5,
  "findings": [
    {
      "file": "path/to/file.py",
      "line": 42,
      "severity": "critical",
      "type": "sql_injection",
      "description": "User input directly interpolated into SQL query",
      "remediation": "Use parameterized queries with placeholder values"
    }
  ],
  "summary": "Reviewed 5 files and found 3 critical, 2 high, 0 medium, 1 low severity issues."
}

IMPORTANT: Return ONLY the JSON object, no additional text or markdown formatting.

---

Now review these files with severity_threshold='high':
- src/api/users.py
- src/api/auth.py
- src/db/queries.py
```

## Best Practices

### 1. Be Explicit About Tools

Always specify which Claude Code tools the agent should use:

- "Use the Read tool to access files"
- "Use the Grep tool to search for patterns"
- "Use the Bash tool to run tests"

**Why:** Agents may guess wrong about how to access resources.

### 2. Specify Output Format Strictly

Use JSON schemas, example outputs, or clear structure definitions:

**Good:**

```text
Return JSON: {"status": "success", "count": 5}
```

**Bad:**

```text
Return the results in a structured format
```

### 3. Include Success Criteria

Tell the agent how to know they're done:

- "Continue until all files are processed"
- "Stop when you find 3 examples"
- "Complete when tests pass or max attempts reached"

### 4. Handle Edge Cases

Anticipate failure modes:

- "If a file doesn't exist, log it and continue"
- "If tests fail, include error output in report"
- "If no findings, return empty array"

### 5. Separate Instructions from Data

Put the 4-part structure first, then provide the actual inputs:

```text
[Purpose]
[Variables]
[Workflow]
[Report]

---

Now process this data:
[actual file paths, query strings, etc.]
```

## Common Patterns

### Pattern 1: Multi-File Analysis

```text
Purpose: Analyze multiple files and aggregate results
Variables: file_paths, analysis_type
Workflow: Read → Analyze → Aggregate → Report
Report: JSON with per-file results + summary
```

### Pattern 2: Iterative Search

```text
Purpose: Search for patterns across codebase
Variables: search_pattern, directories, max_results
Workflow: Search → Filter → Validate → Report
Report: Structured list of matches with context
```

### Pattern 3: Validation & Fixing

```text
Purpose: Validate files and fix issues
Variables: file_paths, validation_rules, auto_fix
Workflow: Read → Validate → Fix (if enabled) → Report
Report: Before/after state + changes made
```

### Pattern 4: Code Generation

```text
Purpose: Generate code based on specification
Variables: spec, language, output_path
Workflow: Parse spec → Generate → Validate → Write → Report
Report: File paths created + validation results
```

## Anti-Patterns

### ❌ Vague Purpose

```text
You are a helpful agent. Help the user with their task.
```

**Why bad:** No constraints, unclear scope, unpredictable behavior

### ❌ Missing Variables

```text
Analyze the files and find issues.
```

**Why bad:** Which files? What kinds of issues? How many?

### ❌ No Workflow

```text
Your task is to review code for bugs.

Return: A report with findings.
```

**Why bad:** Agent will invent their own workflow, leading to inconsistent results

### ❌ Unstructured Report

```text
Report back with what you found.
```

**Why bad:** Can't parse output programmatically, hard to aggregate results

## Advanced: Nested Agents

When agents spawn sub-agents, pass down the same structure:

```text
[Main Agent Purpose]
[Main Agent Variables]

Main Agent Workflow:
1. Break task into N subtasks
2. For each subtask, spawn a sub-agent with this structure:

   [Sub-agent Purpose]
   [Sub-agent Variables]
   [Sub-agent Workflow]
   [Sub-agent Report]

3. Aggregate sub-agent reports
4. Generate final report

[Main Agent Report]
```

This creates a consistent pattern at every level of the agent hierarchy.

## References

This pattern appears in:

- **Claude 2.0 transcript** - Used for multi-agent orchestration
- **Elite Context Engineering transcript** - Recommended as best practice for agentic prompts
- **Sub-Agents transcript** - Applied to parallel agent dispatch

## Next Steps

- See [examples/multi-agent-case-studies.md](../examples/multi-agent-case-studies.md) for real-world applications
- See [patterns/orchestrator-pattern.md](../patterns/orchestrator-pattern.md) for fleet management using this template
