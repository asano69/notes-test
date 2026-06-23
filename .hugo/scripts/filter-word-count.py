#!/usr/bin/env python3
import os
import sys
import re
from concurrent.futures import ProcessPoolExecutor, as_completed

def RGB_count_characters(file_path, strip_yaml=False):
    """ファイル内の文字数をカウントする"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # YAMLフロントマターを除外する処理
            if strip_yaml:
                content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL | re.MULTILINE)
                
            return file_path, len(content), None
    except Exception as e:
        return file_path, -1, str(e)

def get_all_files(target_dir):
    """隠しフォルダ・特定のファイルをスキップしながら対象ファイルを【絶対パス】でリストアップ"""
    file_paths = []
    # 探索の起点となるディレクトリ自体を絶対パスに変換
    base_dir = os.path.abspath(target_dir)
    
    for root, dirs, files in os.walk(base_dir, followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.startswith('.'):
                continue
            if file == '_index.md':
                continue
            if file.endswith(('.md', '.markdown')):
                # root が既に絶対パスなので、結合すると自動的に絶対パスになります
                file_paths.append(os.path.join(root, file))
    return file_paths

def find_md_files_parallel(target_dir, min_chars, max_chars, strip_yaml=False, path_only=False):
    if not path_only:
        print(f"START: {os.path.abspath(target_dir)}")
        print(f"RANGE: {min_chars} to {max_chars} chars")
        print(f"STRIP YAML: {strip_yaml}")
        print("-" * 50)
        print("Scanning directory tree...")
        
    file_paths = get_all_files(target_dir)
    total_files = len(file_paths)
    
    if not path_only:
        print(f"Found {total_files} markdown files. Processing in parallel...")
        print("-" * 50)
        sys.stdout.flush()
    
    match_count = 0
    checked_count = 0
    
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(RGB_count_characters, fp, strip_yaml) for fp in file_paths]
        
        for future in as_completed(futures):
            checked_count += 1
            file_path, char_count, error_msg = future.result()
            
            if not path_only:
                print(f" Progress: {checked_count}/{total_files} files...", end='\r', flush=True)
            
            if error_msg or char_count == -1:
                print(f"\n[ERROR] Failed to read: {file_path} ({error_msg})", file=sys.stderr)
                continue
                
            if min_chars <= char_count <= max_chars:
                if path_only:
                    print(file_path)
                else:
                    print(" " * 80, end='\r')
                    print(f"[{char_count} chars] {file_path}")
                match_count += 1

    if not path_only:
        print("\n" + "-" * 50)
        print(f"FINISHED. Total scanned: {checked_count}")
        print(f"Matched files: {match_count}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: filter-word-count.py [directory] [min_chars] [max_chars] [--strip-yaml] [--path-only]", file=sys.stderr)
        print("Example: filter-word-count.py . 0 500 --strip-yaml --path-only", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    
    try:
        min_length = int(sys.argv[2])
        max_length = float('inf') if sys.argv[3].lower() == 'inf' else int(sys.argv[3])
    except ValueError:
        print("Error: Character counts must be integers (or 'inf' for max).", file=sys.stderr)
        sys.exit(1)

    strip_yaml_mode = '--strip-yaml' in sys.argv
    path_only_mode = '--path-only' in sys.argv

    find_md_files_parallel(target_directory, min_length, max_length, strip_yaml_mode, path_only_mode)
