#!/bin/bash
# Push current Replit state to GitHub
set -e

# Configure git credentials
git config credential.helper store
git config user.email "aftershock@replit.com"
git config user.name "Aftershock Bot"

COMMIT_MSG="${1:-Update from Replit}"

# NOTE: tiers_data.json, index.html, static/ and skins/ are live-synced directly
# by the running bot via the GitHub Contents API on every change (see
# _push_data_to_github / _push_website_to_github / _push_image_to_github in main.py).
# This script must NEVER commit or push those files — doing so would force-push this
# dev workspace's stale local copies over the production data the live bot just wrote,
# effectively reverting test submissions on the website. Only code files are synced here.

CODE_FILES="main.py config.py requirements.txt railway_server.py Procfile railway.json nixpacks.toml runtime.txt requirements-web.txt push_to_github.sh replit.md"

# ── 1. Push bot code to AFTERSHOCK-TIERS ────────────────────────────────────
echo "▶ Pushing to AFTERSHOCK-TIERS..."
git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/shadyy000777-commits/AFTERSHOCK-TIERS
git add -- $CODE_FILES
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    echo "✅ Committed: $COMMIT_MSG"
else
    echo "ℹ️  Nothing new to commit."
fi
git push origin main
echo "✅ Pushed to AFTERSHOCK-TIERS"

# ── 2. Push bot code files to Discord-bot repo ──────────────────────────────
echo ""
echo "▶ Pushing bot files to Discord-bot..."
DISCORD_BOT_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/shadyy000777-commits/Discord-bot"

# Fetch current Discord-bot state
git fetch "$DISCORD_BOT_URL" main 2>/dev/null || git fetch "$DISCORD_BOT_URL" master 2>/dev/null || true

# Create a temporary branch from Discord-bot main (or orphan if repo is empty)
if git fetch "$DISCORD_BOT_URL" main 2>/dev/null; then
    git checkout -b _discordbot-push FETCH_HEAD 2>/dev/null
else
    git checkout --orphan _discordbot-push
    git rm -rf . --quiet 2>/dev/null || true
fi

# Overlay the latest bot files from main
git checkout main -- main.py config.py requirements.txt

# Commit and push
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    git push "$DISCORD_BOT_URL" _discordbot-push:main --force
    echo "✅ Pushed main.py, config.py, requirements.txt to Discord-bot"
else
    echo "ℹ️  No bot file changes to push to Discord-bot."
fi

# Clean up temp branch
git checkout main
git branch -D _discordbot-push 2>/dev/null || true
