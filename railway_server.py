import os
import urllib.request
from flask import Flask, send_from_directory, make_response
from waitress import serve

app = Flask(__name__)

# Bot pushes live tiers_data.json and skins to My-site repo
DATA_RAW_BASE = "https://raw.githubusercontent.com/shadyy000777-commits/My-site/main"
WEBSITE_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "website")
STATIC_DIR    = os.path.join(WEBSITE_DIR, "static")


def _github_headers():
    headers = {"User-Agent": "railway-server/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _fetch(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers=_github_headers())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "application/octet-stream")


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
    """Fetch live tiers_data.json from My-site (updated by the bot after every change)."""
    url = f"{DATA_RAW_BASE}/tiers_data.json"
    try:
        data, _ = _fetch(url)
        resp = make_response(data, 200)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    except Exception as e:
        print(f"[Railway] tiers_data.json fetch failed: {e}")
        return make_response(f'{{"players": {{}}, "error": "{e}"}}', 502)


@app.route("/skins/<path:filename>")
def serve_skin(filename):
    """Proxy skins from My-site/skins/ (where the bot uploads them)."""
    url = f"{DATA_RAW_BASE}/skins/{filename}"
    try:
        data, content_type = _fetch(url)
        resp = make_response(data, 200)
        resp.headers["Content-Type"] = content_type
        resp.headers["Cache-Control"] = "public, max-age=300"
        return resp
    except Exception:
        return make_response("", 404)


@app.route("/static/<path:filename>")
def serve_static(filename):
    """Logo, bg.gif and other static assets — served from local repo files."""
    return send_from_directory(STATIC_DIR, filename)


@app.route("/tiers_data.json", methods=["OPTIONS"])
@app.route("/skins/<path:filename>", methods=["OPTIONS"])
def cors_preflight(**kwargs):
    resp = make_response("", 204)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[Railway] Web server starting on port {port}")
    serve(app, host="0.0.0.0", port=port, threads=8)
