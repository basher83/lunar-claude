# Bug Report: Old claude-docs Skill Directory Not Removed

**Date:** 2025-11-17
**Status:** ✅ RESOLVED
**Plugin:** claude-docs (meta category)
**Severity:** Medium - Causes confusion and stale data
**Resolution:** Removed untracked old directory, verified script works correctly

## Symptom

After renaming the skill from `claude-docs` to `official-docs` in commit ba097c5, the old `skills/claude-docs/` directory still exists in the repository with stale documentation files.

## Root Cause Investigation

### Phase 1: Evidence Gathering

1. **Git History Review**
   - Commit `ba097c5`: "refactor: restructure claude-docs plugin and rename skill to official-docs"
   - This commit renamed `skills/claude-docs/SKILL.md` → `skills/official-docs/SKILL.md`
   - Script updated: `find_or_create_ai_docs_dir()` now returns `"skills/official-docs/reference"`

2. **Current State**
   ```bash
   $ ls -la plugins/meta/claude-docs/skills/
   total 16
   drwxrwxrwx+ 4 codespace codespace 4096 Nov 17 20:49 .
   drwxrwxrwx+ 7 codespace codespace 4096 Nov 17 20:49 ..
   drwxrwxrwx+ 3 codespace codespace 4096 Nov 17 20:49 claude-docs      # OLD - should not exist
   drwxrwxrwx+ 3 codespace codespace 4096 Nov 17 20:49 official-docs    # NEW - correct
   ```

3. **Hook Script Analysis**
   - File: `hooks/hooks.json` (line 9)
   - Command: `${CLAUDE_PLUGIN_ROOT}/scripts/claude_docs.py --format json`
   - Hook script itself is CORRECT - it just calls the Python script

4. **Python Script Analysis**
   - File: `scripts/claude_docs.py` (line 376)
   - Current: `return script_dir.parent / "skills" / "official-docs" / "reference"`
   - Script is CORRECT - writes to new location

5. **Old Directory Contents**
   - Contains 17 reference markdown files (stale documentation)
   - Has its own `.download_cache.json` (outdated cache)
   - All files are from before the rename

### Phase 2: Pattern Analysis

**What works:**
- Hook script executes correctly
- Python script writes to `official-docs/reference/`
- New skill loads and functions properly

**What's broken:**
- Old `claude-docs/` directory exists with stale data
- Git still tracks these old files
- Could cause confusion about which is the active skill

**Root Cause:**
Git rename operation (`git mv`) moved the SKILL.md file but did not remove the old `reference/` subdirectory and its contents. The commit message says "Renamed skill from claude-docs to official-docs" but the actual git operation was incomplete.

## The Issue

This is NOT a bug in the hook script or Python script - both are correct. This is **incomplete cleanup** from the refactoring commit. The old skill directory structure should have been removed but wasn't.

## Impact

1. **Stale Data:** Old documentation files remain in repository
2. **Confusion:** Two directories suggest two skills exist
3. **Wasted Space:** Duplicate documentation in git history
4. **Git Status:** Shows untracked or uncommitted old files

## Fix Applied

Removed the old untracked `skills/claude-docs/` directory:

```bash
rm -rf plugins/meta/claude-docs/skills/claude-docs/
```

Note: Used `rm -rf` instead of `git rm` because the directory contained untracked files created before the rename (Nov 6, 2025) that were never committed to git.

## Verification Complete

✅ **All checks passed:**

1. **Only `skills/official-docs/` exists** - Confirmed via directory listing
2. **Script runs correctly** - Test run downloaded 16 files successfully
3. **Documentation in correct location** - Files at `skills/official-docs/reference/`
4. **Git status clean** - No untracked files, working tree clean

**Evidence:**
```bash
$ ls -1 plugins/meta/claude-docs/skills/official-docs/reference/ | wc -l
16

$ ls plugins/meta/claude-docs/skills/
official-docs

$ git status plugins/meta/claude-docs/
On branch main
nothing to commit, working tree clean
```

**Timeline:**
- Nov 6, 19:28 UTC: Script ran, created untracked files in old `claude-docs/` location
- Nov 16, 04:24: Commit ba097c5 refactored code, renamed skill to `official-docs`
- Nov 17, 21:05: Removed old untracked directory, ran script successfully to new location

## Related Files

- `plugins/meta/claude-docs/skills/claude-docs/` (to be removed)
- `plugins/meta/claude-docs/skills/official-docs/` (correct location)
- `plugins/meta/claude-docs/scripts/claude_docs.py` (correct - no changes needed)
- `plugins/meta/claude-docs/hooks/hooks.json` (correct - no changes needed)

## Commit Reference

- Original rename: `ba097c5b7d451578509da6bff7888569c90cf6b3`
