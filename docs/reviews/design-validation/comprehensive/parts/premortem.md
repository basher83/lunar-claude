# Pre-Mortem Analysis: Research Pipeline v2

**Analyzed**: 2025-12-01
**Document**: docs/plans/2025-12-01-research-pipeline-v2-design-feedback.md
**Method**: Pre-mortem failure scenario analysis

---

## Design Context

**Summary**: A multi-agent research system for Claude Code that dispatches 4 specialized researcher agents (GitHub, Tavily, DeepWiki, Exa) in parallel to gather implementation patterns, synthesizes findings with conflict resolution, and provides codebase-contextualized integration recommendations with persistent knowledge base caching.

**Problem Statement**: Eliminate repetitive manual research by building a Claude Code-native research pipeline that discovers battle-tested implementations, validates patterns across multiple sources, and provides actionable integration guidance tailored to the existing codebase.

**Key Components**:

- 4 specialized researcher agents (GitHub, Tavily, DeepWiki, Exa) with JSON schema-validated outputs
- Synthesizer agent for cross-source validation and conflict resolution
- Orchestrator slash command for parallel dispatch and progress tracking
- Persistent knowledge base with semantic indexing and cache reuse
- Codebase contextualization engine for integration recommendations

---

## Failure Scenarios

### Scenario 1: Agent Coordination Chaos

| Aspect | Details |
|--------|---------|
| **Failure Point** | The orchestrator cannot reliably dispatch 4 agents in parallel, track their completion, or handle partial failures. Agents timeout inconsistently, reports arrive out of order, and the synthesizer processes incomplete data, producing low-confidence results that users distrust. |
| **Root Cause** | We assumed Claude Code's Task tool provides robust parallel execution guarantees without validating timeout handling, agent lifecycle management, or state tracking patterns. The design treats agents as fire-and-forget operations without considering race conditions, partial completion states, or orchestrator restart scenarios. |
| **Warning Signs** | No explicit state machine for agent lifecycle (dispatched → running → completed/failed/timeout). Missing timeout configuration strategy (per-agent vs global). No discussion of how orchestrator tracks "3 of 4 agents complete" state. Absence of circuit breaker patterns for repeated agent failures. |
| **Precedent** | Airflow's early task orchestration suffered from similar issues - DAG tasks would timeout inconsistently, partial failures weren't properly surfaced, and retry logic caused duplicate execution. Required years of refinement to build robust XCom state tracking and task lifecycle management. Similar patterns in Temporal/Cadence where workflow state tracking is explicitly required. |

### Scenario 2: Context Window Economics Breakdown

| Aspect | Details |
|--------|---------|
| **Failure Point** | Research reports from 4 agents + synthesis + codebase context exceed Claude's context window, causing truncation or expensive multi-pass processing. The system becomes prohibitively slow (>2 minutes) or expensive ($0.50+ per query), making it unusable for iterative research workflows. |
| **Root Cause** | We designed for feature richness without modeling token economics. Each agent's JSON report is assumed "small enough" without measuring actual token consumption. No compression strategy, no progressive disclosure, no intelligent pruning of low-relevance findings before synthesis. |
| **Warning Signs** | No token budget calculations in the design. GitHub agent could return 5+ repositories with full README contents (5k-10k tokens each). Synthesis template shows extensive markdown formatting with all 4 source reports repeated. Codebase contextualization adds grep results and file contents without size limits. Missing discussion of "what do we cut when we hit limits?" |
| **Precedent** | LangChain's early map-reduce patterns failed at scale because they didn't account for intermediate result sizes. AutoGPT-style agent loops became unusable when conversation history grew unbounded. M2 Deep Research explicitly uses compression and summarization between stages - we reference it but don't adopt the pattern. |

### Scenario 3: Cache Poisoning and Stale Knowledge

| Aspect | Details |
|--------|---------|
| **Failure Point** | The knowledge base fills with low-quality, outdated, or incorrect research that gets served to users instead of fresh results. Tag-based cache matching returns irrelevant results (high false positive rate). Users learn to distrust cached findings and always force refresh, making the cache worthless. |
| **Root Cause** | We designed cache lookup using simple keyword matching and tag overlap without validating semantic similarity accuracy. No cache invalidation strategy beyond 30-day TTL. No quality scoring or feedback mechanism to identify bad cache entries. Confidence scores are stored but not used for cache ranking. |
| **Warning Signs** | Cache search algorithm uses naive keyword/tag overlap (lines 912-951) without testing precision/recall. No user feedback loop to mark cache entries as "helpful" or "outdated". Missing discussion of how to handle rapidly evolving domains (e.g., AI libraries change every 2 months). No cache warming or pre-population strategy for common queries. |
| **Precedent** | Search engine caching learned this lesson decades ago - Google's cache system uses freshness signals, user engagement metrics, and domain-specific TTLs. Stack Overflow struggled with outdated answers ranking higher than current best practices until they added freshness scoring. Browser DNS caches needed TTL + validation to prevent serving stale records. |

---

## Research Gaps

### Not Investigated

- Existing agent orchestration patterns in Claude Code ecosystem (what do other plugins do for parallel agent dispatch?)
- Token consumption profiles for typical research queries (what's the actual cost per query?)
- Cache hit rate validation methods (how do we measure if semantic matching works?)
- User interaction patterns for research tools (do users want conversational follow-ups or one-shot results?)
- MCP tool reliability characteristics (which tools timeout most? which have rate limits?)

### Not Validated

- Claude Code's Task tool actually supports parallel execution with proper state tracking
- 4-agent parallel dispatch completes within 60 seconds under real network conditions
- JSON schema validation performance impact (does it add latency?)
- Synthesizer agent can fit 4 full reports + synthesis logic in context window
- Cache directory I/O patterns won't cause filesystem bottlenecks on NFS/cloud storage

### Not Explored

- Edge case: User kills slash command mid-execution (orphaned agent processes?)
- Edge case: Two users run same query simultaneously (cache directory race condition?)
- Edge case: Agent returns malformed JSON that passes schema but has semantic errors
- Edge case: GitHub API rate limit hit during agent execution (does retry logic exist?)
- Failure mode: All 4 agents return "no results found" (how to surface this gracefully?)

### Overlooked Standards

- OpenTelemetry for agent tracing and observability (industry standard for distributed systems)
- JSON Schema $ref and $defs for reusable schema components (DRY schema design)
- RFC 7807 Problem Details for structured error responses (better than free-form error messages)
- Semantic versioning for cache schema (what happens when schema v2 is incompatible with v1 cache?)
- OAuth token refresh patterns for long-running MCP tool sessions

---

## Build vs. Integrate Analysis

| Question | Answer |
|----------|--------|
| Existing solutions? | - [Perplexity API](https://docs.perplexity.ai/) - Multi-source research with citations<br>- [Exa Search API](https://exa.ai/) - Neural search with content extraction<br>- [Tavily Research API](https://tavily.com/) - Dedicated research agent API<br>- [LangChain Research Agents](https://python.langchain.com/docs/use_cases/web_research) - Pre-built research patterns<br>- [AutoGPT Research Mode](https://github.com/Significant-Gravitas/AutoGPT) - Autonomous research loops |
| Why build? | We need **codebase contextualization** (none of the above integrate with local code patterns), **persistent cross-session knowledge base** (APIs don't cache for users), and **Claude Code-native UX** (slash commands, agent composition patterns). However, we're rebuilding **all the orchestration, synthesis, and quality control** that mature tools already solved. |
| Gaps justifying custom dev? | 1. Integration with Claude Code's agent system (can't use external APIs directly as agents)<br>2. Codebase pattern matching for "how does this research apply to MY code?"<br>3. Cross-session knowledge persistence in local cache<br>4. Semantic indexing tied to project structure/domain |
| Components to leverage? | - Use Tavily/Exa/DeepWiki **as-is** via MCP instead of wrapping them in custom agents<br>- Adopt LangChain's map-reduce synthesis pattern instead of custom synthesizer<br>- Integrate existing JSON schema validation libraries instead of custom validation<br>- Use standard cache invalidation patterns (ETags, Last-Modified) from HTTP caching specs |

---

## Validation Plan

### For Scenario 1: Agent Coordination Chaos

- **Research**: Study Claude Code plugin patterns for multi-agent orchestration. Analyze how `superpowers:dispatching-parallel-agents` handles agent lifecycle. Review Temporal/Prefect/Airflow state machine patterns for workflow orchestration.
- **PoC**: Build minimal 2-agent orchestrator with explicit state tracking (dispatched → running → done/failed/timeout). Test timeout scenarios, partial failures, and retry logic. Measure actual completion times under realistic network latency.
- **Questions**: (1) Does Claude Code's Task tool return agent PIDs or handles for tracking? (2) How do we detect "agent is still running" vs "agent died silently"? (3) What's the right timeout for each agent type based on empirical data? (4) Should we use a state machine library or hand-roll lifecycle management?
- **Success Criteria**: (1) PoC handles 2/2 agents completing successfully, 1/2 failing, and both timing out. (2) State transitions are observable and debuggable. (3) Orchestrator can be interrupted and resume. (4) Empirical timeout values are documented with evidence.

### For Scenario 2: Context Window Economics Breakdown

- **Research**: Measure token consumption of sample research reports from each agent type. Analyze M2 Deep Research's compression patterns. Study Claude's caching API for prompt caching opportunities. Review LangChain's map-reduce token budgeting strategies.
- **PoC**: Generate realistic research reports for a complex query ("Battle-tested Kubernetes on Proxmox with Ansible"). Count tokens for: (1) 4 agent reports, (2) synthesis input, (3) synthesis output, (4) codebase context, (5) final response. Test with Claude's 200k context window to find breaking point.
- **Questions**: (1) What's the P50 and P95 token consumption per query? (2) At what point do we exceed context window? (3) Which components are compressible without losing quality? (4) Can we use prompt caching to reduce effective token count? (5) What's the cost per query in production usage?
- **Success Criteria**: (1) Token budget model with P50/P95 values documented. (2) Compression strategy reduces total tokens by 40%+ without quality loss. (3) Cost per query < $0.10 for typical use cases. (4) System gracefully handles queries that exceed limits with progressive degradation.

### For Scenario 3: Cache Poisoning and Stale Knowledge

- **Research**: Study semantic search algorithms (embeddings, BM25, hybrid search). Analyze cache invalidation patterns from CDNs (Cloudflare, Fastly). Review search engine freshness scoring (Google's QDF, Bing's relevance decay). Investigate feedback loop patterns from recommendation systems.
- **PoC**: Build cache lookup test harness with 20 real queries and manually labeled "good match" / "bad match" results. Implement baseline (keyword matching) and compare with embedding-based semantic similarity. Measure precision/recall. Test with queries from fast-moving domains (AI frameworks) vs stable domains (Linux networking).
- **Questions**: (1) What precision/recall threshold makes cache useful vs annoying? (2) Should we use embeddings (adds latency) or stick with keyword matching (simpler)? (3) How do we detect when cached results are stale without re-running research? (4) Can users mark cache entries as "outdated" to train the system? (5) What domains need shorter TTLs?
- **Success Criteria**: (1) Cache lookup achieves >70% precision (relevant matches) and >50% recall (finds matches when they exist). (2) Freshness scoring mechanism prevents serving outdated AI framework research. (3) User feedback mechanism exists (even if manual initially). (4) Domain-specific TTL configuration documented with rationale.

---

## Recommendation

**Proceed**: CONDITIONAL

**If Conditional, requires**:

- [ ] Agent orchestration PoC demonstrating reliable parallel execution, timeout handling, and state tracking with empirical completion time measurements
- [ ] Token economics model with measured P50/P95 consumption, compression strategy reducing tokens 40%+, and cost per query validation
- [ ] Cache validation study showing >70% precision with semantic matching approach, freshness scoring mechanism, and domain-specific TTL strategy
- [ ] Integration assessment: evaluate using Tavily/Exa APIs directly via MCP vs building custom wrapper agents (validate if wrapper adds value or just complexity)
- [ ] Failure mode testing: document behavior for all-agents-fail, schema-validation-fail, cache-corruption, and mid-execution-interrupt scenarios

**Confidence Level**: Medium

The design is architecturally sound and references proven patterns (M2 Deep Research, Anthropic research-agent), but critical implementation details need empirical validation before committing to 80-100 hours of development. The three failure scenarios are plausible based on precedent (Airflow orchestration issues, LangChain context overflow, search engine cache staleness), and the research gaps indicate insufficient validation of core assumptions. The build vs. integrate analysis suggests we may be over-building - using MCP tools directly instead of wrapping them in custom agents could reduce complexity by 40%.

**Key Risk**: We're building complex orchestration logic (parallel dispatch, state tracking, timeout handling) that existing workflow engines solved years ago. Consider whether Claude Code should integrate with a lightweight workflow engine (Temporal, Prefect) rather than hand-rolling orchestration.

**Alternative Path**: Start with sequential (not parallel) execution of 2 agents (GitHub + Tavily) to validate the synthesis → contextualization → caching pipeline. This reduces complexity by 60%, allows faster iteration, and proves value before investing in 4-agent parallel orchestration. Add DeepWiki and Exa after validating the core loop works.
