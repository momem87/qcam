from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
# Use /tmp for ephemeral storage on Fly.io if no volume is attached
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body style="background:#000; color:#fff; text-align:center;">
                <h1>QCam Live</h1>
                <img id="stream" src="/live" style="width:80%;">
                <script>
                    setInterval(() => {
                        document.getElementById('stream').src = '/live?t=' + Date.now();
                    }, 3000);
                </script>
            </body>
        </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files: return "No file", 400
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'latest.jpg'))
    return "OK", 200

@app.route('/live')
def live():
    return send_from_directory(UPLOAD_FOLDER, 'latest.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
