---
paths: docs/**/*.md, ai_docs/**/*.md
---

# Documentation Standards

## Markdown Conventions

- Use ATX-style headers (`#` not underlines)
- One blank line before and after headers
- Use fenced code blocks with language specifiers
- No trailing whitespace
- Files end with a single newline

## Linting

Documentation is linted with `rumdl`. Configuration in `.rumdl.toml`.

```bash
# Check markdown files
rumdl docs/

# Auto-fix where possible
rumdl --fix docs/
```

## Documentation Structure

```text
docs/
├── architecture/     # System design documents
├── checklists/       # Validation checklists
├── developer/        # Developer guides
├── ideas/            # Feature ideas and proposals
├── notes/            # Session notes and investigations
├── plans/            # Implementation plans
├── research/         # Research findings
├── reviews/          # Audit reports and reviews
└── templates/        # Document templates
```

## File Naming

- Use lowercase with hyphens: `my-document.md`
- Date prefix for time-sensitive docs: `2025-01-15-feature-design.md`
- Be descriptive but concise

## Links

- Use relative links for internal references
- Verify links work with `lychee` (config in `lychee.toml`)
