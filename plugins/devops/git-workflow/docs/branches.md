## Branch Naming Conventions

Use descriptive, prefixed branch names:

### Branch Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New functionality | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/login-redirect-loop` |
| `hotfix/` | Urgent production fixes | `hotfix/security-patch` |
| `release/` | Release preparation | `release/v2.1.0` |
| `docs/` | Documentation updates | `docs/api-reference` |
| `refactor/` | Code restructuring | `refactor/database-layer` |
| `test/` | Test additions | `test/integration-suite` |
| `chore/` | Maintenance | `chore/dependency-updates` |

### Naming Rules

- Use kebab-case (lowercase with hyphens)
- Keep names descriptive but concise
- Include ticket/issue number when applicable: `feature/123-user-auth`
- Avoid generic names like `feature/update` or `fix/bug`

## Protected Branches

Never force-push or directly commit to:

- `main` / `master`
- `develop`
- `staging` / `production`
- `release/*` branches

Always use pull requests for these branches.

## Quick Reference

### Creating a Feature Branch

```bash
git checkout -b feature/descriptive-name
```
