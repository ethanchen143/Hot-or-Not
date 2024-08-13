import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import time 
from inference import infer

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return "No file part", 400
    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        session['file_path'] = file_path
        
        return redirect(url_for('waiting'))

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@app.route('/process', methods=['POST'])
def process_file():
    file_path = session.get('file_path')
    
    if not file_path:
        return jsonify({"status": "error", "message": "No file path found"}), 400

    result = process_audio(file_path)

    return jsonify({"status": "success", "result": result})

@app.route('/hot')
def hot():
    return render_template('hot.html')

@app.route('/not')
def no():
    return render_template('not.html')


def process_audio(file_path):
    return 'hot' if infer(file_path) else 'not'


if __name__ == '__main__':
    app.run(debug=True)