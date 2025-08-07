#!/bin/bash

# Setup Auto-Update System for Trading Bot on Hostinger VPS
# Run this script on your VPS to enable automatic updates

echo "🚀 Setting Up Auto-Update System for Trading Bot"
echo "================================================"

# 1. Copy the auto-update script to VPS
echo "📥 Downloading auto-update script..."
wget -O /opt/trading-bot/auto_update.sh https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/auto_update_deployment.sh

# Make it executable
chmod +x /opt/trading-bot/auto_update.sh

# 2. Create a manual update command
echo "🔧 Creating manual update command..."
sudo tee /usr/local/bin/update-trading-bot > /dev/null <<EOF
#!/bin/bash
cd /opt/trading-bot && ./auto_update.sh
EOF

sudo chmod +x /usr/local/bin/update-trading-bot

# 3. Set up automatic updates via cron (optional)
echo "⏰ Setting up automatic updates..."
echo "Choose your update frequency:"
echo "1) Every 30 minutes"
echo "2) Every hour" 
echo "3) Every 6 hours"
echo "4) Once daily at 2 AM"
echo "5) Manual only (no automatic updates)"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        CRON_SCHEDULE="*/30 * * * *"
        DESCRIPTION="every 30 minutes"
        ;;
    2)
        CRON_SCHEDULE="0 * * * *"
        DESCRIPTION="every hour"
        ;;
    3)
        CRON_SCHEDULE="0 */6 * * *"
        DESCRIPTION="every 6 hours"
        ;;
    4)
        CRON_SCHEDULE="0 2 * * *"
        DESCRIPTION="daily at 2 AM"
        ;;
    5)
        echo "✅ Manual updates only. Use 'update-trading-bot' command when needed."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Setting up manual only."
        exit 1
        ;;
esac

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE cd /opt/trading-bot && ./auto_update.sh >> /var/log/trading_bot_updates.log 2>&1") | crontab -

echo "✅ Automatic updates scheduled $DESCRIPTION"
echo ""
echo "📋 Setup Complete! Available Commands:"
echo "======================================"
echo "• Manual update: update-trading-bot"
echo "• View logs: tail -f /var/log/trading_bot_updates.log"  
echo "• Check cron jobs: crontab -l"
echo "• Remove auto-updates: crontab -r"
echo ""
echo "🎯 How It Works:"
echo "• Script checks GitHub for new commits"
echo "• Pulls changes if available"
echo "• Updates Python dependencies"
echo "• Restarts trading bot service"
echo "• Logs all activities"
echo ""
echo "🌐 Your bot will always be up-to-date at: http://82.25.112.7:8501"