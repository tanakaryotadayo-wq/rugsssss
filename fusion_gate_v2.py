from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3, time

DB_PATH = "data.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

def get_conn():
    return sqlite3.connect(DB_PATH)

app = Flask(__name__)
start_time = time.time()
init_db()

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
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/item", methods=["POST"])
def create_item():
    try:
        data = request.get_json(force=True) or {}
        name = str(data.get("name", "")).strip()
        value = str(data.get("value", "")).strip()
        if not name or not value:
            return jsonify({"status": "error", "message": "name and value required"}), 400
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO items (name, value, created_at) VALUES (?, ?, ?)",
                (name, value, datetime.now().isoformat())
            )
            item_id = cur.lastrowid
            conn.commit()
        return jsonify({"status": "ok", "id": item_id, "name": name, "value": value}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/item/<int:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        with get_conn() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, name, value, created_at FROM items WHERE id = ?",
                (item_id,)
            ).fetchone()
        if not row:
            return jsonify({"status": "error", "message": "not found"}), 404
        return jsonify({"status": "ok", "item": dict(row)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
