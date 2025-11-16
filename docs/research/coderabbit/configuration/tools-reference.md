# CodeRabbit Tools Reference

> Complete reference for all CodeRabbit supported tools and their configuration options, organized by category.

## Overview

CodeRabbit integrates with 40+ third-party linters, security analyzers, and CI/CD tools to enhance code reviews. These tools run automatically in secure sandboxed environments, providing detailed feedback and 1-click fixes for common issues.

**Note:** Tool integration is available exclusively with CodeRabbit Pro plan.

## Tool Categories

- **Code Quality**: Linters and formatters for various languages
- **Code Security**: Security vulnerability scanners
- **CI/CD**: Pipeline and workflow validators
- **Infrastructure**: Infrastructure-as-Code analyzers
- **Grammar & Style**: Grammar and style checkers

## Configuration Basics

### Enable/Disable Tools

```yaml
reviews:
  tools:
    tool-name:
      enabled: true  # or false
```

### Tool-Specific Configuration

Many tools support custom configuration files:

```yaml
reviews:
  tools:
    tool-name:
      enabled: true
      config_file: "path/to/config"  # Optional custom config file
```

### Tool Profiles

CodeRabbit offers two review profiles that control tool strictness:

- **Chill**: Focuses on critical issues, reduces noise from minor style violations
- **Assertive**: Provides comprehensive feedback including style and best practice suggestions

Configure via `reviews.profile: "chill"` or `reviews.profile: "assertive"`.

## Code Quality Tools

### JavaScript/TypeScript

#### ESLint

**Description:** Static code analysis tool for JavaScript files
**Version:** Latest
**Category:** Code Quality

```yaml
reviews:
  tools:
    eslint:
      enabled: true
```

**Configuration:** Automatically uses `.eslintrc.js`, `.eslintrc.json`, `eslint.config.js`, or `package.json` eslintConfig field.

#### Biome

**Description:** Fast formatter, linter, and analyzer for web projects
**Version:** v2.1.2
**Category:** Code Quality
**Supports:** JavaScript, TypeScript, JSX, JSON, CSS

```yaml
reviews:
  tools:
    biome:
      enabled: true
```

**Configuration:** Automatically uses `biome.json` or `biome.jsonc`.

#### Oxlint (oxc)

**Description:** JavaScript/TypeScript linter for OXC written in Rust
**Version:** v1.25.0
**Category:** Code Quality
**Supports:** JavaScript, TypeScript, JSX

```yaml
reviews:
  tools:
    oxc:
      enabled: true
```

### Python

#### Ruff

**Description:** Python linter and code formatter
**Version:** v0.14.3
**Category:** Code Quality

```yaml
reviews:
  tools:
    ruff:
      enabled: true
      config_file: "pyproject.toml"  # Optional
```

**Configuration:** Automatically uses `pyproject.toml`, `ruff.toml`, or `.ruff.toml`.

#### Pylint

**Description:** Python static code analysis tool
**Version:** v4.0.2
**Category:** Code Quality

```yaml
reviews:
  tools:
    pylint:
      enabled: true
```

**Configuration:** Automatically uses `.pylintrc`, `pylintrc`, `setup.cfg`, or `pyproject.toml`.

#### Flake8

**Description:** Python linter that wraps PyFlakes, pycodestyle and McCabe script
**Version:** v7.3.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    flake8:
      enabled: true
```

**Configuration:** Automatically uses `.flake8`, `setup.cfg`, or `tox.ini`.

### Go

#### golangci-lint

**Description:** Fast linters runner for Go
**Version:** v2.5.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    golangci-lint:
      enabled: true
      config_file: ".golangci.yml"  # Optional
```

**Configuration files supported:**
- `.golangci.yml`
- `.golangci.yaml`
- `.golangci.toml`
- `.golangci.json`
- User-defined via `config_file`

### Rust

#### Clippy

**Description:** Collection of lints to catch common mistakes and improve Rust code
**Version:** Latest
**Category:** Code Quality

```yaml
reviews:
  tools:
    clippy:
      enabled: true
```

**Configuration:** Automatically uses `clippy.toml` or `Cargo.toml` clippy section.

### Ruby

#### RuboCop

**Description:** Ruby static code analyzer (linter) and code formatter
**Version:** v1.81.7
**Category:** Code Quality

```yaml
reviews:
  tools:
    rubocop:
      enabled: true
```

**Configuration:** Automatically uses `.rubocop.yml`, `.rubocop.yaml`, or `.rubocop.yml.rb`.

#### Brakeman

**Description:** Static analysis security vulnerability scanner for Ruby on Rails applications
**Version:** v7.1.0
**Category:** Code Security

```yaml
reviews:
  tools:
    brakeman:
      enabled: true
```

**Configuration:** Automatically uses `config/brakeman.yml` or `config/brakeman.ignore`.

### PHP

#### PHPStan

**Description:** Tool to analyze PHP code
**Version:** v2.1.31
**Category:** Code Quality

```yaml
reviews:
  tools:
    phpstan:
      enabled: true
      level: "max"  # Options: "default", "0"-"9", "max"
```

**Configuration:** Requires `phpstan.neon` or `phpstan.neon.dist` with `paths:` parameter. Level setting ignored if config file specifies level.

#### PHPMD

**Description:** Tool to find potential problems in PHP code
**Version:** v2.15.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    phpmd:
      enabled: true
```

**Configuration:** Automatically uses `phpmd.xml` or `phpmd.xml.dist`.

#### PHPCS (PHP CodeSniffer)

**Description:** PHP linter and coding standard checker
**Version:** v3.7.2
**Category:** Code Quality

```yaml
reviews:
  tools:
    phpcs:
      enabled: true
```

**Configuration:** Automatically uses `phpcs.xml`, `phpcs.xml.dist`, or `.phpcs.xml`.

### Java

#### PMD

**Description:** Extensible multilanguage static code analyzer, mainly for Java
**Version:** v7.18.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    pmd:
      enabled: true
      config_file: "/pmd-config/*.yml"  # Optional
```

**Configuration:** Automatically uses `pmd.xml` or custom config file.

### Kotlin

#### Detekt

**Description:** Static code analysis tool for Kotlin files
**Version:** v1.23.8
**Category:** Code Quality

```yaml
reviews:
  tools:
    detekt:
      enabled: true
      config_file: "detekt.yml"  # Optional
```

**Configuration:** Automatically uses `detekt.yml` or `detekt.yaml`.

### Swift

#### SwiftLint

**Description:** Swift linter
**Version:** v0.57.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    swiftlint:
      enabled: true
      config_file: ".swiftlint.yml"  # Optional
```

**Configuration:** Automatically uses `.swiftlint.yml` or `.swiftlint.yaml`.

### C/C++

#### Cppcheck

**Description:** Static code analysis tool for C and C++ programming languages
**Version:** v2.18.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    cppcheck:
      enabled: true
```

**Configuration:** Automatically uses `cppcheck.xml` or command-line options.

#### Clang

**Description:** Static analysis on C and C++ code
**Version:** v14.0.6
**Category:** Code Quality

```yaml
reviews:
  tools:
    clang:
      enabled: true
```

### Markdown

#### markdownlint

**Description:** Static analysis tool to enforce standards and consistency for Markdown files
**Version:** v0.18.1
**Category:** Code Quality

```yaml
reviews:
  tools:
    markdownlint:
      enabled: true
```

**Configuration:** Automatically uses `.markdownlint.json`, `.markdownlint.yaml`, or `.markdownlint.yml`.

### YAML

#### YAMLlint

**Description:** Linter for YAML files
**Version:** v1.37.1
**Category:** Code Quality

```yaml
reviews:
  tools:
    yamllint:
      enabled: true
```

**Configuration:** Automatically uses `.yamllint`, `.yamllint.yml`, or `.yamllint.yaml`.

### Shell Scripts

#### ShellCheck

**Description:** Static analysis tool that finds bugs in shell scripts
**Version:** v0.11.0
**Category:** Code Quality
**Supports:** sh, bash, ksh, dash

```yaml
reviews:
  tools:
    shellcheck:
      enabled: true
```

**Configuration:** Automatically uses `.shellcheckrc` or command-line options.

### Makefiles

#### checkmake

**Description:** Linter for Makefiles
**Version:** v0.2.2
**Category:** Code Quality

```yaml
reviews:
  tools:
    checkmake:
      enabled: true
```

### HTML

#### HTMLHint

**Description:** Static code analysis tool for HTML files
**Version:** v1.7.1
**Category:** Code Quality

```yaml
reviews:
  tools:
    htmlhint:
      enabled: true
```

**Configuration:** Automatically uses `.htmlhintrc` or `.htmlhint.json`.

### SQL

#### SQLFluff

**Description:** Open source, dialect-flexible and configurable SQL linter
**Version:** v3.5.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    sqlfluff:
      enabled: true
```

**Configuration:** Automatically uses `.sqlfluff` or `pyproject.toml`.

### Protobuf

#### Buf

**Description:** Linting for Protobuf files
**Version:** v1.59.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    buf:
      enabled: true
```

**Configuration:** Automatically uses `buf.yaml` or `buf.yml`.

### Rego (Open Policy Agent)

#### Regal

**Description:** Linter and language server for Rego
**Version:** v0.36.1
**Category:** Code Quality

```yaml
reviews:
  tools:
    regal:
      enabled: true
```

### Lua

#### Luacheck

**Description:** Lua code linting to ensure code quality
**Version:** v1.2.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    luacheck:
      enabled: true
```

**Configuration:** Automatically uses `.luacheckrc` or `.luacheckrc.lua`.

### Prisma

#### Prisma Lint

**Description:** Linter for Prisma schema files
**Version:** v0.10.3
**Category:** Code Quality

```yaml
reviews:
  tools:
    prismaLint:
      enabled: true
```

**Configuration files supported:**
- `.prismalintrc.json`
- `.prismalintrc`
- `.prismalintrc.js`
- `.prismalintrc.yaml`
- `.prismalintrc.yml`
- `prismalint.config.js`
- User-defined via `config_file`

**Note:** By default looks for schema at `prisma/schema.prisma`. Uses custom schema path from `package.json` if specified.

### Shopify

#### Shopify Theme Check

**Description:** Linter for Shopify themes
**Version:** CLI 3.84.2, Theme 3.58.2
**Category:** Code Quality

```yaml
reviews:
  tools:
    shopifyThemeCheck:
      enabled: true
```

### Pattern Matching

#### ast-grep

**Description:** Code analysis tool using abstract syntax tree patterns
**Version:** v0.39.7
**Category:** Code Quality

```yaml
reviews:
  tools:
    ast-grep:
      enabled: true
      rule_dirs: ["rules/"]           # List of rules directories
      util_dirs: ["utils/"]           # List of utils directories
      essential_rules: true            # Use ast-grep essentials package
      packages: ["common-patterns"]   # Predefined packages
```

## Code Security Tools

### Gitleaks

**Description:** Secret scanner
**Version:** v8.28.0
**Category:** Code Security

```yaml
reviews:
  tools:
    gitleaks:
      enabled: true
```

**Configuration:** Automatically uses `.gitleaksignore` or `.gitleaks.toml`.

### Semgrep

**Description:** Static analysis tool for security vulnerabilities and code quality issues
**Version:** v1.142.0
**Category:** Code Security

```yaml
reviews:
  tools:
    semgrep:
      enabled: true
      config_file: ".semgrep.yml"  # Optional
```

**Configuration:** Automatically uses `.semgrep.yml` or custom config file.

### OSV Scanner

**Description:** Tool for vulnerability package scanning
**Version:** v2.2.4
**Category:** Code Security

```yaml
reviews:
  tools:
    osvScanner:
      enabled: true
```

### Brakeman

**Description:** Static analysis security vulnerability scanner for Ruby on Rails applications
**Version:** v7.1.0
**Category:** Code Security

```yaml
reviews:
  tools:
    brakeman:
      enabled: true
```

## Infrastructure Tools

### Checkov

**Description:** Static code analysis tool for infrastructure-as-code files
**Version:** v3.2.334
**Category:** Infrastructure
**Supports:** Terraform, CloudFormation, Kubernetes, Helm, Docker, Azure ARM, Ansible

```yaml
reviews:
  tools:
    checkov:
      enabled: true
```

**Configuration:** Automatically uses `.checkov.yml` or `.checkov.yaml`.

### Hadolint

**Description:** Dockerfile linter
**Version:** v2.14.0
**Category:** Infrastructure

```yaml
reviews:
  tools:
    hadolint:
      enabled: true
```

**Configuration:** Automatically uses `.hadolint.yaml` or `.hadolint.yml`.

## CI/CD Tools

### GitHub Actions

#### actionlint

**Description:** Static checker for GitHub Actions workflow files
**Version:** v1.7.8
**Category:** CI/CD

```yaml
reviews:
  tools:
    actionlint:
      enabled: true
```

### CircleCI

**Description:** Static checker for CircleCI config files
**Version:** v0.1.33494
**Category:** CI/CD

```yaml
reviews:
  tools:
    circleci:
      enabled: true
```

**Configuration:** Automatically uses `.circleci/config.yml`.

### Pipeline Remediation

**Description:** CI/CD failure remediation tool
**Category:** CI/CD
**Supports:** Azure DevOps Pipelines, CircleCI, GitLab Pipelines, GitHub Actions

```yaml
reviews:
  tools:
    # Automatically enabled for supported CI/CD platforms
```

## Grammar & Style Tools

### LanguageTool

**Description:** Style and grammar checker for 30+ languages
**Version:** Latest
**Category:** Grammar & Style
**Supports:** Plaintext, Markdown

```yaml
reviews:
  tools:
    languagetool:
      enabled: true
      enabled_rules: ["EN_QUOTES"]           # IDs of rules to enable
      disabled_rules: ["EN_UNPAIRED_BRACKETS"] # IDs of rules to disable
      enabled_categories: ["TYPOS"]          # IDs of categories to enable
      disabled_categories: ["CASING"]        # IDs of categories to disable
      enabled_only: false                    # Only use enabled rules/categories
      level: "default"                      # Options: "default", "picky"
```

**Note:** `EN_UNPAIRED_BRACKETS` and `EN_UNPAIRED_QUOTES` are always disabled. `TYPOS`, `TYPOGRAPHY`, and `CASING` categories are always disabled.

### Dotenv Linter

**Description:** Tool for checking and fixing .env files
**Version:** v4.0.0
**Category:** Code Quality

```yaml
reviews:
  tools:
    dotenvLint:
      enabled: true
```

**Files:** Runs on `**/.env` and `**/.env.*` patterns. Does not run on files that don't start with `.env` (e.g., `test.env`).

**Configuration:** Uses default settings if no configuration file found.

## GitHub Checks Integration

### GitHub Checks

**Description:** Integration with GitHub Checks API
**Category:** CI/CD

```yaml
reviews:
  tools:
    github-checks:
      enabled: true
      timeout_ms: 90000  # Wait time in milliseconds (default: 90s, max: 15min)
```

**Configuration:**
- `timeout_ms`: Time to wait for all GitHub Checks to conclude
- Default: 90000ms (90 seconds)
- Maximum: 900000ms (15 minutes)

## Complete Tool List by Category

### Code Quality (30+ tools)

- **JavaScript/TypeScript**: ESLint, Biome, Oxlint
- **Python**: Ruff, Pylint, Flake8
- **Go**: golangci-lint
- **Rust**: Clippy
- **Ruby**: RuboCop
- **PHP**: PHPStan, PHPMD, PHPCS
- **Java**: PMD
- **Kotlin**: Detekt
- **Swift**: SwiftLint
- **C/C++**: Cppcheck, Clang
- **Markdown**: markdownlint
- **YAML**: YAMLlint
- **Shell**: ShellCheck
- **Makefiles**: checkmake
- **HTML**: HTMLHint
- **SQL**: SQLFluff
- **Protobuf**: Buf
- **Rego**: Regal
- **Lua**: Luacheck
- **Prisma**: Prisma Lint
- **Shopify**: Shopify Theme Check
- **Pattern Matching**: ast-grep
- **Environment Files**: Dotenv Linter

### Code Security (4 tools)

- Gitleaks (secret scanning)
- Semgrep (security vulnerabilities)
- OSV Scanner (vulnerability scanning)
- Brakeman (Ruby on Rails security)

### Infrastructure (2 tools)

- Checkov (IaC analysis)
- Hadolint (Dockerfile linting)

### CI/CD (3 tools)

- actionlint (GitHub Actions)
- CircleCI (CircleCI config)
- Pipeline Remediation (multi-platform)

### Grammar & Style (1 tool)

- LanguageTool (grammar and style checking)

## Tool Configuration Best Practices

1. **Enable relevant tools**: Only enable tools for languages/frameworks you use
2. **Use custom configs**: Provide tool-specific configuration files when needed
3. **Profile selection**: Use "chill" for less noise, "assertive" for comprehensive feedback
4. **Security first**: Always enable security tools (Gitleaks, Semgrep, OSV Scanner)
5. **Infrastructure**: Enable Checkov and Hadolint for infrastructure projects

## Default Behavior

By default, CodeRabbit considers all available tools. To disable specific tools:

```yaml
reviews:
  tools:
    tool-name:
      enabled: false
```

## Tool Versions

Tool versions are automatically managed by CodeRabbit and updated regularly. Version information is provided for reference but doesn't need to be configured.

## Related Resources

- [Configuration Guide](./yaml-configuration-guide.md) - Complete YAML configuration guide
- [GitHub Commands Reference](../referance/github-commands.md) - PR command reference
- [CodeRabbit Tools Documentation](https://docs.coderabbit.ai/tools/list) - Official tools list
- [Tools Reference Schema](https://docs.coderabbit.ai/reference/tools-reference) - Complete schema reference
