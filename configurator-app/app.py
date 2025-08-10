
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import requests
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def index():
    config_content = None
    config_source = None
    # Only load config if POST, otherwise reset everything
    if request.method == 'POST':
        # Handle file upload
        file = request.files.get('configFile')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                config_content = f.read()
            config_source = filename
        # Handle URL input
        elif request.form.get('configUrl'):
            url = request.form.get('configUrl')
            orig_url = url
            # Auto-convert GitHub page URL to raw URL
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
    # On GET, always reset (no config loaded)
    return render_template('index.html', config_content=config_content, config_source=config_source)


@app.route('/edit', methods=['POST'])
def edit():
    import datetime
    edited_config = request.form.get('editedConfig')
    # Try to get filename from previous session or fallback
    filename = None
    # Try to get filename from hidden input (add this in the form)
    if 'filename' in request.form:
        filename = request.form['filename']
    # Fallback to referrer parsing if needed
    if not filename:
        ref = request.referrer
        if ref and 'config_source=' in ref:
            filename = ref.split('config_source=')[-1]
        elif ref and ref.startswith('http'):
            filename = ref.split('/')[-1]
    # Clean up filename if it's a URL
    if filename and filename.startswith('http'):
        filename = filename.split('/')[-1]
    # Default to configuration.h if not found
    if not filename or filename == '':
        filename = 'configuration.h'
    # Ensure .h extension for Marlin config files
    if 'adv' in filename.lower():
        base = 'configuration_adv'
    else:
        base = 'configuration'
    ext = '.h'
    # Add date-time tag
    dt_tag = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    tagged_filename = f"{base}_{dt_tag}{ext}"
    if edited_config:
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], tagged_filename)
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(edited_config)
        return send_file(temp_path, as_attachment=True, download_name=tagged_filename)
    return redirect(url_for('index'))


# Download handled by /edit route after modification


if __name__ == '__main__':
    app.run(debug=True)
