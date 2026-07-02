Here you go! Copy everything below:

```python
"""
MCTiers Discord Bot
===================
Replicates the MCTiers tier testing system for Minecraft PvP players.
Supports slash commands and prefix commands (!).

Setup:
  pip install discord.py python-dotenv aiohttp
  Create .env with DISCORD_TOKEN=your_token_here
  python bot.py
"""

import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import json
import random
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_TOKEN_HERE")

TIERS = {
    "HT1": {"label": "High Tier 1", "color": 0xFF0000, "emoji": "🔴", "rank": 1},
    "HT2": {"label": "High Tier 2", "color": 0xFF4500, "emoji": "🟠", "rank": 2},
    "HT3": {"label": "High Tier 3", "color": 0xFF8C00, "emoji": "🟡", "rank": 3},
    "T1":  {"label": "Tier 1",      "color": 0xFFD700, "emoji": "⭐", "rank": 4},
    "T2":  {"label": "Tier 2",      "color": 0xADFF2F, "emoji": "🟢", "rank": 5},
    "T3":  {"label": "Tier 3",      "color": 0x00CED1, "emoji": "🔵", "rank": 6},
    "T4":  {"label": "Tier 4",      "color": 0x6495ED, "emoji": "💙", "rank": 7},
    "T5":  {"label": "Tier 5",      "color": 0x9370DB, "emoji": "🟣", "rank": 8},
    "LT":  {"label": "Low Tier",    "color": 0x808080, "emoji": "⚪", "rank": 9},
    "UT":  {"label": "Untiered",    "color": 0x5C5C5C, "emoji": "⬛", "rank": 10},
}

GAMEMODES = {
    "crystal": "Crystal PvP",
    "sword":   "Sword PvP",
    "uhc":     "UHC PvP",
    "pot":     "Potion PvP",
    "axe":     "Axe PvP",
    "smp":     "SMP PvP",
    "bedwars": "Bed Wars",
    "nodebuff":"No Debuff",
}

player_db: dict[int, dict] = {}
test_sessions: dict[int, dict] = {}
cooldowns: dict[int, datetime] = {}
COOLDOWN_MINUTES = 30


def default_player(user: discord.User) -> dict:
    return {
        "discord_id": user.id,
        "username": str(user),
        "ign": None,
        "tiers": {},
        "tests_taken": 0,
        "joined": datetime.utcnow().isoformat(),
        "last_updated": datetime.utcnow().isoformat(),
    }


def get_player(user: discord.User) -> dict:
    if user.id not in player_db:
        player_db[user.id] = default_player(user)
    return player_db[user.id]


TIER_QUESTIONS: dict[str, list[dict]] = {
    "crystal": [
        {"q": "Can you consistently place end crystals on obsidian while being attacked?",           "weight": 2},
        {"q": "Do you understand anchor mechanics and how to anti-anchor efficiently?",              "weight": 2},
        {"q": "Can you perform a clean one-cycle on a player with full absorption?",                 "weight": 3},
        {"q": "Do you know how to properly hold a totem while offhanding a crystal?",               "weight": 1},
        {"q": "Can you read and predict enemy crystal placements mid-fight?",                        "weight": 2},
        {"q": "How well do you manage your surround game under pressure?",                           "weight": 2},
    ],
    "sword": [
        {"q": "Can you consistently land W-tap combos while maintaining CPS above 12?",             "weight": 2},
        {"q": "Do you know how to jitter-click without hand strain for extended fights?",            "weight": 1},
        {"q": "Can you read an opponent's hit timing to land knockback-heavy hits?",                 "weight": 3},
        {"q": "How well do you manage sprint-reset mechanics mid-combo?",                            "weight": 2},
        {"q": "Do you understand and use strafing patterns to dodge enemy attacks?",                 "weight": 2},
        {"q": "Can you perform butterfly or drag-clicking reliably in a fight?",                     "weight": 1},
    ],
    "uhc": [
        {"q": "Do you know the optimal gear progression for golden apple timing?",                   "weight": 2},
        {"q": "Can you consistently hit flint-and-steel traps against moving targets?",             "weight": 2},
        {"q": "How well do you manage bow + sword switching in mid-range fights?",                   "weight": 3},
        {"q": "Can you read a player's health and adjust aggression accordingly?",                   "weight": 2},
        {"q": "Do you understand pearl-catch mechanics and strafing under arrows?",                  "weight": 2},
        {"q": "How confident are you at gap-click (golden apple) timing during fights?",            "weight": 2},
    ],
    "pot": [
        {"q": "Can you pot-clutch below 3 hearts consistently in a 1v1?",                           "weight": 3},
        {"q": "Do you know the optimal potion order for maximum survivability?",                     "weight": 2},
        {"q": "Can you track both your potions and the enemy's simultaneously?",                     "weight": 2},
        {"q": "How well do you manage distance to control when the opponent can pot?",               "weight": 2},
        {"q": "Do you use terrain to block line-of-sight while potting?",                            "weight": 2},
        {"q": "Can you juggle a sword and potion swap without losing aggression?",                   "weight": 2},
    ],
    "axe": [
        {"q": "Do you understand axe durability and when to switch mid-fight?",                     "weight": 1},
        {"q": "Can you time shield-disables consistently with axe hits?",                            "weight": 3},
        {"q": "How well do you use axes combined with crossbow snipes?",                             "weight": 2},
        {"q": "Do you incorporate critical hits effectively to maximize DPS?",                       "weight": 2},
        {"q": "Can you handle a sword player who keeps distance?",                                   "weight": 2},
        {"q": "How well do you manage shield-break timing under pressure?",                         "weight": 3},
    ],
    "smp": [
        {"q": "Can you fight in mixed-gear scenarios (full netherite vs iron)?",                    "weight": 2},
        {"q": "Do you understand knockback reduction and how armor affects it?",                    "weight": 1},
        {"q": "Can you effectively use totems of undying in live scenarios?",                       "weight": 3},
        {"q": "How well do you adapt to different weapon types mid-fight?",                         "weight": 2},
        {"q": "Do you use environment and terrain to your advantage in SMP fights?",                "weight": 2},
        {"q": "Can you manage inventory quickly during a fight?",                                   "weight": 1},
    ],
    "bedwars": [
        {"q": "Can you consistently rush a bed with limited resources?",                            "weight": 2},
        {"q": "Do you know optimal bridge techniques for speed and safety?",                        "weight": 2},
        {"q": "How well do you prioritize targets in a multi-team fight?",                          "weight": 3},
        {"q": "Can you effectively defend your bed against various rush strategies?",               "weight": 2},
        {"q": "Do you manage resources (iron, gold, diamonds) efficiently during a game?",         "weight": 2},
        {"q": "Can you adapt mid-game when your team is eliminated?",                               "weight": 2},
    ],
    "nodebuff": [
        {"q": "Can you pot accurately under fire without missing throws?",                          "weight": 3},
        {"q": "Do you know the no-debuff server-specific mechanics and meta?",                      "weight": 2},
        {"q": "How well do you manage spacing to control the fight tempo?",                        "weight": 2},
        {"q": "Can you read and counter opponents who use fishing rod combos?",                    "weight": 2},
        {"q": "Do you use knockback potions effectively as a tool?",                               "weight": 2},
        {"q": "How consistent are you at hitting enemies during their pot animations?",            "weight": 2},
    ],
}

SCORE_RESPONSES = {
    (0,  30):  "UT",
    (30, 45):  "LT",
    (45, 55):  "T5",
    (55, 63):  "T4",
    (63, 70):  "T3",
    (70, 77):  "T2",
    (77, 83):  "T1",
    (83, 89):  "HT3",
    (89, 95):  "HT2",
    (95, 101): "HT1",
}

ANSWER_SCORES = {
    "yes":        100,
    "mostly":     80,
    "sometimes":  60,
    "rarely":     35,
    "no":         10,
    "unsure":     45,
}

ANSWER_ALIASES = {
    "y": "yes", "n": "no", "m": "mostly", "s": "sometimes",
    "r": "rarely", "u": "unsure", "idk": "unsure",
    "ye": "yes", "nah": "no", "nope": "no", "yep": "yes",
}

TIER_FLAVOR: dict[str, str] = {
    "HT1": "Absolutely elite. You play at the highest competitive level.",
    "HT2": "Near the top. Very strong fundamentals with excellent execution.",
    "HT3": "High-tier player. Consistently strong in most matchups.",
    "T1":  "Top of the mid-tier range. Solid mechanics with room to grow.",
    "T2":  "Competent fighter. You hold your own in most lobbies.",
    "T3":  "Developing player. The fundamentals are there, keep grinding.",
    "T4":  "Early intermediate. Focus on consistency and mechanic practice.",
    "T5":  "Learning the ropes. Keep watching VODs and practicing daily.",
    "LT":  "Low tier. Don't be discouraged — everyone starts somewhere.",
    "UT":  "Untiered. Practice the basics and come back to retest soon!",
}


def score_to_tier(score: float) -> str:
    for (lo, hi), tier in SCORE_RESPONSES.items():
        if lo <= score < hi:
            return tier
    return "UT"


def calculate_tier(answers: list[tuple[str, int]]) -> tuple[str, float]:
    if not answers:
        return "UT", 0.0
    total_weight = sum(w for _, w in answers)
    weighted_score = sum(ANSWER_SCORES.get(a, 45) * w for a, w in answers)
    raw = (weighted_score / total_weight) if total_weight else 0
    variance = random.uniform(-3, 3)
    final = max(0, min(100, raw + variance))
    return score_to_tier(final), round(final, 1)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
tree = bot.tree


def tier_embed(tier_key: str, score: float, gamemode: str, username: str) -> discord.Embed:
    t = TIERS[tier_key]
    gm_label = GAMEMODES.get(gamemode, gamemode.title())
    embed = discord.Embed(
        title=f"{t['emoji']} {t['label']} — {gm_label}",
        description=TIER_FLAVOR[tier_key],
        color=t["color"],
        timestamp=datetime.utcnow(),
    )
    embed.set_author(name=f"MCTiers Result for {username}")
    embed.add_field(name="Tier",     value=f"`{tier_key}`",        inline=True)
    embed.add_field(name="Score",    value=f"`{score}/100`",       inline=True)
    embed.add_field(name="Gamemode", value=f"`{gm_label}`",        inline=True)
    embed.set_footer(text="MCTiers Bot • Results are based on self-reported skill")
    return embed


def profile_embed(player: dict, user: discord.User) -> discord.Embed:
    embed = discord.Embed(
        title=f"📋 Tier Profile — {player['username']}",
        color=0x2F3136,
        timestamp=datetime.utcnow(),
    )
    if player["ign"]:
        embed.add_field(name="Minecraft IGN", value=f"`{player['ign']}`", inline=False)
    if player["tiers"]:
        lines = []
        for gm, tk in sorted(player["tiers"].items()):
            t = TIERS.get(tk, TIERS["UT"])
            gm_label = GAMEMODES.get(gm, gm.title())
            lines.append(f"{t['emoji']} **{gm_label}** — `{tk}` ({t['label']})")
        embed.add_field(name="Tier Ratings", value="\n".join(lines), inline=False)
    else:
        embed.add_field(name="Tier Ratings", value="No tiers yet. Use `/test` to get rated!", inline=False)
    embed.add_field(name="Tests Taken", value=str(player["tests_taken"]), inline=True)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text="MCTiers Bot")
    return embed


def help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🎮 MCTiers Bot — Help",
        description="Tier testing system inspired by MCTiers. Get rated in various Minecraft PvP gamemodes!",
        color=0x5865F2,
    )
    embed.add_field(
        name="📌 Slash Commands",
        value=(
            "`/test <gamemode>` — Start a tier test\n"
            "`/profile [@user]` — View tier profile\n"
            "`/leaderboard <gamemode>` — Top players\n"
            "`/setign <name>` — Set your Minecraft IGN\n"
            "`/tiers` — List all tiers\n"
            "`/gamemodes` — List all gamemodes\n"
            "`/help` — Show this message"
        ),
        inline=False,
    )
    embed.add_field(
        name="⌨️ Prefix Commands (!)",
        value=(
            "`!test <gamemode>` — Start a tier test\n"
            "`!profile [@user]` — View tier profile\n"
            "`!lb <gamemode>` — Leaderboard\n"
            "`!tiers` — List all tiers"
        ),
        inline=False,
    )
    embed.add_field(
        name="🎯 Gamemodes",
        value=" | ".join(f"`{gm}`" for gm in GAMEMODES),
        inline=False,
    )
    embed.add_field(
        name="💬 During a Test",
        value=(
            "Answer each question with:\n"
            "`yes` / `mostly` / `sometimes` / `rarely` / `no` / `unsure`\n"
            "Or short forms: `y`, `m`, `s`, `r`, `n`, `u`\n\n"
            "Type `cancel` at any time to abort the test."
        ),
        inline=False,
    )
    embed.set_footer(text="MCTiers Bot • Inspired by mctiers.com")
    return embed


def tiers_list_embed() -> discord.Embed:
    embed = discord.Embed(title="🏆 MCTiers — Tier List", color=0xFFD700)
    for key, data in TIERS.items():
        embed.add_field(
            name=f"{data['emoji']} {key} — {data['label']}",
            value=TIER_FLAVOR[key],
            inline=False,
        )
    return embed


async def run_test_session(user: discord.User, gamemode: str, channel: discord.abc.Messageable):
    uid = user.id
    if uid in cooldowns:
        remaining = cooldowns[uid] + timedelta(minutes=COOLDOWN_MINUTES) - datetime.utcnow()
        if remaining.total_seconds() > 0:
            mins = int(remaining.total_seconds() // 60) + 1
            await channel.send(
                embed=discord.Embed(
                    title="⏳ Cooldown Active",
                    description=f"Please wait **{mins} minute(s)** before testing again.",
                    color=0xFF4500,
                )
            )
            return
    if uid in test_sessions:
        await channel.send("❌ You already have an active test session. Type `cancel` to abort it.")
        return
    questions = TIER_QUESTIONS.get(gamemode)
    if not questions:
        await channel.send(f"❌ Unknown gamemode `{gamemode}`. Use `/gamemodes` to see available options.")
        return
    gm_label = GAMEMODES[gamemode]
    test_sessions[uid] = {"gamemode": gamemode, "answers": [], "q_index": 0, "channel": channel}
    intro = discord.Embed(
        title=f"🧪 Tier Test — {gm_label}",
        description=(
            f"Starting your **{gm_label}** tier test, {user.mention}!\n\n"
            f"You'll be asked **{len(questions)} questions**. Answer honestly for accurate results.\n\n"
            "**Valid answers:** `yes` · `mostly` · `sometimes` · `rarely` · `no` · `unsure`\n"
            "Type `cancel` at any time to stop."
        ),
        color=0x5865F2,
    )
    intro.set_footer(text="MCTiers Bot • Answer honestly for accurate results")
    await channel.send(embed=intro)
    await asyncio.sleep(1.5)
    await ask_question(user, channel, questions, 0)


async def ask_question(user: discord.User, channel: discord.abc.Messageable, questions: list, index: int):
    q = questions[index]
    embed = discord.Embed(
        title=f"Question {index + 1} / {len(questions)}",
        description=f"**{q['q']}**",
        color=0x3498DB,
    )
    embed.set_footer(text="yes · mostly · sometimes · rarely · no · unsure")
    await channel.send(embed=embed)


async def process_test_answer(message: discord.Message):
    uid = message.author.id
    if uid not in test_sessions:
        return False
    session = test_sessions[uid]
    content = message.content.strip().lower()
    if content == "cancel":
        del test_sessions[uid]
        await message.channel.send(
            embed=discord.Embed(
                title="❌ Test Cancelled",
                description="Your tier test has been cancelled. Use `/test` to start a new one.",
                color=0xFF0000,
            )
        )
        return True
    answer = ANSWER_ALIASES.get(content, content)
    if answer not in ANSWER_SCORES:
        await message.channel.send(
            f"⚠️ Invalid answer. Please reply with: `yes`, `mostly`, `sometimes`, `rarely`, `no`, or `unsure`"
        )
        return True
    gamemode = session["gamemode"]
    questions = TIER_QUESTIONS[gamemode]
    q_index = session["q_index"]
    weight = questions[q_index]["weight"]
    session["answers"].append((answer, weight))
    session["q_index"] += 1
    progress = "▓" * (session["q_index"]) + "░" * (len(questions) - session["q_index"])
    await message.add_reaction("✅")
    if session["q_index"] >= len(questions):
        answers = session["answers"]
        del test_sessions[uid]
        cooldowns[uid] = datetime.utcnow()
        tier_key, score = calculate_tier(answers)
        player = get_player(message.author)
        player["tiers"][gamemode] = tier_key
        player["tests_taken"] += 1
        player["last_updated"] = datetime.utcnow().isoformat()
        result_embed = tier_embed(tier_key, score, gamemode, str(message.author))
        result_embed.add_field(
            name="Progress",
            value=f"`[{progress}]`",
            inline=False,
        )
        await message.channel.send(
            content=f"🎉 Test complete, {message.author.mention}!",
            embed=result_embed,
        )
    else:
        await ask_question(message.author, message.channel, questions, session["q_index"])
    return True


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await tree.sync()
    print("✅ Slash commands synced")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="MCTiers | /help"
        )
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    handled = await process_test_answer(message)
    if not handled:
        await bot.process_commands(message)


@tree.command(name="help", description="Show all bot commands and how to use them")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=help_embed(), ephemeral=True)


@tree.command(name="tiers", description="View the full tier list with descriptions")
async def slash_tiers(interaction: discord.Interaction):
    await interaction.response.send_message(embed=tiers_list_embed())


@tree.command(name="gamemodes", description="List all available gamemodes for tier testing")
async def slash_gamemodes(interaction: discord.Interaction):
    embed = discord.Embed(title="🎮 Available Gamemodes", color=0x00CED1)
    for key, label in GAMEMODES.items():
        qs = len(TIER_QUESTIONS.get(key, []))
        embed.add_field(name=f"`{key}`", value=f"{label} ({qs} questions)", inline=True)
    await interaction.response.send_message(embed=embed)


@tree.command(name="test", description="Start a tier test for a specific gamemode")
@app_commands.describe(gamemode="The gamemode to be tested in (e.g. crystal, sword, uhc)")
async def slash_test(interaction: discord.Interaction, gamemode: str):
    gamemode = gamemode.lower().strip()
    if gamemode not in GAMEMODES:
        gm_list = ", ".join(f"`{g}`" for g in GAMEMODES)
        await interaction.response.send_message(
            f"❌ `{gamemode}` is not a valid gamemode.\n**Available:** {gm_list}",
            ephemeral=True,
        )
        return
    await interaction.response.send_message(
        f"🧪 Starting your **{GAMEMODES[gamemode]}** tier test...", ephemeral=False
    )
    await run_test_session(interaction.user, gamemode, interaction.channel)


@tree.command(name="profile", description="View your tier profile or another user's")
@app_commands.describe(user="The Discord user to look up (leave blank for yourself)")
async def slash_profile(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    player = get_player(target)
    await interaction.response.send_message(embed=profile_embed(player, target))


@tree.command(name="setign", description="Set your Minecraft in-game name")
@app_commands.describe(ign="Your Minecraft username")
async def slash_setign(interaction: discord.Interaction, ign: str):
    if len(ign) > 16 or not ign.replace("_", "").isalnum():
        await interaction.response.send_message("❌ Invalid IGN. Must be 1-16 alphanumeric characters.", ephemeral=True)
        return
    player = get_player(interaction.user)
    player["ign"] = ign
    await interaction.response.send_message(
        embed=discord.Embed(
            title="✅ IGN Updated",
            description=f"Your Minecraft IGN has been set to `{ign}`.",
            color=0x57F287,
        ),
        ephemeral=True,
    )


@tree.command(name="leaderboard", description="View the top tiered players for a gamemode")
@app_commands.describe(gamemode="The gamemode leaderboard to view")
async def slash_leaderboard(interaction: discord.Interaction, gamemode: str):
    gamemode = gamemode.lower().strip()
    if gamemode not in GAMEMODES:
        await interaction.response.send_message(f"❌ Unknown gamemode `{gamemode}`.", ephemeral=True)
        return
    ranked = [
        (uid, data) for uid, data in player_db.items()
        if gamemode in data.get("tiers", {})
    ]
    ranked.sort(key=lambda x: TIERS.get(x[1]["tiers"][gamemode], {}).get("rank", 99))
    gm_label = GAMEMODES[gamemode]
    embed = discord.Embed(title=f"🏆 Leaderboard — {gm_label}", color=0xFFD700)
    if not ranked:
        embed.description = "No players have been tiered in this gamemode yet!"
    else:
        lines = []
        medals = ["🥇", "🥈", "🥉"]
        for i, (uid, data) in enumerate(ranked[:10]):
            tier_key = data["tiers"][gamemode]
            t = TIERS.get(tier_key, TIERS["UT"])
            medal = medals[i] if i < 3 else f"`#{i+1}`"
            name = data.get("ign") or data.get("username", f"User#{uid}")
            lines.append(f"{medal} {t['emoji']} **{name}** — `{tier_key}`")
        embed.description = "\n".join(lines)
    await interaction.response.send_message(embed=embed)


@tree.command(name="compare", description="Compare your tier with another user")
@app_commands.describe(user="The user to compare with", gamemode="The gamemode to compare")
async def slash_compare(interaction: discord.Interaction, user: discord.Member, gamemode: str):
    gamemode = gamemode.lower().strip()
    if gamemode not in GAMEMODES:
        await interaction.response.send_message(f"❌ Unknown gamemode `{gamemode}`.", ephemeral=True)
        return
    p1 = get_player(interaction.user)
    p2 = get_player(user)
    gm_label = GAMEMODES[gamemode]
    t1_key = p1["tiers"].get(gamemode)
    t2_key = p2["tiers"].get(gamemode)
    embed = discord.Embed(title=f"⚔️ Comparison — {gm_label}", color=0xE91E63)
    def fmt(player, tk):
        if not tk:
            return "*(Not tiered)*"
        t = TIERS[tk]
        return f"{t['emoji']} `{tk}` — {t['label']}"
    embed.add_field(name=str(interaction.user), value=fmt(p1, t1_key), inline=True)
    embed.add_field(name="VS", value="⚔️", inline=True)
    embed.add_field(name=str(user), value=fmt(p2, t2_key), inline=True)
    if t1_key and t2_key:
        r1 = TIERS[t1_key]["rank"]
        r2 = TIERS[t2_key]["rank"]
        if r1 < r2:
            winner = interaction.user.mention
        elif r2 < r1:
            winner = user.mention
        else:
            winner = "It's a **tie**!"
        embed.add_field(name="Result", value=f"🏆 {winner} ranks higher!", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.command(name="test")
async def prefix_test(ctx: commands.Context, gamemode: str = None):
    if not gamemode:
        await ctx.send("Usage: `!test <gamemode>` — e.g. `!test crystal`")
        return
    gamemode = gamemode.lower()
    if gamemode not in GAMEMODES:
        await ctx.send(f"❌ Unknown gamemode. Use `!gamemodes` for the list.")
        return
    await run_test_session(ctx.author, gamemode, ctx.channel)


@bot.command(name="profile")
async def prefix_profile(ctx: commands.Context, user: discord.Member = None):
    target = user or ctx.author
    player = get_player(target)
    await ctx.send(embed=profile_embed(player, target))


@bot.command(name="tiers")
async def prefix_tiers(ctx: commands.Context):
    await ctx.send(embed=tiers_list_embed())


@bot.command(name="gamemodes")
async def prefix_gamemodes(ctx: commands.Context):
    await ctx.send(embed=discord.Embed(
        title="🎮 Gamemodes",
        description="\n".join(f"`{k}` — {v}" for k, v in GAMEMODES.items()),
        color=0x00CED1,
    ))


@bot.command(name="lb")
async def prefix_lb(ctx: commands.Context, gamemode: str = None):
    if not gamemode:
        await ctx.send("Usage: `!lb <gamemode>`")
        return
    gamemode = gamemode.lower()
    if gamemode not in GAMEMODES:
        await ctx.send(f"❌ Unknown gamemode `{gamemode}`.")
        return
    ranked = [
        (uid, data) for uid, data in player_db.items()
        if gamemode in data.get("tiers", {})
    ]
    ranked.sort(key=lambda x: TIERS.get(x[1]["tiers"][gamemode], {}).get("rank", 99))
    gm_label = GAMEMODES[gamemode]
    embed = discord.Embed(title=f"🏆 Leaderboard — {gm_label}", color=0xFFD700)
    if not ranked:
        embed.description = "No players tiered yet!"
    else:
        lines = []
        medals = ["🥇", "🥈", "🥉"]
        for i, (uid, data) in enumerate(ranked[:10]):
            tk = data["tiers"][gamemode]
            t = TIERS.get(tk, TIERS["UT"])
            medal = medals[i] if i < 3 else f"`#{i+1}`"
            name = data.get("ign") or data.get("username", f"User#{uid}")
            lines.append(f"{medal} {t['emoji']} **{name}** — `{tk}`")
        embed.description = "\n".join(lines)
    await ctx.send(embed=embed)


@bot.command(name="help")
async def prefix_help(ctx: commands.Context):
    await ctx.send(embed=help_embed())


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument. Use `!help` for usage info.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"⚠️ An error occurred: `{error}`")


if __name__ == "__main__":
    if TOKEN == "MTUxMjc3MTM5MDE3MDczMDU5NA.GNYWoC.2ap7zW1pO5RQzhXPpibj5j5hmGTuc3fz2dMSX4":
        print("⚠️  No token found! Set DISCORD_TOKEN in your .env file.")
    else:
        bot.run(TOKEN)
