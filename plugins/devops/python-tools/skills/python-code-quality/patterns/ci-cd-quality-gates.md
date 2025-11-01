# CI/CD Quality Gates for Ruff and Pyright

Block merges when code quality fails. Run comprehensive checks in CI that catch
issues missed locally.

## GitHub Actions

### Basic Quality Check

Create `.github/workflows/quality.yml`:

```yaml
name: Code Quality

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ruff pyright
          pip install -r requirements.txt

      - name: Run ruff
        run: |
          ruff check .
          ruff format --check .

      - name: Run pyright
        run: pyright
```

### Comprehensive Check with Caching

```yaml
name: Code Quality

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install ruff pyright
          pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check . --output-format=github

      - name: Check formatting
        run: ruff format --check . --diff

      - name: Type check with pyright
        run: pyright --outputjson > pyright-report.json

      - name: Upload pyright report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: pyright-report
          path: pyright-report.json
```

## GitLab CI

Create `.gitlab-ci.yml`:

```yaml
code-quality:
  stage: test
  image: python:3.11
  before_script:
    - pip install ruff pyright
    - pip install -r requirements.txt
  script:
    - ruff check .
    - ruff format --check .
    - pyright
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Quality Metrics

### Track Quality Over Time

```yaml
- name: Generate quality report
  run: |
    ruff check . --output-format=json > ruff-report.json
    pyright --outputjson > pyright-report.json

- name: Comment PR with quality metrics
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const ruffReport = JSON.parse(fs.readFileSync('ruff-report.json'));
      const pyrightReport = JSON.parse(fs.readFileSync('pyright-report.json'));

      const comment = `## Code Quality Report

      **Ruff:** ${ruffReport.length} issues
      **Pyright:** ${pyrightReport.generalDiagnostics.length} issues
      `;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

## Branch Protection Rules

### GitHub

Settings → Branches → Branch protection rules:

1. Require status checks to pass before merging
2. Select "Code Quality" workflow
3. Require branches to be up to date before merging

### GitLab

Settings → Repository → Protected branches:

1. Allowed to merge: Developers + Maintainers
2. Require approval from code owners
3. Pipelines must succeed

## Best Practices

1. **Fail fast** - Run quality checks before tests
2. **Cache dependencies** - Speed up CI with pip caching
3. **Parallel jobs** - Run ruff and pyright in parallel
4. **Quality trends** - Track violations over time
5. **Auto-fix in CI** - Create PR with ruff fixes automatically

## Auto-fix Bot Example

```yaml
- name: Auto-fix with ruff
  run: ruff check --fix .

- name: Commit fixes
  run: |
    git config user.name "ruff-bot"
    git config user.email "bot@example.com"
    git add .
    git diff --staged --quiet || git commit -m "style: auto-fix ruff violations"
    git push
```

## Troubleshooting

**CI passes but pre-commit fails:**

- Ensure same ruff/pyright versions in CI and pre-commit
- Check `.pre-commit-config.yaml` rev matches installed version

**CI too slow:**

- Use pip caching
- Run quality checks in parallel with tests
- Consider skipping pyright on non-Python file changes
