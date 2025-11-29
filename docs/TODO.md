# TODO

## skill-factory End-to-End Testing

**Priority: HIGH** - Workflow gap was fixed but not validated end-to-end.

### Test Procedure

1. Start fresh Claude Code session (commands need reload)
2. Invoke skill-factory for a new skill:

   ```text
   Use skill-factory to create a skill for [topic]
   ```

3. Verify each phase executes in order:
   - [ ] Entry point detection asks about research
   - [ ] TodoWrite initialized with all 10 phases
   - [ ] `/meta-claude:skill:research` runs (or skipped)
   - [ ] `/meta-claude:skill:format` runs
   - [ ] `/meta-claude:skill:create` scaffolds skill directory
   - [ ] `/meta-claude:skill:write` synthesizes content from references
   - [ ] `/meta-claude:skill:review-content` validates quality
   - [ ] `/meta-claude:skill:review-compliance` runs quick_validate.py
   - [ ] `/meta-claude:skill:validate-runtime` tests loading
   - [ ] `/meta-claude:skill:validate-integration` checks conflicts
   - [ ] `/meta-claude:skill:validate-audit` runs auditor agent
   - [ ] Completion options presented

### Key Validations

- [ ] `write` command is discoverable via SlashCommand
- [ ] `write` actually synthesizes content (not just TODOs)
- [ ] Dependencies enforced: write→review-content→review-compliance
- [ ] Fail-fast triggers on Tier 3 issues
- [ ] Error handling works at each phase

### Test Scenarios

| Scenario | Command | Expected |
|----------|---------|----------|
| With research | `skill-factory foo docs/research/foo/` | Skip research, start at format |
| Without research | `skill-factory bar` | Ask about research sources |
| Skip research | Select "Skip" option | Start at create with empty refs |
