# Workflow Examples

## Example 1: Creating Infrastructure Skill (Path 2)

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

## Example 2: Creating Skill with Existing Research (Path 1)

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

## Example 3: Workflow Failure with Guided Fix

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

## Example 4: Workflow Failure with Complex Issue

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

## Command Output Reference

### Successful Command Outputs

**Research:**

```bash
✓ Research completed for terraform-best-practices
Saved to: docs/research/skills/terraform-best-practices/
Files: 5 documents (github: 3, research: 2)
```

**Format:**

```text
✓ Formatting completed
Cleaned: 5 files, removed 247 UI artifacts
Output: docs/research/skills/terraform-best-practices/
```

**Validation (Pass):**

```text
✓ Content review passed (5/5 quality dimensions)
✓ Compliance check passed
✓ Runtime validation passed
✓ Integration validation passed
```

### Failed Command Outputs

**Tier 1 (Auto-fix):**

```json
{
  "status": "fail",
  "issues": [
    {
      "tier": "simple",
      "category": "frontmatter",
      "description": "Missing description field",
      "fix": "Add description: 'Terraform infrastructure best practices'",
      "auto_fixable": true
    }
  ]
}
```

**Tier 2 (Guided fix):**

```json
{
  "status": "fail",
  "issues": [
    {
      "tier": "medium",
      "category": "examples",
      "description": "Examples section lacks practical configurations",
      "suggestion": "[Proposed examples with common patterns]",
      "auto_fixable": false
    }
  ]
}
```

**Tier 3 (Complex):**

```json
{
  "status": "fail",
  "issues": [
    {
      "tier": "complex",
      "category": "architectural",
      "description": "Violates composition rules",
      "recommendation": "Restructure to use SlashCommand tool",
      "auto_fixable": false
    }
  ]
}
```
