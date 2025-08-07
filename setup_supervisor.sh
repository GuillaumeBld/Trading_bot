#!/bin/bash

# Hostinger VPS Supervisor Setup Script for Trading Bot
# Run this script on your Hostinger VPS to set up persistent services

echo "🚀 Setting up Supervisor for Trading Bot on Hostinger VPS"
echo "========================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install supervisor
echo "🔧 Installing Supervisor..."
sudo apt install supervisor nginx -y

# Enable and start supervisor
echo "▶️ Starting Supervisor service..."
sudo systemctl enable supervisor
sudo systemctl start supervisor

# Create trading bot supervisor configuration
echo "📝 Creating Supervisor configuration for Trading Bot..."
sudo tee /etc/supervisor/conf.d/trading_bot.conf > /dev/null <<EOF
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
EOF

# Create main dashboard supervisor configuration
echo "📝 Creating Supervisor configuration for Main Dashboard..."
sudo tee /etc/supervisor/conf.d/trading_dashboard.conf > /dev/null <<EOF
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
EOF

# Create Nginx configuration
echo "🌐 Setting up Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/trading_bot > /dev/null <<EOF
server {
    listen 80;
    server_name 82.25.112.7;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/trading_bot /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    sudo systemctl restart nginx
else
    echo "❌ Nginx configuration has errors"
fi

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8501
sudo ufw --force enable

# Fix permissions
echo "🔐 Setting up permissions..."
sudo chown -R root:root /opt/trading-bot
sudo chmod +x /opt/trading-bot/venv/bin/activate

# Reload supervisor configuration
echo "🔄 Reloading Supervisor configuration..."
sudo supervisorctl reread
sudo supervisorctl update

# Start the trading bot service
echo "🚀 Starting Trading Bot service..."
sudo supervisorctl start trading_bot

# Wait a moment for service to start
sleep 5

# Check status
echo "📊 Checking service status..."
sudo supervisorctl status

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📍 Your Trading Bot is now running as a persistent service!"
echo ""
echo "🔗 Access URLs:"
echo "   - Direct Streamlit: http://82.25.112.7:8501"
echo "   - Via Nginx: http://82.25.112.7"
echo ""
echo "📋 Useful Commands:"
echo "   - Check status: sudo supervisorctl status"
echo "   - View logs: sudo tail -f /var/log/trading_bot.log"
echo "   - Restart service: sudo supervisorctl restart trading_bot"
echo "   - Stop service: sudo supervisorctl stop trading_bot"
echo "   - Start service: sudo supervisorctl start trading_bot"
echo ""
echo "📁 Log Files:"
echo "   - App logs: /var/log/trading_bot.log"
echo "   - Error logs: /var/log/trading_bot_error.log"
echo "   - Supervisor logs: /var/log/supervisor/supervisord.log"
echo ""
echo "🔧 To manage services interactively:"
echo "   sudo supervisorctl"
echo ""
echo "✨ Your Trading Bot will now survive disconnections, crashes, and reboots!"