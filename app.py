from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Fly.io context: Use /tmp for storing images temporarily
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def home():
    return "QCam Server is Running. Go to /live to see the image."

# THIS IS THE MISSING PART CAUSING 404
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    # Save the file as latest.jpg
    file.save(os.path.join(UPLOAD_FOLDER, 'latest.jpg'))
    return "Image Received", 200

@app.route('/live')
def live():
    return send_from_directory(UPLOAD_FOLDER, 'latest.jpg')

if __name__ == '__main__':
    # Fly.io looks for port 8080 by default
    app.run(host='0.0.0.0', port=8080)
