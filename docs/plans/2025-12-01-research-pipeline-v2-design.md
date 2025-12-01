# Research Pipeline v2: Contextual Research Advisor

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Multi-agent research system that finds battle-proven implementations and provides contextual integration advice.

**Architecture:** Slash command dispatches specialized researcher sub-agents in parallel, each with dedicated MCP tools. Reports are cached to build a knowledge base. The orchestrator (main Claude session) synthesizes findings with codebase context to provide integration recommendations.

**Tech Stack:** Claude Code sub-agents, MCP servers (GitHub, Tavily, DeepWiki, Exa), JSON cache

---

**Date:** 2025-12-01
**Status:** Design Complete, Ready for Implementation
**Supersedes:** `2025-11-06-research-pipeline-design.md`

## Executive Summary

This design describes a multi-agent research pipeline invoked via `/lunar-research` that:

1. Dispatches 4 specialized researcher sub-agents in parallel
2. Each agent uses dedicated MCP tools to find relevant implementations
3. Reports are cached to `.claude/research-cache/` building a knowledge base
4. The orchestrator (main Claude session) synthesizes findings with codebase context
5. Produces narrative summaries with integration suggestions

**Key Differentiator:** The orchestrator isn't just a search aggregator—it's a **contextual advisor** that knows your codebase, challenges assumptions with evidence, and suggests integration paths.

## Architecture Overview

```text
User: "Find battle-proven MicroK8s → Proxmox via Ansible implementations"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│           /lunar-research (Slash Command)                   │
│                      ORCHESTRATOR                           │
│                                                             │
│  • Dispatches research agents (Phase 1)                     │
│  • Dispatches synthesizer agent (Phase 2)                   │
│  • Reads synthesis, adds codebase context (Phase 3)         │
│  • MINIMAL CONTEXT - just coordination                      │
└─────────────────────────────────────────────────────────────┘
        │
        │ Phase 1: Parallel research
        ├───────────────────────────────────────────┐
        │           │           │                   │
        ▼           ▼           ▼                   ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐       ┌─────────┐
   │ github  │ │ tavily  │ │deepwiki │       │   exa   │
   │ -agent  │ │ -agent  │ │ -agent  │       │ -agent  │
   └────┬────┘ └────┬────┘ └────┬────┘       └────┬────┘
        │           │           │                   │
        ▼           ▼           ▼                   ▼
   github-      tavily-     deepwiki-           exa-
   report.json  report.json report.json        report.json
        │           │           │                   │
        └───────────┴─────┬─────┴───────────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ Knowledge Base │
                 │ .claude/       │
                 │ research-cache/│
                 │ <query>/       │
                 └───────┬────────┘
                         │
        │ Phase 2: Synthesis
        │                │
        ▼                ▼
   ┌──────────────────────────┐
   │    synthesizer-agent     │
   │                          │
   │  • Reads all 4 reports   │
   │  • Combines findings     │
   │  • Writes synthesis.md   │
   └────────────┬─────────────┘
                │
                ▼
           synthesis.md
                │
        │ Phase 3: Contextualize
        │                │
        ▼                ▼
   ┌──────────────────────────┐
   │    Orchestrator reads    │
   │    synthesis.md, adds    │
   │    codebase integration  │
   │    suggestions           │
   └────────────┬─────────────┘
                │
                ▼
        Final response to user
```

## Key Design Decisions

### Decision 1: Orchestrator = Main Claude Session

**NOT a separate sub-agent.** The slash command runs in the main Claude session, which:
- Has full codebase context
- Can use the Task tool to dispatch sub-agents
- Can synthesize findings with awareness of existing patterns
- Provides contextual recommendations, not just search results

**Critical Constraint:** Sub-agents cannot spawn other sub-agents. Only the main session can orchestrate.

### Decision 2: Parallel Dispatch, Always 4 Agents (MVP)

For MVP, always dispatch all 4 researcher agents in parallel. Future optimization can add intelligent selection based on query type.

**Rationale:** Simpler implementation, comprehensive coverage, parallel execution minimizes latency impact.

### Decision 3: Contextual Advisor, Not Search Aggregator

The synthesis phase is where value is created:

| Search Aggregator | Contextual Advisor |
|-------------------|-------------------|
| "Here are 5 repos" | "Found 3 approaches. Given your existing patterns in X, approach Y aligns best because..." |
| Raw results | Evidence-based recommendations |
| User figures it out | Claude guides integration |

### Decision 4: Knowledge Base by Default

Every research run contributes to `.claude/research-cache/`. Over time:
- Similar queries can leverage cached findings
- Tags enable discovery across research runs
- Avoids re-researching the same topics

## Component Specifications

### 1. Slash Command: `/lunar-research`

**Location:** `.claude/commands/lunar-research.md`

**Invocation:**
- User: `/lunar-research <query>`
- Claude: Can invoke via SlashCommand tool when research would help

**Responsibilities:**
1. Parse the research query
2. Dispatch 4 researcher sub-agents in parallel via Task tool
3. Collect reports from all agents
4. Cache combined findings to knowledge base
5. Synthesize findings with codebase context
6. Return narrative summary + integration suggestions

**Slash Command Structure:**

```markdown
---
description: Research implementations, patterns, and best practices across multiple sources
arguments:
  - name: query
    description: What to research (e.g., "MicroK8s deployment to Proxmox via Ansible")
    required: true
---

# Lunar Research

[Orchestration instructions here]
```

### 2. Researcher Sub-Agents

Each researcher is a specialized sub-agent with:
- Dedicated MCP tools for its data source
- Read/Write/Edit tools for documentation
- Standardized report format output

#### 2.1 GitHub Researcher (`github-agent.md`)

**Location:** `.claude/agents/research/github-agent.md`

**Tools:**
- GitHub MCP tools (search repos, read files, fetch issues)
- Read, Write, Edit (for documenting findings)

**Specialization:**
- Finding repositories with implementations
- Analyzing code patterns and structure
- Extracting from README, issues, discussions
- Assessing project maturity (stars, activity, maintenance)

**Best For:**
- "How do others implement X?"
- Finding battle-tested code examples
- Discovering common patterns in real projects

#### 2.2 Tavily Researcher (`tavily-agent.md`)

**Location:** `.claude/agents/research/tavily-agent.md`

**Tools:**
- Tavily MCP tools (web search, extract)
- Read, Write, Edit

**Specialization:**
- Recent blog posts and tutorials
- Community discussions and guides
- Current best practices and trends
- Comparative analyses

**Best For:**
- "What's the recommended way to do X in 2024?"
- Finding tutorials and walkthroughs
- Recent developments and changes

#### 2.3 DeepWiki Researcher (`deepwiki-agent.md`)

**Location:** `.claude/agents/research/deepwiki-agent.md`

**Tools:**
- DeepWiki MCP tools (read_wiki_structure, read_wiki_contents, ask_question)
- Read, Write, Edit

**Specialization:**
- Official documentation understanding
- Architecture and design documentation
- API references and specifications
- Project structure analysis

**Best For:**
- "How does X work officially?"
- Understanding project architecture
- API and configuration details

#### 2.4 Exa Researcher (`exa-agent.md`)

**Location:** `.claude/agents/research/exa-agent.md`

**Tools:**
- Exa MCP tools (semantic search, find similar)
- Read, Write, Edit

**Specialization:**
- Semantic/conceptual search
- Finding similar implementations
- Discovering related technologies
- Academic and technical papers

**Best For:**
- "What's similar to X?"
- Finding alternatives and comparisons
- Technical deep-dives

#### 2.5 Synthesizer Agent (`synthesizer-agent.md`)

**Location:** `.claude/agents/research/synthesizer-agent.md`

**Tools:**
- Read (to read all researcher reports)
- Write (to write synthesis.md)
- Edit

**Purpose:**
Combines findings from all 4 researcher reports into a unified synthesis document. This keeps the orchestrator's context clean by offloading the heavy lifting of report combination.

**Responsibilities:**
1. Read all 4 researcher reports from the cache directory
2. Identify common findings across sources
3. Resolve conflicts between sources (official docs > community > blogs)
4. Aggregate patterns, gotchas, and alternatives
5. Calculate overall confidence based on source agreement
6. Write structured `synthesis.md` to cache directory

**Output:** `synthesis.md` containing:
- Executive summary
- Recommended approach with evidence
- Aggregated patterns from all sources
- Combined gotchas and warnings
- Alternatives considered
- Source citations

**Why a Separate Agent:**
- Keeps orchestrator context minimal (just coordination)
- Single responsibility: combine reports, nothing else
- Can be improved independently of research or orchestration
- Heavy text processing doesn't bloat orchestrator

### 3. Report Format Schema

Standardized JSON format for all researcher reports:

```json
{
  "researcher": "github",
  "query": "MicroK8s Proxmox Ansible deployment",
  "timestamp": "2025-12-01T10:30:00Z",

  "confidence": 0.85,
  "completeness": "partial",

  "sources": [
    {
      "url": "https://github.com/example/microk8s-proxmox",
      "title": "MicroK8s Proxmox Ansible Deployment",
      "type": "repository",
      "relevance": "high",
      "metadata": {
        "stars": 234,
        "last_updated": "2024-10-15",
        "language": "YAML"
      }
    }
  ],

  "findings": {
    "implementations": [
      {
        "name": "microk8s-proxmox-ansible",
        "url": "https://github.com/...",
        "approach": "Uses cloud-init templates + Ansible roles for MicroK8s installation",
        "maturity": "production",
        "evidence": "234 stars, 50+ forks, active maintenance, used by 3 companies per README"
      }
    ],
    "patterns": [
      "Cloud-init for initial VM provisioning before Ansible runs",
      "Separate roles: proxmox_vm, microk8s_install, microk8s_addons",
      "Inventory generated dynamically from Proxmox API"
    ],
    "gotchas": [
      "MicroK8s requires br_netfilter kernel module - must enable in cloud-init",
      "Proxmox API token auth preferred over password for automation",
      "MicroK8s clustering requires specific port ranges opened"
    ],
    "alternatives": [
      "K3s lighter weight but less addon ecosystem",
      "RKE2 more enterprise but heavier setup"
    ]
  },

  "gaps": [
    "No HA cluster examples found",
    "Missing CEPH storage integration patterns"
  ],

  "summary": "Found 3 battle-tested repos for MicroK8s on Proxmox. Best candidate is X due to active maintenance and comprehensive role structure. Key insight: cloud-init pre-provisioning is essential pattern.",

  "tags": ["microk8s", "proxmox", "ansible", "kubernetes", "cloud-init", "homelab"]
}
```

**Field Definitions:**

| Field | Type | Purpose |
|-------|------|---------|
| `researcher` | string | Which agent produced this report |
| `query` | string | Original research query |
| `timestamp` | ISO8601 | When research was conducted |
| `confidence` | float 0-1 | Agent's confidence in findings |
| `completeness` | enum | "none" / "partial" / "comprehensive" |
| `sources[]` | array | Traceable citations with metadata |
| `findings.implementations[]` | array | Specific repos/solutions found |
| `findings.patterns[]` | array | Extracted reusable patterns |
| `findings.gotchas[]` | array | Pain points and warnings |
| `findings.alternatives[]` | array | Other approaches considered |
| `gaps` | array | What couldn't be found |
| `summary` | string | Agent's synthesis of findings |
| `tags` | array | Semantic indexing for knowledge base |

### 4. Knowledge Base

**Location:** `.claude/research-cache/`

**Structure:**

```bash
.claude/research-cache/
├── index.json                           # Query index for discovery
├── microk8s-proxmox-ansible/
│   ├── research.json                    # Combined findings from all agents
│   ├── github-report.json               # Individual agent report
│   ├── tavily-report.json
│   ├── deepwiki-report.json
│   └── exa-report.json
└── terraform-aws-eks/
    ├── research.json
    └── [agent reports...]
```

**Index Schema (`index.json`):**

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "microk8s-proxmox-ansible",
      "query": "MicroK8s deployment to Proxmox via Ansible",
      "timestamp": "2025-12-01T10:30:00Z",
      "tags": ["microk8s", "proxmox", "ansible", "kubernetes"],
      "confidence": 0.85,
      "path": "microk8s-proxmox-ansible/research.json"
    }
  ]
}
```

**Cache Lookup Logic:**
1. Check index for matching tags or similar query
2. If found and < 30 days old, offer to reuse
3. If found but stale, offer to refresh
4. If not found, conduct new research

### 5. Synthesis Output

The orchestrator produces a narrative response with:

1. **Executive Summary:** What was found across all sources
2. **Recommended Approach:** Best option with evidence
3. **Integration Suggestions:** How findings relate to existing codebase
4. **Alternatives Considered:** Other options and why not recommended
5. **Gotchas to Avoid:** Aggregated warnings from all sources
6. **Next Steps:** Concrete actions the user can take

**Example Output:**

```markdown
## Research Findings: MicroK8s on Proxmox via Ansible

### Summary
Found 7 relevant implementations across GitHub, 12 blog tutorials via Tavily,
and comprehensive MicroK8s docs via DeepWiki. Confidence: High (0.87).

### Recommended Approach
**Repository:** `github.com/example/microk8s-proxmox-ansible`
- 234 stars, actively maintained, production-tested
- Uses cloud-init + Ansible roles pattern
- Aligns with your existing `proxmox-infrastructure` plugin patterns

### Integration with Your Codebase
Looking at your `plugins/infrastructure/` structure:
1. The role structure matches your `role-structure-standards.md`
2. Their cloud-init approach complements your existing templates
3. Consider adding to `proxmox-infrastructure` skill as new workflow

### Gotchas to Avoid
- Enable `br_netfilter` kernel module in cloud-init (3 repos hit this)
- Use API tokens, not passwords, for Proxmox auth
- MicroK8s clustering needs ports 25000, 16443, 12379 open

### Alternatives Considered
- **K3s:** Lighter but less addon ecosystem - not recommended given your
  existing MicroK8s patterns
- **RKE2:** Enterprise-grade but overkill for homelab scale

### Next Steps
1. Clone recommended repo as reference
2. Adapt roles to match your structure
3. Add as new workflow in `proxmox-infrastructure` skill
```

## Implementation Phases

### Phase 1: Foundation (Tasks 1-4)

1. Create report format schema as JSON Schema file
2. Create slash command skeleton `/lunar-research`
3. Create first researcher agent (github-agent) as template
4. Test single-agent dispatch and report collection

### Phase 2: Full Research Pipeline (Tasks 5-8)

5. Create remaining researcher agents (tavily, deepwiki, exa)
6. Implement parallel dispatch in slash command
7. Implement report collection and caching
8. Create knowledge base index management

### Phase 3: Synthesis (Tasks 9-11)

9. Implement report aggregation logic
10. Implement contextual synthesis with codebase awareness
11. Format and return narrative output

### Phase 4: Polish (Tasks 12-14)

12. Add cache lookup and reuse logic
13. Add progress reporting during research
14. Testing and refinement

## File Manifest

Files to create:

| Path | Type | Purpose |
|------|------|---------|
| `.claude/commands/lunar-research.md` | Slash Command | Orchestration entry point |
| `.claude/agents/research/github-agent.md` | Sub-agent | GitHub MCP researcher |
| `.claude/agents/research/tavily-agent.md` | Sub-agent | Tavily MCP researcher |
| `.claude/agents/research/deepwiki-agent.md` | Sub-agent | DeepWiki MCP researcher |
| `.claude/agents/research/exa-agent.md` | Sub-agent | Exa MCP researcher |
| `.claude/agents/research/synthesizer-agent.md` | Sub-agent | Combines reports into synthesis |
| `.claude/schemas/research-report.json` | JSON Schema | Report format validation |
| `.claude/research-cache/index.json` | Data | Knowledge base index |

## Success Criteria

The implementation is successful when:

1. **Research works:** `/lunar-research "topic"` dispatches all 4 agents and collects reports
2. **Reports are consistent:** All agents produce valid reports matching the schema
3. **Caching works:** Findings are stored and indexed in knowledge base
4. **Synthesis is contextual:** Output references relevant existing codebase patterns
5. **Integration suggestions are actionable:** User can follow recommendations directly
6. **Knowledge base grows:** Repeated research builds discoverable cache

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Orchestrator architecture | Main Claude session, not sub-agent |
| Slash command name | `/lunar-research` |
| Agent selection strategy | All 4 always (MVP), smart selection (future) |
| Sub-agent tools | MCP + Read/Write/Edit |
| Cache location | `.claude/research-cache/` |
| Synthesis output | Narrative + integration suggestions |

## References

- **Previous Design:** `docs/plans/2025-11-06-research-pipeline-design.md`
- **Design Feedback:** `docs/plans/2025-11-06-research-pipeline-design-feedback.md`
- **Multi-Agent Patterns:** `multi-agent-composition` skill
- **Sub-Agent Docs:** Claude Code official documentation

---

**This design captures the refined vision from the 2025-12-01 planning session. It supersedes the original 2025-11-06 design with clarified architecture (orchestrator = main session), concrete component specifications, and a clear implementation path.**
