from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # This will look for index.html in the templates folder
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'latest.jpg'))
    return "Success", 200

@app.route('/live')
def live():
    return send_from_directory(UPLOAD_FOLDER, 'latest.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
