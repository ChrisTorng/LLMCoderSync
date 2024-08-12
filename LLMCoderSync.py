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
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, src_folder)
            if not should_ignore(rel_path, ignore_patterns):
                dest_path = os.path.join(dest_folder, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)

def main():
    current_folder = os.getcwd()
    gitignore_path = os.path.join(current_folder, '.gitignore')
    ignore_patterns = read_gitignore(gitignore_path)
    
    parent_folder = os.path.dirname(current_folder)
    current_folder_name = os.path.basename(current_folder)
    sync_folder_name = f"{current_folder_name}.sync"
    sync_folder_path = os.path.join(parent_folder, sync_folder_name)
    
    sync_folder(current_folder, sync_folder_path, ignore_patterns)
    print(f"同步完成。檔案已複製到 {sync_folder_path}")

if __name__ == "__main__":
    main()