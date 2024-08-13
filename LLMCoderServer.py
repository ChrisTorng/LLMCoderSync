import os
from flask import Flask, render_template, request, jsonify
from LLMCoderSync import should_ignore, get_ignore_patterns, should_sync, should_add_line_numbers, read_ignore_file

app = Flask(__name__, template_folder='.')

def list_files(start_path):
    gitignore_patterns, claudeignore_patterns, syncignore_patterns = get_ignore_patterns(start_path)
    linenumberignore_patterns = read_ignore_file(os.path.join(start_path, '.linenumberignore'))
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
    syncignore_path = os.path.join(os.getcwd(), '.syncignore')
    
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
    linenumberignore_path = os.path.join(os.getcwd(), '.linenumberignore')
    
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

if __name__ == '__main__':
    app.run(debug=True)