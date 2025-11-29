# Documentation Sync vs Skill Generation

Clarification of two distinct concerns that share overlapping techniques.

## The Two Concerns

| Aspect | Documentation Sync | Skill Generation |
|--------|-------------------|------------------|
| **Purpose** | Keep local reference docs current | Create new skills from knowledge |
| **Output** | `references/*.md` for Claude to read | `SKILL.md` + structured skill directory |
| **User** | Anyone using Claude Code | Skill developers |
| **Lifecycle** | Periodic maintenance | One-time per skill |
| **Tools** | sync_docs.py, jina_reader_docs.py | skill-factory, skill-creator |

## Why They're Different

**Documentation Sync:**

- Passive reference material
- No YAML frontmatter needed
- Organized for efficient token loading (tiered)
- Updated regularly as upstream docs change
- Read-only consumption by Claude

**Skill Generation:**

- Active Claude behavior modification
- Requires YAML frontmatter (name, description, triggers)
- Organized per Anthropic skill specifications
- Created once, iterated as needed
- Teaches Claude new capabilities

## How They Relate

```text
┌─────────────────────┐
│  Documentation Sync │
│    (sync_docs.py)   │
└──────────┬──────────┘
           │
           │ CAN FEED INTO
           ▼
┌─────────────────────┐
│  Skill Generation   │
│   (skill-factory)   │
│                     │
│  Research phase can │
│  use synced docs as │
│  input material     │
└─────────────────────┘
```

## Tool Mapping

| Tool | Location | Concern |
|------|----------|---------|
| `sync_docs.py` | `claude-dev-sandbox/scripts/` | Documentation Sync |
| `jina_reader_docs.py` | `scripts/` | Documentation Sync |
| `skill-factory` | `meta-claude/skills/` | Skill Generation |
| `skill-creator` | `meta-claude/skills/` | Skill Generation |
| `firecrawl_*.py` | `scripts/` | Both (general research) |

## Recommendation

**Keep separate, make composable.**

- Maintain as independent tools with single responsibility
- Allow skill-factory to optionally use sync_docs.py output as research input
- Don't merge into monolithic tool

## Integration Point

When skill-factory needs Claude Code documentation for research:

```bash
# Option A: Use existing research command
/meta-claude:skill:research claude-hooks

# Option B: Pre-sync docs, then reference
sync_docs.py --output-dir docs/research/skills/claude-hooks/ --core-only
/meta-claude:skill:create claude-hooks docs/research/skills/claude-hooks/
```

## Summary

| Question | Answer |
|----------|--------|
| Same problem? | No |
| Related? | Yes - shared techniques |
| Combine tools? | No - keep separate |
| Allow composition? | Yes - output of one can feed other |
