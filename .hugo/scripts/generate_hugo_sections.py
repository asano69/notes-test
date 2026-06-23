#!/usr/bin/env python3
"""Generate or update Hugo _index.md files for every non-hidden folder in a directory tree.

Usage:
    python generate_hugo_sections.py <root_folder>

For each folder found (including the root folder itself):
  - If _index.md does not exist, it is created from scratch.
  - If _index.md already exists, only the "categories" field is corrected
    (when it does not match the expected path) and "lastmod" is bumped to
    the current time. All other existing content is left untouched.
"""
import argparse
import os
import re
from pathlib import Path
from zoneinfo import ZoneInfo
import datetime

TEMPLATE = """---
title: "{title}"
summary:
tags: []
categories: [{category}]
draft: false
date: {date}
lastmod: {date}
---
"""

# Matches the front matter block: from the opening "---" to the closing "---".
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
CATEGORIES_RE = re.compile(r"^categories:\s*\[.*\]\s*$", re.MULTILINE)
LASTMOD_RE = re.compile(r"^lastmod:\s*.*$", re.MULTILINE)


def category_for(current: Path, root: Path) -> str:
    """Return the category path: folder names from root down to current, joined by '/'."""
    rel = current.relative_to(root)
    if rel == Path("."):
        # The root folder itself has no parent within the tree, so it acts as its own category.
        return current.name
    return rel.as_posix()


def create_index_file(index_file: Path, title: str, category: str, date: str) -> None:
    """Write a brand-new _index.md from the template."""
    content = TEMPLATE.format(title=title, category=category, date=date)
    index_file.write_text(content, encoding="utf-8")
    print(f"Created {index_file}")


def update_index_file(index_file: Path, category: str, date: str) -> None:
    """Fix the categories field of an existing _index.md if needed, without touching anything else.

    Only the "categories" line is rewritten, and only if it differs from the
    expected value. When that happens, "lastmod" is also bumped to `date`.
    Every other line (title, summary, tags, draft, date, ...) is preserved
    exactly as it was.
    """
    content = index_file.read_text(encoding="utf-8")
    fm_match = FRONT_MATTER_RE.match(content)
    if not fm_match:
        print(f"Skipped {index_file}: no front matter found")
        return

    front_matter = fm_match.group(1)
    expected_line = f"categories: [{category}]"

    cat_match = CATEGORIES_RE.search(front_matter)
    if not cat_match:
        print(f"Skipped {index_file}: no categories field found")
        return

    if cat_match.group(0) == expected_line:
        # Already correct; leave the file completely untouched.
        return

    new_front_matter = (
        front_matter[: cat_match.start()] + expected_line + front_matter[cat_match.end() :]
    )
    new_front_matter, replaced = LASTMOD_RE.subn(f"lastmod: {date}", new_front_matter, count=1)
    if not replaced:
        print(f"Warning: no lastmod field found in {index_file}; categories updated but lastmod left as-is")

    new_content = content[: fm_match.start(1)] + new_front_matter + content[fm_match.end(1) :]
    index_file.write_text(new_content, encoding="utf-8")
    print(f"Updated categories (and lastmod) in {index_file}")


def generate_index_files(root: Path, date: str) -> None:
    """Walk the directory tree and create/update _index.md in every non-hidden folder."""
    for dirpath, dirnames, _ in os.walk(root):
        # Prevent os.walk from descending into hidden folders.
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        current = Path(dirpath)
        if current.name.startswith("."):
            continue

        index_file = current / "_index.md"
        category = category_for(current, root)

        if index_file.exists():
            update_index_file(index_file, category, date)
        else:
            create_index_file(index_file, current.name, category, date)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or update Hugo _index.md files recursively.")
    parser.add_argument("folder", type=Path, help="Root folder to process")
    args = parser.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Error: {args.folder} is not a directory")

    # Use the current JST time, accurate to the second, matching the front matter convention.
    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    generate_index_files(args.folder, now)


if __name__ == "__main__":
    main()
