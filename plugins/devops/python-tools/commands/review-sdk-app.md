---
description: Review and validate a Claude Agent SDK application against best practices
argument-hint: [path-to-app]
---

You are tasked with reviewing a Claude Agent SDK (Python) application to ensure it follows SDK best practices and official documentation patterns. Follow these steps carefully:

## Reference Documentation

Before starting, load the **claude-agent-sdk skill** to access patterns, examples, and the validation checklist:

```bash
# Load the skill for comprehensive SDK knowledge
/skill claude-agent-sdk
```

The skill provides:
- **Validation checklist**: `assets/sdk-validation-checklist.md` (comprehensive review guide)
- **SDK patterns**: `SKILL.md` and `references/` (official best practices)
- **Working examples**: `examples/` (reference implementations)
- **Template**: `assets/sdk-template.py` (ideal structure)

## Review Approach

You have TWO options for reviewing SDK applications:

### Option 1: Automated Validation (Recommended)

Launch the **agent-sdk-verifier-py** subagent for comprehensive automated review:

```bash
# The subagent will:
# - Read all application files
# - Check SDK patterns and configuration
# - Validate against official documentation
# - Provide detailed report with specific issues and recommendations
```

**Best for:**
- Quick validation
- New applications
- Pre-deployment checks
- Comprehensive coverage

### Option 2: Manual Guided Review

Follow the validation checklist step-by-step with guided assistance.

**Best for:**
- Learning SDK patterns
- Understanding specific issues
- Deep dive into SDK concepts
- Educational reviews

## Gather Information

Ask the user (if not provided via $ARGUMENTS):

1. **Application path**: "What is the path to your SDK application?"
   - If $ARGUMENTS is provided, use that as the application path
   - Wait for response before continuing

2. **Review type**: "Would you like:
   - Automated validation (launch agent-sdk-verifier-py)
   - Manual guided review (step-by-step checklist)
   - Both (automated first, then deep dive on issues)"
   - Wait for response before continuing

## Automated Validation Flow

If user chooses automated validation:

1. **Launch verifier agent**:
   - Use Task tool to launch `agent-sdk-verifier-py` subagent
   - Provide the application path to the agent
   - Wait for verification report

2. **Review the report**:
   - **Overall Status**: PASS | PASS WITH WARNINGS | FAIL
   - **Critical Issues**: Must be fixed before deployment
   - **Warnings**: Suboptimal patterns or improvements
   - **Passed Checks**: Correctly configured elements
   - **Recommendations**: Specific improvements with references

3. **Address issues**:
   - For each critical issue: explain the problem and provide fix
   - For warnings: explain why the recommendation matters
   - Reference specific skill documentation for context

4. **Re-validate if changes made**:
   - After fixes, offer to re-run validation
   - Ensure all critical issues are resolved

## Manual Guided Review Flow

If user chooses manual review, systematically work through the validation checklist (`assets/sdk-validation-checklist.md`):

### Section 1: Imports & Dependencies

Read the application files and check:

- [ ] Async runtime import (anyio or asyncio)
- [ ] Claude SDK imports are accurate
- [ ] UV script headers (if single-file script)

**Ask user**: "Found any issues with imports? (Y/N)"

If yes, explain the issue and show correct pattern from skill examples.

### Section 2: Async Runtime

Check:

- [ ] Runtime execution (`anyio.run()` or `asyncio.run()`)
- [ ] Async/await patterns are correct
- [ ] Context managers for ClaudeSDKClient

**Ask user**: "Found any issues with async patterns? (Y/N)"

### Section 3: query() vs ClaudeSDKClient Choice

Check:

- [ ] Correct approach for use case
- [ ] Not using hooks/custom tools with query()

**Ask user**: "Is the query()/ClaudeSDKClient choice appropriate? (Y/N)"

If no, explain when to use each approach (reference SKILL.md lines 29-44).

### Section 4: Orchestrator Configuration (if applicable)

Check:

- [ ] System prompt is `"claude_code"` for orchestrators
- [ ] Task tool is included in allowed_tools
- [ ] Agents are registered programmatically

**Ask user**: "Found any orchestrator configuration issues? (Y/N)"

### Section 5: Agent Definitions (if applicable)

Check:

- [ ] Agent structure is correct (description, prompt, tools, model)
- [ ] Agent names match between definition and usage
- [ ] Tools are restricted to minimum needed

**Ask user**: "Found any agent definition issues? (Y/N)"

### Section 6: Permission Control

Check:

- [ ] Permission strategy is appropriate
- [ ] Permission mode is valid
- [ ] Permission callback (if used) is correct

**Ask user**: "Found any permission issues? (Y/N)"

### Section 7: Hooks (if used)

Check:

- [ ] Hooks ONLY used with ClaudeSDKClient
- [ ] Hook types are supported (not using SessionStart, etc.)
- [ ] Hook signature is correct
- [ ] Hook output structure is valid

**Ask user**: "Found any hook issues? (Y/N)"

### Section 8: ClaudeSDKClient Usage (if applicable)

Check:

- [ ] Context manager pattern is used
- [ ] Query → receive_response flow
- [ ] Interrupts (if used) are correct

**Ask user**: "Found any ClaudeSDKClient usage issues? (Y/N)"

### Section 9: Message Handling

Check:

- [ ] Message types are checked correctly
- [ ] TextBlock extraction is correct
- [ ] ResultMessage handling

**Ask user**: "Found any message handling issues? (Y/N)"

### Section 10: Error Handling

Check:

- [ ] API key validation (if running standalone)
- [ ] Safe dictionary access
- [ ] Async exception handling

**Ask user**: "Found any error handling issues? (Y/N)"

### Section 11: Settings & Configuration

Check:

- [ ] setting_sources is configured appropriately
- [ ] Model selection is appropriate
- [ ] Budget limits (if needed)

**Ask user**: "Found any configuration issues? (Y/N)"

### Section 12: Best Practices

Check:

- [ ] Follows DRY principle
- [ ] Clear comments and documentation
- [ ] Type hints are used
- [ ] No anti-patterns

**Ask user**: "Found any best practice violations? (Y/N)"

### Manual Review Summary

After completing all sections, provide:

```markdown
## Validation Summary

### ✅ Passed Checks:
- [List of passed checks]

### ❌ Issues Found:
- [List of issues with severity: CRITICAL | WARNING | INFO]

### 🔧 Fixes Required:
1. [Specific fix with file:line reference and code example]
2. [Specific fix with file:line reference and code example]

### 📊 Overall Assessment:
- **SDK Pattern Adherence**: [High/Medium/Low]
- **Production Ready**: [Yes/No/With Fixes]
- **Recommended Next Steps**: [Specific actions]
```

## Providing Fixes

For each issue identified:

1. **Explain the problem**:
   - Why it's an issue
   - What SDK pattern is being violated
   - Reference to skill documentation

2. **Show the correct pattern**:
   - Code example from skill examples or template
   - Explain why this pattern is preferred
   - Link to relevant skill reference

3. **Provide specific fix**:
   - Exact code change needed
   - File and line reference
   - Before/after comparison if helpful

## Follow-up Actions

After review:

1. **Offer to implement fixes**:
   - "Would you like me to implement these fixes?"
   - If yes, make changes and re-validate

2. **Suggest re-validation**:
   - "Would you like to run automated validation to confirm fixes?"
   - Launch agent-sdk-verifier-py if requested

3. **Recommend next steps**:
   - Additional features to consider
   - Testing recommendations
   - Deployment considerations

## Important Notes

- **USE THE VALIDATION CHECKLIST**: `assets/sdk-validation-checklist.md` is your comprehensive guide
- **REFERENCE SKILL DOCUMENTATION**: Always link to specific skill files for context
- **SHOW WORKING EXAMPLES**: Use examples from `examples/` directory
- **BE SPECIFIC**: Provide file:line references and exact code changes
- **EXPLAIN WHY**: Don't just identify issues, explain the SDK reasoning
- **PRIORITIZE ISSUES**: CRITICAL (breaks functionality) > WARNING (suboptimal) > INFO (nice to have)
- **VERIFY FIXES**: Re-validate after making changes
- **USE AGENT-SDK-VERIFIER-PY**: Leverage automated validation for comprehensive coverage

## Key SDK Patterns to Verify

Always check these common issues:

1. **Orchestrator missing system_prompt**: Must use `"claude_code"`
2. **Orchestrator missing Task tool**: Cannot delegate without it
3. **Agent name mismatches**: Definition name must match usage
4. **Hooks with query()**: Not supported, use ClaudeSDKClient
5. **Custom tools with query()**: Not supported, use ClaudeSDKClient
6. **Excessive tool permissions**: Restrict to minimum needed
7. **Missing agent registration**: Use `agents={}` parameter
8. **Wrong async runtime call**: Use `anyio.run()` or `asyncio.run()`
9. **Missing context manager**: ClaudeSDKClient requires `async with`
10. **Unsafe dictionary access**: Use `.get()` for optional fields

Begin by asking about the application path (if not provided) and review type preference.
