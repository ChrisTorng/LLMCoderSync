import os
from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)