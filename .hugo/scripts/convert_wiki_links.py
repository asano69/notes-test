#!/usr/bin/env python3
"""
Preprocessing script: converts Obsidian wiki links ([[...]]) to Hugo
Markdown links ([label](url)).
Usage: python convert_wiki_links.py <content_dir> [--dry-run]
Requires Python 3.10+. No external dependencies.
"""
import re
import sys
import argparse
from pathlib import Path

WIKI_LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')


def url_for_file(file_path: Path, content_dir: Path) -> str:
    """Return the default Hugo permalink for a content file: its path
    relative to the content directory, without the extension, with a
    trailing slash. An _index.md resolves to its parent directory's URL.
    e.g. content_dir/test/aaa.md       -> '/test/aaa/'
         content_dir/test/_index.md    -> '/test/'
    """
    rel = file_path.relative_to(content_dir).with_suffix('')
    if rel.name == '_index':
        rel = rel.parent
    posix = rel.as_posix()
    return '/' if posix == '.' else f'/{posix}/'


def build_index(content_dir: Path) -> tuple[dict[str, Path], dict[str, list[Path]]]:
    """Build two lookup tables from all .md files under content_dir.
    by_path: 'sample/design/hello' (relative to content_dir, no extension) -> Path
    by_stem: 'hello' -> [Path, ...] (multiple entries signal an ambiguous stem)
    """
    by_path: dict[str, Path] = {}
    by_stem: dict[str, list[Path]] = {}
    for md_file in content_dir.rglob('*.md'):
        # Use forward slashes so keys match Obsidian's wiki link syntax on all platforms
        key = str(md_file.relative_to(content_dir).with_suffix('')).replace('\\', '/')
        by_path[key] = md_file
        by_stem.setdefault(md_file.stem, []).append(md_file)
    return by_path, by_stem


def replace_wiki_links(text: str, by_path: dict[str, Path],
                        by_stem: dict[str, list[Path]], content_dir: Path) -> str:
    """Replace all [[wiki link]] occurrences in text with Markdown links."""
    def resolve(match: re.Match) -> str:
        inner = match.group(1)
        ref, display = inner.split('|', 1) if '|' in inner else (inner, inner)
        ref, display = ref.strip(), display.strip()
        if '/' in ref:
            # Explicit path e.g. [[content/posts/hello|label]]
            target = by_path.get(ref)
            if target is None:
                print(f'Warning: path not found: {ref!r}', file=sys.stderr)
                return match.group(0)
        else:
            # Stem-only e.g. [[PageTitle]] or [[PageTitle|label]]
            candidates = by_stem.get(ref, [])
            if not candidates:
                print(f'Warning: no file found for stem {ref!r}', file=sys.stderr)
                return match.group(0)
            if len(candidates) > 1:
                print(f'Warning: ambiguous stem {ref!r} -> {[str(c) for c in candidates]}',
                      file=sys.stderr)
                return match.group(0)
            target = candidates[0]
        url = url_for_file(target, content_dir)
        return f'[{display}]({url})'
    return WIKI_LINK_RE.sub(resolve, text)


def process_file(file_path: Path, content_dir: Path,
                  by_path: dict[str, Path], by_stem: dict[str, list[Path]],
                  dry_run: bool = False) -> None:
    """Replace wiki links in a single file and write the result back."""
    text = file_path.read_text(encoding='utf-8')
    new_content = replace_wiki_links(text, by_path, by_stem, content_dir)
    if dry_run:
        print(f'=== {file_path} ===\n{new_content}')
    else:
        file_path.write_text(new_content, encoding='utf-8')
        print(f'Processed: {file_path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert Obsidian wiki links to Hugo Markdown links')
    parser.add_argument('content_dir', help='Hugo content directory')
    parser.add_argument('--dry-run', action='store_true',
                         help='Print results without writing files')
    args = parser.parse_args()

    content_dir = Path(args.content_dir).resolve()
    if not content_dir.is_dir():
        print(f'Error: not a directory: {content_dir}', file=sys.stderr)
        sys.exit(1)

    by_path, by_stem = build_index(content_dir)
    for md_file in sorted(content_dir.rglob('*.md')):
        process_file(md_file, content_dir, by_path, by_stem, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
