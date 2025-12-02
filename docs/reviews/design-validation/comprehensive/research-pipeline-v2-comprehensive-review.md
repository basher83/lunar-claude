# Comprehensive Design Review: Research Pipeline v2

**Reviewed**: 2025-12-01
**Document**: docs/plans/2025-12-01-research-pipeline-v2-design-feedback.md
**Method**: 5-agent parallel validation (self-critique, premortem, landscape, SWOT, ADR)

---

## Executive Summary

**Overall Recommendation**: PROCEED WITH CAUTION

**Confidence Level**: Medium

**Key Findings**:

1. **Architecture is validated by production systems** - Supervisor-worker pattern with parallel execution confirmed by Anthropic's research system (90.2% improvement), M2 Deep Research, and Langflow. The design is architecturally sound.

2. **Critical validation gaps must be addressed first** - All 5 reviews independently identified the need for Phase 0 validation before committing to 80-100 hours: parallel Task tool PoC, token economics model, and cache lookup accuracy testing.

3. **Hybrid approach recommended over pure build** - SWOT analysis shows 70% time savings by integrating M2 Deep Research core while building custom Claude Code layer and knowledge base. Pure build ($14K-$19K TCO) vs Hybrid (~$5K-$7K).

**Critical Risks**:

- Agent coordination failures without explicit state machine design (Premortem Scenario 1)
- Context window overflow with 4 agent reports + synthesis (Premortem Scenario 2)
- Cache poisoning from naive keyword matching (Premortem Scenario 3)
- Pattern worship bias - overvaluing Anthropic patterns without validating necessity (Self-critique)

**Required Actions**:

- [ ] Execute Phase 0 validation (8 hours) before committing to full 4-week plan
- [ ] Build PoC proving Claude Code Task tool supports parallel dispatch with time savings
- [ ] Identify JSON Schema validation tooling accessible to Claude agents
- [ ] A/B test: Multi-agent vs single-agent research quality on 5 sample queries
- [ ] Validate cache lookup precision >70% with semantic matching approach

---

## Cross-Review Synthesis

### Common Themes

| Theme | Self-Critique | Pre-Mortem | Landscape | SWOT | ADR |
|-------|---------------|------------|-----------|------|-----|
| Parallel execution unvalidated | ✓ "Task tool validation needed" | ✓ "Agent coordination chaos scenario" | ✓ "Parallel is critical but needs testing" | ✓ "Task tool provides without overhead" | ✓ "Verify parallel execution with mock agents" |
| Supervisor-worker pattern validated | ✓ "Proven pattern reuse" | ✓ "Adopt from Anthropic/M2" | ✓ "All successful systems converge here" | ✓ "Integrate M2 core" | ✓ "Chosen architecture" |
| Token economics concern | ✓ "Context overflow in synthesizer" | ✓ "15× overhead unsustainable" | ✓ "Token budget explains 80% performance" | ✓ "Cost comparison needed" | ✓ "15× overhead requires high-value tasks" |
| Cache lookup quality unknown | ✓ "Cache key collision risks" | ✓ "Cache poisoning scenario" | ✓ "Need precision/recall testing" | ✓ "Semantic indexing unique requirement" | ✓ ">30% cache hit rate target" |
| Codebase contextualization is key differentiator | ✓ "Core justification for custom build" | ✓ "No existing solution provides this" | ✓ "Validated gap - none exist" | ✓ "Build custom layer" | ✓ "Primary differentiator" |

### Contradictions

- **Integrate vs Build**: SWOT recommends hybrid (integrate M2 core), while ADR chooses full custom build. Resolution: Start with hybrid for MVP, evolve to custom if M2 limitations emerge.

- **Complexity vs Simplicity**: Self-critique suggests starting with 2 agents, while Landscape validates 4-agent approach. Resolution: Both are valid - start with 2 (GitHub + Tavily) to validate core loop, add DeepWiki + Exa after proving value.

### Strongest Validations

- **Multi-source research improves quality**: 90.2% improvement over single-agent (Anthropic), 40% accuracy gain over static RAG (NVIDIA research)
- **Persistent knowledge base justified**: No existing solution offers cross-session semantic cache for developer tools
- **Claude Code native integration justified**: External frameworks cannot access local files, plugins, or MCP servers natively
- **JSON Schema enforcement critical**: M2 Deep Research and Parallel.ai both use this; prevents "telephone game" errors

---

## Build vs Integrate Decision

**Recommendation**: HYBRID (per SWOT analysis)

| Factor | Build | Integrate | Winner |
|--------|-------|-----------|--------|
| Time to production | 4 weeks (80-100 hrs) | 1 week (6-8 hrs) | Integrate |
| 3-Year TCO | $14K-$19K | $2.1K-$3.2K | Integrate |
| Codebase contextualization | Native | Requires wrapper | Build |
| Claude Code integration | Native | Requires shim | Build |
| Synthesis quality | Unproven | Battle-tested (M2) | Integrate |
| Knowledge base control | Full | Limited | Build |

**Hybrid Strategy**:

| Component | Decision | Source |
|-----------|----------|--------|
| Research Orchestration Engine | Integrate | M2 Deep Research |
| GitHub/Tavily/Exa/DeepWiki Agents | Extend | M2 + Custom prompts |
| Synthesis Algorithm | Integrate | M2 Deep Research |
| Slash Command Interface | Build | Custom Claude Code |
| Knowledge Base & Caching | Build | Custom (unique requirement) |
| Codebase Contextualization | Build | Custom (core differentiator) |
| Progress Tracking | Build | Custom Claude Code hooks |

**Solutions to Leverage**:

- **M2 Deep Research**: Supervisor-worker pattern, JSON schemas, synthesis algorithms (saves 60-70 hours)
- **Anthropic patterns**: Effort scaling rules, tool selection heuristics, delegation best practices
- **Tavily/Exa/GitHub MCP**: Use directly via MCP, don't wrap in custom agents

---

## Unified Validation Plan

| Validation | Source | Priority |
|------------|--------|----------|
| Parallel Task tool PoC (2+ agents, measure timing) | Self-critique, Premortem | HIGH |
| JSON Schema validation tooling identification | Self-critique | HIGH |
| Token economics model (P50/P95 per query) | Premortem | HIGH |
| A/B test: multi-agent vs single-agent quality | Self-critique | HIGH |
| Cache lookup precision/recall testing (>70% target) | Premortem | HIGH |
| Context overflow handling strategy | Premortem | MEDIUM |
| Failure mode documentation | Premortem | MEDIUM |
| User validation interviews (2-3 users) | Self-critique | LOW |

### Phase 0 Recommendation (8 hours before main build)

| Task | Hours | Success Criteria |
|------|-------|------------------|
| Parallel agent dispatch PoC | 2 | 2× speedup demonstrated with 2 dummy agents |
| JSON Schema validation research | 1 | Specific tool identified with working example |
| A/B quality test | 3 | 4-agent vs single-agent on 5 queries, blind evaluation |
| Simplified cache design | 1 | Grep-based tag search finds relevant cache in <1 second |
| User validation | 1 | 2 users confirm research system would be valuable |

**Decision Point**: After Phase 0, reassess confidence. If PoC succeeds → proceed with simplified Phase 1 (2 agents, basic synthesis). If PoC fails → pivot to sequential execution with aggressive caching.

---

## Individual Reviews

### Self-Critique

**Confidence**: Medium

**Key Strengths Identified**:

- Proven pattern reuse (M2 Deep Research, Anthropic research-agent)
- Comprehensive validation strategy with JSON schemas and confidence scoring
- Persistent knowledge base with semantic discovery

**Key Concerns**:

- Parallel execution complexity without Task tool validation
- Schema validation enforcement mechanism unspecified
- Codebase contextualization lacks concrete search strategy

**Biases Checked**:

- Pattern worship bias (overvaluing authoritative sources)
- Sunk cost in original design
- Not-invented-here avoidance leading to over-composition

**Recommendation**: Proceed with caution, execute Phase 0 validation first

[Full report: parts/self-critique.md](parts/self-critique.md)

---

### Pre-Mortem

**Confidence**: Medium

**Failure Scenarios**:

1. **Agent Coordination Chaos**: Orchestrator can't reliably track 4 parallel agents, state management failures
2. **Context Window Economics Breakdown**: Reports exceed context, costs become prohibitive ($0.50+/query)
3. **Cache Poisoning**: Naive keyword matching fills cache with irrelevant results, users lose trust

**Research Gaps**:

- No agent orchestration patterns studied in Claude Code ecosystem
- Token consumption profiles not measured
- MCP tool reliability characteristics unknown

**Recommendation**: Proceed conditionally, requires 5 validation items first

[Full report: parts/premortem.md](parts/premortem.md)

---

### Landscape Research

**Confidence**: High

**Mature Solutions Found**:

- LangGraph (60% fit) - Excellent orchestration, requires Python
- CrewAI (50% fit) - Great prototyping, YAML config mismatch
- M2 Deep Research (70% fit) - Close match, lacks MCP integration
- Anthropic Research System (90% fit) - Perfect match, proprietary

**Validated Gaps**:

- Codebase contextualization (none exist)
- Persistent cross-session knowledge base (none exist)
- Claude Code CLI integration (none exist)

**Patterns to Adopt**:

- Supervisor-worker architecture
- JSON Schema validation
- Layered memory (vector + SQL)
- Interleaved thinking for state preservation

**Recommendation**: Proceed to design, 40-50% component reuse possible

[Full report: parts/landscape.md](parts/landscape.md)

---

### SWOT Analysis

**Confidence**: High

**Recommendation**: HYBRID approach

**Key Trade-off**: Prioritizing time-to-value over architectural purity by accepting Python dependency for research core

**Cost Analysis**:

- Pure Build: $14K-$19K over 3 years
- Pure Integrate: $2.1K-$3.2K over 3 years
- Hybrid: ~$5K-$7K (70% savings vs pure build)

[Full report: parts/swot.md](parts/swot.md)

---

### ADR

**Confidence**: High

**Chosen Alternative**: Custom Claude Code-Native Solution (adapted from Anthropic patterns)

**Rejected Alternatives**:

- Do Nothing: Productivity bottleneck (10+ minutes per research task)
- Existing Frameworks: External dependencies, no codebase integration
- Traditional RAG: Cannot discover new information
- Direct Anthropic Adaptation: Cloud-scale complexity for CLI use case

**Success Metrics Defined**:

- Research speed: < 60 seconds
- Cache hit rate: > 30%
- Confidence accuracy: > 0.75 correlation
- Schema compliance: 100%

[Full report: parts/adr.md](parts/adr.md)

---

## Final Checklist

- [x] All 5 validation perspectives completed
- [x] Contradictions between reviews resolved (hybrid vs pure build → start hybrid)
- [x] Build vs integrate decision has evidence (TCO comparison, gap analysis)
- [x] Validation plan is actionable (Phase 0 defined with 8-hour scope)
- [x] Existing solutions thoroughly evaluated (6 OSS, 5 SaaS, 3 frameworks)
- [x] Team has capacity for chosen approach (single developer, 80-100 hours available)
- [x] Success criteria defined (7 metrics with targets)
- [x] Re-evaluation triggers identified (agent success rate, speed, cache hit rate)

---

## Decision

**Proceed**: CONDITIONAL

**Must complete Phase 0 validation first (8 hours)**:

- [ ] Parallel agent dispatch PoC with measured time savings
- [ ] JSON Schema validation tooling identification
- [ ] A/B test: multi-agent vs single-agent quality
- [ ] Cache lookup precision >70% with semantic matching
- [ ] 2 user validation interviews

**If Phase 0 succeeds**:

Proceed with hybrid MVP (2 agents, M2 core, 40 hours) targeting 80% value in 2 weeks

**If Phase 0 fails**:

Pivot to sequential single-agent with aggressive caching

**Re-evaluate if**:

- Agent success rate drops below 60%
- Research speed exceeds 90 seconds
- Cache hit rate below 20% after 50 queries
- LangGraph/CrewAI adds native Claude Code support

**Next Review Date**: 2025-03-01 (3 months) or after 100 production queries
