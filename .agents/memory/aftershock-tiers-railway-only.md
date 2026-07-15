---
name: Aftershock Tiers bot dual-running on Railway + Replit
description: User has explicitly chosen to run the Discord bot on both Railway and Replit at once, despite known conflict risk — do not "fix" this by stopping Replit without asking.
---

The Discord bot for this project (Aftershock Tiers) normally should run only on Railway — running the same `DISCORD_TOKEN` on both Railway and Replit at once causes duplicate/conflicting gateway sessions. The user has been asked twice (as of 2026-07-15) whether to make it Railway-only and both times explicitly chose to keep running it on both anyway.

**Confirmed real incident:** a tester's `/submittest` for a player was never written to `tiers_data.json` at all (no trace in players/tests/profiles). Its expected timing lined up with a window where the Replit workflow had just been restarted alongside the live Railway instance — a plausible dropped/conflicting interaction, not a GitHub-push bug. When a submitted test or command silently doesn't persist, check for dual-run overlap first before assuming a push/sync issue.

**How to apply:** do not stop the "Start application" workflow or suggest Railway-only as a fix without user buy-in — they've declined it twice. It's fine to restart the Replit workflow briefly for screenshots/verification, but be aware that any overlap window with the live Railway bot can silently drop a command a tester runs at the same time.
