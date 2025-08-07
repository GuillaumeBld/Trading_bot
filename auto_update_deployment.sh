#!/bin/bash

# Auto-Update Trading Bot from GitHub
# This script pulls latest changes and restarts services

echo "🔄 Starting Auto-Update Process for Trading Bot"
echo "=============================================="

# Change to trading bot directory
cd /opt/trading-bot || {
    echo "❌ Error: Cannot find /opt/trading-bot directory"
    exit 1
}

# Check current git status
echo "📊 Current Status:"
git status --porcelain
echo ""

# Backup current local changes (if any)
echo "💾 Backing up any local changes..."
git stash push -m "Auto-backup before update $(date)"

# Fetch latest changes
echo "📥 Fetching latest changes from GitHub..."
git fetch origin

# Check if there are updates available
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Already up to date! No changes needed."
    echo "Current commit: $LOCAL"
    exit 0
fi

echo "🔄 Updates available! Pulling changes..."
echo "Current commit: $LOCAL"
echo "New commit: $REMOTE"

# Pull latest changes
git pull origin main

# Check if pull was successful
if [ $? -eq 0 ]; then
    echo "✅ Successfully pulled latest changes"
    
    # Activate virtual environment and update dependencies
    echo "📦 Updating Python dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    
    # Restart services using supervisor
    echo "🔄 Restarting trading bot services..."
    sudo supervisorctl restart trading_bot
    
    # Check if services are running
    sleep 5
    STATUS=$(sudo supervisorctl status trading_bot | grep RUNNING)
    
    if [ -n "$STATUS" ]; then
        echo "✅ Trading bot restarted successfully!"
        echo "🌐 Access your updated bot at: http://82.25.112.7:8501"
    else
        echo "❌ Warning: Service may not have started properly"
        echo "Check logs with: sudo supervisorctl tail trading_bot"
    fi
    
    # Log the update
    echo "$(date): Updated to commit $REMOTE" >> /var/log/trading_bot_updates.log
    
else
    echo "❌ Error during git pull. Check for conflicts."
    echo "Manual intervention may be required."
    exit 1
fi

echo ""
echo "🎉 Auto-update process completed!"
echo "=============================================="