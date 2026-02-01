from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QCam Control</title>
</head>
<body>
    <h1>QCam Control Panel</h1>
    <button onclick="check()">Check Camera</button>
    <pre id="out"></pre>

    <script>
        function check() {
            fetch('/api/health')
              .then(r => r.json())
              .then(d => document.getElementById('out').innerText = JSON.stringify(d))
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/health")
def health():
    return jsonify(status="ok")
