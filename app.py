import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string, send_from_directory
import requests

app = Flask(__name__)

PI_BASE_URL = os.environ.get("PI_BASE_URL", "").rstrip("/")
CAP_DIR = "/data/captures"
os.makedirs(CAP_DIR, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>QCam Control</title>
  <style>
    body { font-family: Arial; padding: 16px; }
    button { padding: 10px 14px; margin-right: 8px; }
    img { max-width: 100%; border: 1px solid #ddd; margin-top: 12px; }
    pre { background: #f6f6f6; padding: 10px; }
  </style>
</head>
<body>
  <h1>QCam Control Panel</h1>

  <button onclick="check()">Health</button>
  <button onclick="capture()">Capture</button>

  <pre id="out"></pre>
  <img id="img" style="display:none;" />

  <script>
    function check() {
      fetch('/api/health').then(r => r.json())
        .then(d => document.getElementById('out').innerText = JSON.stringify(d, null, 2))
        .catch(e => document.getElementById('out').innerText = String(e));
    }

    function capture() {
      document.getElementById('out').innerText = "Capturing...";
      fetch('/api/capture', {method:'POST'}).then(r => r.json())
        .then(d => {
          document.getElementById('out').innerText = JSON.stringify(d, null, 2);
          if (d.ok && d.url) {
            const img = document.getElementById('img');
            img.src = d.url + "?t=" + Date.now();
            img.style.display = "block";
          }
        })
        .catch(e => document.getElementById('out').innerText = String(e));
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
    return jsonify(status="ok", pi_base_url=PI_BASE_URL)

@app.route("/api/capture", methods=["POST"])
def capture():
    if not PI_BASE_URL:
        return jsonify(ok=False, error="PI_BASE_URL not set"), 400

    # جرّب مسارات شائعة للـ snapshot
    candidates = [
        f"{PI_BASE_URL}/snapshot.jpg",
        f"{PI_BASE_URL}/snapshot",
        f"{PI_BASE_URL}/api/snapshot",
        f"{PI_BASE_URL}/api/capture",
    ]

    last_err = None
    img_bytes = None
    used_url = None

    for u in candidates:
        try:
            r = requests.get(u, timeout=20)
            if r.status_code == 200 and r.content and ("image" in r.headers.get("content-type","") or len(r.content) > 1000):
                img_bytes = r.content
                used_url = u
                break
            last_err = f"{u} -> {r.status_code}"
        except Exception as e:
            last_err = f"{u} -> {e}"

    if not img_bytes:
        return jsonify(ok=False, error="Could not fetch image from Pi", tried=candidates, last=last_err), 502

    fname = datetime.utcnow().strftime("cap_%Y%m%d_%H%M%S.jpg")
    path = os.path.join(CAP_DIR, fname)
    with open(path, "wb") as f:
        f.write(img_bytes)

    return jsonify(ok=True, saved=fname, url=f"/captures/{fname}", pi_source=used_url)

@app.route("/captures/<path:filename>")
def serve_capture(filename):
    return send_from_directory(CAP_DIR, filename, as_attachment=False)
