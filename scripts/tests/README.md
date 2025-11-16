# Scripts Test Suite

Automated tests for repository automation scripts.

## Running Tests

```bash
# Run all tests
pytest scripts/tests/

# Run specific test file
pytest scripts/tests/test_firecrawl_sdk_research.py

# Run with coverage
pytest --cov=scripts scripts/tests/

# Run with verbose output
pytest -v scripts/tests/
```

## Test Coverage

- **test_firecrawl_sdk_research.py**: Tests for Firecrawl SDK research tool
  - API key retrieval and validation
  - Retry logic with exponential backoff
  - Quality filtering and scoring
  - Research document generation

## Requirements

```bash
pip install pytest pytest-asyncio pytest-cov
```

## Test Structure

Each test file follows pytest conventions:

- Test classes group related tests
- Fixtures provide reusable test resources
- Mocks isolate external dependencies (API calls, file I/O)
- Descriptive test names explain what is tested
