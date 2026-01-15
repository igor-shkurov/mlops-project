#!/bin/bash
# sync-pdfs.sh - Sync specific branch

BRANCH="igor"  # Change this
REPO_PATH="."
cd $REPO_PATH

# Fetch specific branch
git fetch origin $BRANCH

# Get local and remote commit hashes
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ $LOCAL != $REMOTE ]; then
    # Check for PDF changes in specific branch
    if git diff --name-only $LOCAL $REMOTE | grep -q "pdfs/.*\.pdf"; then
        echo "PDF changes detected on $BRANCH, pulling..."
        git pull origin $BRANCH
        docker-compose restart ingestion
    else
        echo "No PDF changes, just pulling..."
        git pull origin $BRANCH
    fi
fi