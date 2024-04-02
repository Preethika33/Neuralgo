import time
from flask import Flask, request, jsonify, render_template
import os
import zipfile
import shutil
import main

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(zip_file, extract_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

def has_audio_files(extract_folder):
    for root, _, files in os.walk(extract_folder):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.ogg'):
                return True
    return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        temp_folder = os.path.join(UPLOAD_FOLDER, 'temp')
        
        os.makedirs(temp_folder, exist_ok=True)
        
        zip_path = os.path.join(temp_folder, file.filename)
        file.save(zip_path)
        time.sleep(10)

        extract_folder = os.path.join(temp_folder, 'extracted')
        extract_zip(zip_path, extract_folder)

        res = main.recallll(r"uploads\temp\extracted\Call Data Sample")

        if not has_audio_files(extract_folder):
            shutil.rmtree(temp_folder)  
            return jsonify({'error': 'No audio files found in the zip'})

        return jsonify({'success':  res})

    else:
        return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)