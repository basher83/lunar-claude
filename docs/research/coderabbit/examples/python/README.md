# Python Configuration Examples

> Real-world CodeRabbit configuration examples for Python projects.

## Available Examples

### 1. coderabbit-python-portal.yaml

**Comprehensive multi-language Python project configuration**

- **Size**: ~11KB
- **Complexity**: High
- **Use Case**: Large projects with Python, BASH, and documentation

**Highlights:**

- Extensive review instructions for Python, BASH, and documentation
- Multiple tool integrations (Ruff, ShellCheck, LanguageTool, markdownlint, yamllint)
- Custom labeling system
- Path-specific instructions for various file types
- Documentation standards (RFC-style references)
- Test code review guidelines

### 2. coderabbit-wg-utilities.yaml

**Focused Python utilities library configuration**

- **Size**: ~1.3KB
- **Complexity**: Medium
- **Use Case**: Python utility libraries

**Highlights:**

- PEP 8 style guide enforcement
- Performance optimization focus
- Directory-specific path filters
- Functional efficiency evaluation

### 3. pytest-google-style-config.yaml

**Google style guide + Pytest testing configuration**

- **Size**: ~1.3KB
- **Complexity**: Medium
- **Use Case**: Projects following Google Python style guide with Pytest

**Highlights:**

- Google Python style guide compliance
- Pytest testing framework best practices
- Docstring verification
- API dependency tracking
- Multiple base branch support

### 4. python-ruff-config.yaml

**Minimal Ruff-focused configuration**

- **Size**: ~708 bytes
- **Complexity**: Low
- **Use Case**: Quick setup with Ruff linter

**Highlights:**

- Japanese language reviews
- Assertive review profile
- Ruff linter focus
- Minimal configuration

## Quick Start

1. **Review the examples** to find one that matches your project
2. **Copy to your repository root**:
   ```bash
   cp python-ruff-config.yaml .coderabbit.yaml
   ```

3. **Customize** for your project needs
4. **Validate** using CodeRabbit's YAML validator

## Comparison Table

| Feature | python-portal | wg-utilities | pytest-google | ruff-config |
|---------|--------------|--------------|---------------|-------------|
| Review Profile | chill | N/A | chill | assertive |
| Language | en | en | en | ja |
| Path Instructions | ✅ Extensive | ✅ Focused | ✅ Style-focused | ✅ Minimal |
| Tool Config | ✅ Multiple | ❌ None | ❌ None | ✅ Ruff |
| Labeling | ✅ Custom | ❌ None | ❌ None | ❌ None |
| Documentation Focus | ✅ High | ❌ None | ✅ Medium | ❌ None |
| Testing Focus | ✅ High | ❌ None | ✅ High (Pytest) | ❌ None |

## Choosing the Right Example

- **New to CodeRabbit?** → Start with `python-ruff-config.yaml`
- **Large multi-language project?** → Use `coderabbit-python-portal.yaml`
- **Utility library?** → Use `coderabbit-wg-utilities.yaml`
- **Google style + Pytest?** → Use `pytest-google-style-config.yaml`

## Source

All examples are from the [awesome-coderabbit](https://github.com/coderabbitai/awesome-coderabbit) repository:

- [Python Configs Directory](https://github.com/coderabbitai/awesome-coderabbit/tree/main/configs/python)
