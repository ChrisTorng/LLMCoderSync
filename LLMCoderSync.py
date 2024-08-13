import os
import shutil
import subprocess
import pathlib
import stat
import io

def read_ignore_file(path):
    ignore_patterns = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ignore_patterns

def get_ignore_patterns(current_folder):
    gitignore_path = os.path.join(current_folder, '.gitignore')
    claudeignore_path = os.path.join(current_folder, '.claudeignore')
    syncignore_path = os.path.join(current_folder, '.syncignore')
    gitignore_patterns = read_ignore_file(gitignore_path)
    claudeignore_patterns = read_ignore_file(claudeignore_path)
    syncignore_patterns = read_ignore_file(syncignore_path)
    return gitignore_patterns, claudeignore_patterns, syncignore_patterns

def should_ignore(path, gitignore_patterns, claudeignore_patterns, syncignore_patterns=None):
    full_path = os.path.abspath(path)
    if os.name == 'nt':
        attributes = os.stat(full_path).st_file_attributes
        if attributes & stat.FILE_ATTRIBUTE_HIDDEN:
            return True
    elif os.name == 'posix':
        if os.path.basename(full_path).startswith('.'):
            return True
    for pattern in gitignore_patterns + claudeignore_patterns:
        if pathlib.Path(path).match(pattern):
            return True
    return False

def get_ignore_patterns(current_folder):
    gitignore_path = os.path.join(current_folder, '.gitignore')
    claudeignore_path = os.path.join(current_folder, '.claudeignore')
    syncignore_path = os.path.join(current_folder, '.syncignore')
    gitignore_patterns = read_ignore_file(gitignore_path)
    claudeignore_patterns = read_ignore_file(claudeignore_path)
    syncignore_patterns = read_ignore_file(syncignore_path)
    return gitignore_patterns, claudeignore_patterns, syncignore_patterns

def should_sync(path, syncignore_patterns):
    for pattern in syncignore_patterns:
        if pathlib.Path(path).match(pattern):
            return False
    return True

def should_add_line_numbers(path, linenumberignore_patterns):
    for pattern in linenumberignore_patterns:
        if pathlib.Path(path).match(pattern):
            return False
    return True

def add_line_numbers(src_path, dest_path, linenumberignore_patterns):
    rel_path = os.path.relpath(src_path, os.getcwd())
    if not should_add_line_numbers(rel_path, linenumberignore_patterns):
        shutil.copy2(src_path, dest_path)
        return False
        return False
    with io.open(src_path, 'r', encoding='utf-8', errors='ignore') as src_file:
        with io.open(dest_path, 'w', encoding='utf-8') as dest_file:
            for i, line in enumerate(src_file, 1):
                dest_file.write(f'{i:>3}. {line}')
    return True

def sync_folder(src_folder, dest_folder, gitignore_patterns, claudeignore_patterns, syncignore_patterns, linenumberignore_patterns):
    total_files = 0
    for root, dirs, files in os.walk(src_folder, topdown=True):
        rel_root = os.path.relpath(root, src_folder)
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(rel_root, d), gitignore_patterns, claudeignore_patterns)]
        if should_ignore(rel_root, gitignore_patterns, claudeignore_patterns):
            continue
        for file in files:
            rel_path = os.path.join(rel_root, file)
            if not should_ignore(rel_path, gitignore_patterns, claudeignore_patterns) and should_sync(rel_path, syncignore_patterns):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if not os.path.exists(dest_path) or os.stat(src_path).st_mtime > os.stat(dest_path).st_mtime:
                    line_numbers_added = add_line_numbers(src_path, dest_path, linenumberignore_patterns)
                    print(f'Copied {"with" if line_numbers_added else "without"} line numbers: {rel_path}')
                    total_files += 1
    return total_files

def main():
    current_folder = os.getcwd()
    gitignore_patterns, claudeignore_patterns, syncignore_patterns = get_ignore_patterns(current_folder)
    linenumberignore_patterns = read_ignore_file(os.path.join(current_folder, '.linenumberignore'))
    
    parent_folder = os.path.dirname(current_folder)
    current_folder_name = os.path.basename(current_folder)
    sync_folder_name = f"{current_folder_name}.sync"
    sync_folder_path = os.path.join(parent_folder, sync_folder_name)
    
    if os.path.exists(sync_folder_path):
        shutil.rmtree(sync_folder_path)
    os.makedirs(sync_folder_path)
    
    total_files = sync_folder(current_folder, sync_folder_path, gitignore_patterns, claudeignore_patterns, syncignore_patterns, linenumberignore_patterns)
    print(f'{total_files} files have been copied to {sync_folder_path}')

if __name__ == "__main__":
    main()