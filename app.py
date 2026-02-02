from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Dashboard is Online"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, 'latest.jpg')
    file.save(file_path)
    return "Upload Success", 200

@app.route('/live')
def live_image():
    return send_from_directory(UPLOAD_FOLDER, 'latest.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
