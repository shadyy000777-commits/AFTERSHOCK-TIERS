#!/bin/bash
# Push current Replit state to GitHub (AFTERSHOCK-TIERS only)
# Railway auto-deploys from this repo — pushing here is all that's needed.
set -e

git config credential.helper store
git config user.email "aftershock@replit.com"
git config user.name "Aftershock Bot"

COMMIT_MSG="${1:-Update from Replit}"

# NOTE: root-level tiers_data.json, index.html, static/ and skins/ are live-synced
# directly by the running bot via the GitHub Contents API on every change — those files
# must NEVER be committed/pushed here or they would overwrite live production data.
#
# website/index.html and website/static/ are the Railway-served copies and must be
# included so Railway's site reflects any markup/design changes.

CODE_FILES="main.py config.py requirements.txt railway_server.py Procfile railway.json nixpacks.toml runtime.txt requirements-web.txt push_to_github.sh replit.md website/index.html website/static"

echo "▶ Pushing to AFTERSHOCK-TIERS (Railway auto-deploys on push)..."
git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/shadyy000777-commits/AFTERSHOCK-TIERS

# Stash local uncommitted changes, pull latest, then re-apply
git stash 2>/dev/null || true
git fetch origin main
git reset --hard origin/main
git stash pop 2>/dev/null || true

git add -- $CODE_FILES
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    echo "✅ Committed: $COMMIT_MSG"
else
    echo "ℹ️  Nothing new to commit."
fi

git push origin main
echo "✅ Pushed to AFTERSHOCK-TIERS — Railway will deploy automatically."
