---
description: Systematic Landscape Research Protocol
argument-hint: [problem-domain] [key-requirements-or-design-doc]
---

# Purpose

Execute systematic research to discover existing solutions before finalizing a design.
This protocol ensures you've thoroughly explored the landscape and can justify any
decision to build rather than integrate.

Use this command BEFORE designing a solution to avoid reinventing the wheel.

## Variables

PROBLEM_DOMAIN: $1 (e.g., "markdown linting", "API gateway", "workflow orchestration")
KEY_REQUIREMENTS: $2 (file path to requirements doc OR comma-separated list)
OUTPUT_DIR: `docs/reviews/design-validation/landscape-research/`
FILE_NAME: `<problem-domain-slug>.md`

## Instructions

- IMPORTANT: If no `PROBLEM_DOMAIN` is provided, stop and ask the user to provide it.
- If `KEY_REQUIREMENTS` is a file path, read it first.
- Verify `OUTPUT_DIR` exists, create it if it doesn't.
- Save research output to `OUTPUT_DIR/FILE_NAME`.
- Be thorough - the goal is to AVOID building what already exists.
- Use web search tools to conduct actual research, not just hypotheticals.

## Workflow

### Phase 1: Open Source Discovery

**Search Targets:**

- GitHub, GitLab, Sourcehut repositories
- Package registries (npm, PyPI, Maven Central, crates.io, etc.)
- Awesome lists and curated collections
- Stack Overflow discussions and tool recommendations

**For each relevant project found, document:**

| Project | Stars/Adoption | Key Features | Gaps vs. Needs | License | Maturity |
|---------|----------------|--------------|----------------|---------|----------|
| [name] | [metrics] | [strengths] | [missing] | [license] | [active/stale] |

**Assess reusability:**

- Components/libraries we could use directly
- Patterns or architectures to learn from
- Integration points available

### Phase 2: Commercial/SaaS Solutions

**Search Targets:**

- Product Hunt, G2, Capterra
- Industry analyst reports (if available)
- Vendor comparisons and review sites
- LinkedIn for company/product discovery

**For each relevant solution, document:**

| Solution | Pricing | Feature Match | Integration | Viability |
|----------|---------|---------------|-------------|-----------|
| [name] | [cost] | [% needs met] | [API quality] | [stability] |

**Answer:**

- Could this be extended/configured to meet our needs?
- Total cost of ownership vs. building?
- Migration/integration difficulty?

### Phase 3: Academic & Standards Research

**Search Targets:**

- Google Scholar for relevant papers
- arXiv for recent research
- Industry standards bodies (IETF, W3C, OASIS, etc.)
- Technical specifications or RFCs

**Document findings on:**

- Proven algorithms, approaches, or patterns
- Standards for interoperability
- Research showing what doesn't work (anti-patterns)
- Performance benchmarks or comparison studies

### Phase 4: Community & Expert Intelligence

**Search Targets:**

- Reddit communities (r/programming, domain-specific subs)
- Hacker News discussions and Show HN posts
- Discord/Slack communities
- Conference talks or practitioner blog posts
- Technical podcasts

**Capture insights on:**

- What teams tried that failed and why
- Current best practices or emerging patterns
- Tools or approaches gaining traction
- Common pitfalls to avoid

### Phase 5: Synthesis & Gap Analysis

Synthesize all research into actionable conclusions:

1. **Mature Solutions** - Production-ready options with limitations
2. **Emerging/Experimental** - Promising but risky options
3. **Proven Patterns** - Approaches with evidence to adopt
4. **Validated Gaps** - Requirements not met by existing solutions
5. **Integration Strategy** - What to use vs. what to build

## Output Format

Save the research to `OUTPUT_DIR/FILE_NAME` using this structure:

```markdown
# Landscape Research: [Problem Domain]

**Researched**: [date]
**Domain**: [problem domain]
**Requirements**: [summary or link to requirements]

---

## Phase 1: Open Source Discovery

### Projects Evaluated

| Project | Stars/Adoption | Key Features | Gaps vs. Needs | License | Maturity |
|---------|----------------|--------------|----------------|---------|----------|
| [project 1] | [metrics] | [strengths] | [missing] | [license] | [status] |
| [project 2] | [metrics] | [strengths] | [missing] | [license] | [status] |
| [project 3] | [metrics] | [strengths] | [missing] | [license] | [status] |

### Reusability Assessment

- **Direct use**: [components/libraries]
- **Learn from**: [patterns/architectures]
- **Integration points**: [APIs/hooks]

---

## Phase 2: Commercial/SaaS Solutions

### Solutions Evaluated

| Solution | Pricing | Feature Match | Integration | Viability |
|----------|---------|---------------|-------------|-----------|
| [solution 1] | [cost] | [%] | [quality] | [status] |
| [solution 2] | [cost] | [%] | [quality] | [status] |
| [solution 3] | [cost] | [%] | [quality] | [status] |

### Build vs. Buy Analysis

- **Extensible?** [yes/no + details]
- **TCO comparison**: [build cost vs. buy cost]
- **Migration difficulty**: [low/medium/high + reasoning]

---

## Phase 3: Academic & Standards

### Relevant Research

- [paper/standard 1]: [key finding]
- [paper/standard 2]: [key finding]

### Standards to Follow

- [standard 1]: [why relevant]
- [standard 2]: [why relevant]

### Anti-Patterns Identified

- [approach that doesn't work]: [evidence]

---

## Phase 4: Community Intelligence

### Failure Stories

- [project/team]: [what they tried, why it failed]

### Best Practices

- [practice 1]: [source]
- [practice 2]: [source]

### Emerging Trends

- [trend 1]: [evidence of traction]

### Pitfalls to Avoid

- [pitfall 1]: [why]
- [pitfall 2]: [why]

---

## Phase 5: Synthesis

### Mature Solutions (Production-Ready)

1. **[Solution]**: [what it solves] | Limitations: [gaps]
2. **[Solution]**: [what it solves] | Limitations: [gaps]
3. **[Solution]**: [what it solves] | Limitations: [gaps]

### Emerging/Experimental

- **[Project]**: Potential: [upside] | Risks: [concerns]

### Proven Patterns to Adopt

1. [pattern with evidence]
2. [architecture with track record]
3. [standard/protocol to follow]

### Validated Gaps (Justifying Custom Work)

| Gap | Evidence | Why Existing Won't Work |
|-----|----------|-------------------------|
| [requirement] | [tested X, Y, Z] | [specific reason] |

### Integration Strategy

| Component | Decision | Source |
|-----------|----------|--------|
| [component 1] | Use existing | [which solution] |
| [component 2] | Build custom | [why] |
| [component 3] | Extend | [base + modifications] |

---

## Research Checklist

- [ ] Searched 3+ platforms for open-source solutions
- [ ] Evaluated 3+ commercial/SaaS alternatives
- [ ] Reviewed relevant academic research or standards
- [ ] Consulted community discussions/expert opinions
- [ ] Documented evidence for "why existing solutions don't work"
- [ ] Identified reusable components or patterns
- [ ] Confirmed we're not recreating something that exists
- [ ] Understood why similar projects succeeded or failed

---

## Recommendation

**Proceed to Design**: YES / NO / NEED MORE RESEARCH

**Key Findings**:

- [finding 1]
- [finding 2]
- [finding 3]

**If Need More Research**:

- [ ] [specific research gap]
- [ ] [specific research gap]
```
