# Discord Bot

A Python Discord bot using discord.py with a Flask keep-alive web server.

## Stack
- Python 3.12
- discord.py — slash commands, image card generation
- Flask + waitress — keep-alive HTTP server
- aiohttp, Pillow, pilmoji — HTTP requests and image rendering

## Required secrets
- `DISCORD_TOKEN` — Discord bot token (required to run)
- `GITHUB_TOKEN` — GitHub personal access token (optional; used to sync `tiers_data.json` to GitHub)

## Missing before running
- `config.py` — imported by `main.py` but not present in the repo. It must export:
  `TIERS`, `GAMEMODE_EMOJIS`, `GAMEMODE_ABBREV`, `REGION_COLORS`, `CARD_BG`, `CARD_HEADER`,
  `CARD_ACCENT`, `CARD_CIRCLE_FILL`, `CARD_CIRCLE_BORDER_LT`, `CARD_DIVIDER`, `CARD_TEXT_WHITE`,
  `CARD_TEXT_GREY`, `CARD_EMOJI_SIZE`, `QUEUE_TIMEOUT_SECONDS`, `FONT_BOLD`, `FONT_REGULAR`,
  `TIER_POINTS`, `OVERALL_RANKS`

## How to run
```
pip install -r requirements.txt
python main.py
```

## User preferences
