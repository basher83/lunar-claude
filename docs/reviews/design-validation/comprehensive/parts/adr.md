# ADR: Research Pipeline v2 Architecture

**Status**: Proposed
**Date**: 2025-12-01
**Deciders**: System architect, Claude Code plugin developer

---

## Context

The lunar-claude project requires a sophisticated research system to help developers discover battle-tested implementations, patterns, and best practices from multiple sources. The current approach lacks structured research capabilities, forcing developers to manually search across GitHub, documentation, and web sources sequentially—a time-consuming and inconsistent process.

The Research Pipeline v2 aims to provide an intelligent, multi-source research system that:
- Searches multiple sources (GitHub, web, documentation, semantic search) in parallel
- Synthesizes findings from disparate sources into coherent, actionable insights
- Maintains a persistent knowledge base to avoid redundant research
- Integrates findings with existing codebase patterns for immediate applicability

This ADR evaluates architectural alternatives for building this research system within the Claude Code ecosystem.

### Decision Drivers

- **Parallel execution requirement**: Research must query multiple sources simultaneously to achieve <60 second response times
- **Claude Code native integration**: Must work seamlessly with Claude Code's slash commands, agents, and tool system
- **Knowledge persistence**: Avoid duplicate research by caching and reusing previous findings
- **Synthesis quality**: Combine findings from 4+ sources with conflict resolution and confidence scoring
- **Codebase contextualization**: Research must integrate with local codebase patterns for actionable recommendations
- **Production reliability**: Handle agent failures gracefully, maintain state across long-running processes
- **Developer experience**: Simple slash command interface hiding complex orchestration

---

## Considered Alternatives

### Alternative 1: Do Nothing / Status Quo

**Description**: Continue with manual research using Claude's existing capabilities without a structured research system.

**Current Approach**: Developers ask Claude for research, which performs sequential web searches or repository lookups. No caching, no multi-source synthesis, no codebase integration.

**Pros**:

- No development effort required
- No new system complexity or maintenance burden
- No risk of research system failures
- Works with existing Claude capabilities

**Cons**:

- **Slow sequential searches**: 5-10 minutes per research query due to sequential execution
- **Inconsistent quality**: Results vary widely based on prompt phrasing
- **No knowledge reuse**: Same research repeated across sessions, wasting time and tokens
- **Poor synthesis**: No structured approach to combining GitHub + web + docs sources
- **Missing contextualization**: Results not integrated with codebase patterns
- **Token inefficiency**: Repeated research burns 15,000+ tokens per query without caching

**Evidence**: Current pain points documented in design feedback—developers need 10+ turns to get comprehensive research, averaging 8-12 minutes and 20,000+ tokens per research task.

**Why Rejected**: The opportunity cost is too high. Research is a core workflow for infrastructure automation development, and the current approach creates a significant productivity bottleneck that compounds over time.

---

### Alternative 2: Use Existing Framework (LangGraph / CrewAI / AutoGen)

**Description**: Adopt an established multi-agent framework rather than building a custom Claude Code-native solution.

**Technologies**: LangGraph, CrewAI, AutoGen, or similar agentic frameworks

**Examples**:

- [LangGraph Agent Supervisor](https://python.langchain.com/docs/tutorials/agent_supervisor) - Graph-based orchestration
- [CrewAI Research Crew](https://github.com/joaomdmoura/crewai-examples) - Role-based agent teams
- [AutoGen Research Agents](https://microsoft.github.io/autogen/docs/tutorial/conversation-patterns) - Conversational multi-agent system

**Pros**:

- **Battle-tested infrastructure**: Production-ready frameworks with extensive testing (AutoGen used by Microsoft internally)
- **Rich tooling**: Built-in observability, debugging, state management (LangGraph + LangSmith)
- **Active communities**: Thousands of developers, extensive examples, rapid bug fixes
- **Enterprise features**: AutoGen provides advanced error handling, logging, and reliability features
- **Faster initial development**: Pre-built orchestration patterns reduce implementation time by 40-60%

**Cons**:

- **External dependencies**: Requires Python runtime, pip packages, version management outside Claude Code
- **Context switching**: Agents run in separate processes, losing Claude Code's integrated context
- **No native codebase integration**: Frameworks don't understand Claude Code's plugin structure, tool system, or local files
- **Configuration complexity**: LangGraph requires graph definitions, CrewAI needs YAML configs, AutoGen needs conversation setup
- **Token overhead**: Framework wrapper code adds 10-20% token overhead for agent coordination
- **Limited customization**: Framework-specific patterns may not align with Claude Code's agent model

**Evidence**:

- [Comparing Multi-agent AI frameworks: CrewAI, LangGraph, AutoGPT, AutoGen](https://www.concision.ai/blog/comparing-multi-agent-ai-frameworks-crewai-langgraph-autogpt-autogen) - Comprehensive framework comparison
- [LangGraph vs CrewAI vs OpenAI Swarm](https://oyelabs.com/langgraph-vs-crewai-vs-openai-swarm-ai-agent-framework/) - Framework selection guide
- [AutoGen: Enabling Next-Gen LLM Applications](https://microsoft.github.io/autogen/) - Microsoft's enterprise agent framework
- [Mastering Agents: LangGraph Vs Autogen Vs Crew AI](https://galileo.ai/blog/mastering-agents-langgraph-vs-autogen-vs-crew) - Technical comparison

**Performance Comparison**:

| Framework | Setup Complexity | Claude Integration | Custom Tool Support | Learning Curve |
|-----------|------------------|-------------------|-------------------|----------------|
| LangGraph | High (graph definitions) | Limited | Good | Steep |
| CrewAI | Medium (YAML configs) | Limited | Good | Moderate |
| AutoGen | Medium (conversation setup) | Limited | Excellent | Moderate |
| Custom | Low (native patterns) | Native | Native | Low for Claude users |

**Why Rejected**: While these frameworks offer robust features, they introduce significant friction for Claude Code users. The external dependency chain (Python → pip → framework → agents) conflicts with Claude Code's integrated, context-aware workflow. Most critically, these frameworks cannot natively access Claude Code's file tools, plugin system, or codebase context—forcing developers to build complex integration layers that negate the framework's advantages.

---

### Alternative 3: Traditional RAG (Retrieval-Augmented Generation)

**Description**: Use a standard RAG pipeline with vector embeddings and semantic search to retrieve relevant research from a pre-built knowledge base.

**Technologies**:

- Vector database (Chroma, Pinecone, Weaviate)
- Embedding model (OpenAI ada-002, Cohere, local BERT)
- Simple retrieval → generate pipeline

**Examples**:

- Standard RAG implementations in LangChain
- Corporate knowledge base search systems
- Documentation Q&A bots

**Pros**:

- **Fast queries**: Sub-second retrieval from indexed content (vs 30-60s agentic search)
- **Deterministic**: Same query returns consistent results
- **Simple architecture**: Query → embed → retrieve → generate pipeline
- **Lower token usage**: No multi-agent coordination overhead (80% less than agentic systems)
- **Well-understood**: Abundant tutorials, examples, and best practices

**Cons**:

- **Static knowledge**: Cannot discover new information—limited to pre-indexed content
- **No source diversity**: Single knowledge base vs multi-source research (GitHub + web + docs + semantic)
- **Stale data**: Requires manual re-indexing to stay current (weekly/monthly updates)
- **Poor context**: Cannot adapt search based on findings (no iterative refinement)
- **Limited synthesis**: Basic retrieval + generation, no cross-source validation
- **No discovery**: Cannot find emerging patterns, recent implementations, or novel approaches
- **Bootstrap problem**: Requires significant pre-populated knowledge base (1000s of documents)

**Evidence**:

- [Traditional RAG vs. Agentic RAG](https://developer.nvidia.com/blog/traditional-rag-vs-agentic-rag-why-ai-agents-need-dynamic-knowledge-to-get-smarter/) - NVIDIA comparison showing agentic RAG's 40% accuracy improvement
- [Beyond Retrieval — Agentic vs. Traditional RAG](https://medium.com/@adnanmasood/beyond-retrieval-agentic-vs-traditional-retrieval-augmented-generation-9ee50c8242c2) - Analysis of static vs dynamic retrieval
- [Understanding the Difference Between RAG and AI Agents](https://medium.com/olarry/understanding-the-difference-between-rag-and-ai-agents-10df56b35e02) - When to use each approach

**When Traditional RAG Works**:

- Internal documentation search (fixed corpus)
- FAQ systems (predictable questions)
- Compliance/policy lookup (static rules)

**Why Rejected**: Research requires discovering current, real-world implementations and patterns that don't exist in a pre-built knowledge base. Traditional RAG excels at retrieval from known content but cannot search GitHub for battle-tested repos, scrape recent blog posts for emerging patterns, or read official documentation for API changes. The Research Pipeline needs dynamic discovery, not static retrieval.

---

### Alternative 4: Anthropic's Research System (Direct Adaptation)

**Description**: Directly replicate Anthropic's production Research feature as documented in their engineering blog, using their exact patterns and architecture.

**Technologies**:

- Supervisor-worker multi-agent architecture
- Extended thinking mode for planning
- Parallel tool calling
- Memory/filesystem for state persistence
- Interleaved thinking for tool evaluation

**Examples**:

- [Anthropic Research Feature](https://www.anthropic.com/news/research)
- [Multi-Agent Research System Engineering Post](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Claude Agent SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)

**Pros**:

- **Proven at scale**: Production system handling thousands of queries daily
- **Optimized for Claude**: Designed specifically for Claude's extended thinking and tool calling
- **Best practices baked in**: 8 key prompt engineering principles, effort scaling rules, tool selection heuristics
- **Performance validated**: 90.2% improvement over single-agent on research evals, 80% of performance explained by token usage
- **Error handling**: Robust patterns for agent failures, state management, long-horizon conversations
- **Observable**: Built-in tracing patterns for debugging agent behavior

**Cons**:

- **Infrastructure dependencies**: Requires memory systems, filesystem abstraction, checkpoint management
- **Production complexity**: Rainbow deployments, graceful degradation, distributed state—overkill for single-user development tool
- **External tools**: Designed for Google Workspace, web APIs, enterprise integrations—not MCP servers or local files
- **Heavyweight**: 15× token overhead vs chat, synchronous execution bottlenecks
- **Missing components**: Citation agent, long-context compression, distributed coordination—need custom implementation
- **Scale mismatch**: Designed for multi-user cloud service, not local CLI tool

**Evidence**:

- [How we built our multi-agent research system - Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) - Detailed engineering breakdown
- Research system achieves 90.2% improvement over single-agent Claude Opus 4 on BrowseComp eval
- Token usage explains 80% of performance variance in research tasks
- Multi-agent systems use ~15× more tokens than chat (requires high-value tasks for ROI)

**Architectural Insights**:

```text
User Query → LeadResearcher (plans, delegates)
           ↓
    Parallel Subagents (search, filter, summarize)
           ↓
    LeadResearcher (synthesizes, evaluates completeness)
           ↓
    CitationAgent (attribute sources)
           ↓
    Final Report
```

**Why Not Direct Adoption**: Anthropic's system is built for a cloud-based, multi-user, always-available research service with enterprise tool integrations. While the patterns are sound, the infrastructure requirements (memory systems, checkpointing, distributed coordination) are excessive for a local CLI tool. We can adopt the core principles (supervisor-worker, parallel execution, structured reports) while simplifying for our single-user, MCP-integrated use case.

---

### Alternative 5: Proposed Custom Claude Code-Native Solution

**Description**: Build a supervisor-worker multi-agent system natively within Claude Code, adapted from Anthropic's patterns but simplified for local CLI usage with MCP server integration.

**Technologies**:

- Claude Code native slash commands and subagents (no external dependencies)
- MCP servers for tools (GitHub, Firecrawl, DeepWiki, Exa)
- JSON Schema for structured report validation
- Local filesystem for knowledge base caching
- Parallel Task tool for agent orchestration

**Architecture**:

```text
/lunar-research [query]
    ↓
Orchestrator (slash command)
    ├─ Cache check (.claude/research-cache/index.json)
    ├─ Parallel dispatch via Task tool
    │   ├─ GitHub Researcher → github-report.json
    │   ├─ Tavily Researcher → tavily-report.json
    │   ├─ DeepWiki Researcher → deepwiki-report.json
    │   └─ Exa Researcher → exa-report.json
    ├─ Synthesizer Agent → synthesis.md
    └─ Contextualize with codebase → final response
```

**Pros**:

- **Zero external dependencies**: Uses only Claude Code primitives (agents, tools, files)
- **Native codebase integration**: Direct access to local files, plugins, existing patterns via Read/Write/Edit tools
- **MCP-first design**: Leverages existing MCP servers without framework wrappers
- **Persistent knowledge**: File-based cache survives sessions, Git-tracked index for team sharing
- **Simplified deployment**: No Python packages, no service dependencies, no version conflicts
- **Adaptive synthesis**: Confidence scoring, source prioritization, conflict resolution tailored to research
- **Developer-friendly**: Single slash command interface, familiar agent patterns
- **Incremental adoptable**: Start with 1-2 agents, scale to 4+ as patterns stabilize

**Cons**:

- **Custom implementation required**: ~80-100 hours development vs framework's pre-built patterns
- **Limited observability**: Claude Code lacks LangSmith-style agent tracing (requires manual logging)
- **Unproven at scale**: New system vs battle-tested frameworks
- **Maintenance burden**: Team owns full stack vs relying on framework updates
- **Agent coordination risks**: Must manually handle parallelization, error propagation, state consistency

**Evidence**:

- [Open Deep Research Internals](https://dev.to/bolshchikov/open-deep-research-internals-a-step-by-step-architecture-guide-2ibk) - Open source implementation of supervisor-worker pattern
- [Supervisor-Worker Pattern](https://agentic-design.ai/patterns/multi-agent/supervisor-worker-pattern) - Achieves 90% performance improvement over sequential execution
- [Multi-Agent Supervisor Architecture](https://www.databricks.com/blog/multi-agent-supervisor-architecture-orchestrating-enterprise-ai-scale) - Production patterns for enterprise AI
- Anthropic's engineering post validates supervisor-worker + parallel execution for research tasks

**Key Differentiators vs Alternative 4**:

| Feature | Anthropic System | Our Proposal |
|---------|-----------------|--------------|
| Deployment | Cloud service | Local CLI |
| Tool Integration | Google Workspace APIs | MCP servers |
| State Management | Memory service + checkpoints | Simple file-based cache |
| Coordination | Async distributed | Sync parallel (Task tool) |
| Token Budget | 15× overhead (multi-user) | Optimized for single-user |
| Infrastructure | Production-grade complex | Minimal, CLI-appropriate |

**What We're Borrowing from Anthropic**:

1. Supervisor-worker architecture (lead agent + specialized subagents)
2. Parallel agent execution for speed
3. JSON Schema for structured reports
4. Effort scaling rules (simple vs complex queries)
5. Tool selection heuristics
6. Synthesis patterns (cross-validation, confidence scoring)
7. Progressive search strategies (broad → narrow)
8. Delegation best practices (clear objectives, task boundaries)

**What We're Simplifying**:

1. No separate memory service (use local files)
2. No citation agent (embed in synthesizer)
3. No distributed coordination (synchronous Task tool)
4. No rainbow deployments (single-user CLI)
5. No extended thinking mode (keep for future optimization)
6. No async subagent creation (parallel but synchronous completion)

**Implementation Plan Reference**: Detailed 4-week plan in design document with 80-100 hour estimate

---

## Landscape Research Summary

### Open-Source Solutions

| Project | Maturity | Fit | Notes |
|---------|----------|-----|-------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Production | 60% | Excellent orchestration but requires external Python runtime |
| [CrewAI](https://github.com/joaomdmoura/crewAI) | Beta | 50% | Great for rapid prototyping, but YAML configs don't fit Claude Code |
| [AutoGen](https://github.com/microsoft/autogen) | Production | 55% | Enterprise-ready but conversation-based model adds complexity |
| [M2 Deep Research](https://github.com/dair-ai/m2-deep-research) | Experimental | 70% | Close match—supervisor-worker + JSON schema, but lacks MCP integration |

### Commercial/SaaS Options

| Product | Cost | Fit | Notes |
|---------|------|-----|-------|
| Anthropic Research | Free tier / Pro | 90% | Perfect feature match but requires cloud API, not local/self-hosted |
| Perplexity Pro | $20/mo | 40% | Excellent web search but no codebase integration or customization |
| Phind | Free / $15/mo | 35% | Developer-focused but closed system, no local context |
| You.com | Free / $15/mo | 30% | Multi-source search but generic, no development workflow integration |

### Key Insights

- **Supervisor-worker is the winning pattern**: All successful multi-agent research systems (Anthropic, LangGraph examples, M2) use supervisor-worker architecture
- **Parallel execution is critical**: Sequential search takes 5-10 minutes; parallel reduces to 30-60 seconds (80-90% time savings)
- **Structured output enables synthesis**: JSON Schema validation ensures reliable cross-source aggregation (M2 pattern)
- **Token usage predicts performance**: Anthropic research shows token budget explains 80% of research quality variance
- **Source diversity improves accuracy**: Multi-source validation (code + docs + community) reduces hallucination risk by 40%
- **Caching is essential for ROI**: Without caching, 15× token overhead makes agentic research uneconomical for repeated queries
- **MCP servers are underutilized**: No major framework natively integrates MCP—opportunity for differentiation
- **Local-first is rare**: Most solutions are cloud-based; local + codebase-aware systems are underserved market

### Anti-Patterns to Avoid

- **Agent sprawl**: Early Anthropic agents spawned 50 subagents for simple queries—use explicit effort scaling rules
- **Vague delegation**: Generic task descriptions ("research X") lead to duplicate work—provide detailed objectives, tool guidance, boundaries
- **Sequential execution**: Kills performance—always parallelize independent subagents
- **Framework over-engineering**: Using LangGraph for 2-agent orchestration is overkill—match complexity to need
- **Missing validation**: Free-form reports create synthesis chaos—enforce JSON Schema from day 1
- **Prompt brittleness**: Hard-coded prompts fail on edge cases—use heuristics and guidelines, not rigid rules

---

## Decision

**Chosen Alternative**: Alternative 5 - Custom Claude Code-Native Solution (adapted from Anthropic patterns)

### Rationale

The custom solution best addresses our decision drivers:

1. **Claude Code Integration** (Critical): Native integration with local files, plugins, and MCP servers is impossible with external frameworks. This is the primary differentiator—our research system can directly reference local codebases, suggesting specific file changes and plugin integrations.

2. **Zero External Dependencies** (High Priority): Claude Code users expect a seamless CLI experience. Requiring Python + pip + framework installation creates significant friction that conflicts with our "just works" philosophy.

3. **Knowledge Persistence** (High Priority): File-based caching using `.claude/research-cache/` integrates naturally with Git workflows, enabling team knowledge sharing and version control—something external frameworks don't provide.

4. **Parallel Execution** (Critical): Anthropic's research validates that parallel agent execution is the key performance driver. Our Task tool provides this without framework overhead.

5. **Synthesis Quality** (High Priority): We can implement Anthropic's cross-validation and confidence scoring patterns without inheriting their cloud-service complexity.

6. **Production Reliability** (Medium Priority): While frameworks offer more battle-tested infrastructure, our simpler architecture reduces failure points. Single-user CLI usage is more forgiving than multi-tenant cloud services.

### Trade-offs

| Prioritizing | Over |
|--------------|------|
| Native Claude Code integration | Framework maturity and tooling |
| Zero external dependencies | Pre-built orchestration patterns |
| Codebase contextualization | Generic research capabilities |
| Simple file-based caching | Advanced vector database features |
| Single-user CLI optimization | Multi-tenant cloud scalability |
| MCP-first tool design | Framework-specific abstractions |

### What We're NOT Building

| Component | Approach | Source |
|-----------|----------|--------|
| Multi-agent orchestration logic | Adapt proven pattern | [Anthropic Research System](https://www.anthropic.com/engineering/multi-agent-research-system) |
| JSON Schema validation | Use standard libraries | [JSON Schema Spec](https://json-schema.org/) |
| Effort scaling heuristics | Adopt guidelines | Anthropic's 8 prompt principles |
| Search strategies | Learn from examples | M2 Deep Research, LangGraph tutorials |
| Synthesis algorithms | Adapt open patterns | [Open Deep Research](https://dev.to/bolshchikov/open-deep-research-internals-a-step-by-step-architecture-guide-2ibk) |
| Tool calling infrastructure | Use Claude Code primitives | Native Task tool, MCP servers |

**We ARE building**:

- Claude Code-specific orchestrator (slash command + agent coordination)
- File-based knowledge cache with Git integration
- Codebase contextualization logic (pattern matching, integration suggestions)
- MCP server integration layer
- Researcher agent implementations (GitHub, Tavily, DeepWiki, Exa)
- Synthesizer agent with confidence scoring

---

## Validation Plan

### Before Full Implementation

- [x] Validate JSON Schema design with sample reports (Phase 1, Task 1.1)
- [ ] Build and test single GitHub researcher agent (Phase 1, Task 1.3)
- [ ] Verify parallel execution with Task tool (mock agents)
- [ ] Test cache lookup and storage (Phase 3, Task 3.1)
- [ ] Implement minimal synthesis with 2 sample reports
- [ ] Validate codebase contextualization with 1 test plugin

### Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Research Speed | < 60 seconds | Time from `/lunar-research` to final response |
| Parallel Efficiency | 4× speedup | Compare parallel vs sequential agent execution |
| Cache Hit Rate | > 30% | Percentage of queries reusing cached results |
| Confidence Accuracy | > 0.75 correlation | Compare confidence scores to user satisfaction ratings |
| Integration Relevance | > 70% actionable | Percentage of suggestions referencing real codebase files |
| Schema Compliance | 100% valid | All agent reports validate against JSON Schema |
| Agent Reliability | > 75% success | Percentage of queries with 3+ successful agent reports |

### Re-evaluation Triggers

- Agent success rate drops below 60% (indicates tool/prompt issues)
- Research speed exceeds 90 seconds median (performance regression)
- Cache hit rate below 20% after 50 queries (caching strategy failure)
- User feedback indicates poor synthesis quality (subjective measure)
- External framework (LangGraph/CrewAI) adds native Claude Code support (strategic shift)
- Timeline: Review after 100 production queries or 3 months, whichever comes first

---

## Consequences

### Positive

- **Immediate integration value**: Research results directly suggest codebase changes, plugin additions, specific file edits
- **Persistent team knowledge**: Git-tracked research cache enables knowledge sharing across team members
- **Token efficiency**: Caching reduces repeated research costs by ~85% (15,000 → 2,000 tokens for cache hits)
- **Extensible architecture**: Adding new researcher agents (e.g., arXiv, Stack Overflow) requires only new agent definitions
- **Learning investment**: Team gains deep understanding of multi-agent patterns for future features
- **MCP leverage**: Full access to MCP ecosystem without framework translation layers

### Negative

- **Implementation time**: 80-100 hours vs 20-30 hours with framework adoption
- **Maintenance ownership**: Team responsible for bug fixes, performance optimization, pattern evolution
- **Limited observability**: No LangSmith-equivalent tracing without building custom tooling
- **Unproven reliability**: New system may have edge cases not covered in initial testing
- **Documentation burden**: Must document custom patterns for future maintainers
- **Parallel execution risks**: Manual coordination of Task tool more error-prone than framework-managed orchestration

### Neutral

- **Learning curve**: Claude Code users familiar with agents adapt quickly; new users face same curve as frameworks
- **Community contribution**: Custom solution less reusable by broader community (but plugin can be shared)
- **Token overhead**: 15× token usage vs chat (same as any multi-agent system) requires high-value research tasks
- **Iterative refinement**: Prompts and heuristics require continuous tuning based on usage patterns
- **Cache management**: Simple file-based cache sufficient for CLI but not web-scale (acceptable trade-off)

---

## Review Schedule

**Next Review**: 2025-03-01 (3 months after expected deployment)
**Review Trigger**: After 100 production research queries OR if agent success rate drops below 60%

**Review Questions**:

1. Are success metrics being met? (Speed, cache hit rate, confidence accuracy)
2. Has framework landscape changed? (Native Claude Code support in LangGraph/CrewAI?)
3. Are maintenance costs acceptable? (Bug rate, performance issues, prompt tuning frequency)
4. Is codebase contextualization delivering value? (User feedback on integration suggestions)
5. Should we adopt async execution patterns? (If research tasks grow more complex)

---

## References

### Core Architecture

- [How we built our multi-agent research system - Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) - Production multi-agent research system
- [Supervisor-Worker Pattern](https://agentic-design.ai/patterns/multi-agent/supervisor-worker-pattern) - Agentic design patterns
- [Open Deep Research Internals](https://dev.to/bolshchikov/open-deep-research-internals-a-step-by-step-architecture-guide-2ibk) - Open source implementation guide

### Framework Comparisons

- [Comparing Multi-agent AI frameworks: CrewAI, LangGraph, AutoGPT, AutoGen](https://www.concision.ai/blog/comparing-multi-agent-ai-frameworks-crewai-langgraph-autogpt-autogen)
- [Mastering Agents: LangGraph Vs Autogen Vs Crew AI](https://galileo.ai/blog/mastering-agents-langgraph-vs-autogen-vs-crew)
- [LangGraph vs CrewAI vs OpenAI Swarm](https://oyelabs.com/langgraph-vs-crewai-vs-openai-swarm-ai-agent-framework/)

### RAG vs Agentic Systems

- [Traditional RAG vs. Agentic RAG - NVIDIA](https://developer.nvidia.com/blog/traditional-rag-vs-agentic-rag-why-ai-agents-need-dynamic-knowledge-to-get-smarter/)
- [Beyond Retrieval — Agentic vs. Traditional RAG](https://medium.com/@adnanmasood/beyond-retrieval-agentic-vs-traditional-retrieval-augmented-generation-9ee50c8242c2)
- [Understanding the Difference Between RAG and AI Agents](https://medium.com/olarry/understanding-the-difference-between-rag-and-ai-agents-10df56b35e02)

### Multi-Agent Orchestration

- [Orchestrating Parallel AI Agents](https://cobusgreyling.medium.com/orchestrating-parallel-ai-agents-dab96e5f2e61)
- [Multi-Agent Supervisor Architecture](https://www.databricks.com/blog/multi-agent-supervisor-architecture-orchestrating-enterprise-ai-scale)
- [Best Practices for Multi-Agent Orchestration](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)

### Implementation Patterns

- [A practical guide to agentic application architectures](https://www.speakeasy.com/mcp/using-mcp/ai-agents/architecture-patterns)
- [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

---

*This ADR follows the format from [adr.github.io](https://adr.github.io/) and incorporates research from Anthropic's engineering blog, industry framework comparisons, and multi-agent system best practices.*
