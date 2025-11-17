# Skill Format

Light cleanup of research materials - remove UI artifacts and apply basic formatting.

## Usage

```bash
/skill-format <research-dir>
```

## What This Does

Runs `format_skill_research.py` to:

- Remove GitHub UI elements (navigation, headers, footers)
- Remove redundant blank lines
- Ensure code fences have proper spacing
- Ensure lists have proper spacing

**Philosophy:** "Car wash" approach - remove chunks of mud before detail work.

Does NOT restructure content for skill format.

## Instructions

Run the cleanup script:

```bash
${CLAUDE_PLUGIN_ROOT}/../../scripts/format_skill_research.py <research-dir>
```

The script processes all `.md` files recursively in the directory.

## Expected Output

```text
Found N markdown files to clean
Processing: file1.md
✓ Cleaned: file1.md
Processing: file2.md
✓ Cleaned: file2.md

✓ Formatted N files in <research-dir>
```

## Error Handling

**If directory not found:**

```text
Error: Directory not found: <research-dir>
```

Suggest: Check path or run `/skill-research` first

**If no markdown files:**

```text
No markdown files found in <research-dir>
```

Action: Skip formatting, continue workflow

## Examples

**Format research:**

```bash
/skill-format docs/research/skills/docker-master/
# Output: ✓ Formatted 5 files in docs/research/skills/docker-master/
```

**Already clean:**

```bash
/skill-format docs/research/skills/clean-skill/
# Output: No markdown files found (or no changes needed)
```
