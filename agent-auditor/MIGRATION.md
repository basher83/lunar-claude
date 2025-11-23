# Migration Checklist

This document tracks the migration of agent-auditor content from lunar-claude to a standalone repository.

## Status

**Current Phase:** Packaging Complete ✅

All content has been copied to `agent-auditor/` directory. Original files remain in lunar-claude repository.

## What Was Copied

### Documentation (✅ Complete)
- [x] Research documentation from `docs/research/audit-skill/`
- [x] Review documentation from `docs/reviews/skill-auditor/`
- [x] Audit reports from `docs/reviews/audits/meta-claude/`
- [x] Notes from `docs/notes/` (skill-auditor related)
- [x] Planning documents from `docs/plans/` (skill-auditor related)

### Source Code (✅ Complete)
- [x] Python SDK from `scripts/skill_auditor/`
- [x] Main CLI script `scripts/skill-auditor.py`
- [x] All test files

### Agents (✅ Complete)
- [x] All agent definitions from `plugins/meta/meta-claude/agents/skill/`

### Commands (✅ Complete)
- [x] Command definitions from `plugins/meta/meta-claude/commands/skill/`

## Next Steps for New Repository

### 1. Repository Setup
- [ ] Create new GitHub repository `agent-auditor`
- [ ] Initialize git repository
- [ ] Copy content from `agent-auditor/` to new repo root
- [ ] Create `.gitignore` (Python, Claude Code patterns)
- [ ] Add LICENSE file

### 2. Project Configuration
- [ ] Create `pyproject.toml` with proper dependencies
- [ ] Set up Python package structure
- [ ] Configure build system (uv, pip, etc.)
- [ ] Add pre-commit hooks if desired

### 3. Update File Paths
- [ ] Update import paths in Python files
- [ ] Update file references in agent definitions
- [ ] Update documentation cross-references
- [ ] Fix any hardcoded paths

### 4. Documentation
- [ ] Create comprehensive README.md
- [ ] Write usage guides
- [ ] Document API reference
- [ ] Create CHANGELOG.md from git history

### 5. Testing
- [ ] Verify all tests pass in new structure
- [ ] Update test paths if needed
- [ ] Set up CI/CD if desired

### 6. Cleanup
- [ ] Review and remove unnecessary files
- [ ] Organize documentation structure
- [ ] Archive historical versions appropriately

## Files That Reference Skill Auditor (Need Updates)

These files in lunar-claude reference skill-auditor and may need updates:

- `CLAUDE.md` - Line 8 mentions skill-auditor in audit protocol
  - **Action:** Add note pointing to new repository

- `.claude-plugin/marketplace.json` - May reference skill-auditor commands
  - **Action:** Remove or update references

## Notes

- All files copied (not moved) - originals preserved
- Structure mirrors proposed new repository layout
- Some files may need path updates after migration
- Agent definitions may reference local paths that need updating
