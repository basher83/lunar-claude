# Error Handling & Fix Strategy

## Core Principle: Fail Fast

When a phase fails without auto-fix capability, the workflow **stops immediately**. No complex recovery, no
checkpointing, no resume commands—only clean exit with clear error reporting and preserved artifacts.

## Rule-Based Fix Tiers

Issues are categorized into three tiers based on complexity:

### Tier 1: Simple (Auto-Fix)

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

### Tier 2: Medium (Guided Fix with Approval)

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

### Tier 3: Complex (Stop and Report)

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

## One-Shot Fix Policy

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

## Issue Categorization Response Format

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

## Parsing Command Responses

When a command completes, analyze its output to determine status:

- Look for "Success", "PASS", or exit code 0 → Continue
- Look for "Error", "FAIL", or exit code 1 → Apply fix strategy
- Parse issue tier metadata (if provided) to select fix approach
- If no tier metadata, infer tier from issue description
