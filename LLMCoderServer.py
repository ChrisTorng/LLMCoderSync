import os
from flask import Flask, render_template_string
from LLMCoderSync import should_ignore, get_ignore_patterns

app = Flask(__name__)

def list_files(start_path):
    gitignore_patterns, claudeignore_patterns = get_ignore_patterns(start_path)
    file_list = []
    for root, _, files in os.walk(start_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), start_path)
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
