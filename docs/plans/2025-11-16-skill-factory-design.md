# Skill Factory - Create-Review-Validate Workflow Design

**Date:** 2025-11-16
**Status:** Design Complete, Ready for Implementation
**Goal:** Comprehensive workflow for creating, reviewing, and validating Claude Code skills with speed, quality, and accessibility
**Scope:** Creates ANY skill (conventional-git-commits, docker-master, brand-guidelines, etc.) - not limited to meta-claude plugin
**Orchestrator:** `skill-factory` skill
**Command Namespace:** `commands/skill/*` → `/skill-*` commands

## Overview

The create-review-validate cycle orchestrates skill creation from research through validation within the meta-claude plugin. This workflow ensures skills comply with official specifications and integrate cleanly with Claude Code.

## Architecture

### Relationship to Existing skill-creator

The meta-claude plugin already contains a `skill-creator` skill that guides the core creation workflow (Understand → Plan → Initialize → Edit → Package → Iterate). This proven workflow creates any skill for any purpose.

**skill-factory extends this foundation** by adding:
- **Pre-creation phases:** Research gathering and formatting
- **Post-creation phases:** Content review and validation
- **Quality gates:** Compliance checking, runtime testing, integration validation

**Delegation Architecture:**
skill-factory orchestrates the full lifecycle while delegating to existing proven tools:
- **skill-creator skill** → Core creation workflow
- **quick_validate.py** → Compliance validation (frontmatter, naming, structure)
- **claude-skill-auditor agent** → Comprehensive audit

This separation maintains the stability of skill-creator while adding research-backed, validated skill creation with quality gates.

### Core Pattern: Skill Orchestrating Slash Commands

The create-review-validate cycle follows the multi-agent-composition framework where skills are the top compositional layer that orchestrates primitives.

**Components:**
- **Orchestrator:** `skill-factory` skill (research + validation wrapper around skill-creator)
- **Primitives:** 8 independent slash commands under `commands/skill/` namespace
- **State Management:** TodoWrite (visual progress tracking, KISS approach)
- **Workflow Engine:** Conditional logic within the skill based on prompt context

### Naming Conventions

**Orchestrator Skill:**
- Name: `skill-factory`
- Rationale: Manufacturing metaphor (research → creation → quality assurance)
- Location: `plugins/meta/meta-claude/skills/skill-factory/`

**Command Namespace:**
- Directory structure: `commands/skill/` (grouped by component type)
- Command pattern: `/meta-claude:skill:*` (e.g., `/meta-claude:skill:research`, `/meta-claude:skill:create`)
- Future expansion: `commands/agent/`, `commands/command/`, `commands/hook/`

**Command Files:**
```sql
plugins/meta/meta-claude/commands/skill/
├── research.md          → /meta-claude:skill:research
├── format.md            → /meta-claude:skill:format
├── create.md            → /meta-claude:skill:create
├── review-content.md    → /meta-claude:skill:review-content
├── review-compliance.md → /meta-claude:skill:review-compliance
├── validate-runtime.md  → /meta-claude:skill:validate-runtime
├── validate-integration.md → /meta-claude:skill:validate-integration
└── validate-audit.md    → /meta-claude:skill:validate-audit
```

### Entry Point Detection

The skill analyzes the user's prompt to determine the workflow path:

**Explicit Research Path:**
```text
User: "Create coderabbit skill, research in plugins/meta/claude-dev-sandbox/skills/coderabbit/"
→ Skill detects research location, uses Path 1
```

**Ambiguous Path:**
```text
User: "Create coderabbit skill"
→ Skill asks: "Have you already gathered research?"
→ User response determines path
```

### Workflow Paths

**Path 1: Research Exists**
```text
/meta-claude:skill:format → /meta-claude:skill:create → /meta-claude:skill:review-content → /meta-claude:skill:review-compliance →
/meta-claude:skill:validate-runtime → /meta-claude:skill:validate-integration → /meta-claude:skill:validate-audit → Complete
```

**Path 2: Research Needed**
```text
/meta-claude:skill:research → /meta-claude:skill:format → /meta-claude:skill:create → /meta-claude:skill:review-content →
/meta-claude:skill:review-compliance → /meta-claude:skill:validate-runtime → /meta-claude:skill:validate-integration →
/meta-claude:skill:validate-audit → Complete
```

## Primitive Slash Commands

Each command stands alone as an independent, reusable, testable building block. Power users invoke them directly; beginners receive orchestrated guidance.

**Implementation Strategy:**
- **Delegation:** Commands that invoke existing proven tools (skill-creator skill, quick_validate.py, claude-skill-auditor agent)
- **New Build:** Commands that implement new functionality (research, formatting, content review, runtime validation, integration testing)

### 1. `/meta-claude:skill:research <skill-name> [sources]`

**Implementation:** New Build

**Purpose:** Fully automated research gathering

**Responsibilities:**
- Mini brainstorm with user to define scope (if sources not provided)
- Select appropriate research script based on context:
  - **General research:** `firecrawl_sdk_research.py` - Web search with category filtering (github, research, pdf), quality scoring (⭐), retry logic
  - **Specific URLs:** `firecrawl_scrape_url.py` - Single-URL scraper for known documentation
  - **Official docs:** `jina_reader_docs.py` - Claude Code documentation via Jina Reader API
- Execute chosen script with appropriate parameters
- Save research to default location: `docs/research/skills/<skill-name>/`
- Support custom path via `--output-dir` flag

**Research Script Selection Logic:**
```text
If user provides specific URLs → firecrawl_scrape_url.py
Else if researching Claude Code patterns → jina_reader_docs.py
Else (general topic research) → firecrawl_sdk_research.py
```

**Inputs:** Skill name, optional source URLs/keywords/categories
**Outputs:** Research markdown files in designated directory with source attribution
**Dependencies:** None (requires FIRECRAWL_API_KEY environment variable)
**Exit Codes:** Success (research saved) | Failure (API errors, missing credentials)

---

### 2. `/meta-claude:skill:format <research-dir>`

**Implementation:** New Build

**Purpose:** Light cleanup - remove UI artifacts, basic formatting (the car wash analogy: chunks of mud off before detail work)

**Responsibilities:**
- Run cleanup scripts (similar to cleanup_bash_research.py)
- Remove navigation elements, headers, footers, UI artifacts
- Basic markdown formatting (no restructuring yet)
- Output cleaned files to same directory or `<research-dir>/cleaned/`

**Inputs:** Research directory path
**Outputs:** Cleaned markdown files
**Dependencies:** Requires `/meta-claude:skill:research` output OR user-provided research
**Exit Codes:** Success (cleaned files ready) | Failure (malformed input)

---

### 3. `/meta-claude:skill:create <skill-name> <research-dir>`

**Implementation:** Delegation (invokes skill-creator skill)

**Purpose:** Create skill using proven skill-creator workflow

**Responsibilities:**
- Invoke skill-creator skill with research context
- Skill-creator guides through: Understand → Plan → Initialize → Edit → Package
- Use cleaned research as knowledge base for skill content
- Generate SKILL.md with proper structure via init_skill.py and package_skill.py
- Output skill directory at specified location

**Inputs:** Skill name, research directory
**Outputs:** Complete skill directory structure
**Dependencies:** Requires `/meta-claude:skill:format` output
**Exit Codes:** Success (skill created) | Failure (skill-creator errors)

---

### 4. `/meta-claude:skill:review-content <skill-path>`

**Implementation:** New Build

**Purpose:** Review content quality (clarity, completeness, usefulness)

**Responsibilities:**
- Analyze SKILL.md content for clarity
- Check examples are practical and accurate
- Verify instructions are actionable
- Assess usefulness for Claude's context
- Generate quality report with suggestions

**Inputs:** Path to skill directory
**Outputs:** Quality report (pass/fail + suggestions)
**Dependencies:** Requires `/meta-claude:skill:create` output
**Exit Codes:** Pass (quality acceptable) | Fail (issues found, report provided)

---

### 5. `/meta-claude:skill:review-compliance <skill-path>`

**Implementation:** Delegation (runs quick_validate.py)

**Purpose:** Technical compliance validation

**Responsibilities:**
- Run skill-creator/scripts/quick_validate.py on skill directory
- Validates frontmatter format (valid YAML, required fields: name, description)
- Checks naming convention (hyphen-case, max 64 chars, no leading/trailing/consecutive hyphens)
- Verifies description format (no angle brackets, max 1024 chars)
- Ensures no unexpected frontmatter properties
- Confirms SKILL.md file exists
- Generate compliance report from script output

**Inputs:** Path to skill directory
**Outputs:** Compliance report (pass/fail + specific violations)
**Dependencies:** Sequential - requires `/review-content` to pass first
**Exit Codes:** Pass (compliant) | Fail (violations found, report provided)

---

### 6. `/meta-claude:skill:validate-runtime <skill-path>`

**Implementation:** New Build

**Purpose:** Runtime testing - actually load the skill

**Responsibilities:**
- Attempt to load skill in Claude Code context
- Verify no syntax errors
- Test that skill description triggers properly
- Confirm progressive disclosure works
- Generate runtime test report

**Inputs:** Path to skill directory
**Outputs:** Runtime test report (pass/fail + error details)
**Dependencies:** Sequential - requires `/review-compliance` to pass
**Exit Codes:** Pass (loads successfully) | Fail (runtime errors, report provided)

---

### 7. `/meta-claude:skill:validate-integration <skill-path>`

**Implementation:** New Build

**Purpose:** Integration testing with Claude Code ecosystem

**Responsibilities:**
- Verify no conflicts with existing skills
- Test composition with slash commands
- Check compatibility with other meta-claude components
- Generate integration report

**Inputs:** Path to skill directory
**Outputs:** Integration report (pass/fail + conflict details)
**Dependencies:** Sequential - requires `/validate-runtime` to pass
**Exit Codes:** Pass (integrates cleanly) | Fail (conflicts found, report provided)

---

### 8. `/meta-claude:skill:validate-audit <skill-path>`

**Implementation:** Delegation (invokes claude-skill-auditor agent)

**Purpose:** Run comprehensive audit (non-blocking feedback)

**Responsibilities:**
- Invoke existing claude-skill-auditor agent from meta-claude
- Agent performs comprehensive skill analysis against official Anthropic specifications
- Collect audit feedback on structure, content quality, and best practices
- Generate detailed audit report with recommendations
- Never blocks workflow (purely informational, runs even if prior validation failed)

**Inputs:** Path to skill directory
**Outputs:** Audit report (recommendations + best practices)
**Dependencies:** Tiered - runs after runtime + integration (can run even if they fail)
**Exit Codes:** Always success (audit is non-blocking feedback)

## Dependency Model

### Review Phase (Sequential)

```text
/meta-claude:skill:review-content (no dependency)
  ↓ (must pass)
/meta-claude:skill:review-compliance (depends on content passing)
```

**Rationale:** Content quality must be acceptable before checking technical compliance. No point validating frontmatter if the content is fundamentally flawed.

### Validation Phase (Tiered)

```text
/meta-claude:skill:validate-runtime (depends on compliance passing)
  ↓ (must pass)
/meta-claude:skill:validate-integration (depends on runtime passing)
  ↓ (runs regardless)
/meta-claude:skill:validate-audit (non-blocking, informational)
```

**Rationale:**
- Runtime must work before testing integration
- Integration must work before comprehensive audit
- Audit provides feedback even if validation fails (helps debugging)

## State Management

### TodoWrite-Based Progress Tracking

The skill-creator-v2 skill uses TodoWrite to track workflow progress and provide real-time visibility.

**Example TodoWrite State (Path 2 - Research Needed):**

```javascript
[
  {"content": "Research skill domain", "status": "in_progress", "activeForm": "Researching skill domain"},
  {"content": "Format research materials", "status": "pending", "activeForm": "Formatting research materials"},
  {"content": "Create skill structure", "status": "pending", "activeForm": "Creating skill structure"},
  {"content": "Review content quality", "status": "pending", "activeForm": "Reviewing content quality"},
  {"content": "Review technical compliance", "status": "pending", "activeForm": "Reviewing technical compliance"},
  {"content": "Validate runtime loading", "status": "pending", "activeForm": "Validating runtime loading"},
  {"content": "Validate integration", "status": "pending", "activeForm": "Validating integration"},
  {"content": "Audit skill (non-blocking)", "status": "pending", "activeForm": "Auditing skill"},
  {"content": "Complete workflow", "status": "pending", "activeForm": "Completing workflow"}
]
```

### Workflow Execution Pattern

```text
For each todo in sequence:
  1. Mark todo as in_progress
  2. Invoke corresponding slash command via SlashCommand tool
  3. Check command result:
     - Success → Mark todo completed, continue to next
     - Failure → Apply fix strategy (see Error Handling section)
  4. Update TodoWrite before next phase
```

### Dependency Enforcement

Before invoking a command, the skill checks dependencies:

```text
Before running /review-compliance:
  Check: Is "Review content quality" completed?
    - Yes → Invoke /review-compliance
    - No → Skip, workflow failed earlier
```

### Progress Visibility

TodoWrite provides:
- Real-time phase tracking (what's running now)
- Completion history (what's done)
- Pending phases (what's coming)
- Clear linear progression
- User can see exactly where workflow is

## Error Handling & Fix Strategy

### Core Principle: Fail Fast

When a phase fails without auto-fix, the workflow stops immediately. The system provides no complex recovery mechanisms, no checkpointing, no resume commands—only a clean exit with clear error reporting.

### Rule-Based Fix Tiers

Issues are categorized into three tiers based on complexity:

#### Tier 1: Simple (Auto-Fix)

**Issue Types:**
- Formatting issues (whitespace, indentation)
- Missing frontmatter fields (can be inferred)
- Markdown syntax errors (quote escaping, link formatting)
- File structure issues (missing directories)

**Actions:**
1. Automatically apply fix
2. Auto re-run the failed command once
3. Continue if passes, fail fast if still broken

**Example:**
```text
/review-compliance fails: "Missing frontmatter description field"
  ↓
Tier: Simple → AUTO-FIX
  ↓
Fix: Add description field inferred from skill name
  ↓
Auto re-run: /review-compliance <skill-path>
  ↓
Result: Pass → Mark todo completed, continue to /validate-runtime
```

---

#### Tier 2: Medium (Guided Fix with Approval)

**Issue Types:**
- Content clarity suggestions
- Example improvements
- Instruction rewording
- Structure optimization

**Actions:**
1. Present issue and suggested fix
2. Ask user: "Apply this fix? [Yes/No/Edit]"
3. If Yes → Apply fix, re-run command once
4. If No → Fail fast
5. If Edit → Show fix, let user modify, apply, re-run

**Example:**
```text
/review-content fails: "Examples section unclear, lacks practical context"
  ↓
Tier: Medium → GUIDED FIX
  ↓
Suggested fix: [Shows proposed rewrite with clearer examples]
  ↓
Ask: "Apply this fix? [Yes/No/Edit]"
  ↓
User: Yes
  ↓
Apply fix
  ↓
Re-run: /review-content <skill-path>
  ↓
Result: Pass → Mark todo completed, continue to /review-compliance
```

---

#### Tier 3: Complex (Stop and Report)

**Issue Types:**
- Architectural problems (skill design flaws)
- Insufficient research (missing critical information)
- Unsupported use cases (skill doesn't fit Claude Code model)
- Schema violations (fundamental structure issues)
- Composition rule violations (e.g., attempting to nest sub-agents)

**Actions:**
1. Report the issue with detailed explanation
2. Provide recommendations for manual fixes
3. **Fail fast** - exit workflow immediately
4. User must fix manually and restart workflow

**Example:**
```text
/review-content fails: "Skill attempts to nest sub-agents within sub-agents, which violates Claude Code composition rules"
  ↓
Tier: Complex → STOP AND REPORT
  ↓
Report:
  ❌ Skill creation failed at: Review Content Quality

  Issue found:
  - [Tier 3: Complex] Skill attempts to nest sub-agents, which violates composition rules

  Recommendation:
  - Restructure skill to invoke sub-agents via SlashCommand tool instead
  - See: docs/multi-agent-composition/patterns/orchestrator-pattern.md

  Workflow stopped. Please fix manually and restart with:
    /meta-claude:skill:create coderabbit docs/research/skills/coderabbit/

  Artifacts preserved at:
    Research: docs/research/skills/coderabbit/
    Partial skill: plugins/meta/meta-claude/skills/coderabbit/

  ↓
WORKFLOW EXITS (fail fast)
```

---

### Fix Categorization Response Format

Each primitive command returns errors with tier metadata:

```javascript
{
  "status": "fail",
  "issues": [
    {
      "tier": "simple",
      "category": "frontmatter",
      "description": "Missing description field",
      "fix": "Add description: 'Guide for creating CodeRabbit skills'",
      "auto_fixable": true
    },
    {
      "tier": "medium",
      "category": "content-clarity",
      "description": "Examples section unclear, lacks practical context",
      "suggestion": "[Proposed rewrite with clearer examples]",
      "auto_fixable": false
    },
    {
      "tier": "complex",
      "category": "architectural",
      "description": "Skill violates composition rules by nesting sub-agents",
      "recommendation": "Restructure to use SlashCommand tool for sub-agent invocation",
      "auto_fixable": false
    }
  ]
}
```

### One-Shot Fix Policy

To prevent infinite loops:

```text
Phase fails
  ↓
Apply fix (auto or guided)
  ↓
Re-run command ONCE
  ↓
Result:
  - Pass → Continue
  - Fail → FAIL FAST (no second fix attempt)
```

**Rationale:** If the first fix fails, the issue exceeds initial assessment. The system stops and lets the user investigate rather than looping infinitely.

### Iteration Logic (Auto-Loop on Fixes)

When a primitive command supports auto-fix:

```text
Phase fails with fixable issues
  ↓
Apply fix strategy (auto/guided/manual based on tier)
  ↓
Fix applied successfully
  ↓
AUTO RE-RUN the same primitive command (once)
  ↓
Check result:
  - Pass → Mark todo completed, continue to next phase
  - Fail again → FAIL FAST (report issue, exit workflow)
```

## Success Completion

When all phases pass successfully:

```text
✅ Skill created and validated successfully!

Location: <skill-output-path>/

Research materials: docs/research/skills/<skill-name>/
Keep research materials? [Keep/Remove] (default: Keep)

Next steps - choose an option:
  [1] Test the skill now - Try invoking it in a new conversation
  [2] Create PR - Submit skill to repository
  [3] Add to plugin.json - Integrate with plugin manifest (if applicable)
  [4] Done - Exit workflow

What would you like to do?
```

**Artifact Cleanup:**
- User chooses Keep or Remove for research materials
- Default: Keep (preserves research for iterations)
- If Remove: Deletes docs/research/skills/<skill-name>/ directory

**User Actions:**
1. **Test the skill now** → Skill guides user to test invocation
2. **Create PR** → Skill creates git branch, commits, pushes, opens PR
3. **Add to plugin.json** → Skill updates manifest, validates structure (for plugin skills)
4. **Done** → Clean exit

Workflow executes the user's choice, then exits cleanly.

## Design Principles

### 1. Primitives First
Slash commands are the foundation. The skill orchestrates them using the SlashCommand tool. This follows the multi-agent-composition principle: "Always start with prompts."

### 2. KISS State Management
TodoWrite provides visibility without complexity. No external state files, no databases, no complex checkpointing. Simple, effective progress tracking.

### 3. Fail Fast
No complex recovery mechanisms. When something can't be auto-fixed or user declines a fix, exit immediately with clear guidance. Preserves artifacts, provides next steps.

### 4. Context-Aware Entry
Detects workflow path from user's prompt. Explicit research location → Path 1. Ambiguous → Ask user. Natural language interface.

### 5. Composable & Testable
Every primitive works standalone (power users) or orchestrated (guided users). Each command is independently testable and verifiable.

### 6. Expandable Foundation
Start with skills (most complex component type). Validate the workflow approach. Extend to agents, commands, hooks later using the same pattern.

### 7. Quality Gates
Sequential dependencies ensure quality: content before compliance, runtime before integration. Tiered validation with non-blocking audit for comprehensive feedback.

## Implementation Roadmap

### Phase 1: Primitives (Start Here)

**New Build (5 commands):**
- [ ] Implement `/meta-claude:skill:research` command (firecrawl automation)
- [ ] Implement `/meta-claude:skill:format` command (cleanup script)
- [ ] Implement `/meta-claude:skill:review-content` command (quality assessment)
- [ ] Implement `/meta-claude:skill:validate-runtime` command (load testing)
- [ ] Implement `/meta-claude:skill:validate-integration` command (conflict detection)

**Delegation (3 commands):**
- [ ] Implement `/meta-claude:skill:create` command (invokes skill-creator skill)
- [ ] Implement `/meta-claude:skill:review-compliance` command (runs quick_validate.py)
- [ ] Implement `/meta-claude:skill:validate-audit` command (invokes claude-skill-auditor agent)

### Phase 2: Orchestration
- [ ] Create `skill-factory` skill (separate from existing)
- [ ] Implement context-aware entry point detection
- [ ] Implement TodoWrite-based state management
- [ ] Implement workflow path selection (research exists vs. needed)
- [ ] Implement sequential command invocation via SlashCommand tool
- [ ] Implement dependency enforcement

### Phase 3: Error Handling
- [ ] Implement rule-based fix tier categorization
- [ ] Implement auto-fix for Tier 1 (simple) issues
- [ ] Implement guided fix for Tier 2 (medium) issues
- [ ] Implement fail-fast for Tier 3 (complex) issues
- [ ] Implement one-shot fix policy (re-run once, then fail)
- [ ] Implement iteration logic with re-validation

### Phase 4: Completion
- [ ] Implement success completion flow
- [ ] Implement next-action options (test, PR, add to manifest, done)
- [ ] Implement clean exit with artifact preservation
- [ ] Write tests for each primitive command
- [ ] Write integration tests for full workflow
- [ ] Documentation and examples

### Phase 5: Future Expansion
- [ ] Extend to agents (`/research-agent`, `/create-agent`, etc.)
- [ ] Extend to commands (`/research-command`, `/create-command`, etc.)
- [ ] Extend to hooks (`/research-hook`, `/create-hook`, etc.)
- [ ] Universal orchestrator skill that adapts to component type

## Benefits

### For All Users (Speed, Quality, Accessibility)
- **Speed:** Automated research, formatting, validation reduces manual steps
- **Quality:** Multiple review gates ensure compliance and usefulness
- **Accessibility:** Guided workflow for beginners, primitives for experts

### For Beginners
- Natural language entry ("Create X skill")
- Automatic workflow orchestration
- Clear error messages with fix suggestions
- TodoWrite visibility shows progress

### For Power Users
- Direct access to primitives (bypass orchestration)
- Composable commands for custom workflows
- Fail-fast approach respects their time
- Artifacts preserved for manual iteration

### For Meta-Claude Plugin
- Consistent skill quality
- Reduced review burden (automated compliance checks)
- Extensible pattern for other component types
- Clear separation of concerns (primitives vs orchestration)

## Trade-offs

### Benefits
- ✅ Comprehensive quality assurance
- ✅ Automated research and formatting
- ✅ Clear linear workflow with visibility
- ✅ Fail-fast prevents infinite loops
- ✅ Composable primitives enable flexibility
- ✅ Extensible to other component types

### Costs
- ❌ Upfront investment to build primitives
- ❌ More commands to maintain (8 primitives + orchestrator skill)
- ❌ Complexity of dependency management
- ❌ Need to resolve existing skill-creator conflict
- ❌ Learning curve for fix tier categorization

### Mitigations
- Start with primitives (testable, reusable building blocks)
- Use existing tools (TodoWrite, SlashCommand tool, existing auditor)
- KISS state management (no external files or databases)
- Clear documentation and examples
- Extensible design amortizes investment across component types

## Open Questions

### 1. Existing skill-creator relationship ✅ RESOLVED

**Decision:** Keep separate via delegation architecture
- **skill-creator:** Core creation workflow (proven, stable) - remains unchanged
- **skill-factory:** Research + validation orchestrator that wraps skill-creator
- **Relationship:** skill-factory invokes skill-creator skill for Step 3 (creation)
- **Benefit:** Maintains stability of proven workflow while adding quality gates

### 2. Research source defaults ✅ RESOLVED

**Decision:** Use existing research scripts with intelligent selection
- **firecrawl_sdk_research.py:** General research with web search, category filtering (github/research/pdf), quality scoring
- **firecrawl_scrape_url.py:** Specific known URLs
- **jina_reader_docs.py:** Official Claude Code documentation
- **Selection logic:** Based on user input (URLs provided vs. general topic vs. Claude Code patterns)
- **Benefit:** Reuses proven automation, handles defaults intelligently, supports custom sources

### 3. Validation strictness ✅ RESOLVED

**Decision:** Permissive validation (warnings don't fail the workflow)
- **Rationale:** This is a development/authoring tool, not a CI/CD pipeline
- **Behavior:** Validation reports issues but allows workflow to continue when possible
- **Philosophy:** Guide users toward quality without blocking their progress
- **Hard failures only for:** Critical compliance violations (invalid YAML, missing required fields)
- **Warnings for:** Style suggestions, best practice recommendations, quality improvements
- **Benefit:** Supports rapid iteration while still providing quality feedback

### 4. Artifact cleanup ✅ RESOLVED

**Decision:** Ask user at completion
- **When:** After successful skill creation and validation
- **Prompt:** "Research materials saved to docs/research/skills/<skill-name>/. Keep or remove? [Keep/Remove]"
- **Keep:** Preserves research for future iterations, builds knowledge base over time
- **Remove:** Cleans up workspace, research can be re-gathered if needed later
- **Default:** Keep (if user doesn't respond or skips)
- **Benefit:** User decides based on their workflow preferences and disk space concerns

## Success Metrics

How do we know this design succeeds?

1. **Time to create skill:** Reduce from hours to minutes for experienced users
2. **Skill quality:** 100% compliance with official specs on first validation
3. **User satisfaction:** Beginners can create high-quality skills without deep knowledge
4. **Maintainability:** Primitives are independently testable and reusable
5. **Extensibility:** Pattern extends to agents/commands/hooks with minimal changes

## Next Steps

1. Review and validate this design document
2. Apply writing clarity improvements (elements-of-style skill)
3. Commit design document to git
4. Set up implementation workspace (git worktree)
5. Create detailed implementation plan (superpowers:writing-plans)
6. Begin Phase 1: Primitive command implementation

---

**Document Status:** Design Complete, Ready for Implementation
**Next Action:** Validate design, prepare for implementation
