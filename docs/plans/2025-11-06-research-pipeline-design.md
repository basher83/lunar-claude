# Research Pipeline: Meta-Learning System for Claude Code

**Date:** 2025-11-06
**Status:** Design Phase
**Purpose:** Create a reusable system that researches tools/repositories and generates expert-level knowledge artifacts for Claude Code

## Executive Summary

This design describes a multi-agent research pipeline that accepts a GitHub repository (or other research target) as input, conducts comprehensive multi-layered research, and produces structured knowledge artifacts in multiple formats (Skills, developer onboarding docs, API references, tutorials, etc.).

The system uses an intelligent orchestrator to manage specialized research agents, caches findings for reuse, and supports pluggable documentation generators for different output types.

## The Problem

Claude Code frequently encounters new tools, libraries, frameworks, and repositories that it needs to understand and leverage effectively. Currently, this understanding must be built from scratch in each session, leading to:

- Repeated research effort across sessions
- Inconsistent depth of understanding
- No persistent knowledge artifacts
- Limited ability to share learnings across the community

## The Vision

A system where you can say:

```sql
"Research jina-ai/MCP and create a skill and dev onboarding guide"
```

And the system:
1. Orchestrates specialized research agents (DeepWiki, Firecrawl, GitHub, Web Search)
2. Conducts comprehensive research across multiple dimensions
3. Caches findings for reuse
4. Generates multiple output formats (Skill + Onboarding guide) from one research run
5. Produces expert-level knowledge artifacts ready for immediate use

Or you can research now, generate docs later:

```text
"Research terraform-providers/aws"     # Research only, cache results
[Later...]
"Generate skill from terraform-providers/aws research"
"Generate API reference from terraform-providers/aws research"
```

## Core Architecture

### High-Level Flow

```sql
User Request
    ↓
┌───────────────────────────────────┐
│   Orchestrator (Manager)          │
│   • Parse intent & target         │
│   • Select researchers            │
│   • Manage research workflow      │
│   • Decide when enough info       │
└───────────┬───────────────────────┘
            │
   ┌────────┼─────────┬─────────┐
   ▼        ▼         ▼         ▼
┌────────┐┌────────┐┌────────┐┌────────┐
│DeepWiki││Firecrawl││ GitHub ││  Web   │
│Research││Research││Research││ Search │
│        ││        ││        ││Research│
│MCP:    ││MCP:    ││MCP: gh ││MCP:    │
│deepwiki││firecrawl││Tools:  ││firecrawl│
│        ││        ││Read    ││        │
└───┬────┘└───┬────┘└───┬────┘└───┬────┘
    │         │         │         │
    └─────────┴────┬────┴─────────┘
                   │
          ┌────────▼─────────┐
          │ Research Findings │
          │ (Cached)          │
          └────────┬──────────┘
                   │
          ┌────────▼─────────┐
          │  Intent Router    │
          │  (Based on output │
          │   type requested) │
          └────────┬──────────┘
                   │
   ┌───────────────┼────────────┬─────────┐
   ▼               ▼            ▼         ▼
┌────────┐   ┌──────────┐  ┌────────┐┌─────────┐
│ Skill  │   │Dev Docs  │  │  API   ││Tutorial │
│Document│   │Documenter│  │Ref Doc ││Document │
└───┬────┘   └────┬─────┘  └───┬────┘└────┬────┘
    │             │            │          │
    ▼             ▼            ▼          ▼
SKILL.md   ONBOARDING.md  API_REF.md  TUTORIAL.md
```

### Component Breakdown

#### 1. Orchestrator (Manager Agent)

**Role:** Intelligent coordination and decision-making

**Responsibilities:**
- Parse user intent (what research target, what outputs)
- Select which researchers to deploy based on target type and output needs
- Evaluate researcher reports and decide if more research is needed
- Determine when research is sufficient for requested outputs
- Route cached findings to appropriate documenter(s)

**Intelligence Model:** LLM-driven (not hardcoded rules)

**Why LLM-driven:**
- Can adapt to unexpected situations
- Can re-task researchers mid-flight based on findings
- Can handle edge cases we didn't anticipate
- Makes the system extensible without code changes
- If we wanted hardcoded rules, we'd just write a Python script

**Example Decision Flow:**
```bash
Orchestrator receives: "Research jina-ai/MCP, output: skill"
    ↓
Analyzes target: GitHub repo
Analyzes output: Skill (needs architecture, API, patterns, best practices)
    ↓
Deploys: DeepWiki, GitHub, Firecrawl researchers
    ↓
DeepWiki reports: "Found architecture docs, confidence: 0.9"
GitHub reports: "Found examples, confidence: 0.7, gaps: no test patterns"
Firecrawl reports: "Found blog posts with usage patterns, confidence: 0.6"
    ↓
Orchestrator evaluates: "Sufficient for skill generation"
    ↓
Routes to: Skill Documenter
```

**Alternative scenario with re-tasking:**
```text
Orchestrator receives: "Research obscure-tool/cli, output: dev docs"
    ↓
Deploys: DeepWiki, GitHub researchers
    ↓
DeepWiki reports: "No documentation found, confidence: 0.0"
GitHub reports: "Repo has minimal README, confidence: 0.3"
    ↓
Orchestrator evaluates: "Insufficient, need more sources"
    ↓
Deploys: Web Search, Firecrawl to find community resources
    ↓
Continues until sufficient information gathered
```

#### 2. Research Agents (Specialized Sub-Agents)

**Design Principle:** Each researcher is a purpose-built specialist with NO knowledge of other researchers and NO orchestration authority.

**Core Researchers (MVP):**

##### DeepWiki Researcher
- **Tool:** DeepWiki MCP
- **Specialty:** Official documentation, wikis, structured knowledge
- **Best for:** Architecture, API specs, official guides

##### Firecrawl Researcher
- **Tool:** Firecrawl MCP
- **Specialty:** Web scraping, blog posts, tutorials, community content
- **Best for:** Usage patterns, real-world examples, community knowledge

##### GitHub Researcher
- **Tool:** GitHub MCP + Read file tools
- **Specialty:** Source code, examples, tests, issues, discussions
- **Best for:** Code patterns, test strategies, implementation details

##### Web Search Researcher
- **Tool:** Firecrawl MCP (search capability)
- **Specialty:** Broad web search, finding scattered resources
- **Best for:** Community articles, Stack Overflow, comparative analysis

**Researcher Reporting Protocol:**

Each researcher returns **hybrid format** (structured metadata + prose findings):

```json
{
  "researcher": "deepwiki",
  "confidence": 0.85,
  "completeness": "partial",
  "findings": {
    "architecture": "Found detailed component diagrams showing...",
    "api_surface": "Comprehensive API documentation with...",
    "usage_patterns": "Minimal examples in official docs..."
  },
  "gaps": [
    "No API examples found in documentation",
    "No real-world usage patterns documented",
    "Testing strategies not covered"
  ]
}
```

**Critical Constraint:** Researchers report ONLY what they found and what's missing from their perspective. They do NOT:
- Recommend which other researchers to deploy
- Make orchestration decisions
- Have knowledge of what other researchers found

**Why:** Separation of concerns. Researchers are domain experts with single-perspective knowledge. The orchestrator has full context and orchestration authority.

#### 3. Research Cache

**Purpose:** Store research findings for reuse across multiple documentation outputs

**Storage:** Project-specific directory (MVP)
- Location: `.claude/research-cache/<normalized-target-name>.json`
- Format: JSON with metadata + findings from all researchers
- Benefits:
  - Git-committable
  - Shareable with team
  - Easy to inspect/debug

**Cache Structure:**
```json
{
  "target": "jina-ai/MCP",
  "timestamp": "2025-11-06T23:45:00Z",
  "researchers": {
    "deepwiki": { ... },
    "github": { ... },
    "firecrawl": { ... }
  },
  "metadata": {
    "orchestrator_assessment": "comprehensive",
    "research_dimensions_covered": [
      "architecture",
      "api_surface",
      "usage_patterns",
      "best_practices"
    ]
  }
}
```

**Future Roadmap:** RAG database for semantic search (v2+)

#### 4. Documenter Agents (Specialized Sub-Agents)

**Design Principle:** Each documenter is a completely separate sub-agent with a single purpose.

**Why Separate Agents (Not Variants):**

From multi-agent-composition principles:
- **Don't force context switching:** Each documenter has fundamentally different context needs
- **Single purpose:** A Skill documenter writes SKILL.md files. A Dev Docs documenter writes onboarding guides. Period.
- **Different prompts:** Each documenter needs unique instructions, examples, and success criteria
- **Scalability:** Easy to add new documenter types without affecting existing ones

**Core Documenters (MVP):**

##### Skill Documenter
- **Output:** Complete Skill structure (SKILL.md + supporting subdirectories)
- **Context Needed:** SKILL.md spec, progressive disclosure patterns, trigger descriptions
- **May leverage:** skill-creator skill for structure/validation
- **Output Location:** TBD (see open questions)

##### Dev Onboarding Documenter
- **Output:** Developer onboarding guide
- **Context Needed:** Onboarding best practices, quickstart patterns, common pitfalls
- **Focus:** Getting developers productive quickly

**Future Documenters:**
- API Reference Documenter
- Tutorial Documenter
- Architecture Diagram Documenter
- Troubleshooting Guide Documenter

**Documenter Input:** Receives cached research findings + output format specification

**Documenter Output:** Structured documentation artifact ready for use

## Research Dimensions

The system aims for **expert-level understanding** across all critical dimensions:

1. **Architecture & Code Structure**
   - Entry points, module organization, key abstractions
   - Data flow, component interactions
   - Design patterns and architectural decisions

2. **Usage Patterns & Examples**
   - How developers actually use the tool
   - Common patterns and workflows
   - Real-world examples from production code

3. **API Surface & Contracts**
   - Public interfaces and method signatures
   - Configuration options and parameters
   - Input/output contracts

4. **Best Practices & Gotchas**
   - Anti-patterns to avoid
   - Common mistakes and how to prevent them
   - Performance considerations and optimization

5. **Testing & Validation**
   - How to verify correct usage
   - Testing strategies and patterns
   - Debugging approaches

6. **Ecosystem & Integration**
   - Dependencies and requirements
   - How it fits with other tools
   - Common integration patterns

## Key Design Decisions and Reasoning

### Decision 1: LLM-Driven Orchestrator (Not Hardcoded Rules)

**Rationale:**
- The value proposition is intelligent orchestration
- Hardcoded rules = might as well write a Python script
- LLM can adapt, re-task, handle edge cases
- Overhead is tiny compared to research work itself
- "Unpredictability" is actually intelligent adaptation

**Trade-off:** Slight overhead and less deterministic behavior, but massive flexibility gain

### Decision 2: Researchers Have No Cross-Agent Knowledge

**Rationale:**
- Researchers are purpose-built specialists
- They have no orchestration authority
- They report findings and gaps from their perspective only
- Orchestrator has full context and makes decisions

**Why This Matters:** Prevents architectural violations where researchers try to coordinate or make decisions outside their domain

### Decision 3: Hybrid Reporting Format (Structured + Prose)

**Rationale:**
- Structured metadata helps orchestrator make decisions (confidence, completeness, gaps)
- Prose findings preserve nuance and context
- Documenter agents need rich prose to create quality output
- Best of both worlds

### Decision 4: Separate Documenter Sub-Agents

**Rationale (from multi-agent-composition):**
- Each documenter has fundamentally different context needs (SKILL.md spec vs onboarding best practices)
- Different prompts = different agent capabilities
- Don't force context switching in a single agent
- Single purpose principle: one agent, one job

### Decision 5: Two-Mode Operation (Full Pipeline + Research-Then-Generate)

**Rationale:**
- Flexibility: sometimes you know what you need now, sometimes you don't
- Research caching enables one research run → multiple outputs
- Can add new documenters later and regenerate from cached research
- Prevents repeated research work

**Example Scenarios:**

**Scenario 1: Full Pipeline**
```bash
Input: "Create skill and dev docs for jina-ai/MCP"
Flow: Orchestrator → Research (cached) → [Skill + Dev Docs] parallel → Done
Output: SKILL.md + ONBOARDING.md
```

**Scenario 2: Research Now, Docs Later**
```text
Session 1:
Input: "Research jina-ai/MCP"
Flow: Orchestrator → Research → Cache → Done

Session 2 (later):
Input: "Generate skill from jina-ai/MCP research"
Flow: Load cache → Skill Documenter → SKILL.md

Session 3 (even later):
Input: "Generate API reference from jina-ai/MCP research"
Flow: Load cache → API Ref Documenter → API_REF.md
```

**Scenario 3: New Documenter Type**
```text
[6 months later, build Tutorial Documenter]
Input: "Generate tutorial from jina-ai/MCP research"
Flow: Load cache → Tutorial Documenter → TUTORIAL.md
```

### Decision 6: Project-Specific Cache (MVP)

**Rationale:**
- Simple to implement and debug
- Git-committable and shareable
- No external dependencies
- Good enough for MVP

**Future:** RAG database for semantic search, versioning, staleness detection (v2+)

## Multi-Agent Composition Principles Applied

This design directly applies principles from the `multi-agent-composition` skill:

### Core 4 Framework
- **Context:** Each agent (orchestrator, researchers, documenters) has precisely the context it needs
- **Model:** LLM capabilities enable intelligent orchestration vs hardcoded logic
- **Prompt:** Each agent has specialized prompts for its purpose
- **Tools:** Researchers have MCP tools; documenters have file writing tools

### Orchestrator Pattern
- Master orchestrator (Manager) coordinates specialized agents
- Researchers report findings, orchestrator decides next steps
- Matches "scout-builder" pattern: scouts research, orchestrator builds strategy

### Context Window Protection
- "Don't force your agent to context switch"
- Each researcher: single purpose (DeepWiki = docs, GitHub = code)
- Each documenter: single purpose (Skill writer ≠ Dev docs writer)
- Delete agents when done, treat as temporary resources

### Parallelization
- "Parallel = Sub-Agents"
- Multiple researchers can run simultaneously
- Multiple documenters can run simultaneously
- Nothing else in Claude Code supports parallel execution

### Single Purpose Agents
- Researchers: domain experts, no orchestration authority
- Documenters: output specialists, no research capability
- Orchestrator: coordination only, no research or documentation

## Critical Insights from Brainstorming

### Insight 1: Not Limited to GitHub Repos
Initially framed as "research GitHub repos," but the architecture supports ANY research target:
- GitHub repositories
- Blog posts and tutorials
- Documentation websites
- Tools with scattered resources
- Comparative analysis (tool A vs tool B)

The orchestrator selects appropriate researchers based on target type.

### Insight 2: Research Once, Infinite Outputs
The caching layer decouples research from documentation:
- Research is expensive and comprehensive
- Documentation generation is cheap and specialized
- One research run can generate unlimited output types
- New documenter types can leverage existing cached research

This dramatically changes the value proposition.

### Insight 3: Extensibility Without Code Changes
Because the orchestrator is LLM-driven:
- Add new researcher → orchestrator learns to use it
- Add new documenter → orchestrator learns to route to it
- No hardcoded rules to update
- System grows organically

### Insight 4: Researchers Must Not Coordinate
A critical architectural constraint: researchers have no knowledge of each other and no orchestration authority.

**Wrong:**
```json
{
  "researcher": "deepwiki",
  "recommendation": "Deploy GitHub researcher to find examples"
}
```

**Right:**
```json
{
  "researcher": "deepwiki",
  "gaps": ["No examples found in documentation"]
}
```

The orchestrator reads the gaps and decides to deploy GitHub researcher.

## MVP Scope

### In Scope for MVP

**Orchestrator:**
- Parse user intent (target + output types)
- Select researchers based on target type
- Evaluate researcher reports
- Decide when research is sufficient
- Route to appropriate documenters

**Researchers:**
- DeepWiki Researcher (MCP)
- Firecrawl Researcher (MCP)
- GitHub Researcher (MCP + file tools)
- Web Search Researcher (Firecrawl search)

**Documenters:**
- Skill Documenter
- Dev Onboarding Documenter

**Cache:**
- Project-specific JSON files
- Store/retrieve research findings
- Basic metadata (timestamp, target, researchers used)

**Modes:**
- Full pipeline (research + generate in one go)
- Two-step (research now, generate later)

### Out of Scope for MVP

**Advanced caching:**
- Staleness detection
- Version tracking
- RAG database integration
- Semantic search

**Advanced researchers:**
- Stack Overflow researcher
- Reddit/community researcher
- Video content researcher
- Documentation diff researcher (version changes)

**Advanced documenters:**
- API Reference Documenter
- Tutorial Documenter
- Architecture Diagram Documenter
- Troubleshooting Guide Documenter
- Migration Guide Documenter

**Error handling:**
- Researcher retry logic
- Fallback strategies
- Partial research recovery

**Observability:**
- Hooks for monitoring
- Progress tracking
- Cost estimation

## Future Roadmap

### v2: Advanced Caching & Intelligence
- RAG database integration for semantic search
- Staleness detection (re-research if cache >30 days old)
- Version tracking (detect when researched tool has new version)
- Cache analytics (most researched tools, cache hit rate)

### v3: Expanded Research Capabilities
- Additional researchers (Stack Overflow, Reddit, Videos)
- Comparative research (tool A vs tool B)
- Trend analysis (tool popularity, adoption, issues)
- Dependency graph research

### v4: Advanced Documentation Types
- API Reference with interactive examples
- Architecture diagrams (Mermaid, GraphViz)
- Tutorial series with progressive difficulty
- Troubleshooting decision trees

### v5: Collaborative Research
- Multi-user cache sharing
- Research marketplace (share findings with community)
- Collaborative refinement (users improve cached research)
- Quality voting and curation

## Open Questions for Implementation

These questions were intentionally left for the implementation phase:

1. **User Interface:** How do users invoke this system?
   - Skill that Claude invokes automatically when detecting research needs?
   - Slash command like `/research <target> --output <type>`?
   - Sub-agent that can be called from other workflows?

2. **Output Location:** Where do generated skills/docs get written?
   - New plugin: `plugins/researched/<tool-name>/`?
   - Current project: `.claude/skills/<tool-name>/`?
   - Configurable location?

3. **Skill Naming:** What naming convention for auto-generated skills?
   - `using-<tool-name>` (e.g., `using-jina-mcp`)?
   - `<tool-name>-guide` (e.g., `jina-mcp-guide`)?
   - User-specified during research?

4. **Cache Invalidation:** Should there be manual cache clearing?
   - Command to invalidate specific cached research?
   - Command to clear all cache?
   - Automatic cleanup of old cache files?

5. **Error Handling:** What happens when researchers fail?
   - Continue with partial results?
   - Retry with different researchers?
   - Fail fast and report to user?

6. **Progress Visibility:** How does user see research progress?
   - Real-time updates as researchers complete?
   - Summary at end?
   - Silent operation?

7. **Cost Management:** Research can be expensive (many LLM calls)
   - Set budget limits?
   - Estimate cost before starting?
   - Incremental approval for expensive operations?

## Success Criteria

The MVP is successful if:

1. **Research works:** Can successfully research a GitHub repository across multiple dimensions
2. **Cache works:** Research findings are stored and can be reused
3. **Multiple outputs work:** Can generate both Skill and Dev Docs from one research run
4. **Quality is high:** Generated artifacts are expert-level and immediately useful
5. **System is extensible:** Easy to add new researchers and documenters
6. **Two modes work:** Both full pipeline and research-then-generate modes function

## Next Steps

1. **Choose implementation approach:**
   - Start with orchestrator or researchers?
   - Build top-down or bottom-up?
   - Prototype or production-quality from start?

2. **Resolve open questions:**
   - User interface design
   - Output location convention
   - Naming conventions

3. **Create detailed implementation plan:**
   - Use `superpowers:writing-plans` to break down into tasks
   - Identify which components can be built/tested independently
   - Define integration points

4. **Build and iterate:**
   - Start with minimal orchestrator + one researcher + one documenter
   - Validate end-to-end flow
   - Add remaining researchers and documenters
   - Refine based on real usage

## References

- **multi-agent-composition skill:** Architecture principles and patterns
- **superpowers:brainstorming skill:** Process for refining this design
- **Claude Code documentation:** MCP servers, sub-agents, skills architecture

---

**This design represents the consolidated understanding from the 2025-11-06 brainstorming session. It captures both the architecture and the reasoning behind key decisions. Future Claude sessions can reference this document to understand not just WHAT we're building, but WHY we made these choices.**
