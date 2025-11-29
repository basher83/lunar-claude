# Skill Generation: Approaches Comparison

Analysis of three approaches to generating Claude Code skills from documentation.

## Projects Analyzed

| Project | Purpose | Source |
|---------|---------|--------|
| **skill-factory** | 8-phase orchestrated skill creation | `plugins/meta/meta-claude/skills/skill-factory/` |
| **Skill Seekers** | Automated docs-to-skill converter | `github.com/yusufkaraaslan/Skill_Seekers` |
| **sync_docs.py** | Hybrid documentation sync | `plugins/meta/claude-dev-sandbox/scripts/sync_docs.py` |

## Feature Matrix

| Feature | skill-factory | Skill Seekers | sync_docs.py |
|---------|:-------------:|:-------------:|:------------:|
| Orchestration workflow | 8 phases | 6 stages | Single-purpose |
| Firecrawl integration | Yes | No | No |
| BFS site crawling | No | Yes | Yes |
| llms.txt parsing | No | No | Yes |
| GitHub AST analysis | No | Yes | No |
| PDF extraction | No | Yes | No |
| Conflict detection | No | Yes | No |
| AI enhancement | No | Yes | No |
| Smart categorization | Manual | Weighted scoring | URL patterns |
| ETag/MD5 caching | No | MD5 only | ETag + MD5 |
| Tiered storage | No | Categories | core/extended/full |
| Validation phases | 4 types | None | None |
| TodoWrite progress | Yes | No | No |

## Strengths by Project

### skill-factory

- Comprehensive validation (runtime, integration, compliance, audit)
- TodoWrite progress tracking
- Firecrawl SDK for web research
- Error handling with 3-tier fix strategy

### Skill Seekers

- Multi-source: docs + GitHub + PDF
- AI enhancement (75 → 500+ lines)
- Conflict detection (docs vs code)
- Smart categorization (URL:3, title:2, content:1 scoring)
- Pattern extraction ("Example:", "Usage:" markers)

### sync_docs.py

- HTTP header caching (ETag + Last-Modified)
- Tiered storage for token efficiency
- Combined discovery (crawl + llms.txt)
- Incremental updates

## Integration Options

### Option 1: Replace jina_reader_docs.py

Use sync_docs.py for Claude Code documentation research:

```bash
# Current (jina)
scripts/jina_reader_docs.py --output-dir "docs/research/skills/<name>"

# Proposed (sync_docs.py)
plugins/meta/claude-dev-sandbox/scripts/sync_docs.py \
  --output-dir "docs/research/skills/<name>" \
  --extended
```

**Benefits:** Caching, tiered storage, broader coverage (100 vs ~20 pages)

### Option 2: Add GitHub Scraper

Port Skill Seekers' GitHub AST analysis:

```bash
/meta-claude:skill:research <name> --source github.com/org/repo
```

**Benefits:** Extract actual API signatures, validate docs against code

### Option 3: Add AI Enhancement Phase

Insert between `create` and `review-content`:

```text
create → [enhance] → review-content
           ↓
    Analyze references/*.md
    Extract best examples
    Generate comprehensive SKILL.md
```

**Benefits:** Transform 75-line templates to 500+ line guides

### Option 4: Add Smart Categorization

Port Skill Seekers' weighted scoring to format phase:

```python
def categorize(page):
    score = 0
    if keyword in url: score += 3
    if keyword in title: score += 2
    if keyword in content: score += 1
    return category if score >= 2 else "other"
```

**Benefits:** Automatic content organization without manual brainstorming

## Recommended Priority

1. **Option 1** (Low effort, high value) - Better Claude Code docs
2. **Option 3** (Medium effort, high value) - Quality improvement
3. **Option 4** (Low effort, medium value) - Automation
4. **Option 2** (High effort, high value) - Code validation

## References

- Skill Seekers: <https://github.com/yusufkaraaslan/Skill_Seekers>
- Anthropic Scraper: <https://github.com/seanGSISG/Anthropic-Documentation-Scraper>
- sync_docs.py: `plugins/meta/claude-dev-sandbox/scripts/sync_docs.py`
- skill-factory: `plugins/meta/meta-claude/skills/skill-factory/SKILL.md`
