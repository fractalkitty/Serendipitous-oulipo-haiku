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
git push origin main

echo "Hourly update complete!"
echo "Repository status:"
git status --porcelain