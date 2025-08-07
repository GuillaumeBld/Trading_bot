# Hostinger VPS Supervisor Setup for Trading Bot

## Problem: Connection Drops and App Not Persistent

Your trading bot is working but the connection drops because Streamlit is running in foreground mode. When you disconnect from SSH or the terminal session ends, the app stops. **Supervisor** is the solution to run your app as a persistent background service.

## Solution: Install and Configure Supervisor

### Step 1: Install Supervisor on Hostinger VPS

Connect to your VPS and run:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install supervisor
sudo apt install supervisor -y

# Enable and start supervisor
sudo systemctl enable supervisor
sudo systemctl start supervisor

# Check supervisor status
sudo systemctl status supervisor
```

### Step 2: Create Supervisor Configuration for Trading Bot

Create a supervisor configuration file:

```bash
sudo nano /etc/supervisor/conf.d/trading_bot.conf
```

Add the following configuration:

```ini
[program:trading_bot]
command=/bin/bash -c "cd /opt/trading-bot && source venv/bin/activate && streamlit run test_trading_bot.py --server.port=8501 --server.address=0.0.0.0 --server.fileWatcherType=none --browser.gatherUsageStats=false"
directory=/opt/trading-bot
autostart=true
autorestart=true
startsecs=10
startretries=3
user=root
redirect_stderr=true
stdout_logfile=/var/log/trading_bot.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=3
stderr_logfile=/var/log/trading_bot_error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=3
environment=PATH="/opt/trading-bot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

### Step 3: Configure Supervisor for Main Dashboard

Create another configuration for the main dashboard:

```bash
sudo nano /etc/supervisor/conf.d/trading_dashboard.conf
```

Add this configuration:

```ini
[program:trading_dashboard]
command=/bin/bash -c "cd /opt/trading-bot && source venv/bin/activate && python scripts/run_dashboard.py"
directory=/opt/trading-bot
autostart=false
autorestart=true
startsecs=10
startretries=3
user=root
redirect_stderr=true
stdout_logfile=/var/log/trading_dashboard.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=3
stderr_logfile=/var/log/trading_dashboard_error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=3
environment=PATH="/opt/trading-bot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
priority=200
```

### Step 4: Reload Supervisor and Start Services

```bash
# Reload supervisor configuration
sudo supervisorctl reread

# Update supervisor with new configurations
sudo supervisorctl update

# Start the trading bot service
sudo supervisorctl start trading_bot

# Check status
sudo supervisorctl status
```

## Managing Your Trading Bot Services

### Basic Supervisor Commands

```bash
# Check all services status
sudo supervisorctl status

# Start a service
sudo supervisorctl start trading_bot

# Stop a service
sudo supervisorctl stop trading_bot

# Restart a service
sudo supervisorctl restart trading_bot

# View logs in real-time
sudo tail -f /var/log/trading_bot.log

# View error logs
sudo tail -f /var/log/trading_bot_error.log

# Enter supervisor interactive mode
sudo supervisorctl
```

### Interactive Supervisor Session

```bash
sudo supervisorctl
# Inside supervisor shell:
supervisor> status
supervisor> start trading_bot
supervisor> stop trading_bot
supervisor> restart trading_bot
supervisor> tail trading_bot
supervisor> exit
```

## Configure Firewall for Web Access

```bash
# Allow HTTP traffic
sudo ufw allow 80

# Allow HTTPS traffic
sudo ufw allow 443

# Allow Streamlit port
sudo ufw allow 8501

# Enable firewall
sudo ufw enable

# Check firewall status
sudo ufw status
```

## Setting Up Nginx Reverse Proxy (Optional)

For production use, set up Nginx to serve your app on port 80:

```bash
# Install nginx
sudo apt install nginx -y

# Create nginx configuration
sudo nano /etc/nginx/sites-available/trading_bot
```

Add this Nginx configuration:

```nginx
server {
    listen 80;
    server_name 82.25.112.7;  # Your VPS IP

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable the Nginx site:

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/trading_bot /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## Health Check Script (Optional)

Create a health check script to ensure your app stays responsive:

```bash
sudo nano /opt/trading-bot/health_check.py
```

Add this health check script:

```python
#!/usr/bin/env python3
import requests
import os
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/trading_bot_health.log'),
        logging.StreamHandler()
    ]
)

APP_URL = "http://127.0.0.1:8501"

def check_health():
    try:
        response = requests.get(APP_URL, timeout=10)
        if response.status_code == 200:
            logging.info("Trading bot is healthy")
            return True
        else:
            logging.warning(f"Trading bot returned status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return False

def restart_service():
    logging.info("Restarting trading bot service...")
    os.system("supervisorctl restart trading_bot")

if __name__ == "__main__":
    while True:
        if not check_health():
            restart_service()
        time.sleep(60)  # Check every minute
```

Make it executable and create a supervisor config for it:

```bash
chmod +x /opt/trading-bot/health_check.py

sudo nano /etc/supervisor/conf.d/trading_bot_health.conf
```

Add health check configuration:

```ini
[program:trading_bot_health]
command=/opt/trading-bot/venv/bin/python /opt/trading-bot/health_check.py
directory=/opt/trading-bot
autostart=true
autorestart=true
user=root
redirect_stderr=true
stdout_logfile=/var/log/trading_bot_health.log
stderr_logfile=/var/log/trading_bot_health_error.log
```

## Troubleshooting

### Common Issues and Solutions

1. **Service won't start:**
   ```bash
   # Check logs
   sudo tail -f /var/log/trading_bot_error.log
   
   # Check supervisor logs
   sudo tail -f /var/log/supervisor/supervisord.log
   ```

2. **Permission issues:**
   ```bash
   # Fix ownership
   sudo chown -R root:root /opt/trading-bot
   
   # Fix permissions
   sudo chmod +x /opt/trading-bot/venv/bin/python
   ```

3. **Virtual environment issues:**
   ```bash
   # Recreate virtual environment
   cd /opt/trading-bot
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Checking Service Status

```bash
# Check if supervisor is running
sudo systemctl status supervisor

# Check trading bot process
ps aux | grep streamlit

# Check network connections
netstat -tlnp | grep 8501

# Check logs
sudo tail -f /var/log/trading_bot.log
```

## Final Steps

1. **Start your trading bot service:**
   ```bash
   sudo supervisorctl start trading_bot
   ```

2. **Verify it's running:**
   ```bash
   sudo supervisorctl status
   ```

3. **Access your app:**
   - Direct access: `http://82.25.112.7:8501`
   - With Nginx: `http://82.25.112.7`

4. **Monitor logs:**
   ```bash
   sudo tail -f /var/log/trading_bot.log
   ```

## Benefits of This Setup

✅ **Persistent service** - Runs even when you disconnect from SSH
✅ **Auto-restart** - Automatically restarts if the app crashes
✅ **Logging** - All output captured in log files
✅ **Process management** - Easy start/stop/restart controls
✅ **Boot persistence** - Starts automatically when server reboots
✅ **Resource monitoring** - Can track CPU/memory usage
✅ **Professional setup** - Production-ready configuration

Your trading bot will now run persistently on your Hostinger VPS and survive disconnections, crashes, and server reboots!