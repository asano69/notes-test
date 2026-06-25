#!/usr/bin/env python3
"""Generate or update Hugo _index.md files for every non-hidden folder in a directory tree.

Usage:
    python generate_hugo_sections.py <root_folder>

For each folder found (including the root folder itself):
  - If _index.md does not exist, it is created from scratch.
  - If _index.md already exists and contains a 'categories' field, that
    field is removed and 'lastmod' is bumped to the current time.
    All other existing content is left untouched.
  - If _index.md already exists and has no 'categories' field, it is left
    completely untouched.
"""

import argparse
import datetime
import os
import re
from pathlib import Path
from zoneinfo import ZoneInfo

TEMPLATE = """---
title: "{title}"
summary: ""
tags: []
draft: false
date: {date}
lastmod: {date}
---
"""

# Matches the front matter block: from the opening "---" to the closing "---".
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
# Matches a full "categories: [...]" line including its trailing newline,
# so the entire line is removed cleanly when the field is present.
CATEGORIES_RE = re.compile(r"^categories:\s*\[.*\]\n", re.MULTILINE)
LASTMOD_RE = re.compile(r"^lastmod:\s*.*$", re.MULTILINE)


def create_index_file(index_file: Path, title: str, date: str) -> None:
    """Write a brand-new _index.md from the template."""
    content = TEMPLATE.format(title=title, date=date)
    index_file.write_text(content, encoding="utf-8")
    print(f"Created {index_file}")


def update_index_file(index_file: Path, date: str) -> None:
    """Remove the 'categories' field from an existing _index.md if present.

    When the field is found, it is removed and 'lastmod' is bumped to `date`.
    Every other line is preserved exactly as it was.
    If the file has no 'categories' field it is left completely untouched.
    """
    content = index_file.read_text(encoding="utf-8")
    fm_match = FRONT_MATTER_RE.match(content)
    if not fm_match:
        print(f"Skipped {index_file}: no front matter found")
        return

    front_matter = fm_match.group(1)
    cat_match = CATEGORIES_RE.search(front_matter)
    if not cat_match:
        # Already has no categories field; leave completely untouched.
        return

    # Remove the categories line (the regex includes the trailing newline).
    new_front_matter = front_matter[: cat_match.start()] + front_matter[cat_match.end() :]

    # Bump lastmod since the file is being changed.
    new_front_matter, replaced = LASTMOD_RE.subn(f"lastmod: {date}", new_front_matter, count=1)
    if not replaced:
        print(f"Warning: no lastmod field in {index_file}; categories removed but lastmod left as-is")

    new_content = content[: fm_match.start(1)] + new_front_matter + content[fm_match.end(1) :]
    index_file.write_text(new_content, encoding="utf-8")
    print(f"Removed categories (and updated lastmod) in {index_file}")


def generate_index_files(root: Path, date: str) -> None:
    """Walk the directory tree and create/update _index.md in every non-hidden folder."""
    for dirpath, dirnames, _ in os.walk(root):
        # Prevent os.walk from descending into hidden folders.
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        current = Path(dirpath)
        if current.name.startswith("."):
            continue
        index_file = current / "_index.md"
        if index_file.exists():
            update_index_file(index_file, date)
        else:
            create_index_file(index_file, current.name, date)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate or update Hugo _index.md files recursively."
    )
    parser.add_argument("folder", type=Path, help="Root folder to process")
    args = parser.parse_args()
    if not args.folder.is_dir():
        raise SystemExit(f"Error: {args.folder} is not a directory")
    # Use the current JST time, accurate to the second, matching the front matter convention.
    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    generate_index_files(args.folder, now)


if __name__ == "__main__":
    main()
