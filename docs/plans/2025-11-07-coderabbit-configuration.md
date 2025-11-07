# CodeRabbit Configuration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create comprehensive CodeRabbit configuration file (.coderabbit.yaml) with assertive profile, full automation, and path-specific review instructions.

**Architecture:** Single YAML configuration file in repository root that defines CodeRabbit's review behavior, tool integration, knowledge base settings, and code generation preferences. Configuration follows CodeRabbit schema v2 and integrates with existing tooling (ruff, shellcheck, markdownlint).

**Tech Stack:** YAML, CodeRabbit schema v2, Python (for validation)

---

## Task 1: Create Base Configuration Structure

**Files:**
- Create: `.coderabbit.yaml`

**Step 1: Create file with schema reference and global settings**

Create `.coderabbit.yaml` with:

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: "Provide comprehensive feedback on plugin architecture, security, documentation quality, and code standards. Include actionable suggestions with examples."
early_access: false
```

**Step 2: Verify schema reference works**

Open `.coderabbit.yaml` in VS Code and verify:
- No YAML syntax errors
- Schema validation is active (hover over keys shows descriptions)

Expected: Editor shows autocomplete and validation

**Step 3: Commit base structure**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): add base configuration with schema"
```

---

## Task 2: Configure Review Profile and Automation

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add reviews section with assertive profile**

Add to `.coderabbit.yaml` after `early_access`:

```yaml

reviews:
  profile: assertive
  request_changes_workflow: false
  high_level_summary: true
  high_level_summary_placeholder: "@coderabbitai summary"
  high_level_summary_in_walkthrough: true
  auto_title_placeholder: "@coderabbitai"
  auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"

  collapse_walkthrough: false
  changed_files_summary: true
  sequence_diagrams: false
  review_effort: true
  assess_linked_issues: true
  related_issues: true
  related_prs: true
  poem: false
```

**Step 2: Add automation settings**

Add after `poem: false`:

```yaml

  suggested_labels: true
  auto_apply_labels: true
  suggested_reviewers: true
  auto_assign_reviewers: true

  commit_status: true
  fail_commit_status: false
  review_status: true

  abort_on_close: true
  disable_cache: false
```

**Step 3: Validate YAML syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 4: Commit review configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure assertive profile with full automation"
```

---

## Task 3: Configure Auto-Review Settings

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add auto_review section**

Add after `disable_cache: false`:

```yaml

  auto_review:
    enabled: true
    auto_incremental_review: true
    drafts: false
    ignore_title_keywords:
      - "WIP"
      - "DO NOT MERGE"
      - "DRAFT"
    labels: []
    base_branches: []
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit auto-review settings**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure auto-review for PRs"
```

---

## Task 4: Configure Automated Labeling

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add labeling_instructions**

Add after `auto_assign_reviewers: true`:

```yaml

  labeling_instructions:
    - label: "security"
      instructions: "Critical security issues including authentication, authorization, injection vulnerabilities, credential management, or data exposure"
    - label: "documentation"
      instructions: "Changes to markdown documentation, README files, or inline code documentation"
    - label: "automation"
      instructions: "Changes to Python scripts in scripts/ directory, mise tasks, or CI/CD workflows"
    - label: "bugfix"
      instructions: "Bug fixes that resolve existing issues or correct incorrect behavior"
    - label: "feature"
      instructions: "New functionality or enhancements to existing features"
    - label: "breaking-change"
      instructions: "Changes that break backward compatibility or require users to update their usage"
    - label: "dependencies"
      instructions: "Updates to Python packages, tool versions, or external dependencies"
    - label: "testing"
      instructions: "Changes to test files, test infrastructure, or testing documentation"
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit labeling configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): add automated labeling strategy"
```

---

## Task 5: Configure Path Filters

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add path_filters section**

Add after `base_branches: []`:

```yaml

  path_filters:
    # Exclude virtual environments and caches
    - "!**/.venv/**"
    - "!**/venv/**"
    - "!**/__pycache__/**"
    - "!**/.ruff_cache/**"
    - "!**/.rumdl-cache/**"
    - "!**/.pytest_cache/**"
    - "!**/.mypy_cache/**"

    # Exclude build artifacts
    - "!**/dist/**"
    - "!**/build/**"
    - "!**/.eggs/**"
    - "!**/node_modules/**"

    # Exclude working documents
    - "!docs/plans/**"
    - "!docs/research/**"
    - "!docs/reviews/**"
    - "!docs/notes/**"

    # Exclude examples and templates
    - "!plugins/**/examples/**"
    - "!plugins/**/assets/templates/**"

    # Exclude test fixtures
    - "!tests/fixtures/**"
    - "!**/test/fixtures/**"

    # Include primary directories
    - "scripts/**"
    - "plugins/**"
    - "docs/**"
    - ".claude/**"
    - ".claude-plugin/**"
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit path filters**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure path filters for focused reviews"
```

---

## Task 6: Configure Path-Specific Instructions (Part 1)

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add path_instructions for Python and plugin files**

Add after `path_filters` section:

```yaml

  path_instructions:
    - path: "scripts/**/*.py"
      instructions: |
        Review Python automation scripts for:
        - Ruff compliance with existing ruff.toml configuration
        - Type hints for all function signatures
        - Google-style docstrings with Args, Returns, and Raises sections
        - Proper error handling with specific exceptions
        - Security: validate inputs, avoid shell injection, handle credentials safely
        - Logging for debugging and monitoring
        - Command-line argument validation

    - path: "plugins/**/.claude-plugin/*.json"
      instructions: |
        Validate plugin manifests for:
        - Required fields present: name, version, description, author, keywords
        - Semantic versioning format (X.Y.Z)
        - JSON schema compliance
        - Accurate dependency specifications
        - Consistency with marketplace registry

    - path: ".claude-plugin/marketplace.json"
      instructions: |
        Critical marketplace registry review:
        - All listed plugins have corresponding directories
        - Plugin metadata matches individual plugin.json files
        - Version numbers are consistent across registry and plugin files
        - No duplicate plugin names or paths
        - Valid JSON structure

    - path: "**/*.sh"
      instructions: |
        Shell script review:
        - Shellcheck compliance
        - Error handling: set -e, set -u, set -o pipefail
        - Input validation and sanitization
        - No hardcoded credentials or sensitive data
        - Clear comments for complex operations
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit path instructions part 1**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): add path instructions for Python and plugin files"
```

---

## Task 7: Configure Path-Specific Instructions (Part 2)

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add path_instructions for documentation files**

Add after the shell script instructions:

```yaml

    - path: "plugins/**/skills/**/*.md"
      instructions: |
        Skills documentation quality:
        - Clear skill metadata (name, description)
        - Unambiguous usage instructions
        - Concrete, executable examples
        - Follows skill documentation standards
        - No sensitive information or credentials in examples
        - Proper markdown formatting

    - path: "plugins/**/commands/**/*.md"
      instructions: |
        Slash command documentation:
        - Clear command purpose and use cases
        - Accurate argument specifications
        - Usage examples with expected output
        - Integration notes with other commands if relevant

    - path: "plugins/**/agents/**/*.md"
      instructions: |
        Agent definitions review:
        - Clear agent purpose and capabilities
        - Tool access properly specified
        - Behavioral instructions are unambiguous
        - No conflicting instructions
        - Model specifications follow inheritance pattern (default to inherit from parent)

    - path: "docs/**/*.md"
      instructions: |
        Published documentation standards:
        - Clear, concise technical writing
        - Accurate code examples and commands
        - Proper markdown formatting per .rumdl.toml
        - Valid internal links
        - Examples are up-to-date with current codebase
        - No outdated information

    - path: "{*.toml,*.yaml,*.json}"
      instructions: |
        Configuration file review:
        - Valid syntax for file type
        - Schema compliance where applicable
        - Comments explain non-obvious settings
        - Consistent with project conventions
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit path instructions part 2**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): add path instructions for documentation files"
```

---

## Task 8: Configure Tool Integration

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add finishing_touches section**

Add after `path_instructions` section:

```yaml

  finishing_touches:
    docstrings:
      enabled: true
    unit_tests:
      enabled: true
```

**Step 2: Add tools section**

Add after `finishing_touches`:

```yaml

  tools:
    # Python tools
    ruff:
      enabled: true
    pylint:
      enabled: true

    # Shell tools
    shellcheck:
      enabled: true

    # Markdown tools
    markdownlint:
      enabled: true

    # YAML tools
    yamllint:
      enabled: true

    # Security scanning
    gitleaks:
      enabled: false
    checkov:
      enabled: true

    # GitHub checks integration
    github-checks:
      enabled: true
      timeout_ms: 90000
```

**Step 3: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 4: Commit tool configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure tool integration"
```

---

## Task 9: Configure Chat Settings

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add chat section**

Add after the `reviews` section (at same indentation level as `reviews:`):

```yaml

chat:
  auto_reply: true
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit chat configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): enable auto-reply in chat"
```

---

## Task 10: Configure Knowledge Base

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add knowledge_base section**

Add after the `chat` section:

```yaml

knowledge_base:
  opt_out: false
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/CLAUDE.md"
      - "plugins/meta/claude-docs/skills/claude-docs/reference/**/*.md"
  learnings:
    scope: auto
  web_search:
    enabled: true
  issues:
    scope: auto
  pull_requests:
    scope: auto
```

**Step 2: Validate syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Commit knowledge base configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure knowledge base with CLAUDE.md and official docs"
```

---

## Task 11: Configure Code Generation

**Files:**
- Modify: `.coderabbit.yaml`

**Step 1: Add code_generation section**

Add after the `knowledge_base` section:

```yaml

code_generation:
  docstrings:
    language: en-US
    path_instructions:
      - path: "scripts/**/*.py"
        instructions: "Use Google-style docstrings with Args, Returns, and Raises sections. Type hints in signatures (not docstrings). Include usage examples for complex functions. Focus on behavior and edge cases rather than implementation details."
      - path: "plugins/**/tools/**/*.py"
        instructions: "Brief docstrings focusing on tool purpose and parameters. Include examples for non-obvious usage."
  unit_tests:
    path_instructions:
      - path: "scripts/**/*.py"
        instructions: "Generate tests covering happy paths, error handling, edge cases, and boundary conditions. Use pytest framework. Focus on validating behavior, not implementation details. Mock external dependencies (file I/O, network calls, subprocess). Tests should be independent and not rely on execution order."
```

**Step 2: Validate final syntax**

Run:
```bash
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))" && echo "✓ YAML syntax valid"
```

Expected: "✓ YAML syntax valid"

**Step 3: Verify file completeness**

Run:
```bash
cat .coderabbit.yaml | head -5
```

Expected output should start with:
```text
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: "Provide comprehensive feedback..."
```

**Step 4: Commit final configuration**

```bash
git add .coderabbit.yaml
git commit -m "feat(coderabbit): configure code generation for docstrings and tests"
```

---

## Task 12: Verify Configuration

**Files:**
- Read: `.coderabbit.yaml`

**Step 1: Check file size**

Run:
```bash
ls -lh .coderabbit.yaml
```

Expected: File size approximately 5-6KB

**Step 2: Verify schema validation**

Open `.coderabbit.yaml` in VS Code and check:
- No YAML syntax errors highlighted
- No schema validation errors
- Hover over keys shows CodeRabbit schema documentation

Expected: Clean validation, no errors

**Step 3: Remove backup file**

Run:
```bash
rm backup.coderabbit.yaml
git add -u
git commit -m "chore: remove backup CodeRabbit config"
```

**Step 4: View final git log**

Run:
```bash
git log --oneline -12
```

Expected: 12 commits showing incremental CodeRabbit configuration build

---

## Verification Commands

After implementation, verify:

```bash
# Check YAML syntax
uv run python -c "import yaml; yaml.safe_load(open('.coderabbit.yaml'))"

# View file
cat .coderabbit.yaml

# Check file exists and size
ls -lh .coderabbit.yaml

# Review commits
git log --oneline --grep="coderabbit"
```

## Success Criteria

Configuration is complete when:
1. ✅ `.coderabbit.yaml` exists in repository root
2. ✅ YAML syntax is valid (no parse errors)
3. ✅ Schema reference is correct and validates in editor
4. ✅ All sections present: language, reviews, chat, knowledge_base, code_generation
5. ✅ Path filters exclude working docs and examples
6. ✅ Path instructions cover all critical file types
7. ✅ Tools configured with existing configs respected
8. ✅ Knowledge base references CLAUDE.md and official docs
9. ✅ All changes committed with descriptive messages
10. ✅ backup.coderabbit.yaml removed
