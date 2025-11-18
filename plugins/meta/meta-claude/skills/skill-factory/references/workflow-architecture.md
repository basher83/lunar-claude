# Workflow Architecture

## Entry Point Detection

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

## Workflow Paths

### Path 1: Research Exists

```text
format → create → review-content → review-compliance →
validate-runtime → validate-integration → validate-audit → complete
```

### Path 2: Research Needed

```text
research → format → create → review-content → review-compliance →
validate-runtime → validate-integration → validate-audit → complete
```

## State Management

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
