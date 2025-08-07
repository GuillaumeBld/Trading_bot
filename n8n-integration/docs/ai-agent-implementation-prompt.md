#  AI Agent Implementation Prompt for n8n Trading Bot Workflows

## System Context

You are an expert AI agent specializing in n8n workflow automation and trading system integration. Your task is to implement comprehensive n8n workflows for the ChatGPT Micro-Cap Trading Bot system.

## Project Overview

**System**: ChatGPT Micro-Cap Trading Bot with n8n Integration
**Repository**: Available on GitHub with complete Docker deployment
**Architecture**: Trading Bot + FastAPI Wrapper + n8n + PostgreSQL + Redis
**Goal**: Create intelligent, automated trading workflows with multi-channel notifications and risk management

## Available Resources

### 1. **Complete Codebase Structure**
```
ChatGPT-Micro-Cap-Experiment-Rebuilt/
 src/                           # Core trading application
    core/                      # Trading logic and AI integration
    interfaces/                # Dashboards and user interfaces
    services/                  # Market data and real-time services
    config/                    # Configuration management
 n8n-integration/               # Your implementation target
    docker/                    # Complete Docker stack
    workflows/                 # Workflow templates (expand these)
    api-wrapper/               # FastAPI service for integration
    docs/                      # Implementation guides
    examples/                  # Code examples and patterns
 [other directories...]
```

### 2. **Available API Endpoints**
- **Portfolio**: `GET /api/portfolio`, `GET /api/portfolio/performance`
- **Trading**: `POST /api/trade/buy`, `POST /api/trade/sell`
- **Market Data**: `GET /api/market/data`, `GET /api/market/news`
- **AI Analysis**: `POST /api/ai/analyze`, `GET /api/ai/providers`
- **Webhooks**: `POST /api/webhooks/n8n`
- **Notifications**: `POST /api/notifications/send`

### 3. **Docker Services Running**
- **n8n**: http://localhost:5678 (workflow platform)
- **Trading Bot API**: http://localhost:8000 (FastAPI wrapper)
- **Trading Dashboard**: http://localhost:8502 (real-time interface)
- **PostgreSQL**: localhost:5432 (data storage)
- **Redis**: localhost:6379 (caching/queuing)

## Implementation Requirements

### **Phase 1: Core Trading Workflows**  HIGH PRIORITY

#### 1.1 **Automated Trading Signal Processing**
Create workflows that:
- **Monitor AI Recommendations**: Poll `/api/ai/analyze` every 5 minutes
- **Validate Signals**: Check confidence scores, risk parameters, position limits
- **Execute Trades**: Call `/api/trade/buy` or `/api/trade/sell` based on AI analysis
- **Risk Management**: Implement stop-loss, position sizing, maximum daily trades
- **Logging**: Record all decisions and executions in PostgreSQL

**Expected Workflow Nodes**:
- Schedule Trigger (every 5 minutes)
- HTTP Request (AI analysis)
- IF conditions (signal validation)
- HTTP Request (trade execution)
- Database operations (logging)
- Error handling and notifications

#### 1.2 **Portfolio Monitoring & Alerts**
Create workflows that:
- **Real-Time Monitoring**: Check portfolio performance every minute
- **Risk Thresholds**: Trigger alerts on drawdown >15%, volatility spikes, position concentration
- **Performance Tracking**: Calculate and store daily/weekly performance metrics
- **Rebalancing Alerts**: Suggest portfolio adjustments based on risk metrics

**Expected Workflow Nodes**:
- Schedule Trigger (every 1 minute)
- HTTP Request (portfolio data)
- Mathematical calculations (risk metrics)
- Multiple IF conditions (threshold checks)
- Database operations (metric storage)
- Webhook triggers (alert notifications)

#### 1.3 **Multi-Channel Notification System**
Create workflows that:
- **Trade Notifications**: Instant alerts on trade executions
- **Risk Alerts**: Immediate notifications for risk threshold breaches
- **Performance Reports**: Daily/weekly portfolio summaries
- **System Status**: Health checks and error notifications

**Supported Channels**:
- Slack (trading channel)
- Discord (webhook integration)
- Email (SMTP configuration)
- Telegram (bot integration)
- SMS (Twilio integration)

### **Phase 2: Advanced Market Intelligence**  MEDIUM PRIORITY

#### 2.1 **News & Sentiment Analysis Workflow**
- **News Aggregation**: Collect news from multiple sources every 15 minutes
- **Sentiment Analysis**: Process news sentiment using AI providers
- **Impact Assessment**: Correlate news with portfolio positions
- **Trading Signals**: Generate buy/sell signals based on sentiment shifts
- **Alert Generation**: Notify on significant news affecting holdings

#### 2.2 **Market Condition Monitoring**
- **Market Indices Tracking**: Monitor SPY, QQQ, IWM, VIX every 5 minutes
- **Volatility Analysis**: Detect market regime changes
- **Correlation Monitoring**: Track portfolio correlation with market indices
- **Risk Adjustment**: Automatically adjust position sizes based on market conditions

#### 2.3 **Economic Calendar Integration**
- **Event Monitoring**: Track earnings, economic releases, Fed announcements
- **Pre-Event Actions**: Adjust positions before high-impact events
- **Post-Event Analysis**: Analyze market reactions and portfolio impact
- **Strategy Adjustment**: Modify trading strategies based on event outcomes

### **Phase 3: Advanced Automation**  LOWER PRIORITY

#### 3.1 **Dynamic Strategy Adjustment**
- **Performance Analysis**: Evaluate strategy performance weekly
- **Parameter Optimization**: Adjust AI model parameters based on results
- **Strategy Switching**: Switch between conservative/aggressive modes
- **Backtesting Integration**: Test strategy changes on historical data

#### 3.2 **Social Media Integration**
- **Twitter Sentiment**: Monitor trading-related tweets and sentiment
- **Reddit Analysis**: Track relevant subreddits for market sentiment
- **Influencer Monitoring**: Track key trading personalities and their impact
- **Social Signal Generation**: Create trading signals from social sentiment

#### 3.3 **Advanced Risk Management**
- **Portfolio Optimization**: Implement Modern Portfolio Theory calculations
- **Stress Testing**: Run portfolio stress tests under various scenarios
- **Correlation Analysis**: Monitor and manage portfolio correlation risks
- **Dynamic Hedging**: Implement automated hedging strategies

## Technical Implementation Guidelines

### **Workflow Design Principles**

1. **Error Handling**: Every workflow must include comprehensive error handling
   ```
   HTTP Request → IF (Success) → Continue
                ↓ IF (Error)
                → Error Handler → Notification → Stop
   ```

2. **Logging**: All significant actions must be logged to PostgreSQL
   ```
   Action → Database Insert (timestamp, action, result, metadata)
   ```

3. **Rate Limiting**: Respect API rate limits and implement backoff strategies
   ```
   HTTP Request → IF (Rate Limited) → Wait → Retry (max 3 attempts)
   ```

4. **Security**: All API calls must include proper authentication
   ```
   Headers: Authorization: Bearer ${API_KEY}
   ```

### **Data Flow Patterns**

#### Pattern 1: **Scheduled Analysis & Action**
```
Schedule Trigger → Fetch Data → Analyze → Decide → Execute → Log → Notify
```

#### Pattern 2: **Event-Driven Response**
```
Webhook Trigger → Validate → Process → Respond → Log
```

#### Pattern 3: **Continuous Monitoring**
```
Schedule → Monitor → Compare Thresholds → Alert if Needed → Update State
```

### **Required Workflow Variables**

Set these in n8n workflow settings:
```json
{
  "API_BASE_URL": "http://api-wrapper:8000",
  "API_KEY": "your-api-key",
  "WEBHOOK_SECRET": "your-webhook-secret",
  "RISK_THRESHOLDS": {
    "max_drawdown": 0.15,
    "max_position_size": 0.25,
    "daily_trade_limit": 10
  },
  "NOTIFICATION_CHANNELS": {
    "slack_webhook": "https://hooks.slack.com/...",
    "discord_webhook": "https://discord.com/api/webhooks/...",
    "email_smtp": "smtp.gmail.com:587"
  }
}
```

## Specific Workflow Implementation Tasks

### **Task 1: Create "AI Trading Signal Processor" Workflow**

**Workflow Name**: `ai-trading-signal-processor`
**Trigger**: Schedule (every 5 minutes during market hours)
**Purpose**: Automatically execute trades based on AI analysis

**Implementation Steps**:
1. **Schedule Node**: Configure for market hours (9:30 AM - 4:00 PM EST)
2. **AI Analysis Request**: `GET /api/ai/analyze` with portfolio context
3. **Signal Validation**: Check confidence > 0.7, position limits, cash availability
4. **Trade Execution**: Call appropriate trade endpoint based on signal
5. **Result Logging**: Store execution results in database
6. **Notification**: Send trade confirmation to all channels
7. **Error Handling**: Comprehensive error catching and reporting

**Expected JSON Structure** (provide this):
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
      "type": "n8n-nodes-base.scheduleTrigger"
    },
    // ... additional nodes
  ],
  "connections": {
    // ... node connections
  }
}
```

### **Task 2: Create "Portfolio Risk Monitor" Workflow**

**Workflow Name**: `portfolio-risk-monitor`
**Trigger**: Schedule (every 1 minute)
**Purpose**: Continuous portfolio risk monitoring and alerting

**Implementation Requirements**:
- Real-time portfolio value tracking
- Drawdown calculation and alerting
- Position concentration monitoring
- Volatility spike detection
- Automatic risk report generation

### **Task 3: Create "Market News Processor" Workflow**

**Workflow Name**: `market-news-processor`
**Trigger**: Schedule (every 15 minutes)
**Purpose**: Process market news and generate trading insights

**Implementation Requirements**:
- News aggregation from multiple sources
- AI-powered sentiment analysis
- Portfolio impact assessment
- Signal generation based on news sentiment
- Integration with existing trading workflows

### **Task 4: Create "Multi-Channel Notifier" Workflow**

**Workflow Name**: `multi-channel-notifier`
**Trigger**: Webhook (called by other workflows)
**Purpose**: Unified notification system for all alerts

**Implementation Requirements**:
- Support for Slack, Discord, Email, Telegram
- Message formatting based on channel capabilities
- Priority-based routing
- Delivery confirmation and retry logic
- Rate limiting and throttling

## Quality Standards

### **Code Quality**
- All workflows must include detailed descriptions
- Node names must be descriptive and consistent
- Complex logic must be commented
- Error handling must be comprehensive
- Testing scenarios must be included

### **Performance Requirements**
- Workflows must complete within 30 seconds
- API calls must include timeout handling
- Database operations must be optimized
- Memory usage must be monitored
- Concurrent execution must be managed

### **Security Requirements**
- All API keys must be stored in n8n credentials
- Webhook signatures must be verified
- Sensitive data must not be logged
- Access controls must be implemented
- Audit trails must be maintained

## Testing & Validation

### **Required Tests**
1. **Unit Testing**: Test individual workflow nodes
2. **Integration Testing**: Test complete workflow execution
3. **Error Testing**: Test error handling scenarios
4. **Performance Testing**: Test under load conditions
5. **Security Testing**: Test authentication and authorization

### **Validation Criteria**
- All workflows execute without errors
- All notifications are delivered successfully
- All trades are executed correctly
- All data is logged properly
- All security measures are functional

## Deliverables

### **Primary Deliverables**
1. **Complete n8n Workflows**: JSON files for all required workflows
2. **Workflow Documentation**: Detailed documentation for each workflow
3. **Setup Instructions**: Step-by-step implementation guide
4. **Testing Procedures**: Comprehensive testing documentation
5. **Troubleshooting Guide**: Common issues and solutions

### **Secondary Deliverables**
1. **Performance Optimization Guide**: Best practices for workflow performance
2. **Security Hardening Guide**: Security recommendations and implementations
3. **Monitoring & Alerting Setup**: Workflow health monitoring
4. **Backup & Recovery Procedures**: Data protection strategies
5. **Scaling Guidelines**: How to handle increased load

## Success Metrics

### **Functional Metrics**
- 99.9% workflow execution success rate
- <5 second average response time for critical workflows
- 100% notification delivery rate
- Zero unauthorized access attempts
- Complete audit trail for all actions

### **Business Metrics**
- Improved trading performance through automation
- Reduced manual intervention requirements
- Faster response to market conditions
- Better risk management through continuous monitoring
- Enhanced decision-making through comprehensive data analysis

## Implementation Timeline

### **Week 1**: Core Trading Workflows
- Implement AI Trading Signal Processor
- Implement Portfolio Risk Monitor
- Basic notification system
- Initial testing and validation

### **Week 2**: Advanced Intelligence
- Market News Processor
- Enhanced notification system
- Performance optimization
- Security hardening

### **Week 3**: Advanced Features
- Economic calendar integration
- Social media monitoring
- Advanced risk management
- Comprehensive testing

### **Week 4**: Finalization
- Documentation completion
- Final testing and validation
- Performance tuning
- Deployment preparation

## Getting Started

### **Immediate Actions**
1. **Access n8n Interface**: http://localhost:5678
2. **Review API Documentation**: Check `/docs` endpoint
3. **Test API Connectivity**: Verify all endpoints are accessible
4. **Import Base Workflows**: Start with provided templates
5. **Configure Credentials**: Set up all required API keys and tokens

### **Development Environment**
- Use the provided Docker environment
- All services are pre-configured and running
- Database schemas are already created
- API endpoints are documented and tested
- Example code is provided for reference

## Support Resources

### **Documentation**
- Complete API reference at `/docs`
- Setup guide in `n8n-integration/docs/`
- Code examples in `n8n-integration/examples/`
- Troubleshooting guide available

### **Technical Support**
- All source code is available for reference
- Docker logs provide detailed debugging information
- Database can be queried directly for data analysis
- API endpoints can be tested independently

---

##  Your Mission

**Create a comprehensive, production-ready n8n workflow system that transforms the ChatGPT Micro-Cap Trading Bot into a fully automated, intelligent trading platform with real-time risk management, multi-channel notifications, and advanced market intelligence.**

**Start with the core trading workflows and expand systematically. Focus on reliability, security, and performance. Every workflow should be robust enough for production use with real money.**

**Remember: You're building a system that traders will depend on for their financial decisions. Quality, reliability, and security are paramount.**

 **Begin Implementation Now!**