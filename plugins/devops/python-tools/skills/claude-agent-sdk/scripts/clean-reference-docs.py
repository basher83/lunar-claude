#!/usr/bin/env python3
"""Clean reference documentation by removing TypeScript blocks and fixing formatting."""

import re
from pathlib import Path


def remove_typescript_blocks(content: str) -> str:
    """Remove TypeScript code blocks and keep only Python."""
    lines = content.split('\n')
    cleaned_lines = []
    in_typescript_block = False
    in_codegroup = False
    skip_until_python = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect CodeGroup start
        if '<CodeGroup>' in line or '</CodeGroup>' in line:
            in_codegroup = True
            i += 1
            continue

        # Detect TypeScript block start
        if '```typescript' in line.lower() or '```ts' in line.lower():
            in_typescript_block = True
            skip_until_python = True
            i += 1
            continue

        # Detect Python block start
        if '```python' in line.lower():
            in_typescript_block = False
            skip_until_python = False
            cleaned_lines.append(line)
            i += 1
            continue

        # Detect block end
        if line.strip() == '```':
            if in_typescript_block:
                in_typescript_block = False
                skip_until_python = False
                i += 1
                continue
            else:
                cleaned_lines.append(line)
                i += 1
                continue

        # Skip TypeScript content
        if skip_until_python or in_typescript_block:
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    return '\n'.join(cleaned_lines)


def fix_formatting(content: str) -> str:
    """Fix common formatting issues."""
    # Remove duplicate lines that appear in the source
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        # Skip obvious duplicates (same line repeated)
        if i > 0 and line.strip() and lines[i-1].strip() == line.strip():
            # Check if it's not an intentional repeat (like in lists)
            if not line.strip().startswith(('-', '*', '1.', '2.')):
                continue

        fixed_lines.append(line)

    content = '\n'.join(fixed_lines)

    # Fix broken code block markers
    content = re.sub(r'```\n([a-z_]+) =', r'```python\n\1 =', content)

    # Remove empty CodeGroup tags
    content = re.sub(r'<CodeGroup>\s*</CodeGroup>', '', content)

    # Remove Note/Warning tags (keep content)
    content = re.sub(r'</?Note>', '', content)
    content = re.sub(r'</?Warning>', '', content)

    # Clean up excessive blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content


def clean_file(file_path: Path) -> None:
    """Clean a single reference file."""
    print(f"Cleaning {file_path.name}...")

    content = file_path.read_text()

    # Remove TypeScript blocks
    content = remove_typescript_blocks(content)

    # Fix formatting
    content = fix_formatting(content)

    # Write back
    file_path.write_text(content)
    print(f"  ✓ Cleaned {file_path.name}")


def main():
    """Clean all reference documentation files."""
    references_dir = Path(__file__).parent.parent / 'references'

    files_to_clean = [
        'custom-tools.md',
        'sessions.md',
        'skills.md',
        'slash-commands.md'
    ]

    for filename in files_to_clean:
        file_path = references_dir / filename
        if file_path.exists():
            clean_file(file_path)
        else:
            print(f"  ⚠ File not found: {filename}")

    print("\n✅ All files cleaned!")


if __name__ == '__main__':
    main()
