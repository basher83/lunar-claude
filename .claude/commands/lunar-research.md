---
description: Research implementations, patterns, and best practices across multiple sources
allowed-tools: Task, Read, Write, Edit, Glob, Grep
argument-hint: [query]
---

# Lunar Research

Multi-agent research pipeline orchestrator. You coordinate 4 specialized researcher agents and a synthesizer to provide comprehensive research findings.

**IMPORTANT:** You are a COORDINATOR. Dispatch agents to do research - do not research yourself.

## Step 0: Check Knowledge Base

Output: `🔍 Checking knowledge base...`

1. Read `.claude/research-cache/index.json`
2. Search for entries matching the query (fuzzy match on query and tags)
3. Check if any matching entry is less than 30 days old

**If found:**

- Show the user: "Found existing research from [date]. Options:"
  - `reuse` - Use cached results (skip to Phase 3)
  - `refresh` - Update with new research
  - `new` - Start fresh research

**If not found or user chooses refresh/new:** Continue to Phase 1

## Phase 1: Dispatch Researchers

Output: `🚀 Dispatching 4 researcher agents...`

1. **Normalize query to directory name:**
   - Lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Example: "Python CLI best practices" → "python-cli-best-practices"

2. **Create cache directory:**
   - Path: `.claude/research-cache/[normalized-query]/`
   - Create if it doesn't exist

3. **Dispatch ALL 4 researchers in a SINGLE message:**

   Use the Task tool 4 times in ONE message. For each researcher:

   **GitHub Researcher:**
   - `subagent_type`: `github-researcher`
   - `description`: `GitHub research for [query]`
   - `prompt`:

     ```text
     Research: [query]
     Cache directory: .claude/research-cache/[normalized-query]/
     Output file: github-report.json
     ```

   **Tavily Researcher:**
   - `subagent_type`: `tavily-researcher`
   - `description`: `Tavily research for [query]`
   - `prompt`:

     ```text
     Research: [query]
     Cache directory: .claude/research-cache/[normalized-query]/
     Output file: tavily-report.json
     ```

   **DeepWiki Researcher:**
   - `subagent_type`: `deepwiki-researcher`
   - `description`: `DeepWiki research for [query]`
   - `prompt`:

     ```text
     Research: [query]
     Cache directory: .claude/research-cache/[normalized-query]/
     Output file: deepwiki-report.json
     ```

   **Exa Researcher:**
   - `subagent_type`: `exa-researcher`
   - `description`: `Exa research for [query]`
   - `prompt`:

     ```text
     Research: [query]
     Cache directory: .claude/research-cache/[normalized-query]/
     Output file: exa-report.json
     ```

4. **After each completes:** Output `✓ [agent name] complete`

## Phase 2: Dispatch Synthesizer

Output: `🔄 Synthesizing findings...`

1. Dispatch the synthesizer agent:
   - `subagent_type`: `synthesizer-agent`
   - `description`: `Synthesize research for [query]`
   - `prompt`:

     ```text
     Query: [query]
     Cache directory: .claude/research-cache/[normalized-query]/
     ```

2. Output: `✓ Synthesis complete`

## Phase 3: Contextualize and Respond

Output: `🧠 Adding codebase context...`

1. **Read synthesis:** Load `.claude/research-cache/[normalized-query]/synthesis.md`

2. **Check for related patterns in codebase:**
   - Search `plugins/` for related implementations
   - Look for similar patterns in existing code
   - Note any relevant existing infrastructure

3. **Update knowledge base index:**
   - Add entry to `.claude/research-cache/index.json`:

   ```json
   {
     "query": "[original query]",
     "normalizedQuery": "[normalized-query]",
     "timestamp": "[ISO timestamp]",
     "path": ".claude/research-cache/[normalized-query]/",
     "tags": ["extracted", "from", "synthesis"],
     "confidence": [from synthesis]
   }
   ```

4. **Respond to user with:**
   - The synthesis content
   - Codebase integration suggestions based on what you found in `plugins/`
   - Recommendations for next steps

## Orchestration Rules

1. **Dispatch agents - don't research yourself**
   - You call the Task tool, agents do the work
   - Do not use search tools directly

2. **Phase 1: ALL 4 researchers in SINGLE message**
   - This enables parallel execution
   - Do not wait for one before dispatching others

3. **Phase 2: Synthesizer AFTER all researchers complete**
   - Wait for all 4 reports before synthesizing
   - Synthesizer needs all inputs

4. **Phase 3: YOU add codebase context**
   - This is the only phase where you do work directly
   - Read files, search codebase, provide integration advice

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
