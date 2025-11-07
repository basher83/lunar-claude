# CodeRabbit Configuration Design

**Date:** 2025-11-07
**Status:** Validated
**Goal:** Create comprehensive CodeRabbit configuration for lunar-claude plugin marketplace

## Overview

This design establishes a CodeRabbit configuration that provides comprehensive coverage across security, standards enforcement, and code quality. The configuration uses an assertive review profile with full automation for labels, reviewers, and code generation.

## Configuration Strategy

### Profile and Automation
- **Review Profile:** Assertive (comprehensive feedback including style and optimization)
- **Auto-review:** Enabled for all PRs except drafts and WIPs
- **Auto-incremental reviews:** Enabled (reviews new commits in existing PRs)
- **Label automation:** Fully automated (auto-apply)
- **Reviewer assignment:** Fully automated (auto-assign)
- **Tone:** Instructional, focused on plugin architecture, security, documentation quality, and code standards

### Knowledge Base Configuration
- **Data retention:** Enabled (opt_out: false)
- **Code guidelines:** Enabled, detecting:
  - `**/CLAUDE.md` - Project-specific guidelines
  - `plugins/meta/claude-docs/skills/claude-docs/reference/**/*.md` - Official Claude Code documentation
- **Learnings:** Scope set to "auto" (adaptive learning from team preferences)
- **Web search:** Enabled (for framework/library context)
- **Issue tracking:** Auto integration with GitHub issues

### Finishing Touches
- **Docstring generation:** Enabled with path-specific instructions
- **Unit test generation:** Enabled with path-specific instructions
- Both features provide proactive code generation as "finishing touches" commits

## Path Filters and Exclusions

### Excluded Paths
- Virtual environments and caches: `.venv/`, `__pycache__/`, `.ruff_cache/`, `.rumdl-cache/`, `.pytest_cache/`, `.mypy_cache/`
- Build artifacts: `dist/`, `build/`, `.eggs/`, `node_modules/`
- Working documents: `docs/plans/`, `docs/research/`, `docs/reviews/`, `docs/notes/`
- Examples and templates: `plugins/**/examples/`, `plugins/**/assets/templates/`
- Test fixtures: `tests/fixtures/`, `**/test/fixtures/`

### Included Paths (Explicit Focus)
- `scripts/` - Python automation scripts
- `plugins/` - Plugin source code (excluding examples/templates)
- `docs/` - Published documentation (excluding working docs)
- `.claude/` - Claude Code configuration
- `.claude-plugin/` - Marketplace registry and schemas
- Root configuration files

## Automated Labeling Strategy

Type-focused labels automatically applied based on change characteristics:

- **security** - Critical security issues (auth, injection, credentials, data exposure)
- **documentation** - Markdown docs, README files, inline documentation
- **automation** - Python scripts, mise tasks, CI/CD workflows
- **bugfix** - Bug fixes resolving existing issues
- **feature** - New functionality or enhancements
- **breaking-change** - Backward compatibility breaks
- **dependencies** - Package updates, tool version changes
- **testing** - Test files, test infrastructure, testing docs

Multiple labels can be applied when appropriate.

## Path-Specific Review Instructions

### Python Automation Scripts (`scripts/**/*.py`)
- Ruff compliance with existing ruff.toml
- Type hints for all function signatures
- Google-style docstrings (Args, Returns, Raises)
- Proper error handling with specific exceptions
- Security: input validation, avoid shell injection, safe credential handling
- Logging for debugging and monitoring
- Command-line argument validation

### Plugin Manifests (`plugins/**/.claude-plugin/*.json`)
- Required fields: name, version, description, author, keywords
- Semantic versioning format (X.Y.Z)
- JSON schema compliance
- Accurate dependency specifications
- Consistency with marketplace registry

### Marketplace Registry (`.claude-plugin/marketplace.json`)
- All listed plugins have corresponding directories
- Plugin metadata matches individual plugin.json files
- Version numbers consistent across registry and plugin files
- No duplicate plugin names or paths
- Valid JSON structure

### Shell Scripts (`**/*.sh`)
- Shellcheck compliance
- Error handling: set -e, set -u, set -o pipefail
- Input validation and sanitization
- No hardcoded credentials or sensitive data
- Clear comments for complex operations

### Skills Documentation (`plugins/**/skills/**/*.md`)
- Clear skill metadata (name, description)
- Unambiguous usage instructions
- Concrete, executable examples
- Follows skill documentation standards
- No sensitive information in examples
- Proper markdown formatting

### Slash Commands (`plugins/**/commands/**/*.md`)
- Clear command purpose and use cases
- Accurate argument specifications
- Usage examples with expected output
- Integration notes with other commands if relevant

### Agent Definitions (`plugins/**/agents/**/*.md`)
- Clear agent purpose and capabilities
- Tool access properly specified
- Behavioral instructions are unambiguous
- No conflicting instructions
- Model specifications follow inheritance pattern (default to inherit from parent)

### Published Documentation (`docs/**/*.md`)
- Clear, concise technical writing
- Accurate code examples and commands
- Proper markdown formatting per .rumdl.toml
- Valid internal links
- Up-to-date examples matching current codebase
- No outdated information

### Configuration Files (`*.toml`, `*.yaml`, `*.json` in root)
- Valid syntax for file type
- Schema compliance where applicable
- Comments explain non-obvious settings
- Consistent with project conventions

## Tool Integration

### Enabled Tools
- **Python:** ruff (uses ruff.toml), pylint
- **Shell:** shellcheck
- **Markdown:** markdownlint (uses .rumdl.toml patterns)
- **YAML:** yamllint
- **JSON:** Built-in JSON validation
- **Security:** checkov (infrastructure as code security)
- **GitHub:** github-checks (90s timeout for CI/CD integration)

### Tool Behavior
- Tools respect existing config files (ruff.toml, .rumdl.toml, pyrightconfig.json)
- CodeRabbit also applies its own defaults for additional coverage
- All tools run automatically based on detected file types
- Tool results appear as inline comments with suggested fixes

### Disabled Tools
- gitleaks (explicitly disabled)
- Language-specific tools for unused languages (Go, Rust, Swift, etc.)
- AST-grep (no custom rules defined yet)
- Advanced security scanners not yet needed

## Code Generation Configuration

### Docstring Generation
- **Language:** en-US
- **Path-specific instructions:**
  - `scripts/**/*.py`: Google-style docstrings with Args, Returns, Raises sections. Type hints in signatures (not docstrings). Include usage examples for complex functions. Focus on behavior and edge cases.
  - `plugins/**/tools/**/*.py`: Brief docstrings focusing on tool purpose and parameters. Include examples for non-obvious usage.

### Unit Test Generation
- **Path-specific instructions:**
  - `scripts/**/*.py`: Generate tests covering happy paths, error handling, edge cases, and boundary conditions. Use pytest framework. Focus on validating behavior, not implementation details. Mock external dependencies (file I/O, network, subprocess). Tests must be independent.

## Implementation Notes

The configuration will be implemented in `.coderabbit.yaml` at the repository root. The YAML file will include the schema reference for editor validation and autocomplete:

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
```

All settings will be explicitly specified to ensure predictable behavior and avoid relying on CodeRabbit's default inheritance patterns.

## Success Criteria

The configuration succeeds if it:
1. Catches critical security and architecture issues before human review
2. Enforces plugin structure and documentation standards consistently
3. Reduces routine review burden through automated linting and formatting feedback
4. Applies appropriate labels and assigns reviewers automatically
5. Generates useful docstrings and test suggestions as finishing touches
6. Maintains consistency with existing development tools and workflows
