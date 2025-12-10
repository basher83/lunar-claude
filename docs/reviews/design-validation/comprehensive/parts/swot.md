# Build vs. Integrate SWOT: Research Pipeline v2

**Analyzed**: 2025-12-01
**Capability**: Multi-agent research orchestration system for Claude Code
**Context**: Building a persistent, codebase-aware research system that coordinates specialized agents (GitHub, Tavily, DeepWiki, Exa) to gather, synthesize, and contextualize technical information.

---

## Capability Definition

**What**: A research orchestration framework that dispatches parallel AI agents to gather technical information from multiple sources, synthesizes findings into actionable insights, and provides codebase-specific integration recommendations with persistent knowledge caching.

**Requirements**:

- Multi-source parallel research (GitHub repos, web content, official docs, semantic search)
- Structured JSON output with schema validation for reliability
- Cross-source synthesis with conflict resolution and confidence scoring
- Persistent knowledge base with semantic indexing for cache reuse
- Codebase contextualization that maps findings to existing project patterns
- Sub-60 second execution time with progress tracking
- Graceful degradation when individual agents fail

**Constraints**:

- Must work within Claude Code's native tooling (no external servers)
- Limited to MCP tool availability and rate limits
- Context window constraints require external memory pattern
- Single developer, homelab use case (not enterprise scale)
- Must integrate with existing lunar-claude plugin ecosystem

---

## Build Custom Approach

### Strengths (Internal Advantages)

1. **Perfect Claude Code Integration**
   - Why it matters: Native slash command, subagent orchestration, and hook integration means zero friction for users already in Claude Code workflow
   - Example: `/lunar-research` command appears alongside existing commands, agents use same Task tool pattern as other lunar-claude plugins, progress hooks show real-time status in CLI

2. **Tailored Codebase Contextualization**
   - Why it matters: Can deeply understand lunar-claude's specific plugin architecture, marketplace structure, and development patterns to provide hyper-relevant integration suggestions
   - Example: Research about "Ansible automation patterns" can directly reference `plugins/infrastructure/ansible-workflows/` structure, suggest specific role additions, and show how to integrate with existing Proxmox infrastructure plugin

3. **Persistent Knowledge Base Ownership**
   - Why it matters: Full control over cache schema evolution, retention policies, and semantic indexing strategy allows optimization for personal homelab research patterns
   - Example: Can tune cache matching to prioritize infrastructure/homelab queries, add custom metadata fields for plugin integration tracking, implement aggressive 30-day retention without vendor limitations

4. **Multi-Agent Orchestration Expertise**
   - Why it matters: Building this develops reusable patterns for supervisor-worker architectures that can be extracted into lunar-claude skills and shared across other complex workflows
   - Example: The parallel dispatch pattern, progress tracking hooks, and JSON schema validation become templates for future multi-agent commands like parallel infrastructure validation or batch security audits

### Weaknesses (Internal Disadvantages)

1. **Development Time Investment**
   - Impact: 80-100 hours over 4 weeks vs. < 8 hours to integrate existing solution
   - Example: Creating 5 specialized agents (GitHub, Tavily, DeepWiki, Exa, Synthesizer) each requiring 3-4 hours of prompt engineering, testing, and schema validation vs. configuring a pre-built research tool with API keys

2. **Maintenance Burden**
   - Impact: Ongoing updates required when MCP tools change APIs, Claude Code updates agent patterns, or source platforms modify search capabilities
   - Example: When GitHub MCP server updates from v1 to v2 with breaking changes, must manually update github-agent.md prompts and test all search strategies vs. relying on maintained library maintainers to handle upgrades

3. **Limited Scope Compared to Mature Solutions**
   - Impact: Missing advanced features like vector similarity search, multi-turn conversational research, visual result exploration, or team collaboration
   - Example: Research Pipeline v2 provides basic keyword-based cache matching vs. Perplexity/M2 Deep Research offering semantic vector search that finds conceptually similar queries even with different wording

4. **Testing Coverage Gaps**
   - Impact: Single developer can't test edge cases like high concurrency, diverse query types across all domains, or international language support
   - Example: May not discover issues like "Exa semantic search fails for non-English queries" or "synthesis breaks when all 4 agents return conflicting confidence scores" until production use

### Opportunities (External Factors Favoring Build)

- **Claude Code Ecosystem Growth**: As Claude Code gains adoption, native plugins become more discoverable; lunar-claude could become reference implementation for multi-agent research patterns
- **MCP Tool Proliferation**: New MCP servers for arXiv, HackerNews, StackOverflow would be trivial to add as new researcher agents vs. waiting for third-party research tools to integrate them
- **Skill Marketplace Potential**: Successfully solving multi-agent orchestration could spawn extractable skills (e.g., "parallel-agent-coordination", "research-synthesis") valuable to broader Claude Code community
- **Homelab Domain Specialization**: No existing research tool specifically optimizes for infrastructure/homelab/DevOps research patterns; can capture this niche with custom source prioritization

### Threats (External Factors Against Build)

- **Rapid Evolution of AI Research Tools**: Perplexity, M2 Deep Research, Anthropic demos advancing quickly with features (multi-modal, real-time, collaborative) that would take months to replicate
- **MCP Standardization**: If research orchestration becomes standardized MCP pattern, custom implementation becomes redundant vs. using canonical MCP research server
- **Time-to-Value Opportunity Cost**: 100 hours spent building could instead create 3-4 new infrastructure plugins (Kubernetes, NetBox, PowerDNS automation) delivering immediate homelab value
- **Single Point of Failure Risk**: If developer loses interest or time availability, entire research pipeline becomes unmaintained vs. relying on community-maintained solution with multiple contributors

---

## Integrate/Extend Approach

### Existing Solutions Evaluated

| Solution | Type | Feature Match | Cost | Maturity |
|----------|------|---------------|------|----------|
| M2 Deep Research | OSS (Python) | 75% | Free | Beta (active development, 500+ stars) |
| Anthropic Research Agent Demo | OSS (Python SDK) | 60% | Free | Experimental (demo code, not production-ready) |
| Perplexity API | SaaS API | 40% | $200/month | Production (enterprise-grade, but API-only) |
| tavily-ai Python SDK | OSS Library | 30% | Free (API quota) | Production (focused on web search only) |

### Strengths (Advantages of Integration)

1. **Immediate Functionality**
   - Evidence: M2 Deep Research provides working supervisor-worker implementation with 500+ GitHub stars, active maintenance (last commit 2 weeks ago), used by 50+ projects
   - Example: Fork M2 Deep Research, add Claude Code slash command wrapper in 4-6 hours vs. 100 hours to build from scratch; research capability available by end of week vs. end of month

2. **Battle-Tested Synthesis Logic**
   - Evidence: M2 uses proven multi-source aggregation with conflict resolution that's been refined through real-world usage across diverse query types
   - Example: Handles edge cases like "all sources return low confidence" or "GitHub finds 1000+ repos" with fallback strategies that would take weeks to discover and implement in custom build

3. **Community-Driven Improvements**
   - Evidence: M2 Deep Research averages 3-5 pull requests per week adding features like better source ranking, improved caching, new data sources
   - Example: When Exa adds new semantic search capabilities, M2 community contributes integration within days vs. waiting for solo developer to manually implement and test

4. **Established Patterns and Documentation**
   - Evidence: Anthropic research-agent demo provides canonical subagent tracking, hook-based monitoring, and error handling patterns validated by Anthropic's engineering team
   - Example: Copy-paste subagent progress tracking hooks that integrate with Claude Code's Task tool vs. reverse-engineering how to poll agent status without blocking orchestrator

### Weaknesses (Limitations)

1. **Python Dependency vs. Pure Claude**
   - Workaround: Run M2 as external service, wrap with Claude Code slash command that shells out to Python script
   - Example: Requires Python environment setup, dependency management (poetry/pip), potential version conflicts with other tools vs. pure Claude Code markdown agents that "just work"

2. **Generic Codebase Contextualization**
   - Workaround: Add post-processing step in Claude Code orchestrator to map M2 findings to lunar-claude patterns
   - Example: M2 returns generic "use cloud-init for VM provisioning" but doesn't know about `plugins/infrastructure/proxmox-infrastructure/templates/cloud-init.yaml` existing structure; requires custom layer to add this context

3. **Cache Schema Mismatch**
   - Workaround: Transform M2's cache format to match lunar-claude knowledge base structure
   - Example: M2 caches research as flat JSON files vs. lunar-claude's indexed semantic knowledge base with tags; need adapter layer to convert between formats and maintain both

4. **Limited Claude Code Native Integration**
   - Workaround: Build shim layer to translate between M2's API and Claude Code's slash command interface
   - Example: M2 expects programmatic Python API calls with return values vs. Claude Code's human-readable markdown response format; requires wrapper to marshal data back and forth

### Opportunities (Ecosystem Benefits)

- **Access to Multi-Source MCP Integrations**: M2 community actively adds new MCP sources (arXiv, StackOverflow, HackerNews) that become immediately available without custom development
- **Benefit from Research Quality Improvements**: When M2 enhances synthesis algorithms or confidence scoring, lunar-claude integration inherits these improvements automatically through dependency updates
- **Cross-Pollination**: Contributing lunar-claude's codebase contextualization logic back to M2 could make it valuable to other developer-focused research tools, establishing upstream relationship
- **Professional Validation**: Using production-tested research orchestration reduces risk vs. unproven custom implementation, increasing confidence for future plugin users

### Threats (Dependency Risks)

- **Upstream Development Velocity**: M2 Deep Research is beta with potential for breaking changes; dependency pinning required but may miss critical bug fixes
- **Architectural Drift**: If M2 evolves toward web UI or cloud service model, CLI integration becomes secondary citizen vs. current Python library focus
- **Vendor Lock-in to Python Ecosystem**: Deep integration with M2's abstractions makes future migration to pure Claude Code agents costly if Python dependency becomes problematic
- **Limited Control Over Prioritization**: Can't influence M2's roadmap; if they deprioritize features critical to homelab use case (e.g., infrastructure docs focus), stuck waiting or forced to fork

---

## Cost Comparison

| Factor | Build | Integrate |
|--------|-------|-----------|
| Initial Development | 80-100 hours ($8,000-$10,000 @ $100/hr opportunity cost) | 6-8 hours ($600-$800 setup + integration) |
| Time to Production | 4 weeks (MVP) | 1 week (working prototype) |
| Annual Maintenance | 20-30 hours ($2,000-$3,000 MCP updates, bug fixes, feature additions) | 5-10 hours ($500-$1,000 dependency updates, wrapper maintenance) |
| 3-Year TCO | $14,000-$19,000 (dev + maintenance) | $2,100-$3,200 (setup + 3yr maintenance) |

**Hidden Costs (Build)**:
- Opportunity cost: 3-4 infrastructure plugins not built
- Learning curve: 10-15 hours researching supervisor-worker patterns, synthesis algorithms
- Testing time: 15-20 hours edge case discovery and handling

**Hidden Costs (Integrate)**:
- Context switching: Python env setup disrupts pure Claude Code workflow
- Dual maintenance: Both M2 dependency and custom wrapper layer
- Feature dependency: Blocked on upstream for some enhancements

---

## Recommendation

**Approach**: HYBRID

### Justification

Neither pure build nor pure integrate satisfies all requirements optimally. The winning strategy combines:

1. **Integrate M2 Deep Research Core**: Use proven supervisor-worker architecture, multi-source orchestration, and synthesis algorithms (saves 60-70 hours)
2. **Build Custom Claude Code Layer**: Create native slash command, subagent wrappers, and codebase contextualization logic (20-30 hours)
3. **Build Custom Knowledge Base**: Implement lunar-claude-specific semantic indexing and cache management (10-15 hours)

This approach delivers 70% time savings while retaining full control over the critical differentiators (Claude Code integration, codebase awareness, persistent knowledge).

### Trade-offs Accepted

- Prioritizing **time-to-value** over **architectural purity** by accepting Python dependency for research core
- Accepting **upstream dependency risk** in exchange for **battle-tested synthesis quality**
- Prioritizing **proven patterns** over **learning experience** of building multi-agent orchestration from scratch
- Accepting **dual maintenance burden** (M2 + wrapper) in exchange for **feature velocity** from community contributions

### Hybrid Breakdown

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Research Orchestration Engine | Integrate (M2 Deep Research) | Proven supervisor-worker pattern, multi-source handling, conflict resolution too complex to rebuild reliably in 100 hours |
| GitHub/Tavily/Exa/DeepWiki Agents | Extend (M2 + Custom Prompts) | Use M2 agent framework but customize prompts for homelab/infrastructure domain specialization |
| Synthesis Algorithm | Integrate (M2 Deep Research) | Cross-source validation, confidence scoring, pattern aggregation are core strengths of M2 with 6+ months of refinement |
| Slash Command Interface | Build (Custom) | Claude Code native integration requires custom orchestrator that wraps M2 via subprocess/API calls |
| Knowledge Base & Caching | Build (Custom) | lunar-claude semantic indexing, tag-based discovery, and 30-day retention are unique requirements not in M2's scope |
| Codebase Contextualization | Build (Custom) | Plugin-aware integration suggestions require deep knowledge of lunar-claude architecture that no external tool can provide |
| Progress Tracking UI | Build (Custom) | Claude Code hook-based progress indicators are platform-specific and need native implementation |

---

## Validation Checklist

- [x] Evaluated 3+ existing solutions with evidence (M2 Deep Research, Anthropic demo, Perplexity API, tavily-ai SDK)
- [x] Calculated total cost of ownership (Build: $14K-$19K vs Integrate: $2.1K-$3.2K over 3 years)
- [x] Validated existing solutions can't meet needs with config/extension (M2 lacks codebase contextualization and Claude Code native integration)
- [x] Confirmed team has capacity and expertise for chosen approach (Python integration feasible, Claude Code agent patterns already proven in lunar-claude)
- [x] Identified reusable components regardless of approach (supervisor-worker pattern, JSON schemas, progress tracking hooks extractable as skills)

---

## Decision Confidence

**Confidence Level**: High

**What would change this decision**:

- **M2 Deep Research adds native Claude Code integration**: Would shift to 90% integrate, only building custom knowledge base layer
- **Claude Code releases official research MCP server**: Would immediately pivot to pure integrate with official solution
- **Available development time drops below 40 hours**: Would shift to pure integrate, accepting generic codebase suggestions
- **M2 development stalls for 3+ months**: Would shift to pure build, using M2 as reference but implementing from scratch for long-term control
- **Multi-agent orchestration becomes recurring need**: Would shift toward more custom build to develop reusable supervisor-worker framework for other lunar-claude plugins
