---
name: Aftershock Tiers live data sync
description: How tiers_data.json/website/skins stay in sync between the live bot and GitHub, and why the dev repo's push script must not touch them.
---

The production Discord bot (running on Railway) pushes `tiers_data.json`, `index.html`, `static/` assets, and skin images **directly to GitHub via the Contents API** (`_push_data_to_github`, `_push_website_to_github`, `_push_image_to_github` in `main.py`) on every relevant change — e.g. every `/submittest`. This happens to `AFTERSHOCK-TIERS`, `My-site`, and `INDEX` repos, live, independent of anything in this Replit repo.

The Railway website (`railway_server.py`) fetches `tiers_data.json` and skins live from `raw.githubusercontent.com` on every request (no-store headers) — it does not need a redeploy to pick up changes, just a fresh GitHub commit.

**Why this matters:** `push_to_github.sh` (this dev repo's sync script) used to `git add -A` and force-push, which included this workspace's stale local `tiers_data.json`/`index.html`/`static/` copies — overwriting the live bot's real-time production data and making test submissions appear to vanish/not show on the website. Root-caused via GitHub commit history showing a Replit-authored commit ("Remove tier data from JSON...") landing after the bot's own auto-sync commits.

**How to apply:** `push_to_github.sh` must only ever add/commit explicit code files (`main.py`, `config.py`, `requirements.txt`, `railway_server.py`, `Procfile`, `railway.json`, `nixpacks.toml`, `runtime.txt`, `requirements-web.txt`, `push_to_github.sh`, `replit.md`) — never `tiers_data.json`, `index.html`, `static/`, or `skins/`. If the live site ever looks "stuck" or reverted, check for a stray commit in `AFTERSHOCK-TIERS`/`INDEX` history that touched those data files from something other than the bot's own auto-sync, and check GitHub raw CDN caching (~5min TTL) as a secondary, more benign explanation of a short delay.
