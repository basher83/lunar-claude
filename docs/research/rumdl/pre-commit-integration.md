# Pre-commit Integration

## The Problem: Include Patterns Don't Filter Explicit Files

When using rumdl with pre-commit hooks, the `include` patterns in `.rumdl.toml` **do not filter files** as expected.

### Why This Happens

The rumdl file selection logic (from `global-settings.md`):

1. **Start with candidate files** - If paths are provided via CLI, use those files
2. Apply .gitignore filtering
3. Apply include patterns
4. Apply exclude patterns

The key insight: pre-commit passes **explicit file paths** to rumdl, not a directory to scan. When rumdl receives explicit files like `rumdl check docs/notes/foo.md`, it processes those files directly without applying include/exclude filtering.

This is documented in `global-settings.md`:
> "This setting only affects directory scanning, not explicitly provided file paths"

### Symptoms

- `rumdl check .` works correctly (respects include patterns)
- `prek run rumdl --all-files` ignores include patterns and lints everything
- Files that should be excluded show violations in pre-commit

### Solution: Filter at Pre-commit Level

Add a `files:` regex pattern to the rumdl hook in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/rvben/rumdl-pre-commit
  rev: v0.0.166
  hooks:
    - id: rumdl
      # Only lint user-facing documentation (mirrors .rumdl.toml include patterns)
      files: ^(README\.md|plugins/[^/]+/README\.md|docs/(architecture|checklists)/[^/]+\.md)$
```

This filters files **before** they're passed to rumdl, achieving the same effect as include patterns.

### Best Practice

Keep both configurations in sync:

| Location | Purpose |
|----------|---------|
| `.rumdl.toml` `include` | CLI usage (`rumdl check .`) |
| `.pre-commit-config.yaml` `files` | Pre-commit hooks |

The patterns should match the same files, just expressed in different syntax (glob vs regex).

### Pattern Translation Examples

| rumdl glob (TOML) | pre-commit regex (YAML) |
|-------------------|-------------------------|
| `./README.md` | `^README\.md$` |
| `plugins/*/README.md` | `plugins/[^/]+/README\.md` |
| `plugins/*/*/README.md` | `plugins/[^/]+/[^/]+/README\.md` |
| `docs/architecture/*.md` | `docs/architecture/[^/]+\.md` |
| `**/*.md` | `.*\.md$` |
