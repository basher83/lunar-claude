---
description: Research multiple topics in parallel using jina-search sub-agents
allowed-tools: Task
argument-hint: [topic1] [topic2] [topic3...]
---

# Parallel Research Command

Research multiple topics simultaneously by spawning parallel jina-search sub-agents.

## Arguments

Topics to research: $ARGUMENTS

## Process

Follow these steps to execute parallel research:

### Step 1: Parse Topics

Split the arguments into individual research topics. Each distinct argument represents one research topic.

### Step 2: Create Sub-Agent Prompts

For each topic, prepare a research prompt:

```sql
Research [topic] and create a comprehensive report.

Focus on:
- Current best practices
- Latest developments and documentation
- Practical implementation guidance
- Authoritative sources

Save findings to docs/research/[topic-slug].md
```

### Step 3: Launch Parallel Sub-Agents

**CRITICAL**: Launch ALL sub-agents in a SINGLE message with multiple Task tool calls.

For each topic, create a Task tool call:
- `subagent_type`: "jina-search"
- `description`: "Research [topic]"
- `prompt`: The research prompt from Step 2

### Step 4: Report Results

After all sub-agents complete, provide a summary:

```markdown
## Parallel Research Complete

**Topics Researched**: [COUNT]

**Reports Generated**:
- docs/research/[topic1-slug].md
- docs/research/[topic2-slug].md
- docs/research/[topic3-slug].md

**Next Steps**:
- Review reports for consistency
- Cross-reference findings across topics
- Synthesize key insights
```

## Examples

**Single topic**:
```text
/parallel-research "React performance optimization"
```

**Multiple topics**:
```text
/parallel-research "React Hooks" "Vue Composition API" "Svelte stores"
```

**Complex topics with spaces**:
```text
/parallel-research "Next.js 14 server components" "Remix data loading patterns" "Astro content collections"
```

## Output

Each sub-agent will create an independent research report in `docs/research/` with comprehensive findings, citations, and actionable recommendations.
