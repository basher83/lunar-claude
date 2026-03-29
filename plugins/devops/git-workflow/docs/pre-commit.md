## Pre-Commit Workflow

Before committing:

1. **Review changes**: `git diff` and `git status`
2. **Check for sensitive files**: Never commit `.env`, credentials, API keys
3. **Run pre-commit hooks**: Let formatters and linters process files
4. **Re-stage if hooks modify files**: Add reformatted files and retry commit

### Handling Pre-Commit Hook Failures

When hooks modify files:

1. Review the changes made by hooks
2. Re-add the modified files: `git add <files>`
3. Retry the commit
4. Document any issues for manual review
