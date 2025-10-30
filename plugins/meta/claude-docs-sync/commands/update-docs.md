---
name: update-docs
description: Update Claude Code documentation from docs.claude.com
---

# Update Documentation Command

Downloads fresh Claude Code documentation to ai_docs/.

## Usage

```bash
/update-docs              # Update default pages
/update-docs --all        # Download all 70+ pages
/update-docs --check      # Check what needs updating (dry-run)
/update-docs --interactive # Choose specific pages
```

## Implementation

Executes the claude_docs.py script with appropriate format:

- **User invocation**: Rich format (colorful tables, performance analysis)
- **Hook invocation**: JSON format (machine-readable, compact)

The script auto-detects context and selects format accordingly.
