# MCTiers Discord Bot

A self-contained Discord bot that replicates the MCTiers tier testing system for Minecraft PvP players. Supports slash commands and `!` prefix commands.

## Stack
- Python 3.12
- discord.py — slash commands, prefix commands, embeds
- python-dotenv — loads `DISCORD_TOKEN` from environment
- aiohttp — async HTTP

## Required secrets
- `DISCORD_TOKEN` — Discord bot token (required to run) — set in Replit as a secret

## Features
- `/test <gamemode>` — interactive tier test (crystal, sword, uhc, pot, axe, smp, bedwars, nodebuff)
- `/profile` — view tier profile
- `/leaderboard <gamemode>` — top tiered players
- `/setign <name>` — set Minecraft IGN
- `/tiers`, `/gamemodes`, `/help`
- Prefix equivalents: `!test`, `!profile`, `!lb`, `!tiers` (note: needs the "Message Content Intent" enabled in the Discord Developer Portal to work — see follow-up task)
- The same process also serves a companion tier-list website (Flask, `main.py` + `website/`) on port 5000, showing the leaderboard/rankings from `tiers_data.json`.

## How to run on Replit
`DISCORD_TOKEN` is already set as a Replit secret. The **Start application** workflow runs:
```
pip install -r requirements.txt -q && python main.py
```
This single process logs the Discord bot in AND serves the website on port 5000 (visible in the Replit preview pane).

Note: `railway_server.py`, `Procfile`, and `railway.json` are leftovers from a previous Railway deployment and are not used on Replit.

## User preferences
- After committing changes to Discord bot code/commands (`main.py`, `config.py`, `requirements.txt`), always run `bash push_to_github.sh "<commit message>"` so those changes are pushed to the `Discord-bot` GitHub repo (and `AFTERSHOCK-TIERS`).
- After committing changes to website/player data (`index.html`, `tiers_data.json`, `static/`), always run the same script so those changes are pushed to the `INDEX` GitHub repo (connected to Netlify).
- Do this automatically after relevant changes — don't wait to be asked to push each time.
