#!/usr/bin/env python3
"""
Comprehensive documentation cleaner - removes TypeScript blocks and fixes formatting.
"""

import re
from pathlib import Path


def clean_markdown(content: str) -> str:
    """Clean markdown content by removing TypeScript blocks and fixing formatting."""
    lines = content.split('\n')
    cleaned = []
    in_codeblock = False
    block_lang = None
    skip_block = False
    buffer = []

    for line in lines:
        # Detect code block start
        code_start = re.match(r'^\s*```(\w+)', line)
        if code_start:
            lang = code_start.group(1).lower()
            in_codeblock = True
            block_lang = lang

            # Skip TypeScript blocks
            if lang in ('typescript', 'ts', 'tsx', 'javascript', 'js'):
                skip_block = True
                buffer = []
                continue
            else:
                skip_block = False
                cleaned.append(line)
                continue

        # Detect code block end
        if line.strip() == '```' and in_codeblock:
            in_codeblock = False
            if not skip_block:
                cleaned.append(line)
            skip_block = False
            block_lang = None
            buffer = []
            continue

        # Skip lines in skipped blocks
        if skip_block:
            continue

        # Remove CodeGroup tags
        if '<CodeGroup>' in line or '</CodeGroup>' in line:
            continue

        # Remove Note/Warning tags but keep content
        line = re.sub(r'</?Note>', '', line)
        line = re.sub(r'</?Warning>', '', line)

        # Remove TypeScript-specific syntax
        if ' as const' in line:
            continue

        # Skip theme={null} attributes
        if 'theme={null}' in line:
            continue

        cleaned.append(line)

    # Post-process: remove duplicate consecutive non-empty lines
    final = []
    prev_line = None
    for line in cleaned:
        # Skip exact duplicates of non-empty lines
        if line.strip() and line == prev_line:
            continue
        final.append(line)
        prev_line = line

    # Join and clean up excessive blank lines
    content = '\n'.join(final)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content


def process_file(file_path: Path) -> None:
    """Process a single markdown file."""
    print(f"Processing {file_path.name}...")

    # Read original content
    content = file_path.read_text(encoding='utf-8')

    # Clean the content
    cleaned = clean_markdown(content)

    # Write back
    file_path.write_text(cleaned, encoding='utf-8')

    # Stats
    orig_lines = len(content.split('\n'))
    clean_lines = len(cleaned.split('\n'))
    removed = orig_lines - clean_lines

    print(f"  ✓ {file_path.name}: {orig_lines} → {clean_lines} lines ({removed} removed)")


def main():
    """Clean all target reference files."""
    script_dir = Path(__file__).parent
    refs_dir = script_dir.parent / 'references'

    target_files = [
        'custom-tools.md',
        'sessions.md',
        'skills.md',
        'slash-commands.md'
    ]

    print("🧹 Cleaning reference documentation...\n")

    for filename in target_files:
        file_path = refs_dir / filename
        if file_path.exists():
            process_file(file_path)
        else:
            print(f"  ⚠  File not found: {filename}")

    print("\n✅ Cleaning complete!")


if __name__ == '__main__':
    main()
