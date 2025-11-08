from flask import Flask, jsonify
from datetime import datetime
import time

app = Flask(__name__)
start_time = time.time()

@app.route("/api/status", methods=["GET"])
def status():
    try:
        uptime = round(time.time() - start_time, 2)
        return jsonify({
            "status": "ok",
            "current_time": datetime.now().isoformat(),
            "uptime_seconds": uptime
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
