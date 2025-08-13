


import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from werkzeug.utils import secure_filename
from flash_cards import FLASH_CARDS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/list-config-files', methods=['GET'])
def list_config_files():
    '''List the files in the selected configurationfolder.'''
    folder = request.args.get('folder')
    config_dir = os.path.join('config', folder) if folder else None
    files = []
    if config_dir and os.path.isdir(config_dir):
        for f in os.listdir(config_dir):
            if f.endswith(('.h', '.ini', '.txt')):
                files.append(f)
    return jsonify({'files': files})

# Download edited config file
@app.route('/edit', methods=['POST'])
def download_edited_config():
    edited_config = request.form.get('editedConfig')
    filename = request.form.get('filename', 'configuration.h')
    if not edited_config:
        return "No config data provided.", 400
    response = Response(edited_config, mimetype='text/plain')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

# Support AJAX GET for file content
@app.route('/edit', methods=['GET'])
def edit_get():
    folder = request.args.get('folder')
    filename = request.args.get('filename')
    if not folder or not filename:
        return jsonify({'error': 'Missing folder or filename'}), 400
    # Use the actual workspace root
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CR6Community-Marlin_TB'))
    base_dir = os.path.join(workspace_root, 'config', folder)
    file_path = os.path.join(base_dir, filename)
    file_path = os.path.realpath(file_path)
    print(f"DEBUG: Trying to open file: {file_path}")
    if not os.path.isfile(file_path):
        print(f"DEBUG: File not found: {file_path}")
        return jsonify({'error': 'File not found', 'path': file_path}), 404
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"DEBUG: File loaded successfully: {file_path}")
        return jsonify({'content': content})
    except Exception as e:
        print(f"DEBUG: Exception reading file: {file_path} - {e}")
        return jsonify({'error': str(e), 'path': file_path}), 500
# Redirect root to Start Here tab
@app.route('/')
def root():
    return redirect(url_for('start_here_tab'))

# Configurator tab route (was previously at /)
@app.route('/configurator', methods=['GET', 'POST'])
def configurator():
    config_content = None
    config_source = None
    if request.method == 'POST':
        file = request.files.get('configFile')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                config_content = f.read()
            config_source = filename
        elif request.form.get('configUrl'):
            url = request.form.get('configUrl')
            orig_url = url
            if url.startswith('https://github.com/') and '/blob/' in url:
                url = url.replace('https://github.com/', 'https://raw.githubusercontent.com/')
                url = url.replace('/blob/', '/')
            try:
                resp = requests.get(url, timeout=10)
                if resp.ok:
                    config_content = resp.text
                    config_source = orig_url
                else:
                    config_content = f"Could not fetch config from URL. Status code: {resp.status_code}"
                    config_source = orig_url
            except Exception:
                config_content = "Could not fetch config from URL."
                config_source = orig_url
    folder = request.args.get('folder')
    filename = request.args.get('filename')
    if folder and filename:
        config_path = os.path.join('config', folder, filename)
        if os.path.isfile(config_path):
            with open(config_path, 'r') as f:
                config_content = f.read()
            config_source = config_path
    return render_template('index.html', config_content=config_content, config_source=config_source)

@app.route('/start-here')
def start_here_tab():
    return render_template('start_here.html', flash_cards=FLASH_CARDS)

if __name__ == '__main__':
    app.run(debug=True)
