# MCTiers Discord Bot

A self-contained Discord bot that replicates the MCTiers tier testing system for Minecraft PvP players. Supports slash commands and `!` prefix commands.

## Stack
- Python 3.12
- discord.py — slash commands, prefix commands, embeds
- python-dotenv — loads `DISCORD_TOKEN` from environment
- aiohttp — async HTTP

## Required secrets
- `DISCORD_TOKEN` — Discord bot token (required to run)

## Features
- `/test <gamemode>` — interactive tier test (crystal, sword, uhc, pot, axe, smp, bedwars, nodebuff)
- `/profile` — view tier profile
- `/leaderboard <gamemode>` — top tiered players
- `/setign <name>` — set Minecraft IGN
- `/tiers`, `/gamemodes`, `/help`
- Prefix equivalents: `!test`, `!profile`, `!lb`, `!tiers`

## How to run
Set `DISCORD_TOKEN` as a Replit secret, then start the **Start application** workflow.

```
pip install -r requirements.txt
python main.py
```

## User preferences
