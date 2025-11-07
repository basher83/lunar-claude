# Research Pipeline Design: Review & Feedback

**Date:** 2025-11-06
**Reviewer:** Claude Code Architecture Review
**Document Reviewed:** `2025-11-06-research-pipeline-design.md`
**Status:** Design Phase Feedback

## Executive Summary

This document provides constructive, actionable feedback on the Research Pipeline design. The design is **fundamentally sound** with excellent architectural thinking, but requires clarification on several implementation details and architectural constraints before coding begins.

**Overall Assessment:** Strong design with clear separation of concerns, good extensibility, and alignment with Claude Code patterns. Main gaps are in implementation specifics and architectural layer definitions.

---

## Strengths

### 1. **Clear Separation of Concerns**
The design correctly separates researchers (domain experts) from orchestrator (decision-maker). This prevents architectural violations and maintains clean boundaries.

### 2. **Caching Strategy**
The research-then-generate decoupling is excellent. One expensive research run → multiple cheap documentation outputs is a powerful pattern.

### 3. **Alignment with Multi-Agent Patterns**
The design correctly applies orchestrator/scout-builder patterns from `multi-agent-composition` skill. Researchers are scouts, orchestrator is the builder.

### 4. **Extensibility**
LLM-driven orchestrator enables organic growth without code changes—new researchers/documenters integrate automatically.

---

## Critical Issues & Recommendations

### 1. Sub-Agent Nesting Constraint ⚠️ **CRITICAL**

**Issue:** The design implies researchers are sub-agents, but Claude Code has a hard constraint: **sub-agents cannot nest other sub-agents**. If the orchestrator is also a sub-agent, this breaks the architecture.

**Current Ambiguity:**
- Is orchestrator a primary agent or sub-agent?
- Can orchestrator spawn researchers if orchestrator is a sub-agent? (No—hard limit)

**Recommendation:** Clarify the architecture layer specification:

**Option A: Orchestrator as Primary Agent** (Recommended)
- Orchestrator = Primary agent (not a sub-agent)
- Researchers = Sub-agents invoked in parallel by orchestrator
- Documenters = Sub-agents invoked sequentially/parallel by orchestrator
- **Constraint:** Researchers cannot spawn other researchers (sub-agents cannot nest)

**Option B: Orchestrator as Skill**
- Orchestrator = Skill that orchestrates researchers
- Researchers = Sub-agents invoked via SlashCommand tool
- Documenters = Sub-agents invoked via SlashCommand tool
- **Trade-off:** Loses some parallelism benefits, but follows composition rules

**Option C: Orchestrator as Skill, Researchers as Skills** (Not Recommended)
- Loses parallelism benefits
- No context isolation
- Doesn't match the design intent

**Action Required:**
Add an "Architecture Layer Specification" section to the design document:

```markdown
## Architecture Layer Specification

- **Orchestrator:** Primary agent (not a sub-agent)
- **Researchers:** Sub-agents invoked in parallel by orchestrator
- **Documenters:** Sub-agents invoked sequentially or in parallel by orchestrator
- **Critical Constraint:** Researchers cannot spawn other researchers (sub-agents cannot nest)
- **Tool Usage:** Orchestrator uses SlashCommand tool to invoke researcher sub-agents
```

---

### 2. Missing Researcher Prompt Templates ⚠️ **HIGH PRIORITY**

**Issue:** No specification for researcher sub-agent prompts. Without standardized templates, researchers may not follow the reporting protocol consistently.

**Impact:** Inconsistent reporting format → orchestrator can't make good decisions → poor research quality

**Recommendation:** Add researcher prompt template section to design:

```markdown
## Researcher Sub-Agent Prompt Template

Each researcher sub-agent should follow this structure:

```yaml
---
name: deepwiki-researcher
description: Specialized researcher using DeepWiki MCP to find official documentation
tools: [DeepWiki MCP tools, Read, Grep]
model: sonnet
---

# DeepWiki Researcher

## Purpose
Research [TARGET] using DeepWiki MCP to find official documentation, architecture specs, and API references.

## Research Dimensions
1. Architecture & Code Structure
2. API Surface & Contracts
3. Usage Patterns & Examples
4. Best Practices & Gotchas
5. Testing & Validation
6. Ecosystem & Integration

## Reporting Protocol
Report findings in this exact format:
{
  "researcher": "deepwiki",
  "confidence": 0.0-1.0,
  "completeness": "none|partial|comprehensive",
  "findings": {
    "architecture": "[prose findings]",
    "api_surface": "[prose findings]",
    "usage_patterns": "[prose findings]",
    "best_practices": "[prose findings]",
    "testing": "[prose findings]",
    "ecosystem": "[prose findings]"
  },
  "gaps": ["list of missing information"]
}

## Critical Constraints
- Report ONLY what you found and what's missing
- DO NOT recommend other researchers
- DO NOT make orchestration decisions
- DO NOT reference other researchers' findings
- Confidence score: 0.0 = no findings, 1.0 = comprehensive coverage
- Completeness: "none" = no relevant info, "partial" = some dimensions covered, "comprehensive" = all dimensions covered
```

**Action Required:**
- Create prompt templates for all 4 MVP researchers (DeepWiki, Firecrawl, GitHub, Web Search)
- Include in design document or separate `researcher-templates/` directory
- Test templates ensure consistent reporting format

---

### 3. Orchestrator Decision Logic Underspecified ⚠️ **HIGH PRIORITY**

**Issue:** "LLM-driven" is too vague. Without concrete decision criteria, orchestrator may be inconsistent, expensive, or make poor decisions.

**Impact:** Unpredictable behavior, high token costs, poor research quality

**Recommendation:** Add decision framework section:

```markdown
## Orchestrator Decision Framework

### Researcher Selection Logic

**Target Type Analysis:**
- GitHub repo → Always deploy GitHub researcher
- Documentation site → Always deploy DeepWiki researcher
- Blog post/tutorial → Always deploy Firecrawl researcher
- Unknown → Deploy all researchers

**Output Type Requirements:**
- Skill → Needs: architecture, API, patterns, best practices
- Dev Docs → Needs: quickstart, examples, common pitfalls
- API Ref → Needs: comprehensive API surface

**Confidence Thresholds:**
- High confidence (≥0.8) → Proceed to documenters
- Medium confidence (0.5-0.8) → Deploy complementary researchers
- Low confidence (<0.5) → Deploy all researchers + web search

### Re-tasking Logic

- If gaps identified in critical dimensions → Deploy complementary researchers
- If all researchers report low confidence → Deploy web search researcher
- Maximum 2 re-tasking rounds to prevent infinite loops
- If still insufficient after 2 rounds → Report to user with partial findings

### Complementary Researcher Mapping

- DeepWiki gaps → GitHub researcher (for code examples)
- GitHub gaps → Firecrawl researcher (for community content)
- Firecrawl gaps → Web Search researcher (for scattered resources)
- All gaps → Web Search researcher (last resort)

### Sufficiency Criteria

Research is sufficient when:
- Confidence ≥ 0.7 AND completeness ≥ "partial" for critical dimensions
- OR confidence ≥ 0.5 AND completeness = "comprehensive"
- Critical dimensions depend on output type (see Output Type Requirements)
```

**Action Required:**
- Define concrete decision rules while keeping LLM flexibility for edge cases
- Add to design document
- Consider creating decision matrix table for quick reference

---

### 4. Cache Format & Versioning ⚠️ **MEDIUM PRIORITY**

**Issue:** Cache structure is defined, but no versioning or migration strategy. Future changes to cache format will break existing caches.

**Recommendation:** Add cache versioning:

```markdown
## Cache Versioning

### Cache Schema Version

```json
{
  "version": "1.0.0",
  "target": "jina-ai/MCP",
  "timestamp": "2025-11-06T23:45:00Z",
  "cache_format_version": "1.0",
  "researchers": {
    "deepwiki": { ... },
    "github": { ... },
    "firecrawl": { ... }
  },
  "metadata": {
    "orchestrator_assessment": "comprehensive",
    "research_dimensions_covered": [...],
    "token_usage": {
      "total": 45000,
      "per_researcher": {
        "deepwiki": 12000,
        "github": 15000,
        "firecrawl": 18000
      }
    }
  }
}
```

### Migration Strategy

- If `cache_format_version` < current → Re-research or migrate
- Add `staleness_days` field for future staleness detection
- Version bump triggers: schema changes, new fields, breaking changes
```

**Action Required:**
- Define cache schema version (start at "1.0")
- Document migration strategy
- Add version field to cache structure

---

### 5. Error Handling & Partial Results ⚠️ **MEDIUM PRIORITY**

**Issue:** Error handling marked "Out of scope for MVP" is risky. Basic error handling is essential for a usable system.

**Recommendation:** Add minimal error handling for MVP:

```markdown
## MVP Error Handling

### Researcher Failures

**MCP Tool Unavailable:**
- If DeepWiki MCP unavailable → Skip DeepWiki researcher, log warning
- Continue with available researchers
- Report partial availability to user

**Researcher Timeout/Failure:**
- If researcher fails → Log error, continue with other researchers
- Mark researcher as "failed" in cache
- If all researchers fail → Report to user, suggest manual research

**Partial Results:**
- Cache what was found, mark as "incomplete"
- Set `completeness: "partial"` in cache metadata
- Allow documenters to work with partial data (with warnings)

### Documenter Failures

**Generation Failure:**
- If documenter fails → Report error, preserve cached research
- User can retry documenter without re-researching
- Log failure reason for debugging

**Validation Failure:**
- If generated artifact fails validation → Report to user
- Preserve research cache
- Allow manual fixes

### Cache Corruption

- If cache file corrupted → Re-research automatically
- Log corruption event
- Consider cache backup strategy (future)
```

**Action Required:**
- Define minimal error handling for MVP
- Add to design document
- Consider error recovery strategies

---

### 6. Cost Estimation & Budgets ⚠️ **MEDIUM PRIORITY**

**Issue:** Research can be expensive (many LLM calls), but no cost visibility or limits. Users may accidentally trigger expensive operations.

**Recommendation:** Add cost awareness:

```markdown
## Cost Management (MVP)

### Cost Estimation

Before starting research, orchestrator estimates:
- Number of researchers to deploy
- Estimated token usage per researcher
- Estimated total cost (if cost API available)

**Estimation Formula:**
- DeepWiki: ~10-15k tokens (depends on doc size)
- GitHub: ~15-20k tokens (depends on repo size)
- Firecrawl: ~15-25k tokens (depends on pages scraped)
- Web Search: ~10-15k tokens (depends on results)

### User Approval

- If estimated cost > threshold (e.g., 50k tokens) → Request user approval
- Show cost breakdown: "Research will use ~50k tokens (~$0.50). Continue?"
- User can approve, modify (fewer researchers), or cancel

### Cost Tracking

- Log actual token usage to cache metadata
- Enable cost analysis for future optimization
- Track cost per researcher for optimization insights
```

**Action Required:**
- Add cost estimation logic
- Define approval thresholds
- Add cost tracking to cache metadata

---

### 7. Output Location & Naming Convention ⚠️ **HIGH PRIORITY**

**Issue:** Left as "open question" but needed for MVP. Without this, documenters don't know where to write files.

**Recommendation:** Propose a convention:

```markdown
## Output Location Convention (Proposed)

### Default Structure

```
.claude/research-outputs/<normalized-target-name>/
├── skills/
│   └── <tool-name>-guide/
│       ├── SKILL.md
│       └── [supporting files]
├── docs/
│   ├── ONBOARDING.md
│   ├── API_REF.md
│   └── TUTORIAL.md
└── cache/
    └── research-cache.json
```

### Naming Convention

**Target Normalization:**
- `owner/repo` → `owner-repo` (lowercase, hyphens)
- `blog-post-url` → `blog-post-url` (normalize URL)
- Special chars → hyphens

**Skill Names:**
- Format: `using-<tool-name>` (e.g., `using-jina-mcp`)
- Alternative: `<tool-name>-guide` (e.g., `jina-mcp-guide`)
- User preference: Allow override via flag

**User Override:**
- `--output-dir` flag for custom location
- `--skill-name` flag for custom skill name
```

**Action Required:**
- Decide on output location convention
- Document in design
- Implement in documenters

---

### 8. Progress Visibility ⚠️ **MEDIUM PRIORITY**

**Issue:** No visibility into research progress. Users don't know if system is working or stuck.

**Recommendation:** Add progress reporting:

```markdown
## Progress Reporting (MVP)

### Research Phase

**Real-time Updates:**
- "Deploying DeepWiki researcher..."
- "DeepWiki researcher: Found architecture docs (confidence: 0.9)"
- "Deploying GitHub researcher..."
- "GitHub researcher: Found examples (confidence: 0.7)"

**Summary After Each Researcher:**
- "DeepWiki complete: Architecture and API docs found"
- "GitHub complete: Code examples found, missing test patterns"

**Final Summary:**
- "Research complete: 3/4 researchers succeeded"
- "Overall confidence: 0.85, Completeness: comprehensive"
- "Cached to: .claude/research-cache/jina-ai-mcp.json"

### Documentation Phase

- "Generating Skill document..."
- "Skill document complete: 2,450 tokens"
- "Writing to: .claude/research-outputs/jina-ai-mcp/skills/using-jina-mcp/SKILL.md"
- "Dev onboarding guide complete: 1,800 tokens"
```

**Action Required:**
- Define progress reporting format
- Add to orchestrator implementation
- Consider progress hooks for observability (future)

---

### 9. Researcher Tool Constraints ⚠️ **MEDIUM PRIORITY**

**Issue:** Researchers need specific tools, but no tool restrictions specified. Researchers might accidentally modify files or use wrong tools.

**Recommendation:** Specify tool restrictions:

```markdown
## Researcher Tool Constraints

### DeepWiki Researcher
- **Allowed Tools:** DeepWiki MCP tools only
- **Restricted:** No file writing (read-only research)
- **Rationale:** Should only read/research, never write

### GitHub Researcher
- **Allowed Tools:** GitHub MCP + Read file tools
- **Restricted:** No file writing (read-only research)
- **Rationale:** Should only read code/examples, never modify

### Firecrawl Researcher
- **Allowed Tools:** Firecrawl MCP tools only
- **Restricted:** No file writing (read-only research)
- **Rationale:** Should only scrape/read web content

### Web Search Researcher
- **Allowed Tools:** Firecrawl search capability only
- **Restricted:** No file writing (read-only research)
- **Rationale:** Should only search, never write

**Implementation:** Use sub-agent `tools` field to restrict tool access
```

**Action Required:**
- Define tool restrictions for each researcher
- Document in researcher prompt templates
- Enforce via sub-agent tool configuration

---

### 10. Skill Documenter Integration ⚠️ **LOW PRIORITY**

**Issue:** Mentions leveraging "skill-creator skill" but unclear how. Integration approach affects implementation.

**Recommendation:** Clarify integration:

```markdown
## Skill Documenter Implementation

### Option A: Use skill-creator as Reference (Recommended for MVP)
- Load skill-creator SKILL.md as reference
- Follow its patterns and structure
- Generate SKILL.md following same format
- **Pros:** Simple, no dependencies
- **Cons:** Must maintain format manually

### Option B: Invoke skill-creator via SlashCommand
- Use SlashCommand tool to invoke skill-creator
- Pass research findings as context
- Let skill-creator generate structure
- **Pros:** Reuses existing skill, consistent format
- **Cons:** Adds dependency, may need skill-creator modifications

### Option C: Hybrid Approach
- Use skill-creator SKILL.md as template
- Generate SKILL.md programmatically
- Validate against skill-creator patterns
- **Pros:** Best of both worlds
- **Cons:** More complex

**Recommendation:** Option A for MVP, Option B for v2
```

**Action Required:**
- Decide on skill-creator integration approach
- Document decision in design
- Implement accordingly

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
1. ✅ Resolve architecture layer (orchestrator vs sub-agents)
2. ✅ Create researcher prompt templates
3. ✅ Define cache schema with versioning
4. ✅ Decide output location convention

### Phase 2: Core Functionality (Week 2-3)
5. ✅ Build orchestrator with decision framework
6. ✅ Implement 4 researchers with prompt templates
7. ✅ Implement cache storage/retrieval
8. ✅ Add basic error handling

### Phase 3: Documentation (Week 4)
9. ✅ Implement Skill Documenter
10. ✅ Implement Dev Onboarding Documenter
11. ✅ Add progress reporting

### Phase 4: Polish (Week 5)
12. ✅ Add cost estimation
13. ✅ User interface (slash command or skill)
14. ✅ Testing and refinement

---

## Additional Suggestions

### 1. Research Quality Score
Add a "Research Quality Score" metric that combines:
- Confidence (0.0-1.0)
- Completeness (none/partial/comprehensive)
- Coverage (number of dimensions covered)

**Formula:** `quality_score = (confidence * 0.5) + (completeness_score * 0.3) + (coverage_score * 0.2)`

### 2. Research Validation Step
Add a "Research Validation" step where orchestrator reviews findings before caching:
- Check for contradictions between researchers
- Identify gaps that need filling
- Validate confidence scores are reasonable

### 3. Research Comparison Mode
Enable "Research Comparison" mode to compare findings across multiple research runs:
- Track changes over time
- Identify when re-research is needed
- Compare different research strategies

### 4. Research Dimensions Coverage Matrix
Document which dimensions each researcher covers:

| Researcher | Architecture | API Surface | Patterns | Best Practices | Testing | Ecosystem |
|------------|--------------|-------------|----------|----------------|---------|-----------|
| DeepWiki   | ✅           | ✅          | ⚠️        | ✅              | ⚠️       | ✅         |
| GitHub     | ✅           | ✅          | ✅        | ⚠️              | ✅       | ⚠️         |
| Firecrawl  | ⚠️           | ⚠️          | ✅        | ✅              | ⚠️       | ✅         |
| Web Search | ⚠️           | ⚠️          | ✅        | ✅              | ⚠️       | ✅         |

**Legend:** ✅ = Strong coverage, ⚠️ = Partial coverage

---

## Questions for Design Team

1. **Architecture Layer:** Is orchestrator a primary agent or sub-agent? (Critical)
2. **User Interface:** Slash command (`/research`) or Skill (auto-invoke)? (High priority)
3. **Output Location:** Default location or always user-specified? (High priority)
4. **Naming Convention:** `using-<tool>` or `<tool>-guide`? (Medium priority)
5. **Cost Thresholds:** What token/cost threshold triggers approval? (Medium priority)
6. **Error Recovery:** How aggressive should retry logic be? (Medium priority)
7. **Cache Invalidation:** Manual only, or automatic staleness detection? (Low priority)

---

## Conclusion

The design is **fundamentally sound** with excellent architectural thinking. The main gaps are in **implementation specifics** and **architectural constraints**. Addressing these before coding will prevent significant rework.

**Key Takeaways:**
1. Clarify architecture layer (orchestrator vs sub-agents) - **Critical**
2. Create researcher prompt templates - **High Priority**
3. Define decision framework for orchestrator - **High Priority**
4. Resolve output location convention - **High Priority**
5. Add minimal error handling - **Medium Priority**

**Next Steps:**
1. Review this feedback with design team
2. Resolve open questions
3. Update design document with clarifications
4. Create detailed implementation plan
5. Begin Phase 1 implementation

---

**This feedback represents a comprehensive review of the Research Pipeline design. All recommendations are actionable and should be addressed before implementation begins.**
