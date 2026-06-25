#!/usr/bin/env python3
"""Add a date prefix (YYYY-MM-DD-) to markdown file names, based on the
"date" field in each file's YAML frontmatter.

If a file name already has a date prefix, the old prefix is replaced with
the date from the frontmatter, so re-running this script never produces a
doubled-up or stale date.
"""

import argparse
from pathlib import Path
from typing import Optional
import re

# Matches a "YYYY-MM-DD" date prefix at the start of a file name
DATE_PREFIX_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-')

# Matches a "date:" line inside the frontmatter block
DATE_FIELD_RE = re.compile(r'^date:\s*(.+?)\s*$', re.MULTILINE)

# Extracts a "YYYY-MM-DD" date from the value found by DATE_FIELD_RE
DATE_VALUE_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')


def extract_date(markdown_path: Path) -> Optional[str]:
    """Return the "YYYY-MM-DD" date from a markdown file's frontmatter, or None."""
    try:
        text = markdown_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None

    if not text.startswith('---'):
        return None

    # Frontmatter is the block between the first "---" and the next "---"
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None
    frontmatter = parts[1]

    field_match = DATE_FIELD_RE.search(frontmatter)
    if not field_match:
        return None

    value = field_match.group(1).strip('\'"')  # strip optional quotes
    date_match = DATE_VALUE_RE.match(value)
    return date_match.group(1) if date_match else None


def add_date_prefix(markdown_path: Path, dry_run: bool) -> None:
    """Rename a single markdown file to start with its frontmatter date."""
    date_str = extract_date(markdown_path)
    if date_str is None:
        print(f'  skip (no date in frontmatter): {markdown_path.name}')
        return

    # Strip any existing date prefix before adding the new one
    base_name = DATE_PREFIX_RE.sub('', markdown_path.stem)
    new_name = f'{date_str}-{base_name}{markdown_path.suffix}'

    if new_name == markdown_path.name:
        print(f'  skip (already correct): {markdown_path.name}')
        return

    new_path = markdown_path.with_name(new_name)
    if new_path.exists():
        print(f'  skip (target already exists): {markdown_path.name} -> {new_name}')
        return

    if dry_run:
        print(f'  would rename: {markdown_path.name} -> {new_name}')
    else:
        markdown_path.rename(new_path)
        print(f'  renamed: {markdown_path.name} -> {new_name}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a date prefix to markdown file names, based on each file's frontmatter 'date' field."
    )
    parser.add_argument('directory', type=Path, help='Directory containing markdown files')
    parser.add_argument('-r', '--recursive', action='store_true', help='Also process subdirectories')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Show what would be renamed, without renaming')
    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f'{args.directory} is not a directory')

    pattern = '**/*.md' if args.recursive else '*.md'
    markdown_files = sorted(args.directory.glob(pattern))

    if not markdown_files:
        print('No markdown files found.')
        return

    for markdown_path in markdown_files:
        add_date_prefix(markdown_path, args.dry_run)


if __name__ == '__main__':
    main()
