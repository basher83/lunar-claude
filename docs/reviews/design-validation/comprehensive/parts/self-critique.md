# Design Review: Research Pipeline v2 Design Feedback

**Reviewed**: 2025-12-01
**Document**: docs/plans/2025-12-01-research-pipeline-v2-design-feedback.md
**Reviewer**: Claude (self-critique method)

---

## Phase 1: Initial Assessment

### Strengths

1. **Proven Pattern Reuse with Clear Attribution**
   - Aspect: The design explicitly references two battle-tested implementations (M2 Deep Research and Anthropic's research-agent demo) with specific patterns to adopt from each
   - Why effective: Instead of designing from scratch, this leverages proven supervisor-worker architecture, JSON schemas, and subagent tracking patterns that have demonstrated success in production
   - Evidence: Specific references throughout the plan (Tasks 1.1, 1.2, 1.3) cite exact patterns from M2 Deep Research for schemas and Anthropic demo for agent monitoring, reducing greenfield risk

2. **Comprehensive Validation Strategy Built Into Architecture**
   - Aspect: Multi-layered validation including JSON schema enforcement, cross-source agreement scoring, confidence metrics, and source priority hierarchies
   - Why effective: The design prevents low-quality results through structural constraints rather than relying on post-hoc filtering. The synthesizer agent (Task 2.4) implements explicit conflict resolution rules and confidence calculations
   - Evidence: Research report schema (Task 1.1) has strict validation rules; synthesizer uses 4-factor confidence formula (40% source agreement + 30% individual confidence + 20% maturity + 10% completeness); source priority hierarchy (DeepWiki > GitHub > Tavily > Exa) provides deterministic conflict resolution

3. **Persistent Knowledge Base with Semantic Discovery**
   - Aspect: The `.claude/research-cache/` structure with indexed entries, tags for semantic search, and 30-day staleness management creates a learning system that improves over time
   - Why effective: Addresses the "reinventing the wheel" problem in research by enabling cache hits on similar queries, reducing API costs and response time while building institutional knowledge
   - Evidence: Task 3.1 implements `search_cache()` with tag overlap + keyword matching relevance scoring; cache index structure (Task 1.2) includes tags, confidence, timestamp; Task 4.1 includes cache reuse test scenario

### Concerns

1. **Parallel Execution Complexity Without Claude Code Task Tool Validation**
   - Assumption/Decision: The plan assumes the Task tool can reliably dispatch 4 agents in parallel and track their completion without explicit testing of this capability
   - Risk: Claude Code's Task tool may not support true parallelism, may have undocumented concurrency limits, or may serialize execution under the hood. If agents run sequentially, the 60-second target becomes impossible (4 agents × 30s each = 120s minimum)
   - Validation needed: Before Phase 1, create proof-of-concept test that dispatches 4 minimal agents in parallel and measures actual execution time. Verify Task tool returns handles immediately vs blocking until completion

2. **Schema Validation Enforcement Without Tooling**
   - Assumption/Decision: Task 1.1 defines a JSON Schema but the plan doesn't specify how/when validation occurs or what tooling enforces it
   - Risk: Agents may produce invalid JSON that passes undetected until synthesis fails. Manual validation in Markdown agents is error-prone. The error handling section (Task 5.2) mentions "schema validation failure" but doesn't explain the validation mechanism
   - Validation needed: Identify specific JSON Schema validation tool (Python jsonschema, ajv, etc.), create validation helper that agents can invoke before writing reports, add validation step to orchestrator before synthesis phase

3. **Codebase Contextualization Lacks Concrete Search Strategy**
   - Assumption/Decision: Task 4.2 describes contextualization as "search codebase for plugins/skills related to research topic" but doesn't specify search patterns, file path heuristics, or relevance scoring
   - Risk: Vague contextualization produces generic suggestions like "consider adding to plugins/infrastructure/" instead of specific actions like "extend plugins/infrastructure/proxmox-infrastructure/roles/cloud-init.yaml based on pattern from repo X". Low-quality integration suggestions defeat the unique value proposition
   - Validation needed: Define explicit contextualization algorithm - which tools to use (Grep patterns? File glob patterns? AST analysis?), how to score relevance (keyword matches in file paths + content?), minimum relevance threshold to include in suggestions

### Integration vs. Build

| Question | Answer |
|----------|--------|
| Existing solutions identified? | Yes - M2 Deep Research provides supervisor-worker pattern and JSON schemas; Anthropic research-agent demo provides subagent tracking and hook patterns. However, no complete Claude Code-native research system exists with persistent knowledge base + codebase contextualization |
| Evidence against existing solutions | M2 Deep Research is standalone Python application without Claude Code integration, lacks codebase contextualization, requires separate infrastructure. Anthropic demo is proof-of-concept focused on research quality, not production-ready with caching/knowledge base. Neither system provides semantic indexing for discovery across sessions |
| Custom build justified? | Yes, with caveat - the orchestration layer, knowledge base, and contextualization are custom builds that compose existing patterns. The researcher agents themselves could potentially be simplified by using existing MCP tool wrappers more directly rather than custom agent definitions (this should be validated in Phase 1) |

---

## Phase 2: Self-Critique Findings

### Biases Identified

- **Pattern worship bias**: I may be overvaluing the M2 Deep Research and Anthropic patterns because they come from authoritative sources, without critically evaluating whether their complexity is necessary for this use case. The 4-agent parallel architecture might be over-engineered compared to a simpler sequential approach with better caching.

- **Not-invented-here avoidance**: By focusing heavily on composing existing patterns, I may be missing opportunities to simplify. The synthesizer agent (Task 2.4) is complex - could a simpler approach work, like just concatenating findings with basic deduplication?

- **Sunk cost in original design**: The design feedback document represents significant thinking. I may be defending it because of effort invested rather than objectively evaluating whether a simpler approach (e.g., single researcher agent that calls multiple tools sequentially) would meet needs with less complexity.

### Blind Spots Discovered

- **MCP tool reliability assumptions**: The plan assumes GitHub MCP, Tavily, DeepWiki, and Exa tools are stable, fast, and comprehensive. What if GitHub API rate limits are hit immediately? What if DeepWiki doesn't cover the queried topic? No fallback strategies exist beyond "graceful degradation."

- **Context window management**: Task 2.4 synthesizer reads 4 complete JSON reports. If each researcher finds 50 sources, the synthesizer input could be massive. No truncation strategy, no summarization before synthesis, no handling for context overflow.

- **User experience during 60-second waits**: The progress indicators (Task 3.2) are described but may not be implementable in Claude Code's CLI. If the user just sees "thinking..." for 60 seconds with no updates, they may interrupt or lose confidence.

- **Cache key collision risks**: Task 1.4 describes normalizing queries to "lowercase, remove special chars, create slug" but doesn't handle semantic duplicates (e.g., "MicroK8s on Proxmox" vs "Proxmox with MicroK8s" would create different cache keys despite being identical queries).

- **No evaluation criteria for "good" research**: The success metrics (Task 5.3) focus on technical metrics (speed, schema compliance) but not research quality. How do we know if findings are actually useful vs just schematically valid?

### Reality Check Results

- **Engineering time vs value**: This is a 80-100 hour project (4 weeks). For a personal homelab repository, this is substantial investment. Could 80% of value be achieved in 20% of time with simpler approach? What's the opportunity cost vs other priorities?

- **Build vs integrate justification needs strengthening**: While M2 Deep Research can't be directly integrated, could its supervisor-worker architecture be used as-is with Claude Code agents? The plan recreates similar patterns in Markdown agent definitions - is that reinvention justified or should we use M2 as a library?

- **Senior engineer challenge**: "Why not just use a single agent that calls firecrawl search, reads top 3 results, and gives you an answer in 15 seconds?" The multi-agent architecture's value proposition (comprehensive coverage, cross-validation) is stated but not proven necessary.

- **Half-time shipping exercise**: If forced to ship in 2 weeks (40 hours), I would cut: synthesizer agent (just concatenate findings), cache utilities (manual file inspection), progress tracking (nice-to-have), codebase contextualization (user can do manually). This suggests those are secondary to core research functionality.

### Validation Gaps

- **No proof that 4 agents provide better results than 1**: The design assumes more sources = better research, but doesn't validate this. A simple A/B test (4-agent vs single-agent with firecrawl) on 10 sample queries would prove/disprove this assumption.

- **Parallel execution capability unproven**: Before building 4 agents, need proof-of-concept that demonstrates Claude Code Task tool supports parallel dispatch with actual time savings.

- **Schema validation enforcement mechanism unspecified**: Can't proceed without knowing how agents will validate JSON output. Need to identify specific tooling and integration point.

- **Cache lookup algorithm effectiveness unknown**: The tag overlap + keyword matching relevance scoring (Task 3.1) is reasonable but unvalidated. Should test on sample queries to see if it actually identifies similar research vs false positives.

- **No stakeholder validation**: This is a personal project, but have I considered whether this research system would be useful for others? Should validate with potential users before 100-hour investment.

---

## Phase 3: Revised Assessment

### Strengthened Justification

After self-critique, these decisions survive with evidence:

**1. Multi-source research is valuable**
- Evidence: Personal experience shows single sources miss context. GitHub code without documentation is incomplete; documentation without real implementations is theoretical; blog posts without code are superficial.
- Refinement: Still validate with simple A/B test, but proceed with multi-source assumption

**2. Persistent knowledge base addresses real pain point**
- Evidence: Repeated research on similar topics (Kubernetes, Proxmox, Ansible) wastes time and API costs. Cache with semantic discovery would have saved dozens of hours in past 6 months.
- Refinement: Simplify cache structure - just store synthesis.md files with tags in frontmatter, no complex index.json

**3. JSON schema validation prevents quality issues**
- Evidence: Unstructured agent outputs are hard to synthesize programmatically. Schema enforcement from M2 Deep Research pattern is proven to work.
- Refinement: Must identify validation tooling before Phase 1

**4. Codebase contextualization is unique value**
- Evidence: Generic research is available via ChatGPT/Claude. The differentiation is "how does this apply to MY codebase?" This justifies custom build.
- Refinement: Define concrete search patterns, require code examples in integration suggestions

### Required Mitigations

| Risk | Mitigation | Owner |
|------|------------|-------|
| Parallel execution may not work in Claude Code | Create POC in Phase 0 (before Task 1.1): dispatch 2 dummy agents, measure timing, verify true parallelism | Self |
| Schema validation mechanism unclear | Research and specify validation tooling in Phase 0: identify JSON Schema validator accessible to Claude agents, document integration pattern | Self |
| Context overflow in synthesizer | Add input size check before synthesis: if total reports > 10K tokens, truncate sources arrays to top 5 per agent before synthesis | Self |
| Cache key collisions on semantic duplicates | Improve cache lookup: normalize query to canonical form (lowercase, sort words, remove stop words) and check for exact match before tag-based similarity | Self |
| 60-second wait with no feedback | Reduce target to 30 seconds by cutting 1-2 agents if needed, investigate Claude Code's ability to stream progress updates | Self |
| Over-engineering vs simpler alternatives | Start with MVP in Phase 1: build 2 agents (GitHub + Tavily), simple concatenation synthesis, manual caching. Validate value before building complexity | Self |

### Integration Strategy (Refined)

| Component | Decision | Evidence |
|-----------|----------|----------|
| Supervisor-worker architecture | **Configure** M2 pattern for Claude | Proven pattern, reduces risk. Adapt to Markdown agent format rather than recreate |
| JSON Schema validation | **Integrate** existing validator | Python jsonschema library accessible via bash commands, don't build custom |
| GitHub/Tavily/DeepWiki/Exa researchers | **Build** as Claude agents | These are thin wrappers over MCP tools with domain-specific search strategies - lightweight, justified |
| Synthesizer agent | **Simplify** initial version | Start with template-based concatenation + basic deduplication, add complex cross-validation in v2 if needed |
| Knowledge base index | **Simplify** to frontmatter tags | Don't build index.json + search algorithm. Store tags in synthesis.md frontmatter, use grep/glob to search |
| Codebase contextualization | **Build** with defined patterns | Core differentiation, but must specify: use Grep for keyword search in plugin dirs, require minimum 2 matches to include suggestion |
| Progress tracking | **Defer** to Phase 5 | Nice-to-have. If Claude Code doesn't support streaming updates, cut from MVP |

### Decision Confidence

**Confidence Level**: Medium

**What would increase confidence**:

- POC proving Claude Code Task tool supports parallel agent dispatch with measured time savings (target: 2x speedup with 2 agents)
- Identification of specific JSON Schema validation tooling accessible to Claude agents with working example
- Simple A/B test: 4-agent research vs single-agent firecrawl on 5 sample queries, blind evaluation of result quality
- Simplified cache design validated: can grep-based tag search find relevant cached research in < 1 second?
- User validation: discuss with 2-3 potential users to confirm research system would be valuable vs hypothetical need

**Re-evaluation triggers**:

- If POC shows parallel execution doesn't work → pivot to sequential execution with aggressive caching
- If schema validation can't be integrated → accept unstructured outputs, rely on prompt engineering for consistency
- If A/B test shows single-agent results are equivalent → cut to 2 agents maximum (GitHub + one general-purpose)
- If cache lookup is slow (>3 seconds) → simplify to manual cache management, defer semantic search to v2
- If first 40 hours of work produces unusable results → stop, reassess if research system is right solution to problem

---

## Final Checklist

- [x] Challenged my own assumptions explicitly - Identified pattern worship bias, over-engineering risk, unvalidated parallel execution assumption
- [x] Identified and addressed potential biases - Noted sunk cost fallacy in defending original design, NIH avoidance leading to over-composition
- [x] Validated that existing solutions truly don't meet needs - M2 Deep Research confirmed as not Claude Code native, lacks codebase contextualization; Anthropic demo is POC not production system
- [x] Confirmed justification for custom development vs. integration - Custom orchestrator and contextualization justified; schema validation and some patterns should be integrated not rebuilt
- [x] Surfaced blind spots and created mitigation plan - Found 6 blind spots (MCP reliability, context overflow, UX, cache collisions, evaluation criteria, engineering ROI) with specific mitigations
- [ ] Obtained external perspective or review - **NOT COMPLETE** - This is self-critique only; would benefit from peer review or user validation
- [x] Ready to proceed OR identified what research is still needed - **RESEARCH NEEDED**: Phase 0 POC for parallel execution, schema validation tooling identification, A/B test for multi-agent value, simplified cache design validation, user interviews

---

## Recommendation

**PROCEED WITH CAUTION** - Execute Phase 0 validation work before committing to full 4-week plan:

1. **Week 0 (8 hours)**:
   - POC: Parallel agent dispatch in Claude Code (2 hours)
   - Research: JSON Schema validation tooling (1 hour)
   - A/B test: Multi-agent vs single-agent research quality (3 hours)
   - Simplify: Cache design from index.json to frontmatter-based (1 hour)
   - Validate: Discuss with 2 users (1 hour)

2. **Decision point**: After Week 0, reassess confidence level. If POC and tests succeed, proceed with simplified Phase 1 (2 agents, basic synthesis, manual cache). If POC fails or A/B test shows no quality gain, pivot to simpler single-agent architecture.

3. **Incremental value delivery**: Build MVP in first 2 weeks (40 hours) targeting 80% value - basic research with 2 agents, simple caching, basic contextualization. Ship and use for 2 weeks before deciding whether to invest remaining 40 hours in optimization.

This approach reduces risk of 100-hour investment without validation while preserving the core value proposition.
