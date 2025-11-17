---
name: skill-factory
description: >
  Orchestrates the full skill creation lifecycle from research through validation. Use when creating ANY skill
  (conventional-git-commits, docker-master, brand-guidelines, etc.) with automated research, quality reviews, and
  comprehensive validation. Guides users through create-review-validate workflow with real-time progress tracking.
---

# Skill Factory

Comprehensive workflow orchestrator for creating high-quality Claude Code skills with automated research, content
review, and multi-tier validation.

## When to Use This Skill

Use skill-factory when:

- **Creating any new skill** - From initial idea to validated, production-ready skill
- **Research needed** - Automate gathering of documentation, examples, and best practices
- **Quality assurance required** - Ensure skills meet official specifications and best practices
- **Guided workflow preferred** - Step-by-step progression with clear checkpoints
- **Validation needed** - Runtime testing, integration checks, and comprehensive auditing

**Scope:** Creates skills for ANY purpose (not limited to meta-claude plugin):

- Infrastructure skills (terraform-best-practices, ansible-vault-security)
- Development skills (docker-compose-helper, git-workflow-automation)
- Domain-specific skills (brand-guidelines, conventional-git-commits)
- Any skill that extends Claude's capabilities

## Quick Start

### Path 1: Research Already Gathered

If you have research materials ready:

```bash
# Research exists at docs/research/skills/<skill-name>/
skill-factory <skill-name> docs/research/skills/<skill-name>/
```

The skill will:

1. Format research materials
2. Create skill structure
3. Review content quality
4. Review technical compliance
5. Validate runtime loading
6. Validate integration
7. Run comprehensive audit
8. Present completion options

### Path 2: Research Needed

If starting from scratch:

```bash
# Let skill-factory handle research
skill-factory <skill-name>
```

The skill will ask about research sources and proceed through full workflow.

### Example Usage

```text
User: "Create a skill for CodeRabbit code review best practices"

skill-factory detects no research path provided, asks:

"Have you already gathered research for this skill?
[Yes - I have research at <path>]
[No - Help me gather research]
[Skip - I'll create from knowledge only]"

User: "No - Help me gather research"

skill-factory proceeds through Path 2:
1. Research skill domain
2. Format research materials
3. Create skill structure
... (continues through all phases)
```

## Workflow Architecture

### Entry Point Detection

The skill analyzes your prompt to determine the workflow path:

**Explicit Research Path (Path 1):**

```text
User: "Create coderabbit skill, research in docs/research/skills/coderabbit/"
→ Detects research location, uses Path 1 (skip research phase)
```

**Ambiguous Path:**

```text
User: "Create coderabbit skill"
→ Asks: "Have you already gathered research?"
→ User response determines path
```

**Research Needed (Path 2):**

```text
User selects "No - Help me gather research"
→ Uses Path 2 (full workflow including research)
```

### Workflow Paths

#### Path 1: Research Exists

```text
format → create → review-content → review-compliance →
validate-runtime → validate-integration → validate-audit → complete
```

#### Path 2: Research Needed

```text
research → format → create → review-content → review-compliance →
validate-runtime → validate-integration → validate-audit → complete
```

### State Management

Progress tracking uses TodoWrite for real-time visibility:

**Path 2 Example (Full Workflow):**

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

**Path 1 Example (Research Exists):**

Omit first "Research skill domain" task from TodoWrite list.

## Workflow Execution

### Phase Invocation Pattern

For each phase in the workflow:

1. **Mark phase as in_progress** (update TodoWrite)
2. **Check dependencies** (verify prior phases completed)
3. **Invoke command** using SlashCommand tool:

   ```text
   /skill-research <skill-name> [sources]
   /skill-format <research-dir>
   /skill-create <skill-name> <research-dir>
   /skill-review-content <skill-path>
   /skill-review-compliance <skill-path>
   /skill-validate-runtime <skill-path>
   /skill-validate-integration <skill-path>
   /skill-validate-audit <skill-path>
   ```

4. **Check result** (success or failure with tier metadata)
5. **Apply fix strategy** (if needed - see Error Handling section)
6. **Mark phase completed** (update TodoWrite)
7. **Continue to next phase** (or exit if fail-fast triggered)

### Dependency Enforcement

Before running each command, verify dependencies:

**Review Phase (Sequential):**

```text
/skill-review-content (no dependency)
  ↓ (must pass)
/skill-review-compliance (depends on content passing)
```

**Validation Phase (Tiered):**

```text
/skill-validate-runtime (depends on compliance passing)
  ↓ (must pass)
/skill-validate-integration (depends on runtime passing)
  ↓ (runs regardless)
/skill-validate-audit (non-blocking, informational)
```

**Dependency Check Pattern:**

```text
Before running /skill-review-compliance:
  Check: Is "Review content quality" completed?
    - Yes → Invoke /skill-review-compliance
    - No → Skip (workflow failed earlier, stop here)
```

### Command Invocation with SlashCommand Tool

Use the SlashCommand tool to invoke each primitive command:

```javascript
// Example: Invoking research phase
SlashCommand({
  command: "/skill-research ansible-vault-security"
})

// Example: Invoking format phase
SlashCommand({
  command: "/skill-format docs/research/skills/ansible-vault-security"
})

// Example: Invoking create phase
SlashCommand({
  command: "/skill-create ansible-vault-security docs/research/skills/ansible-vault-security"
})
```

**IMPORTANT:** Wait for each command to complete before proceeding to the next phase. Check the response status
before continuing.

## Error Handling & Fix Strategy

### Core Principle: Fail Fast

When a phase fails without auto-fix capability, the workflow **stops immediately**. No complex recovery, no
checkpointing, no resume commands—only clean exit with clear error reporting and preserved artifacts.

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
2. Auto re-run the failed command ONCE
3. Continue if passes, fail fast if still broken

**Example:**

```text
/skill-review-compliance fails: "Missing frontmatter description field"
  ↓
Tier: Simple → AUTO-FIX
  ↓
Fix: Add description field inferred from skill name
  ↓
Auto re-run: /skill-review-compliance <skill-path>
  ↓
Result: Pass → Mark todo completed, continue to /skill-validate-runtime
```

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
/skill-review-content fails: "Examples section unclear, lacks practical context"
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
Re-run: /skill-review-content <skill-path>
  ↓
Result: Pass → Mark todo completed, continue to /skill-review-compliance
```

#### Tier 3: Complex (Stop and Report)

**Issue Types:**

- Architectural problems (skill design flaws)
- Insufficient research (missing critical information)
- Unsupported use cases (doesn't fit Claude Code model)
- Schema violations (fundamental structure issues)
- Composition rule violations (e.g., attempting to nest sub-agents)

**Actions:**

1. Report the issue with detailed explanation
2. Provide recommendations for manual fixes
3. **Fail fast** - exit workflow immediately
4. User must fix manually and restart workflow

**Example:**

```text
/skill-review-content fails: "Skill attempts to nest sub-agents, violates composition rules"
  ↓
Tier: Complex → STOP AND REPORT
  ↓
Report:
  ❌ Skill creation failed at: Review Content Quality

  Issue found:
  - [Tier 3: Complex] Skill attempts to nest sub-agents, which violates composition rules

  Recommendation:
  - Restructure skill to invoke sub-agents via SlashCommand tool instead
  - See: plugins/meta/meta-claude/skills/multi-agent-composition/

  Workflow stopped. Please fix manually and restart.

  Artifacts preserved at:
    Research: docs/research/skills/coderabbit/
    Partial skill: plugins/meta/meta-claude/skills/coderabbit/

  ↓
WORKFLOW EXITS (fail fast)
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
  - Pass → Continue to next phase
  - Fail → FAIL FAST (no second fix attempt)
```

**Rationale:** If the first fix fails, the issue exceeds initial assessment. Stop and let the user investigate rather
than looping infinitely.

### Issue Categorization Response Format

Each primitive command returns errors with tier metadata:

```javascript
{
  "status": "fail",
  "issues": [
    {
      "tier": "simple",
      "category": "frontmatter",
      "description": "Missing description field",
      "fix": "Add description: 'Guide for CodeRabbit code review'",
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

**Parsing Command Responses:**

When a command completes, analyze its output to determine status:

- Look for "Success", "PASS", or exit code 0 → Continue
- Look for "Error", "FAIL", or exit code 1 → Apply fix strategy
- Parse issue tier metadata (if provided) to select fix approach
- If no tier metadata, infer tier from issue description

## Success Completion

When all phases pass successfully:

```text
✅ Skill created and validated successfully!

Location: <skill-output-path>/

Research materials: docs/research/skills/<skill-name>/
Keep research materials? [Keep/Remove] (default: Keep)
```

**Artifact Cleanup:**

Ask user about research materials:

- **Keep** (default): Preserves research for future iterations, builds knowledge base
- **Remove**: Cleans up workspace, research can be re-gathered if needed

**Next Steps:**

Present options to user:

```text
Next steps - choose an option:
  [1] Test the skill now - Try invoking it in a new conversation
  [2] Create PR - Submit skill to repository
  [3] Add to plugin.json - Integrate with plugin manifest (if applicable)
  [4] Done - Exit workflow

What would you like to do?
```

**User Actions:**

1. **Test the skill now** → Guide user to test skill invocation
2. **Create PR** → Create git branch, commit, push, open PR
3. **Add to plugin.json** → Update manifest, validate structure (for plugin skills)
4. **Done** → Clean exit

Execute the user's choice, then exit cleanly.

## Examples

### Example 1: Creating Infrastructure Skill (Path 2)

```text
User: "Create terraform-best-practices skill"

skill-factory:
"Have you already gathered research for this skill?
[Yes - I have research at <path>]
[No - Help me gather research]
[Skip - I'll create from knowledge only]"

User: "No - Help me gather research"

skill-factory initializes TodoWrite with 9 tasks, starts workflow:

[Phase 1: Research]
Invokes: /skill-research terraform-best-practices
Mini brainstorm about scope and categories
Executes firecrawl research script
Research saved to docs/research/skills/terraform-best-practices/
✓ Research completed

[Phase 2: Format]
Invokes: /skill-format docs/research/skills/terraform-best-practices
Cleans UI artifacts and navigation elements
✓ Formatting completed

[Phase 3: Create]
Invokes: /skill-create terraform-best-practices docs/research/skills/terraform-best-practices
Delegates to skill-creator skill
Follows Understand → Plan → Initialize → Edit → Package workflow
✓ Skill created at plugins/infrastructure/terraform-skills/skills/terraform-best-practices/

[Phase 4: Review Content]
Invokes: /skill-review-content plugins/infrastructure/terraform-skills/skills/terraform-best-practices
Analyzes clarity, completeness, examples, actionability, usefulness
✓ Content review passed (5/5 quality dimensions)

[Phase 5: Review Compliance]
Invokes: /skill-review-compliance plugins/infrastructure/terraform-skills/skills/terraform-best-practices
Runs quick_validate.py
✓ Compliance check passed

[Phase 6: Validate Runtime]
Invokes: /skill-validate-runtime plugins/infrastructure/terraform-skills/skills/terraform-best-practices
Tests skill loading in Claude Code context
✓ Runtime validation passed

[Phase 7: Validate Integration]
Invokes: /skill-validate-integration plugins/infrastructure/terraform-skills/skills/terraform-best-practices
Checks for conflicts with existing skills
✓ Integration validation passed

[Phase 8: Audit]
Invokes: /skill-validate-audit plugins/infrastructure/terraform-skills/skills/terraform-best-practices
Runs claude-skill-auditor agent
ℹ Audit completed with recommendations (non-blocking)

[Phase 9: Complete]
✅ Skill created and validated successfully!

Location: plugins/infrastructure/terraform-skills/skills/terraform-best-practices/

Research materials: docs/research/skills/terraform-best-practices/
Keep research materials? [Keep/Remove] (default: Keep)

User: Keep

Next steps - choose an option:
  [1] Test the skill now
  [2] Create PR
  [3] Add to plugin.json
  [4] Done

User: [2] Create PR

skill-factory creates branch, commits skill, pushes, opens PR
Workflow complete!
```

### Example 2: Creating Skill with Existing Research (Path 1)

```text
User: "Create coderabbit skill, research in docs/research/skills/coderabbit/"

skill-factory detects explicit research path, uses Path 1

Initializes TodoWrite with 8 tasks (skips research), starts workflow:

[Phase 1: Format]
Invokes: /skill-format docs/research/skills/coderabbit
✓ Formatting completed

[Phase 2: Create]
Invokes: /skill-create coderabbit docs/research/skills/coderabbit
✓ Skill created

[Continues through remaining phases...]
✓ Workflow complete
```

### Example 3: Workflow Failure with Guided Fix

```text
[Phase 4: Review Content]
Invokes: /skill-review-content plugins/meta/meta-claude/skills/docker-compose

Command response:
{
  "status": "fail",
  "issues": [
    {
      "tier": "medium",
      "category": "examples",
      "description": "Examples section missing practical docker-compose.yml configurations",
      "suggestion": "[Shows proposed examples with common patterns]",
      "auto_fixable": false
    }
  ]
}

skill-factory detects Tier 2 (guided fix):

"Content review found issues that can be fixed:

Issue: Examples section missing practical docker-compose.yml configurations

Suggested fix:
[Shows proposed docker-compose.yml examples]

Apply this fix? [Yes/No/Edit]"

User: Yes

skill-factory applies fix, re-runs command:

Invokes: /skill-review-content plugins/meta/meta-claude/skills/docker-compose
✓ Content review passed

Continues to next phase...
```

### Example 4: Workflow Failure with Complex Issue

```text
[Phase 4: Review Content]
Invokes: /skill-review-content plugins/meta/meta-claude/skills/advanced-orchestration

Command response:
{
  "status": "fail",
  "issues": [
    {
      "tier": "complex",
      "category": "architectural",
      "description": "Skill attempts to nest sub-agents within sub-agents, which violates Claude Code composition rules",
      "recommendation": "Restructure skill to use SlashCommand tool for sub-agent invocation. See multi-agent-composition skill for patterns.",
      "auto_fixable": false
    }
  ]
}

skill-factory detects Tier 3 (complex), fails fast:

❌ Skill creation failed at: Review Content Quality

Issue found:
- [Tier 3: Complex] Skill attempts to nest sub-agents within sub-agents, which violates Claude Code composition rules

Recommendation:
- Restructure skill to use SlashCommand tool for sub-agent invocation
- See: plugins/meta/meta-claude/skills/multi-agent-composition/patterns/orchestrator-pattern.md

Workflow stopped. Please fix manually and restart with:
  skill-factory advanced-orchestration docs/research/skills/advanced-orchestration/

Artifacts preserved at:
  Research: docs/research/skills/advanced-orchestration/
  Partial skill: plugins/meta/meta-claude/skills/advanced-orchestration/

WORKFLOW EXITS
```

## Design Principles

### 1. Primitives First

Slash commands are the foundation. The skill orchestrates them using the SlashCommand tool. This follows the
multi-agent-composition principle: "Always start with prompts."

### 2. KISS State Management

TodoWrite provides visibility without complexity. No external state files, no databases, no complex checkpointing.
Simple, effective progress tracking.

### 3. Fail Fast

No complex recovery mechanisms. When something can't be auto-fixed or user declines a fix, exit immediately with
clear guidance. Preserves artifacts, provides next steps.

### 4. Context-Aware Entry

Detects workflow path from user's prompt. Explicit research location → Path 1. Ambiguous → Ask user. Natural
language interface.

### 5. Composable & Testable

Every primitive works standalone (power users) or orchestrated (guided users). Each command is independently
testable and verifiable.

### 6. Quality Gates

Sequential dependencies ensure quality: content before compliance, runtime before integration. Tiered validation
with non-blocking audit for comprehensive feedback.

## Implementation Notes

### Delegation Architecture

skill-factory extends the proven skill-creator skill by adding:

- **Pre-creation phases:** Research gathering and formatting
- **Post-creation phases:** Content review and validation
- **Quality gates:** Compliance checking, runtime testing, integration validation

**Delegation to existing tools:**

- **skill-creator skill** → Core creation workflow (Understand → Plan → Initialize → Edit → Package)
- **quick_validate.py** → Compliance validation (frontmatter, naming, structure)
- **claude-skill-auditor agent** → Comprehensive audit

This separation maintains the stability of skill-creator while adding research-backed, validated skill creation
with quality gates.

### Progressive Disclosure

This skill provides:

1. **Quick Start** - Fast path for common use cases
2. **Workflow Architecture** - Understanding the orchestration model
3. **Detailed Phase Documentation** - Deep dive into each phase
4. **Error Handling** - Comprehensive fix strategies
5. **Examples** - Real-world scenarios

Load sections as needed for your use case.

## Troubleshooting

### Research Phase Fails

**Symptom:** `/skill-research` command fails with API errors

**Solutions:**

- Verify FIRECRAWL_API_KEY is set: `echo $FIRECRAWL_API_KEY`
- Check network connectivity
- Verify research script permissions: `chmod +x scripts/firecrawl_*.py`
- Try manual research and use Path 1 (skip research phase)

### Content Review Fails Repeatedly

**Symptom:** `/skill-review-content` fails even after applying fixes

**Solutions:**

- Review the specific issues in the quality report
- Check if issues are Tier 3 (complex) - these require manual redesign
- Consider if the skill design matches Claude Code's composition model
- Consult multi-agent-composition skill for architectural guidance

### Compliance Validation Fails

**Symptom:** `/skill-review-compliance` reports frontmatter or naming violations

**Solutions:**

- Run quick_validate.py manually: `scripts/quick_validate.py <skill-path>`
- Check frontmatter YAML syntax (valid YAML, required fields)
- Verify skill name follows hyphen-case convention
- Ensure description is clear and within 1024 characters

### Integration Validation Fails

**Symptom:** `/skill-validate-integration` reports conflicts

**Solutions:**

- Check for duplicate skill names in the plugin
- Review skill description for overlap with existing skills
- Consider renaming or refining scope to avoid conflicts
- Ensure skill complements rather than duplicates existing functionality

## Success Metrics

You know skill-factory succeeds when:

1. **Time to create skill:** Reduced from hours to minutes
2. **Skill quality:** 100% compliance with official specs on first validation
3. **User satisfaction:** Beginners create high-quality skills without deep knowledge
4. **Maintainability:** Primitives are independently testable and reusable
5. **Workflow clarity:** Users understand current phase and next steps at all times

## Related Resources

- **skill-creator skill** - Core skill creation workflow (delegated by skill-factory)
- **multi-agent-composition skill** - Architectural patterns and composition rules
- **Primitive commands** - Individual slash commands under `/skill-*` namespace
- **quick_validate.py** - Compliance validation script
- **claude-skill-auditor agent** - Comprehensive skill audit agent
