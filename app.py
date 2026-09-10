from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import statistics
import time
from datetime import datetime

app = Flask(__name__)
DB = "monitor.db"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            success INTEGER,
            error TEXT,
            checked_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def save_log(url, method, status, response_time, success, error=""):
    con = sqlite3.connect(DB)
    con.execute(
        """INSERT INTO api_logs
        (url, method, status_code, response_time, success, error, checked_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (url, method, status, response_time, int(success), error,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    con.commit()
    con.close()

def get_logs():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT * FROM api_logs ORDER BY id DESC").fetchall()
    con.close()
    return [dict(r) for r in rows]

def check_api(url):
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=8)
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        success = 200 <= response.status_code < 400
        save_log(url, "GET", response.status_code, elapsed, success,
                 "" if success else f"HTTP {response.status_code}")
        return {
            "url": url,
            "status_code": response.status_code,
            "response_time": elapsed,
            "success": success,
            "error": "" if success else f"HTTP {response.status_code}"
        }
    except requests.RequestException as exc:
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        save_log(url, "GET", None, elapsed, False, str(exc))
        return {
            "url": url,
            "status_code": None,
            "response_time": elapsed,
            "success": False,
            "error": str(exc)
        }

@app.route("/")
def dashboard():
    logs = get_logs()
    total = len(logs)
    successful = sum(x["success"] for x in logs)
    failed = total - successful
    times = [x["response_time"] for x in logs]
    avg = round(statistics.mean(times), 2) if times else 0
    fastest = round(min(times), 2) if times else 0
    slowest = round(max(times), 2) if times else 0
    success_rate = round(successful / total * 100, 1) if total else 0
    return render_template(
        "index.html",
        logs=logs[:25],
        total=total,
        successful=successful,
        failed=failed,
        avg=avg,
        fastest=fastest,
        slowest=slowest,
        success_rate=success_rate
    )

@app.route("/check", methods=["POST"])
def check():
    url = request.form.get("url", "").strip()
    if not url:
        return jsonify({"error": "Please enter an API URL."}), 400
    if not (url.startswith("http://") or url.startswith("https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400
    return jsonify(check_api(url))

@app.route("/clear", methods=["POST"])
def clear():
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM api_logs")
    con.commit()
    con.close()
    return jsonify({"ok": True})

init_db()

if __name__ == "__main__":
    app.run(debug=True)
