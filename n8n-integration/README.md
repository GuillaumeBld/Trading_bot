# 🔗 n8n Integration for ChatGPT Micro-Cap Trading Bot

This folder contains everything needed to integrate the ChatGPT Micro-Cap Trading Bot with n8n workflows, including Docker deployment, API wrappers, and example workflows.

## 🎯 Overview

The integration allows you to:
- **Automate Trading Workflows** - Trigger trades based on external events
- **Send Notifications** - Alert via Slack, Discord, email, SMS
- **Data Pipeline** - Process and forward trading data
- **External Integrations** - Connect to brokers, news APIs, social media
- **Risk Management** - Automated monitoring and alerts
- **Reporting** - Generate and distribute trading reports

## 📁 Folder Structure

```
n8n-integration/
├── README.md                    # This file
├── workflows/                   # n8n workflow templates
│   ├── trading-alerts.json      # Trading notification workflows
│   ├── portfolio-monitoring.json # Portfolio tracking workflows
│   ├── news-sentiment.json      # News sentiment analysis
│   └── risk-management.json     # Risk monitoring workflows
├── docker/                      # Docker deployment files
│   ├── docker-compose.yml       # Complete stack deployment
│   ├── Dockerfile.trading-bot   # Trading bot container
│   ├── Dockerfile.api-wrapper   # API wrapper container
│   └── .env.example            # Environment variables template
├── api-wrapper/                 # FastAPI wrapper for n8n integration
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── routes/                 # API route definitions
│   └── requirements.txt        # API wrapper dependencies
├── examples/                    # Example integrations
│   ├── webhook-examples.py     # Webhook integration examples
│   ├── api-client.py          # API client examples
│   └── sample-workflows/       # Complete workflow examples
└── docs/                       # Detailed documentation
    ├── setup-guide.md          # Step-by-step setup
    ├── api-reference.md        # API documentation
    ├── workflow-templates.md   # Workflow explanations
    └── troubleshooting.md      # Common issues and solutions
```

## 🚀 Quick Start Options

### Option 1: Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment/n8n-integration

# Copy environment template
cp docker/.env.example docker/.env
# Edit docker/.env with your settings

# Start the complete stack
docker-compose -f docker/docker-compose.yml up -d

# Access n8n at http://localhost:5678
# Access trading bot API at http://localhost:8000
# Access trading dashboard at http://localhost:8502
```

### Option 2: Manual Setup
```bash
# 1. Start the trading bot with API wrapper
cd n8n-integration/api-wrapper
pip install -r requirements.txt
python main.py

# 2. Install and start n8n
npm install n8n -g
n8n start

# 3. Import workflows from workflows/ folder
```

### Option 3: Cloud Deployment
```bash
# Deploy to your preferred cloud provider
# See docs/cloud-deployment.md for specific instructions
```

## 🔧 Integration Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Trading Bot    │    │   API Wrapper   │    │      n8n        │
│                 │    │   (FastAPI)     │    │   Workflows     │
│ • Core Logic    │◄──►│                 │◄──►│                 │
│ • AI Trading    │    │ • REST API      │    │ • Notifications │
│ • Dashboard     │    │ • Webhooks      │    │ • Integrations  │
│ • Data Storage  │    │ • Event Stream  │    │ • Automation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  External APIs  │
                    │                 │
                    │ • Brokers       │
                    │ • News Sources  │
                    │ • Social Media  │
                    │ • Notifications │
                    └─────────────────┘
```

## 📊 Available Workflows

### 1. Trading Alerts (`workflows/trading-alerts.json`)
- **Triggers**: New trades, portfolio changes, performance milestones
- **Actions**: Slack/Discord notifications, email alerts, SMS
- **Use Case**: Stay informed about trading activity

### 2. Portfolio Monitoring (`workflows/portfolio-monitoring.json`)
- **Triggers**: Schedule-based or threshold-based
- **Actions**: Generate reports, update spreadsheets, send summaries
- **Use Case**: Regular portfolio performance tracking

### 3. News Sentiment Analysis (`workflows/news-sentiment.json`)
- **Triggers**: Market news, social media mentions
- **Actions**: Sentiment analysis, trading signals, alerts
- **Use Case**: News-driven trading decisions

### 4. Risk Management (`workflows/risk-management.json`)
- **Triggers**: Risk threshold breaches, market volatility
- **Actions**: Stop-loss execution, position sizing adjustments
- **Use Case**: Automated risk control

## 🛠️ API Endpoints

The API wrapper provides these endpoints for n8n integration:

### Portfolio Management
- `GET /api/portfolio` - Get current portfolio
- `GET /api/portfolio/performance` - Get performance metrics
- `POST /api/portfolio/refresh` - Refresh portfolio data

### Trading Operations
- `POST /api/trade/buy` - Execute buy order
- `POST /api/trade/sell` - Execute sell order
- `GET /api/trades/recent` - Get recent trades
- `GET /api/trades/history` - Get trade history

### Market Data
- `GET /api/market/data` - Get current market data
- `GET /api/market/news` - Get latest news
- `GET /api/market/sentiment` - Get market sentiment

### Notifications & Webhooks
- `POST /api/webhooks/register` - Register webhook
- `POST /api/webhooks/trigger` - Trigger webhook
- `GET /api/notifications` - Get notifications

### AI & Analysis
- `POST /api/ai/analyze` - Get AI trading recommendation
- `GET /api/ai/providers` - List available AI providers
- `POST /api/ai/configure` - Configure AI settings

## 🔔 Webhook Integration

### Receiving Webhooks from n8n
```python
# Trading bot receives webhooks from n8n workflows
@app.post("/webhooks/n8n/trade-signal")
async def handle_trade_signal(signal: TradeSignal):
    # Process trading signal from n8n
    result = await execute_trade(signal)
    return {"status": "success", "trade_id": result.id}
```

### Sending Webhooks to n8n
```python
# Trading bot sends events to n8n
async def notify_n8n(event_type: str, data: dict):
    webhook_url = "https://your-n8n.domain/webhook/trading-bot"
    await send_webhook(webhook_url, {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "data": data
    })
```

## 🐳 Docker Deployment

### Complete Stack
The `docker-compose.yml` includes:
- **Trading Bot** - Core application with dashboard
- **API Wrapper** - FastAPI service for n8n integration
- **n8n** - Workflow automation platform
- **PostgreSQL** - Database for n8n and trading data
- **Redis** - Caching and message queue
- **Nginx** - Reverse proxy and load balancer

### Environment Variables
```bash
# Trading Bot Configuration
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
TRADING_MODE=live  # or 'paper'

# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-password

# Database Configuration
POSTGRES_DB=trading_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WEBHOOK_SECRET=your-webhook-secret
```

## 🌐 Cloud Deployment Options

### Option 1: Railway
```bash
# Deploy to Railway
railway login
railway new
railway add postgresql
railway deploy
```

### Option 2: DigitalOcean App Platform
```bash
# Use the provided app.yaml configuration
doctl apps create --spec app.yaml
```

### Option 3: AWS ECS/Fargate
```bash
# Use the provided CloudFormation templates
aws cloudformation create-stack --template-body file://aws-deployment.yml
```

### Option 4: Google Cloud Run
```bash
# Deploy containers to Cloud Run
gcloud run deploy trading-bot --source .
gcloud run deploy n8n-workflows --source ./n8n-integration
```

## 📱 Mobile Integration

### Telegram Bot Integration
```javascript
// n8n workflow node for Telegram notifications
{
  "parameters": {
    "chatId": "your-chat-id",
    "text": "🚀 New trade executed: {{$json.symbol}} - {{$json.action}} {{$json.shares}} shares at ${{$json.price}}"
  }
}
```

### Discord Webhook
```javascript
// n8n workflow node for Discord notifications
{
  "parameters": {
    "webhookUri": "your-discord-webhook-url",
    "text": "📊 Portfolio Update: Total Value: ${{$json.total_value}} ({{$json.change_percent}}%)"
  }
}
```

## 🔐 Security Considerations

### API Security
- **Authentication**: JWT tokens or API keys
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all inputs
- **HTTPS Only**: Encrypt all communications

### Webhook Security
- **Signature Verification**: Verify webhook signatures
- **IP Whitelisting**: Restrict webhook sources
- **Payload Validation**: Validate webhook payloads
- **Secret Management**: Use environment variables

### Docker Security
- **Non-root Users**: Run containers as non-root
- **Network Isolation**: Use Docker networks
- **Secret Management**: Use Docker secrets
- **Image Scanning**: Scan for vulnerabilities

## 📈 Monitoring & Logging

### Application Monitoring
- **Health Checks**: API endpoint monitoring
- **Performance Metrics**: Response times, throughput
- **Error Tracking**: Exception monitoring
- **Resource Usage**: CPU, memory, disk usage

### Trading Monitoring
- **Trade Execution**: Success/failure rates
- **Portfolio Performance**: Real-time tracking
- **Risk Metrics**: Drawdown, volatility monitoring
- **AI Performance**: Model accuracy tracking

### n8n Workflow Monitoring
- **Execution Status**: Success/failure tracking
- **Performance**: Execution time monitoring
- **Error Handling**: Failed workflow notifications
- **Data Flow**: Input/output validation

## 🆘 Support & Troubleshooting

### Common Issues
1. **Connection Errors**: Check network connectivity and firewall settings
2. **Authentication Failures**: Verify API keys and credentials
3. **Webhook Timeouts**: Increase timeout settings
4. **Docker Issues**: Check container logs and resource allocation

### Getting Help
- **Documentation**: Check `docs/` folder for detailed guides
- **Examples**: Review `examples/` for working implementations
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions for community support

## 🎯 Next Steps

1. **Choose Deployment Method** - Docker Compose, manual, or cloud
2. **Configure Environment** - Set up API keys and settings
3. **Import Workflows** - Load example workflows into n8n
4. **Test Integration** - Verify webhook and API communication
5. **Customize Workflows** - Adapt examples to your needs
6. **Monitor & Optimize** - Set up monitoring and performance tracking

---

**Ready to automate your trading workflows with n8n?** 🚀

Start with the Docker Compose setup for the easiest deployment, then customize the workflows to match your trading strategy and notification preferences.