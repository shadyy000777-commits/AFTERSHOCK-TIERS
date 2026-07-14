# Memory Index

- [Live-synced data vs dev repo push script](aftershock-tiers-data-sync.md) — bot pushes tiers_data.json/website/skins live via GitHub API; dev repo's push script must never touch those files.
- [Bot runs only on Railway](aftershock-tiers-railway-only.md) — never start the Discord bot workflow on Replit; it conflicts with the live Railway gateway session.
