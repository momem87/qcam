from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

RPI_URL = "https://citizenship-determination-invitations-instance.trycloudflare.com"

@app.route('/')
def index():
    return render_template('index.html', rpi_url=RPI_URL)

@app.route('/api/snapshot')
def take_snapshot():
    try:
        response = requests.get(f"{RPI_URL}/api/snapshot", timeout=15)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
