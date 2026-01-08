import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, abort

app = Flask(__name__, static_folder="static")

API_KEY = os.environ.get("API_KEY", "")  # set this in Render dashboard

LATEST = {
    "updated_at": None,
    "t_hist": [],
    "y_hist": [],
    "t_pred": [],
    "y_pred": [],
    "title": "Solar Power Forecast"
}

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/latest")
def latest():
    return jsonify(LATEST)

@app.post("/update")
def update():
    # simple auth (recommended)
    if API_KEY:
        got = request.headers.get("X-API-Key", "")
        if got != API_KEY:
            abort(401)

    payload = request.get_json(force=True)

    # expected keys
    for k in ["t_hist", "y_hist", "t_pred", "y_pred"]:
        if k not in payload:
            return jsonify({"error": f"Missing key: {k}"}), 400

    LATEST["t_hist"] = payload["t_hist"]
    LATEST["y_hist"] = payload["y_hist"]
    LATEST["t_pred"] = payload["t_pred"]
    LATEST["y_pred"] = payload["y_pred"]
    LATEST["title"]  = payload.get("title", LATEST["title"])
    LATEST["updated_at"] = datetime.utcnow().isoformat() + "Z"

    return jsonify({"ok": True, "updated_at": LATEST["updated_at"]})
