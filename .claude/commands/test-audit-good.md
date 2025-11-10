---
description: Well-formed test command with all best practices
argument-hint: [input-file]
allowed-tools: Read, Write
---

# Test Good Command

You are a test command that demonstrates all best practices for slash command creation.

## Process

1. Read the input file at `$1`
2. Process the content
3. Write output

## Input

The command accepts one argument: the path to a file.

You will use the Read tool to access the file specified by the first positional argument.

## Output Format

Present results in markdown format with clear sections:

- Summary section
- Details section
- Recommendations section

## Examples

```bash
/test-audit-good data.txt
```

Expected output: Processed data in markdown format.

## Implementation

Read file content using Read tool, then write formatted output using Write tool.
