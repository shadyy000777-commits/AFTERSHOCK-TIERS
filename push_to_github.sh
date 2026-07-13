#!/bin/bash
# Push current Replit state to GitHub
set -e

# Configure git identity (no credential.helper — we pass tokens only inline, per-push, never stored on disk)
git config user.email "aftershock@replit.com"
git config user.name "Aftershock Bot"

COMMIT_MSG="${1:-Update from Replit}"

# ── 1. Push full bot to AFTERSHOCK-TIERS ────────────────────────────────────
echo "▶ Pushing to AFTERSHOCK-TIERS..."
AFTERSHOCK_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/shadyy000777-commits/AFTERSHOCK-TIERS"
if ! git diff --quiet || ! git diff --cached --quiet || git ls-files --others --exclude-standard | grep -q .; then
    git add -A
    git commit -m "$COMMIT_MSG"
    echo "✅ Committed: $COMMIT_MSG"
else
    echo "ℹ️  Nothing new to commit."
fi
git push --force "$AFTERSHOCK_URL" main:main
echo "✅ Pushed to AFTERSHOCK-TIERS"

# ── 2. Push website files to INDEX (connected to Netlify) ───────────────────
echo ""
echo "▶ Pushing website files to INDEX..."
INDEX_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/shadyy000777-commits/INDEX"

# Fetch current INDEX state
git fetch "$INDEX_URL" main 2>/dev/null

# Create a temporary branch from INDEX main
git checkout -b _index-push FETCH_HEAD 2>/dev/null

# Overlay the latest website files from main
git checkout main -- index.html tiers_data.json static/

# Commit and push
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    git push "$INDEX_URL" _index-push:main --force
    echo "✅ Pushed website files to INDEX → Netlify will redeploy"
else
    echo "ℹ️  No website changes to push to INDEX."
fi

# Clean up temp branch
git checkout main
git branch -D _index-push 2>/dev/null || true

# ── 3. Push bot code files to Discord-bot repo ──────────────────────────────
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
