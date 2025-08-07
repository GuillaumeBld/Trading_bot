# Hostinger VPS Access with Google OAuth Login

## Problem
You're using Google OAuth to log into Hostinger but need to access your VPS terminal to set up the trading bot.

## Solution: Multiple Access Methods

### Method 1: Browser Terminal (EASIEST)

Hostinger provides a **Browser Terminal** feature that works with your OAuth login:

1. **Access hPanel**:
   - Go to [https://hpanel.hostinger.com](https://hpanel.hostinger.com)
   - Login with your **Google OAuth** (as usual)

2. **Navigate to Your VPS**:
   - Click **"VPS"** in the left sidebar
   - Click on your VPS server (srv850639)

3. **Open Browser Terminal**:
   - Click the **"Browser Terminal"** button
   - A new browser tab will open
   - Allow pop-ups if blocked by your browser

4. **Login to VPS**:
   - You'll see a login prompt: `srv850639 login:`
   - Enter: `root`
   - Enter the password (see Method 3 below to find it)

### Method 2: Reset Root Password

If you don't know your current root password:

1. **In hPanel** → **VPS** → **Your VPS** → **Settings**
2. **Find "Main settings" section**
3. **Locate "Root password"**
4. **Enter a new strong password** (12+ chars, uppercase, lowercase, number, symbol)
5. **Click "Update"**
6. **Wait for completion**: Check **"Backup & Monitoring"** → **"Latest Actions"**
7. **Look for "ct_set_rootpasswd" with "Success" status**

### Method 3: Find Current SSH Password

Your SSH credentials should be visible in hPanel:

1. **In hPanel** → **VPS** → **Your VPS** → **Overview**
2. **Look for "SSH Information" section**
3. **SSH password should be displayed**
4. **SSH username is usually: `root`**
5. **SSH IP**: `82.25.112.7`

## Step-by-Step: Complete Setup Process

### Step 1: Access Your VPS
Use **Method 1 (Browser Terminal)** - it's the easiest:

```bash
# Once you're logged into the browser terminal, you'll see:
root@srv850639:~# 
```

### Step 2: Run the Setup Commands

Copy and paste this command to download and run the setup:

```bash
wget https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/HOSTINGER_RECONNECT_COMMANDS.sh && chmod +x HOSTINGER_RECONNECT_COMMANDS.sh && ./HOSTINGER_RECONNECT_COMMANDS.sh
```

### Step 3: Alternative Manual Setup

If the script doesn't work, run these commands one by one:

```bash
# Check system status
uptime
df -h

# Install supervisor for persistent hosting
sudo apt update
sudo apt install supervisor nginx -y

# Download and install trading bot
cd /opt
git clone https://github.com/GuillaumeBld/Trading_bot.git trading-bot
cd trading-bot

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create supervisor configuration
sudo tee /etc/supervisor/conf.d/trading_bot.conf > /dev/null <<EOF
[program:trading_bot]
command=/bin/bash -c "cd /opt/trading-bot && source venv/bin/activate && streamlit run scripts/run_dashboard.py --server.port=8501 --server.address=0.0.0.0"
directory=/opt/trading-bot
user=root
autostart=true
autorestart=true
startsecs=10
startretries=3
stdout_logfile=/var/log/trading_bot.log
stderr_logfile=/var/log/trading_bot_error.log
environment=PATH="/opt/trading-bot/venv/bin"
EOF

# Start the service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start trading_bot
sudo supervisorctl status
```

### Step 4: Verify Setup

Check that everything is running:

```bash
# Check supervisor status
sudo supervisorctl status

# Check if the service is accessible
curl http://localhost:8501

# Check logs
sudo supervisorctl tail trading_bot
```

## Expected Results

After successful setup:
- ✅ Trading bot runs as persistent background service
- ✅ Accessible at `http://82.25.112.7:8501`
- ✅ Automatically restarts on crashes or reboots
- ✅ Survives SSH disconnections
- ✅ 24/7 availability

## Troubleshooting

### Browser Terminal Issues
- **Empty terminal**: Reboot VPS from hPanel, then retry
- **Pop-up blocked**: Allow pop-ups from `hpanel.hostinger.com`
- **Stuck on "starting serial terminal"**: Press Enter multiple times

### Password Issues
- **Don't know root password**: Use Method 2 to reset it
- **Password not working**: Try the password from hPanel SSH Information section
- **Still can't access**: Contact Hostinger support - they can help with OAuth accounts

### Service Issues
- **Service won't start**: Check logs with `sudo supervisorctl tail trading_bot`
- **Port conflicts**: Use `sudo netstat -tlnp | grep :8501` to check if port is used
- **Permission errors**: Make sure you're running as root user

## Important Notes

1. **No SSH Client Needed**: Browser terminal works entirely in your web browser
2. **OAuth Compatible**: This method works with Google OAuth login
3. **Persistent Service**: Once set up, your trading bot will run 24/7
4. **Auto-Recovery**: Service automatically restarts if it crashes
5. **Log Management**: All logs are saved and accessible via supervisor

This setup ensures your trading bot remains online even when you're not connected to the VPS!