import os
import shutil
import pathlib

def read_gitignore(path):
    ignore_patterns = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ignore_patterns

def should_ignore(path, ignore_patterns):
    for pattern in ignore_patterns:
        if pathlib.Path(path).match(pattern):
            return True
    return False

def sync_folder(src_folder, dest_folder, ignore_patterns):
    for root, dirs, files in os.walk(src_folder):
        rel_root = os.path.relpath(root, src_folder)
        if should_ignore(rel_root, ignore_patterns):
            continue
        for file in files:
            rel_path = os.path.join(rel_root, file)
            if not should_ignore(rel_path, ignore_patterns):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if not os.path.exists(dest_path) or os.stat(src_path).st_mtime > os.stat(dest_path).st_mtime:
                    shutil.copy2(src_path, dest_path)
                    print(f'Copied: {rel_path}')
        for dir in dirs:
            if should_ignore(os.path.join(rel_root, dir), ignore_patterns):
                dirs.remove(dir)

def main():
    current_folder = os.getcwd()
    gitignore_path = os.path.join(current_folder, '.gitignore')
    ignore_patterns = read_gitignore(gitignore_path)
    
    parent_folder = os.path.dirname(current_folder)
    current_folder_name = os.path.basename(current_folder)
    sync_folder_name = f"{current_folder_name}.sync"
    sync_folder_path = os.path.join(parent_folder, sync_folder_name)
    
    if os.path.exists(sync_folder_path):
        shutil.rmtree(sync_folder_path)
    os.makedirs(sync_folder_path)
    
    sync_folder(current_folder, sync_folder_path, ignore_patterns)
    print(f"Sync completed. Files have been copied to {sync_folder_path}")

if __name__ == "__main__":
    main()