---
type: design-considerations
plugin: plugin-dev
last_updated: 2025-12-18T01:15:00
---

# Plugin-Dev Design Considerations

Tracking decisions, future ideas, and observations that emerge during development.

## Open Considerations

### CON-001: Convert plugin-review command to skill

**Raised:** 2025-12-18
**Context:** During creation of /plugin-review command
**Status:** Under consideration

**Observation:**
The plugin-review command has grown to include:
- 6-phase workflow methodology
- Mandatory proof-based format
- 4 detailed examples
- State file template
- Component-specific checklists
- Integration with multiple skills

This exhibits skill characteristics:
- Reusable knowledge (review methodology)
- Could auto-trigger on "review my plugin", "validate this plugin"
- Progressive disclosure potential
- Domain expertise Claude doesn't inherently have

**Potential structure:**
```text
skills/plugin-review/
├── SKILL.md              # Core methodology, proof format, checklists
├── references/
│   ├── examples.md       # The 4 detailed examples
│   ├── state-template.md # State file template
│   └── phase-details.md  # Deep dive on each phase
└── scripts/
    └── discover-components.sh  # Component discovery helper
```

**Decision:** Wait to see how command performs in practice before refactoring.

**Next action:** Use /plugin-review on another plugin, evaluate if skill conversion warranted.

---

### CON-003: /consider command UX friction

**Raised:** 2025-12-18
**Context:** Testing /plugin-dev:consider command
**Status:** Under consideration

**Observation:**
Current UX has friction points:
1. Shows only counts, not actual entry titles - user can't see what CON-001 is without reading file
2. "Add entry" requires second prompt to select type (CON/DEC/IDEA) - two prompts for simple action
3. No quick path for mid-flow capture

**Desired UX:**
- Show actual entry titles with status, not just counts
- Single prompt with direct type selection
- Faster capture when in flow

**Next action:** Revise command to show entry summaries and streamline prompts.

---

### CON-004: Skills acknowledging CLAUDE.md overrides

**Raised:** 2025-12-18
**Context:** git-workflow skill and commit-craft agent review
**Status:** Under consideration

**Observation:**
When skills provide prescriptive defaults (commit formats, naming conventions, etc.), conflicts can arise with project-specific CLAUDE.md conventions.

**Pattern used in git-workflow:**
- Skill: "Project-specific CLAUDE.md conventions take precedence over these defaults."
- Agent step 0: "Check Project Conventions... Project conventions override skill defaults."

**Questions to resolve:**
- Should this be required for all skills with prescriptive content?
- Or only recommended as best practice?
- Does it add noise to skills that rarely conflict?

**Next action:** Evaluate during next plugin review - does absence of this note cause issues?

---

### CON-002: skill-development skill has loading bug

**Raised:** 2025-12-18
**Context:** During git-workflow plugin review
**Status:** Bug tracked

**Observation:**
The skill-development skill fails to load due to GitHub #12781 (dynamic bash pattern bug). The skill documents how to avoid the bug but is itself broken by it.

**Tracked in:** `.claude/plugin-dev-bugs.local.md` as BUG-001

**Next action:** Fix the skill by replacing `!` backtick examples with `$` notation.

---

## Decisions Made

### DEC-001: Proof-based format is mandatory

**Date:** 2025-12-18
**Context:** plugin-review command design

**Decision:** All change proposals in plugin reviews MUST follow structured proof format with exact skill quotes.

**Rationale:** "Proof-based" was initially aspirational. Adding mandatory format with examples enforces the behavior structurally.

**Implementation:** Added MANDATORY section with 4 concrete examples derived from git-workflow review.

---

### DEC-002: State files for workflow tracking

**Date:** 2025-12-18
**Context:** git-workflow plugin review

**Decision:** Complex workflows should create `.claude/<workflow>.local.md` state files.

**Rationale:**
- Enables resumable workflows across sessions
- Documents decisions with rationale
- Tracks commit SHAs
- Provides audit trail

**Pattern established:** git-workflow-plugin-review.local.md, git-workflow-command-testing.local.md

---

### DEC-003: plugin-dev README as canonical template

**Date:** 2025-12-18
**Context:** git-workflow README rewrite

**Decision:** plugin-dev/README.md is the standard template for plugin READMEs.

**Rationale:**
- Comprehensive structure (Overview, Commands, Agents, Skills, Use Cases, etc.)
- Proven pattern during git-workflow review
- /plugin-review Phase 4 should validate against this template

**Implementation:** Used to rewrite git-workflow README (0b82997)

---

## Future Ideas

### IDEA-001: /plugin-audit command

Quick validation without full review - just checks structure, naming, manifest. Fast sanity check.

### IDEA-002: Plugin review summary generator

After review complete, generate a summary suitable for PR description or changelog.

### IDEA-003: Cross-plugin pattern detection

Identify patterns used across multiple plugins that could be extracted into shared utilities.

### IDEA-004: State file taxonomy

Standardize templates for different .local.md types:
- `*-review.local.md` - Plugin/code review workflow tracking
- `*-testing.local.md` - Test session tracking
- `*-bugs.local.md` - Bug tracking with severity and status
- `*-considerations.local.md` - Design decisions (CON/DEC/IDEA pattern)

Could create scaffolding commands or templates for each type.

---

## Template

### For new considerations:

```markdown
### CON-XXX: [Title]

**Raised:** YYYY-MM-DD
**Context:** [Where this came up]
**Status:** [Under consideration | Decided | Deferred | Rejected]

**Observation:**
[What was noticed]

**Options:**
1. [Option A]
2. [Option B]

**Decision:** [If decided]

**Next action:** [What to do next]
```

### For decisions:

```markdown
### DEC-XXX: [Title]

**Date:** YYYY-MM-DD
**Context:** [What prompted this]

**Decision:** [What was decided]

**Rationale:** [Why]

**Implementation:** [How it was implemented]
```
