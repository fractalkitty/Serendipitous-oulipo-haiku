#!/bin/bash
# Hourly update script for haiku generation and site updates

echo "Starting hourly haiku update..."

# Go to scripts directory
cd "$(dirname "$0")"
echo "Working in: $(pwd)"

# Run the Python scripts
echo "Generating new haiku..."
python3 generate_haiku.py

echo "Updating archive..."
python3 update_archive.py

echo "Updating RSS feed..."
python3 update_rss.py

# Go back to project root
cd ..
echo "Back to project root: $(pwd)"

# Git operations
echo "Adding files to git..."
git add .

echo "Committing changes..."
git commit -m "Update haiku $(date +%Y-%m-%d\ %H:%M)"

echo "Pushing to remote..."
echo "Current time: $(date)"
echo "Git status before push:"
git status

# Try the push with full output
if git push origin main 2>&1; then
    echo "Push successful at $(date)"
else
    echo "Push failed at $(date) with exit code $?"
    echo "Git status after failed push:"
    git status
    echo "Network test:"
    ping -c 1 github.com
fi

echo "Hourly update complete!"

echo "Repository status:"
git status --porcelain