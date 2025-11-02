# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-02

### 🔒 Security

- **changelog**: Add git-cliff configuration and documentation by @basher83


### 🚀 Features

- Create marketplace category and template directories by @basher83

- Create clean marketplace manifest by @basher83

- Create plugin template directory structure by @basher83

- Add template plugin manifest by @basher83

- Add template README with standard sections by @basher83

- Add example agent template by @basher83

- Add example skill template by @basher83

- Add example hooks configuration by @basher83

- Create meta-claude plugin structure by @basher83

- Add skill-creator skill by @basher83

- Add agent-creator skill by @basher83

- Add hook-creator skill by @basher83

- Add command-creator skill by @basher83

- Add new-plugin command by @basher83

- Add meta-claude to marketplace by @basher83

- Add structure verification script by @basher83

- Add python-uv-tools plugin to devops category by @basher83

- Add three homelab infrastructure plugins by @basher83

- Add claude-dev-sandbox plugin with python-uv-scripts skill by @basher83

- **claude-docs-sync**: Create plugin structure and README by @basher83

- **claude-docs-sync**: Add JSON output format to script by @basher83

- **claude-docs-sync**: Add minimal documentation awareness skill by @basher83

- **claude-docs-sync**: Add update-docs slash command by @basher83

- **claude-docs-sync**: Add SessionStart staleness check hook by @basher83

- Add claude-docs plugin with auto-sync skill by @basher83

- **skills**: Add crawl4ai web scraping skill by @basher83

- **plugins**: Add claude-dev-sandbox plugin with research docs by @basher83

- **scripts**: Add documentation extraction example by @basher83

- **plugins**: Add python-tools plugin with consolidated python-uv-scripts skill by @basher83

- **scripts**: Add bash command validator hook example by @basher83

- **meta**: Enhance verify-structure.py with comprehensive validation by @basher83

- **claude**: Add PostToolUse hooks for auto-formatting by @basher83

- **scripts**: Add Python formatter and checker scripts by @basher83

- **claude**: Add agents and hooks configuration by @basher83

- **python-tools**: Add python-code-quality skill structure by @basher83

- **python-tools**: Add python-json-parsing skill structure by @basher83

- **python-tools**: Add generic config templates for ruff and pyright by @basher83

- **python-tools**: Add pre-commit and CI/CD integration patterns

- **agents**: Add intelligent markdown linting agent definitions by @basher83

- **orchestrator**: Add intelligent markdown linting workflow by @basher83

- **orchestrator**: Integrate Claude SDK for subagent spawning by @basher83

- **orchestrator**: Implement investigation result aggregation by @basher83

- **commands**: Add /intelligent-lint slash command by @basher83

- **commands**: Add intelligent markdown linting slash command by @basher83

- **scripts**: Add rumdl output parser for intelligent linting by @basher83


### 🐛 Bug Fixes

- Correct .gitkeep placement in plugin template by @basher83

- **netbox**: Remove invalid [tool.uv.metadata] from API client scripts by @basher83

- **hooks**: Update python_formatter.py path to new location by @basher83

- **config**: Exclude .claude/ from rumdl and use official slash command format by @basher83

- **ansible**: Resolve markdown linting in cluster-automation by @basher83

- **ansible**: Resolve markdown linting in testing-comprehensive by @basher83

- **ansible**: Resolve markdown linting in variable-management-patterns by @basher83

- **netbox**: Shorten frontmatter description and wrap long line by @basher83

- **orchestrator**: Add --dry-run support and subprocess error handling by @basher83

- **orchestrator**: Improve error handling in subagent spawning by @basher83

- **tests**: Import aggregation function instead of duplicating it by @basher83

- **plugins**: Resolve markdown linting in plugins and templates by @basher83

- **docs**: Resolve markdown linting in docs and examples by @basher83


### 📚 Documentation

- Add meta-claude README by @basher83

- Update README with marketplace documentation by @basher83

- Add mcp-builder example skill by @basher83

- Add documentation maintenance agent design by @basher83

- Add project instructions and reorganize documentation by @basher83

- Add claude-docs-sync plugin design document by @basher83

- Update skill section to minimal approach by @basher83

- **ai_docs**: Add web scraping tool research docs by @basher83

- **ideas**: Add hook-based approach to extend DeepWiki MCP by @basher83

- **CLAUDE.md**: Simplify project documentation by @basher83

- Update planning and idea documents by @basher83

- **python-uv-scripts**: Simplify skill description by @basher83

- **ai_docs**: Add comprehensive ruff documentation by @basher83

- **python-tools**: Update README for expanded toolkit by @basher83

- Update README and architecture with implementation status by @basher83

- **ideas**: Add AI-powered markdown linting design notes by @basher83

- Wrap long lines in remaining documentation files by @basher83

- **plans**: Add intelligent markdown linting agent MVP plan by @basher83


### ♻️ Refactor

- **claude-docs-sync**: Add type-safe format enum and fix output handling by @basher83

- Remove .claude/skills/python-uv-scripts (moved to plugin) by @basher83

- Remove python-uv-tools plugin (renamed to python-tools) by @basher83

- Clean up claude-dev-sandbox migrated content by @basher83

- **scripts**: Improve markdown_formatter.py error handling by @basher83

- **plugins**: Rename python-uv-tools to python-tools by @basher83

- **python-tools**: Migrate ruff/pyright docs to python-code-quality skill by @basher83

- **python-tools**: Migrate formatting tools to python-code-quality skill by @basher83

- **python-tools**: Migrate JSON research to python-json-parsing skill by @basher83

- Improve code quality across Python scripts by @basher83


### 🧪 Testing

- Add end-to-end test for intelligent linting by @basher83


### 👷 CI/CD

- **ruff**: Add ruff configuration and tooling setup by @basher83


### 🔧 Miscellaneous

- Add .worktrees/ to .gitignore by @basher83

- Add documentation references and examples by @basher83

- **dev**: Add devcontainer config by @basher83

- **deps**: Update dependency uv to v0.9.5 by @renovate[bot]

- **devcontainer**: Delete start over by @basher83

- Remove empty .gitkeep files from plugins directories by @basher83

- Apply markdown linting fixes across all documentation by @basher83

- Add development tools and documentation by @basher83

- **ai_docs**: Remove outdated Claude Code reference docs by @basher83

- **claude-docs**: Stop tracking .download_cache.json by @basher83

- **meta**: Remove obsolete skill-creator SKILL.md by @basher83


### Config

- **rumdl**: Increase line length limit to 120 characters by @basher83


### New Contributors

- @basher83 made their first contribution
- @ made their first contribution
- @renovate[bot] made their first contribution
<!-- generated by git-cliff -->
