# 🤖 AI Agent Implementation Prompt - n8n Trading Bot Workflows

## Quick Start Prompt for AI Agent

**ROLE**: You are an expert n8n workflow automation specialist tasked with implementing comprehensive trading bot workflows.

**CONTEXT**: Complete ChatGPT Micro-Cap Trading Bot with FastAPI wrapper, Docker deployment, and n8n integration ready.

**OBJECTIVE**: Create production-ready n8n workflows for automated trading, risk management, and notifications.

---

## 🎯 IMMEDIATE TASKS

### **PRIORITY 1: Core Trading Automation**

1. **AI Trading Signal Processor** (Start Here)
   - Schedule: Every 5 minutes during market hours
   - Fetch AI analysis from `/api/ai/analyze`
   - Validate signals (confidence >0.7, risk checks)
   - Execute trades via `/api/trade/buy` or `/api/trade/sell`
   - Log results and send notifications

2. **Portfolio Risk Monitor**
   - Schedule: Every 1 minute
   - Monitor `/api/portfolio/performance`
   - Alert on drawdown >15%, position concentration >25%
   - Trigger risk reduction actions

3. **Multi-Channel Notifier**
   - Webhook trigger for all notifications
   - Support: Slack, Discord, Email, Telegram
   - Format messages per channel
   - Handle delivery failures

### **PRIORITY 2: Market Intelligence**

4. **News Sentiment Processor**
   - Fetch news from `/api/market/news`
   - Analyze sentiment impact on portfolio
   - Generate trading signals from news

5. **Market Condition Monitor**
   - Track major indices (SPY, QQQ, IWM, VIX)
   - Detect volatility spikes
   - Adjust trading parameters

---

## 🛠️ TECHNICAL SPECIFICATIONS

### **Available Services**
- **n8n**: http://localhost:5678 (admin/your-password)
- **Trading API**: http://localhost:8000 (Bearer token auth)
- **Database**: PostgreSQL on localhost:5432
- **Cache**: Redis on localhost:6379

### **API Endpoints to Use**
```bash
GET  /api/portfolio              # Current portfolio
GET  /api/portfolio/performance  # Performance metrics
POST /api/trade/buy             # Execute buy order
POST /api/trade/sell            # Execute sell order
POST /api/ai/analyze            # Get AI recommendations
GET  /api/market/data           # Market data
POST /api/webhooks/n8n          # Receive webhooks
```

### **Authentication**
```javascript
// In n8n HTTP Request nodes
Headers: {
  "Authorization": "Bearer {{$credentials.tradingBotAPI.apiKey}}",
  "Content-Type": "application/json"
}
```

---

## 📋 WORKFLOW TEMPLATES

### **Template 1: AI Trading Signal Processor**

```json
{
  "name": "AI Trading Signal Processor",
  "active": true,
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "value": 5}]
        }
      },
      "name": "Every 5 Minutes",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [240, 300]
    },
    {
      "parameters": {
        "url": "http://api-wrapper:8000/api/ai/analyze",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {"name": "provider", "value": "openai"},
            {"name": "include_market_data", "value": true}
          ]
        }
      },
      "name": "Get AI Analysis",
      "type": "n8n-nodes-base.httpRequest",
      "position": [460, 300]
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json.recommendations[0].confidence}}",
              "operation": "larger",
              "value2": 0.7
            }
          ]
        }
      },
      "name": "High Confidence Signal?",
      "type": "n8n-nodes-base.if",
      "position": [680, 300]
    }
  ]
}
```

### **Template 2: Risk Monitor**

```json
{
  "name": "Portfolio Risk Monitor",
  "active": true,
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "value": 1}]
        }
      },
      "name": "Every Minute",
      "type": "n8n-nodes-base.scheduleTrigger"
    },
    {
      "parameters": {
        "url": "http://api-wrapper:8000/api/portfolio/performance"
      },
      "name": "Get Portfolio Performance",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{Math.abs($json.performance_metrics.max_drawdown)}}",
              "operation": "larger",
              "value2": 0.15
            }
          ]
        }
      },
      "name": "Drawdown > 15%?",
      "type": "n8n-nodes-base.if"
    }
  ]
}
```

---

## 🚨 CRITICAL REQUIREMENTS

### **Error Handling**
Every workflow MUST include:
```javascript
// Error handling node
{
  "parameters": {
    "errorMessage": "Workflow failed: {{$json.error}}"
  },
  "name": "Error Handler",
  "type": "n8n-nodes-base.noOp"
}
```

### **Logging**
All actions MUST be logged:
```javascript
// Database logging
{
  "parameters": {
    "operation": "insert",
    "table": "workflow_logs",
    "columns": "timestamp, workflow_name, action, result, metadata"
  },
  "name": "Log Action",
  "type": "n8n-nodes-base.postgres"
}
```

### **Security**
- Store API keys in n8n credentials
- Verify webhook signatures
- Never log sensitive data
- Use HTTPS for all external calls

---

## 📊 SUCCESS CRITERIA

### **Functional Requirements**
- [ ] AI signals processed every 5 minutes
- [ ] Trades executed within 30 seconds of signal
- [ ] Risk alerts triggered within 1 minute
- [ ] 99.9% notification delivery rate
- [ ] Complete audit trail in database

### **Performance Requirements**
- [ ] <10 second workflow execution time
- [ ] <5MB memory usage per workflow
- [ ] Handle 100+ concurrent executions
- [ ] Zero data loss during failures

---

## 🔧 IMPLEMENTATION STEPS

### **Step 1: Environment Setup**
```bash
# Start the stack
cd n8n-integration
docker-compose -f docker/docker-compose.yml up -d

# Access n8n
open http://localhost:5678
```

### **Step 2: Create Credentials**
In n8n interface:
1. Go to Settings > Credentials
2. Add "HTTP Header Auth" credential
3. Name: "Trading Bot API"
4. Header: "Authorization"
5. Value: "Bearer your-api-key"

### **Step 3: Import Base Workflow**
1. Copy the JSON template above
2. Go to Workflows > Import from Clipboard
3. Paste and save
4. Configure all nodes
5. Test execution

### **Step 4: Expand and Customize**
- Add error handling to every node
- Implement comprehensive logging
- Add notification channels
- Test edge cases
- Optimize performance

---

## 🎯 START HERE

**IMMEDIATE ACTION**: 
1. Access n8n at http://localhost:5678
2. Import the "AI Trading Signal Processor" template
3. Configure API credentials
4. Test with a single execution
5. Add error handling and logging
6. Expand to full automation

**YOUR GOAL**: Create a production-ready trading automation system that can:
- Execute trades based on AI analysis
- Monitor risks continuously
- Send instant notifications
- Handle errors gracefully
- Scale to high-frequency trading

**TIME LIMIT**: Implement core workflows within 2 hours

🚀 **BEGIN IMPLEMENTATION NOW!**