#!/bin/bash
# Weekly git history squash to keep repo size manageable

echo "Starting weekly git history squash..."

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Create a fresh orphan branch
git checkout --orphan temp-squash-branch

# Add all current files
git add -A

# Commit everything as a single commit
git commit -m "Weekly squash: $(date +%Y-%m-%d) - $(git rev-list --count HEAD 2>/dev/null || echo 'many') commits compressed"

# Delete old branch and rename new one
git branch -D $CURRENT_BRANCH
git branch -m $CURRENT_BRANCH

# Force push to replace history
git push -f origin $CURRENT_BRANCH

echo "History squashed! Repo reset to single commit."
echo "Old history removed, poems.json preserved."