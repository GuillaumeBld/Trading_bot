# 🌐 Hostinger Deployment - Step by Step

## 🚨 IMPORTANT SECURITY FIRST

**IMMEDIATELY** do this:
1. Go to your Hostinger dashboard
2. **Revoke/regenerate** the API key you shared (ttEsr2Kqk4V7CDMVVx0p6PcKiGECXR4gl1QgiJXu4fbc201f)
3. **Never share API keys** in public conversations again
4. Use the new API key for deployment

## 🎯 Quick Deployment (5 Minutes)

### Step 1: Connect to Your VPS
```bash
# SSH into your Hostinger VPS
ssh root@your-server-ip
# or if you have a username:
ssh username@your-domain.com
```

### Step 2: Upload and Deploy Your Code

#### Option A: Direct Upload (Recommended for now)
```bash
# Install required dependencies first
sudo apt update
sudo apt install -y unzip git python3 python3-pip python3-venv curl

# Create project directory
mkdir -p /opt/trading-bot
cd /opt/trading-bot

# Since you don't have a public GitHub repo yet, you'll need to upload your files
# You can use SCP, SFTP, or the Hostinger file manager
# For now, let's create the basic structure manually
```

#### Option B: Upload via SCP (from your local machine)
```bash
# From your local machine, upload the unified-trading-bot folder
scp -r /path/to/unified-trading-bot root@your-server-ip:/opt/trading-bot/

# Then SSH back to your server
ssh root@your-server-ip
cd /opt/trading-bot/unified-trading-bot
```

#### Option C: Use GitHub Repository (Recommended)
```bash
# Clone the repository directly to your server
git clone https://github.com/GuillaumeBld/Trading_bot.git /opt/trading-bot
cd /opt/trading-bot
```

**The script will automatically:**
- ✅ Install Docker, Docker Compose, Git, Python
- ✅ Clone the repository
- ✅ Set up environment variables
- ✅ Deploy all services (Trading Bot, n8n, Database)
- ✅ Configure Nginx reverse proxy
- ✅ Set up SSL certificate (optional)
- ✅ Configure firewall
- ✅ Set up monitoring and backups

### Step 3: Configure Your Settings

When prompted, enter:
- **Your OpenAI API Key**: `sk-your-new-openai-key`
- **Domain name** (if you have one): `your-domain.com`
- **SSL certificate**: Choose `y` for HTTPS

The script generates secure passwords automatically.

### Step 4: Access Your Services

After deployment:
- **Trading Dashboard**: `http://your-domain.com` or `http://your-ip:8502`
- **n8n Workflows**: `http://your-domain.com/n8n` or `http://your-ip:5678`
- **API Docs**: `http://your-domain.com/api/docs` or `http://your-ip:8000/docs`

## 🎛️ What You'll Have After Deployment

### 1. **Real-Time Trading Dashboard**
- Live portfolio monitoring
- Dynamic charts and metrics
- AI-powered recommendations
- Risk management alerts

### 2. **n8n Workflow Automation**
- Automated trading signals
- Multi-channel notifications (Slack, Discord, Email)
- Portfolio risk monitoring
- Market news analysis

### 3. **Complete API System**
- RESTful API for all trading functions
- Webhook support for external integrations
- Secure authentication
- Comprehensive documentation

### 4. **Production Infrastructure**
- PostgreSQL database
- Redis caching
- Nginx reverse proxy
- SSL certificates
- Automated backups
- Health monitoring

## 🔧 Manual Configuration (If Needed)

### If Automatic Script Doesn't Work:

1. **Install Dependencies Manually:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

2. **Clone and Deploy:**
```bash
# Clone repository
git clone https://github.com/your-username/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment

# Configure environment
cd n8n-integration
cp docker/env.example docker/.env
nano docker/.env  # Add your API keys

# Deploy services
docker-compose -f docker/docker-compose.yml up -d
```

## 🧪 Testing Your Deployment

### Health Checks:
```bash
# Test API
curl http://your-domain.com/api/health

# Test Dashboard
curl -I http://your-domain.com

# Check service status
docker-compose -f n8n-integration/docker/docker-compose.yml ps
```

### Expected Response:
- **API Health**: `{"status": "healthy", "services": {...}}`
- **Dashboard**: `200 OK` response
- **All Services**: Should show "Up" status

## 🔐 Security Setup

### 1. **Change Default Passwords**
```bash
# Edit environment file
nano n8n-integration/docker/.env

# Change these values:
N8N_BASIC_AUTH_PASSWORD=your-new-password
API_KEY=your-new-api-key
```

### 2. **Configure Firewall**
```bash
# Enable firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```

### 3. **Set Up SSL** (if you have a domain)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

## 📊 Using Your Trading Bot

### 1. **Access n8n Workflows**
- Go to: `http://your-domain.com/n8n`
- Login: `admin` / `your-password`
- Import workflows from the `workflows/` folder

### 2. **Configure Notifications**
- Set up Slack webhook
- Configure Discord notifications
- Add email SMTP settings
- Set up Telegram bot

### 3. **Start Trading**
- Add your OpenAI API key
- Configure risk parameters
- Enable AI trading signals
- Monitor performance

## 🆘 Troubleshooting

### Common Issues:

1. **Services Won't Start**
```bash
# Check logs
docker-compose -f n8n-integration/docker/docker-compose.yml logs

# Restart services
docker-compose -f n8n-integration/docker/docker-compose.yml restart
```

2. **Can't Access Dashboard**
```bash
# Check if port is open
sudo netstat -tulpn | grep :8502

# Check firewall
sudo ufw status
```

3. **Database Issues**
```bash
# Reset database
docker-compose -f n8n-integration/docker/docker-compose.yml down -v
docker-compose -f n8n-integration/docker/docker-compose.yml up -d
```

## 📞 Support

If you need help:
1. Check the logs: `docker-compose logs [service-name]`
2. Review the deployment guide: `deployment/hostinger-deployment-guide.md`
3. Check service status: `docker-compose ps`
4. Verify environment variables in `.env`

## 🎉 Success!

After successful deployment, you'll have:
- ✅ **Professional Trading Dashboard** with real-time updates
- ✅ **Automated n8n Workflows** for trading signals and alerts
- ✅ **Complete API System** for external integrations
- ✅ **Secure Infrastructure** with SSL and monitoring
- ✅ **Production-Ready Setup** with backups and health checks

**Your AI-powered trading bot is now live on Hostinger!** 🚀

---

**Next Steps:**
1. Configure your API keys and trading parameters
2. Set up notification channels (Slack, Discord, etc.)
3. Import and customize n8n workflows
4. Start with paper trading to test everything
5. Monitor performance and adjust as needed

**Happy Trading!** 📈🤖