---
name: Aftershock Tiers bot runs only on Railway
description: Why the Discord bot workflow on Replit must stay stopped, and how to verify code without running it.
---

The Discord bot for this project (Aftershock Tiers) must run only on Railway, never on Replit. Running it in both places at once uses the same `DISCORD_TOKEN` and causes duplicate/conflicting gateway sessions.

**Why:** confirmed by prior duplicate-session issues; established as standing policy in `replit.md`.

**How to apply:** keep the "Start application" workflow stopped by default. Verify code changes with `python -m py_compile main.py` instead of running the live bot. Only start it on Replit if the user explicitly asks to run it there (e.g. temporarily, with Railway's instance stopped). If it's accidentally started (e.g. via an automatic workflow restart), stop it immediately (`pkill -f "python main.py"`) rather than leaving both instances connected. A "failed"/stopped status for this workflow is the expected, intended state — no action needed.
