#!/bin/bash
# Push current Replit state to GitHub (AFTERSHOCK-TIERS)
set -e

# Ensure credentials are configured
echo "https://x-access-token:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
git config credential.helper store
git config user.email "aftershock@replit.com"
git config user.name "Aftershock Bot"

# Stage and commit any uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet || git ls-files --others --exclude-standard | grep -q .; then
    git add -A
    COMMIT_MSG="${1:-Update from Replit}"
    git commit -m "$COMMIT_MSG"
    echo "✅ Committed: $COMMIT_MSG"
else
    echo "ℹ️  Nothing new to commit."
fi

# Force-push to GitHub (Replit is the source of truth)
git push --force origin main
echo "✅ Pushed to GitHub: shadyy000777-commits/AFTERSHOCK-TIERS"
