import os
import urllib.request
from flask import Flask, send_from_directory, make_response, Response
from waitress import serve

app = Flask(__name__)

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/shadyy000777-commits/AFTERSHOCK-TIERS/main"
WEBSITE_DIR = os.path.join(os.path.dirname(__file__), "website")
STATIC_DIR  = os.path.join(WEBSITE_DIR, "static")


@app.route("/")
def index():
    html_path = os.path.join(WEBSITE_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    resp = make_response(content, 200)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return resp


@app.route("/tiers_data.json")
def tiers_data():
    url = f"{GITHUB_RAW_BASE}/tiers_data.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read()
        resp = make_response(data, 200)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    except Exception as e:
        return make_response(f'{{"error": "Failed to fetch data: {e}"}}', 502)


@app.route("/skins/<path:filename>")
def serve_skin(filename):
    url = f"{GITHUB_RAW_BASE}/static/skins/{filename}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read()
            content_type = r.headers.get("Content-Type", "image/png")
        resp = make_response(data, 200)
        resp.headers["Content-Type"] = content_type
        resp.headers["Cache-Control"] = "public, max-age=300"
        return resp
    except Exception:
        return make_response("Not found", 404)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route("/api/tiers", methods=["OPTIONS"])
@app.route("/tiers_data.json", methods=["OPTIONS"])
def cors_preflight():
    resp = make_response("", 204)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[Railway] Starting web server on port {port}")
    serve(app, host="0.0.0.0", port=port, threads=8)
