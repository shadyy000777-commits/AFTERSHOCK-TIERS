#!/bin/bash
# Push current Replit state to GitHub
set -e

# Configure git credentials
git config credential.helper store
git config user.email "aftershock@replit.com"
git config user.name "Aftershock Bot"

COMMIT_MSG="${1:-Update from Replit}"

# ── 1. Push full bot to AFTERSHOCK-TIERS ────────────────────────────────────
echo "▶ Pushing to AFTERSHOCK-TIERS..."
git remote set-url origin https://github.com/shadyy000777-commits/AFTERSHOCK-TIERS
if ! git diff --quiet || ! git diff --cached --quiet || git ls-files --others --exclude-standard | grep -q .; then
    git add -A
    git commit -m "$COMMIT_MSG"
    echo "✅ Committed: $COMMIT_MSG"
else
    echo "ℹ️  Nothing new to commit."
fi
git push --force origin main
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
