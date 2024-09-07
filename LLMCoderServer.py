import os
import subprocess
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
from LLMCoderSync import should_ignore, get_ignore_patterns, should_sync, should_add_line_numbers, read_ignore_file, main as llm_coder_sync

if getattr(sys, 'frozen', False):
    # 如果是打包後的環境
    template_folder = os.path.join(sys._MEIPASS)
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # 如果是開發環境
    app = Flask(__name__, template_folder='.', static_folder='static')

# Create sync folder on startup
current_folder = os.getcwd()
parent_folder = os.path.dirname(current_folder)
current_folder_name = os.path.basename(current_folder)
sync_folder_name = f"{current_folder_name}.sync"
sync_folder_path = os.path.join(parent_folder, sync_folder_name)
if not os.path.exists(sync_folder_path):
    os.makedirs(sync_folder_path)

# Create necessary files in sync folder
for file_name in ['.claudeignore', '.syncignore', '.linenumberignore']:
    file_path = os.path.join(sync_folder_path, file_name)
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

# Create SyncCommand files in sync folder
sync_command_path = os.path.join(sync_folder_path, 'SyncCommand')
if os.name == 'nt':
    sync_command_path += '.cmd'
if not os.path.exists(sync_command_path):
    open(sync_command_path, 'w').close()

def list_files(start_path):
    gitignore_patterns, claudeignore_patterns, syncignore_patterns = get_ignore_patterns(start_path, sync_folder_path)
    linenumberignore_patterns = read_ignore_file(os.path.join(sync_folder_path, '.linenumberignore'))
    file_list = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        rel_root = os.path.relpath(root, start_path)
        
        # Filter out directories that should be ignored by .gitignore or .claudeignore
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(rel_root, d), gitignore_patterns, claudeignore_patterns)]
        if should_ignore(rel_root, gitignore_patterns, claudeignore_patterns):
            continue
        
        for file in files:
            rel_path = os.path.join(rel_root, file)
            if not should_ignore(rel_path, gitignore_patterns, claudeignore_patterns):
                should_sync_file = should_sync(rel_path, syncignore_patterns)
                should_add_line_numbers_file = should_add_line_numbers(rel_path, linenumberignore_patterns)
                file_list.append((rel_path, should_sync_file, should_add_line_numbers_file))
    return file_list

@app.route('/')
def index():
    current_folder = os.getcwd()
    files = list_files(current_folder)
    return render_template('LLMCoderServer.html', files=files, current_folder=current_folder)

@app.route('/update_sync', methods=['POST'])
def update_sync():
    file_path = request.json['file']
    should_sync = request.json['should_sync']
    syncignore_path = os.path.join(sync_folder_path, '.syncignore')

       # Get all files in the current directory
    all_files = [f for f in list_files(os.getcwd()) if f[0] != '.syncignore']

    # Create .syncignore if it doesn't exist
    if not os.path.exists(syncignore_path):
        open(syncignore_path, 'w').close()
    
    # Read existing .syncignore content
    with open(syncignore_path, 'r') as f:
        ignored_files = set(line.strip() for line in f.readlines())
    
    # Update the set based on the current file
    if should_sync:
        ignored_files.discard(file_path)
    else:
        ignored_files.add(file_path)
    
    # Write the updated content back to .syncignore
    with open(syncignore_path, 'w') as f:
        for file, _, _ in all_files:
            if file in ignored_files:
                f.write(f"{file}\n")
    
    return jsonify({'status': 'success'})

@app.route('/update_line_numbers', methods=['POST'])
def update_line_numbers():
    file_path = request.json['file']
    should_add_line_numbers = request.json['should_add_line_numbers']
    linenumberignore_path = os.path.join(sync_folder_path, '.linenumberignore')

    # Get all files in the current directory
    all_files = [f for f in list_files(os.getcwd()) if f[0] != '.linenumberignore']
    
    # Create .linenumberignore if it doesn't exist
    if not os.path.exists(linenumberignore_path):
        open(linenumberignore_path, 'w').close()
    
    # Read existing .linenumberignore content
    with open(linenumberignore_path, 'r') as f:
        ignored_files = set(line.strip() for line in f.readlines())
    
    # Update the set based on the current file
    if should_add_line_numbers:
        ignored_files.discard(file_path)
    else:
        ignored_files.add(file_path)
    
    # Write the updated content back to .linenumberignore
    with open(linenumberignore_path, 'w') as f:
        for file, _, _ in all_files:
            if file in ignored_files:
                f.write(f"{file}\n")
   
    return jsonify({'status': 'success'})

@app.route('/sync', methods=['POST'])
def sync():
    # Call LLMCoderSync.py
    llm_coder_sync()

    # Create the SyncCommand file
    sync_command_path = os.path.join(sync_folder_path, 'SyncCommand')
    if os.name == 'nt':
        sync_command_path += '.cmd'
   
    # Make the file executable on Unix-like systems
    if os.name != 'nt':
        os.chmod(sync_command_path, 0o755)
    
    # Execute the command and capture output
    try:
        if os.name == 'nt':
            output = subprocess.check_output(sync_command_path, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            output = subprocess.check_output(['sh', sync_command_path], stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({'status': 'success', 'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': str(e), 'output': e.output})

@app.route('/file_content/<path:file_path>')
def file_content(file_path):
    current_folder = os.getcwd()
    parent_folder = os.path.dirname(current_folder)
    current_folder_name = os.path.basename(current_folder)
    sync_folder_name = f"{current_folder_name}.sync"
    sync_folder_path = os.path.join(parent_folder, sync_folder_name)
    sync_file_path = os.path.join(sync_folder_path, file_path)

    try:
        if os.path.exists(sync_folder_path) and os.path.exists(sync_file_path) and \
           os.path.getmtime(sync_file_path) >= os.path.getmtime(file_path):
            with open(sync_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            status = "synced"
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            status = "not synced!"
        return jsonify({'content': content, 'status': status})
    except Exception as e:
        return jsonify({'error': f"Error reading file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)