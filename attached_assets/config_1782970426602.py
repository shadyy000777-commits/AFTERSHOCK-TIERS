# ═══════════════════════════════════════════════════════════════
#  AFTERSHOCK TIERS — config.py
#  Edit this file to customise the bot.  No need to touch main.py.
# ═══════════════════════════════════════════════════════════════


# ── TIER SYSTEM ─────────────────────────────────────────────────
# List of all valid tiers, highest to lowest.
# Add or remove tiers here as needed.
TIERS = ["HT1", "HT2", "HT3", "HT4", "HT5", "LT1", "LT2", "LT3", "LT4", "LT5"]


# ── GAMEMODES ───────────────────────────────────────────────────
# Maps gamemode name → emoji shown in /panel buttons and profile circles.
# The name must match exactly what you type in /addgamemode.
# You can also add/change emojis live with /addgamemode.
GAMEMODE_EMOJIS = {
    "Sword":   "<:Sword_smooth:1512168702362255380>",
    "Axe":     "<:axe1:1500454383681273986>",
    "NethOP":  "<:nethpot:1466808945522770132>",
    "UHC":     "<:uhc:1512169002082762912>",
    "SMP":     "<:SMP:1512168820830109858>",
    "Pot":     "<:diapot_icon:1512168870922948848>",
    "Mace":    "<:mace1:1466809319810142260>",
    "Crystal": "<:Crystal:1512168746918084679>",
    "Vanilla": "<:Crystal:1512168746918084679>",
}

# Fallback 2-letter abbreviation shown in profile circles
# if no emoji image can be fetched for that gamemode.
GAMEMODE_ABBREV = {
    "mace":    "MC",
    "nethop":  "NO",
    "sword":   "SW",
    "axe":     "AX",
    "uhc":     "UH",
    "pot":     "PT",
    "smp":     "SM",
    "vanilla": "VA",
    "cart":    "CA",
    "dia smp": "DS",
    "crystal": "CR",
}


# ── REGIONS ─────────────────────────────────────────────────────
# Badge colour (R, G, B) for each region code on the profile card.
# Add new regions or change colours freely.
REGION_COLORS = {
    "NA":  (139, 28,  28),   # red
    "EU":  (28,  68,  139),  # blue
    "AS":  (28,  115, 65),   # green
    "OCE": (88,  38,  139),  # purple
    "SA":  (139, 88,  28),   # orange
}


# ── PROFILE CARD COLOURS ────────────────────────────────────────
# All values are (R, G, B) tuples.
CARD_BG                = (18,  20,  30)   # main dark background
CARD_HEADER            = (26,  30,  44)   # lighter top-half strip
CARD_ACCENT            = (240, 168,  0)   # gold diagonal + HT tier text
CARD_CIRCLE_FILL       = (34,  38,  54)   # gamemode circle background
CARD_CIRCLE_BORDER_LT  = (52,  56,  74)   # LT tier circle outline colour
CARD_DIVIDER           = (44,  48,  66)   # horizontal dividing line
CARD_TEXT_WHITE        = (255, 255, 255)
CARD_TEXT_GREY         = (120, 125, 148)  # subtitles, LT tier labels

# Size of the emoji image pasted inside each gamemode circle (pixels).
CARD_EMOJI_SIZE = 28


# ── TIER POINTS ─────────────────────────────────────────────────
# Points awarded per tier on the website leaderboard.
TIER_POINTS = {
    "HT1": 100, "LT1": 90,
    "HT2": 80,  "LT2": 70,
    "HT3": 60,  "LT3": 50,
    "HT4": 40,  "LT4": 30,
    "HT5": 20,  "LT5": 10,
}

# ── OVERALL RANKS ────────────────────────────────────────────────
# Thresholds for the overall rank badge shown on each player card.
# Format: (min_points, label, bg_hex, text_hex)
OVERALL_RANKS = [
    (700, "Conquered",        "#ff6b35", "#fff0e8"),
    (500, "Combat Master",   "#c8960a", "#fff8e0"),
    (300, "Combat Ace",      "#5b8dee", "#e8f0ff"),
    (175, "Combat Specialist","#3cde7e", "#e0fff0"),
    (75,  "Combat Cadet",    "#a060ff", "#f0e8ff"),
    (1,   "Rookie",          "#50566e", "#c8cce0"),
]

# ── QUEUE ───────────────────────────────────────────────────────
# How many seconds a /queue stays open before it auto-closes.
QUEUE_TIMEOUT_SECONDS = 180   # 180 = 3 minutes


# ── FONTS ───────────────────────────────────────────────────────
# Paths to fonts used on the profile card.
# These are the system DejaVu fonts — change only if you install a custom font.
FONT_BOLD    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
