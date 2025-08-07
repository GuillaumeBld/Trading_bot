# GitHub Auto-Deploy Guide for Hostinger VPS

## Overview

This guide sets up automatic deployment from your GitHub repository to your Hostinger VPS, so changes you make to your code automatically appear on your live trading bot.

## 🚀 Quick Setup

### Method 1: Automatic Setup Script

Run this **single command** on your Hostinger VPS:

```bash
wget https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/setup_auto_updates.sh && chmod +x setup_auto_updates.sh && ./setup_auto_updates.sh
```

### Method 2: Manual Setup

If you prefer to set it up manually:

```bash
# 1. Download the auto-update script
cd /opt/trading-bot
wget https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/auto_update_deployment.sh
chmod +x auto_update_deployment.sh

# 2. Create manual update command
sudo ln -s /opt/trading-bot/auto_update_deployment.sh /usr/local/bin/update-trading-bot

# 3. Test the update system
update-trading-bot
```

## 🔄 How Auto-Updates Work

### Workflow:
1. **You push changes** to GitHub (`git push origin main`)
2. **Auto-update script detects changes** (via cron job or manual trigger)
3. **Script pulls latest code** (`git pull origin main`)
4. **Dependencies are updated** (`pip install -r requirements.txt`)
5. **Services restart automatically** (`supervisorctl restart trading_bot`)
6. **Your live bot is updated** at `http://82.25.112.7:8501`

### Update Frequency Options:
- **Every 30 minutes** - For active development
- **Every hour** - Balanced approach
- **Every 6 hours** - Conservative updates
- **Daily at 2 AM** - Minimal disruption
- **Manual only** - Full control

## 🛠️ Manual Update Commands

### Immediate Update
```bash
# Run update right now
update-trading-bot
```

### Check for Updates (No Action)
```bash
cd /opt/trading-bot
git fetch origin
git status
```

### View Update Logs
```bash
tail -f /var/log/trading_bot_updates.log
```

## 📋 Update Process Details

### What Gets Updated:
✅ **Python code changes** (new features, bug fixes)  
✅ **Configuration files** (settings, constants)  
✅ **Templates and assets** (HTML, CSS, images)  
✅ **Dependencies** (requirements.txt changes)  
✅ **n8n workflows** (if stored in repo)  

### What's Preserved:
✅ **Local configuration** (environment variables)  
✅ **Log files** (trading history, error logs)  
✅ **Virtual environment** (recreated only if needed)  
✅ **Service configuration** (supervisor settings)  

## 🔧 Advanced Configuration

### Custom Update Schedule

Edit the cron job for custom timing:

```bash
# Edit cron jobs
crontab -e

# Example: Update every 15 minutes during trading hours (9 AM - 4 PM EST)
*/15 9-16 * * 1-5 cd /opt/trading-bot && ./auto_update_deployment.sh >> /var/log/trading_bot_updates.log 2>&1
```

### Pre/Post Update Hooks

Create custom scripts that run before/after updates:

```bash
# Pre-update hook (runs before git pull)
echo '#!/bin/bash
echo "Backing up current configuration..."
cp -r config/ config.backup/' > /opt/trading-bot/pre-update.sh

# Post-update hook (runs after restart)
echo '#!/bin/bash
echo "Sending notification that update completed..."
curl -X POST webhook-url -d "Trading bot updated successfully"' > /opt/trading-bot/post-update.sh

chmod +x /opt/trading-bot/*.sh
```

### Rollback Capability

If an update causes issues:

```bash
# View recent commits
cd /opt/trading-bot
git log --oneline -5

# Rollback to previous version
git reset --hard HEAD~1
sudo supervisorctl restart trading_bot

# Or rollback to specific commit
git reset --hard COMMIT_HASH
sudo supervisorctl restart trading_bot
```

## 🚨 Troubleshooting

### Update Failed
```bash
# Check what went wrong
tail /var/log/trading_bot_updates.log

# Manual intervention
cd /opt/trading-bot
git status
git stash  # Save local changes
git pull origin main
sudo supervisorctl restart trading_bot
```

### Service Won't Start
```bash
# Check service status
sudo supervisorctl status trading_bot

# View service logs
sudo supervisorctl tail trading_bot

# Manual restart
sudo supervisorctl restart trading_bot
```

### Dependency Issues
```bash
# Force reinstall dependencies
cd /opt/trading-bot
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
sudo supervisorctl restart trading_bot
```

## 📊 Monitoring Updates

### Dashboard Integration

Add update status to your trading bot dashboard:

```python
# Add to your Streamlit app
import subprocess
import datetime

def get_last_update():
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=short'], 
            cwd='/opt/trading-bot',
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()
    except:
        return "Unknown"

# Display in sidebar
st.sidebar.info(f"Last update: {get_last_update()}")
```

### Update Notifications

Send notifications when updates complete:

```bash
# Add to post-update hook
curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
  -d "chat_id=$CHAT_ID" \
  -d "text=🚀 Trading bot updated successfully at $(date)"
```

## 🔐 Security Considerations

### GitHub Access
- **Public repos**: No authentication needed
- **Private repos**: Set up SSH keys or access tokens

### Update Safety
- **Test changes locally** before pushing to main
- **Use feature branches** for experimental code
- **Monitor logs** after updates
- **Have rollback plan** ready

### Backup Strategy
```bash
# Create backup before updates
mkdir -p /opt/backups
tar -czf "/opt/backups/trading-bot-$(date +%Y%m%d_%H%M%S).tar.gz" /opt/trading-bot
```

## 🎯 Best Practices

### Development Workflow
1. **Develop locally** and test thoroughly
2. **Push to GitHub** (`git push origin main`)
3. **Wait for auto-update** (or trigger manually)
4. **Verify update** at `http://82.25.112.7:8501`
5. **Monitor logs** for any issues

### Production Safety
- **Use separate branches** for development vs production
- **Test updates** during low-traffic periods
- **Monitor performance** after updates
- **Keep backups** of working versions

This system gives you **continuous deployment** capabilities, making your trading bot always up-to-date with your latest code changes!