import os
import json
import base64
import urllib.request
from flask import Flask, send_from_directory, make_response
from waitress import serve

app = Flask(__name__)

# AFTERSHOCK-TIERS is kept in sync by the bot (tiers_data.json + skins pushed on every change)
# Use the GitHub API (not raw CDN) for tiers_data.json — raw.githubusercontent.com has aggressive
# CDN caching that can serve stale data for minutes even with cache-busting headers.
GITHUB_OWNER    = "shadyy000777-commits"
GITHUB_REPO     = "AFTERSHOCK-TIERS"
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/main"
WEBSITE_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "website")
STATIC_DIR      = os.path.join(WEBSITE_DIR, "static")


def _fetch(url: str, timeout: int = 10, nocache: bool = False):
    headers = {"User-Agent": "railway-server/1.0"}
    if nocache:
        headers["Cache-Control"] = "no-cache, no-store"
        headers["Pragma"] = "no-cache"
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}_={int(__import__('time').time())}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "application/octet-stream")


def _fetch_via_api(path: str, timeout: int = 10):
    """Fetch a file from GitHub via the Contents API (always returns current data, no CDN cache)."""
    url = f"{GITHUB_API_BASE}/contents/{path}"
    headers = {
        "User-Agent": "railway-server/1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    return base64.b64decode(data["content"].replace("\n", ""))


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
    """Fetch live tiers_data.json via GitHub API (bypasses CDN cache — always current data)."""
    try:
        data = _fetch_via_api("tiers_data.json")
        resp = make_response(data, 200)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return resp
    except Exception as e:
        print(f"[Railway] tiers_data fetch error: {e}")
        return make_response('{"players":{}}', 502)


@app.route("/static/skins/<path:filename>")
@app.route("/skins/<path:filename>")
def serve_skin(filename):
    """Skins pushed by the bot to AFTERSHOCK-TIERS/static/skins/ — proxy them live."""
    url = f"{GITHUB_RAW_BASE}/static/skins/{filename}"
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
    """Logo, bg.gif and other static assets — served locally from the repo."""
    return send_from_directory(STATIC_DIR, filename)


@app.route("/tiers_data.json", methods=["OPTIONS"])
def cors_preflight():
    resp = make_response("", 204)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[Railway] Web server starting on port {port}")
    serve(app, host="0.0.0.0", port=port, threads=8)
