## [unreleased]

### 🚀 Features

- Add pr-message-reviewer sub-agent for parallel PR reviews
- Add marketplace.json schema validation
- Integrate marketplace validation and remove hardcoded checks
- Implement strict mode support
- Add conflict detection between marketplace and plugin.json
- Add --strict CLI flag and warning display
- *(meta-claude)* Add comprehensive test suite with pytest infrastructure
- *(claude-docs)* Bump to version 1.0.0 marking production readiness
- *(scripts)* Add cleanup_bash_research utility and test infrastructure
- *(agents)* Add commit-craft-v2 agent
- *(meta-claude)* Add /skill-research command for automated research
- *(skill)* Add /skill-review-compliance command
- *(skill)* Add /skill-validate-audit command
- *(skill)* Add /skill-create command
- *(skill)* Add /skill-format command with cleanup script
- *(meta-claude)* Add /skill-review-content command
- *(meta-claude)* Implement /skill-validate-runtime command
- *(meta-claude)* Add /skill-validate-integration command
- *(meta-claude)* Implement skill-factory orchestrator skill
- *(skill-factory)* Add command output reference examples
- *(meta-claude)* Implement objective slash command validation framework
- *(meta-claude)* Complete first command audit and refine audit process
- *(meta-claude)* Complete Phase II - add executable instructions to skill-factory
- *(meta-claude)* Fix all skill-factory audit issues - achieve 100% effectiveness
- *(meta-claude)* Add visual workflow guide to skill-factory
- *(meta-claude)* Add description progressive disclosure check to skill-auditor
- *(meta-claude)* Add quoted trigger phrases to skill descriptions
- *(skill-auditor)* Add deterministic report consolidation rules
- *(skill-auditor)* Add deterministic report consolidation rules
- *(meta-claude)* Add skill-auditor-v3 with deterministic scoring
- *(meta-claude)* Add skill-auditor-v4 with surgical determinism fix
- *(meta-claude)* Add skill-auditor-v5 with convergent feedback architecture
- *(skill-auditor)* Add description extraction from SKILL.md
- *(skill-auditor)* Add quoted phrase extraction
- *(skill-auditor)* Add domain indicator extraction
- *(skill-auditor)* Add forbidden files, line count, and implementation detail checks
- *(skill-auditor)* Add Claude Agent SDK application with deterministic analysis
- *(skill-auditor)* Implement Skill Auditor SDK application with deterministic metrics extraction and analysis
- *(skill-auditor)* Add metrics structure validation
- *(meta-claude)* Add skill-auditor-v6 hybrid agent
- *(audit)* Add prevent-audit-taint rule to ensure unbiased prompt usage
- *(skill-auditor)* Enhance B4 pattern detection for implementation details (#18)
- *(audit)* Implement hybrid mode in skill auditor for improved environment handling
- *(agent-auditor)* Package audit system for standalone repository
- *(scripts)* Add intelligent markdown linter with Claude Agent SDK
- *(note-smith)* Add LangSmith tracing support
- *(notes)* Add notes for LangSmith tracing implementation
- *(marketplace)* Register hookify plugin
- *(plugin)* Add hookify meta plugin
- *(claude-dev-sandbox)* Add new plugin with official docs and sync infrastructure
- *(commands)* Enhance generate-changelog with git-cliff integration
- *(meta-claude)* Add coderabbit skill with comprehensive documentation
- *(meta-claude)* Add skill write command for AI-assisted skill authoring
- *(skill-factory)* Integrate write command into skill creation workflow
- *(meta-claude)* Add slash-command-creator skill
- *(python-tools)* Add review-uv-script command

### 🐛 Bug Fixes

- Use specific exception types for file reading
- Improve JSON error handling specificity
- Apply specific exception handling to all JSON loading
- Add error handling to schema validation
- Address remaining issues from PR #15 review
- Prevent PermissionError handler from raising during diagnostics
- Improve validation of dict-valued plugin sources
- Add path traversal protection and type safety improvements
- Return validated path instead of buggy lstrip reconstruction
- Use regex to extract hook script paths from wrapper commands
- *(meta-claude)* Correct agent frontmatter compliance and clarify plugin vs user agent distinction
- *(skill)* Clarify --category vs --categories in /skill-research
- *(skill)* Add scoring guidelines to /skill-review-content
- *(skill)* Address code review issues in /skill-validate-integration
- *(skill-factory)* Implement audit recommendations for improved discoverability
- *(skill-factory)* Add Quick Decision Guide for 8 operations
- *(skill-auditor)* Update skill documentation paths for improved clarity
- *(meta-claude)* Apply audit fixes to skill slash commands
- *(meta-claude)* Apply audit fixes to skill create command
- *(meta-claude)* Add blank line detection algorithm to audit agent
- *(meta-claude)* Add argument-hint format validation algorithm to audit agent
- *(meta-claude)* Replace manual blank line detection with rumdl execution
- *(meta-claude)* Use lowercase argument-hint format in skill create command
- *(meta-claude)* Apply audit fixes to skill slash commands
- *(meta-claude)* Fix critical bash permissions and perspective in research command
- *(meta-claude)* Achieve 100% slash command compliance across all 8 skill commands
- *(skill-factory)* Remove implementation details from description
- *(skill-factory)* Remove content duplication to comply with progressive disclosure
- *(skill-auditor)* Remove invalid directory name restrictions
- *(skill-factory)* Improve description triggers and remove file reference
- *(skill-factory)* Remove implementation details from description and strengthen triggers
- *(skill-factory)* Implement auditor recommendations for effectiveness
- *(skill-auditor)* Replace subjective trigger analysis with deterministic quoted-phrase methodology
- *(skill-auditor)* Use generic examples to avoid confirmation bias
- *(commit-craft)* Fix name
- *(skill-auditor)* Fix case-insensitive deduplication bug in metrics extractor
- *(skill-auditor)* Fix false failures in determinism test script
- *(skill-auditor)* Add error handling for file read failures
- *(skill-auditor)* Add comprehensive Claude SDK error handling
- *(skill-auditor)* Improve path validation with helpful messages
- *(skill-auditor)* Add comprehensive exception handling to audit_skill
- *(skill-auditor)* Clarify determinism test messages
- *(skill-auditor)* Address CodeRabbit review feedback
- *(skill-auditor)* Add return type annotations to test functions
- *(renovate)* Correct preset path syntax in configuration
- *(docs)* Resolve markdown linting issues across documentation
- *(claude-dev-sandbox)* Improve sync script error handling and validation
- *(skill-factory)* Correct completion options for skills
- *(claude-docs)* Improve error handling and file encoding

### 💼 Other

- Continue component checks when manifest missing or invalid
- *(rumdl)* Exclude agent-creator skill from linting for dense knowledge base
- *(audit-command)* Remove outdated slash command compliance auditor agent

### 🚜 Refactor

- Improve exception handling in validate_plugin_path
- Narrow exception handling in validate_json_schema
- Replace regex-based frontmatter validation with YAML parsing
- Centralize JSON file loading into reusable helper
- Improve type hints and context strings for JSON loader
- Improve type safety and schema documentation
- Eliminate double-counting and avoid redefining helper
- Restructure claude-docs plugin and rename skill to official-docs
- *(scripts)* Rename fetch-hooks-guide to firecrawl_scrape_url for clarity
- *(meta-claude)* Move skill agents to plugin structure
- *(meta-claude)* Clarify audit Notes section and enforce template adherence
- *(skill-auditor)* Remove redundant system_prompt and update SDK version
- *(skill-auditor)* Move validation import to module level
- *(skill-auditor)* Extract magic numbers to named constants
- *(skill-auditor)* Remove redundant bash determinism test
- *(commit-craft)* Rewrite agent with comprehensive guidelines
- *(scripts)* Add comprehensive error handling to markdown linter
- *(meta-claude)* Remove deprecated skill auditor agent versions
- *(meta-claude)* Remove deprecated skill-creator agent
- *(commands)* Remove deprecated analysis commands
- *(skill-creator)* Refactor skill creation workflow and structure
- *(scripts)* Move format_skill_research.py to skill-factory
- *(coderabbit)* Migrate skill from meta-claude to claude-dev-sandbox
- *(claude-dev-sandbox)* Remove working-with-claude-code skill

### 📚 Documentation

- Update changelog for v0.3.0 release
- Add PR #12 verification after action review
- Add pr-review example for slash command documentation
- Add PR review toolkit analysis
- Add implementation summary for verify-structure enhancements
- Add implementation plan for PR #15 critical fixes
- Enhance validate_markdown_frontmatter docstring
- Add TODO for pluginRoot support
- *(meta-claude)* Improve README clarity and update version to 0.3.0
- *(scripts)* Update README with improved tool descriptions and new script names
- Add bash best practices research and plugin review documentation
- *(research)* Add CodeRabbit CLI documentation
- *(claude-dev-sandbox)* Add CodeRabbit research materials
- *(ideas)* Add create-review-validate workflow documentation
- *(plans)* Add skill-creator-v2 workflow design
- *(plans)* Clarify delegation architecture in skill-creator-v2
- *(plans)* Clarify research script implementation for /research-skill
- *(plans)* Resolve final open questions for skill-creator-v2
- *(plans)* [**breaking**] Finalize naming conventions for skill-factory workflow
- Create slash command audit tracking system and fix command references
- *(meta-claude)* Complete slash command audit for all 8 skill commands
- *(meta-claude)* Add visual guide reference to skill-factory
- Add critical audit agent protocol to CLAUDE.md
- Document skill-auditor determinism test results
- *(skill-auditor)* Add architecture and usage documentation
- *(skill-auditor)* Improve domain indicator comment
- *(skill-auditor)* Document all modules in README
- Document deterministic vs semantic audit checks
- Comprehensive skill audit research documentation
- *(audit)* Separate implementation plan from validation results
- *(audit)* Document embedded agent architecture approach
- *(audit)* Add Claude Code review of external assessment
- *(rules)* Add Jina MCP and GitHub MCP usage rules for Cursor
- *(research)* Add rumdl markdown linter research and SDK plan
- *(mcp-builder)* Modernize skill with updated MCP guidelines
- *(skill-creator)* Improve skill structure and guidelines
- *(commit-craft)* Update manual fix thresholds for violations
- *(commit-craft)* Update lock file reference in commit guidelines
- Improve formatting in review-pr-msg command
- Update README.md with new script descriptions
- Add Mintlify documentation research
- *(python-tools)* Fix markdown formatting in SDK references
- Remove outdated local plugin testing sections from CLAUDE.md
- Add skill generation research and methodology comparison
- *(claude-dev-sandbox)* Add test results and hook documentation
- *(coderabbit)* Fix markdown formatting in research docs
- Update changelog
- *(skill-factory)* Fix documentation inaccuracies
- *(TODO)* Update skill-factory testing procedures and remove outdated references

### 🎨 Styling

- Fix formatting and markdown linting in pr-review.md
- *(changelog)* Remove excessive blank lines for consistency
- *(cliff)* Align configuration with Virgo-Core format
- *(audit)* Fix whitespace in research documentation
- *(docs)* Apply markdown linting auto-fixes
- *(meta-claude)* Fix markdown formatting in multi-agent example

### 🧪 Testing

- Final testing and cleanup for verify-structure enhancements
- Add marketplace.json unicode error test
- Add comprehensive test suite for core functionality
- *(skill-auditor)* Add determinism verification test
- *(skill-auditor)* Add tests for build_analysis_prompt logic
- *(skill-auditor)* Fix B2/B3 test coverage gaps
- *(skill-auditor)* Add edge case tests for extraction
- *(skill-auditor)* Add automated determinism integration tests

### ⚙️ Miscellaneous Tasks

- *(meta-claude)* Add .gitignore for Python artifacts and test cache
- *(meta-claude)* Remove obsolete claude-skill-auditor-v2 agent file
- *(sandbox)* Clean up build area and relocate video-processor
- Update CodeRabbit and pre-commit configuration
- *(renovate)* Use shared renovate config presets
- Remove agent-auditor directory (moved to separate repo)
- *(rumdl)* Exclude references/ directories from MD033 checks
## [0.3.0] - 2025-11-12

### 🚀 Features

- *(mise)* Add intelligent markdown linting tasks
- *(plugins)* Add python-tools plugin with SDK support
- *(agents)* Add skill-creator subagent with comprehensive testing methodology
- *(agents)* Add claude-skill-auditor subagent for comprehensive skill validation
- *(agents,commands)* Add agent-sdk-verifier and review-sdk-app command
- *(skills,scripts)* Add doc-generator skill and note_smith.py SDK demo
- *(commands)* Add load_superpowers command placeholder
- *(plugins)* Update python-tools plugin with SDK improvements and uv converter
- *(docs)* Add comprehensive validation framework with checklist-template-subagent pattern
- *(meta-claude)* Add composing-claude-code skill and release v0.2.0
- *(commands)* Add generate-changelog command
- *(claude-dev-sandbox)* Add video-processor skill
- *(scripts)* Add dual-mode support to markdown_formatter.py
- *(scripts)* Add --blocking mode and fix exit code consistency
- *(coderabbit)* Add base configuration with schema
- *(coderabbit)* Configure assertive profile with full automation
- *(coderabbit)* Configure auto-review for PRs
- *(coderabbit)* Add automated labeling strategy
- *(coderabbit)* Configure path filters for focused reviews
- *(coderabbit)* Add path instructions for Python and plugin files
- *(coderabbit)* Add path instructions for documentation files
- *(coderabbit)* Configure tool integration
- *(coderabbit)* Enable auto-reply in chat
- *(coderabbit)* Configure knowledge base with CLAUDE.md and official docs
- *(coderabbit)* Configure code generation for docstrings and tests
- Add skill creator and context isolation reference
- *(multi-agent-v2)* Add skill definition and reference documentation
- *(multi-agent-v2)* Add composition patterns
- *(multi-agent-v2)* Add decision tree workflow
- *(multi-agent-v2)* Add example case studies and progression
- *(multi-agent-v2)* Add anti-patterns documentation
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
- *(meta)* Add prime_research orchestrator command
- *(meta)* Add claude-skill-auditor-v2 with effectiveness validation
- *(meta)* Add audit-command slash command compliance auditor
- *(meta)* Add claim verification slash commands
- Add jina_reader_docs.py script for direct HTTP scraping
- Add jina_mcp_docs.py script for parallel scraping
- Add firecrawl_mcp_docs.py script for robust scraping
- *(scripts)* Add Firecrawl SDK research tool with Pydantic fix
- *(claude-dev-sandbox)* Add mcp-builder skill for MCP server development

### 🐛 Bug Fixes

- *(lint)* Use explicit glob pattern for .claude exclusion
- *(claude-docs)* Enable HTTP redirect following in httpx client
- *(meta-claude)* Correct file references and enhance skill descriptions
- Address code review issues in technical compliance
- Correct line number references in architectural checks
- Address Task 6 code review issues
- Remove executable bash patterns from audit-command documentation
- *(config)* Update rumdl.toml to use underscore syntax
- Remove emojis and add test shebang per project standards
- Update jina_mcp_docs.py to match project standards and document POC limitations
- Add API key validation and improve error handling in firecrawl_mcp_docs.py
- Parse MCP tool responses correctly to avoid duplicate content
- *(claude-docs)* Remove ANTHROPIC_API_KEY requirement and fix output directory paths

### 🚜 Refactor

- *(scripts)* Migrate intelligent markdown linting to claude-agent-sdk
- *(agents)* Update frontmatter to use comma-separated tools format
- *(scripts)* Improve SDK implementation in intelligent-markdown-lint
- *(lint)* Use .rumdl.toml for exclusions instead of pre-commit config
- *(meta-claude)* Rename composing-claude-code skill to multi-agent-composition
- *(multi-agent)* Consolidate agentic prompt documentation
- *(multi-agent)* Upgrade visual-decision-trees to comprehensive guide
- Reorganize multi-agent composition and skill creator
- *(meta-claude)* Reorganize audit report and update skill auditor
- Streamline python-uv-scripts skill documentation
- Remove duplicate skill-creator from claude-dev-sandbox
- Rename hooks.json to hooks.json.example
- *(ansible-best-practices)* Enhance SKILL.md with pattern decision guide and quick reference

### 📚 Documentation

- Add testing campaign notes and detailed analysis
- Update prompts notes and sync Claude Code docs
- Fix broken links and trailing whitespace
- Expand TODO.md with detailed action items and remove outdated notes
- *(git-cliff)* Expand configuration documentation with advanced patterns and troubleshooting
- *(reviews)* Add comprehensive skill audit system
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
- *(plans)* Add research pipeline design feedback
- *(plan)* Add CodeRabbit configuration design
- *(plan)* Add CodeRabbit configuration implementation plan
- *(plan)* Apply elements-of-style to evaluation design
- *(developer)* Add CodeRabbit configuration guide
- *(research)* Add persuasion techniques for coding agents
- Add skill auditor reviews and YouTube transcripts
- *(multi-agent)* Update SKILL.md to reflect reorganization
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
- *(claude-docs)* Add script testing results and performance analysis

### 🎨 Styling

- *(docs)* Exclude review documents from markdown linting
- Apply markdown formatting to continuous improvement reports
- Fix formatting in research and review documentation
- Add missing EOF newlines
- Fix markdown formatting in coderabbit.md

### 🧪 Testing

- Add initial continuous improvement reports
- Add comprehensive test suite for audit command
- Remove temporary test files for audit command
- Add failing tests for jina_mcp_docs.py
- Add failing tests for firecrawl_mcp_docs.py
- Verify all script variations work end-to-end

### ⚙️ Miscellaneous Tasks

- Remove obsolete scripts and backup files
- *(lint)* Exclude docs/notes/ from markdown linting
- *(tooling)* Migrate from pre-commit to prek and add link checking
- Add Cursor IDE configuration rules
- Remove backup CodeRabbit config
- Fix trailing whitespace in agentic-prompt-guide.md
- Add cursor worktrees configuration
- Remove author attribution from changelog entries
- Ignore lychee cache file
- Add .lycheecache to gitignore
- *(claude-dev-sandbox)* Remove duplicate skills and update README
## [0.2.0] - 2025-11-02

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
- *(changelog)* Add git-cliff configuration and documentation
- Add claude-dev-sandbox plugin with python-uv-scripts skill
- *(claude-docs-sync)* Create plugin structure and README
- *(claude-docs-sync)* Add JSON output format to script
- *(claude-docs-sync)* Add minimal documentation awareness skill
- *(claude-docs-sync)* Add update-docs slash command
- *(claude-docs-sync)* Add SessionStart staleness check hook
- Add claude-docs plugin with auto-sync skill
- *(skills)* Add crawl4ai web scraping skill
- *(plugins)* Add claude-dev-sandbox plugin with research docs
- *(scripts)* Add documentation extraction example
- *(plugins)* Add python-tools plugin with consolidated python-uv-scripts skill
- *(scripts)* Add bash command validator hook example
- *(meta)* Enhance verify-structure.py with comprehensive validation
- *(claude)* Add PostToolUse hooks for auto-formatting
- *(scripts)* Add Python formatter and checker scripts
- *(claude)* Add agents and hooks configuration
- *(python-tools)* Add python-code-quality skill structure
- *(python-tools)* Add python-json-parsing skill structure
- *(python-tools)* Add generic config templates for ruff and pyright
- *(python-tools)* Add pre-commit and CI/CD integration patterns
- *(agents)* Add intelligent markdown linting agent definitions
- *(orchestrator)* Add intelligent markdown linting workflow
- *(orchestrator)* Integrate Claude SDK for subagent spawning
- *(orchestrator)* Implement investigation result aggregation
- *(commands)* Add /intelligent-lint slash command
- *(commands)* Add intelligent markdown linting slash command
- *(scripts)* Add rumdl output parser for intelligent linting

### 🐛 Bug Fixes

- Correct .gitkeep placement in plugin template
- *(netbox)* Remove invalid [tool.uv.metadata] from API client scripts
- *(hooks)* Update python_formatter.py path to new location
- *(config)* Exclude .claude/ from rumdl and use official slash command format
- *(ansible)* Resolve markdown linting in cluster-automation
- *(ansible)* Resolve markdown linting in testing-comprehensive
- *(ansible)* Resolve markdown linting in variable-management-patterns
- *(netbox)* Shorten frontmatter description and wrap long line
- *(orchestrator)* Add --dry-run support and subprocess error handling
- *(orchestrator)* Improve error handling in subagent spawning
- *(tests)* Import aggregation function instead of duplicating it
- *(plugins)* Resolve markdown linting in plugins and templates
- *(docs)* Resolve markdown linting in docs and examples

### 💼 Other

- *(ruff)* Add ruff configuration and tooling setup
- *(rumdl)* Increase line length limit to 120 characters

### 🚜 Refactor

- *(claude-docs-sync)* Add type-safe format enum and fix output handling
- Remove .claude/skills/python-uv-scripts (moved to plugin)
- Remove python-uv-tools plugin (renamed to python-tools)
- Clean up claude-dev-sandbox migrated content
- *(scripts)* Improve markdown_formatter.py error handling
- *(plugins)* Rename python-uv-tools to python-tools
- *(python-tools)* Migrate ruff/pyright docs to python-code-quality skill
- *(python-tools)* Migrate formatting tools to python-code-quality skill
- *(python-tools)* Migrate JSON research to python-json-parsing skill
- Improve code quality across Python scripts

### 📚 Documentation

- Add meta-claude README
- Update README with marketplace documentation
- Add mcp-builder example skill
- Add documentation maintenance agent design
- Add project instructions and reorganize documentation
- Add claude-docs-sync plugin design document
- Update skill section to minimal approach
- *(ai_docs)* Add web scraping tool research docs
- *(ideas)* Add hook-based approach to extend DeepWiki MCP
- *(CLAUDE.md)* Simplify project documentation
- Update planning and idea documents
- *(python-uv-scripts)* Simplify skill description
- *(ai_docs)* Add comprehensive ruff documentation
- *(python-tools)* Update README for expanded toolkit
- Update README and architecture with implementation status
- *(ideas)* Add AI-powered markdown linting design notes
- Wrap long lines in remaining documentation files
- *(plans)* Add intelligent markdown linting agent MVP plan

### 🎨 Styling

- Apply markdown linting fixes across all documentation

### 🧪 Testing

- Add end-to-end test for intelligent linting

### ⚙️ Miscellaneous Tasks

- Add .worktrees/ to .gitignore
- Add documentation references and examples
- *(dev)* Add devcontainer config
- *(devcontainer)* Delete start over
- Remove empty .gitkeep files from plugins directories
- Add development tools and documentation
- *(ai_docs)* Remove outdated Claude Code reference docs
- *(claude-docs)* Stop tracking .download_cache.json
- *(meta)* Remove obsolete skill-creator SKILL.md
- Release v0.2.0
