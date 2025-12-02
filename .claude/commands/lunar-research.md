---
description: Research implementations, patterns, and best practices across multiple sources
allowed-tools: Task, Read, Write, Edit, Glob, Grep
argument-hint: [query]
---

# Lunar Research

**Purpose:** Orchestrator for 3-tier research pipeline. COORDINATION ONLY - dispatch agents, don't research yourself.

## Step 0: Check Knowledge Base

🔍 Checking knowledge base...

1. Read `.claude/research-cache/index.json`
2. Check for matching entries less than 30 days old
3. If found: Ask user "Reuse existing research, refresh it, or start new?"
4. If reuse: Skip to Phase 3

## Phase 1: Dispatch Researchers

🚀 Dispatching 4 researcher agents...

1. **Normalize query to directory name:**
   - Convert query to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Example: "Python CLI best practices" → "python-cli-best-practices"

2. **Create cache directory:**
   ```bash
   mkdir -p .claude/research-cache/[normalized-query]
   ```

3. **Dispatch ALL 4 researchers in SINGLE message:**

   Use Task tool to dispatch all 4 agents in parallel (single message, multiple Task calls):

   **GitHub Researcher:**
   ```text
   Research: [query]
   Cache dir: .claude/research-cache/[normalized-query]
   Output: github-report.json
   ```

   **Tavily Researcher:**
   ```text
   Research: [query]
   Cache dir: .claude/research-cache/[normalized-query]
   Output: tavily-report.json
   ```

   **DeepWiki Researcher:**
   ```text
   Research: [query]
   Cache dir: .claude/research-cache/[normalized-query]
   Output: deepwiki-report.json
   ```

   **Exa Researcher:**
   ```text
   Research: [query]
   Cache dir: .claude/research-cache/[normalized-query]
   Output: exa-report.json
   ```

4. **Progress indicators:**
   - After each completes: "✓ [agent-name] complete"

## Phase 2: Dispatch Synthesizer

🔄 Synthesizing findings...

1. **Wait for all 4 researchers to complete**

2. **Dispatch synthesizer agent:**
   ```text
   Cache dir: .claude/research-cache/[normalized-query]
   Query: [query]
   ```

3. **Progress indicator:**
   - "✓ Synthesis complete"

## Phase 3: Contextualize and Respond

🧠 Adding codebase context...

1. **Read synthesis:**
   - Read `.claude/research-cache/[normalized-query]/synthesis.md`

2. **Check for related patterns in codebase:**
   - Use Glob to search `plugins/` for related implementations
   - Use Grep to search for related patterns in existing code
   - Identify integration opportunities

3. **Update knowledge base index:**
   - Add new entry to `.claude/research-cache/index.json` with:
     - query
     - normalized directory name
     - timestamp
     - tags (extracted from synthesis)
     - confidence (from synthesis)

4. **Respond to user:**
   - Present synthesis findings
   - Add codebase-specific integration suggestions
   - Highlight relevant existing patterns in plugins/
   - Suggest next steps for implementation

## Orchestration Rules

**CRITICAL:**

1. **You are the orchestrator, not the researcher**
   - Dispatch agents using Task tool
   - Do NOT do research yourself
   - Do NOT call MCP tools directly

2. **Phase 1: Parallel execution**
   - ALL 4 researchers in SINGLE message
   - Use 4 separate Task tool calls in one response
   - Do NOT wait between dispatches

3. **Phase 2: Sequential after Phase 1**
   - Synthesizer ONLY after all 4 researchers complete
   - Single Task tool call for synthesizer

4. **Phase 3: You add value**
   - Read the synthesis
   - Add codebase context (this is YOUR job)
   - Provide integration advice
   - Update knowledge base

## Error Handling

- If a researcher fails: Note it in response, continue with available reports
- If synthesizer fails: Check all 4 reports exist, retry once
- If cache directory exists: Ask user if they want to overwrite or use existing
