# 🚀 n8n Integration Setup Guide

Complete step-by-step guide to set up the ChatGPT Micro-Cap Trading Bot with n8n workflows.

## 📋 Prerequisites

Before starting, ensure you have:

- **Docker & Docker Compose** installed
- **Git** for cloning the repository
- **API Keys** for AI providers (OpenAI, Anthropic, etc.)
- **Notification Service Accounts** (Slack, Discord, Telegram, etc.)
- **Basic understanding** of Docker and environment variables

## 🎯 Quick Start (Recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment/n8n-integration

# Copy environment template
cp docker/env.example docker/.env

# Edit environment variables
nano docker/.env  # or use your preferred editor
```

### 2. Configure Environment Variables

Edit `docker/.env` with your actual values:

```bash
# Essential Configuration
OPENAI_API_KEY=sk-your-openai-key-here
TRADING_MODE=paper
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
POSTGRES_PASSWORD=your-secure-db-password
```

### 3. Start the Stack

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check service status
docker-compose -f docker/docker-compose.yml ps
```

### 4. Access Services

- **n8n Workflows**: http://localhost:5678 (admin/your-password)
- **Trading Dashboard**: http://localhost:8502
- **API Documentation**: http://localhost:8000/docs
- **Basic Dashboard**: http://localhost:8501

## 🔧 Detailed Setup

### Step 1: Environment Configuration

#### Required API Keys

1. **OpenAI API Key**
   ```bash
   # Get from: https://platform.openai.com/api-keys
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **Anthropic API Key** (Optional)
   ```bash
   # Get from: https://console.anthropic.com
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **News API Key** (Optional)
   ```bash
   # Get from: https://newsapi.org
   NEWS_API_KEY=your-news-api-key
   ```

#### Notification Services

1. **Slack Integration**
   ```bash
   # Create Slack app at: https://api.slack.com/apps
   SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
   SLACK_CHANNEL=#trading-alerts
   ```

2. **Discord Webhook**
   ```bash
   # Create webhook in Discord server settings
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook
   ```

3. **Telegram Bot**
   ```bash
   # Create bot with @BotFather
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   TELEGRAM_CHAT_ID=your-chat-id
   ```

4. **Email Configuration**
   ```bash
   # Gmail example (use app password)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

#### Security Settings

```bash
# Generate secure passwords (32+ characters)
JWT_SECRET_KEY=$(openssl rand -base64 32)
WEBHOOK_SECRET=$(openssl rand -base64 16)
N8N_ENCRYPTION_KEY=$(openssl rand -base64 32)
POSTGRES_PASSWORD=$(openssl rand -base64 16)
REDIS_PASSWORD=$(openssl rand -base64 16)
```

### Step 2: Service Configuration

#### Database Setup

The PostgreSQL database is automatically configured with:
- Trading bot data storage
- n8n workflow storage
- User authentication data

#### Redis Configuration

Redis is used for:
- API response caching
- Background task queues
- Session storage

#### n8n Configuration

Key n8n settings:
```bash
# Authentication
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Webhook settings
N8N_WEBHOOK_URL=http://localhost:5678
N8N_EDITOR_BASE_URL=http://localhost:5678
```

### Step 3: Start Services

#### Using Docker Compose

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

#### Individual Service Control

```bash
# Start specific services
docker-compose -f docker/docker-compose.yml up -d postgres redis
docker-compose -f docker/docker-compose.yml up -d trading-bot
docker-compose -f docker/docker-compose.yml up -d api-wrapper
docker-compose -f docker/docker-compose.yml up -d n8n

# Restart a service
docker-compose -f docker/docker-compose.yml restart trading-bot
```

### Step 4: Import Workflows

#### Method 1: Auto-Import (Recommended)

Workflows are automatically imported from the `workflows/` directory when n8n starts.

#### Method 2: Manual Import

1. Access n8n at http://localhost:5678
2. Login with your credentials
3. Go to **Workflows** → **Import from File**
4. Select workflow JSON files from `workflows/` directory
5. Configure credentials for each workflow

### Step 5: Configure Credentials

#### In n8n Interface:

1. **API Credentials**
   - Name: `Trading Bot API`
   - Type: `HTTP Header Auth`
   - Header: `Authorization`
   - Value: `Bearer your-api-key`

2. **Slack Credentials**
   - Name: `Slack Bot`
   - Type: `Slack API`
   - Access Token: `your-slack-bot-token`

3. **Discord Webhook**
   - Name: `Discord Alerts`
   - Type: `Discord Webhook`
   - Webhook URL: `your-discord-webhook-url`

4. **Email Credentials**
   - Name: `Email Alerts`
   - Type: `SMTP`
   - Host: `smtp.gmail.com`
   - Port: `587`
   - Username: `your-email@gmail.com`
   - Password: `your-app-password`

## 🧪 Testing the Setup

### 1. Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check trading bot status
curl http://localhost:8501/_stcore/health

# Check n8n status
curl http://localhost:5678/healthz
```

### 2. Test Webhook

```bash
# Send test webhook to n8n
curl -X POST http://localhost:5678/webhook/trading-bot-alerts \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=your-signature" \
  -d '{
    "event_type": "trade_executed",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "data": {
      "symbol": "AAPL",
      "action": "buy",
      "shares": 10,
      "price": 150.00,
      "reasoning": "Test trade execution"
    }
  }'
```

### 3. Test API Endpoints

```bash
# Get portfolio data
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/api/portfolio

# Get market data
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:8000/api/market/data?symbols=AAPL,GOOGL

# Execute test trade
curl -X POST http://localhost:8000/api/trade/buy \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "shares": 1,
    "price": 150.00,
    "action": "buy"
  }'
```

## 🔧 Advanced Configuration

### Custom Workflows

1. **Create New Workflow**
   - Open n8n interface
   - Click **+ New Workflow**
   - Add nodes and configure connections
   - Save and activate

2. **Workflow Templates**
   - Use provided templates as starting points
   - Customize notification formats
   - Add custom logic nodes
   - Integrate external services

### Performance Tuning

#### Database Optimization

```yaml
# In docker-compose.yml
postgres:
  command: postgres -c max_connections=200 -c shared_buffers=256MB
  deploy:
    resources:
      limits:
        memory: 1G
      reservations:
        memory: 512M
```

#### API Scaling

```yaml
# Scale API wrapper
api-wrapper:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '1.0'
        memory: 512M
```

### SSL/HTTPS Setup

1. **Generate SSL Certificates**
   ```bash
   # Self-signed certificate (development)
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout docker/ssl/key.pem \
     -out docker/ssl/cert.pem
   ```

2. **Configure Nginx**
   ```nginx
   # In docker/nginx.conf
   server {
       listen 443 ssl;
       ssl_certificate /etc/nginx/ssl/cert.pem;
       ssl_certificate_key /etc/nginx/ssl/key.pem;
   }
   ```

## 🔍 Monitoring & Logging

### Enable Monitoring Stack

```bash
# Start with monitoring
docker-compose -f docker/docker-compose.yml --profile monitoring up -d

# Access monitoring
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### Log Management

```bash
# View service logs
docker-compose -f docker/docker-compose.yml logs trading-bot
docker-compose -f docker/docker-compose.yml logs api-wrapper
docker-compose -f docker/docker-compose.yml logs n8n

# Follow logs in real-time
docker-compose -f docker/docker-compose.yml logs -f --tail=100
```

### Health Monitoring

```bash
# Check all service health
docker-compose -f docker/docker-compose.yml ps

# Detailed service inspection
docker inspect trading-bot-core
docker stats trading-bot-core
```

## 🚨 Troubleshooting

### Common Issues

#### Services Won't Start

```bash
# Check Docker daemon
systemctl status docker

# Check port conflicts
netstat -tulpn | grep :5678
netstat -tulpn | grep :8000

# Check disk space
df -h

# Check memory usage
free -m
```

#### Database Connection Issues

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Test database connection
docker-compose exec postgres psql -U postgres -d trading_bot -c "\l"

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### n8n Workflow Issues

1. **Check Credentials**
   - Verify all credentials are properly configured
   - Test API connections manually

2. **Webhook Issues**
   - Verify webhook URLs are accessible
   - Check webhook signatures
   - Review n8n execution logs

3. **Notification Failures**
   - Test notification services individually
   - Check service API limits
   - Verify authentication tokens

#### API Connection Issues

```bash
# Test API connectivity
curl -v http://localhost:8000/health

# Check API logs
docker-compose logs api-wrapper

# Verify API key authentication
curl -H "Authorization: Bearer wrong-key" http://localhost:8000/api/portfolio
```

### Performance Issues

1. **Slow Response Times**
   - Monitor resource usage
   - Check database query performance
   - Review API rate limits

2. **Memory Issues**
   - Increase container memory limits
   - Monitor memory leaks
   - Optimize data caching

3. **Network Issues**
   - Check Docker network configuration
   - Verify service discovery
   - Test inter-container communication

## 📞 Support

### Getting Help

1. **Check Documentation**
   - Review all documentation files
   - Check API reference
   - Review workflow templates

2. **Debug Information**
   ```bash
   # Collect debug information
   docker-compose -f docker/docker-compose.yml config
   docker-compose -f docker/docker-compose.yml ps
   docker-compose -f docker/docker-compose.yml logs --no-color > debug.log
   ```

3. **Community Support**
   - GitHub Issues for bug reports
   - GitHub Discussions for questions
   - Stack Overflow for technical issues

### Best Practices

1. **Security**
   - Use strong passwords
   - Regularly rotate API keys
   - Keep services updated
   - Monitor access logs

2. **Backup**
   - Regular database backups
   - Configuration file backups
   - Workflow export backups

3. **Maintenance**
   - Monitor service health
   - Update Docker images
   - Clean up old logs
   - Review and optimize workflows

---

**Your n8n integration is now ready!** 🎉

Access your services and start automating your trading workflows with the power of n8n and AI-driven trading decisions.