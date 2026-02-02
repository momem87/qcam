from flask import Flask, request, Response, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

# Dashboard HTML with MJPEG Stream
HTML_PAGE = '''
<html>
    <head><title>QCam Live Stream</title></head>
    <body style="background:#000; color:#fff; text-align:center;">
        <h1>QCam Live Stream</h1>
        <img src="/video_feed" style="width:80%; border:3px solid #333;">
        <p>Streaming from Raspberry Pi...</p>
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'latest.jpg'))
    return "OK", 200

def generate_frames():
    while True:
        # Read the latest image saved by /upload
        if os.path.exists(os.path.join(UPLOAD_FOLDER, 'latest.jpg')):
            with open(os.path.join(UPLOAD_FOLDER, 'latest.jpg'), 'rb') as f:
                frame = f.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
