import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask import send_file
from werkzeug.utils import secure_filename
from inference import infer
from waitress import serve
import sys

# Configure logging - only show INFO and above, disable debug messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('analysis_files', exist_ok=True)

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
        logger.info(f"Uploading file: {filename}")
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

    logger.info(f"Processing file: {file_path}")
    result = infer(file_path)
    
    if result is None:
        return jsonify({"status": "error", "message": "Feature extraction failed"}), 500
    
    final_result = 'hot' if result else 'not'
    fp = f"{os.path.basename(file_path)}.csv"
    logger.info(f"Result for {file_path}: {final_result}")
    return jsonify({"status": "success", "result": final_result, "filepath": fp})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('analysis_files', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Download error for {filename}: {e}")
        return str(e), 404

@app.route('/hot')
def hot():
    return render_template('hot.html')

@app.route('/not')
def no():
    return render_template('not.html')
    
if __name__ == '__main__':
    logger.info("Starting server...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))