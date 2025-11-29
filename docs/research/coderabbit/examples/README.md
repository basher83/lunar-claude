# CodeRabbit Configuration Examples

> Real-world CodeRabbit configuration examples from the [awesome-coderabbit](https://github.com/coderabbitai/awesome-coderabbit) repository.

## Overview

This directory contains practical, production-ready CodeRabbit configuration examples organized by language and use case. These examples demonstrate various configuration patterns and best practices for different project types.

## Python Examples

### coderabbit-python-portal.yaml

**Use Case:** Comprehensive Python project with multi-language support (Python, BASH, Shell scripts)

**Key Features:**

- Extensive review instructions for Python, BASH, and documentation
- Multiple tool integrations (Ruff, ShellCheck, LanguageTool, markdownlint, yamllint)
- Custom labeling instructions for different file types
- Path-specific instructions for README, Python files, tests, requirements files, and GitHub workflows
- Documentation review requirements including RFC-style references
- Test code review guidelines
- Copyright year checking

**Best For:**

- Large Python projects with multiple file types
- Projects requiring strict documentation standards
- Projects with BASH/shell script components
- Projects needing comprehensive code review coverage

**Source:** [awesome-coderabbit/python/coderabbit-python-portal.yaml](https://github.com/coderabbitai/awesome-coderabbit/blob/main/configs/python/coderabbit-python-portal.yaml)

### coderabbit-wg-utilities.yaml

**Use Case:** Focused Python utilities library

**Key Features:**

- PEP 8 style guide enforcement
- Performance optimization focus
- Path filters for specific library directory (`wg_utilities/**/*.py`)
- Functional efficiency evaluation
- Variable and function naming assessment
- Logical error detection

**Best For:**

- Python utility libraries
- Performance-critical codebases
- Projects requiring strict PEP 8 compliance
- Focused code review on specific directories

**Source:** [awesome-coderabbit/python/coderabbit-wg-utilities.yaml](https://github.com/coderabbitai/awesome-coderabbit/blob/main/configs/python/coderabbit-wg-utilities.yaml)

### pytest-google-style-config.yaml

**Use Case:** Python project following Google style guide with Pytest testing

**Key Features:**

- Google Python style guide compliance
- Pytest testing framework best practices
- Docstring verification and updates
- API dependency tracking
- TODO comment completion
- Test coverage requirements
- Multiple base branch support (`develop`, `feat/*`)

**Best For:**

- Projects following Google Python style guide
- Projects using Pytest for testing
- Projects requiring comprehensive test coverage
- Projects with multiple feature branches

**Source:** [awesome-coderabbit/python/pytest-google-style-config.yaml](https://github.com/coderabbitai/awesome-coderabbit/blob/main/configs/python/pytest-google-style-config.yaml)

### python-ruff-config.yaml

**Use Case:** Minimal Python configuration focused on Ruff linter

**Key Features:**

- Japanese language reviews (`language: "ja"`)
- Assertive review profile
- Ruff linter focus
- Simple path filters
- WIP and "DO NOT MERGE" keyword filtering

**Best For:**

- Japanese-language projects
- Projects primarily using Ruff for linting
- Minimal configuration needs
- Quick setup scenarios

**Source:** [awesome-coderabbit/python/python-ruff-config.yaml](https://github.com/coderabbitai/awesome-coderabbit/blob/main/configs/python/python-ruff-config.yaml)

## Using These Examples

### 1. Choose an Example

Select the example that best matches your project:

- **Comprehensive projects**: `coderabbit-python-portal.yaml`
- **Utility libraries**: `coderabbit-wg-utilities.yaml`
- **Google style + Pytest**: `pytest-google-style-config.yaml`
- **Minimal setup**: `python-ruff-config.yaml`

### 2. Customize for Your Project

Copy the example to your repository root as `.coderabbit.yaml` and customize:

```bash
# Copy example
cp docs/research/coderabbit/examples/python/coderabbit-python-portal.yaml .coderabbit.yaml

# Edit for your project
vim .coderabbit.yaml

```

### 3. Adjust Key Settings

- **Language**: Change `language` field if needed
- **Path filters**: Update `path_filters` to match your project structure
- **Path instructions**: Modify `path_instructions` for your specific needs
- **Tools**: Enable/disable tools based on your tech stack
- **Review profile**: Choose `chill` or `assertive` based on team preferences

### 4. Test Your Configuration

Use CodeRabbit's YAML validator:

- Online: https://docs.coderabbit.ai/configuration/yaml-validator
- VS Code: Install YAML extension with schema validation

## Configuration Patterns

### Pattern 1: Comprehensive Multi-Language Project

```yaml
# See: coderabbit-python-portal.yaml
reviews:
  instructions: >-
    # Multiple language support
    # Extensive path instructions
    # Custom labeling
  path_instructions:
    - path: "**/*.py"
      instructions: "Python-specific instructions"
    - path: "**/*.sh"
      instructions: "BASH-specific instructions"

```

### Pattern 2: Focused Library Configuration

```yaml
# See: coderabbit-wg-utilities.yaml
reviews:
  path_filters:
    - "library_name/**/*.py"  # Focus on specific directory
  path_instructions:
    - path: "library_name/**/*.py"
      instructions: "Library-specific review guidelines"

```

### Pattern 3: Style Guide + Testing Framework

```yaml
# See: pytest-google-style-config.yaml
reviews:
  path_instructions:
    - path: "src/**/*.py"
      instructions: "Google style guide compliance"
    - path: "tests/**/*"
      instructions: "Pytest best practices"

```

### Pattern 4: Minimal Configuration

```yaml
# See: python-ruff-config.yaml
reviews:
  profile: "assertive"
  tools:
    ruff:
      enabled: true

```

## Common Customizations

### Adding Your Own Path Instructions

```yaml
reviews:
  path_instructions:
    - path: "your/path/**/*.py"
      instructions: "Your custom review instructions here"

```

### Enabling Additional Tools

```yaml
reviews:
  tools:
    ruff:
      enabled: true
    gitleaks:
      enabled: true
    checkov:
      enabled: true

```

### Custom Labeling

```yaml
reviews:
  labeling_instructions:
    - label: "your-label"
      instructions: "When to apply this label"

```

## Related Resources

- [YAML Configuration Guide](../configuration/yaml-configuration-guide.md) - Complete configuration reference
- [Tools Reference](../configuration/tools-reference.md) - All supported tools
- [GitHub Commands Reference](../referance/github-commands.md) - PR command reference
- [Awesome CodeRabbit](https://github.com/coderabbitai/awesome-coderabbit) - More examples and resources

## Contributing

These examples are sourced from the [awesome-coderabbit](https://github.com/coderabbitai/awesome-coderabbit) repository. To contribute your own examples:

1. Add your configuration to the awesome-coderabbit repository
2. Submit a PR with your example
3. Once merged, we can update this directory

## License

These examples are provided as-is from the awesome-coderabbit repository. Please refer to the original repository for license information.
