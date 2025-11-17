---
name: skill-factory
description: |
  Orchestrates Claude Code skill development using 8 primitive slash commands (/skill-research, /skill-format,
  /skill-create, /skill-review-content, /skill-review-compliance, /skill-validate-runtime, /skill-validate-integration,
  /skill-validate-audit). This skill should be used when: (1) Creating SKILL.md files with YAML frontmatter and
  progressive disclosure, (2) Building skills with scripts/, references/, or assets/ directories, (3) Automating
  firecrawl-based research gathering for skill domains, (4) Validating skills against Anthropic specifications using
  quick_validate.py, or (5) Requiring TodoWrite-tracked workflow with tiered error handling (auto-fix, guided-fix,
  fail-fast). Creates infrastructure skills (terraform-best-practices), development skills (docker-compose-helper),
  or domain-specific skills (brand-guidelines, conventional-git-commits) extending Claude capabilities.
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

The workflow uses a three-tier fix strategy with fail-fast principles:

- **Tier 1 (Simple):** Auto-fix formatting, frontmatter, markdown syntax - automatically re-run once
- **Tier 2 (Medium):** Guided fixes for content clarity - ask user approval before applying
- **Tier 3 (Complex):** Stop and report architectural issues - fail fast with recommendations

**One-Shot Policy:** Apply fix once, re-run once, then fail fast if still broken (prevents infinite loops).

**Detailed Error Handling:** See [references/error-handling.md](references/error-handling.md) for complete fix tier
definitions, examples, issue categorization format, and command response parsing guidance.

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

The skill-factory workflow supports various scenarios:

1. **Path 2 (Full Workflow):** Creating skills from scratch with automated research gathering
2. **Path 1 (Existing Research):** Creating skills when research materials already exist
3. **Guided Fix Workflow:** Applying Tier 2 fixes with user approval
4. **Fail-Fast Pattern:** Handling Tier 3 complex issues with immediate exit

**Detailed Examples:** See [references/workflow-examples.md](references/workflow-examples.md) for complete walkthrough
scenarios showing TodoWrite state transitions, command invocations, error handling, and success paths.

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
