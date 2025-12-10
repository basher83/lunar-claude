# Detailed Implementation Plan: Research Pipeline v2

## Executive Summary

This plan adapts proven patterns from **M2 Deep Research** (supervisor-worker architecture, JSON schemas) and **Anthropic's research-agent demo** (subagent tracking, hook-based monitoring) to build a Claude Code-native research system with persistent knowledge base and codebase contextualization.

***

## Phase 1: Foundation \& Infrastructure (Week 1)

### Task 1.1: Create Research Report JSON Schema

**Duration**: 2 hours
**Reference**: M2 Deep Research report format[^1]

**Action Items**:

1. Create `.claude/schemas/research-report.json`
2. Define JSON Schema with validation rules:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Research Report Schema",
  "type": "object",
  "required": ["researcher", "query", "timestamp", "confidence", "completeness", "sources", "findings", "gaps", "summary", "tags"],
  "properties": {
    "researcher": {
      "type": "string",
      "enum": ["github", "tavily", "deepwiki", "exa"]
    },
    "query": {
      "type": "string",
      "description": "Original research query"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Agent's confidence in findings (0-1)"
    },
    "completeness": {
      "type": "string",
      "enum": ["none", "partial", "comprehensive"]
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["url", "title", "type", "relevance"],
        "properties": {
          "url": {"type": "string", "format": "uri"},
          "title": {"type": "string"},
          "type": {"type": "string"},
          "relevance": {"type": "string", "enum": ["high", "medium", "low"]},
          "metadata": {"type": "object"}
        }
      }
    },
    "findings": {
      "type": "object",
      "required": ["implementations", "patterns", "gotchas", "alternatives"],
      "properties": {
        "implementations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "url", "approach", "maturity", "evidence"],
            "properties": {
              "name": {"type": "string"},
              "url": {"type": "string", "format": "uri"},
              "approach": {"type": "string"},
              "maturity": {"type": "string", "enum": ["experimental", "beta", "production", "mature", "archived"]},
              "evidence": {"type": "string"}
            }
          }
        },
        "patterns": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Reusable patterns extracted from sources"
        },
        "gotchas": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Pain points and warnings"
        },
        "alternatives": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Other approaches considered"
        }
      }
    },
    "gaps": {
      "type": "array",
      "items": {"type": "string"},
      "description": "What couldn't be found"
    },
    "summary": {
      "type": "string",
      "description": "Agent's synthesis of findings"
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Semantic indexing for knowledge base"
    }
  }
}
```

**Validation**:

- Test schema with sample reports from each researcher type
- Ensure all required fields are present and properly typed


### Task 1.2: Initialize Knowledge Base Structure

**Duration**: 1 hour
**Reference**: Your design doc + M2 Deep Research caching pattern

**Action Items**:

1. Create `.claude/research-cache/` directory
2. Create initial `index.json`:

```json
{
  "version": "1.0",
  "schema_version": "research-report-v1",
  "created": "2025-12-01T16:00:00Z",
  "entries": []
}
```

3. Create `.claude/research-cache/.gitignore`:

```text
# Ignore all cache contents except index
*
!.gitignore
!index.json
```

4. Document cache management utilities needed:
    - `add_to_index(query, tags, path)` - Add new research entry
    - `search_cache(query, tags)` - Find similar cached research
    - `cleanup_stale(days=30)` - Remove old entries

### Task 1.3: Create First Researcher Agent (GitHub Template)

**Duration**: 4 hours
**Reference**: Anthropic research-agent demo patterns[^2]

**Action Items**:

1. Create `.claude/agents/research/github-agent.md`:

```markdown
---
name: GitHub Researcher
version: 1.0
tools:
  - github-mcp-direct (all tools)
  - read
  - write
  - edit
---

# GitHub Researcher Agent

You are a specialized research agent focused on finding battle-tested implementations, code patterns, and real-world usage examples from GitHub repositories.

## Your Mission

Given a research query, you will:

1. **Search GitHub repositories** using multiple strategies:
   - Repository search with relevant keywords
   - Code search for specific implementations
   - Issue/discussion search for gotchas and solutions
   
2. **Analyze findings** for:
   - Project maturity (stars, forks, last update, maintenance status)
   - Implementation quality (code structure, documentation, tests)
   - Real-world usage (companies using it, production evidence)
   - Common patterns across multiple repos
   
3. **Extract actionable insights**:
   - Proven implementation approaches
   - Reusable code patterns
   - Common gotchas and warnings
   - Alternative approaches and why chosen

## Search Strategy

**Step 1: Repository Discovery**
- Use `search_repositories` with query optimization:
  - Include technology keywords + "stars:>50" for quality filter
  - Try variations: exact matches, related terms, alternate names
  - Sort by stars for most popular, by updated for most active

**Step 2: Deep Analysis**
- For top 3-5 repositories:
  - Read README.md for approach overview
  - Check issues for gotchas (search for "problem", "bug", "warning")
  - Review recent commits for active maintenance
  - Look for production usage evidence (USERS.md, case studies)

**Step 3: Code Pattern Extraction**
- Use `search_code` to find:
  - Configuration patterns (search for config files)
  - Implementation patterns (search for key function names)
  - Common structures across multiple repos

## Output Format

You MUST write your findings to a JSON file named `github-report.json` in the cache directory provided by the orchestrator.

Use this exact structure (validated against `.claude/schemas/research-report.json`):

```json

{
"researcher": "github",
"query": "<original query>",
"timestamp": "<ISO8601>",
"confidence": 0.0-1.0,
"completeness": "none|partial|comprehensive",
"sources": [
{
"url": "https://github.com/owner/repo",
"title": "Repo Name",
"type": "repository",
"relevance": "high|medium|low",
"metadata": {
"stars": 1234,
"forks": 56,
"last_updated": "2024-11-15",
"language": "Python",
"license": "MIT"
}
}
],
"findings": {
"implementations": [
{
"name": "Project Name",
"url": "https://github.com/...",
"approach": "Brief description of their approach",
"maturity": "production",
"evidence": "234 stars, active maintenance, used by X companies"
}
],
"patterns": [
"Pattern 1: Description",
"Pattern 2: Description"
],
"gotchas": [
"Gotcha 1: Description with evidence from issues",
"Gotcha 2: Description"
],
"alternatives": [
"Alternative 1: Why not recommended",
"Alternative 2: Use case where it's better"
]
},
"gaps": [
"Couldn't find HA cluster examples",
"No CEPH integration patterns found"
],
"summary": "1-2 sentence synthesis of what you found",
"tags": ["tag1", "tag2", "tag3"]
}

```

## Success Criteria

- Found at least 3 relevant repositories OR documented why none exist
- Confidence score reflects evidence quality (high stars + activity = high confidence)
- Completeness reflects coverage (found all aspects of query = comprehensive)
- All URLs are valid GitHub links
- Patterns are specific and actionable, not vague
- Gotchas are backed by evidence (issue numbers, commit references)
- Tags enable semantic discovery (include technology, domain, use case)

## Example Queries

**Query**: "MicroK8s deployment to Proxmox via Ansible"

**Your Process**:
1. Search repos: "microk8s proxmox ansible stars:>10"
2. Analyze top 3 repos: README, issues, recent commits
3. Code search: "ansible microk8s role" to find patterns
4. Synthesize: best implementation, common patterns, gotchas
5. Write github-report.json to cache directory
```

2. **Test the agent**:
    - Create test invocation script
    - Mock cache directory
    - Verify JSON output validates against schema

***

### Task 1.4: Create Slash Command Skeleton

**Duration**: 3 hours
**Reference**: Your design doc orchestrator specification

**Action Items**:

1. Create `.claude/commands/lunar-research.md`:
```markdown
---
description: Research implementations, patterns, and best practices across multiple sources
arguments:
  - name: query
    description: What to research (e.g., "MicroK8s deployment to Proxmox via Ansible")
    required: true
---

# Lunar Research Command

You are the **orchestrator** for a multi-agent research system. Your role is to coordinate specialized researcher agents, manage the knowledge base, and synthesize findings with codebase context.

## Orchestration Workflow

### Phase 1: Preparation & Cache Check

1. **Parse the research query** from user input
2. **Generate cache key**: Normalize query to lowercase, remove special chars, create slug
3. **Check knowledge base**: 
   - Read `.claude/research-cache/index.json`
   - Search for matching queries by tags or similar text
   - If found and < 30 days old: offer to reuse or refresh
   - If not found: proceed with new research

4. **Create cache directory**: `.claude/research-cache/<cache-key>/`

### Phase 2: Parallel Research Dispatch

**CRITICAL**: You MUST dispatch all 4 researcher agents in parallel using the Task tool. Do NOT wait for one to complete before starting the next.

```

Dispatch all agents simultaneously:

Task 1 - GitHub Researcher:

- Agent: .claude/agents/research/github-agent.md
- Input: { "query": "<user query>", "cache_dir": ".claude/research-cache/<cache-key>/" }
- Output file: github-report.json

Task 2 - Tavily Researcher:

- Agent: .claude/agents/research/tavily-agent.md
- Input: { "query": "<user query>", "cache_dir": ".claude/research-cache/<cache-key>/" }
- Output file: tavily-report.json

Task 3 - DeepWiki Researcher:

- Agent: .claude/agents/research/deepwiki-agent.md
- Input: { "query": "<user query>", "cache_dir": ".claude/research-cache/<cache-key>/" }
- Output file: deepwiki-report.json

Task 4 - Exa Researcher:

- Agent: .claude/agents/research/exa-agent.md
- Input: { "query": "<user query>", "cache_dir": ".claude/research-cache/<cache-key>/" }
- Output file: exa-report.json

```

5. **Show progress indicator** to user:
```

🔍 Research in progress...
✓ GitHub Researcher: Searching repositories...
✓ Tavily Researcher: Scanning web sources...
✓ DeepWiki Researcher: Reading documentation...
✓ Exa Researcher: Neural search activated...

```

6. **Wait for all 4 agents to complete** and write their reports

### Phase 3: Synthesis

1. **Dispatch synthesizer agent**:
   - Agent: `.claude/agents/research/synthesizer-agent.md`
   - Input: { "cache_dir": ".claude/research-cache/<cache-key>/", "query": "<user query>" }
   - Task: Read all 4 reports, combine findings, write synthesis.md

2. **Wait for synthesis to complete**

### Phase 4: Contextualization & Response

1. **Read synthesis.md** from cache directory

2. **Analyze current codebase context**:
   - What patterns already exist in the codebase?
   - Which plugins/skills relate to this research?
   - Where would this fit in the existing structure?

3. **Generate narrative response** with these sections:

```


## Research Findings: <Topic>

### Summary

<1-2 sentences: what was found, confidence level>

### Recommended Approach

**<Solution Name>** from <source>

- Why it's best: <evidence-based reasoning>
- Maturity: <production-ready / experimental>
- Evidence: <stars, usage, maintenance>


### Integration with Your Codebase

Looking at your existing patterns:

```
- <Specific file/plugin> uses similar approach to <finding>
```

- Recommendation: <actionable integration suggestion>
- Example: <concrete next step>


### Key Patterns to Adopt

1. **<Pattern 1>**: <description> (seen in X/4 sources)
2. **<Pattern 2>**: <description> (seen in X/4 sources)
3. **<Pattern 3>**: <description>

### Gotchas to Avoid

```
- <Gotcha 1>: <description with evidence>
```

```
- <Gotcha 2>: <description>
```


### Alternatives Considered

```
- **<Alternative 1>**: <why not recommended OR use case>
```

```
- **<Alternative 2>**: <why not recommended OR use case>
```


### Next Steps

1. <Concrete action>
2. <Concrete action>
3. <Concrete action>
```

4. **Update knowledge base index**:
   - Add entry to `.claude/research-cache/index.json`
   - Include: query, cache_key, timestamp, tags, confidence, path

5. **Return formatted response** to user

## Error Handling

- **Agent failure**: If 1-2 agents fail, proceed with available reports but note in response
- **All agents fail**: Return error and suggest manual research
- **Schema validation failure**: Log error, attempt to parse what's available
- **Cache corruption**: Recreate index from existing directories

## Effort Scaling Rules

Based on query complexity, adjust approach:

- **Simple fact-finding** (e.g., "What is MicroK8s?"): Consider using 1-2 agents only (future optimization)
- **Direct comparison** (e.g., "K3s vs MicroK8s"): Use all 4 agents, focus on comparison in synthesis
- **Complex research** (current default): Always use all 4 agents in parallel

## Success Metrics

- Research completed in < 60 seconds (parallel execution)
- All 4 reports generated successfully
- Synthesis combines findings without duplication
- Integration suggestions reference actual codebase files
- User can act on recommendations immediately
```

2. **Create orchestrator test harness**:
    - Mock Task tool responses
    - Verify parallel dispatch logic
    - Test cache directory creation

***

## Phase 2: Complete Researcher Fleet (Week 2)

### Task 2.1: Create Tavily Researcher Agent

**Duration**: 3 hours
**Pattern**: Mirror github-agent.md structure

**Specialization Focus**:

- Recent blog posts, tutorials, guides
- Community discussions and recommendations
- Current best practices (2024-2025)
- Step-by-step walkthroughs

**Search Strategy**:

```markdown
1. Broad web search for recent content (past 6 months)
2. Tutorial/guide search with "how to" variations
3. Community platform search (Reddit, HN, forums)
4. Best practices search with year filter
```

**Output**: `tavily-report.json` matching schema

***

### Task 2.2: Create DeepWiki Researcher Agent

**Duration**: 3 hours

**Specialization Focus**:

- Official documentation deep-dive
- Architecture and design documents
- API references and specifications
- Configuration options and parameters

**Search Strategy**:

```markdown
1. Identify official documentation sources
2. Use deepwiki tools to read structure and navigate
3. Extract architecture diagrams and design decisions
4. Find configuration references and examples
```

**Output**: `deepwiki-report.json` matching schema

***

### Task 2.3: Create Exa Researcher Agent

**Duration**: 3 hours

**Specialization Focus**:

- Semantic/conceptual search beyond keywords
- Finding similar implementations
- Academic papers and technical deep-dives
- Discovering related technologies

**Search Strategy**:

```markdown
1. Semantic search with conceptual queries
2. Find similar content to top results
3. Search for academic papers on arXiv/Scholar
4. Discover related technologies and alternatives
```

**Output**: `exa-report.json` matching schema

***

### Task 2.4: Create Synthesizer Agent

**Duration**: 4 hours
**Reference**: M2 Deep Research synthesis approach[^1]

**Action Items**:

1. Create `.claude/agents/research/synthesizer-agent.md`:
```markdown
---
name: Research Synthesizer
version: 1.0
tools:
  - read
  - write
  - edit
---

# Research Synthesizer Agent

You combine findings from 4 specialized researcher agents into a unified synthesis document.

## Your Mission

Read all 4 research reports and create a comprehensive synthesis that:
1. Identifies common findings across sources (validates reliability)
2. Resolves conflicts using source priority (official docs > code > blogs)
3. Aggregates patterns, gotchas, and alternatives
4. Calculates overall confidence based on agreement
5. Produces structured synthesis.md

## Input

You will receive a cache directory path containing:
- `github-report.json` - GitHub code and repo analysis
- `tavily-report.json` - Web content and tutorials
- `deepwiki-report.json` - Official documentation
- `exa-report.json` - Semantic search and papers

## Process

### Step 1: Read All Reports
Load and parse all 4 JSON reports. Handle missing reports gracefully.

### Step 2: Cross-Validate Findings

**Identify consensus** (mentioned by 3+ sources):
- HIGH confidence patterns
- Broadly validated approaches
- Universal gotchas

**Identify partial agreement** (mentioned by 2 sources):
- MEDIUM confidence patterns
- Context-dependent approaches

**Identify unique insights** (mentioned by 1 source):
- Source-specific findings
- Lower confidence but potentially valuable

### Step 3: Resolve Conflicts

When sources disagree, use this priority:
1. **DeepWiki** (official docs) - authoritative for "how it should work"
2. **GitHub** (real code) - authoritative for "how it actually works"
3. **Tavily** (community) - authoritative for "current best practices"
4. **Exa** (academic) - authoritative for "theoretical background"

### Step 4: Aggregate by Category

**Implementations**: Deduplicate across sources, rank by maturity + evidence
**Patterns**: Group similar patterns, note prevalence (X/4 sources)
**Gotchas**: Combine and prioritize by severity + frequency
**Alternatives**: Consolidate options with pros/cons

### Step 5: Calculate Confidence

```

Overall Confidence = (
0.4 * (sources_agreement_ratio) +
0.3 * (avg_individual_confidence) +
0.2 * (implementation_maturity_score) +
0.1 * (source_completeness)
)

```

## Output Format

Write `synthesis.md` to the cache directory:

```


# Research Synthesis: <Query>

**Generated**: <timestamp>
**Sources**: 4 agents (GitHub, Tavily, DeepWiki, Exa)
**Confidence**: <0.0-1.0> (<High/Medium/Low>)
**Completeness**: <Comprehensive/Partial/Limited>

***

## Executive Summary

<2-3 sentences: what was found, key takeaway, confidence level>

## Recommended Approach

**<Solution Name>**

- **Source**: <Primary source with link>
- **Approach**: <How it works>
- **Maturity**: <Production/Beta/Experimental>
- **Evidence**: <Validation across sources>
- **Why Best**: <Reasoning based on findings>

**Validation**: Confirmed by <X/4> sources:

- GitHub: <Finding>
- Tavily: <Finding>
- DeepWiki: <Finding>
- Exa: <Finding>


## Key Patterns (Across All Sources)

### Pattern 1: <Name>

- **Description**: <What it is>
- **Prevalence**: Seen in <X/4> sources
- **Example**: <Concrete example from code/docs>
- **Why It Works**: <Rationale>


### Pattern 2: <Name>

- **Description**: <What it is>
- **Prevalence**: Seen in <X/4> sources
- **Example**: <Concrete example>


## Gotchas \& Warnings

### Critical (Must Address)

```
- **<Gotcha 1>**: <Description>
```

- **Sources**: <Which sources mentioned it>
- **Evidence**: <Issue links, error messages, documentation>
- **Solution**: <How to avoid/fix>


### Important (Should Address)

```
- **<Gotcha 2>**: <Description>
```

- **Sources**: <Which sources>
- **Solution**: <How to avoid/fix>


## Alternatives Considered

### Alternative 1: <Name>

- **What**: <Description>
- **Pros**: <Advantages>
- **Cons**: <Disadvantages>
- **Use Case**: <When to choose this instead>
- **Sources**: <Which sources discussed it>


### Alternative 2: <Name>

- Similar structure...


## Source-Specific Insights

### From GitHub Analysis

<Unique findings only found in code repositories>

### From Web Research (Tavily)

<Unique findings from blogs, tutorials, community>

### From Official Docs (DeepWiki)

<Unique findings from documentation>

### From Semantic Search (Exa)

<Unique findings from academic/technical sources>

## Gaps \& Limitations

**Could Not Find**:

```
- <Gap 1>: <What was searched for but not found>
```

```
- <Gap 2>: <Why this might be a limitation>
```

**Conflicting Information**:

```
- <Conflict 1>: <Where sources disagreed, how resolved>
```


## Confidence Assessment

**Overall Confidence**: <0.85> (High)

**Breakdown**:

- Source Agreement: <4/4 sources agree on core approach>
- Individual Confidence: <Avg 0.82 across agents>
- Implementation Maturity: <Production-ready examples found>
- Completeness: <Comprehensive coverage>

**Reliability Indicators**:

- ✓ Official documentation confirms approach
- ✓ Multiple production implementations found
- ✓ Active community discussion
- ✓ Recent updates (within 6 months)


## Citations

### GitHub Sources

1. [Repo Name](url) - <Brief description>
2. [Repo Name](url) - <Brief description>

### Web Sources

1. [Article Title](url) - <Brief description>
2. [Tutorial Title](url) - <Brief description>

### Documentation

1. [Official Docs](url) - <Section>
2. [API Reference](url) - <Section>

### Academic/Technical

1. [Paper Title](url) - <Brief description>
2. [Technical Blog](url) - <Brief description>

***

**Note to Orchestrator**: This synthesis is ready for contextualization with codebase patterns. Focus on integration suggestions in your final response.

```

2. **Test synthesis logic**:
   - Create 4 sample reports with overlapping findings
   - Verify conflict resolution prioritization
   - Confirm confidence calculation accuracy

---

## Phase 3: Knowledge Base & Caching (Week 2-3)

### Task 3.1: Implement Cache Utilities
**Duration**: 4 hours

**Action Items**:
1. Create `.claude/utils/cache_manager.py` (for reference, not executed):

```

"""
Cache management utilities for research pipeline.
These are reference implementations - actual logic runs in Claude.
"""

def add_to_index(query: str, cache_key: str, tags: list, confidence: float, path: str):
"""
Add research entry to knowledge base index.

    Args:
        query: Original research query
        cache_key: Normalized cache directory name
        tags: Semantic tags for discovery
        confidence: Overall confidence score (0-1)
        path: Relative path to cache directory
    """
    index_path = ".claude/research-cache/index.json"
    
    # Read current index
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    # Create new entry
    entry = {
        "id": cache_key,
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "tags": tags,
        "confidence": confidence,
        "path": path
    }
    
    # Add to entries
    index["entries"].append(entry)
    
    # Write back
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    def search_cache(query: str, tags: list, max_age_days: int = 30):
"""
Search for similar cached research.

    Returns matching entries sorted by relevance.
    """
    index_path = ".claude/research-cache/index.json"
    
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    matches = []
    for entry in index["entries"]:
        # Check age
        age_days = (datetime.now() - datetime.fromisoformat(entry["timestamp"])).days
        if age_days > max_age_days:
            continue
        
        # Check tag overlap
        tag_overlap = len(set(tags) & set(entry["tags"]))
        
        # Check query similarity (simple keyword matching)
        query_words = set(query.lower().split())
        entry_words = set(entry["query"].lower().split())
        query_overlap = len(query_words & entry_words)
        
        # Calculate relevance score
        relevance = (tag_overlap * 2) + query_overlap
        
        if relevance > 0:
            matches.append({
                "entry": entry,
                "relevance": relevance,
                "age_days": age_days
            })
    
    # Sort by relevance
    matches.sort(key=lambda x: x["relevance"], reverse=True)
    
    return matches[:5]  # Top 5 matches
    ```

2. **Create cache lookup prompt for orchestrator**:

```


## Cache Lookup Process

Before dispatching researchers, check for existing research:

1. **Extract tags from query**:
    - Technology keywords: microk8s, proxmox, ansible
    - Domain: infrastructure, deployment, kubernetes
    - Type: implementation, tutorial, comparison
2. **Search index**:

```python
matches = search_cache(query, tags, max_age_days=30)
```

3. **Evaluate matches**:
    - **High relevance** (score > 5): Offer to reuse
    - **Medium relevance** (score 2-5): Offer to refresh
    - **Low relevance** (score < 2): Proceed with new research
4. **User interaction**:

```
Found similar research from <X> days ago:
"<Cached query>" (confidence: 0.85)

Options:
1. Reuse cached findings
2. Refresh with new research
3. View cached findings first
```

```

---

### Task 3.2: Implement Progress Tracking
**Duration**: 3 hours  
**Reference**: Anthropic research-agent hooks pattern[^2]

**Action Items**:
1. Add progress indicators to orchestrator:

```


## Progress Reporting

During Phase 2 (parallel dispatch), show real-time updates:

**Initial**:

```
🔍 Lunar Research: <query>

Dispatching 4 specialized researchers...
⏳ GitHub Researcher: Starting...
⏳ Tavily Researcher: Starting...
⏳ DeepWiki Researcher: Starting...
⏳ Exa Researcher: Starting...
```

**As agents complete** (monitor task tool responses):

```
✓ GitHub Researcher: Found 5 repositories (confidence: 0.82)
⏳ Tavily Researcher: Scanning web sources...
⏳ DeepWiki Researcher: Reading documentation...
⏳ Exa Researcher: Neural search in progress...
```

**Synthesis phase**:

```
✓ All researchers complete
🔄 Synthesizing findings across 4 sources...
✓ Synthesis complete (confidence: 0.85)
📝 Preparing integration recommendations...
```

**Final**:

```
✅ Research complete! (45 seconds)
```

```

2. **Test progress reporting** with simulated delays

---

## Phase 4: Integration & Testing (Week 3-4)

### Task 4.1: End-to-End Integration Test
**Duration**: 6 hours

**Test Scenarios**:

1. **Simple Query Test**:
   - Query: "What is MicroK8s?"
   - Expected: All 4 agents return findings, synthesis generated, codebase suggestions
   - Validation: Response time < 60s, all reports valid JSON

2. **Complex Query Test**:
   - Query: "Battle-tested MicroK8s deployment to Proxmox via Ansible with HA"
   - Expected: Deep research across all sources, high-confidence synthesis
   - Validation: Multiple implementations found, patterns extracted, gotchas documented

3. **Cache Reuse Test**:
   - Query: Repeat previous query
   - Expected: Cache hit detected, offer to reuse
   - Validation: User can choose to reuse or refresh

4. **Partial Failure Test**:
   - Simulate 1 agent failing (e.g., Exa timeout)
   - Expected: Continue with 3 agents, note limitation in response
   - Validation: Synthesis still generated, confidence adjusted

**Test Checklist**:
- [ ] All 4 researcher agents execute in parallel
- [ ] Reports validate against JSON schema
- [ ] Synthesizer combines findings correctly
- [ ] Cache index updated properly
- [ ] Integration suggestions reference real codebase files
- [ ] Error handling works for agent failures
- [ ] Progress indicators update correctly

---

### Task 4.2: Codebase Contextualization Logic
**Duration**: 4 hours

**Action Items**:
1. Create contextual analysis prompt for orchestrator:

```


## Codebase Contextualization (Phase 4)

After reading synthesis.md, analyze how findings relate to existing codebase:

### Step 1: Identify Relevant Areas

Search codebase for:

- **Plugins/Skills** related to research topic
- **Existing implementations** of similar patterns
- **Configuration files** that might be affected
- **Documentation** that should reference findings

Example:

```
Query: "MicroK8s deployment to Proxmox via Ansible"

Relevant areas:
- plugins/infrastructure/proxmox-infrastructure/
- plugins/automation/ansible-workflows/
- docs/infrastructure/kubernetes-patterns.md
```


### Step 2: Pattern Matching

Compare research patterns with existing code:

**Research Pattern**: "Cloud-init for VM provisioning before Ansible"
**Existing Code**: `proxmox-infrastructure` already uses cloud-init templates
**Integration**: "Your proxmox-infrastructure plugin uses cloud-init (see templates/cloud-init.yaml). The research validates this approach and suggests adding..."

### Step 3: Generate Integration Suggestions

Format:

```markdown
### Integration with Your Codebase

**Finding**: <Pattern from research>
**Your Current Approach**: <Existing code/pattern>
**Recommendation**: <Specific action>
**Example**: <Concrete code or file change>

**New Capability to Add**:
1. Create new role in `plugins/infrastructure/microk8s-deployment/`
2. Adapt pattern from <repo URL> for role structure
3. Integrate with existing `proxmox-infrastructure` workflow
```


### Step 4: Prioritize Suggestions

- **High Priority**: Directly applicable, minimal changes needed
- **Medium Priority**: Requires adaptation, moderate effort
- **Low Priority**: Exploratory, future consideration

```

---

### Task 4.3: Documentation & Examples
**Duration**: 4 hours

**Action Items**:
1. Create `.claude/docs/research-pipeline-usage.md`:

```


# Research Pipeline Usage Guide

## Quick Start

```bash
/lunar-research "MicroK8s deployment to Proxmox via Ansible"
```


## What It Does

1. **Searches 4 sources in parallel**:
    - GitHub: Code repositories and implementations
    - Tavily: Blog posts, tutorials, community discussions
    - DeepWiki: Official documentation
    - Exa: Semantic search and academic sources
2. **Synthesizes findings**: Combines results, resolves conflicts, validates patterns
3. **Provides integration guidance**: Shows how findings relate to your codebase

## Example Queries

### Infrastructure Research

```
/lunar-research "Kubernetes cluster backup strategies"
/lunar-research "Terraform state management best practices"
/lunar-research "Prometheus monitoring for microservices"
```


### Development Patterns

```
/lunar-research "Python asyncio best practices 2024"
/lunar-research "React Server Components patterns"
/lunar-research "GraphQL schema design patterns"
```


### Comparisons

```
/lunar-research "K3s vs MicroK8s for edge computing"
/lunar-research "PostgreSQL vs MySQL for time-series data"
/lunar-research "gRPC vs REST API performance"
```


## Understanding Results

### Confidence Scores

- **0.8-1.0 (High)**: Multiple sources agree, production evidence exists
- **0.5-0.8 (Medium)**: Some agreement, beta/experimental implementations
- **0.0-0.5 (Low)**: Sparse information, conflicting sources


### Completeness Levels

- **Comprehensive**: Found implementations, patterns, gotchas, alternatives
- **Partial**: Found some aspects, missing others
- **Limited**: Minimal information available


## Cache Management

### View Cached Research

```
/lunar-research --list-cache
```


### Clear Stale Cache (>30 days)

```
/lunar-research --cleanup-cache
```


### Force Refresh (Bypass Cache)

```
/lunar-research "topic" --refresh
```


## Tips for Better Results

1. **Be specific**: "Docker multi-stage builds for Python" > "Docker optimization"
2. **Include context**: "MicroK8s for edge computing" > "MicroK8s setup"
3. **Specify timeframe**: "React best practices 2024" > "React best practices"
4. **Technology stack**: "PostgreSQL backups on Kubernetes" > "database backups"

## Troubleshooting

**"Confidence: Low" results**:

- Topic may be too new or niche
- Try broader query or alternative technologies

**Agent failures**:

- Check MCP server connectivity
- Review error messages in agent reports

**No codebase suggestions**:

- Research may not relate to current codebase
- Consider manual integration planning

```

2. **Create example outputs** for common scenarios

---

## Phase 5: Optimization & Polish (Week 4)

### Task 5.1: Performance Optimization
**Duration**: 4 hours

**Optimizations**:

1. **Intelligent Agent Selection** (post-MVP):
```


## Query Classification

Classify query to determine which agents to use:

**Fact-Finding** (e.g., "What is X?"):

- Use: DeepWiki (official docs) only
- Duration: ~15 seconds

**Implementation Search** (e.g., "How to implement X?"):

- Use: GitHub + Tavily
- Duration: ~30 seconds

**Comparison** (e.g., "X vs Y"):

- Use: All 4 agents
- Duration: ~45 seconds

**Deep Research** (e.g., "Battle-tested X for Y with Z"):

- Use: All 4 agents + extended search
- Duration: ~60 seconds

```

2. **Caching Strategies**:
- Cache MCP tool responses for 24 hours
- Reuse similar queries (>80% tag overlap)
- Progressive enhancement (add to existing cache)

3. **Timeout Handling**:
- Set agent timeout: 30 seconds
- Fallback to partial results if 1-2 agents timeout
- Retry failed agents once before giving up

---

### Task 5.2: Error Handling & Resilience
**Duration**: 3 hours

**Error Scenarios**:

1. **All Agents Fail**:
```

Response:
"Research agents encountered errors. Attempting manual search fallback..."
<Use orchestrator's own web search as fallback>
"Note: This is a simplified search. For comprehensive research, please retry later."

```

2. **Schema Validation Failure**:
```

- Log validation errors
- Attempt to extract valid fields
- Use partial report with warning
- Report schema issues for agent improvement

```

3. **Cache Corruption**:
```

- Detect corrupted index.json
- Rebuild from existing cache directories
- Log recovery process
- Continue with research

```

---

### Task 5.3: Quality Assurance
**Duration**: 6 hours

**QA Checklist**:

- [ ] **Functionality Tests**:
  - [ ] All 4 agents execute correctly
  - [ ] Synthesis combines findings without duplication
  - [ ] Cache lookup works accurately
  - [ ] Codebase contextualization references real files
  
- [ ] **Performance Tests**:
  - [ ] Parallel execution < 60 seconds
  - [ ] Cache hits < 5 seconds
  - [ ] Agent timeouts handled gracefully
  
- [ ] **Data Quality Tests**:
  - [ ] Reports validate against schema
  - [ ] URLs are valid and accessible
  - [ ] Confidence scores correlate with evidence
  - [ ] Tags enable semantic discovery
  
- [ ] **Edge Cases**:
  - [ ] Query with no results
  - [ ] Query with 1000+ GitHub repos
  - [ ] Query with conflicting information
  - [ ] Query in non-English language
  
- [ ] **User Experience**:
  - [ ] Progress indicators update correctly
  - [ ] Error messages are actionable
  - [ ] Integration suggestions are specific
  - [ ] Citations are properly formatted

---

## Implementation Timeline

| Week | Phase | Tasks | Deliverables |
|------|-------|-------|--------------|
| **Week 1** | Foundation | 1.1-1.4 | Schema, cache structure, GitHub agent, slash command skeleton |
| **Week 2** | Researcher Fleet | 2.1-2.4 | Tavily, DeepWiki, Exa agents, synthesizer agent |
| **Week 2-3** | Caching | 3.1-3.2 | Cache utilities, progress tracking |
| **Week 3-4** | Integration | 4.1-4.3 | E2E tests, contextualization, documentation |
| **Week 4** | Polish | 5.1-5.3 | Performance optimization, error handling, QA |

**Total Duration**: 4 weeks (approximately 80-100 hours)

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Research Speed** | < 60 seconds | Time from slash command to final response |
| **Parallel Efficiency** | 4x speedup vs sequential | Compare parallel vs sequential execution |
| **Cache Hit Rate** | > 30% | Percentage of queries using cached results |
| **Confidence Accuracy** | > 0.8 | Correlation between confidence scores and user satisfaction |
| **Integration Relevance** | > 70% | Percentage of suggestions that reference real codebase files |
| **Schema Compliance** | 100% | All reports validate against JSON schema |

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| **MCP Tool Failures** | Implement retries, fallback to alternative tools, graceful degradation |
| **Context Overflow** | Use synthesizer agent to compress findings, external memory pattern |
| **API Rate Limits** | Implement exponential backoff, respect rate limits, cache aggressively |
| **Low-Quality Results** | Confidence scoring, multi-source validation, user feedback loop |
| **Slow Performance** | Parallel execution, timeouts, intelligent agent selection |

---

## Future Enhancements (Post-MVP)

1. **Intelligent Agent Selection**: Classify queries to dispatch only relevant agents
2. **Multi-Turn Conversations**: Follow-up questions that reference previous research
3. **Export Formats**: Generate PDF reports, Markdown summaries, JSON exports
4. **Custom Research Templates**: User-defined agent combinations and priorities
5. **Web UI**: Browser-based interface for visual research exploration
6. **Vector Search**: Semantic indexing for knowledge base discovery
7. **Collaborative Research**: Share findings across team, merge knowledge bases

---

## References

1. [M2 Deep Research Agent](https://github.com/dair-ai/m2-deep-research) - Supervisor-worker architecture, JSON schemas
2. [Anthropic Research Agent Demo](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/research-agent) - Subagent tracking, hook patterns
3. Your Design Document: `2025-12-01-research-pipeline-v2-design.md`

---

**This implementation plan provides a concrete, step-by-step roadmap to build your Research Pipeline v2, incorporating proven patterns from M2 Deep Research and Anthropic's demos while maintaining your unique value propositions: Claude Code integration, persistent knowledge base, and codebase contextualization.**
