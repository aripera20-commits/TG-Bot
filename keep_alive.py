from flask import Flask, jsonify
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "alive", "service": "Football Bot"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def keep_alive():
    logger.info("Starting keep_alive server...")
    Thread(target=run_server, daemon=True).start()

if __name__ == "__main__":
    run_server()
