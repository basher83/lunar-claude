# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-11-12

### 🔒 Security

- Streamline python-uv-scripts skill documentation


### 🚀 Features

- **mise**: Add intelligent markdown linting tasks

- **plugins**: Add python-tools plugin with SDK support

- **agents**: Add skill-creator subagent with comprehensive testing methodology

- **agents**: Add claude-skill-auditor subagent for comprehensive skill validation

- **agents,commands**: Add agent-sdk-verifier and review-sdk-app command

- **skills,scripts**: Add doc-generator skill and note_smith.py SDK demo

- **commands**: Add load_superpowers command placeholder

- **plugins**: Update python-tools plugin with SDK improvements and uv converter

- **docs**: Add comprehensive validation framework with checklist-template-subagent pattern

- **meta-claude**: Add composing-claude-code skill and release v0.2.0

- **commands**: Add generate-changelog command

- **claude-dev-sandbox**: Add video-processor skill

- **scripts**: Add dual-mode support to markdown_formatter.py

- **scripts**: Add --blocking mode and fix exit code consistency

- **coderabbit**: Add base configuration with schema

- **coderabbit**: Configure assertive profile with full automation

- **coderabbit**: Configure auto-review for PRs

- **coderabbit**: Add automated labeling strategy

- **coderabbit**: Configure path filters for focused reviews

- **coderabbit**: Add path instructions for Python and plugin files

- **coderabbit**: Add path instructions for documentation files

- **coderabbit**: Configure tool integration

- **coderabbit**: Enable auto-reply in chat

- **coderabbit**: Configure knowledge base with CLAUDE.md and official docs

- **coderabbit**: Configure code generation for docstrings and tests

- Add skill creator and context isolation reference

- **multi-agent-v2**: Add skill definition and reference documentation

- **multi-agent-v2**: Add composition patterns

- **multi-agent-v2**: Add decision tree workflow

- **multi-agent-v2**: Add example case studies and progression

- **multi-agent-v2**: Add anti-patterns documentation

- Add /improve slash command for continuous improvement analysis

- Add Claude Code component conversion workflows

- Add mem-search skill to claude-dev-sandbox

- Add mem-search skill to claude-dev-sandbox

- Add audit-command slash command structure

- Implement technical compliance validation

- Implement quality practices validation

- Implement architectural standards validation

- Implement report generation and formatting

- Enhance error handling for edge cases

- Finalize slash command audit system (Task 8)

- **meta**: Add prime_research orchestrator command

- **meta**: Add claude-skill-auditor-v2 with effectiveness validation

- **meta**: Add audit-command slash command compliance auditor

- **meta**: Add claim verification slash commands

- Add jina_reader_docs.py script for direct HTTP scraping

- Add jina_mcp_docs.py script for parallel scraping

- Add firecrawl_mcp_docs.py script for robust scraping

- **scripts**: Add Firecrawl SDK research tool with Pydantic fix

- **claude-dev-sandbox**: Add mcp-builder skill for MCP server development


### 🐛 Bug Fixes

- **lint**: Use explicit glob pattern for .claude exclusion

- **claude-docs**: Enable HTTP redirect following in httpx client

- **meta-claude**: Correct file references and enhance skill descriptions

- Address code review issues in technical compliance

- Correct line number references in architectural checks

- Address Task 6 code review issues

- Remove executable bash patterns from audit-command documentation

- **config**: Update rumdl.toml to use underscore syntax

- Remove emojis and add test shebang per project standards

- Update jina_mcp_docs.py to match project standards and document POC limitations

- Add API key validation and improve error handling in firecrawl_mcp_docs.py

- Parse MCP tool responses correctly to avoid duplicate content

- **claude-docs**: Remove ANTHROPIC_API_KEY requirement and fix output directory paths


### 📚 Documentation

- Add testing campaign notes and detailed analysis

- Update prompts notes and sync Claude Code docs

- Fix broken links and trailing whitespace

- Expand TODO.md with detailed action items and remove outdated notes

- **git-cliff**: Expand configuration documentation with advanced patterns and troubleshooting

- **reviews**: Add comprehensive skill audit system

- Add metacognitive development framework and parahuman cognition research

- Add claude-mem usage guide and token efficiency analysis

- Add research notes, Safety config, new idea, and exclude research from linting

- Add research pipeline meta-learning system design

- Add emergence analysis from research pipeline design session

- Add metacognitive exploration transcript

- Add plugin-auditor agent design

- Update CLAUDE.md and add prime-mind notes

- Add prime-mind-v2 command with improved actionability

- Add claude-docs-upgrade challenge planning documents

- Add plan comparison and prime-mind prompt analysis

- Add web scraping research and planning documentation

- **plans**: Add research pipeline design feedback

- **plan**: Add CodeRabbit configuration design

- **plan**: Add CodeRabbit configuration implementation plan

- **plan**: Apply elements-of-style to evaluation design

- **developer**: Add CodeRabbit configuration guide

- **research**: Add persuasion techniques for coding agents

- Add skill auditor reviews and YouTube transcripts

- **multi-agent**: Update SKILL.md to reflect reorganization

- Add documentation for /improve slash command

- Add workflow analysis for /improve command implementation

- Add slash command audit system design

- Add slash command audit implementation plan

- Enhance continuous improvement rules

- Add agentic workflow conversion task

- Add table of contents to skill-creator skill

- Add Task 6 implementation report

- Add comprehensive issue #73 investigation notes

- Improve convert-to-slash command formatting and permissions

- Add Core 4 framework analysis for lunar-claude

- Add skill auditor effectiveness improvement proposals

- Add beyond-mcp architecture research analysis

- Document AI metacognition and failure mode patterns

- Add claude-docs-upgrade PR comparison and review analysis

- Add prompt engineering verification failure modes case study

- Add script comparison guide for claude_docs variations

- Update README with script variations section

- **claude-docs**: Add script testing results and performance analysis


### ♻️ Refactor

- **scripts**: Migrate intelligent markdown linting to claude-agent-sdk

- **agents**: Update frontmatter to use comma-separated tools format

- **scripts**: Improve SDK implementation in intelligent-markdown-lint

- **lint**: Use .rumdl.toml for exclusions instead of pre-commit config

- **meta-claude**: Rename composing-claude-code skill to multi-agent-composition

- **multi-agent**: Consolidate agentic prompt documentation

- **multi-agent**: Upgrade visual-decision-trees to comprehensive guide

- Reorganize multi-agent composition and skill creator

- **meta-claude**: Reorganize audit report and update skill auditor

- Remove duplicate skill-creator from claude-dev-sandbox

- Rename hooks.json to hooks.json.example

- **ansible-best-practices**: Enhance SKILL.md with pattern decision guide and quick reference


### 🧪 Testing

- Add initial continuous improvement reports

- Add comprehensive test suite for audit command

- Remove temporary test files for audit command

- Add failing tests for jina_mcp_docs.py

- Add failing tests for firecrawl_mcp_docs.py

- Verify all script variations work end-to-end


### 🔧 Miscellaneous

- Remove obsolete scripts and backup files

- **lint**: Exclude docs/notes/ from markdown linting

- **deps**: Update dependency uv to v0.9.7

- **tooling**: Migrate from pre-commit to prek and add link checking

- **docs**: Exclude review documents from markdown linting

- Add Cursor IDE configuration rules

- Remove backup CodeRabbit config

- Fix trailing whitespace in agentic-prompt-guide.md

- Add cursor worktrees configuration

- Remove author attribution from changelog entries

- Apply markdown formatting to continuous improvement reports

- Ignore lychee cache file

- Add .lycheecache to gitignore

- Fix formatting in research and review documentation

- Add missing EOF newlines

- Fix markdown formatting in coderabbit.md

- **claude-dev-sandbox**: Remove duplicate skills and update README

## [0.2.0] - 2025-11-02

### 🔒 Security

- **changelog**: Add git-cliff configuration and documentation


### 🚀 Features

- Create marketplace category and template directories

- Create clean marketplace manifest

- Create plugin template directory structure

- Add template plugin manifest

- Add template README with standard sections

- Add example agent template

- Add example skill template

- Add example hooks configuration

- Create meta-claude plugin structure

- Add skill-creator skill

- Add agent-creator skill

- Add hook-creator skill

- Add command-creator skill

- Add new-plugin command

- Add meta-claude to marketplace

- Add structure verification script

- Add python-uv-tools plugin to devops category

- Add three homelab infrastructure plugins

- Add claude-dev-sandbox plugin with python-uv-scripts skill

- **claude-docs-sync**: Create plugin structure and README

- **claude-docs-sync**: Add JSON output format to script

- **claude-docs-sync**: Add minimal documentation awareness skill

- **claude-docs-sync**: Add update-docs slash command

- **claude-docs-sync**: Add SessionStart staleness check hook

- Add claude-docs plugin with auto-sync skill

- **skills**: Add crawl4ai web scraping skill

- **plugins**: Add claude-dev-sandbox plugin with research docs

- **scripts**: Add documentation extraction example

- **plugins**: Add python-tools plugin with consolidated python-uv-scripts skill

- **scripts**: Add bash command validator hook example

- **meta**: Enhance verify-structure.py with comprehensive validation

- **claude**: Add PostToolUse hooks for auto-formatting

- **scripts**: Add Python formatter and checker scripts

- **claude**: Add agents and hooks configuration

- **python-tools**: Add python-code-quality skill structure

- **python-tools**: Add python-json-parsing skill structure

- **python-tools**: Add generic config templates for ruff and pyright

- **python-tools**: Add pre-commit and CI/CD integration patterns

- **agents**: Add intelligent markdown linting agent definitions

- **orchestrator**: Add intelligent markdown linting workflow

- **orchestrator**: Integrate Claude SDK for subagent spawning

- **orchestrator**: Implement investigation result aggregation

- **commands**: Add /intelligent-lint slash command

- **commands**: Add intelligent markdown linting slash command

- **scripts**: Add rumdl output parser for intelligent linting


### 🐛 Bug Fixes

- Correct .gitkeep placement in plugin template

- **netbox**: Remove invalid [tool.uv.metadata] from API client scripts

- **hooks**: Update python_formatter.py path to new location

- **config**: Exclude .claude/ from rumdl and use official slash command format

- **ansible**: Resolve markdown linting in cluster-automation

- **ansible**: Resolve markdown linting in testing-comprehensive

- **ansible**: Resolve markdown linting in variable-management-patterns

- **netbox**: Shorten frontmatter description and wrap long line

- **orchestrator**: Add --dry-run support and subprocess error handling

- **orchestrator**: Improve error handling in subagent spawning

- **tests**: Import aggregation function instead of duplicating it

- **plugins**: Resolve markdown linting in plugins and templates

- **docs**: Resolve markdown linting in docs and examples


### 📚 Documentation

- Add meta-claude README

- Update README with marketplace documentation

- Add mcp-builder example skill

- Add documentation maintenance agent design

- Add project instructions and reorganize documentation

- Add claude-docs-sync plugin design document

- Update skill section to minimal approach

- **ai_docs**: Add web scraping tool research docs

- **ideas**: Add hook-based approach to extend DeepWiki MCP

- **CLAUDE.md**: Simplify project documentation

- Update planning and idea documents

- **python-uv-scripts**: Simplify skill description

- **ai_docs**: Add comprehensive ruff documentation

- **python-tools**: Update README for expanded toolkit

- Update README and architecture with implementation status

- **ideas**: Add AI-powered markdown linting design notes

- Wrap long lines in remaining documentation files

- **plans**: Add intelligent markdown linting agent MVP plan


### ♻️ Refactor

- **claude-docs-sync**: Add type-safe format enum and fix output handling

- Remove .claude/skills/python-uv-scripts (moved to plugin)

- Remove python-uv-tools plugin (renamed to python-tools)

- Clean up claude-dev-sandbox migrated content

- **scripts**: Improve markdown_formatter.py error handling

- **plugins**: Rename python-uv-tools to python-tools

- **python-tools**: Migrate ruff/pyright docs to python-code-quality skill

- **python-tools**: Migrate formatting tools to python-code-quality skill

- **python-tools**: Migrate JSON research to python-json-parsing skill

- Improve code quality across Python scripts


### 🧪 Testing

- Add end-to-end test for intelligent linting


### 👷 CI/CD

- **ruff**: Add ruff configuration and tooling setup


### 🔧 Miscellaneous

- Add .worktrees/ to .gitignore

- Add documentation references and examples

- **dev**: Add devcontainer config

- **deps**: Update dependency uv to v0.9.5

- **devcontainer**: Delete start over

- Remove empty .gitkeep files from plugins directories

- Apply markdown linting fixes across all documentation

- Add development tools and documentation

- **ai_docs**: Remove outdated Claude Code reference docs

- **claude-docs**: Stop tracking .download_cache.json

- **meta**: Remove obsolete skill-creator SKILL.md

- Release v0.2.0


### Config

- **rumdl**: Increase line length limit to 120 characters


### New Contributors

- @basher83 made their first contribution
- @ made their first contribution
<!-- generated by git-cliff -->
