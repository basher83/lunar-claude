# Workflow Execution

## Phase Invocation Pattern

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
