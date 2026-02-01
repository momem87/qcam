from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# IMPORTANT: Ensure this matches your active Cloudflare Tunnel URL
RPI_URL = "https://aspect-lists-adding-throw.trycloudflare.com"

@app.route('/')
def index():
    return render_template('index.html', rpi_url=RPI_URL)

@app.route('/api/snapshot')
def take_snapshot():
    try:
        # Calls the API running on your Raspberry Pi (Port 8000)
        response = requests.get(f"{RPI_URL}/api/snapshot", timeout=15)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Fly.io expects port 8080
    app.run(host='0.0.0.0', port=8080)
