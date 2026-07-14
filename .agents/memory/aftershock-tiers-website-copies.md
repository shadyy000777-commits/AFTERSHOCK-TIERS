---
name: Aftershock Tiers dual index.html files
description: Root index.html vs website/index.html serve two different sites — edit both or things silently diverge.
---

This project has **two copies** of the site markup, serving two different deployments:

- Root `index.html` — pushed live by the running bot itself (`_push_website_to_github` in `main.py`, via GitHub Contents API) to feed the **Netlify** site (`My-site`/`INDEX` repos). The dev repo's `push_to_github.sh` must never commit/push this — it's bot-owned.
- `website/index.html` (+ `website/static/`) — the file **Railway**'s `railway_server.py` actually serves (`Procfile: web: python railway_server.py`). The bot does NOT keep this one in sync automatically; it only updates via a real git commit+push. `push_to_github.sh` includes `website/index.html`/`website/static` in its code-file list specifically so Railway's site reflects design changes.

**Why this matters:** the two files can silently diverge (one had ~1330 lines, the other ~1205, missing recent features) since only one path is bot-managed. A design/markup change made to only one copy will show up on one site but not the other, looking like "the website isn't updating" even though nothing is broken.

**How to apply:** whenever editing site design/markup (not live data), edit root `index.html` then copy it over `website/index.html` (or vice versa) before pushing, so both Netlify and Railway serve the same markup. `tiers_data.json`/skins stay bot-owned either way — never manually sync those.
