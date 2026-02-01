from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "QCam API is running"

@app.route("/api/health")
def health():
    return jsonify(status="ok")
