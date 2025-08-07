#!/bin/bash

# Quick Hostinger Deployment Script for Trading Bot
# This script helps you deploy the trading bot to your Hostinger VPS

echo " Trading Bot - Hostinger Quick Setup"
echo "====================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}This script will help you deploy your trading bot to Hostinger VPS${NC}"
echo ""

# Step 1: Check if we're on the server or local machine
if [ -f "/etc/hostinger-release" ] || [ -f "/etc/ubuntu-release" ]; then
    echo -e "${GREEN} Detected you're on the server${NC}"
    SERVER_MODE=true
else
    echo -e "${YELLOW} Detected you're on local machine${NC}"
    SERVER_MODE=false
fi

if [ "$SERVER_MODE" = true ]; then
    echo ""
    echo " Setting up server environment..."
    
    # Install dependencies
    echo "Installing required packages..."
    sudo apt update
    sudo apt install -y unzip git python3 python3-pip python3-venv curl nano htop
    
    # Install Docker
    if ! command -v docker &> /dev/null; then
        echo "Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
    fi
    
    # Install Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Create project directory
    sudo mkdir -p /opt/trading-bot
    sudo chown $USER:$USER /opt/trading-bot
    cd /opt/trading-bot
    
    echo ""
    echo -e "${GREEN} Server setup complete!${NC}"
    echo ""
    echo " Next steps:"
    echo "1. Upload your trading bot files to /opt/trading-bot/"
    echo "2. Run: cd /opt/trading-bot && python3 -m venv venv"
    echo "3. Run: source venv/bin/activate"
    echo "4. Run: pip install -r requirements.txt"
    echo "5. Run: python setup.py"
    echo "6. Run: python scripts/run_dashboard.py"
    echo ""
    echo " You can upload files using:"
    echo "   - Hostinger File Manager (in your control panel)"
    echo "   - SCP: scp -r unified-trading-bot/ root@your-server:/opt/trading-bot/"
    echo "   - SFTP with tools like FileZilla"
    
else
    echo ""
    echo " Instructions for uploading from local machine:"
    echo ""
    echo "1. First, run this on your Hostinger server:"
    echo "   curl -O https://raw.githubusercontent.com/your-repo/unified-trading-bot/main/deploy-to-hostinger.sh"
    echo "   bash deploy-to-hostinger.sh"
    echo ""
    echo "2. Then upload your files using one of these methods:"
    echo ""
    echo "    SCP (recommended):"
    echo "   scp -r $(pwd)/unified-trading-bot root@YOUR-SERVER-IP:/opt/trading-bot/"
    echo ""
    echo "    RSYNC (faster for updates):"
    echo "   rsync -avz --progress $(pwd)/unified-trading-bot/ root@YOUR-SERVER-IP:/opt/trading-bot/"
    echo ""
    echo "    Hostinger File Manager:"
    echo "   - Login to your Hostinger control panel"
    echo "   - Go to File Manager"
    echo "   - Navigate to /opt/trading-bot/"
    echo "   - Upload and extract your files"
    
fi

echo ""
echo -e "${GREEN} Setup script completed!${NC}"