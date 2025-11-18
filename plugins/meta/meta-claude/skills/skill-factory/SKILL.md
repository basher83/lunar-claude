---
name: skill-factory
description: |
  Orchestrates Claude Code skill development using 8 primitive slash commands
  (/meta-claude:skill:research, /meta-claude:skill:format, /meta-claude:skill:create,
  /meta-claude:skill:review-content, /meta-claude:skill:review-compliance,
  /meta-claude:skill:validate-runtime, /meta-claude:skill:validate-integration,
  /meta-claude:skill:validate-audit). Use when: (1) Creating SKILL.md files with YAML frontmatter and
  progressive disclosure, (2) Building skills with scripts/, references/, or assets/ directories,
  (3) Automating firecrawl-based research gathering, (4) Validating skills against Anthropic specifications,
  or (5) Requiring TodoWrite-tracked workflow with tiered error handling (auto-fix, guided-fix, fail-fast).
  Creates infrastructure, development, or domain-specific skills extending Claude capabilities.
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

## Quick Decision Guide

Choose your starting point:

**Most common:** Creating skill from scratch
→ Use: `skill-factory <skill-name>` (starts research workflow)

**Research already gathered:** You have `docs/research/skills/<name>/`
→ Use: `skill-factory <skill-name> <research-path>` (skips research)

**Validation only:** Skill exists, need quality check
→ Use: `/meta-claude:skill:review-content <path>` (direct validation)

**Integration check:** Adding skill to existing plugin
→ Use: `/meta-claude:skill:validate-integration <path>` (conflict detection)

For full workflow details, see Quick Start section below.

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

## When This Skill Is Invoked

**Your role:** You are the skill-factory orchestrator. Your task is to guide the user through creating
a high-quality, validated skill using 8 primitive slash commands.

### Step 1: Entry Point Detection

Analyze the user's prompt to determine which workflow path to use:

**If research path is explicitly provided:**

```text
User: "skill-factory coderabbit docs/research/skills/coderabbit/"
→ Use Path 1 (skip research phase)
```

**If no research path is provided:**

Ask the user using AskUserQuestion:

```text
"Have you already gathered research for this skill?"

Options:
[Yes - I have research at a specific location]
[No - Help me gather research]
[Skip - I'll create from knowledge only]
```

**Based on user response:**

- **Yes** → Ask for research path, use Path 1
- **No** → Use Path 2 (include research phase)
- **Skip** → Use Path 1 without research (create from existing knowledge)

### Step 2: Initialize TodoWrite

Create a TodoWrite list based on the selected path:

**Path 2 (Full Workflow with Research):**

```javascript
TodoWrite([
  {"content": "Research skill domain", "status": "pending", "activeForm": "Researching skill domain"},
  {"content": "Format research materials", "status": "pending", "activeForm": "Formatting research materials"},
  {"content": "Create skill structure", "status": "pending", "activeForm": "Creating skill structure"},
  {"content": "Review content quality", "status": "pending", "activeForm": "Reviewing content quality"},
  {"content": "Review technical compliance", "status": "pending", "activeForm": "Reviewing technical compliance"},
  {"content": "Validate runtime loading", "status": "pending", "activeForm": "Validating runtime loading"},
  {"content": "Validate integration", "status": "pending", "activeForm": "Validating integration"},
  {"content": "Run comprehensive audit", "status": "pending", "activeForm": "Running comprehensive audit"},
  {"content": "Complete workflow", "status": "pending", "activeForm": "Completing workflow"}
])
```

**Path 1 (Research Exists or Skipped):**

Omit the first "Research skill domain" task. Start with "Format research materials" or
"Create skill structure" depending on whether research exists.

### Step 3: Execute Workflow Sequentially

For each phase in the workflow, follow this pattern:

#### 1. Mark phase as in_progress

Update the corresponding TodoWrite item to `in_progress` status.

#### 2. Check dependencies

Before running a command, verify prior phases completed:

- Review-compliance requires review-content to pass
- Validate-runtime requires review-compliance to pass
- Validate-integration requires validate-runtime to pass
- Validate-audit runs regardless (non-blocking feedback)

#### 3. Invoke command using SlashCommand tool

```text
/meta-claude:skill:research <skill-name> [sources]
/meta-claude:skill:format <research-dir>
/meta-claude:skill:create <skill-name> <research-dir>
/meta-claude:skill:review-content <skill-path>
/meta-claude:skill:review-compliance <skill-path>
/meta-claude:skill:validate-runtime <skill-path>
/meta-claude:skill:validate-integration <skill-path>
/meta-claude:skill:validate-audit <skill-path>
```

**IMPORTANT:** Wait for each command to complete before proceeding to the next phase.
Do not invoke multiple commands in parallel.

#### 4. Check command result

Each command returns success or failure with specific error details.

#### 5. Apply fix strategy if needed

Use the three-tier fix strategy:

**Tier 1 (Simple - Auto-fix):**

- Formatting errors, frontmatter syntax, markdown issues
- Apply fix automatically, re-run command once
- If still fails → escalate to Tier 2

**Tier 2 (Medium - Guided-fix):**

- Content clarity issues, instruction rewording
- Present suggested fix to user
- Ask: "Apply this fix? [Yes/No/Edit]"
- If user approves → Apply fix, re-run once
- If user declines or still fails → fail fast

**Tier 3 (Complex - Fail-fast):**

- Architectural problems, schema violations, composition rule violations
- Report issue with detailed explanation
- Provide recommendations for manual fixes
- **Exit workflow immediately** - user must fix manually

**One-shot policy:** Apply fix once, re-run once. If still broken, fail fast (prevents infinite loops).

#### 6. Mark phase completed

Update TodoWrite item to `completed` status.

#### 7. Continue to next phase

Proceed to the next workflow phase, or exit if fail-fast triggered.

### Step 4: Completion

When all phases pass successfully:

**Present completion summary:**

```text
✅ Skill created and validated successfully!

Location: <skill-output-path>/

Research materials: docs/research/skills/<skill-name>/
```

**Ask about artifact cleanup:**

```text
Keep research materials? [Keep/Remove] (default: Keep)
```

**Present next steps using AskUserQuestion:**

```text
Next steps - choose an option:
[Test the skill now - Try invoking it in a new conversation]
[Create PR - Submit skill to repository]
[Add to plugin.json - Integrate with plugin manifest]
[Done - Exit workflow]
```

**Execute user's choice:**

- **Test** → Guide user to test skill invocation
- **Create PR** → Create git branch, commit, push, open PR
- **Add to plugin.json** → Update manifest, validate structure
- **Done** → Clean exit

### Key Execution Principles

**Sequential Execution:** Do not run commands in parallel. Wait for each phase to complete before proceeding.

**Context Window Protection:** You are orchestrating commands, not sub-agents. Your context window is safe
because you're invoking slash commands sequentially, not spawning multiple agents.

**State Management:** TodoWrite provides real-time progress visibility. Update it at every phase
transition.

**Fail Fast:** When Tier 3 issues occur or user declines fixes, exit immediately with clear guidance.
Don't attempt complex recovery.

**Dependency Enforcement:** Never skip dependency checks. Review phases are sequential, validation
phases are tiered.

**One-shot Fixes:** Apply each fix once, re-run once, then fail if still broken. This prevents infinite loops.

**User Communication:** Report progress clearly. Show which phase is running, what the result was,
and what's happening next.

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
   /meta-claude:skill:research <skill-name> [sources]
   /meta-claude:skill:format <research-dir>
   /meta-claude:skill:create <skill-name> <research-dir>
   /meta-claude:skill:review-content <skill-path>
   /meta-claude:skill:review-compliance <skill-path>
   /meta-claude:skill:validate-runtime <skill-path>
   /meta-claude:skill:validate-integration <skill-path>
   /meta-claude:skill:validate-audit <skill-path>
   ```

4. **Check result** (success or failure with tier metadata)
5. **Apply fix strategy** (if needed - see Error Handling section)
6. **Mark phase completed** (update TodoWrite)
7. **Continue to next phase** (or exit if fail-fast triggered)

### Dependency Enforcement

Before running each command, verify dependencies:

**Review Phase (Sequential):**

```text
/meta-claude:skill:review-content (no dependency)
  ↓ (must pass)
/meta-claude:skill:review-compliance (depends on content passing)
```

**Validation Phase (Tiered):**

```text
/meta-claude:skill:validate-runtime (depends on compliance passing)
  ↓ (must pass)
/meta-claude:skill:validate-integration (depends on runtime passing)
  ↓ (runs regardless)
/meta-claude:skill:validate-audit (non-blocking, informational)
```

**Dependency Check Pattern:**

```text
Before running /meta-claude:skill:review-compliance:
  Check: Is "Review content quality" completed?
    - Yes → Invoke /meta-claude:skill:review-compliance
    - No → Skip (workflow failed earlier, stop here)
```

### Command Invocation with SlashCommand Tool

Use the SlashCommand tool to invoke each primitive command:

```javascript
// Example: Invoking research phase
SlashCommand({
  command: "/meta-claude:skill:research ansible-vault-security"
})

// Example: Invoking format phase
SlashCommand({
  command: "/meta-claude:skill:format docs/research/skills/ansible-vault-security"
})

// Example: Invoking create phase
SlashCommand({
  command: "/meta-claude:skill:create ansible-vault-security docs/research/skills/ansible-vault-security"
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

**Symptom:** `/meta-claude:skill:research` command fails with API errors

**Solutions:**

- Verify FIRECRAWL_API_KEY is set: `echo $FIRECRAWL_API_KEY`
- Check network connectivity
- Verify research script permissions: `chmod +x scripts/firecrawl_*.py`
- Try manual research and use Path 1 (skip research phase)

### Content Review Fails Repeatedly

**Symptom:** `/meta-claude:skill:review-content` fails even after applying fixes

**Solutions:**

- Review the specific issues in the quality report
- Check if issues are Tier 3 (complex) - these require manual redesign
- Consider if the skill design matches Claude Code's composition model
- Consult multi-agent-composition skill for architectural guidance

### Compliance Validation Fails

**Symptom:** `/meta-claude:skill:review-compliance` reports frontmatter or naming violations

**Solutions:**

- Run quick_validate.py manually: `scripts/quick_validate.py <skill-path>`
- Check frontmatter YAML syntax (valid YAML, required fields)
- Verify skill name follows hyphen-case convention
- Ensure description is clear and within 1024 characters

### Integration Validation Fails

**Symptom:** `/meta-claude:skill:validate-integration` reports conflicts

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
