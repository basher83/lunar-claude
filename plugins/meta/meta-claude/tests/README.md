# meta-claude Test Suite

Automated tests for meta-claude plugin Python scripts.

## Running Tests

```bash
# Run all tests
pytest plugins/meta/meta-claude/tests/

# Run with coverage
pytest --cov=plugins/meta/meta-claude/skills/skill-factory/scripts plugins/meta/meta-claude/tests/

# Run with verbose output
pytest -v plugins/meta/meta-claude/tests/
```

## Test Coverage

- **test_quick_validate.py**: Tests for skill validation logic
- **test_package_skill.py**: Tests for skill packaging into .skill files

## Requirements

```bash
pip install pytest pytest-cov pyyaml
```

## Test Structure

Each test file follows pytest conventions:

- Test classes group related tests
- Fixtures provide reusable test resources
- Descriptive test names explain what is tested
