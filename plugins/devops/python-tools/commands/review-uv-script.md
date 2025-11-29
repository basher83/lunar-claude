---
description: Review uv Python script for PEP 723 compliance and best practices
argument-hint: [script-path]
allowed-tools: Read, Grep, Glob
---

# UV Python Script Review

Review the uv Python script at `$ARGUMENTS` against best practices.

## Script to Review

@$ARGUMENTS

## Confidence Scoring

Rate each potential issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0-25 | Likely false positive or stylistic preference |
| 26-50 | Minor nitpick, not explicitly in best practices |
| 51-75 | Valid but low-impact issue |
| 76-90 | Important issue requiring attention |
| 91-100 | Critical bug or explicit best practice violation |

**Only report issues with confidence ≥ 80.** Quality over quantity.

## Review Categories

### 1. PEP 723 Metadata Block (Critical)

**Required elements:**

- Has `# /// script` opening marker (exactly `/// script`, not `/// scripts` or `//`)
- Has `# ///` closing marker
- `requires-python` is specified (e.g., `>=3.11`)
- `dependencies` array is present (even if empty)
- Each TOML line starts with `#`

**Forbidden patterns:**

- `[tool.uv.metadata]` - Invalid field, causes runtime error
- Custom top-level fields (`author`, `version`, `description`) - Only `requires-python` and `dependencies` allowed
- Missing `#` prefix on TOML lines

**Valid [tool.uv] usage** (without `.metadata`):

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# [tool.uv]
# exclude-newer = "2025-01-01T00:00:00Z"  # Valid
# ///
```

### 2. Shebang Line (Important)

- Has proper shebang: `#!/usr/bin/env -S uv run --script`
- Consider `--quiet` flag for production scripts
- Shebang must be first line (before metadata block)

### 3. Dependency Management (Important)

**Version pinning:**

- Use `>=X.Y.Z` for utilities (allows updates)
- Use `==X.Y.Z` only for deployment scripts requiring reproducibility
- No bare package names (`"httpx"` → `"httpx>=0.27.0"`)

**Heavy dependencies flag:**

- Flag `tensorflow`, `torch`, `transformers` - Too heavy for single-file scripts
- Suggest using proper uv project instead

### 4. Documentation (Medium)

- Module docstring present after metadata block
- Docstring includes: purpose, usage, examples
- Metadata (team, author, version) in docstring, NOT in TOML

### 5. Silent Failure Detection (Critical)

Hunt for error handling that hides failures:

**Absolutely Forbidden:**

- Empty `except:` blocks
- `except Exception: pass` or `except: pass`
- Catching exceptions without logging or re-raising
- Returning `None`/default on error without indication

**Scrutinize Each Handler:**

- Does the except block catch only expected error types?
- Could this catch block accidentally suppress unrelated errors?
- Is the error logged with sufficient context?
- Does the user receive clear, actionable feedback?

**Common Python Silent Failure Patterns:**

```python
# BAD: Silent swallowing
try:
    result = api_call()
except:
    result = None  # User has no idea it failed

# BAD: Overly broad catch
try:
    data = json.loads(response)
except Exception:
    pass  # Hides syntax errors, type errors, etc.

# GOOD: Specific handling with feedback
try:
    data = json.loads(response)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON response: {e}", file=sys.stderr)
    sys.exit(1)
```

### 6. Security Patterns (Critical)

**Secrets Management:**

- No hardcoded secrets (API keys, passwords, tokens, database URLs)
- Use `os.getenv()` with validation for missing values
- Consider keyring or Infisical for production

**Command Injection:**

- Flag `subprocess.run(..., shell=True)` with user input
- Prefer list form: `subprocess.run(["cmd", arg1, arg2])`
- Validate all user-provided arguments

**Path Traversal:**

- Flag paths containing `..`
- Use `Path.resolve()` and `.relative_to()` for validation
- Validate paths are within expected directories

**JSON Security:**

- **NEVER** use `eval()` for JSON parsing - use `json.loads()`
- Use `json.dumps()` for serialization (prevents injection)
- Always specify `encoding="utf-8"` for file operations

**Network Security:**

- HTTPS-only for external requests
- Certificate verification enabled (`verify=True`)
- Timeouts on all external calls

### 7. Type Design Analysis (Medium)

**Type Hints Quality (1-10):**

- Are parameters typed?
- Are return types specified?
- Are complex types properly annotated (Optional, Union, TypedDict)?

**Common Issues:**

- `def foo(data):` → `def foo(data: dict[str, Any]) -> bool:`
- Missing `Optional[]` for nullable parameters
- Using `Any` when specific type is known

**Suppression patterns:**

- Check `# type: ignore` comments - are they justified?
- Check `# noqa` comments - are they necessary?

### 8. Code Quality (Medium)

**Clarity over brevity:**

- Avoid nested ternary operators
- Avoid overly dense one-liners
- Functions do one thing
- Variable names are descriptive

**Script complexity:**

- Script exceeds 500 lines → Should be a uv project
- 15+ dependencies → Should be a uv project
- Multiple modules needed → Should be a uv project

**Platform compatibility:**

- Platform-specific imports without guards (e.g., `import pwd` on Windows)
- Use `sys.platform` checks for platform-specific code

### 9. External Operations (Important)

**File operations:**

- Always use `encoding="utf-8"` for `open()`
- Check file size before reading large files
- Use context managers (`with` statements)

**Subprocess calls:**

- Include `timeout` parameter
- Use `capture_output=True` for error handling
- Check `returncode` or use `check=True`

**HTTP requests:**

- Include timeout: `httpx.get(url, timeout=10.0)`
- Call `response.raise_for_status()`
- Handle specific exceptions (HTTPStatusError, RequestError)

## Output Format

```markdown
## Review: [filename]

**Overall: [PASS/NEEDS WORK]** - [Brief assessment]

### Critical Issues (confidence ≥90)

| Issue | Location | Confidence | Fix |
|-------|----------|------------|-----|
| [Description] | `file.py:42` | 95 | [Specific fix] |

### Important Issues (confidence 80-89)

| Issue | Location | Confidence | Fix |
|-------|----------|------------|-----|
| [Description] | `file.py:15` | 85 | [Specific fix] |

### Suggestions (confidence 70-79, optional)

- [Suggestion with rationale]

### Strengths

- [What the script does well]

## Recommended Action

1. [First priority fix]
2. [Second priority fix]
```

## Anti-Pattern Quick Reference

| Anti-Pattern | Detection | Severity |
|--------------|-----------|----------|
| `[tool.uv.metadata]` | In script block | Critical |
| Custom TOML fields | `author`, `version` at top level | Critical |
| Wrong marker | `/// scripts`, `//`, missing closer | Critical |
| Missing `#` prefix | TOML lines without `#` | Critical |
| `eval()` for JSON | `eval(json_string)` | Critical |
| Hardcoded secrets | API keys, passwords in code | Critical |
| Bare `except:` | Empty or pass-only catch | Critical |
| `shell=True` + user input | Command injection risk | Critical |
| Path with `..` | Path traversal risk | Critical |
| Missing shebang | No `#!/usr/bin/env` line | Important |
| Unpinned deps | `"httpx"` vs `"httpx>=0.27.0"` | Important |
| Heavy deps | tensorflow, torch in script | Important |
| Broad `except Exception` | Without specific handling | Important |
| Missing `requires-python` | Not in metadata block | Important |
| No timeout | External calls without timeout | Important |
| Missing `encoding` | `open()` without encoding | Important |
| No type hints | Functions without annotations | Medium |
| Over 500 lines | Script too large | Medium |
| Platform-specific | `import pwd` without guard | Medium |

## Review Principles

1. **Be thorough but filter aggressively** - Report only high-confidence issues
2. **Provide actionable feedback** - Every issue needs a specific fix
3. **Include line numbers** - `file.py:42` format for all issues
4. **Acknowledge good patterns** - Note what's done well
5. **Consider maintenance burden** - Suggest pragmatic improvements

## Tooling Recommendations

After manual review, suggest running:

```bash
# Lint and format
ruff check --fix $ARGUMENTS
ruff format $ARGUMENTS

# Type check
pyright $ARGUMENTS

# Validate PEP 723 metadata
uv run --script $ARGUMENTS --help  # Quick syntax check
```
