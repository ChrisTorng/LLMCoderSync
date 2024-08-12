import os
from flask import Flask, render_template_string
from LLMCoderSync import should_ignore, get_ignore_patterns

app = Flask(__name__)

def list_files(start_path):
    gitignore_patterns, claudeignore_patterns = get_ignore_patterns(start_path)
    file_list = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        rel_root = os.path.relpath(root, start_path)
        
        # Filter out directories that should be ignored
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(rel_root, d), gitignore_patterns, claudeignore_patterns)]
        
        # Check if the current directory should be ignored
        if should_ignore(rel_root, gitignore_patterns, claudeignore_patterns):
            continue
        
        for file in files:
            rel_path = os.path.join(rel_root, file)
            if not should_ignore(rel_path, gitignore_patterns, claudeignore_patterns):
                file_list.append(rel_path)
    return file_list

@app.route('/')
def index():
    current_folder = os.getcwd()
    files = list_files(current_folder)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File List</title>
    </head>
    <body>
        <h1>Files in Current Directory</h1>
        <ul>
        {% for file in files %}
            <li>{{ file }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, files=files)

if __name__ == '__main__':
    app.run(debug=True)