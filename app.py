import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask import send_file
from werkzeug.utils import secure_filename
from inference import infer
from waitress import serve

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('analysis_files', exist_ok=True)

logger.info("Starting application...")

@app.route('/')
def index():
    logger.debug("Serving index page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.debug("Processing file upload")
    if 'audio_file' not in request.files:
        logger.error("No file part in request")
        return "No file part", 400
    file = request.files['audio_file']
    if file.filename == '':
        logger.error("No selected file")
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.debug(f"Saving file to {file_path}")
        file.save(file_path)
        session['file_path'] = file_path
        return redirect(url_for('waiting'))

@app.route('/waiting')
def waiting():
    logger.debug("Serving waiting page")
    return render_template('waiting.html')

@app.route('/process', methods=['POST'])
def process_file():
    logger.debug("Starting file processing")
    file_path = session.get('file_path')
    
    if not file_path:
        logger.error("No file path found in session")
        return jsonify({"status": "error", "message": "No file path found"}), 400

    logger.debug(f"Processing file: {file_path}")
    result = 'hot' if infer(file_path) else 'not'
    fp = f"{file_path.split('/')[-1]}.csv"
    logger.debug(f"Processing complete. Result: {result}")
    return jsonify({"status": "success", "result": result, "filepath": fp})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    logger.debug(f"Downloading file: {filename}")
    file_path = os.path.join('analysis_files', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Download error: {e}")
        return str(e), 404

@app.route('/hot')
def hot():
    logger.debug("Serving hot page")
    return render_template('hot.html')

@app.route('/not')
def no():
    logger.debug("Serving not page")
    return render_template('not.html')

if __name__ == '__main__':
    logger.info("Initializing server...")
    try:
        # Development mode
        # app.run(host='0.0.0.0', port=8000, debug=True)
        
        # Production mode with Waitress
        logger.info("Starting Waitress server...")
        serve(app, host='0.0.0.0', port=8000, threads=1)
    except Exception as e:
        logger.error(f"Server failed to start: {e}")