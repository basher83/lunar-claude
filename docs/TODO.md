# TODO

## ansible-workflows Plugin Validation and Testing

**Priority: HIGH** - New pipeline orchestration system needs end-to-end validation.

### Test Scenarios

1. **Happy path**: `/ansible-workflows:create-playbook` → generator → validator (PASS) → reviewer (APPROVED)
2. **Validation failure**: generator → validator (FAIL) → debugger → validator (PASS)
3. **Review rejection**: validator (PASS) → reviewer (NEEDS_REWORK) → debugger
4. **Stop hook test**: Interrupt mid-pipeline, verify session stop is blocked
5. **Max retries**: 3 validation failures → escalate to user

### Key Validations

- [ ] State file created with correct YAML frontmatter
- [ ] Context bundles written at each agent handoff
- [ ] SubagentStop hook updates pipeline phase correctly
- [ ] Stop hook blocks termination when `active: true`
- [ ] Gitignore patterns auto-added to project
- [ ] `$CLAUDE_PROJECT_DIR` paths resolve correctly
- [ ] Retry counter increments on validation failures
- [ ] Pipeline completes and sets `active: false` on APPROVED

### Hook Script Testing

```bash
# Test hook scripts directly
echo '{"cwd": "/tmp/test", "session_id": "test"}' | \
  uv run plugins/infrastructure/ansible-workflows/hooks/check-pipeline-state.py
```

## meta-claude Plugin Review and Refactor

**Priority: MEDIUM** - Plugin needs modernization to match current patterns.

### Review Areas

- [ ] Skill definitions follow current SKILL.md standards
- [ ] Commands use proper frontmatter format (JSON arrays for allowed-tools)
- [ ] Agent descriptions have concrete trigger examples
- [ ] skill-factory workflow still functional after skill-development updates
- [ ] Remove deprecated or unused components
- [ ] Consolidate overlapping skills

### Potential Refactors

- Align with plugin-dev patterns (the meta plugin for plugin development)
- Consider merging meta-claude into plugin-dev or deprecating
- Update skill-factory to use newer orchestration patterns (bundles, state files)

## skill-factory Review and Refactor

**Priority: MEDIUM** - Workflow is outdated and needs modernization.

### Current Issues

- Uses old orchestration pattern (TodoWrite phases vs. state files + bundles)
- 10-phase workflow may be overly complex
- Depends on meta-claude commands that may also be outdated
- Not aligned with current plugin-dev skill-development patterns

### Review Areas

- [ ] Evaluate if skill-factory is still needed vs. plugin-dev:skill-development
- [ ] Compare orchestration approach to ansible-workflows (state files, bundles)
- [ ] Check if slash commands are still functional
- [ ] Review validation scripts for current compatibility
- [ ] Assess overlap with plugin-dev plugin

### Refactor Options

1. **Deprecate**: Remove skill-factory, use plugin-dev:skill-development instead
2. **Modernize**: Update to use state files + context bundles pattern
3. **Simplify**: Reduce 10-phase workflow to essential steps
4. **Merge**: Consolidate into plugin-dev as unified skill creation workflow

### Legacy Test Procedure (if keeping)

1. Start fresh Claude Code session
2. Invoke: `Use skill-factory to create a skill for [topic]`
3. Verify phases execute and hand off correctly

## Bulk Plugin Validation

**Priority: LOW** - Found issues in ansible-workflows (allowed-tools format). Other plugins may have similar problems.

### Task

Run `plugin-dev:plugin-validator` across all plugins in marketplace:

```bash
# Get all plugin paths
jq -r '.plugins[].path' .claude-plugin/marketplace.json
```

### Common Issues to Check

- [ ] `allowed-tools` using comma strings instead of JSON arrays
- [ ] Missing or outdated README.md
- [ ] Agent descriptions lacking `<example>` blocks
- [ ] Skills missing concrete triggers
- [ ] Hooks using old patterns

## evaluate hook for upgrade

**Priority: LOW** - Script does a fairly good job but sometimes adds wrong language in fenced code blocks.

File: `scripts/markdown_formatter.py`
