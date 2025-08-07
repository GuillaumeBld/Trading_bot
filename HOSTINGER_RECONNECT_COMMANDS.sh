#!/bin/bash

# Hostinger VPS Reconnection and Persistent Setup Commands
# Run these commands after logging back into your Hostinger VPS

echo "🔐 Logged back into Hostinger VPS - Setting up persistent services"
echo "=================================================================="

# Step 1: Check system status
echo "📊 Checking system status..."
uptime
free -h
df -h

# Step 2: Download the latest setup scripts
echo "📥 Downloading latest setup scripts from GitHub..."
cd /root
wget https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/setup_supervisor.sh
wget https://raw.githubusercontent.com/GuillaumeBld/Trading_bot/main/HOSTINGER_SUPERVISOR_SETUP.md

# Make the script executable
chmod +x setup_supervisor.sh

# Step 3: Run the supervisor setup
echo "🚀 Running Supervisor setup for persistent hosting..."
./setup_supervisor.sh

# Step 4: Check if trading bot is already installed
if [ -d "/opt/trading-bot" ]; then
    echo "✅ Trading bot directory found at /opt/trading-bot"
    cd /opt/trading-bot
    
    # Activate virtual environment and check status
    source venv/bin/activate
    pip list | grep streamlit
    
    # Start the supervisor service for trading bot
    echo "▶️ Starting trading bot service with Supervisor..."
    sudo supervisorctl start trading_bot
    sudo supervisorctl status
    
else
    echo "🔧 Trading bot not found - running full installation..."
    
    # Clone the repository if not exists
    cd /opt
    git clone https://github.com/GuillaumeBld/Trading_bot.git trading-bot
    cd trading-bot
    
    # Set up Python environment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Run initial setup
    python3 setup.py install
    
    # Start supervisor service
    sudo supervisorctl start trading_bot
    sudo supervisorctl status
fi

# Step 5: Check service status and URLs
echo "🌐 Checking service status and access URLs..."
sudo supervisorctl status
sudo systemctl status nginx

echo ""
echo "🎉 Setup Complete!"
echo "==================="
echo "Your trading bot should now be running persistently at:"
echo "• Direct Access: http://82.25.112.7:8501"
echo "• Via Nginx: http://82.25.112.7"
echo ""
echo "To check logs: sudo supervisorctl tail trading_bot"
echo "To restart: sudo supervisorctl restart trading_bot"
echo "To stop: sudo supervisorctl stop trading_bot"
echo ""
echo "The service will automatically restart if it crashes or if the VPS reboots."