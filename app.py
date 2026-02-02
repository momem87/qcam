from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

# Dashboard HTML
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>QCam Dashboard</title>
    <meta http-equiv="refresh" content="5"> <style>
        body { background: #121212; color: white; text-align: center; font-family: sans-serif; }
        img { width: 80%; border: 5px solid #333; border-radius: 15px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>QCam Live Feed</h1>
    <img src="/live?t={{time}}" alt="Live Stream">
    <p>Auto-refreshing every 5 seconds...</p>
</body>
</html>
'''

@app.route('/')
def index():
    import time
    return render_template_string(HTML_PAGE, time=time.time())

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
