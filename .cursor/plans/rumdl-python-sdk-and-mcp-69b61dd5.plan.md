<!-- 69b61dd5-1618-48bf-b60c-385d1ed00274 963959b6-e196-4df2-9cd5-4ef810d44158 -->

# Implementation Plan: rumdl Python SDK and MCP Server

## Architecture Overview

Monorepo structure with two packages:

- `rumdl-python`: Core SDK wrapping rumdl CLI commands
- `rumdl-mcp`: MCP server that uses the SDK

```text
rumdl-python-mcp/
├── rumdl-python/          # SDK package
│   ├── rumdl/
│   │   ├── __init__.py
│   │   ├── client.py      # RumdlClient class
│   │   ├── types.py       # Type definitions
│   │   ├── errors.py      # Custom exceptions
│   │   └── config.py      # Configuration handling
│   ├── tests/
│   ├── README.md
│   └── pyproject.toml
├── rumdl-mcp/             # MCP server package
│   ├── rumdl_mcp/
│   │   ├── __init__.py
│   │   └── server.py      # FastMCP server
│   ├── tests/
│   ├── README.md
│   └── pyproject.toml      # Depends on rumdl-python
└── README.md              # Monorepo overview
```

## Phase 1: Python SDK Foundation

### 1.1 Project Setup

**Create `rumdl-python/pyproject.toml`:**

- Package name: `rumdl-python`
- Python >=3.11
- Dependencies: `typing-extensions`, `pydantic` (for types)
- Optional: `aiofiles` for async support

**Create `rumdl-python/rumdl/__init__.py`:**

- Export `RumdlClient` as main API
- Export types and exceptions

### 1.2 Type Definitions (`rumdl-python/rumdl/types.py`)

Define TypedDict classes for structured data:

- `Issue`: line, column, rule, message, fixable, severity
- `LintResult`: summary (total_files, files_with_issues, total_issues, fixable_issues), files (list of file results)
- `FixResult`: fixed_count, remaining_issues, files_modified
- `FormatResult`: formatted_content, issues_remaining
- `Statistics`: rule violations with counts
- `ConfigResult`: effective configuration
- `RuleInfo`: rule ID, description, category, fixable

### 1.3 Error Handling (`rumdl-python/rumdl/errors.py`)

Custom exceptions:

- `RumdlError`: Base exception
- `RumdlNotFoundError`: rumdl binary not found
- `RumdlExecutionError`: Command execution failed
- `RumdlParseError`: JSON parsing failed
- `RumdlConfigError`: Configuration issues

### 1.4 Core Client (`rumdl-python/rumdl/client.py`)

**RumdlClient class with methods:**

```python
class RumdlClient:
    def __init__(self, rumdl_path: str | None = None, config_path: str | None = None)

    # Core methods
    def lint(self, path: str, output_format: str = "json", **options) -> LintResult
    def fix(self, path: str, dry_run: bool = False, **options) -> FixResult
    def format(self, path: str, **options) -> FormatResult

    # Advanced methods
    def statistics(self, path: str) -> Statistics
    def diff(self, path: str) -> str
    def config(self, defaults_only: bool = False) -> ConfigResult
    def rules(self, rule_id: str | None = None) -> list[RuleInfo] | RuleInfo

    # Utility methods
    def _run_command(self, args: list[str], **kwargs) -> subprocess.CompletedProcess
    def _parse_json_output(self, output: str) -> dict
```

**Implementation details:**

- Use `subprocess.run()` to execute rumdl CLI
- Parse JSON output using `json.loads()`
- Handle errors with custom exceptions
- Support all rumdl CLI flags via **options
- Auto-detect rumdl binary in PATH
- Support configuration file discovery

### 1.5 Configuration Handling (`rumdl-python/rumdl/config.py`)

- Configuration discovery (`.rumdl.toml`, `pyproject.toml`)
- Configuration validation
- Default configuration values

### 1.6 SDK Tests (`rumdl-python/tests/`)

- Unit tests for each method
- Mock subprocess calls
- Test error handling
- Test JSON parsing
- Test configuration discovery

## Phase 2: MCP Server Implementation

### 2.1 Project Setup

**Create `rumdl-mcp/pyproject.toml`:**

- Package name: `rumdl-mcp`
- Dependency: `rumdl-python` (local path or published)
- Dependency: `mcp` (FastMCP)
- Entry point: `rumdl_mcp.server:main`

### 2.2 MCP Server (`rumdl-mcp/rumdl_mcp/server.py`)

**Use FastMCP pattern from codebase examples:**

```python
from mcp.server.fastmcp import FastMCP
from rumdl import RumdlClient
from pydantic import BaseModel, Field

mcp = FastMCP("rumdl_mcp")
rumdl_client = RumdlClient()

# Tool: rumdl_lint
@mcp.tool()
async def rumdl_lint(file_path: str) -> dict:
    """Lint a markdown file using rumdl. Returns structured JSON with issues."""
    return rumdl_client.lint(file_path)

# Tool: rumdl_fix
@mcp.tool()
async def rumdl_fix(file_path: str, dry_run: bool = False) -> dict:
    """Auto-fix markdown issues in a file."""
    return rumdl_client.fix(file_path, dry_run=dry_run)

# Tool: rumdl_format
@mcp.tool()
async def rumdl_format(file_path: str) -> dict:
    """Format markdown file. Returns formatted content."""
    return rumdl_client.format(file_path)

# Tool: rumdl_statistics
@mcp.tool()
async def rumdl_statistics(path: str = ".") -> dict:
    """Get rule violation statistics for AI decision-making."""
    return rumdl_client.statistics(path)

# Tool: rumdl_diff
@mcp.tool()
async def rumdl_diff(file_path: str) -> str:
    """Preview changes without modifying files."""
    return rumdl_client.diff(file_path)

# Tool: rumdl_config
@mcp.tool()
async def rumdl_config(defaults_only: bool = False) -> dict:
    """Get current rumdl configuration."""
    return rumdl_client.config(defaults_only=defaults_only)

# Tool: rumdl_rules
@mcp.tool()
async def rumdl_rules(rule_id: str | None = None) -> dict:
    """List all rules or get details for a specific rule."""
    return rumdl_client.rules(rule_id)

# Tool: rumdl_profile
@mcp.tool()
async def rumdl_profile(path: str = ".") -> dict:
    """Get performance profiling information."""
    # Uses rumdl check --profile
    result = rumdl_client._run_command(["rumdl", "check", "--profile", path])
    return {"profile_data": result.stdout}

if __name__ == "__main__":
    mcp.run()
```

**Tool descriptions:**

- Rich descriptions for AI understanding
- Include examples in docstrings
- Specify parameter types clearly
- Document return value structure

### 2.3 MCP Server Tests (`rumdl-mcp/tests/`)

- Test tool registration
- Test tool execution (mock SDK calls)
- Test error handling
- Test MCP protocol compliance

## Phase 3: Documentation and Examples

### 3.1 SDK Documentation (`rumdl-python/README.md`)

- Installation instructions
- Quick start guide
- API reference
- Examples for each method
- Error handling guide

### 3.2 MCP Server Documentation (`rumdl-mcp/README.md`)

- Installation instructions
- Claude Desktop configuration
- Tool descriptions
- Usage examples
- Integration patterns

### 3.3 Monorepo README

- Overview of both packages
- Installation instructions
- Development setup
- Contributing guidelines

## Phase 4: Publishing and Distribution

### 4.1 PyPI Publishing

- Publish `rumdl-python` to PyPI
- Publish `rumdl-mcp` to PyPI (depends on rumdl-python)
- Version management
- Release notes

### 4.2 GitHub Repository

- Repository setup
- GitHub Actions for CI/CD
- Automated testing
- Release automation

## Implementation Details

### Key Design Decisions

1. **CLI Wrapper Approach**: SDK wraps rumdl CLI commands (not LSP) for simplicity
2. **Synchronous First**: Initial implementation synchronous, async can be added later
3. **Type Safety**: Use TypedDict and Pydantic for type safety
4. **Error Handling**: Comprehensive error handling with custom exceptions
5. **Configuration**: Support rumdl's config discovery mechanism

### Testing Strategy

- Unit tests for SDK (mock subprocess)
- Integration tests with real rumdl binary
- MCP server tests (mock SDK)
- End-to-end tests with Claude Desktop

### Dependencies

**rumdl-python:**

- `typing-extensions` (for Python <3.11 compatibility)
- `pydantic` (for validation, optional)

**rumdl-mcp:**

- `rumdl-python` (local or PyPI)
- `mcp` (FastMCP)

## Success Criteria

1. SDK provides clean Python API for all rumdl operations
2. MCP server exposes all SDK functionality as tools
3. Both packages have comprehensive tests (>80% coverage)
4. Documentation is complete with examples
5. Packages can be installed and used independently
6. MCP server works with Claude Desktop

## Future Enhancements (Post-MVP)

- Async support in SDK
- Caching layer for performance
- Batch operations
- Watch mode support
- Additional MCP tools based on feedback

### To-dos

- [ ] Create monorepo structure with rumdl-python and rumdl-mcp directories
- [ ] Define TypedDict types in rumdl-python/rumdl/types.py (Issue, LintResult, FixResult, etc.)
- [ ] Create custom exception classes in rumdl-python/rumdl/errors.py
- [ ] Implement RumdlClient class with lint(), fix(), format() methods in rumdl-python/rumdl/client.py
- [ ] Add advanced methods to SDK: statistics(), diff(), config(), rules(), profile()
- [ ] Implement configuration handling in rumdl-python/rumdl/config.py
- [ ] Write comprehensive tests for SDK in rumdl-python/tests/
- [ ] Create rumdl-mcp package structure and pyproject.toml with rumdl-python dependency
- [ ] Implement core MCP tools: rumdl_lint, rumdl_fix, rumdl_format in rumdl-mcp/rumdl_mcp/server.py
- [ ] Implement advanced MCP tools: rumdl_statistics, rumdl_diff, rumdl_config, rumdl_rules, rumdl_profile
- [ ] Write tests for MCP server in rumdl-mcp/tests/
- [ ] Write comprehensive SDK documentation in rumdl-python/README.md with API reference and examples
- [ ] Write MCP server documentation in rumdl-mcp/README.md with Claude Desktop setup instructions
- [ ] Create monorepo README.md with overview and development setup instructions
