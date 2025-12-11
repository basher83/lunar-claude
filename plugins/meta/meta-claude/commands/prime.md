---
description: Load context for a new agent session by analyzing codebase structure and README
argument-hint: "[path|--deep|--minimal]"
allowed-tools: Bash, Read
---

# Prime

Load essential context for a new agent session: $ARGUMENTS

## Arguments

- `<path>` - Focus on a specific directory or file pattern
- `--deep` - Include detailed file contents from key areas
- `--minimal` - Only show structure, skip README/CHANGELOG
- (none) - Default full context load

## Context

### Codebase Structure

Git-tracked files: !`git ls-files $ARGUMENTS 2>/dev/null | head -100 || git ls-files | head -100`

Directory tree: !`eza . --tree --level=3 --git-ignore 2>/dev/null || find . -type f -name "*.md" -o -name "*.py" -o -name "*.ts" -o -name "*.json" | head -50`

### Project Documentation

@README.md
@CHANGELOG.md

## Instructions

1. Analyze the codebase structure to understand file organization
2. Read README.md to understand project purpose and setup
3. Note key directories and their purposes
4. Provide a concise overview including:
   - Project purpose
   - Key directories/components
   - Important patterns or conventions
   - Next steps if applicable

If `$ARGUMENTS` contains a path, focus analysis on that area.
If `--minimal`, skip documentation reading.
If `--deep`, also examine key configuration files.
