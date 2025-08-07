# 🌐 Hostinger Deployment Guide for Trading Bot

## Overview

This guide will help you deploy the ChatGPT Micro-Cap Trading Bot to your Hostinger VPS/Cloud hosting account.

## Prerequisites

- Hostinger VPS or Cloud Hosting account
- SSH access to your server
- Domain name (optional)
- API keys for trading and AI services

## Deployment Options

### Option 1: VPS Deployment (Recommended)
Best for: Full control, Docker support, all features

### Option 2: Shared Hosting Deployment
Best for: Basic dashboard only, limited features

## VPS Deployment (Full Features)

### Step 1: Connect to Your VPS

```bash
# Connect via SSH (replace with your server details)
ssh root@your-server-ip
# or
ssh username@your-domain.com
```

### Step 2: Install Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y

# Install Python (if needed)
sudo apt install python3 python3-pip -y
```

### Step 3: Clone Repository

```bash
# Navigate to web directory
cd /var/www

# Clone the repository
git clone https://github.com/your-username/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment

# Set proper permissions
sudo chown -R $USER:$USER /var/www/chatgpt-microcap-experiment
```

### Step 4: Configure Environment

```bash
# Navigate to n8n integration
cd n8n-integration

# Copy environment template
cp docker/env.example docker/.env

# Edit environment variables
nano docker/.env
```

**Configure these essential variables:**

```bash
# AI Provider Settings
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Trading Settings
TRADING_MODE=paper
MAX_POSITION_SIZE=0.20

# Database Settings
POSTGRES_PASSWORD=your-secure-password
REDIS_PASSWORD=your-secure-password

# n8n Settings
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Security
JWT_SECRET_KEY=your-jwt-secret
WEBHOOK_SECRET=your-webhook-secret
API_KEY=your-api-key

# Domain Settings (if using domain)
N8N_WEBHOOK_URL=https://your-domain.com
N8N_EDITOR_BASE_URL=https://your-domain.com
```

### Step 5: Deploy with Docker

```bash
# Start the complete stack
docker-compose -f docker/docker-compose.yml up -d

# Check service status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f
```

### Step 6: Configure Nginx (Optional)

```bash
# Install Nginx
sudo apt install nginx -y

# Create site configuration
sudo nano /etc/nginx/sites-available/trading-bot
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Trading Dashboard
    location / {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # n8n Workflows
    location /n8n/ {
        proxy_pass http://localhost:5678/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Endpoints
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/trading-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: SSL Certificate (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Shared Hosting Deployment (Limited)

### Step 1: Upload Files

```bash
# Create deployment package locally
tar -czf trading-bot-shared.tar.gz src/ requirements.txt *.py

# Upload via FTP/SFTP to public_html/
```

### Step 2: Install Dependencies

```bash
# Connect via SSH to shared hosting
ssh username@your-domain.com

# Navigate to your directory
cd public_html/

# Extract files
tar -xzf trading-bot-shared.tar.gz

# Install Python packages (if pip available)
pip3 install --user -r requirements.txt
```

### Step 3: Configure for Shared Hosting

Create `app.py` for shared hosting:

```python
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables
os.environ['STREAMLIT_SERVER_PORT'] = '8000'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'

# Import and run
from src.interfaces.streamlit_app import main

if __name__ == "__main__":
    main()
```

## Testing Deployment

### Health Checks

```bash
# Check service health
curl http://your-domain.com/health
curl http://your-domain.com/api/health

# Check dashboard
curl -I http://your-domain.com

# Check n8n
curl -I http://your-domain.com/n8n/
```

### Service Status

```bash
# Check Docker containers
docker ps

# Check logs
docker-compose logs trading-bot
docker-compose logs api-wrapper
docker-compose logs n8n

# Check resource usage
docker stats
```

## Monitoring & Maintenance

### Log Monitoring

```bash
# Real-time logs
docker-compose logs -f

# Service-specific logs
docker-compose logs trading-bot
docker-compose logs n8n
docker-compose logs postgres
```

### Backup Strategy

```bash
# Create backup script
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/trading-bot"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec postgres pg_dump -U postgres trading_bot > $BACKUP_DIR/db_$DATE.sql

# Backup configuration
cp docker/.env $BACKUP_DIR/env_$DATE.backup

# Backup workflows
cp -r workflows/ $BACKUP_DIR/workflows_$DATE/

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.backup" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
chmod +x backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /var/www/chatgpt-microcap-experiment/backup.sh
```

### Updates

```bash
# Update repository
cd /var/www/chatgpt-microcap-experiment
git pull origin main

# Rebuild containers
docker-compose -f n8n-integration/docker/docker-compose.yml build
docker-compose -f n8n-integration/docker/docker-compose.yml up -d
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using ports
   sudo netstat -tulpn | grep :8502
   sudo netstat -tulpn | grep :5678
   
   # Kill conflicting processes
   sudo kill -9 $(sudo lsof -t -i:8502)
   ```

2. **Permission Issues**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER /var/www/chatgpt-microcap-experiment
   
   # Fix Docker permissions
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   free -m
   docker stats
   
   # Increase swap if needed
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Service URLs

After deployment, access:
- **Trading Dashboard**: `http://your-domain.com` or `http://your-ip:8502`
- **n8n Workflows**: `http://your-domain.com/n8n` or `http://your-ip:5678`
- **API Documentation**: `http://your-domain.com/api/docs` or `http://your-ip:8000/docs`

## Security Recommendations

1. **Firewall Configuration**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw allow https
   sudo ufw allow 8502  # Trading dashboard
   sudo ufw allow 5678  # n8n (if direct access needed)
   ```

2. **Regular Updates**
   ```bash
   # System updates
   sudo apt update && sudo apt upgrade -y
   
   # Docker updates
   docker-compose pull
   docker-compose up -d
   ```

3. **Access Control**
   - Use strong passwords
   - Enable 2FA where possible
   - Limit SSH access by IP
   - Regular security audits

## Support

If you encounter issues:
1. Check service logs: `docker-compose logs [service-name]`
2. Verify environment variables in `.env`
3. Check network connectivity
4. Review Hostinger documentation
5. Contact support if needed

---

**Your trading bot will be accessible at your domain/IP after successful deployment!** 🚀