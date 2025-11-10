# CodeRabbit Configuration Guide: Mastering the `.coderabbit.yaml` File

Before diving into the specifics of configuration, it's essential to understand that CodeRabbit offers a powerful, version-controlled approach to customizing AI-powered code reviews through the `.coderabbit.yaml` file. This comprehensive guide will walk you through every aspect of configuring CodeRabbit, from basic setup to advanced customization strategies, enabling you to tailor the tool to your team's exact needs.[^1][^2]

## Understanding CodeRabbit Configuration Architecture

CodeRabbit supports multiple configuration approaches, each serving different organizational needs. The **YAML file approach** is the recommended best practice for most development teams, as it provides infrastructure-as-code benefits including configuration change tracking, code review integration, and version history maintenance. When multiple configuration sources exist, CodeRabbit follows a strict priority hierarchy where local `.coderabbit.yaml` files take complete precedence over all other settings, including central configuration, repository settings, and organization settings.[^2][^1]

The configuration priority system operates as follows: the local `.coderabbit.yaml` file has the highest priority and completely overrides all other settings. If a setting isn't defined in the local YAML file, CodeRabbit uses the default value rather than checking lower-priority sources. This non-merging behavior means your local configuration must be comprehensive for the settings you want to control.[^3][^1]

## Getting Started: Initial Setup

Creating your first `.coderabbit.yaml` file begins with understanding the fundamental structure and essential configuration elements. The file should reside in the root directory of your repository and must include the YAML schema reference for validation and autocomplete support in modern editors.[^4][^2]

### Basic Configuration Structure

Every `.coderabbit.yaml` file should start with the schema reference, which enables intelligent editor support and validation. The schema ensures your configuration adheres to CodeRabbit's expected format and provides helpful suggestions during editing:[^5][^2][^4]

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: ""
early_access: false
enable_free_tier: true
```

The global settings section controls fundamental aspects of CodeRabbit's behavior across your entire repository. The **language** setting accepts ISO language codes and determines the language used for reviews and communication. CodeRabbit supports over 60 languages including various English dialects, European languages, Asian languages, and regional variations.[^1][^5]

The **tone_instructions** setting allows you to customize how CodeRabbit communicates in reviews and chat interactions. This optional field accepts up to 250 characters of natural language instructions that modify CodeRabbit's communication style. For example, you might specify "Be concise and focus on critical issues only" or "Use a friendly, educational tone when explaining issues".[^5][^1]

### Essential Configuration Sections

The configuration file divides into four primary sections that control different aspects of CodeRabbit's functionality. The **reviews** section manages automatic code reviews, tool integrations, and review behavior. The **chat** section configures interactive features and third-party integrations. The **knowledge_base** section controls learning capabilities and knowledge sharing features. Finally, the **code_generation** section handles settings for automated documentation and test generation.[^1][^5]

## Configuring Code Review Behavior

The reviews section represents the core of CodeRabbit's functionality and contains the most extensive configuration options. Understanding these settings enables you to fine-tune how CodeRabbit analyzes and reports on code changes.[^6][^4][^1]

### Review Profiles and Strictness

CodeRabbit offers two distinct review profiles that fundamentally change the review approach. The **chill** profile provides balanced feedback focusing on significant issues without overwhelming developers with minor suggestions. This default profile works well for most teams and reduces review noise while maintaining code quality standards.[^5][^1]

The **assertive** profile delivers more comprehensive feedback that some developers might consider nitpicky. This profile examines code more thoroughly and provides suggestions on style, optimization, and best practices that the chill profile might overlook. Teams with strict coding standards or those seeking to improve code quality metrics often prefer this profile:[^6][^1][^5]

```yaml
reviews:
  profile: assertive  # or 'chill' for less feedback
  high_level_summary: true
  review_status: true
```

### Automatic Review Configuration

The auto_review subsection controls when and how CodeRabbit automatically triggers reviews. Enabling automatic reviews means CodeRabbit will analyze every new pull request and subsequent commits without manual intervention. This setting can be selectively disabled for specific scenarios like draft pull requests:[^4][^3][^6][^1]

```yaml
reviews:
  auto_review:
    enabled: true
    auto_incremental_review: true
    drafts: false
    ignore_title_keywords: []
    labels: []
    base_branches: []
```

The **auto_incremental_review** setting determines whether CodeRabbit reviews new commits to existing pull requests. When enabled, CodeRabbit provides focused feedback on changes since the last review rather than re-reviewing the entire pull request. The **drafts** setting controls whether CodeRabbit reviews draft pull requests, which many teams disable to avoid noise during experimental development.[^7][^6][^4][^1][^5]

Advanced automatic review filtering includes **ignore_title_keywords** for skipping reviews based on pull request titles, **labels** for limiting reviews to pull requests with specific labels, and **base_branches** for extending automatic reviews beyond the default branch to include other important branches like staging or development.[^3][^7]

### Pull Request Summaries and Metadata

CodeRabbit can generate comprehensive pull request summaries and automatically suggest metadata improvements. The high-level summary feature creates an overview of changes that gets inserted into the pull request description, helping reviewers quickly understand the scope and impact of changes:[^1][^5]

```yaml
reviews:
  high_level_summary: true
  high_level_summary_placeholder: "@coderabbitai summary"
  high_level_summary_in_walkthrough: false
  auto_title_placeholder: "@coderabbitai"
  auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"
```

The **auto_title_instructions** setting enables automatic pull request title generation when you include the auto_title_placeholder in the PR title. This feature helps enforce consistent naming conventions across your organization. For example, you might require conventional commit format or mandate inclusion of ticket numbers.[^5][^1]

### Walkthrough Customization

The walkthrough comment provides detailed analysis of code changes and can be extensively customized to match your team's preferences. CodeRabbit can generate walkthroughs in expandable sections, include file summaries, create sequence diagrams, estimate review effort, assess issue resolution, and suggest related issues and pull requests:[^1][^5]

```yaml
reviews:
  collapse_walkthrough: false
  changed_files_summary: true
  sequence_diagrams: true
  review_effort: true
  assess_linked_issues: true
  related_issues: true
  related_prs: true
```

Setting **collapse_walkthrough** to true places the detailed walkthrough in a collapsible markdown section, reducing visual clutter in the pull request conversation. The **sequence_diagrams** option generates visual flow diagrams for complex code changes, particularly useful for architectural modifications.[^5][^1]

### Label and Reviewer Suggestions

CodeRabbit can analyze code changes and automatically suggest appropriate labels and reviewers. This automation helps maintain consistent labeling across pull requests and ensures the right people review relevant changes:[^1][^5]

```yaml
reviews:
  suggested_labels: true
  auto_apply_labels: false
  labeling_instructions:
    - label: "security"
      instructions: "Apply this label to changes affecting authentication, authorization, encryption, or data validation"
    - label: "database"
      instructions: "Apply this label to changes in database schemas, migrations, or query logic"
  suggested_reviewers: true
  auto_assign_reviewers: false
```

The **labeling_instructions** array allows you to provide specific guidance for label application. When configured, CodeRabbit considers only the specified labels rather than learning from historical patterns alone. The **auto_apply_labels** and **auto_assign_reviewers** settings enable automatic application of suggestions without manual confirmation.[^5][^1]

### Commit Status Integration

CodeRabbit integrates with repository commit status checks to provide visual feedback about review progress and completion. These settings control how CodeRabbit updates commit status during the review lifecycle:[^1][^5]

```yaml
reviews:
  commit_status: true
  fail_commit_status: false
  review_status: true
```

The **commit_status** setting updates the status to "pending" during reviews and "success" upon completion. The **fail_commit_status** option allows CodeRabbit to set the status to "failure" when reviews cannot be completed due to errors. Setting this to true can prevent merging of problematic pull requests.[^5][^1]

### Request Changes Workflow

The request changes workflow enables CodeRabbit to approve pull requests after all review comments are resolved, useful for teams requiring multiple approvals:[^6][^3]

```yaml
reviews:
  request_changes_workflow: false
```

When enabled, CodeRabbit can approve reviews once its comments are addressed and pre-merge checks pass. Organizations should still require at least one human reviewer approval even with this feature enabled.[^3][^6]

## Path-Based Configuration

Path filtering and path-specific instructions represent powerful customization capabilities that allow different review approaches for different parts of your codebase. This granular control ensures CodeRabbit focuses on relevant code while ignoring generated files, build artifacts, and other non-reviewable content.[^8][^6][^3]

### Path Filters for Exclusion and Inclusion

Path filters use glob patterns to specify which files CodeRabbit should include or exclude from reviews. Excluding build directories, dependencies, and generated code significantly improves review speed and reduces contextual noise:[^2][^6][^3]

```yaml
reviews:
  path_filters:
    # Exclude build and dependency directories
    - "!**/dist/**"
    - "!**/build/**"
    - "!**/node_modules/**"
    - "!**/.next/**"
    - "!**/.nuxt/**"
    - "!**/.yarn/**"

    # Exclude generated code
    - "!**/generated/**"
    - "!**/@generated/**"
    - "!**/__generated__/**"

    # Exclude test fixtures and mock data
    - "!**/__fixtures__/**"
    - "!**/__mocks__/**"
    - "!**/fixtures/**"

    # Include only specific directories
    - "src/**"
    - "lib/**"
```

Path filters also apply to git sparse-checkout operations, so CodeRabbit clones only the specified patterns while ignoring excluded paths. This optimization reduces repository cloning time and resource consumption.[^8][^1]

### Path Instructions for Targeted Reviews

Path instructions provide specific review guidelines for different file types or directories. Unlike code guidelines (which reference existing documentation files), path instructions contain direct review instructions embedded in the configuration:[^8][^6][^3]

```yaml
reviews:
  path_instructions:
    - path: "src/**/*.{ts,tsx}"
      instructions: |
        Review React and TypeScript code for:
        - React hooks best practices and proper dependency arrays
        - Type safety and avoiding 'any' types
        - Component composition and prop validation
        - Performance optimization opportunities (useMemo, useCallback)
        - Accessibility (ARIA attributes, keyboard navigation)

    - path: "src/api/**/*.ts"
      instructions: |
        Focus on API security:
        - Input validation and sanitization
        - SQL injection prevention
        - Authentication and authorization checks
        - Rate limiting implementation
        - Error handling without information disclosure

    - path: "**/*.test.{ts,tsx,js,jsx}"
      instructions: |
        Evaluate test quality:
        - Test coverage of edge cases and error conditions
        - Use of appropriate test assertions
        - Test isolation and independence
        - Mock usage and test data management
        - Clear test descriptions and organization
```

Path instructions apply to files matching the specified glob patterns and provide CodeRabbit with domain-specific context for more relevant reviews. Common use cases include enforcing security practices in API routes, checking React best practices in component files, and validating test quality in test files.[^6][^8]

## Tool Integration and Linters

CodeRabbit supports integration with over 40 static analysis tools, linters, and security scanners. By default, CodeRabbit automatically runs all applicable tools based on detected file types, providing zero-configuration linting out of the box.[^9][^10][^11][^2]

### Understanding Tool Configuration

Each tool can be individually enabled or disabled, and some tools support custom configuration files. The tools section allows granular control over which analyzers run during code reviews:[^9][^2][^1]

```yaml
reviews:
  tools:
    # JavaScript/TypeScript tools
    eslint:
      enabled: true
    biome:
      enabled: true
    oxlint:
      enabled: true

    # Python tools
    ruff:
      enabled: true
    pylint:
      enabled: true
    flake8:
      enabled: true

    # Security scanners
    gitleaks:
      enabled: true
    checkov:
      enabled: true
    semgrep:
      enabled: true
      config_file: ".semgrep.yml"

    # Language-specific linters
    golangci-lint:
      enabled: true
      config_file: ".golangci.yml"
    rubocop:
      enabled: true
    swiftlint:
      enabled: true
      config_file: ".swiftlint.yml"

    # Documentation and formatting
    markdownlint:
      enabled: true
    yamllint:
      enabled: true
    hadolint:
      enabled: true

    # Code quality analyzers
    pmd:
      enabled: true
      config_file: "pmd-ruleset.xml"
    phpstan:
      enabled: true
      level: default
    detekt:
      enabled: true
      config_file: "detekt.yml"
```

The comprehensive tool support covers diverse technology stacks including JavaScript/TypeScript (ESLint, Biome, oxlint), Python (Ruff, Pylint, Flake8), Go (golangci-lint), Ruby (RuboCop, Brakeman), Swift (SwiftLint), PHP (PHPStan, PHPMD, PHPCS), Java (PMD), Kotlin (detekt), Rust (Clippy), and many others.[^10][^9]

### Tool-Specific Configuration Files

Many tools support custom configuration files that define rules, severity levels, and other behavior. CodeRabbit respects these configuration files when they exist in your repository, ensuring consistency with your existing development workflow:[^12][^13][^9]

```yaml
reviews:
  tools:
    eslint:
      enabled: true
      # Looks for .eslintrc.js, .eslintrc.json, etc.

    golangci-lint:
      enabled: true
      config_file: ".golangci.yml"

    pylint:
      enabled: true
      # Looks for .pylintrc, pylintrc, etc.

    markdownlint:
      enabled: true
      # Looks for .markdownlint.json, .markdownlint.yaml, etc.
```

CodeRabbit automatically discovers standard configuration files for most tools, but you can explicitly specify custom paths using the config_file parameter.[^12][^9]

### GitHub Checks Integration

The github-checks tool provides special integration with GitHub's built-in checks, analyzing CI/CD failures and providing remediation suggestions. This tool includes a configurable timeout for check completion:[^4][^9]

```yaml
reviews:
  tools:
    github-checks:
      enabled: true
      timeout_ms: 90000  # 90 seconds
```

### AST-Grep Custom Rules

Advanced users can define custom Abstract Syntax Tree rules using ast-grep for project-specific code patterns and anti-patterns. This powerful feature enables enforcement of architectural decisions and custom coding standards:[^8]

```yaml
reviews:
  tools:
    ast-grep:
      enabled: true
      rule_dirs:
        - "rules"
      util_dirs:
        - "utils"
      essential_rules: true
      packages:
        - "my-org/shared-rules"
```

AST-grep rules must reside in directories named exactly `rules` and `utils` within your repository, though the internal structure of these directories remains flexible.[^8]

## Knowledge Base and Learning Features

CodeRabbit's knowledge base features enable the platform to learn from your team's preferences, understand coding guidelines, and provide increasingly tailored reviews over time. These features require data retention but offer significant value through adaptive behavior.[^14][^15][^6][^1]

### Code Guidelines Integration

CodeRabbit automatically detects and applies coding standards from popular AI agent configuration files, ensuring consistency across your AI tool ecosystem. This zero-setup feature recognizes common configuration patterns and applies the embedded guidelines during code reviews:[^16][^14]

```yaml
knowledge_base:
  opt_out: false
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - ".github/copilot-instructions.md"
      - "**/CLAUDE.md"
      - ".cursor/rules/**"
      - "**/.windsurfrules"
      - "**/.clinerules/**"
      - "**/agent.md"
      - "**/.rules/**"
      - "**/CODING_STANDARDS.md"
      - "**/CODE_STYLE_GUIDE.md"
```

Supported configuration files include `.cursorrules` for Cursor AI editor, `.github/copilot-instructions.md` for GitHub Copilot, `CLAUDE.md` for Claude Code, `.windsurfrules` for Windsurf editor, and various other AI agent configurations. If you already use these files for other AI tools, CodeRabbit automatically follows the same guidelines without additional configuration.[^14][^16]

### Learnings Configuration

Learnings represent CodeRabbit's adaptive learning system that captures your team's review preferences through natural language interactions. Developers teach CodeRabbit by providing feedback on review comments, and the platform incorporates these lessons into future reviews:[^15][^14][^6]

```yaml
knowledge_base:
  learnings:
    scope: auto  # Options: auto, global, local
```

The **scope** setting determines how broadly CodeRabbit applies learned preferences. The **auto** setting (default) applies repository-specific learnings for public repositories and all organizational learnings for private repositories. The **global** setting applies all organizational learnings to every code review regardless of repository. The **local** setting restricts learnings to their respective repositories only.[^15]

Learnings work best when combined with code guidelines—use guidelines for static rules that rarely change, and use learnings for dynamic team preferences that evolve over time.[^14]

### Issue Tracking Integration

CodeRabbit analyzes whether pull request changes adequately address linked issues. This functionality works automatically with GitHub and GitLab issues but requires configuration for external systems like Jira and Linear:[^2][^6]

```yaml
knowledge_base:
  issues:
    scope: auto

  jira:
    usage: auto  # Options: auto, enabled, disabled
    project_keys: []

  linear:
    usage: auto
    team_keys: []
```

The **usage** setting controls how CodeRabbit interacts with external issue trackers. The **auto** setting automatically determines appropriate integration based on detected project configuration. Setting specific project keys or team keys limits integration to particular Jira projects or Linear teams.[^3]

### Web Search Capabilities

CodeRabbit can perform web searches to gather context about libraries, frameworks, and best practices during code reviews. This feature enhances review quality by incorporating current documentation and community knowledge:[^1]

```yaml
knowledge_base:
  web_search:
    enabled: true
```

### Pull Request Context

The pull request configuration enables CodeRabbit to reference and learn from previous pull requests in your repository, providing context-aware suggestions based on similar changes:[^1]

```yaml
knowledge_base:
  pull_requests:
    scope: auto
```

### Data Retention and Privacy

Organizations with strict data retention policies can opt out of all knowledge base features. Disabling data retention immediately and irrevocably deletes all stored learnings, issue metadata, and other knowledge base information associated with your organization:[^15][^6][^3]

```yaml
knowledge_base:
  opt_out: false  # Set to true to disable all knowledge base features
```

Alternatively, you can disable specific knowledge base components while maintaining others. For example, you might enable code guidelines but disable learnings storage.[^3]

## Code Generation Features

CodeRabbit's finishing touches capabilities include automatic generation of docstrings and unit tests. These features help maintain code quality and documentation standards across your codebase.[^17][^18][^4][^1]

### Docstring Generation

Docstring generation creates comprehensive function and class documentation in appropriate formats for your programming language. This feature can be triggered manually via chat commands or configured for automatic generation:[^18][^17][^1]

```yaml
reviews:
  finishing_touches:
    docstrings:
      enabled: true

code_generation:
  docstrings:
    language: en-US
    path_instructions:
      - path: "src/**/*.ts"
        instructions: |
          Use TSDoc format with @param, @returns, and @example tags.
          Include code examples for public API functions.
          Focus on behavior and edge cases rather than implementation details.

      - path: "src/**/*.py"
        instructions: |
          Use Google-style docstrings with Args, Returns, and Raises sections.
          Include type hints in the docstring.
          Provide usage examples for complex functions.

      - path: "**/*test*"
        instructions: |
          Keep test docstrings brief, focusing on what is being tested.
          Use "Test that..." format for clarity.
```

Path-specific docstring instructions enable different documentation standards for different parts of your codebase. For example, public APIs might require comprehensive examples while internal utilities need only brief descriptions.[^19]

### Unit Test Generation

Unit test generation creates comprehensive test suites for your code, following your project's testing conventions and patterns:[^20][^18][^1]

```yaml
reviews:
  finishing_touches:
    unit_tests:
      enabled: true

code_generation:
  unit_tests:
    path_instructions:
      - path: "src/api/**/*.ts"
        instructions: |
          Generate tests covering:
          - Happy path scenarios with valid inputs
          - Error handling for invalid inputs
          - Edge cases and boundary conditions
          - Authentication and authorization scenarios
          - Database interaction mocking
          Use Jest and supertest for API testing.

      - path: "src/components/**/*.tsx"
        instructions: |
          Generate React component tests covering:
          - Component rendering with different props
          - User interaction simulation
          - Conditional rendering logic
          - Integration with hooks and context
          Use React Testing Library and Jest.
```

Unit test generation creates test files as part of finishing touches, which you can review and modify before merging.[^20][^4]

## Chat and Integration Settings

The chat section controls CodeRabbit's interactive features and integrations with third-party platforms:[^5][^1]

```yaml
chat:
  auto_reply: true
  integrations:
    jira:
      usage: enabled  # Options: enabled, disabled, auto
    linear:
      usage: auto
```

The **auto_reply** setting enables CodeRabbit to respond to comments automatically without requiring explicit @mentions. This creates a more conversational review experience but may generate more activity in pull request discussions.[^5][^1]

Integration settings control how CodeRabbit interacts with external platforms. The **usage** parameter accepts three values: **enabled** for always active integration, **disabled** to completely turn off integration, and **auto** for intelligent activation based on detected project configuration.[^3]

## Advanced Configuration Patterns

### Comprehensive Enterprise Configuration

Enterprise teams often require extensive configuration covering security, compliance, code quality, and team workflow requirements. This example demonstrates a production-ready configuration for a large organization:[^21]

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: "Be concise and focus on critical security and performance issues. Provide actionable suggestions with code examples."
early_access: false

reviews:
  profile: assertive
  request_changes_workflow: false
  high_level_summary: true
  high_level_summary_in_walkthrough: true
  auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"

  collapse_walkthrough: false
  sequence_diagrams: true
  review_effort: true
  poem: false

  suggested_labels: true
  auto_apply_labels: true
  labeling_instructions:
    - label: "security"
      instructions: "Critical security issues including authentication, authorization, injection vulnerabilities, or data exposure"
    - label: "performance"
      instructions: "Performance concerns including inefficient algorithms, memory leaks, or database query optimization"
    - label: "breaking-change"
      instructions: "Changes that break backward compatibility or require API consumers to update"

  path_filters:
    - "!**/dist/**"
    - "!**/build/**"
    - "!**/node_modules/**"
    - "!**/.next/**"
    - "!**/coverage/**"
    - "!**/__generated__/**"

  path_instructions:
    - path: "src/auth/**/*.ts"
      instructions: |
        Critical security review required:
        - Verify authentication mechanisms follow OWASP guidelines
        - Check for proper password hashing with bcrypt/argon2
        - Validate JWT token expiration and refresh logic
        - Ensure sensitive data is not logged
        - Check for SQL injection and XSS vulnerabilities

    - path: "src/api/**/*.ts"
      instructions: |
        API security and quality:
        - Input validation using Zod or similar libraries
        - Proper error handling without sensitive information leakage
        - Rate limiting implementation
        - API versioning strategy compliance
        - OpenAPI/Swagger documentation accuracy

    - path: "src/database/**/*.ts"
      instructions: |
        Database code review:
        - Migration scripts are reversible
        - Indexes defined for frequently queried columns
        - N+1 query problems avoided
        - Connection pooling properly configured
        - Transactions used appropriately

  abort_on_close: true
  disable_cache: false

  auto_review:
    enabled: true
    auto_incremental_review: true
    drafts: false
    ignore_title_keywords:
      - "WIP"
      - "DO NOT MERGE"

  finishing_touches:
    docstrings:
      enabled: true
    unit_tests:
      enabled: true

  tools:
    eslint:
      enabled: true
    biome:
      enabled: true
    gitleaks:
      enabled: true
    checkov:
      enabled: true
    github-checks:
      enabled: true
      timeout_ms: 120000

chat:
  auto_reply: true
  integrations:
    jira:
      usage: enabled

knowledge_base:
  opt_out: false
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - "**/CODING_STANDARDS.md"
  learnings:
    scope: auto
  web_search:
    enabled: true

code_generation:
  docstrings:
    language: en-US
    path_instructions:
      - path: "src/**/*.ts"
        instructions: "Use TSDoc format with comprehensive examples for public APIs"
  unit_tests:
    path_instructions:
      - path: "src/**/*.ts"
        instructions: "Generate comprehensive Jest tests covering happy paths, error cases, and edge conditions"
```

### Minimal Configuration for Getting Started

Teams new to CodeRabbit should start with minimal configuration and gradually add customizations based on experience:[^4][^6][^5]

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US

reviews:
  profile: chill
  high_level_summary: true

  auto_review:
    enabled: true
    drafts: false

  path_filters:
    - "!**/node_modules/**"
    - "!**/dist/**"

  poem: false

  tools:
    eslint:
      enabled: true
    gitleaks:
      enabled: true
```

### Technology-Specific Configurations

Different technology stacks benefit from tailored configurations that activate relevant tools and provide appropriate guidance.

**Python Project Configuration:**

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US

reviews:
  profile: assertive

  path_filters:
    - "!**/__pycache__/**"
    - "!**/venv/**"
    - "!**/.pytest_cache/**"

  path_instructions:
    - path: "**/*.py"
      instructions: |
        Review Python code for:
        - PEP 8 compliance and pythonic patterns
        - Type hints for function signatures
        - Proper exception handling
        - Security issues (SQL injection, command injection)
        - Performance optimization opportunities

  tools:
    ruff:
      enabled: true
    pylint:
      enabled: true
    flake8:
      enabled: true
    gitleaks:
      enabled: true
```

**Go Project Configuration:**

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US

reviews:
  profile: assertive

  path_instructions:
    - path: "**/*.go"
      instructions: |
        Review Go code for:
        - Proper error handling without ignored errors
        - Concurrency safety and goroutine leak prevention
        - Context usage in long-running operations
        - Idiomatic Go patterns and conventions
        - Resource cleanup with defer

  tools:
    golangci-lint:
      enabled: true
      config_file: ".golangci.yml"
    gitleaks:
      enabled: true
```

## Configuration Management Best Practices

Effective configuration management requires understanding how to test, validate, and maintain your `.coderabbit.yaml` file over time.[^22][^2][^6]

### Exporting Current Configuration

Before creating a `.coderabbit.yaml` file, you can export your current configuration from the CodeRabbit UI using the chat command. This provides a starting point based on your existing settings:[^22][^2]

```text
@coderabbitai configuration
```

CodeRabbit responds with your current effective configuration in YAML format, which you can copy into a new `.coderabbit.yaml` file.[^2]

### Validating Configuration

CodeRabbit provides an online YAML validator tool that checks syntax and validates against the configuration schema. This tool helps identify errors before committing configuration changes.[^23][^24]

Additionally, the schema reference in your YAML file enables real-time validation in editors like VS Code, providing immediate feedback on configuration errors and autocomplete suggestions for available options.[^2][^4][^5]

### Testing Configuration Changes

When modifying configuration, follow these best practices to minimize disruption:

1. **Test on smaller pull requests first** before applying to large changes[^7]
2. **Keep backups of working configurations** before making significant modifications[^7]
3. **Use version control** to track configuration changes and enable easy rollback[^22][^2]
4. **Review configuration changes in pull requests** just like code changes[^2]
5. **Document configuration decisions** in commit messages for future reference[^22]

### Iterative Refinement

Configuration optimization is an ongoing process. Start with conservative settings and gradually adjust based on review quality and team feedback. Monitor these indicators to guide refinement:

- Review comment quality and relevance
- False positive rate from linters
- Team engagement with CodeRabbit suggestions
- Time saved in manual review processes
- Code quality metrics over time

### Central Configuration for Organizations

Organizations managing many repositories can create central configuration that applies across all repositories lacking their own `.coderabbit.yaml` files. This approach establishes organization-wide defaults while allowing repository-specific overrides:[^25]

1. Create a repository named `coderabbit` in your organization
2. Add a `.coderabbit.yaml` file with default organization settings
3. Individual repositories can override these defaults with their own `.coderabbit.yaml` files

Central configuration follows the priority hierarchy: repository files override central configuration, which overrides organization UI settings.[^25]

## Common Configuration Scenarios

### Scenario: Frontend React Application

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: "Focus on React best practices, performance, and accessibility"

reviews:
  profile: assertive

  path_filters:
    - "!**/node_modules/**"
    - "!**/build/**"
    - "!**/.next/**"
    - "!**/coverage/**"

  path_instructions:
    - path: "src/components/**/*.{tsx,jsx}"
      instructions: |
        Review React components for:
        - Proper hooks usage and dependency arrays
        - Performance optimization (memo, useMemo, useCallback)
        - Accessibility (ARIA attributes, semantic HTML)
        - Component composition and reusability
        - Prop validation with TypeScript

    - path: "src/**/*.test.{tsx,ts}"
      instructions: |
        Ensure tests:
        - Use React Testing Library best practices
        - Test user behavior, not implementation
        - Cover edge cases and error states
        - Use appropriate queries and assertions

  tools:
    eslint:
      enabled: true
    biome:
      enabled: true
    oxlint:
      enabled: true

  finishing_touches:
    docstrings:
      enabled: true

code_generation:
  docstrings:
    path_instructions:
      - path: "src/components/**/*.{tsx,jsx}"
        instructions: "Use JSDoc with @param and @returns. Include usage examples for complex components."
```

### Scenario: Security-Focused Backend API

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US
tone_instructions: "Prioritize security vulnerabilities and provide detailed remediation guidance"

reviews:
  profile: assertive

  path_instructions:
    - path: "src/api/**/*.ts"
      instructions: |
        Critical security review:
        - Input validation and sanitization
        - SQL injection prevention
        - Authentication and authorization
        - Rate limiting and DDoS protection
        - Sensitive data handling and logging
        - Error messages without information disclosure

  tools:
    eslint:
      enabled: true
    gitleaks:
      enabled: true
    checkov:
      enabled: true
    semgrep:
      enabled: true
      config_file: "security-rules.yml"

  labeling_instructions:
    - label: "security-critical"
      instructions: "Any code handling authentication, authorization, encryption, or sensitive data"
    - label: "requires-security-review"
      instructions: "Changes to API endpoints, database queries, or external integrations"

knowledge_base:
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/SECURITY_GUIDELINES.md"
```

### Scenario: Monorepo with Multiple Projects

```yaml
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json

language: en-US

reviews:
  profile: chill

  path_filters:
    - "!**/node_modules/**"
    - "!**/dist/**"
    - "!**/build/**"

  path_instructions:
    - path: "packages/frontend/**/*.{ts,tsx}"
      instructions: "Apply React and TypeScript best practices. Focus on component architecture and state management."

    - path: "packages/backend/**/*.ts"
      instructions: "Review for API security, database query optimization, and error handling."

    - path: "packages/shared/**/*.ts"
      instructions: "Ensure changes maintain backward compatibility. Verify comprehensive unit test coverage."

    - path: "packages/**/README.md"
      instructions: "Check documentation accuracy and completeness. Verify examples are up-to-date."

  tools:
    eslint:
      enabled: true
    markdownlint:
      enabled: true
    gitleaks:
      enabled: true

code_generation:
  docstrings:
    path_instructions:
      - path: "packages/shared/**/*.ts"
        instructions: "Comprehensive TSDoc documentation required for all public APIs with usage examples"
```

## Troubleshooting Common Issues

Understanding common configuration issues helps resolve problems quickly and maintain smooth operations.[^6][^2][^1]

### Configuration Not Taking Effect

**Problem:** Changes to `.coderabbit.yaml` don't appear in reviews.

**Solutions:**

1. Verify the configuration file exists in the repository root
2. Check the file is named exactly `.coderabbit.yaml` (note the leading dot)
3. Ensure the configuration is in the feature branch, not just main
4. Validate YAML syntax using the CodeRabbit validator tool
5. Review CodeRabbit's comment on the pull request to see which configuration source is active

### Tool Not Running

**Problem:** Expected linter or analyzer doesn't execute during reviews.

**Solutions:**

1. Verify the tool is enabled in your configuration
2. Check if the tool supports your file types
3. Ensure required configuration files exist if specified
4. Review tool-specific requirements in the CodeRabbit documentation
5. Check if path filters are excluding relevant files

### Excessive Review Comments

**Problem:** CodeRabbit generates too many comments, overwhelming reviewers.

**Solutions:**

1. Switch from `assertive` to `chill` profile
2. Disable specific tools generating noise
3. Add path filters to exclude generated code and dependencies
4. Configure path instructions to focus on critical issues
5. Adjust tone_instructions to request concise feedback
6. Disable optional walkthrough features like poems and sequence diagrams

### Missing Expected Features

**Problem:** Features like docstring generation or learnings aren't working.

**Solutions:**

1. Verify the feature is enabled in configuration
2. Check organization-level data retention settings
3. Ensure you haven't opted out of knowledge base features
4. Confirm the feature is available in your pricing tier
5. Check if early access features require the `early_access: true` setting

## Conclusion

Mastering CodeRabbit configuration through the `.coderabbit.yaml` file enables teams to create highly customized, context-aware code review workflows that align with organizational standards and development practices. The configuration system provides granular control over review behavior, tool integration, knowledge base features, and code generation capabilities while maintaining the flexibility to adapt as projects evolve.[^6][^2][^1]

Starting with a minimal configuration and iteratively adding customizations based on team feedback represents the most effective approach to CodeRabbit adoption. As your team becomes comfortable with the platform, gradually introduce advanced features like path-specific instructions, custom tool configurations, and knowledge base integrations to maximize value.[^6][^3]

Remember that configuration is version-controlled infrastructure that should undergo the same review rigor as application code. Document configuration decisions, test changes on smaller pull requests, and maintain backups of working configurations to ensure smooth operations. By following these practices and leveraging the comprehensive configuration options available, development teams can transform code review from a bottleneck into an accelerator of software quality and developer productivity.[^22][^2]
<span style="display:none">[^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44]</span>

<div align="center">⁂</div>

[^1]: https://docs.coderabbit.ai/guides/configuration-overview

[^2]: https://docs.coderabbit.ai/getting-started/configure-coderabbit

[^3]: https://docs.coderabbit.ai/guides/initial-configuration

[^4]: https://docs.coderabbit.ai/reference-old/yaml-template

[^5]: https://docs.coderabbit.ai/reference/configuration

[^6]: https://www.abdulazizahwan.com/2024/07/exploring-coderabbit-revolutionizing-code-reviews-with-ai.html

[^7]: https://docs.coderabbit.ai/reference/review-commands

[^8]: https://docs.coderabbit.ai/guides/review-instructions

[^9]: https://docs.coderabbit.ai/reference/tools-reference

[^10]: https://docs.coderabbit.ai/tools/list

[^11]: https://www.coderabbit.ai/supported-linters

[^12]: https://docs.coderabbit.ai/tools/markdownlint

[^13]: https://docs.coderabbit.ai/tools/pylint

[^14]: https://docs.coderabbit.ai/integrations/knowledge-base

[^15]: https://docs.coderabbit.ai/guides/learnings

[^16]: https://docs.coderabbit.ai/changelog/enhanced-code-guidelines-support

[^17]: https://docs.coderabbit.ai/reference/review-commands?%3F%3F%3Futm_term=bpandey

[^18]: https://docs.coderabbit.ai/reference-old/review-commands

[^19]: https://docs.coderabbit.ai/finishing-touches/docstrings

[^20]: https://docs.coderabbit.ai/finishing-touches/unit-test-generation

[^21]: https://github.com/coderabbitai/awesome-coderabbit

[^22]: https://docs.coderabbit.ai/guides/setup-best-practices

[^23]: https://docs.coderabbit.ai/configuration/yaml-validator?%3F%3Futm_term=gitlab

[^24]: https://docs.coderabbit.ai/configuration/yaml-validator?%3F%3F%3Futm_term=lhall

[^25]: https://docs.coderabbit.ai/configuration/central-configuration

[^26]: https://www.devtoolsacademy.com/blog/coderabbit-vs-others-ai-code-review-tools/

[^27]: https://docs.coderabbit.ai/guides/custom-reports

[^28]: https://gist.github.com/bemijonathan/8bc892b1e12954e45a906e0704cff86d

[^29]: https://docs.coderabbit.ai/reference/yaml-template

[^30]: https://foojay.io/today/coderabbit-tutorial-for-java-developers/

[^31]: https://docs.coderabbit.ai/guides/scheduled-reports

[^32]: https://docs.coderabbit.ai/reference-old/configuration

[^33]: https://craftbettersoftware.com/p/code-review-with-ai-best-practices

[^34]: https://www.reddit.com/r/devops/comments/1ojc1b6/tried_coderabbit_for_automated_code_reviews_and/

[^35]: https://docs.coderabbit.ai/reference/yaml-template?%3Futm_term=mjovanovic

[^36]: https://docs.coderabbit.ai/overview/introduction

[^37]: https://javarevisited.blogspot.com/2025/10/how-i-use-coderabbit-to-level-up-my.html

[^38]: https://intodot.net/how-to-set-up-automatic-ai-reviews-in-your-github-pull-requests-with-coderabbit/

[^39]: https://www.youtube.com/watch?v=3SyUOSebG7E

[^40]: https://docs.coderabbit.ai/tools/eslint

[^41]: https://kudelskisecurity.com/research/how-we-exploited-coderabbit-from-a-simple-pr-to-rce-and-write-access-on-1m-repositories

[^42]: https://github.com/coderabbitai/coderabbit-docs/issues/265

[^43]: https://cloud.google.com/blog/products/ai-machine-learning/how-coderabbit-built-its-ai-code-review-agent-with-google-cloud-run

[^44]: https://docs.coderabbit.ai/changelog
