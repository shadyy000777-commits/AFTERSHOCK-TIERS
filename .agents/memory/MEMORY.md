# Memory Index

- [Live-synced data vs dev repo push script](aftershock-tiers-data-sync.md) — bot pushes tiers_data.json/website/skins live via GitHub API; dev repo's push script must never touch those root-level files.
- [Bot on Replit + Railway](aftershock-tiers-railway-only.md) — running the bot on both at once (same token) causes duplicate responses; user has explicitly opted into this tradeoff.
- [Dual index.html files](aftershock-tiers-website-copies.md) — root index.html feeds Netlify (bot-owned), website/index.html feeds Railway (git-push-owned); edit both when changing site markup.
